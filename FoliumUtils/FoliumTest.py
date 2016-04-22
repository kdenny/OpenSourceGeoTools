__author__ = 'kdenny'

import folium
import pandas as pd

def makeFolium(gjfile):
    # state_geo = r'us-states.json'
    # state_unemployment = r'US_Unemployment_Oct2012.csv'
    #
    # state_data = pd.read_csv(state_unemployment)
    #
    # # Let Folium determine the scale.


    stamen = folium.Map(location=[38.9, -77.10], tiles='Stamen Toner',
                        zoom_start=8)
    stamen.simple_marker([38.9, -77.10], popup='Some Other Location',marker_color='red',marker_icon='info-sign')
    stamen.geo_json(geo_path=gjfile)

    # states.geo_json( columns=['state', 'shareGov', 'popups'],
    #         geo_path=state_geo, data=df, data_out='gov_share.json',
    #         key_on='feature.properties.name',
    #         fill_color='PuRd', fill_opacity=0.7, line_opacity=0.2,
    #         legend_name='Incumbent Governor Vote Share (%)')

    folium.Map.save(stamen, 'C:/Users/kdenny/Documents/OpenSourceTools/FoliumUtils/stamen_map.html')