from nmD import *
import pandas as pd

def d(nums: list, inputIndices: list) -> float:
    return nums[0] ** 2 + nums[1] ** 2 + nums[2] ** 2

def main():
    grid = Grid("Test Grid")
    for i in range(3):
        axis = StaticAxis(name=i, ticks=5, isInput=True)
        grid.addStaticAxis(axis)
    
    for i in range(3, 6):
        axis = DynamicAxis(name=i, equation=d, isInput=False)
        grid.addDynamicAxis(axis)
    
    grid.formTable()

if __name__ == "__main__":
    main()