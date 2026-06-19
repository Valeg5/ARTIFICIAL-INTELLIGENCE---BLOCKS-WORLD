import re

'''
Convert PDDL-like text files into coded configurations.
Values in config will be:
- -1 = cube is clear OR cube is on table
- j = index of cube over it
- x = index of cube under it
'''

def create_configuration(cube_names, text_state):
    """
    Μετατρέπει το αρχικό ή το στόχο state σε tuple of tuples
    για ευκολότερη επεξεργασία από τους αλγορίθμους.
    """
    config = []

    # Αρχικοποίηση όλων των κύβων με [-1, -1]
    for _ in range(len(cube_names)):
        config.append([-1, -1])

    # Επεξεργασία εντολών ON
    for line in text_state:
        tokens = re.split('[ ]', line)
        if tokens[0] == 'ON':
            cube_index, below_index = cube_names.index(tokens[1]), cube_names.index(tokens[2])
            config[below_index][0] = cube_index  # πάνω από αυτόν
            config[cube_index][1] = below_index  # κάτω από αυτόν

    return tuple(map(tuple, config))


def parse_pddl_file(file):
    """
    Διαβάζει το PDDL-like αρχείο, εξάγει αντικείμενα, αρχική και στόχο κατάσταση
    και επιστρέφει tuple of tuples για αρχική και στόχο config.
    """
    # Διαβάζουμε μέχρι να βρούμε τη γραμμή με objects
    while True:
        line = file.readline()
        if "objects" in line:
            break

    cube_names = re.split("[ \n]", line)

    # Διαβάζουμε υπόλοιπες γραμμές με αντικείμενα μέχρι το :INIT
    while True:
        line = file.readline()
        if ":INIT" not in line:
            cube_names.extend(re.split("[ \n)]", line))
        else:
            break

    # Καθαρισμός λίστας αντικειμένων
    cube_names.remove("(:objects")
    while '' in cube_names:
        cube_names.remove('')
    while ')' in cube_names:
        cube_names.remove(')')

    # Διαβάζουμε αρχική κατάσταση μέχρι το :goal
    init_state = re.split('[()\n]', line)
    while True:
        line = file.readline()
        if ":goal" not in line:
            init_state.extend(re.split('[()\n]', line))
        else:
            break

    # Καθαρισμός init_state
    while '' in init_state:
        init_state.remove('')
    init_state = [x for x in init_state if not x.isspace()]
    init_state.remove(":INIT ")
    init_state.remove('HANDEMPTY')

    # Διαβάζουμε στόχο μέχρι EOF
    goal_state = re.split('[()\n]', line)
    while True:
        line = file.readline()
        if not line:
            break
        else:
            goal_state.extend(re.split('[()\n]', line))

    # Καθαρισμός goal_state
    goal_state.remove(':goal ')
    goal_state.remove('AND ')
    goal_state = [x for x in goal_state if x != '' and not x.isspace()]

    # Δημιουργία tuple of tuples
    start_config = create_configuration(cube_names, init_state)
    goal_config = create_configuration(cube_names, goal_state)

    return cube_names, start_config, goal_config


def write_solution(moves, solution_file):
    """
    Γράφει τις κινήσεις σε αρχείο λύσης.
    Κάθε κίνηση σε δική της γραμμή, χωρίς αριθμητικά.
    """
    with open(solution_file, "w+") as f:
        for move in moves:
            f.write(move + "\n")
