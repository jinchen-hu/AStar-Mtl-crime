import shapefile
from matplotlib import pyplot as plt

shpFilePath='../shapefile/crime_dt.shp'

shape = shapefile.Reader(shpFilePath, encoding='ISO-8859-1')
shapeRecords = shape.shapeRecords()

for i in range(len(shapeRecords)):
    x = shapeRecords[i].shape.__geo_interface__["coordinates"][0]
    y = shapeRecords[i].shape.__geo_interface__["coordinates"][1]
    plt.plot(x, y)

plt.show()
#print(shapeRecords)