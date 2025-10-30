# The "Explorer" Brain (Version 4.1 - Bug Fix)
# It uses Depth-First Search (DFS) with a path and visited list
class RobotBrain:
    def __init__(self):
        self.visited = set()
        self.path = []

    def decide_action(self, sensor_data):
        # --- 1. Get Current State ---
        current_pos_dict = sensor_data['current_position']
        current_pos = (current_pos_dict['row'], current_pos_dict['col'])
        heading = sensor_data['heading']

        # --- 2. Update Memory (if new tile) ---
        if current_pos not in self.visited:
            self.visited.add(current_pos)
            self.path.append(current_pos)
        
        # --- 3. Find Unvisited Neighbors ---
        neighbor_coords = self._get_neighbor_coords(current_pos, heading)
        new_neighbors = []
        if sensor_data['front'] != 'W' and neighbor_coords['front'] not in self.visited:
            new_neighbors.append('front')
        if sensor_data['left'] != 'W' and neighbor_coords['left'] not in self.visited:
            new_neighbors.append('left')
        if sensor_data['right'] != 'W' and neighbor_coords['right'] not in self.visited:
            new_neighbors.append('right')

        # --- 4. Make Decision: Explore or Backtrack? ---

        # === EXPLORE ===
        if len(new_neighbors) > 0:
            if 'front' in new_neighbors:
                return 'move_forward'
            elif 'left' in new_neighbors:
                return 'turn_left'
            elif 'right' in new_neighbors:
                return 'turn_right'
        
        # === BACKTRACK ===
        # If we are here, there are no new neighbors. We must backtrack.
        
        # *** THE FIX IS HERE ***
        # Only pop if our *current* tile is the one on top of the path stack.
        # This stops us from popping multiple times while just turning around.
        if self.path and self.path[-1] == current_pos:
            self.path.pop()
            
        # 2. If the path is now empty, we are back at the start and failed.
        if not self.path:
            return 'turn_right' # Spin in failure
            
        # 3. Get the tile we want to go back TO
        target_pos = self.path[-1] # The last item in the path (our "parent")
        
        # 4. Find the action that points us at the target_pos
        # We will turn until our "front" sensor faces the target.
        if neighbor_coords['front'] == target_pos:
            return 'move_forward'
        elif neighbor_coords['left'] == target_pos:
            return 'turn_left'
        elif neighbor_coords['right'] == target_pos:
            # This is new: if the target is to our right, turn right.
            return 'turn_right'
        else: 
            # Target is behind us, so just turn (right is as good as left)
            return 'turn_right'


    # --- Helper function to get absolute (row, col) of neighbors ---
    def _get_neighbor_coords(self, current_pos, heading):
        r, c = current_pos
        if heading == 'Up':
            return {
                'front': (r-1, c),
                'left': (r, c-1),
                'right': (r, c+1),
                'back': (r+1, c)
            }
        elif heading == 'Down':
            return {
                'front': (r+1, c),
                'left': (r, c+1),
                'right': (r, c-1),
                'back': (r-1, c)
            }
        elif heading == 'Right':
            return {
                'front': (r, c+1),
                'left': (r-1, c),
                'right': (r+1, c),
                'back': (r, c-1)
            }
        elif heading == 'Left':
            return {
                'front': (r, c-1),
                'left': (r+1, c),
                'right': (r-1, c),
                'back': (r, c+1)
            }