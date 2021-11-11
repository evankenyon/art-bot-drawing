from grid import Grid

def main():
    grid = Grid(100, -100)
    # print(grid.getParsedCommands(63, -68, 63, -17))
    # print(grid.getParsedCommands(63, -17, 18, -17))
    # print(grid.getParsedCommands(18, -17, 18, -67))
    # print(grid.getParsedCommands(18, -67, 62, -67))

    # print(grid.getParsedCommands(5, -19, 6, -19))
    # print(grid.getParsedCommands(6, -19, 6, -15))
    # print(grid.getParsedCommands(6, -15, 0, -8))

    # print(grid.getParsedCommands(3, -7, 4, -9))
    # print(grid.getParsedCommands(4, -9, 4, -11))

    # print(grid.getParsedCommands(0, 0, 1, 0))
    # print(grid.getParsedCommands(1, 0, 0, 0))

    # print(grid.getParsedCommands(68, -63, 67, -61))
    # print(grid.getParsedCommands(67, -61, 67, -58))
    # print(grid.getParsedCommands(68, -63, 67, -61))

    print(grid.getParsedCommands(1, 1, 0, 0))
    print(grid.getParsedCommands(1, 1, 0, 0))

    # G0 X68.0 Y-63.0
    # G0 X67.0 Y-61.0
    # G0 X67.0 Y-58.0


    # G1 X18.0 Y-17.0
    # G1 X18.0 Y-67.0
    # G1 X62.0 Y-67.0
    # G1 X62.0 Y-17.0
    # G1 X18.0 Y-17.0
    # G1 X18.0 Y-67.0
if __name__ == "__main__":
    main()