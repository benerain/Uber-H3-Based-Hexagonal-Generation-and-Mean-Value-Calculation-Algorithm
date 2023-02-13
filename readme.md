# Uber H3-Based Hexagonal Generation and Mean Value Calculation Algorithm

## Algorithm Description

Explanation of the Algorithm:

The main.py file contains two classes: Map class, which is used for visualization and hexagon_mean class, which is used to generate hexagons.   
The file contains test input data:

- sea_surface_temp_raster.tiff: extracted sea surface temperature from nc file
- shandong.geojson or shandong.shp (designated range, either one will do)

The file contains test output data:

- hexagons.shp and hexagons.geojson
- result.csv

After the main function runs, a map will pop up in the Chrome browser for previewing the generated hexagon distribution, and the mean is recorded in the 'data_mean' field of the output vector.



## About H3

The H3 algorithm generates hexagons that are not purely hexagons, but are made up of pentagons and hexagons to accommodate the spherical shape of the earth. The size of the hexagons is controlled by the level, which has a total of 15 levels. The lower the level, the larger the hexagons. For more information, please refer to https://h3geo.org/docs/core-library/restable/.



## Note

If you are not running on a MacOS system, please select the corresponding operating system in the main function lines 9-16, otherwise the map preview may not pop up correctly, but other functions will work normally.

sample output:  

