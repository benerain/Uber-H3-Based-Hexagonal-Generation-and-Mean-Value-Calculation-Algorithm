import folium
import webbrowser
import sys
import geopandas as gp
import rioxarray as rioxr
from h3 import h3
from shapely.geometry import Polygon
import time
import pyroscope

# 在镜像里面跑

# MacOS
# chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'

pyroscope.configure(
    enable_logging=True,
    application_name="uberh3.app",
    server_address="http://pyroscope:4040")

class Map:
    '''
    这个是用来可视化最后六边形的类
    '''
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
        self.my_map = None

    def visualize_hexagons(self, hexagons, color="red", folium_map=None):
        """
        hexagons 是一串六边形代码列表
        """
        polylines = []
        lat = []
        lng = []
        for hex in hexagons:
            polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
            # flatten polygons into loops.
            outlines = [loop for polygon in polygons for loop in polygon]
            polyline = [outline + [outline[0]] for outline in outlines][0]
            lat.extend(map(lambda v: v[0], polyline))
            lng.extend(map(lambda v: v[1], polyline))
            polylines.append(polyline)

        if folium_map is None:
            m = folium.Map(location=[sum(lat) / len(lat), sum(lng) / len(lng)], zoom_start=self.zoom_start, tiles='cartodbpositron')
        else:
            m = folium_map
        for polyline in polylines:
            my_PolyLine = folium.PolyLine(locations=polyline, weight=8, color=color)
            m.add_child(my_PolyLine)
        self.my_map = m

    def showMap(self):
        if not self.my_map:
            # Create the map
            self.my_map = folium.Map(location=self.center, zoom_start=self.zoom_start)


        # Display the map
        self.my_map.save("map.html")
        # webbrowser.get(chrome_path).open("map.html")

class hexagon_mean:
    '''
    tif是需要被均值的图像存在的路径
    region是指定的范围，有3种指定方式。
    1、四角坐标 bounds =[[lat_min, lon_min], [lat_max, lon_max]]
    2、shapefile
    3、geojson
    resolution是分辨率，是0～15之间的整数，数字越小，六边形的面积越大。
    具体每一级的六边形大小参见https://h3geo.org/docs/core-library/restable/
    '''
    def __init__(self, tif, region, resolution):
        self.tif = tif
        self.region = region
        self.res = resolution

    def get_df(self):
        df = (rioxr.open_rasterio(self.tif)
              .sel(band=1)
              .to_pandas()
              .stack()
              .reset_index()
              .rename(columns={'x': 'lon', 'y': 'lat', 0: 'data'}))

        return df


    def screen(self):
        df = self.get_df()
        region = self.region
        if isinstance(region,list): #todo 这里如何保证是一个正确格式的list
            points_inter = df[(df.lat > region[0][0]) & (df.lat < region[1][0])&(df.lon > region[0][1]) & (df.lon < region[1][1])]
            return points_inter

        elif isinstance(region,str):
            if region.endswith('.shp'):
                gdf = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.lon, df.lat)) #todo points_from_xy用了很长时间
                gdf.crs = 'EPSG:4326'

                shparea = gp.read_file(region)
                points_inter  = gp.overlay(gdf, shparea, how='intersection', keep_geom_type=None) #todo gp.overlay也花了很长时间
                return points_inter

            elif region.endswith('.geojson'):
                gdf = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.lon, df.lat))
                gdf.crs = 'EPSG:4326'

                jsonarea = gp.GeoDataFrame.from_file(region)
                points_inter = gp.overlay(gdf, jsonarea, how='intersection', keep_geom_type=None)
                return points_inter
            else:
                print('请输入正确的矢量范围的路径')
        else:
            print("请以bounds =[[lat_min, lon_min], [lat_max, lon_max]]的格式输入四角坐标或者矢量范围的路径")
            sys.exit(-1)

    def hex_mean(self):
        df = self.screen()
        hex_col = 'hex' + str(self.res)
        df[hex_col] = df.apply(lambda x: h3.geo_to_h3(x.lat, x.lon, self.res), 1)
        df_mean = df.groupby(hex_col)['data'].mean().to_frame('data_mean').reset_index()
        df_mean['lat'] = df_mean[hex_col].apply(lambda x: h3.h3_to_geo(x)[0])
        df_mean['lon'] = df_mean[hex_col].apply(lambda x: h3.h3_to_geo(x)[1])

        df_mean.to_csv('result.csv')

        def swap(tup):
            return (tup[1], tup[0])

        def mapt(tup):
            mapped_tuple = map(swap, tup)
            return tuple(mapped_tuple)



        df_mean['geometry0'] = df_mean[hex_col].apply(h3.h3_to_geo_boundary)
        df_mean['geometry_swap'] = df_mean['geometry0'].apply(mapt)
        df_mean['geometry1'] = df_mean['geometry_swap'].apply(Polygon)



        gdf = gp.GeoDataFrame(df_mean, geometry=df_mean['geometry1'],crs='EPSG:4326') #,crs='EPSG:4326'
        gdf = gdf.drop(columns = ['geometry0']) #必须要drop掉tuple列
        gdf = gdf.drop(columns=['geometry_swap'])
        gdf = gdf.drop(columns=['geometry1'])

        gdf.to_file('hexagons.geojson', driver='GeoJSON')
        gdf.to_file('hexagons.shp')

        return df_mean[hex_col].values


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Define coordinates of where we want to center our map
    # coords = [51.5074, 0.1278]


    coords =[37.3615593, -122.0553238]
    tif = 'sea_surface_temp_raster.tiff'
    region = 'shandong.geojson'

    map1 = Map(center=coords, zoom_start=4)

    surface_temp_mean = hexagon_mean(tif,region,4) # 通过更改最后的数字改变六边形大小 范围 int 0～15 ，数字越小六边形越大

    start_time = time.time()
    hexs = surface_temp_mean.hex_mean()
    end_time = time.time()
    print("Time taken by hexs function: ", end_time - start_time)
    map1.visualize_hexagons(hexs)

    map1.showMap()


