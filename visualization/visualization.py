# %%
import json
import networkx as nx
from networkx.readwrite import json_graph
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# %% Create a networkx graph using the json graph data
# input: string
# output: Graph
def createGraph(file):
    with open(file, 'r') as f:
        data = json.load(f)
        G = json_graph.node_link_graph(data)
    return G

# %% Create the six graph
HP_Universe = createGraph('hp_universe_graph.json')
Series = createGraph('hp_series_graph.json')
Alignment = createGraph('hp_align_graph.json')
Personality = createGraph('hp_personality_graph.json')
Affiliations = createGraph('hp_affiliation_graph.json')
Popularity = createGraph('hp_popularity_graph.json')

# %% use plotly to draw the bubble visualization based on the graph
# input: Graph, string, float, int
# output: Figure
def DrawGraph(G,cp='YlGnBu',si=1.2, min_size=5):
    
    pos = nx.random_layout(G)

    def Draw():
            node_trace = go.Scatter(x=[], 
                                    y=[], 
                                    text=[], 
                                    mode='markers+text',
                                    textfont=dict(size=6),
                                    hoverinfo='text'
                                    )

            for node in G.nodes():
                    x, y = pos[node]
                    node_trace['x'] += tuple([x])
                    node_trace['y'] += tuple([y])
                    node_trace['text'] += tuple([node])

            edge_trace = go.Scatter(x=[], 
                                    y=[],
                                    hoverinfo='text',
                                    text=[], 
                                    mode='lines')

            for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_trace['line'] = dict(width=0.5, color="#ccc")
                    edge_trace['x'] += tuple([x0, x1, None])
                    edge_trace['y'] += tuple([y0, y1, None])

            layout = go.Layout(
            title="Welcome to the Harry Potter Universe!",
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

            node_size = [(len(list(G.neighbors(node)))*si + min_size) for node in G.nodes()]
            node_trace['marker'] = dict(size=node_size, colorscale=cp, reversescale=True, color=[],
                                    line=dict(color='black',width=2))

            
            node_adjacencies = []

            for node, adjacencies in enumerate(G.adjacency()):
                    node_adjacencies.append(len(adjacencies[1]))
            node_trace.marker.color = node_adjacencies

            fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

            return fig
    return Draw()

# %% use dash create an app to show the visualization and add interactive features
app = dash.Dash(__name__)

drop_down = [
            {'label': 'All Characters', 'value': 'char'},
            {'label': 'Series', 'value': 'series'},
            {'label': 'Personality', 'value': 'pers'},
            {'label': 'Affiliations', 'value': 'affi'},
            {'label': 'Popularity', 'value': 'pop'},
            {'label': 'Alignment', 'value': 'align'}
            ]
# define the app layout
app.layout = html.Div([
    html.Button('Reset', id='reset-button', n_clicks=0),
    dcc.Dropdown(
        id='graph-dropdown',
        options=drop_down,
        value='char'
    ),
    dcc.Graph(
            id='graph',
            figure=DrawGraph(HP_Universe),
            style={'width': '800px', 'height': '600px'}
            )
])
# interactive features
@app.callback(
    Output('graph', 'figure'),
    [Input('reset-button', 'n_clicks'),
     Input('graph', 'clickData'),
     Input('graph-dropdown', 'value')]
)
def update_graph(n_clicks, clickData, value):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id']

    if triggered_id == 'graph.clickData':
        selected_node = clickData['points'][0]['text']
        if value == 'char':
            subgraph = HP_Universe.subgraph(list(HP_Universe.neighbors(selected_node))+[selected_node])
            return DrawGraph(subgraph,min_size=10)
        elif value == 'series':
            subgraph = Series.subgraph(list(Series.neighbors(selected_node))+[selected_node])
            return DrawGraph(subgraph,min_size=15,si=4)
        elif value == 'pers':
            subgraph = Personality.subgraph(list(Personality.neighbors(selected_node))+[selected_node])
            return DrawGraph(subgraph,si=5,min_size=15)
        elif value == 'affi':
            subgraph = Affiliations.subgraph(list(Affiliations.neighbors(selected_node))+[selected_node])
            return DrawGraph(subgraph,si=5,min_size=15)
        elif value == 'pop':
            subgraph = Popularity.subgraph(list(Popularity.neighbors(selected_node))+[selected_node])
            return DrawGraph(subgraph,si=5,min_size=15)
        elif value == 'align':
            subgraph = Alignment.subgraph(list(Alignment.neighbors(selected_node))+[selected_node])
            return DrawGraph(subgraph,si=5,min_size=15)
    else:
        if value == 'char':
            return DrawGraph(HP_Universe)
        elif value == 'series':
            return DrawGraph(Series, "Brwnyl", 2)
        elif value == 'pers':
            return DrawGraph(Personality,"Pinkyl",2)
        elif value == 'affi':
            return DrawGraph(Affiliations, "Aggrnyl",2)
        elif value == 'pop':
            return DrawGraph(Popularity, "Reds", 2)
        elif value == 'align':
            return DrawGraph(Alignment, "Sunset", 2)


# %% run the dash app
if __name__ == "__main__":
    app.run_server(debug=False)
