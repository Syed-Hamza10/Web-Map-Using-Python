
import folium , pandas

data = pandas.read_csv('Volcanoes.txt')

lat = list(data['LAT'])
long = list(data['LON'])
elv = list(data['ELEV'])
name = list(data['NAME'])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location = [38.58,-99.09], zoom_start=5)

fgv = folium.FeatureGroup(name="Volcanoes")


def change_colour(el):
    if el >= 0 and el <= 1000:
        return 'green'
    elif el>=1000 and el<=3000:
        return 'orange'
    else:
        return 'red'


for lt, ln, el, name in zip(lat, long, elv, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.Marker(location=[lt,ln], popup = folium.Popup(iframe), icon = folium.Icon(color=change_colour(el))))

fgp = folium.FeatureGroup(name="Population Color")    
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function = lambda x: {'fillColor' : 'green' if x['properties']['POP2005']< 1000000 
else 'orange' if 1000000 <= x['properties']['POP2005'] < 2000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save('Map.html')

