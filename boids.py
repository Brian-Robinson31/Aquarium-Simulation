import pygame
import math


class Boids:
    max_speed = 4
    max_force = 1
    perception = 60
    crowding = 30

    def __init__(self, x_pos, y_pos, x_velocity, y_velocity):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def separation(self, boids):
        steering = pygame.math.Vector2(0, 0)
        for boid in boids:
            distance = self._position().distance_to(self._position(boid))
            if distance < self.crowding:
                steering -= self._position(boid) - self._position()
        steering = self._clamp_force(steering)
        return steering

    def alignment(self, boids):
        steering = pygame.math.Vector2(0, 0)
        for boid in boids:
            steering += self._velocity(boid)
        steering /= len(boids)
        steering -= self._velocity()
        steering = self._clamp_force(steering)
        return steering / 8

    def cohesion(self, boids):
        steering = pygame.math.Vector2(0, 0)
        for boid in boids:
            steering += self._position(boid)
        steering /= len(boids)
        steering -= self._position()
        steering = self._clamp_force(steering)
        return steering / 100

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid is self:
                continue
            distance = self._position().distance_to(self._position(boid))
            if distance < self.perception:
                neighbors.append(boid)
        return neighbors

    def boid_step(self, boids):
        if not boids:
            return pygame.math.Vector2(0, 0)

        steering = pygame.math.Vector2(0, 0)
        neighbors = self.get_neighbors(boids)
        if neighbors:
            steering += self.separation(neighbors)
            steering += self.alignment(neighbors)
            steering += self.cohesion(neighbors)

        self.x_velocity += steering.x
        self.y_velocity += steering.y
        self._limit_velocity(self.max_speed)
        return steering

    def _limit_velocity(self, max_speed):
        velocity = self._velocity()
        if velocity.length_squared() > 0 and velocity.length() > max_speed:
            velocity = velocity.normalize() * max_speed
            self.x_velocity = velocity.x
            self.y_velocity = velocity.y

    def _clamp_force(self, vector):
        if vector.length_squared() > 0 and vector.length() > self.max_force:
            return vector.normalize() * self.max_force
        return vector

    def _position(self, boid=None):
        if boid is None:
            return pygame.math.Vector2(self.x_pos, self.y_pos)
        return pygame.math.Vector2(boid.x_pos, boid.y_pos)

    def _velocity(self, boid=None):
        if boid is None:
            return pygame.math.Vector2(self.x_velocity, self.y_velocity)
        return pygame.math.Vector2(boid.x_velocity, boid.y_velocity)

    # Code adapted from : https://github.com/meznak/boids_py/blob/master/boid.py
    # Co-pilot AI was used to help understand and alter code