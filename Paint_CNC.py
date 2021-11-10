from cnc import CNC
import math


# Define clean command
# Define paint command

class Paint_CNC(CNC):
    pass
    
    stroke_distance = 0
    absolute_coords = True
    current_position = [0,0,0] # x, y, z
    current_coordinate_system = 54
    THRESHOLD = 50
    pen_paint_height = -21.5
    pen_water_height = -20
    current_color = "black"
    # Default coordinate system is defined here as G54

    def g0(self, x=None, y=None, z=None):
        # check if pen is down too
        # if coordinate system is not standard, don't calculate difference
        if self.current_coordinate_system != 54:
            return super().g0(x=x,y=y,z=z)
        if self.pen_down:
            dx, dy = self.__calculate_difference(x,y)
            self.stroke_distance += math.sqrt(dx**2 + dy**2)
            print("dx {} dy {}".format(dx,dy))
            print(self.stroke_distance)
            if self.stroke_distance > self.THRESHOLD:
                self.stroke_distance = self.stroke_distance - self.THRESHOLD
                print("would refill here")
                self.refill()
        print(self.current_position)
        self.__update_position(x,y,z)
        return super().g0(x=x, y=y, z=z)
    # New methods to add for more functionality
    def refill(self):
        self.comment("Refilling started")
        self.set_paint_color(self.current_color)
        self.comment("Refilling done")
    def clean(self):
        # Set coordinate system to G54, then 0
        self.comment("Cleaning started")
        self.up()
        self.g55()
        # If zero is set correctly, we should be at one end of the water basin
        self.g0(x=0,y=0,z=0)
        self.__move_brush_around_water()
        self.up()
        self.comment("Cleaning done")
        # self.__return_to_last_painting_position()        

    def set_paint_color(self, color):
        self.comment("Setting color to: {}".format(color_num))
        color_to_num = {"black": 0, "purple": 1, "red": 2, "yellow": 3, "orange": 4, "green": 5, "blue": 6, "brown": 7}
        color_num = color_to_num[color]
        # get some water, clean the brush
        self.clean()
        self.current_color = color
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
        self.g0(z=self.pen_paint_height)
        self.__move_brush_around_paint()
        self.__return_to_last_painting_position()
        self.comment("Done setting color to: {}".format(color))

    # -- Private methods --
    def __move_brush_around_paint(self):
        self.g0(x=8)
        self.g0(x=-16)
        self.g0(x=8)
        self.g0(y=4)
        self.g0(y=-8)
        self.g0(y=4)
    def __move_brush_around_water(self):
        # touch water
        self.g0(z=self.pen_water_height)
        # relative
        self.g91()
        for i in range(4):
            self.g0(y=-30)
            self.g0(y=30)
    def __return_to_last_painting_position(self):
        self.g90()
        self.g54()
        self.up()
        self.g0(x=self.current_position[0],y=self.current_position[1])
        self.down()
    def __update_position(self,x, y, z):
        # dx, dy = self.__calculate_difference(x,y)
        if self.current_coordinate_system == 54:
            if x is None:
                x = self.current_position[0]
            if y is None:
                y = self.current_position[1]
            if z is None:
                z = self.current_position[2]
            self.current_position = [x, y, z]
            # print(self.current_position)
    def __calculate_difference(self,x,y):
        if self.absolute_coords:
            if x is None:
                x = 0
            if y is None:
                y = 0
            dx = abs(self.current_position[0] - x)
            dy = abs(self.current_position[1] - y)
            return [dx,dy]
        return [x,y]
    # -- Overriden G code commands --
    def g54(self):
        self.current_coordinate_system = 54
        return super().g54()
    def g55(self):
        self.current_coordinate_system = 55
        return super().g55()
    def g56(self):
        self.current_coordinate_system = 56
        return super().g56()
    def g90(self):
        self.absolute_coords = True
        return super().g90()
    def g91(self):
        self.absolute_coords = False
        return super().g91()
