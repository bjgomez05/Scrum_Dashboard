import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json

"""librerias necesarios para convertir ciudaddes en lat y lon"""
from mapbox import Geocoder

# Cargamos el archivo con las ciudades 
mxp = pd.read_csv('Miembros_por_pais.csv')

clave = 'pk.eyJ1IjoibWF1cmljaW9hbGkiLCJhIjoiY2tic294Z2N3MDI0NDJ6cWhsZDBqZHlqdSJ9.sHYNFYXlW7EEtzjI5SMs0g' # '.mapbox_token'

geocoder = Geocoder(access_token=clave)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Agregamos la función que optiene la información geografica de las ciudades y vuelve un Dataframe organizado
def lectura(ciudades):
    lat=[]
    lon=[]

    for i in ciudades:
        Geojson = geocoder.forward(str(i)) #aqui colocas el nombre de la ciudad 
        Datos = dict(Geojson.json())

        center=list(Datos["features"][0]["center"])

        #invertimos la lista para obtener el formato deseado
        center= center[::-1]
        #obtenemos la latitud y longitud de
        latitud=(round(center[0],2))
        longitud=(round(center[1],2))
        # print (latitud,longitud)

        lat.append(latitud)
        lon.append(longitud)
    
    DataframeUbicaciones = pd.DataFrame({'lat':lat, 'lon': lon})
    DataframeUbicaciones = DataframeUbicaciones.reset_index(drop=True)

    return DataframeUbicaciones

coordenadas = lectura(mxp['Países']) # Obtenemos el dataframe y lo asignamos a una variable

m_p_p = pd.concat([mxp, coordenadas], axis=1)   # Unimos los dos dataframe en uno solo para poder graficarlo



fig = px.density_mapbox(m_p_p, lat='lat', 
                        lon='lon',
                        z='Miembros',
                        radius=13,
                        title='CONCENTRACIÓN DE MIEMBROS DE LA COMUNIDAD SCRUM LATAM',
                        hover_name='Países',
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