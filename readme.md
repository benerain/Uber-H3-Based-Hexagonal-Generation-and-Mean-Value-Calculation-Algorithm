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

![图片 1](https://user-images.githubusercontent.com/21291632/218384276-001f8366-74ee-4d67-a310-9bafe6ba5a3a.png)
![图片 2](https://user-images.githubusercontent.com/21291632/218384293-7b7cd2b7-dc4a-47f9-883b-d620dbfe03a1.png)



