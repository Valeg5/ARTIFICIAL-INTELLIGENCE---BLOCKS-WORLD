from collections import deque

class SearchFrontier:
    """
    Αναπαριστά το μέτωπο αναζήτησης για BFS, DFS ή A*.
    """
    def __init__(self):
        # FIFO queue για BFS
        self.fifo_queue = deque()
        # LIFO stack για DFS
        self.lifo_stack = deque()
        # Priority queue για αλγορίθμους όπως A*
        self.priority_heap = []

    def __contains__(self, state):
        """
        Έλεγχος αν μια κατάσταση υπάρχει ήδη στο μέτωπο.
        Συγκρίνει μόνο τη config κάθε BlockState.
        """
        if self.fifo_queue:
            for s in self.fifo_queue:
                if tuple(map(tuple, state.config)) == s.config:
                    return True
        elif self.lifo_stack:
            for s in self.lifo_stack:
                if tuple(map(tuple, state.config)) == s.config:
                    return True
        else:  # priority_heap
            for _, s in self.priority_heap:
                if state.config == s.config:
                    return True
        return False


class ExploredSet:
    """
    Αναπαριστά το σύνολο των εξερευνημένων καταστάσεων
    για να αποφευχθούν επαναλήψεις κατά την αναζήτηση.
    """
    def __init__(self):
        self.states = set()
