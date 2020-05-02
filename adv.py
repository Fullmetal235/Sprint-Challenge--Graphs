from room import Room
from player import Player
from world import World
from util import Queue, Stack
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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = ['n', 'w', 's', 'e']

def traversal(visited=None, previous=None, came_from=None):
    current_room = player.current_room.id
    exits = player.current_room.get_exits()
    reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    # redeclaring visited every time as to not cause issues with carrying over values with multiple function calls
    if visited is None:  # don't want to redefine this if we're being passed and updated value
        visited = {}

    if current_room not in visited:
        # have to instantiate an object before you can assign values in a nested object
        visited[current_room] = {}

    # if we're not on the first node, there will always be a previous otherwise
    if previous:
        # what direction did we go to get to the current room?
        # i.e. 0: { 'n': 1 }, north from 0 = 1
        visited[previous][came_from] = current_room
        # what direction would we have to go to get back?
        # i.e. 1: { 's': 0  } south from 1 = 0
        visited[current_room][reverse[came_from]] = previous

    for direction in exits:
        if direction not in visited[current_room]:
            traversal_path.append(direction)
            player.travel(direction)
            # for each viable direction in every single node, we're repeating this for loop
            traversal(visited, previous=current_room, came_from=direction)

    # we hit this case when the direction IS in visited, but we haven't touched all of the nodes yet
    if len(visited) < len(room_graph):
        # retracing steps until we get to a point where
        retrace = reverse[came_from]
        player.travel(retrace)
        traversal_path.append(retrace)

    # print(visited)
    # print(traversal_path)


traversal()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
