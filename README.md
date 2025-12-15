# *D Graphing
This program serves to make graphing out functions that use multiple inputs and multiple outputs easier 

# Usage

Main Features

- Dynamic Graphs
- Table Based Graphs
- Input/Output Axes
- Static/Dynamic Axes

## Axes
You can add either a static axes or a dynamic axis

Dyanmic Axes contain equations and are reserved for output axes when making dynamic graphs.

#### Format for equation function
```python
def equation(nums: list, inputAxesList: list[StaticAxis]) -> float:
    # processing
    # then return some float
    return float
```

Static Axes are the other type of axis. They are reserved for input axes when dynamic graphing, but can be used for either input and output when table graphing

## Dynamic Graphing

Steps

- add both input and output axes
- run form table function

This does a couple things.

- It forms a table based on all of this data.
- Outputs an input dict as a json
- Outputs the entire graph as an image.

The output system is with files

```bash
input
|----> inputDict.json
|
|----> output.png
```

## Table Graphing
This form of graphing will simply display based on a table of datapoints. It relies that every input axes has a relationship with another output axes.

Typically use this whenever you have smaller dimensions, or the data can't be mapped to an equation. You can either directly assign the table, or plugin in a text/csv file.

## Examples

Table usage
```python
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
```

Dynamic Graph Usage
```python
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
```