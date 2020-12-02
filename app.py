import pandas as pd
import dash 
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as  px

#Iniciar server
app = dash.Dash(__name__)
server = app.server

co_cities = pd.read_csv("DATASET/departamentoscolombia.csv")

co_cities = co_cities.query("Departamento in ['Meta', 'Guaviare']")


fig = px.line_mapbox(co_cities, lat="lat", lon="lon", color="Departamento", zoom=3, height=300, title="Intento de líneas con MAPBOX Colombia")

fig.update_layout(mapbox_style = "carto-darkmatter", mapbox_zoom = 4, mapbox_center_lat =41,
    margin ={"r":0, "t":0, "l":0, "b":0})

app.layout = html.Div(children=[
    dcc.Graph(
        id='Gráfico de lineas',
        figure = fig
    )
])
#fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)
    