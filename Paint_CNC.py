from cnc import CNC


# Define clean command
# Define paint command

class Paint_CNC(CNC):
    pass
    # Default coordinate system is G53
    def clean(self):
        # Set coordinate system to G54, then 0
        self.g55()
        # If zero is set correctly, we should be at one end of the water basin
        self.g0(z=0)
        self.g0(x=0,y=0)
        # touch water
        self.g0(z=-24)
        # relative
        self.g91()
        for i in range(4):
            self.g0(y=-30)
            self.g0(y=30)
        self.g90()
        # Set back to g54
        self.g0(z=0)
        
        # self.g54()
        # self.g0(y=0)
        # self.g0(x=0)
        # self.g0(z=0)
    def set_paint_color(self, color):
        color_to_num = {"black": 0, "purple": 1, "red": 2, "yellow": 3, "orange": 4, "green": 5, "blue": 6, "brown": 7}
        color_num = color_to_num[color]
        # get some water, clean the brush
        self.clean()
        # find coordinate based on color number
        relative_y_coord = color_num*24.5
        # set to paint coordinate system
        self.g56()
        # zero
        self.g0(z=8)
        self.g0(x=0, y=0)
        self.g0(z=0)
        # self.g0(x=0,y=0,z=0)
        self.g91()
        self.g0(y=-relative_y_coord)
        # touch paint
        self.g0(z=-19.6)
        self.move_brush_around_paint()
        self.g90()
        self.g0(z=8)
        self.g54()
        self.g0(y=0)
        self.g0(x=0)
        self.g0(z=5)
        #     0:, # black
        #     1:, # purple
        #     2:, # red
        #     3:, # yellow
        #     4:, # orange
        #     5:, # green
        #     6:, # blue
        #     7:  # brown

    def move_brush_around_paint(self):
        self.g0(x=8)
        self.g0(x=-16)
        self.g0(x=8)
        self.g0(y=4)
        self.g0(y=-8)
        self.g0(y=4)

