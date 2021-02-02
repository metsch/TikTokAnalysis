# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import draw_figures
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = pd.read_csv("data/processed/both.csv")
t_file = "trump_1811_1604410542"
b_file = "biden_1817_1604410734"

df_t = pd.read_csv("data/processed/"+t_file+"_exploded.csv")
df_b = pd.read_csv("data/processed/"+b_file+"_exploded.csv")

df_t["file"]="trump"
df_b["file"]="biden"

data = data.drop(["Unnamed: 0","Unnamed: 0.1","authorId","userId"],axis=1)
data.rename(columns={"hashtags":"hashtag"},inplace=True)
df_t.rename(columns={"hashtags":"hashtag"},inplace=True)
df_b.rename(columns={"hashtags":"hashtag"},inplace=True)

top_n_hashtags = data["hashtag"].value_counts().nlargest(25).to_frame(name="occurence")
top_n_hashtags["hashtag"] = top_n_hashtags.index

app.layout = html.Div(children=[
    html.H1(children='Explorative Dashboard with data from TikTok'),
    html.Div(children=[
        dash_table.DataTable(
            data=data.sample(5).to_dict("records"),
            columns=[{'name': str(i), 'id': str(i)} for i in data.columns],
            editable=True,
            style_data_conditional=[
                {
                    "if":{
                        "column_id":"uniqueId"
                    },
                    "backgroundColor":"cyan",
                    "color": "black"
                }
                ,
                                {
                    "if":{
                        "column_id":"hashtag"
                    },
                    "backgroundColor":"darksalmon",
                    "color": "black"
                },
                {
                    "if":{
                        "filter_query":"{source} = 'trump'",
                        "column_id":"source"
                    },
                    "backgroundColor":"red",
                    "color":"white"
                },
                {
                    "if":{
                        "filter_query":"{source} = 'biden'",
                        "column_id":"source"
                    },
                    "backgroundColor":"blue",
                    "color":"white"
                }
            ]
        )
    ]),
    
    html.Div(children=[
        html.H2("Bipartite Network with users and hashtags"),
        html.Div(children='''
            Change the slider to select the amount of videos from which the network graph will be generated
        '''),
        dcc.Slider(
            id="video-count-slider",
            min=10,
            max=800,
            value=100,
            marks={10:"20 videos",100:"200 videos",250:"500 videos",400:"800 videos",500:"1000 videos",800:"1600 videos"},
            step=None
        ),
        html.Div(children=[
            html.Div(
                dcc.Graph(
                    id="network-with-slider"
            ),
            style={'width': '70%', 'display': 'table-cell'}), 
            html.Div(
                id="top_n",
            style={'width': '20%', 'display': 'table-cell'}),
            ]),    
    ]),

    html.Div(children=[
        dcc.Graph(figure = draw_figures.get_pies(data,df_t,df_b))
    ])
])


@app.callback(
    Output("network-with-slider","figure"),
    Output("top_n","children"),
    Input("video-count-slider","value"))
def update_graph(video_count):

    global df_t
    global df_b
    t = df_t.sample(n=video_count,random_state=42)
    b = df_b.sample(n=video_count,random_state=42)
    data = pd.concat([t,b])

    fig1 = draw_figures.get_graph_figure(data)
    fig1.update_layout(transition_duration=2000)

    top_n_hashtags = data["hashtag"].value_counts().nlargest(13).to_frame(name="occurence")
    top_n_hashtags["hashtag"] = top_n_hashtags.index

    dt = dash_table.DataTable(
                data = top_n_hashtags.to_dict("records"),
                columns = [{'name': str(i), 'id': str(i)} for i in top_n_hashtags.columns],
                editable=True,
            ),

    return fig1,dt


if __name__ == '__main__':
    app.run_server(debug=True)