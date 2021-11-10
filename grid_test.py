from grid import Grid

def main():
    grid = Grid(100, -100)
    print(grid.getParsedCommands(63, -68, 63, -17))
    print(grid.getParsedCommands(63, -17, 18, -17))
    print(grid.getParsedCommands(18, -17, 18, -67))
    print(grid.getParsedCommands(18, -67, 62, -67))
    


    # G1 X18.0 Y-17.0
    # G1 X18.0 Y-67.0
    # G1 X62.0 Y-67.0
    # G1 X62.0 Y-17.0
    # G1 X18.0 Y-17.0
    # G1 X18.0 Y-67.0
if __name__ == "__main__":
    main()