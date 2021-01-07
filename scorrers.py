import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer
import plotly.express as px


port = 5000
# or simply open on the default `8050` port


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


app = dash.Dash(__name__)

scorrers = pd.read_csv('scorrers_table.csv', index_col=0)
# print(scorrers)

app.layout = html.Div([

    html.H1('Top scorrers of the PGNiG Superliga in season 2020/2021', style={'text-align': 'center',
                                                                              'color': 'blue'}),

    dcc.Dropdown(
        id='ID_zespol',
        options=[
                    {"label": "Grupa Azoty SPR Tarnów", "value": "Grupa Azoty SPR Tarnów"},
                    {"label": "MKS Zagłębie Lubin", "value": "MKS Zagłębie Lubin"},
                    {"label": "Azoty-Puławy", "value": "Azoty-Puławy"},
                    {"label": "Torus Wybrzeże Gdańsk", "value": "Torus Wybrzeże Gdańsk"},
                    {"label": "Piotrkowianin Piotrków Tryb.", "value": "Piotrkowianin Piotrków Tryb."},
                    {"label": "Łomża Vive Kielce", "value": "Łomża Vive Kielce"},
                    {"label": "Energa MKS Kalisz", "value": "Energa MKS Kalisz"},
                    {"label": "Górnik Zabrze", "value": "Górnik Zabrze"},
                    {"label": "Sandra Spa Pogoń Szczecin", "value": "Sandra Spa Pogoń Szczecin"},
                    {"label": "ORLEN Wisła Płock", "value": "ORLEN Wisła Płock"},
                    {"label": "MMTS Kwidzyn", "value": "MMTS Kwidzyn"},
                    {"label": "Gwardia Opole", "value": "Gwardia Opole"}],
        multi=False,
        value="Gwardia Opole",
        style={"width": "60%"}
    ),

    html.Div(id='output container', children=[]),
    html.Br(),

    dcc.Graph(id='Goals Scorrers', figure={})

])


@app.callback(Output(component_id='Goals Scorrers', component_property='figure'),
              Input(component_id='ID_zespol', component_property='value'))
def update_graph(selected_club):
    print(selected_club)

    dff = scorrers.copy()
    dff = dff[dff['Nazwa'] == selected_club]
    dff['name'] = dff['Imie'] + ' ' + dff['Nazwisko']
    dff['field goals'] = dff['Bramki'] - dff['karne_bramki']
    dff.rename(columns={'karne_bramki': '7m goals'}, inplace=True)

    fig = px.bar(
        data_frame=dff,
        x='name',
        y=['field goals', '7m goals'],
        labels={'name': 'Player'},
    )

    fig.update_layout(yaxis_title="Goals")

    return fig


if __name__ == '__main__':

    Timer(1, open_browser).start()
    app.run_server(debug=False, port=port)
