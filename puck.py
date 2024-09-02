class Puck:

    RADIUS = 1.0

    def __str__(self):
        return f"Puck(Id={self.id}, Alive={self.alive}, "\
               f"s={self.s}, v={self.v}, a={self.a}"

    def is_alive(self):
        return self.alive

    def get_id(self):
        return self.id

    def get_time(self):
        return self.t

    def get_position(self):
        return self.s

    def get_velocity(self):
        return self.v

    def get_acceleration(self):
        return self.a

    def get_name(self):
        return self.name

    def get_fuel(self):
        return self.fuel

    def get_points(self):
        return self.points

