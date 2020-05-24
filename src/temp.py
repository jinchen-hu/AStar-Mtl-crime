import statistics
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt


file = 'shape_file/crime_dt'

# coordinates of Montreal center downtown
coordinates = [(-73.59, 45.49), (-73.55, 45.49), (-73.55, 45.53), (-73.59, 45.53)]
coords = []
x = []
y = []

# read shapefile and store it into a variable
data = shp.Reader(file, encoding = "ISO-8859-1")

# appends coordinates given to be displayed in graph
records = data.shapeRecords()
for i in range(len(records)):
    coords.append(records[i].shape.__geo_interface__["coordinates"])
    x.append(coords[i][0])
    y.append(coords[i][1])

# computation of statistics (std stands for standard deviation)
totalCount = len(x)
mean = (np.mean(x), np.mean(y))
std = (np.std(x), np.std(y))
median = (np.median(x), np.median(y))

# setting all the numbers in descending order
x2 = sorted(x, reverse = True)
y2 = sorted(y, reverse = True)

# initializing graph and grid size
fig, ax1 = plt.subplots(1, 1)
graph = ax1.hist2d(x, y, bins=20)
ax1.set_title("Mean (x, y): " + str(mean) + "\n STD (x, y): " + str(std))
plt.colorbar(graph[3], ax=ax1)

# setting threshold
threshold = 0
user = int(input("Would you rather test a threshold of 50 , 75 or 90 (%): "))
if user == 50:
    threshold = 50
    print(threshold)
elif user == 75:
    threshold = 75
    print(threshold)
elif user == 90:
    threshold = 90
    print(threshold)

plt.show()