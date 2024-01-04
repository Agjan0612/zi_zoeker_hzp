import pandas as pd
import openpyxl as pxl

import dash
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 5000)



vs = pd.read_excel('verstrekkingen_ex_distr.xlsx')
print(vs.head())


app = Dash(__name__)
server = app.server

app.layout = html.Div([

    html.H1('Vul het ZI nummer in en zoek het aantal verstrekkingen per maand',
            style={'textAlign':'center'}),

    dcc.Input(id='aaa',
              type='number',
              debounce=True), #debounce, zodat je eerst een 'enter' moet intoetsen voor je iets gaat zien,

    dcc.RadioItems(id='wel_geen_cf',
                   options=['GEEN CF','WEL CF'],
                   value='WEL CF'),

    html.H3('Verstrekkingen per maand in apotheek Hanzeplein',
            style={'textAlign':'center'}),

    dcc.Graph(id='verstrekkingen per maand'),


])

@callback(

    Output('verstrekkingen per maand', 'figure'),
    Input('aaa', 'value'),
    Input('wel_geen_cf', 'value')
)


def update_grafiek(zi, cf):

    filtered = vs.loc[vs['ZI'] == zi] # hier zorg je ervoor dat je in het dataframe een zi gaat zoeken

    if cf == 'WEL CF':                                                            # als de waarde in de radio items 'WEL CF' is laat je het dataframe onaangeroerd
        filtered_cf = filtered
    else:
        filtered_cf = filtered.loc[filtered['RECEPTHERKOMST'] != 'CF']            # als de waarde in de radio items iets anders is ga je zo fileren dat de CF verstrekkingen er niet in zitten

    fig = px.bar(filtered_cf,                                                     # maak een grafiek van het resultaat van je ifelse loop
                 x='MAAND-JAAR',
                 y='verstrekkingen per maand',
                 color='ZI - ETIKETNAAM',
                 title='VERSTREKKINGEN/MAAND/INCL CF')

    return fig                                                                    # laat de grafiek zien in de app van het resultaat

if __name__ == '__main__':                                                        # draai de app
    app.run(debug=True)

