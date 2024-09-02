# This file is part of the TCAS Server. Do not redistribute.
# Defines Box_Server class, derived from Box class; adds init method
import box

class Box_Server(box.Box):

    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
