# Tres pilares de Dash
# 1. DASH COMPONENTS
# Cualquier cosa, desde el 'control deslizante', la 'casilla de verificación', el 'selector de fecha', el 'menú desplegable', todos son 
# componentes que se necesitan para crear la capacidad interactiva de sus datos. 

# 2. PLOTLY GRAPHS
# Para que los plotly-graphs sean gráficos y otros tipos de vaidación de datos, parcelas que permiten al usuario visualizar datos, 'cuadro de
#  mapa', el 'gráfico de despersión', 'gráfico de lineas', 'grafico de barras' 
# 3. THE CALLBACK
# La devolución de llamada es uno de los elementos más importantes porque hace conección entre los dash-components y los Plot-Graphs 
# (gráficos de diagrama) para crear una capacidad interantiva.

# Algo importante a resaltar es que los dash-components y los Plot-graphs van dentro de la aplicación y los Callback van por fuera del diseño de la aplicación.

import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go

import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')


df['Date'] = pd.to_datetime(        # Utilizamos esta sección para extraer el año de la fecha registrada de cada temblor
    df['Date'],                     # con el fin de utilizarlo para dar animación a mapa (con 'animetion_frame')
    errors = 'coerce',
    format = '%m/%d/%Y'
)

df['Year'] = df['Date'].dt.year

fig = px.density_mapbox(df, lat='Latitude', 
                        lon='Longitude',
                        z='Magnitude',          # Señalamos la columna a la que le vamos a dar mayor visualización (respecto a los datos)
                        radius=10,              # Determinamos el tamaño general de los puntos 
                        center=dict(lat=0, lon=-80),
                        zoom=2,
                        # animation_frame='Year',   # Argumento que le permite dar animación al mapa (variando el argumento deseado)           
                        mapbox_style="open-street-map",
                        # mapbox_style="dark",
                        # margin={"r":0,"t":0,"l":0,"b":0},
                        )


fig.update_layout(
#     mapbox_style="dark", 
#     mapbox_accesstoken=token,
    margin={"r":0,"t":0,"l":0,"b":0},
    # width='100%',
    height=700,
    )

app.layout = html.Div([
        html.H1("Earthquakers in this World", style={'text-align': 'center'}),  # Se le agrega un titulo al DashBoard

        dcc.Graph(figure=fig)    # Llamamos la grafica que vamos a proyectar

])

if __name__ == '__main__':
    app.run_server(debug=True)  

