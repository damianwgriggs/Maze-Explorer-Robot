from world import MazeWorld
from brain import RobotBrain  # Changed from robot_brain

# --- Initialize ---
world = MazeWorld()
brain = RobotBrain()
status = 'CONTINUE'
step_count = 0
max_steps = 100 # Safety limit

print("--- Simulation Start ---")
print(f"Robot starting at: {world.robot_position}, facing: {world.robot_heading}")

# --- Run Simulation Loop ---
while status == 'CONTINUE' and step_count < max_steps:
    step_count += 1
    print(f"\n--- Step {step_count} ---")
    
    # 1. Get sensor data from the world
    sensor_data = world.get_sensor_data()
    
    # 2. Get action from the brain
    action = brain.decide_action(sensor_data)
    print(f"[Brain] Action: {action}")
    
    # 3. Update the world with the action
    status = world.update_world(action)
    print(f"[World] New Position: {world.robot_position}, New Heading: {world.robot_heading}")

# --- End Simulation ---
print("\n--- Simulation End ---")
if status == 'WIN':
    print(f"SUCCESS: Robot reached the end 'E' in {step_count} steps!")
else:
    print(f"FAILURE: Robot did not reach the end after {max_steps} steps.")