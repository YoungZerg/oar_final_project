import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, dcc, html
from pages import general, country


external_stylesheets = [dbc.themes.MINTY]
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для боковой панели. Мы используем position:fixed и фиксированную ширину
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "19rem",
    "padding": "2rem 1rem",
    "background-color": "#3AC086", # Цвет фона боковой панели меняем на тот, который больше всего подходит
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Пользователи интернета по странам", className="display-6", style={"color": "rgb(232, 232, 232)", "font-size": "230%"}),
        html.Hr(),
        html.P(
            "Дашборд выполнил студент БСБО-15-21 Преснухин Д.А.", className="lead", style={"color": "rgb(232, 232, 232)", "font-size": "200%"}
        ),
        dbc.Nav(
            [
                dbc.NavLink("Общие показатели", href="/", active="exact", style={"color": "white"}),
                dbc.NavLink("Показатели по странам", href="/page-1", active="exact", style={"color": "white"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)



app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return general.layout
    elif pathname == "/page-1":
        return country.layout
    # Если пользователь попытается перейти на другую страницу, верните сообщение 404. Мы изменим её в следующей практической.
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

app.css.append_css({"external_url": "/assets/styles.css"})

if __name__ == '__main__':
    app.run_server(debug=True)