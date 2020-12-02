import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go
import geopandas as gpd
from dash.dependencies import Input, Output


#Cargo el token
token = open(".mapbox_token").read() 

# Inicializo la aplicación
app = dash.Dash(__name__)

server = app.server


# Se define la aplicación
app.layout = html.Div(
                children=[
                    html.Div(className='row',  # Defino el elemento row
                        children=[
                            html.Div(className='three columns div-user-controls h6',  # Defino la columna izquierda
                                children = [
                                    html.H2('DASH', style={'textAlign': 'center'}),
                                    html.H2('SCRUM LATAM', style={'textAlign': 'center'}),
                                    html.Br(),
                                    html.P('Visualizando distintos tipos de gráficos de dispersión con Mapbox', style={'textAlign': 'justify'}),
                                    html.Div(className='div-for-dropdown',
                                        children=[
                                            dcc.Dropdown(
                                                id="select",
                                                options=[
                                                    {'label': 'Plotly Express', 'value': 'px'},
                                                    {'label': 'Go', 'value': 'go'},
                                                    {'label': 'Geopandas', 'value': 'gp'},
                                                    {'label': 'Ciudades de Colombia', 'value': 'co'}
                                                ],
                                                value='px'
                                            ),                                            
                                        ], #cierre de children
                                    style={'color': '#1E1E1E'}) #Cierre del html.div div-for-dropdown
                            ]), #Cierre del html.div three columns y children
                            html.Div(className='nine columns div-for-charts bg-grey',  # Defino la columna derecha con color gris
                                children = [
                                    dcc.Graph(id='figura',
                                              config={'displayModeBar': False}
                                    ) #Cierre de dcc.Graph
                            ])#Cierre del html.div eight columns y children
                    ])#Cierre del htlm.div div row
                ])#Cierre del html.div

@app.callback(Output('figura', 'figure'),
              [Input('select', 'value')])
def update_output(select):
    if select == 'px':
        px.set_mapbox_access_token(token)
        df = px.data.carshare()
        fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10, size_max=15)

        fig.update_layout(
            plot_bgcolor  = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            title={'text': 'Ejemplo básico con Plotly Express', 'x': 0.5})
        
    else:
        if select == 'go':
            fig = go.Figure(go.Scattermapbox(
                mode = "markers+text+lines",
                lon = [-75, -80, -50], lat = [45, 20, -20],
                marker = {'size': 20, 'symbol': ["bus", "harbor", "airport"]},
                text = ["Bus", "Harbor", "airport"],textposition = "bottom right"))


            fig.update_layout(
                mapbox = {
                    'accesstoken': token,
                    'style': "light", 'zoom': 0.7},
                plot_bgcolor  = 'rgba(0, 0, 0, 0)',
                paper_bgcolor = 'rgba(0, 0, 0, 0)',
                title={'text': 'Ejemplo básico con graph_objs (go) y marcadores', 'x': 0.5})
        
        else:
            if select =='gp':
                geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

                px.set_mapbox_access_token(open(".mapbox_token").read())
                fig = px.scatter_mapbox(geo_df,
                                        lat=geo_df.geometry.y,
                                        lon=geo_df.geometry.x,
                                        hover_name="name",
                                        zoom=1)

                fig.update_layout(
                plot_bgcolor  = 'rgba(0, 0, 0, 0)',
                paper_bgcolor = 'rgba(0, 0, 0, 0)',
                title={'text': 'Ejemplo básico con GeoPandas', 'x': 0.5})

            else:
                if select == 'co':
                    df = pd.read_csv('data/co.csv')
                    site_lat = df.lat
                    site_lon = df.lng
                    locations_name = df.city

                    fig = go.Figure(go.Scattermapbox(
                            lat=site_lat,
                            lon=site_lon,
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                                size=17,
                                color='rgb(55, 73, 175)',
                                opacity=0.7
                            ),
                            text=locations_name,
                            hoverinfo='text'
                        ))
                    
                    fig.update_layout(
                    title={'text': 'Ciudades de Colombia', 'x': 0.5},
                    autosize=True,
                    hovermode='closest',
                    showlegend=False,
                    plot_bgcolor  = 'rgba(0, 0, 0, 0)',
                    paper_bgcolor = 'rgba(0, 0, 0, 0)',
                    height=600,
                    mapbox=dict(
                        accesstoken=token,
                        bearing=0,
                        center=dict(
                            lat=4.6126,
                            lon=-74.0705
                        ),
                        pitch=0,
                        zoom=4,
                        style='light'
                    ),
                )

    return fig




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)