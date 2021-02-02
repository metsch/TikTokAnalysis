import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import itertools
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.validators.histogram.marker.colorbar._thicknessmode
from plotly.subplots import make_subplots
import math
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

def get_graph_figure(data):
    G = nx.Graph()

    G.add_nodes_from(data["hashtag"].unique(),typ="hashtag",color="darksalmon",bipartite=0)
    G.add_nodes_from(data["uniqueId"].unique(),typ="user",color="cyan",bipartite=1)

    edge_data_t = data[data["file"]=="trump"]
    G.add_edges_from(list(zip(edge_data_t["hashtag"],edge_data_t["uniqueId"])),file="trump")

    edge_data_b = data[data["file"]=="biden"]
    G.add_edges_from(list(zip(edge_data_b["hashtag"],edge_data_b["uniqueId"])),file="biden")

    B = nx.spring_layout(G,k=0.15,iterations=50)

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
        opacity=0.5,
        mode='lines')

    node_x = []
    node_y = []
    typ = []
    node_name = []
    degrees = []
    node_color = []

    nodes = G.nodes(data=True)

    for node in G.nodes():
        x, y = B[node]
        node_x.append(x)
        node_y.append(y)
        typ.append(G.nodes()[node]["typ"])
        node_color.append(G.nodes()[node]["color"])
        

    for node,degree in G.degree():
        node_name.append(node)
        n = 5
        if(degree<n):
            degrees.append(n)
        else:
            degrees.append(degree)

    m = {
        "x":node_x,
        "y":node_y,
        "degrees":degrees,
        "typ":typ,
        "name":node_name,
        "color":node_color
    }

    data = pd.DataFrame(m)
    data["typ"] = data.typ.astype("category")
    node_trace = go.Scatter(
        x=data["x"], y=data["y"],
        mode='markers+text',
        text = data["name"],
        textfont_size=data["degrees"],
        hoverinfo='text',
        marker_color = data["color"],
        marker=dict(
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            #colorscale='Earth',
            size=data["degrees"],
            line_width=1))

    scale = 4
    node_trace.textfont.size = [i/scale if i>=scale else 1 for i in degrees]
    node_trace.textfont.color = "black"

    fig = go.Figure(data=[node_trace,edge_trace],
                layout=go.Layout(                 
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    return fig


def get_pie_figure(data):
    d = data["hashtag"].value_counts().nlargest(25).to_frame()
    fig = px.pie(d,values="hashtag",names=d.index)

    return fig

def get_table_figure(data):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data.columns)),
        cells=dict(values=[data.itemId,data.shareCount,data.playCount,data.commentCount,data.followingCount,data.followerCount,data.heartCount,
                    data.videoCount,data.uniqueId,data.nickName,data.verified,data.hashtag,data.source])
                    )])

    return fig

def get_pies(data,t,b):
    n = 8
    counts_both = data["hashtag"].value_counts().nlargest(n*n).to_frame()
    counts_b = b["hashtag"].value_counts()
    counts_t = t["hashtag"].value_counts()

    specs_temp = []
    for i in range(0,n):
        specs_temp.append({'type':'domain'})

    specs = [specs_temp]*n 
    fig = make_subplots(rows=n, cols=n, specs=specs)

    labels = ["biden","trump"]
    colors = ["blue","red"]
    
    idx = 0
    for i in range(1,n+1):
        for j in range(1,n+1):
            hashtag = str(counts_both.index[idx])

            if(hashtag in counts_t and hashtag in counts_b):
                values = [counts_b[hashtag],counts_t[hashtag]]
            else:
                values = [0,0]
            fig.add_trace(go.Pie(
                values=values,
                title = "#"+hashtag),i,j
            )
            idx=idx+1

    fig.update_traces(hoverinfo='value', textinfo='none',marker_colors=colors,labels=labels)
    fig.update(layout_title_text='Which group uses which hashtag? ',
           layout_showlegend=True)

    return fig

