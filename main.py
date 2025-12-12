from nmD import *
import pandas as pd

def a(nums: list, inputIndices: list) -> float:
    return nums[0] ** 2

def b(nums: list, inputIndices: list) -> float:
    return nums[0] * nums[1]

def c(nums: list, inputIndices: list) -> float:
    return nums[0] + nums[1]



def main():
    grid = Grid("Test Grid")
    for i in range(3):
        axis = StaticAxis(name=i, ticks=5, isInput=True)
        grid.addStaticAxis(axis)
    
    d = [a, b, c]

    for i in range(3, 6):
        axis = DynamicAxis(name=i, equation=d[i - 3], isInput=False)
        grid.addDynamicAxis(axis)
    
    grid.formTable()

if __name__ == "__main__":
    main()