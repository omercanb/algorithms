class Solution:
    north = (0, 1)
    east = (1, 0)
    south = (0, -1)
    west = (-1, 0)
    clockwise_directions = [north, east, south, west]
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
       # Parse the command
       # Maintain the direction and position of the robot
       # Create a set of obstacles
       obstacle_set = set([tuple(obstacle) for obstacle in obstacles])
       # Direction can be directly added to the position
       direction = self.north
       position = (0, 0)
       max_distance = 0
       for command in commands:
           if command == -2:
               # Turn left
               direction_idx = clockwise_directions.index(direction)
               new_direction_idx = (direction_idx - 1) % 4
               direction = clockwise_directions[new_direction_idx]
           if command == -1:
               # Turn right
               direction_idx = clockwise_directions.index(direction)
               new_direction_idx = (direction_idx + 1) % 4
               direction = clockwise_directions[new_direction_idx]
           else:
               forward_units = command
               for k in range(forward_units):
                   new_position = (position[0] + direction[0], position[1] + direction[1])
                   if new_position in obstacle_set:
                       break
                   position = new_position
                   distance = position[0]**2 + position[1]**2
                   if distance >= max_distance:
                       max_distance = distance
    print(position)
    return max_distance




