import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

token = "pk.eyJ1IjoibWF1cmljaW9hbGkiLCJhIjoiY2tic294Z2N3MDI0NDJ6cWhsZDBqZHlqdSJ9.sHYNFYXlW7EEtzjI5SMs0g"



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


fig = px.scatter_mapbox(
        lat=[3], 
        lon=[-70],

        color_discrete_sequence=["fuchsia"], 
        zoom=3, 
        )

fig.update_layout(
    mapbox_style="dark", 
    mapbox_accesstoken=token,
    margin={"r":0,"t":0,"l":0,"b":0},
    #width='100%',
    height=1100,
    )

app.layout = html.Div([
    
        dcc.Graph(figure=fig)

])



if __name__ == '__main__':
    app.run_server(debug=True)    