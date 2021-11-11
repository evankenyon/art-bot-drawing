# do absolute values, start at 0,0
# determine 4 quadrants
# determine step size based on number of vectors


from Paint_CNC import Paint_CNC
import math as m
# def circle(radius, cnc):
#     for theta in range(360):
#         radians = (m.pi/180)*theta
#         x = round(radius*m.cos(radians),3)
#         y = round(radius*m.sin(radians),3)
#         cnc.g0(x=x,y=y)
#         if theta==0:
#             cnc.down()


def start():
    cnc = Paint_CNC()
    cnc.open("./circle.gcode")
    cnc.g90()
    cnc.g0(z=5)
    cnc.f(3000)
    return cnc

if __name__ == '__main__':
    circle_radius_1 = 20
    circle_radius_2 = 30
    cnc = start()
    cnc.set_paint_color(1)
    cnc.circle(0,-30,circle_radius_1)
    cnc.set_paint_color(2)
    cnc.circle(0,-40,circle_radius_1)
    cnc.set_paint_color(5)
    cnc.circle(0,-50,circle_radius_1)
    # cnc.up()
    # polygon(100, 10, cnc)
