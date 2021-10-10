from cnc import CNC

cnc = CNC()

cnc.open("./shading.gcode")

# cnc.render_text_file(open("./test.txt", "r"), 5)
cnc.g90()
cnc.g0(z=5)
cnc.f(3000)
cnc.g0(z=5)
# cnc.g1(z=0)
prevNonUpOrDownCommand = (0, 0)
zVals = [] 


for i in range(0, 150):
    zVals.append(i*0.01)
    

currX = 0
currY = 0
cnc.g0(z=2.5)
for zVal in zVals:
    cnc.g0(x=currY,y=-currX,z=zVal)
    cnc.g0(x=currY + 1,y=-currX,z=zVal)
    currY += 1
#         if currY >= 160:
#             cnc.g0(z=10)
#             currY = 0
#             currX += 10
    

cnc.close()