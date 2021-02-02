import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import itertools
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
def get_df():
    t_file = "trump_1811_1604410542"
    b_file = "biden_1817_1604410734"

    df_t = pd.read_csv("data/processed/"+t_file+"_exploded.csv")
    df_b = pd.read_csv("data/processed/"+b_file+"_exploded.csv")

    df_t["file"]="trump"
    df_b["file"]="biden"

    n = 250
    df_t = df_t.sample(n=n,random_state=42)
    df_b = df_b.sample(n=n,random_state=42)

    data = pd.concat([df_t,df_b])
    return data

def get_graph_figure():
    t_file = "trump_1811_1604410542"
    b_file = "biden_1817_1604410734"

    df_t = pd.read_csv("data/processed/"+t_file+"_exploded.csv")
    df_b = pd.read_csv("data/processed/"+b_file+"_exploded.csv")

    df_t["file"]="trump"
    df_b["file"]="biden"

    n = 250
    df_t = df_t.sample(n=n,random_state=42)
    df_b = df_b.sample(n=n,random_state=42)

    data = pd.concat([df_t,df_b])

    G = nx.MultiGraph()

    G.add_nodes_from(data["hashtags"].unique(),typ="hashtag",bipartite=0)
    G.add_nodes_from(data["uniqueId"].unique(),typ="user",bipartite=1)

    edge_data_t = data[data["file"]=="trump"]
    G.add_edges_from(list(zip(edge_data_t["hashtags"],edge_data_t["uniqueId"])),file="trump")

    edge_data_b = data[data["file"]=="biden"]
    G.add_edges_from(list(zip(edge_data_b["hashtags"],edge_data_b["uniqueId"])),file="biden")

    B = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = B[edge[0]]
        x1, y1 = B[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = B[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=list(G.nodes()),
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=1,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    degrees = [val for (node,val) in G.degree()]
    node_trace.marker.size = degrees
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Social Network',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig


def get_pie_figure():
    t_file = "trump_1811_1604410542"
    b_file = "biden_1817_1604410734"

    df_t = pd.read_csv("data/processed/"+t_file+"_exploded.csv")
    df_b = pd.read_csv("data/processed/"+b_file+"_exploded.csv")

    df_t["file"]="trump"
    df_b["file"]="biden"

    n = 250
    df_t = df_t.sample(n=n,random_state=42)
    df_b = df_b.sample(n=n,random_state=42)

    data = pd.concat([df_t,df_b])

    d = data["hashtags"].value_counts().nlargest(25).to_frame()
    fig = px.pie(d,values="hashtags",names=d.index)

    return fig

def get_pie_figure():
    t_file = "trump_1811_1604410542"
    b_file = "biden_1817_1604410734"

    df_t = pd.read_csv("data/processed/"+t_file+"_exploded.csv")
    df_b = pd.read_csv("data/processed/"+b_file+"_exploded.csv")

    df_t["file"]="trump"
    df_b["file"]="biden"

    n = 250
    df_t = df_t.sample(n=n,random_state=42)
    df_b = df_b.sample(n=n,random_state=42)

    data = pd.concat([df_t,df_b])

    d = data["hashtags"].value_counts().nlargest(25).to_frame()
    fig = px.pie(d,values="hashtags",names=d.index)

    return fig
