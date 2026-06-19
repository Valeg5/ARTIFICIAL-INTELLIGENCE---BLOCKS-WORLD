# Έλεγχος αν ένας κύβος είναι πάνω στο τραπέζι
def is_on_table(cube):
    return cube[1] == -1


# Κλάση που αναπαριστά την κατάσταση των κύβων
class BlockState:

    def __init__(self, config, num_cubes, cube_names, parent=None, action="Initial", cost=0, f=0):
        self.num_cubes = num_cubes          # Πλήθος κύβων
        self.cost = cost                    # g cost (κόστος διαδρομής)
        self.parent = parent                # Γονική κατάσταση (BlockState)
        self.action = action                # Περιγραφή της κίνησης
        self.config = config                # Η διάταξη των κύβων (tuple από tuples)
        '''
        config είναι ένα tuple από tuples:
        Κάθε tuple αναπαριστά έναν κύβο:
            [0] = -1 αν ο κύβος είναι ελεύθερος (clear) αλλιώς index του κύβου που είναι από πάνω
            [1] = -1 αν ο κύβος είναι στο τραπέζι αλλιώς index του κύβου που είναι από κάτω
        Παράδειγμα: (-1, 3) σημαίνει ότι ο κύβος είναι clear και έχει κάτω του τον κύβο με index 3
        '''
        self.children = []                  # Λίστα με παιδιά (επόμενες καταστάσεις)
        self.f = f                          # f cost (για αλγόριθμους όπως A*)
        self.cube_names = cube_names        # Ονόματα κύβων (π.χ. ["A", "B", "C"])

    # Δημιουργεί όλες τις πιθανές νέες καταστάσεις από την τρέχουσα
    def expand(self):
        cube_index = 0
        for current_cube in self.config:
            # Αν ο κύβος είναι clear (δεν έχει τίποτα από πάνω)
            if current_cube[0] == -1:

                # Περίπτωση 1: Αν ο κύβος ΔΕΝ είναι στο τραπέζι -> κίνηση στο τραπέζι
                if not is_on_table(current_cube):
                    new_config = list(map(list, self.config))

                    # Απελευθερώνουμε τον κύβο που ήταν από κάτω
                    new_config[current_cube[1]][0] = -1
                    # Ο τρέχων κύβος πάει στο τραπέζι
                    new_config[cube_index][1] = -1

                    if not self.is_same_with_predecessor(new_config):
                        action_desc = f"Move({self.cube_names[cube_index]},{self.cube_names[current_cube[1]]},table)"
                        # Δημιουργία νέας κατάστασης
                        child_state = BlockState(tuple(map(tuple, new_config)), self.num_cubes, self.cube_names,
                                                 parent=self, action=action_desc, cost=self.cost + 1)
                        self.children.append(child_state)

                # Βρίσκουμε όλους τους άλλους clear κύβους
                free_cubes_indexes = self.find_other_free_cubes(cube_index)

                # Περίπτωση 2: Μετακίνηση του κύβου πάνω σε άλλον clear κύβο
                for target_index in free_cubes_indexes:
                    new_config = list(map(list, self.config))

                    # Ο τρέχων κύβος πάει πάνω στον target
                    new_config[target_index][0] = cube_index
                    new_config[cube_index][1] = target_index

                    # Αν δεν ήταν στο τραπέζι, απελευθερώνουμε τον προηγούμενο κύβο
                    if not is_on_table(current_cube):
                        new_config[current_cube[1]][0] = -1

                    if not self.is_same_with_predecessor(new_config):
                        if is_on_table(current_cube):
                            action_desc = f"Move({self.cube_names[cube_index]},table,{self.cube_names[target_index]})"
                        else:
                            action_desc = f"Move({self.cube_names[cube_index]},{self.cube_names[current_cube[1]]},{self.cube_names[target_index]})"

                        # Δημιουργία νέας κατάστασης
                        child_state = BlockState(tuple(map(tuple, new_config)), self.num_cubes, self.cube_names,
                                                 parent=self, action=action_desc, cost=self.cost + 1)
                        self.children.append(child_state)

            cube_index += 1

    # Επιστρέφει indexes των clear κύβων εκτός από τον δοθέντα
    def find_other_free_cubes(self, exclude_index):
        free_indexes = []
        index = 0
        for cube in self.config:
            if cube[0] == -1 and index != exclude_index:
                free_indexes.append(index)
            index += 1
        return free_indexes

    # Έλεγχος αν η νέα διάταξη είναι ίδια με τον γονέα (για να αποφευχθεί άμεση επανάληψη)
    def is_same_with_predecessor(self, new_config):
        if self.parent is not None:
            if list(map(list, self.parent.config)) == new_config:
                return True
        return False

    # Μέθοδοι σύγκρισης καταστάσεων
    def __eq__(self, other):
        if type(other) is str:
            return False
        return self.config == tuple(map(tuple, other.config))

    def __lt__(self, other):
        if type(other) is str:
            return False
        return self.config < tuple(map(tuple, other.config))

    def __gt__(self, other):
        if type(other) is str:
            return False
        return self.config > tuple(map(tuple, other.config))
