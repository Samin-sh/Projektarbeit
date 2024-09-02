class Box:

    def __str__(self):
        return f"Box(xmin={self.xmin}, xmax={self.xmax}, "\
                   f"ymin={self.ymin}, ymax={self.ymax})"

    def get_x_limits(self):
        return (self.xmin, self.xmax)

    def get_y_limits(self):
        return (self.ymin, self.ymax)
        
