
class Bridge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.repaired = False  # starts damaged

    def repair(self):
        self.repaired = True

    def __repr__(self):
        status = "Repaired" if self.repaired else "Damaged"
        return f"Bridge({self.x},{self.y},{status})"
