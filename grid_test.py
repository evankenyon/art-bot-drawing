from grid import Grid

def main():

    grid = Grid(100, -100)
    print(grid.getParsedCommands(47, -17, 46, -18))
    print(grid.getParsedCommands(46, -18, 47, -19))
    # print(grid.getParsedCommands(0, 0, 1, 1))
    # print(grid.getParsedCommands(1, 1, 2, 2))

    # realPreCondensedCommands = [(0,0), (1,1), (2,2)]
    # condensedCommands = []

    # grid = Grid(100, -100)
    # isUp = False
    # for index in range(len(realPreCondensedCommands)):
    #     if realPreCondensedCommands[index] == 'brown':
    #         condensedCommands.append('brown')
    #         # cnc.set_paint_color(color)
    #     elif realPreCondensedCommands[index] == 'UP':
    #         condensedCommands.append('UP')
    #         isUp = True
    #         # cnc.up()
    #     elif realPreCondensedCommands[index] == 'DOWN':
    #         condensedCommands.append('DOWN')
    #         isUp = False
    #         # cnc.down()
    #     elif index + 1 >= len(realPreCondensedCommands):
    #         continue
    #     elif realPreCondensedCommands[index + 1]  == 'brown' or realPreCondensedCommands[index + 1]  == 'UP' or realPreCondensedCommands[index + 1]  == 'DOWN':
    #         condensedCommands.append(realPreCondensedCommands[index])
    #     else:
    #         if isUp:
    #             print("test")
    #             condensedCommands.append(realPreCondensedCommands[index])
    #         if not isUp:
    #             condensedCommands.extend(grid.getParsedCommands(realPreCondensedCommands[index][0], realPreCondensedCommands[index][1], realPreCondensedCommands[index + 1][0], realPreCondensedCommands[index + 1][1]))
    #     print(condensedCommands)
    # print(condensedCommands)

if __name__ == "__main__":
    main()