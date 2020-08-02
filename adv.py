from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

'''
# First pass solution: 
# Record the room in visited
# Get all the exits with the room.
# Move in one direction, add this to the traversal path and pop it off the directions associated with the room
# Work out the opposite direction and add this to a reverse path so that backtracking is possible and remove the opposite direction from the unexplored paths
# Get exits for the new room and keep note of this (in visited)
# Move in a random direction again and add to the traversal path and pop it off the possible directions
# Keep moving until you reach a dead end
# When there are no more unexplored exits - backtrack along the last direction on the backtracked path and remove it from the backtracked path and add it to the traversal path
# Check that room for unexplored directions and repeat the process again
# This keeps going until the number of rooms visited reaches the length of the rooms graph
'''

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
print('traversal_path', traversal_path)

# Find exits
def get_all_exits_directions(current_room, visited_rooms):
    # declare empty list of valid exits
    valid_exits = []# [] | ['n', | 's', | 'w', | 'e']
    #find our options on where we can go by using utility .get_exits method from room.py file
    for exit in current_room.get_exits(): #['n', 's', 'w', 'e'] | ['n', 's']
        # if the current room has not been visited
        if room_graph[current_room.id][1][exit] not in visited_rooms: #exit: 'n' | 's' not in visited_rooms {0}, exit: 'n'
            # mark as visited and add the exit
            valid_exits.append(exit) # ['n', | 's', | 'w', | 'e']
    #return the updated valid exits
    return valid_exits

# Find rooms to walk to
def find_rooms():

    # create empty set to keep track of  visited rooms
    visited_rooms = set() # {0}
    # adds the player's current room to the set of visited rooms
    visited_rooms.add(player.current_room.id) # visited_rooms = {0}
    print('player.current_room.id', player.current_room.id)
    # empty list to reverse the path out of the room
    backtrack = []
    # print('backtrack', backtrack)

    # while loop the visited rooms is less than the length of unvisited rooms graph's key(id)
    while len(visited_rooms) < len(room_graph.keys()):# 0 < 9 = true
        print('visited_rooms', visited_rooms) #{0} | {0,1}
        # print('room_graph', room_graph.keys())
        #sets the player in the current room to the
        current_room = player.current_room.id # current_room = 0
        print('current_room', current_room)
        # Search for all exit points in room using func get_all_exits_directions()
        valid_exit_path = get_all_exits_directions(player.current_room, visited_rooms) #  valid_exit_path => ['n']
        print('valid_exit_path' , valid_exit_path)

        # if there are no valid exits go reverse
        if len(valid_exit_path) == 0: # ['n', 's', 'w', 'e'] len(4) == 0 => false
            # removes the last path used
            exit_direction = backtrack.pop()
            # print('exit_direction', exit_direction)
            player.travel(exit_direction)
            # adds the exit_direction/path
            traversal_path.append(exit_direction)
            # continue with while loop
            continue 

        # if the room hasn't been visited 
        for exit_direction in valid_exit_path:# exit_direction=>'n' in ['n', 's', 'w', 'e']
            print('exit_direction',exit_direction)
            # add the current room to visited
            visited_rooms.add(room_graph[current_room][1][exit_direction]) # exit_direction=> 'n'
            print('visited_rooms',visited_rooms)# {0,1}
            # adds the exit_direction/path 
            traversal_path.append(exit_direction)
            print('traversal_path',traversal_path)
            print('--------')

            # the reverse path back out 
            if exit_direction == "n":
                backtrack.append("s")
            elif exit_direction == "s":
                backtrack.append("n")
            elif exit_direction == "w":
                backtrack.append("e")
            else:
                backtrack.append("w")
            player.travel(exit_direction)
            break

find_rooms()


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
# print('player.current_room',player.current_room)
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
