from search_frontier import SearchFrontier, ExploredSet
from state import BlockState

import heapq
import re
import time

SEARCH_TIMEOUT = 60


def bfs_search(start_state: BlockState, goal_config):
    """Breadth-First Search"""
    start_time = time.time()

   # Αρχικοποίηση μετώπου και συνόλου εξερευνημένων
    frontier = SearchFrontier().fifo_queue
    frontier.append(start_state)
    explored = ExploredSet().states

    frontier_configs = {start_state.config}
    nodes_expanded = 0

    while frontier and time.time() - start_time < SEARCH_TIMEOUT:
        current_state = frontier.popleft()
        frontier_configs.remove(current_state.config)
        explored.add(current_state.config)

        # Έλεγχος στόχου
        if current_state.config == goal_config:
            print("SUCCESS")
            return current_state, nodes_expanded, current_state.cost, time.time() - start_time

         # Επέκταση κόμβου
        current_state.expand()
        nodes_expanded += 1

        for child in current_state.children:
            if child.config not in explored and child.config not in frontier_configs:
                frontier.append(child)
                frontier_configs.add(child.config)

    print('FAILURE')
    exit()


def dfs_search(start_state: BlockState, goal_config):
    """Depth-First Search"""
    start_time = time.time()

    frontier = SearchFrontier().lifo_stack
    frontier.append(start_state)
    explored = ExploredSet().states

    frontier_configs = {start_state.config}
    max_depth = 0
    nodes_expanded = 0

    while frontier and time.time() - start_time < SEARCH_TIMEOUT:
        current_state = frontier.pop()
        frontier_configs.remove(current_state.config)

        if current_state.config not in explored:
            explored.add(current_state.config)

            if max_depth < current_state.cost:
                max_depth = current_state.cost

            if current_state.config == goal_config:
                print("SUCCESS")
                return current_state, nodes_expanded, max_depth, time.time() - start_time

            current_state.expand()
            current_state.children = current_state.children[::-1]
            nodes_expanded += 1

            for child in current_state.children:
                if child.config not in frontier_configs:
                    frontier.append(child)
                    frontier_configs.add(child.config)

    print('FAILURE')
    exit()


def a_star_search(start_state, goal_config):
    """A* Search"""
    start_time = time.time()

    frontier = SearchFrontier().priority_heap
    entry_finder = {}
    explored = ExploredSet().states

    start_state.f = heuristic_h3(start_state.config, goal_config)
    add_to_frontier(start_state, entry_finder, frontier)

    nodes_expanded = 0
    max_depth = 0

    while frontier and time.time() - start_time < SEARCH_TIMEOUT:
        current_state = pop_from_frontier(frontier, entry_finder)

        if current_state.config not in explored:
            explored.add(current_state.config)

            if max_depth < current_state.cost:
                max_depth = current_state.cost

            if current_state.config == goal_config:
                print("SUCCESS")
                return current_state, nodes_expanded, max_depth, time.time() - start_time

            current_state.expand()
            nodes_expanded += 1

            for child in current_state.children:
                child.f = child.cost + heuristic_h3(child.config, goal_config)

                if child.config not in entry_finder:
                    add_to_frontier(child, entry_finder, frontier)
                elif child.f < entry_finder[child.config][0]:
                    remove_from_frontier(child.config, entry_finder)
                    add_to_frontier(child, entry_finder, frontier)

    print('FAILURE')
    exit()


def best_first_search(start_state, goal_config):
    """Best-First Search"""
    start_time = time.time()

    frontier = SearchFrontier().priority_heap
    entry_finder = {}

    start_state.f = heuristic_h1(start_state.config, goal_config)
    add_to_frontier(start_state, entry_finder, frontier)

    explored = ExploredSet().states
    max_depth = 0
    nodes_expanded = 0

    while frontier and time.time() - start_time < SEARCH_TIMEOUT:
        current_state = pop_from_frontier(frontier, entry_finder)

        if current_state.config not in explored:
            explored.add(current_state.config)

            if max_depth < current_state.cost:
                max_depth = current_state.cost

            if current_state.config == goal_config:
                print("SUCCESS")
                return current_state, nodes_expanded, max_depth, time.time() - start_time

            current_state.expand()
            nodes_expanded += 1

            for child in current_state.children:
                child.f = heuristic_h2(child.config, goal_config)

                if child.config not in entry_finder:
                    add_to_frontier(child, entry_finder, frontier)
                elif child.f < entry_finder[child.config][0]:
                    remove_from_frontier(child.config, entry_finder)
                    add_to_frontier(child, entry_finder, frontier)

    print('FAILURE')
    exit()


# ------------------ Priority Queue Helper Functions ------------------

def add_to_frontier(state, entry_finder, frontier):
    entry = [state.f, state]
    entry_finder[state.config] = entry
    heapq.heappush(frontier, entry)


def remove_from_frontier(config, entry_finder):
    entry = entry_finder.pop(config)
    entry[-1] = '<removed-task>'


def pop_from_frontier(frontier, entry_finder):
    while frontier:
        state = heapq.heappop(frontier)
        if state[1] != '<removed-task>':
            del entry_finder[state[1].config]
            return state[1]


# ------------------ Heuristics ------------------

def heuristic_h1(config, goal_config):
    """Heuristic 1: counts blocks not in correct position."""
    cost = 0
    for i, cube in enumerate(config):
        if cube[1] != goal_config[i][1]:
            cost += 1
    return cost


def heuristic_h2(config, goal_config):
    """Heuristic 2: weighted difference for blocks needing moves."""
    index = 0
    one_move = set()
    two_moves = set()
    cubes_on_table = {}

    for idx, cube in enumerate(config):
        if cube[1] == -1:
            cubes_on_table[idx] = cube

    for idx in cubes_on_table:
        cube = cubes_on_table[idx]
        if cube[1] != goal_config[idx][1]:
            one_move.add(cube)

        current = cube[0]
        while True:
            if config[current][0] == -1:
                break
            if config[current][1] != goal_config[current][1]:
                one_move.add(config[current])
            else:
                below = config[current][1]
                while True:
                    if config[below] in one_move:
                        one_move.add(config[current])
                        break
                    elif config[below][1] == -1:
                        break
                    below = config[below][1]

                below = config[current][1]
                if config[below] in one_move or config[below] in two_moves:
                    two_moves.add(config[current])
                    one_move.discard(config[current])

                below = config[below][1]
                while True:
                    if config[below] in two_moves:
                        two_moves.add(config[current])
                        break
                    elif config[below][1] == -1:
                        break
                    below = config[below][1]

            current = config[current][0]

    return len(one_move) * 2 + len(two_moves) * 4


def heuristic_h3(config, goal_config):
    """Heuristic 3: position mismatch considering both sides."""
    cost = 0
    for i, cube in enumerate(config):
        if cube[0] != goal_config[i][0] and cube[1] != goal_config[i][1]:
            cost += 2
        elif cube[0] != goal_config[i][0] or cube[1] != goal_config[i][1]:
            cost += 1
    return cost


# ------------------ Path and Validation ------------------

def reconstruct_path(state):
    moves = []
    while state.parent is not None:
        moves.append(state.action)
        state = state.parent
    return moves[::-1]


def validate_solution(state, moves, goal_config):
    config = list(map(list, state.config))
    objects = state.cube_names

    for move in moves:
        action = re.split("[(,)]", move)
        moved = objects.index(action[1])
        prev = action[2]
        curr = action[3]

        if prev == 'table':
            if config[objects.index(curr)][0] == -1:
                config[moved][1] = objects.index(curr)
                config[objects.index(curr)][0] = moved
            else:
                return False
        elif curr == 'table':
            if config[moved][0] == -1:
                config[objects.index(prev)][0] = -1
                config[moved][1] = -1
            else:
                return False
        else:
            if config[moved][0] == -1 and config[objects.index(curr)][0] == -1:
                config[objects.index(curr)][0] = moved
                config[objects.index(prev)][0] = -1
                config[moved][1] = objects.index(curr)
            else:
                return False

    return tuple(map(tuple, config)) == goal_config
