import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

layout = html.Div([

    html.Header(
        children=[
            html.H1("Проект", style={'textAlign': 'center'})
        ],
        style={'padding': '20px', 'backgroundColor': '#f8f9fa'}
    ),
    
    html.Section(
        children=[
            html.H2("О проекте"),
            html.P("""
                Проект предоставляет возможность посмотреть на изменение соотношения числа пользователей интернета 
                и других показателей на основе датасета, содержащего данные параметры.
            """),
            html.P("Проект содержит два раздела:"),
            html.Ol([
                html.Li([
                    html.Strong("Раздел “Общие показатели”."), 
                    html.P("""
                        В нем пользователю дашборда предоставляется возможность выбрать один из параметров, определенных 
                        в элементе radio button, а также год, за который пользователь хочет посмотреть данную информацию.
                        Информация разбита как по странам, но в общем виде, так и по регионам, и мировому уровню.
                    """)
                ]),
                html.Li([
                    html.Strong("Раздел “Показатели по странам”."), 
                    html.P("""
                        В нем пользователь дашборда может выбрать регион, а затем отдельную страну из этого региона.
                        Как в и другом разделе, предоставляется возможность выбирать интересующий параметр, изменение 
                        которого по годам показано на графике под карточками. Пользователь может выбирать при помощи 
                        ползунка период просмотра, за который интересует его данный параметр. Также приведена статистика 
                        по лидирующим странам (топ-5 стран) в выбранном регионе по выбранному пользователем показателю.
                    """)
                ])
            ]),
            html.H2("О датасете"),
            html.P("""
                Датасет имеет информацию за 
                период с 1980 по 2020 год, собрано множество стран, также имеются данные как по регионам, так и мировые.
            """),
            html.Ol([
                html.Li([
                    html.Strong("Столбец Entity"), 
                    html.P("""
                        Содержит в себе наименование страны и регионов.
                    """)
                ]),
                html.Li([
                    html.Strong("Столбец Code"), 
                    html.P("""
                        Содержит в себе кодовое наименование стран
                    """)
                ]),
                html.Li([
                    html.Strong("Столбец Year"), 
                    html.P("""
                        Содержит в себе год, за который были сняты данные.
                    """)
                ]),
                html.Li([
                    html.Strong("Столбец Cellular Subscription "), 
                    html.P("""
                        Отражает количество человек, пользующихся мобильной связью (на 100 человек).
                    """)
                ]),
                html.Li([
                    html.Strong("Столбец Internet Users(%)"), 
                    html.P("""
                        Отражает в процентном соотношении количество пользователей интернета по странам.
                    """)
                ]),
                html.Li([
                    html.Strong("Столбец No. of Internet Users"), 
                    html.P("""
                        Отражает количество интернет пользователей в стране.
                    """)
                ]),
                html.Li([
                    html.Strong("Столбец Broadband Subscription "), 
                    html.P("""
                        Отражает количество человек, пользующихся широкополосной связью (на 100 человек).
                    """)
                ]),
            ]),
            html.H2("Работа с данными"),
            html.P("""
                В исходный датасет был добавлен новый столбец для каждой страны - Region. В нем отражено, к какому региону принадлежит та или иная страна. 
            """),
            html.H2("Ссылка на датасет"),
            dbc.Button("Перейти к датасету", outline=False, color="success", href="https://www.kaggle.com/datasets/ashishraut64/internet-users")
        ],
        style={'padding': '20px'}
    )
])
