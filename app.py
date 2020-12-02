import pandas as pd
import dash 
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as  px

#Iniciar server
app = dash.Dash(__name__)
server = app.server

#Agregamos nuestro token para usar MAPBOX
token = open(".mapbox_token").read()

co_cities = pd.read_csv("DATASET/co.csv")

co_cities = co_cities.query("admin_name in ['Meta', 'Tolima']")


fig = px.line_mapbox(co_cities, lat="lat", lon="lng", hover_name="city",color="admin_name", zoom=3, height=300)

fig.update_layout(mapbox_style = "dark", mapbox_accesstoken=token, mapbox_zoom = 4, mapbox_center_lat =41,
    margin ={"r":0, "t":0, "l":0, "b":0})

markdown_text = '''
### DASHBOARD PARA SCRUM LATAM
Este dashboard experimental se hace con el obetivo de probar las capacidades 
que proporciona el mapa de lineas con MAPBOX
'''
app.layout = html.Div(children=[
    dcc.Markdown(children=markdown_text),
    dcc.Graph(
        id='Gráfico de lineas',
        figure = fig
    )
    
])
#fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)
    