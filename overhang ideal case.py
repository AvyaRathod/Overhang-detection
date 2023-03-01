import csv
import os
import numpy as np
from shapely.geometry import Polygon

# Use only when in dire need
delete_files = lambda : os.system("rm -r ./overhang_detection/*.csv")

def extraction():
    with open("overhang_test.gcode") as file:
        data = file.readlines()
    main_array = []
    f =0
    for i in data:
        if ";TYPE:WALL-OUTER\n" == i:
            f = 1
            array = []
            continue
        if f:
            if i[:2] == "G1":
                    array.append(i.rstrip())
            else:
                    main_array.append(array)
                    f = 0
     
# for mul files for every layer

    coordinate = []
    for i, x in enumerate(main_array):
        new = {'X' : None, "Y" : None}
        array = []
        for j in x:
            for k in j.split():
                    if k[0] in ("X" , "Y"):
                        new[k[0]] = float(k[1:])
            array.append((new['X'], new['Y']))
        coordinate.append(array)
    return coordinate

def polygon_area(coordinate):
    # get x and y in vectors
    x = [point[0] for point in coordinate]
    y = [point[1] for point in coordinate]
    # shift coordinates
    x_ = x - np.mean(x)
    y_ = y - np.mean(y)
    # calculate area
    correction = x_[-1] * y_[0] - y_[-1] * x_[0]
    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
    final_area = 0.5 * np.abs(main_area + correction)
    return final_area        

if __name__ == "__main__":
    
    LIMIT = 3

    coordinate = extraction()
    n = len(coordinate)
    for i in range(1, n):
        pgon = Polygon(coordinate[i]) # Assuming the OP's x,y coordinates
        prev = Polygon(coordinate[i-1]).area
        curr = pgon.area
        if (curr - prev) > LIMIT:
            print("OVERHANG DETECTED!")
            break
    
    