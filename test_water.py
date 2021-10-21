from Paint_CNC import Paint_CNC

def start():
    cnc = Paint_CNC()
    cnc.open("./test_water.gcode")
    cnc.g90()
    cnc.g0(z=5)
    cnc.f(3000)
    cnc.g0(z=5)
    cnc.clean()
    return cnc

start()