class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for cols in range(dim[0])] for rows in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter(Light):
    def __init__(self, adaptee):
        self.adaptee = adaptee
        self.dim = (0, 0)
        self.lights = list()
        self.obstacles = list()

    def lighten(self, in_map):
        self.dim = len(in_map[0]), len(in_map)  # cols, rows
        for col in range(self.dim[0]):
            for row in range(self.dim[1]):
                if in_map[row][col] > 0:
                    self.lights.append((col, row))
                elif in_map[row][col] < 0:
                    self.obstacles.append((col, row))

        self.adaptee.set_dim(self.dim)
        self.adaptee.set_lights(self.lights)
        self.adaptee.set_obstacles(self.obstacles)

        return self.adaptee.generate_lights()
