import folium
import pandas as pd

data = pd.read_csv('volcano_db.csv', encoding='latin1')

philippines_volcanoes = data[data['Country'] == 'Philippines']

lat = list(philippines_volcanoes["Latitude"])
lon = list(philippines_volcanoes["Longitude"])
elev = list(philippines_volcanoes["Elev"])
country = list(philippines_volcanoes["Country"])
status = list(philippines_volcanoes["Status"])
name = list(philippines_volcanoes["Volcano Name"])

# lat = list(data["Latitude"])
# lon = list(data["Longitude"])
# elev = list(data["Elev"])
# country = list(data["Country"])
# status = list(data["Status"])
# name = list(data["Volcano Name"])



def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<= elevation < 2000:
        return 'orange'
    else:
        return 'red'
    

map = folium.Map(location=[11.72, 123.71], zoom_start=6, tiles = "Cartodb Positron")

fgVolcanoes= folium.FeatureGroup(name="Volcanoes")

for lt,ln,el,name ,status in zip(lat,lon,elev,name,status):
    # Generate HTML content for popup
    popup_content = f"""
    <h4>{name}</h4>
    <p><b>Status:</b> {status}</p>
    <p><b>Elevation:</b> {el} m</p>
    """
    fgVolcanoes.add_child(folium.CircleMarker(location=[lt,ln], popup=folium.Popup(popup_content, max_width=300),radius = 6, fill_color=color_producer(el),fill_opacity=1, color='grey'))




fgPopulation= folium.FeatureGroup(name="Population")


fgPopulation.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgVolcanoes)
map.add_child(fgPopulation)

map.add_child(folium.LayerControl())

map.save("Map1.html")
