from dash import Dash, dcc, Output, Input, dash_table, html
import dash_bootstrap_components as dbc  # pip install dash_bootstrap_components
import plotly.express as px
import pandas as pd

# Coletando dados do Excel
df_player_season = pd.read_excel('PlayerSeason.2022.xlsx', sheet_name='PlayerSeason.2022')
df_player = pd.read_excel('Player.2022.xlsx', sheet_name='Player.2022')

# Criando os Componentes
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
mytitle = dcc.Markdown(children='# Análises Estatisticas da NFL')
mygraph = dcc.Graph(figure={})
dropdown_col = dcc.Dropdown(options=df_player_season.columns.values[8:-1],
                            value='PassingAttempts',  # Valor inicial
                            clearable=False)
dropdown_num = dcc.Dropdown(options=[10, 20, 50, 100, 200, 500],
                            value=100,  # Valor inicial
                            clearable=False)

# Menu Dropdown para filtragem por time
team_options = [{'label': team, 'value': team} for team in df_player_season['Team'].unique()]
team_options.insert(0, {'label': 'All Teams', 'value': 'All'})
dropdown_team = dcc.Dropdown(options=team_options,
                             value='All',
                             clearable=False)

# Menu Dropdown para filtragem por posição
position_options = [{'label': pos, 'value': pos} for pos in df_player_season['Position'].unique()]
position_options.insert(0, {'label': 'All Positions', 'value': 'All'})
dropdown_position = dcc.Dropdown(options=position_options,
                                 value='All',
                                 clearable=False)

# Tabela com dados dos jogadores
table = dash_table.DataTable(
    id='player-table',
    columns=[{"name": col, "id": col} for col in df_player.columns[2:]],
    data=df_player.to_dict('records'),
    style_cell={'textAlign': 'left', 'color': 'black'},
    filter_action='native',  # Permite filtrar
    sort_action='native',  # Permite sortar
    sort_mode='multi',  # Permite sortar mais de uma coluna
    page_action='native',  # Divide em paginas
    page_current=0,  # Pagina inicial
    page_size=10,  # Número de linhas por pagina
)

# Layout da Webpage
app.layout = dbc.Container([
    mytitle,
    dbc.Row([
        dbc.Col([
            dbc.Label('Escolha uma Estatística'),
            dropdown_col,
        ], width=2),
        dbc.Col([
            dbc.Label('Valores'),
            dropdown_num,
        ], width=1),
        dbc.Col([
            dbc.Label('Times'),
            dropdown_team,
        ], width=2),
        dbc.Col([
            dbc.Label('Posições'),
            dropdown_position,
        ], width=2),
    ], align='center'),
    dbc.Row([
        dbc.Col([
            mygraph,
            html.Br(),  # Espaçamento
        ], width=12),
    ], align='center'),
    dbc.Row([
        dbc.Col([
            table,
        ], width=12),
    ], align='center')
], fluid=True)


# Callbacks
@app.callback(
    Output(mygraph, component_property='figure'),
    [Input(dropdown_col, component_property='value'),
     Input(dropdown_num, component_property='value'),
     Input(dropdown_team, component_property='value'),
     Input(dropdown_position, component_property='value')]
)
def update_graph(column_name, num_values, team, position):
    filtered_df = df_player_season

    # Filtragem por time
    if team != 'All':
        filtered_df = filtered_df.loc[filtered_df['Team'] == team]

    # Filtragem por posição
    if position != 'All':
        filtered_df = filtered_df.loc[filtered_df['Position'] == position]

    fig = px.bar(filtered_df.sort_values(column_name, ascending=False).iloc[:num_values],
                 x='Name', y=column_name,
                 title=f"{column_name} - Bar Graph")

    return fig  # Retorna o grafico desejado


# Abrindo o App
if __name__ == '__main__':
    app.run_server(port=8053)
