Aquarium Simulation

A python aquarium simulation 

Project Structure
- `aquarium.py` - Main aquarium environment/tank manager
- `boids.py` - Boid flocking algorithm implementation
- `fish.py` - Base fish class
- `prey_fish.py` - Prey fish implementation
- `predator_fish.py` - Predator fish implementation
- `Main.py` - Entry point to run the simulation
Installation

Prerequisites
- Python 3.8+

Setup
1. Clone the repository
```bash
git clone https://github.com/Brian-Robinson31/Aqarium-Simulation.git
cd Aqarium-Simulation
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Simulation
```bash
python Main.py
```

The aquarium will open in a new window showing the fish simulation.

M2 Update Status :
Project Status
1. So far, basic movement algorithms for prey fish, predator fish, and food spawning have been implemented. This includes the usual boids style movement for prey fish, and the switch between normal movement and searching for food for both prey and predator fish.
2. There still needs to be proper reproduction for the fish in the tank, along with measuring out the time in which fish get hungry and food spawns to level out with the mathematical equations presented in M1
3. No Drastic changes have been made since the time of the project proposal till now

