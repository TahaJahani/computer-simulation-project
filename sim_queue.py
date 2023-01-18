class Queue:
    insert_method = None
    pop_method = None
    elements = None

    def __init__(self, insert_method, pop_method) -> None:
        self.insert_method = insert_method
        self.pop_method = pop_method
        self.elements = []