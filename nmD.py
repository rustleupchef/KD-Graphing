import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class StaticAxis:
    def __init__(self, name: int, range: tuple, ticks: int, isInput: bool, startingValue=None) -> None:
        self.name = name
        self.range = range
        self.ticks = ticks
        self.isInput = isInput
        self.startingValue = startingValue
        if startingValue is not None:
            if not (range[0] <= startingValue <= range[1]):
                raise ValueError("Starting value must be within the specified range.")
        else:
            self.startingValue = abs(range[1] - range[0])//2

class DynamicAxis:
    def __init__(self, name: int, isInput: bool, startingValue=None) -> None:
        self.name = name
        self.isInput = isInput
        self.startingValue = startingValue

class Grid:
    def __init__ (self, name: str, outputAxes: dict = {}, inputAxes: dict = {}, table: list[list[float]] = []):
        self.name = name
        self.outputAxes = outputAxes
        self.inputAxes = inputAxes
        self.table = table
    
    def countOf(self, isDynamic: bool, isInput: bool) -> int:
        count = 0
        for axis in self.inputAxes.values() if isInput else self.outputAxes.values():
            if (isDynamic and isinstance(axis, DynamicAxis)) or (not isDynamic and isinstance(axis, StaticAxis)):
                count += 1
        return count

    def addStaticAxis(self, axis: StaticAxis) -> None:
        if axis.isInput:
            self.inputAxes[axis.name] = axis
        else:
            self.outputAxes[axis.name] = axis
    
    def addDynamicAxis(self, axis: DynamicAxis) -> None:
        if axis.name in self.inputAxes or axis.name in self.outputAxes:
            raise ValueError(f"An axis with the name {axis.name} already exists.")
        if axis.isInput:
            if self.countOf(isDynamic=True, isInput=True) >= 2:
                raise ValueError("Only one dynamic input axis is allowed.")
            self.inputAxes[axis.name] = axis
        else:
            if self.countOf(isDynamic=True, isInput=False) >= 2:
                raise ValueError("Only one dynamic output axis is allowed.")
            self.outputAxes[axis.name] = axis
    
    def setTable(self, table) -> None:
        if type(table) is str:
            if os.path.exists(table) and os.path.isfile(table):
                with open(table, 'r') as f:
                    text = f.read().split("\n")
                    self.table = [[float(x) for x in line.split(",")] for line in text]
            else:
                raise FileNotFoundError(f"File {table} does not exist.")
        elif type(table) is list:
            self.table = table
        else:
            raise TypeError("Table must be a filename or a list of lists.")

def main(args=None):
    if len(args) != 2:
        raise ValueError("Two arguments required: table filename and grid name.")
    grid = Grid(name=args[1])
    grid.setTable(args[0])
    table = grid.table

    if len(table) == 0 or len(table[0]) == 0:
        raise ValueError("Table cannot be empty.")
    
    threshold = len(table[0]) // 2
    for i in range(len(table[0])):
        axis = StaticAxis(name=i, range=(min(row[i] for row in table), max(row[i] for row in table)), ticks=5, isInput=(i < threshold))
        grid.addStaticAxis(axis)
    
    print([axis.name for axis in grid.inputAxes.values()])
    print([axis.name for axis in grid.outputAxes.values()])
    
    img = mpimg.imread('download.jpeg')
    plt.imshow(img, extent=[0, 200, 0, 200], origin='lower')
    x = [float(d) for d in range(400)]
    y = [float(x1) * 2 for x1 in x]
    plt.plot(x, y)
    plt.title(f"Grid: {grid.name}")
    plt.show()

if __name__ == "__main__":
    main(args=sys.argv[1:])