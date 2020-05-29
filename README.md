# comp472-a1

## Instroduction

The application generates an optimal path on the given map base on A* algorithm after the user input the grid size, threshold, starting point, and destination. It will find the shortest route between these two coordination and avoid any danger.



## Required Packages

* geopandas -- for read map data
* matplotlib -- for drawing images
* numpy -- support array, range, arange, and some data computation
* os -- create folders storing images the application produce
* time -- compute the time cost of search
* signal -- set a timeout signal



## Instruction

1. readMap.py supports methods which read map, manipulate map data, and draw images
   * The image highlights the block areas will be stored in the path '../images/grids/'
   * The image displays the optimal path will be stores in the path '../images/paths/'
2. aStar.py supports the A* algorithm for finding the optimal path between two points the user entered
   1. Find the optimal path
   2. Cannot find the optimal path when the open list is empty
   3. Timeout
3. run.py combines all methods, is our main driver
   1. The user run the method run()
   2. App shows welcome message
   3. Prompt user enter the grid size
      * smaller 0.002 is recommended
   4. Prompt user input the threshold 
      * range: 0 - 100
   5. Display and save the image which the block areas are dyed to be orange
   6. Prompt user input starting point and destination
      1. Longitude, Latitude
      2. If the optimal path is found
         * The path will shows on the image as lines
      3. Otherwise, failure message will display

