from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from data import df, world_df, cleaned_regions, df_c
import plotly.express as px

to_russian = {'Cellular Subscription': 'Мобильная связь',
              'Broadband Subscription': 'Широкополосная связь',
              'Internet Users(%)': 'Кол-во пользователей интернета'}

layout = dbc.Container([
    html.Div([
        html.H3("Общие показатели", style={"textAlign": "center"}), #изменено расположение по центру
    ], style={
              "padding": '10px 5px'}),
    
    html.Div([
        html.Div([
            html.Label("Год"),
            dcc.Dropdown(
                id = "year_input",
                options = [{"label": i, "value": i} for i in range(1980, 2021)],
                value=1980,
                multi=False
            )
        ], style={"width": '30%', "display": "inline-block"}),
        
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
    figure.update_layout(xaxis_title='Год', yaxis_title=to_russian[indication])
    return figure

@callback(
    Output('pie', 'figure'),
    [Input('crossfilter-ind', 'value'),
     Input('year_input', 'value')]
)
def update_pie_chart(indication, year):
    filtered_data = cleaned_regions[(cleaned_regions['Year'] == year)]
    result = filtered_data.rename(columns={'Entity': 'Регионы', 'Year': 'Год', indication: to_russian[indication]})
    figure = px.pie(result, values=to_russian[indication],
                    names=result['Регионы'],
                    title=f'Значения выбранного показателя по регионам: {to_russian[indication]}',
                    hover_data=['Год'])
    return figure

@callback(
    Output('choropleth', 'figure'),
    [Input('crossfilter-ind', 'value'),
     Input('year_input', 'value')]
)
def update_choropleth(indication, year):

    filtered_data = df_c[(df_c['Year'] == year)]
    result = filtered_data.rename(columns={'Year': 'Год', 'Code': 'Код', indication: to_russian[indication]})
    figure = px.choropleth(result,
                           locations='Код',
                           color=to_russian[indication],
                           hover_name="Entity",
                           hover_data=['Год'])
    return figure