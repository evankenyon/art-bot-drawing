from grid import Grid

def main():
    realPreCondensedCommands = ['UP', 'brown', (41.0, -30.0), 'DOWN', (42.0, -30.0), (42.0, -29.0), (43.0, -28.0), 'UP', (44.0, -26.0), 'DOWN', (44.0, -25.0), 'UP', (45.0, -24.0), 'DOWN', (46.0, -23.0), 'UP', (47.0, -22.0), 'DOWN', (47.0, -21.0), 'UP', (53.0, -17.0), 'DOWN', (54.0, -17.0)]
    condensedCommands = []

    grid = Grid(100, -100)
    isUp = False
    for index in range(len(realPreCondensedCommands)):
        if realPreCondensedCommands[index] == 'brown':
            condensedCommands.append('brown')
            # cnc.set_paint_color(color)
        elif realPreCondensedCommands[index] == 'UP':
            condensedCommands.append('UP')
            isUp = True
            # cnc.up()
        elif realPreCondensedCommands[index] == 'DOWN':
            condensedCommands.append('DOWN')
            isUp = False
            # cnc.down()
        elif index + 1 >= len(realPreCondensedCommands):
            continue
        elif realPreCondensedCommands[index + 1]  == 'brown' or realPreCondensedCommands[index + 1]  == 'UP' or realPreCondensedCommands[index + 1]  == 'DOWN':
            condensedCommands.append(realPreCondensedCommands[index])
        else:
            if isUp:
                print("test")
                condensedCommands.append(realPreCondensedCommands[index])
            if not isUp:
                condensedCommands.extend(grid.getParsedCommands(realPreCondensedCommands[index][0], realPreCondensedCommands[index][1], realPreCondensedCommands[index + 1][0], realPreCondensedCommands[index + 1][1]))
        print(condensedCommands)
    # print(condensedCommands)

if __name__ == "__main__":
    main()