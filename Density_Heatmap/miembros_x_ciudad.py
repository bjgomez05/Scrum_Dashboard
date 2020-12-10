import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json

"""librerias necesarios para convertir ciudaddes en lat y lon"""
from mapbox import Geocoder

# Cargamos el archivo con las ciudades 
mxc = pd.read_csv('Miembros_por_ciudad.csv')

clave = 'pk.eyJ1IjoibWF1cmljaW9hbGkiLCJhIjoiY2tic294Z2N3MDI0NDJ6cWhsZDBqZHlqdSJ9.sHYNFYXlW7EEtzjI5SMs0g' # '.mapbox_token'

geocoder = Geocoder(access_token=clave)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Agregamos la función que optiene la información geografica de las ciudades y vuelve un Dataframe organizado
def lectura(ciudades):
    # place=[]
    lat=[]
    lon=[]

    for i in ciudades:
        Geojson = geocoder.forward(str(i)) # aqui colocas el nombre de la ciudad 
        Datos = dict(Geojson.json())
        # print(json.dumps(Datos, indent=4, sort_keys=True))

        center=list(Datos["features"][0]["center"])
        
        # city = list(Datos['features'][0]['place_name'])
        # name = str(''.join(city))

        #invertimos la lista para obtener el formato deseado
        center= center[::-1]
        #obtenemos la latitud y longitud de
        latitud=(round(center[0],2))
        longitud=(round(center[1],2))
        # print (latitud,longitud)

        lat.append(latitud)
        lon.append(longitud)
        # place.append(name)
    
    DataframeUbicaciones = pd.DataFrame({'lat':lat, 'lon': lon})
    # DataframeUbicaciones = pd.DataFrame({'lat':lat, 'lon': lon, 'Ciudad':place})  # Cuando necesitemos un dataframe con los nombres de las ciudades incluidas
    DataframeUbicaciones = DataframeUbicaciones.reset_index(drop=True)

    return DataframeUbicaciones

coordenadas = lectura(mxc['Principales ciudades']) # Obtenemos el dataframe y lo asignamos a una variable

m_p_c = pd.concat([mxc, coordenadas], axis=1)   # Unimos los dos dataframe en uno solo para poder graficarlo



fig = px.density_mapbox(m_p_c, lat='lat', 
                        lon='lon',
                        z='Miembros',
                        radius=13,
                        title='DENSIDAD DE UBICACIONES DE LA COMUNIDAD SCRUM LATAM',
                        hover_name='Principales ciudades',
                        center=dict(lat=0, lon=-80),
                        color_continuous_midpoint=50,
                        zoom=2,
                        # animation_frame='Year',                        
                        # mapbox_style="dark"
                        mapbox_style="open-street-map",
                        height=900,
                        )

app.layout = html.Div([
    
        dcc.Graph(figure=fig)

])

if __name__ == '__main__':
    app.run_server(debug=True)  