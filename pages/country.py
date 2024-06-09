from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, df_c, geo_regions, converted_dataset

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H3("Подробная информация о выбранной стране"),
            ], style={'textAlign': 'center'})
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col([
            html.P("Выберите регион:")
        ],width=2),
        
        dbc.Col([
            dcc.Dropdown(
                id='crossfilter-reg',
                options=[{'label': i, 'value': i} for i in geo_regions],
                value = geo_regions[0],
                multi=False
            )
        ], width=3),
        dbc.Col([
            html.P("Выберите страну:")
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-count',
                multi = False
            )
        ],width=3)
    ]),

    html.Br(),
    dbc.Row([
        html.Div(
            dcc.Slider(
                id = 'crossfilter-year',
                min = converted_dataset['Year'].min(),
                max = converted_dataset['Year'].max(),
                value = 2000,
                step = None,
                marks = {str(year):
                    str(year) for year in converted_dataset['Year'].unique()}
                ),
            style = {'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),
    ]),
    html.Br(),
    dbc.Row([
        html.Div([
            html.Label("Показатели", style={"font-size": "140%"}),
            dcc.RadioItems(
                options=[{"label": "Мобильная связь (на 100 чел.)", "value": "Cellular Subscription"},
                         {"label": "Кол-во пользователей интернета (%)", "value": "Internet Users(%)"},
                         {"label": "Широкополосная связь (на 100 чел.)", "value": "Broadband Subscription"}
                        ],
                id = "crossfilter-ind",
                labelStyle={"display": "inline-block"},
                value="Cellular Subscription",
                inline=True
            )   
        ], style={"width": '99%', "float": "right"})
    ]),

    html.Br(),
    dbc.Row ([
        dbc.Card([
            dbc.CardBody([
                html.H5("Пользователи интернета (%)"),
                html.P(
                       id='card_text1',
                       className="card-value")
            ], className="card-body-custom") 
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Среднее кол-во абонентов мобильной связи (на 100 чел.)"),
                html.P(
                       id='card_text2',
                       className="card-value")
            ], className="card-body-custom")
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Среднее кол-во абонентов фиксированной широкополосной связи (на 100 чел.)"),
                html.P(
                       id='card_text3',
                       className="card-value")
            ], className="card-body-custom")
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Численность пользователей интернета (в млн.)"),
                html.P(
                       id='card_text4',
                       className="card-value")
            ], className="card-body-custom")
        ])
    ]),

    html.Br(),
    dbc.Container([
        dbc.Row ([
            dbc.Col([
                dcc.Graph(id = 'line_chart', config={"displayModeBar": False})
            ],width=8),
            dbc.Col([
                dbc.Row([
                    dbc.Container([
                        dbc.Label("Топ-5 стран по выбранному показателю",
                                  style={"color": "black",
                                         "display": "block",
                                         "text-align": "center",
                                         "font-size": "150%"}),
                        dbc.Table(id="table1")
                    ]),
                    
                ])
            ],width=4)
        ]),
    ])

])


@callback(
    [Output('card_text1','children'),
    Output('card_text2','children'),
    Output('card_text3','children'),
    Output('card_text4','children'),
    Output('table1','children'),
    Output('line_chart', 'figure')
    ],
    [Input('crossfilter-count', 'value'),
    Input('crossfilter-reg', 'value'),
    Input('crossfilter-year', 'value'),
    Input('crossfilter-ind', 'value')
    ]
)
def update_card(country, region, year, indication):
    indication_count = converted_dataset[(converted_dataset['Region'] == region)&(converted_dataset['Year'] == year)].sort_values(by=indication, ascending=False)
    filtered_country = converted_dataset[(converted_dataset['Entity'] == country)&(converted_dataset['Year'] == year)]
    years_country_data = converted_dataset[(converted_dataset['Entity'] == country)&(converted_dataset['Year'] <= year)]
    ct1 = round(filtered_country.iloc[0]['Internet Users(%)'], 2)
    ct2 = round(filtered_country.iloc[0]['Cellular Subscription'], 2)
    ct3 = round(filtered_country.iloc[0]['Broadband Subscription'], 2)
    ct4 = round(filtered_country.iloc[0]['No. of Internet Users']/10**6, 2)
    
    top_5_countries = indication_count[['Entity', indication]].head()

    table = dbc.Table.from_dataframe(
        top_5_countries, striped=True, bordered=True, hover=True, index=False
    )
    figure = px.line(
        years_country_data,
        x="Year",
        y=indication,
        title=f"Значение показателя по стране за 1980-{year}",
        markers=True
    )
    return ct1, ct2, ct3, ct4, table, figure


@callback(
    [Output('crossfilter-count', 'options'),
    Output('crossfilter-count', 'value'),
    ],
    Input('crossfilter-reg', 'value')
)
def update_region(region):
    all_count=converted_dataset[(converted_dataset['Region'] == region)]['Entity'].unique()
    dd_count = [{'label': i, 'value': i} for i in all_count]
    dd_count_value = all_count[0]
    return dd_count, dd_count_value