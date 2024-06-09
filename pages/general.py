from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from data import df, world_df, cleaned_regions, df_c
import plotly.express as px

layout = dbc.Container([
    html.Div([
        html.H3("Общие показатели", style={"textAlign": "center"}), #изменено расположение по центру
    ], style={
              "padding": '10px 5px'}),
    
    html.Div([
        html.Div([
            html.Label("Год"),
            dcc.Input(
                id="year_input",
                type="number",
                placeholder="Введите год (1980-2020)",
                min=1980,
                max=2020
            )
            #dcc.Dropdown(
            #    id = "crossfilter-reg",
            #    options=[{"label": i, "value": i} for i in geo_regions],
            #    value = ["East Asia and Pacific"],
            #    multi=False
            #)
        ], style={"width": '60%', "display": "inline-block"}),
        
        html.Div([
            html.Label("Показатели"),
            dcc.RadioItems(
                options=[{"label": "Мобильная связь (на 100 чел.)", "value": "Cellular Subscription"},
                         {"label": "Кол-во пользователей интернета (%)", "value": "Internet Users(%)"},
                         {"label": "Широкополосная связь (на 100 чел.)", "value": "Broadband Subscription"}
                        ],
                id = "crossfilter-ind",
                labelStyle={"display": "inline-block"},
                value="Cellular Subscription"
            )   
        ], style={"width": '48%', "float": "right", "display": "inline-block"})

    ], style={"borderBottom": "thin lightgrey solid",
              "backgroundColor": "rgb(250, 250, 250)",
              "padding": "10px 50px 50px 110px"}),
    
    html.Div(dcc.Graph(id="choropleth"),
            style={"width": "49%", "display": "inline-block"}),
    html.Div(dcc.Graph(id="pie"),
             style={"width": "49%", "float": "right", "display": "inline-block"}),
    html.Div(dcc.Graph(id="dot_line"),
             style={"width": "100%", "display": "inline-block"})
], fluid=True)

@callback(
    Output('dot_line', 'figure'),
    [Input('crossfilter-ind', 'value')]
)
def update_line_chart(indication):
    figure = px.line(world_df, x='Year', y=indication, markers=True, title="Изменение выбранного показателя на мировом уровне (1980-2020)")
    return figure

@callback(
    Output('pie', 'figure'),
    [Input('crossfilter-ind', 'value'),
     Input('year_input', 'value')]
)
def update_pie_chart(indication, year):
    if year is None:
        filtered_data = cleaned_regions[(cleaned_regions['Year'] == 1980)]
        figure = px.pie(filtered_data, values=indication,
                        names=filtered_data['Entity'],
                        title=f'Значения выбранного показателя по регионам: {indication}',
                        hover_data=['Year'])
    else:
        filtered_data = cleaned_regions[(cleaned_regions['Year'] == year)]
        figure = px.pie(filtered_data, values=indication,
                        names=filtered_data['Entity'],
                        title=f'Значения выбранного показателя по регионам: {indication}',
                        hover_data=['Year'])
    return figure

@callback(
    Output('choropleth', 'figure'),
    [Input('crossfilter-ind', 'value'),
     Input('year_input', 'value')]
)
def update_choropleth(indication, year):
    if year is None:
        filtered_data = df_c[(df_c['Year'] == 1980)]
        figure = px.choropleth(filtered_data,
                               locations='Code',
                               color=indication,
                               hover_name="Entity",
                               hover_data=['Year'])
    else:
        filtered_data = df_c[(df_c['Year'] == year)]
        figure = px.choropleth(filtered_data,
                               locations='Code',
                               color=indication,
                               hover_name="Entity",
                               hover_data=['Year'])
    return figure