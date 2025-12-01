from nmD import *

def d(nums: list, inputIndices: list) -> float:
    n = [nums[x.name] for x in inputIndices]
    return sum(n)

def main():
    grid = Grid("Test Grid")
    for i in range(2):
        axis = StaticAxis(name=i, ticks=5, isInput=True, label=f"Input Axis {i}")
        grid.addStaticAxis(axis)
    
    for i in range(2, 4):
        axis = DynamicAxis(name=i, equation=d, isInput=False, label=f"Output Axis {i-5}")
        grid.addDynamicAxis(axis)
    
    grid.formTable()
    print(grid.table)
    grid.graphTable()
    

if __name__ == "__main__":
    main()