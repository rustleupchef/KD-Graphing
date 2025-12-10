import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import itertools
import inspect
from typing import get_type_hints, Callable
import json

class StaticAxis:
    def __init__(self, name: int, ticks: int, isInput: bool, label = None) -> None:
        self.name = name
        self.ticks = ticks
        self.isInput = isInput
        if label is None:
            label = f"Static Axis {name}"
        self.label = label

class DynamicAxis:
    def __init__(self, name: int, isInput: bool, equation: Callable, label = None) -> None:
        self.name = name
        self.isInput = isInput
        if not self.validate_equation(equation):
            raise ValueError("Equation is not valid; must have two list parameters, and must return an float")
        self.equation = equation
        if label is None:
            label = f"Dynamic Axis {name}"
        self.label = label
    
    def validate_equation(self, func: Callable) -> bool:
        params = inspect.signature(func).parameters
        hints = get_type_hints(func)
        if len(params) != 2:
            print("Parameter count invalid")
            return False
        for name in list(params.keys()):
            if hints.get(name) is not list:
                print(f"Parameter {name} type invalid")
                return False
        if hints.get('return') is not float:
            print("Return type invalid")
            return False
        return True

class Grid:
    def __init__ (self, name: str, outputAxes: list[DynamicAxis, StaticAxis] = [], inputAxes: list[DynamicAxis, StaticAxis] = [], table: list[list[float]] = []):
        self.name = name
        self.outputAxes = outputAxes
        self.inputAxes = inputAxes
        self.table = table
        self.inputDict = {}

    def addStaticAxis(self, axis: StaticAxis) -> None:
        if axis.name in self.inputAxes or axis.name in self.outputAxes:
            raise ValueError(f"An axis with the name {axis.name} already exists.")
        if axis.isInput:
            self.inputAxes.append(axis)
        else:
            self.outputAxes.append(axis)
    
    def addDynamicAxis(self, axis: DynamicAxis) -> None:
        if axis.name in self.inputAxes or axis.name in self.outputAxes:
            raise ValueError(f"An axis with the name {axis.name} already exists.")
        if axis.isInput:
            self.inputAxes.append(axis)
        else:
            self.outputAxes.append(axis)

    def clamp(self, value: float, minVal: float, maxVal: float) -> float:
        return max(min(value, maxVal), minVal)

    def deviation(self, nums: list[float]) -> float:
        mean = sum(nums) / len(nums)
        nums = [abs(x - mean) for x in nums]
        print(f"{nums=}, {mean=}")
        std = sum(nums)/(len(nums))
        return ((std/abs((max(nums) - min(nums))/2) if max(nums) != min(nums) else 1.0) + .5) * 2
    
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
    
    def formatInputDict(self, tick, size, length, index = 1, points = []) -> dict:
        f = {}
        if length == index:
            g = {}
            for point in range(-size, size + 1, tick):
                d = points[:]
                d.append(point)
                g[point] = {"height" : self.outputAxes[index - 1].equation(d, self.inputAxes)}
            return g
        for i in range(-size, size + 1, tick):
            d = points[:]
            d.append(i)
            e = list(itertools.combinations([x for x in range(-size, size + 1, tick)], length - index))
            g = []
            for combo in e:
                temp = d[:]
                for val in combo:
                    temp.append(val)
                g.append(self.outputAxes[index - 1].equation(temp, self.inputAxes))
            
            f[i] = {"graph" : self.formatInputDict(tick, size, length, index + 1, d), "height" : g}
        return f
            

    def formTable(self, size: int = 20) -> None:
        if len(self.inputAxes) != len(self.outputAxes):
            raise ValueError("Number of input axes must equal number of output axes to form table.")
        self.table = []

        length = max([x.name for x in (self.inputAxes + self.outputAxes)]) + 1
        template = [1 for i in range(length)]
        tick = max([x.ticks if isinstance(x, StaticAxis) else 1 for x in self.inputAxes + self.outputAxes])
        combinations = list(itertools.combinations([x for x in range(-size, size + 1, tick)], len(self.inputAxes)))

        for i in range(len(combinations)):
            temp = template[:]
            self.table.append(temp)
        
        for i, row in enumerate(self.table):
            for index, value in enumerate(self.inputAxes):
                row[value.name] = combinations[i][index]
            
            for index, value in enumerate(self.outputAxes):
                if isinstance(value, DynamicAxis):
                    row[value.name] = value.equation(row, self.inputAxes)
        
        self.inputDict = self.formatInputDict(tick, size, len(self.inputAxes), points=[])
        d = json.dumps(self.inputDict, indent=4)
        with open("input/inputDict.json", "w") as f:
            f.write(d)
        

    def graphTable(self) -> None:
        if not os.path.exists("input"):
            os.mkdir("input")
        img = None
        for i in range(max(len(self.inputAxes), len(self.outputAxes))):
            plt.clf()
            x , y = [], []
            for row in self.table:
                x.append(0.5)
                y.append(0.5)
                if i < len(self.inputAxes):
                    x[-1] = row[self.inputAxes[i].name]
                if i < len(self.outputAxes):
                    y[-1] = row[self.outputAxes[i].name]

            print(f"{x=}, {y=}")

            if i < len(self.inputAxes):
                plt.xlabel(self.inputAxes[i].label)
            if i < len(self.outputAxes):
                plt.ylabel(self.outputAxes[i].label)

            if min(y) != max(y):
                plt.ylim(min(y), max(y))
            else:
                plt.ylim(0, max(x))
                y = [max(x)/2 for d in y]
                plt.yticks([])

            if min(x) != max(x):
                plt.xlim(min(x), max(x))
            else:
                plt.xlim(0, max(y))
                x = [max(y)/2 for d in x]
                plt.xticks([])

            if img is None:
                plt.plot(x, y, linewidth=5)
                plt.savefig("input/output.png", bbox_inches="tight", dpi=300)
                img = mpimg.imread("input/output.png")
            else:
                for index, value in enumerate(x):
                    width = (max(x) - min(x))/len(x)
                    height = (max(y) - min(y))/len(y)

                    print(f"{width=} {height=}")

                    widthSD = 1 if width == 0 else self.deviation(y)
                    heightSD = 1 if height == 0 else self.deviation(x)
                    
                    print(f"{widthSD=} {heightSD=}")

                    width = max(y) if width == 0 else width * widthSD
                    height = max(x) if height == 0 else height * heightSD

                    print(f"{width=} {height=}")

                    plt.imshow(img, extent=[value-width/2, value+width/2, y[index]-height/2, y[index]+height/2])
                plt.savefig("input/output.png", bbox_inches="tight", dpi=300)
                img = mpimg.imread("input/output.png")

        plt.title(f"Grid: {self.name}")
        plt.show()

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
        axis = StaticAxis(name=i, ticks=5, isInput=(i < threshold), label= f"x{i}" if i < threshold else f"y{i - threshold}")
        grid.addStaticAxis(axis)
    
    print([axis.name for axis in grid.inputAxes])
    print([axis.name for axis in grid.outputAxes])

    grid.formTable()

if __name__ == "__main__":
    main(args=sys.argv[1:])