from Paint_CNC import Paint_CNC
def start():
    cnc = Paint_CNC()
    cnc.open("./test_paint.gcode")
    cnc.g90()
    cnc.g0(z=5)
    cnc.f(3000)
    cnc.g0(z=5)
    cnc.set_paint_color(4)
    return cnc
start()