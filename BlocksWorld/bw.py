import sys
import os
import search as search_algorithms
from state import BlockState
from file_handler import parse_pddl_file, write_solution


"""
Χρήση: python planner.py <algorithm> <problem_file> <solution_file>
"""


def main():
    try:
        algorithm_name = sys.argv[1].lower()  # Όνομα αλγορίθμου (breadth, depth, best, astar)
        input_filename = sys.argv[2]          # Όνομα αρχείου προβλήματος
        output_filename = sys.argv[3]         # Όνομα αρχείου λύσης
    except IndexError:
        print("Λανθασμένα ορίσματα! Χρήση: python planner.py <algorithm> <problem_file> <solution_file>")
        exit(0)

    input_folder = os.path.join("pddl")  # Φάκελος με τα προβλήματα
    file_path = os.path.join(input_folder, input_filename)

    try:
        with open(file_path, 'r') as f:
            # Ανάγνωση προβλήματος
            cube_names, start_config, goal_config = parse_pddl_file(f)

            # Δημιουργία αρχικής κατάστασης
            start_state = BlockState(start_config, len(start_config), cube_names)

            # Εκτέλεση κατάλληλου αλγορίθμου
            if algorithm_name == "breadth":
                final_state, expanded_nodes, max_depth, exec_time = search_algorithms.bfs_search(start_state, goal_config)
            elif algorithm_name == "depth":
                final_state, expanded_nodes, max_depth, exec_time = search_algorithms.dfs_search(start_state, goal_config)
            elif algorithm_name == "best":
                final_state, expanded_nodes, max_depth, exec_time = search_algorithms.best_first_search(start_state, goal_config)
            elif algorithm_name == "astar":
                final_state, expanded_nodes, max_depth, exec_time = search_algorithms.a_star_search(start_state, goal_config)
            else:
                print("Άγνωστος αλγόριθμος! Επιλέξτε ανάμεσα σε: breadth, depth, best, astar")
                exit(0)

            # Εύρεση διαδρομής
            solution_moves = search_algorithms.reconstruct_path(final_state)

            # Εγγραφή λύσης σε αρχείο
            write_solution(solution_moves, output_filename)

            # Εκτύπωση στατιστικών
            print("Κόστος διαδρομής:", final_state.cost)
            print("Κόμβοι που επεκτάθηκαν:", expanded_nodes)
            print("Μέγιστο βάθος αναζήτησης:", max_depth)
            print("Χρόνος εκτέλεσης:", exec_time)

            # Έλεγχος εγκυρότητας λύσης
            valid_solution = search_algorithms.validate_solution(start_state, solution_moves, goal_config)
            print('Η λύση είναι έγκυρη:', 'ΝΑΙ' if valid_solution else 'ΟΧΙ')

    except EnvironmentError:
        print("Το αρχείο δεν βρέθηκε!")


if __name__ == '__main__':
    main()