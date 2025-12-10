from nmD import *
import pandas as pd

def d(nums: list, inputIndices: list) -> float:
    return sum([nums[x.name] for x in inputIndices])

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