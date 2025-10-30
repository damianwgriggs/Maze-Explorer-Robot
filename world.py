class MazeWorld:
    def __init__(self):
        # W = Wall, C = Clear, S = Start, E = End
        # This is a complex maze with a dead-end "island"
        self.maze = [
            ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
            ['W', 'S', 'C', 'W', 'C', 'C', 'W'],
            ['W', 'C', 'W', 'W', 'C', 'W', 'W'],
            ['W', 'C', 'C', 'C', 'C', 'C', 'W'],
            ['W', 'W', 'W', 'C', 'W', 'E', 'W'],
            ['W', 'C', 'C', 'C', 'W', 'W', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W', 'W']
        ]
        # Robot starts at (row, col) position (1, 1)
        self.robot_position = {'row': 1, 'col': 1}
        # Robot starts facing 'Right'
        self.robot_heading = 'Right' # Can be 'Up', 'Down', 'Left', 'Right'

    # The robot's "brain" calls this to see the world
    def get_sensor_data(self):
        r, c = self.robot_position['row'], self.robot_position['col']
        
        # UPGRADED SENSORS
        sensors = {
            'front': self._get_tile_in_front(r, c, self.robot_heading),
            'left': self._get_tile_on_left(r, c, self.robot_heading),
            'right': self._get_tile_on_right(r, c, self.robot_heading),
            'current_tile': self.maze[r][c],
            
            # NEW "GPS" SENSORS
            'current_position': self.robot_position,
            'heading': self.robot_heading
        }
        print(f"[Sensor] Data: {sensors}") # Print sensor data for debugging
        return sensors

    # The simulator calls this to update the world
    def update_world(self, action):
        r, c = self.robot_position['row'], self.robot_position['col']
        
        # Update heading
        if action == 'turn_left':
            if self.robot_heading == 'Right': self.robot_heading = 'Up'
            elif self.robot_heading == 'Up': self.robot_heading = 'Left'
            elif self.robot_heading == 'Left': self.robot_heading = 'Down'
            elif self.robot_heading == 'Down': self.robot_heading = 'Right'
            
        elif action == 'turn_right':
            if self.robot_heading == 'Right': self.robot_heading = 'Down'
            elif self.robot_heading == 'Up': self.robot_heading = 'Right'
            elif self.robot_heading == 'Left': self.robot_heading = 'Up'
            elif self.robot_heading == 'Down': self.robot_heading = 'Left'
            
        # Update position
        elif action == 'move_forward':
            if self.robot_heading == 'Right' and self.maze[r][c+1] != 'W':
                self.robot_position['col'] += 1
            elif self.robot_heading == 'Left' and self.maze[r][c-1] != 'W':
                self.robot_position['col'] -= 1
            elif self.robot_heading == 'Up' and self.maze[r-1][c] != 'W':
                self.robot_position['row'] -= 1
            elif self.robot_heading == 'Down' and self.maze[r+1][c] != 'W':
                self.robot_position['row'] += 1
        
        # Check for win
        if self.maze[self.robot_position['row']][self.robot_position['col']] == 'E':
            return 'WIN'
            
        return 'CONTINUE'

    # --- Helper functions for sensors ---
    def _get_tile_in_front(self, r, c, heading):
        if heading == 'Right': return self.maze[r][c+1]
        if heading == 'Left': return self.maze[r][c-1]
        if heading == 'Up': return self.maze[r-1][c]
        if heading == 'Down': return self.maze[r+1][c]
        
    def _get_tile_on_left(self, r, c, heading):
        if heading == 'Right': return self.maze[r-1][c] # 'Up'
        if heading == 'Left': return self.maze[r+1][c] # 'Down'
        if heading == 'Up': return self.maze[r][c-1] # 'Left'
        if heading == 'Down': return self.maze[r][c+1] # 'Right'

    def _get_tile_on_right(self, r, c, heading):
        if heading == 'Right': return self.maze[r+1][c] # 'Down'
        if heading == 'Left': return self.maze[r-1][c] # 'Up'
        if heading == 'Up': return self.maze[r][c+1] # 'Right'
        if heading == 'Down': return self.maze[r][c-1] # 'Left'