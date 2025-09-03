class Grid:
    def __init__(self, size=20):
        self.size = size
        # 2D grid, each cell initially empty
        self.cells = [[None for _ in range(size)] for _ in range(size)]
        # Track entities by position (x,y) → entity
        self.entities = {}

    def wrap_position(self, x, y):
        """Wrap around edges (toroidal world)."""
        return x % self.size, y % self.size

    def place_entity(self, entity, x, y):
        """Place an entity on the grid and track it."""
        x, y = self.wrap_position(x, y)
        self.cells[y][x] = entity
        self.entities[(x, y)] = entity
        entity.x, entity.y = x, y

    def move_entity(self, entity, dx, dy):
        """Move entity on the grid by dx, dy."""
        # Remove from old cell
        if (entity.x, entity.y) in self.entities:
            del self.entities[(entity.x, entity.y)]
        self.cells[entity.y][entity.x] = None

        # Compute new position
        new_x, new_y = self.wrap_position(entity.x + dx, entity.y + dy)

        # Place in new cell
        self.cells[new_y][new_x] = entity
        self.entities[(new_x, new_y)] = entity
        entity.x, entity.y = new_x, new_y
