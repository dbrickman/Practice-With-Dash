from distutils.command.clean import clean
import dash
import dash_core_components as doc
from dash import dcc,html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import pymssql
import plotly.graph_objects as go

def cleanData():
    #CLEAN CORN DATA
    corn = pd.read_json('timeseries-CORN.json')
    df_corn = pd.DataFrame(corn.data[2]) #make above data its own data frame
    df_corn.drop(index="USD", axis=1, inplace=True) #drop USD row
    df_corn = df_corn.transpose() #make dates rows and corn the column name
    df_corn = df_corn.reset_index()
    for i in range(len(df_corn)): #most likely an error in the way the data was recorded
        if df_corn['CORN'][i] < 0.01:
            df_corn['CORN'][i] = ((df_corn['CORN'][i]) * 100)
    #CLEAN WHEAT DATA
    wheat = pd.read_json('timeseries-WHEAT.json')
    df_wheat = pd.DataFrame(wheat.data[2]) #make above data its own data frame
    df_wheat.drop(index="USD", axis=1, inplace=True) #drop USD row
    df_wheat = df_wheat.transpose()
    df_wheat = df_wheat.reset_index()
    #CLEAN SOYBEAN DATA
    soybean = pd.read_json('timeseries-SOYBEAN.json')
    df_soybean = pd.DataFrame(soybean.data[2]) #make above data its own data frame
    df_soybean.drop(index="USD", axis=1, inplace=True) #drop USD row
    df_soybean = df_soybean.transpose()
    df_soybean = df_soybean.reset_index()
    #CLEAN GOLD DATA
    gold = pd.read_json('timeseries-GOLD.json')
    df_gold = pd.DataFrame(gold.data[2]) #make above data its own data frame
    df_gold.drop(index="USD", axis=1, inplace=True) #drop USD row
    df_gold = df_gold.transpose()
    df_gold = df_gold.reset_index()
    #MERGE DATA
    df_history = df_corn.copy()
    df_history = df_history.merge(df_wheat, how='inner', on='index')
    df_history = df_history.merge(df_soybean, how='inner', on='index')
    df_history = df_history.merge(df_gold, how='inner', on='index')
    df_history.rename(columns={"index": "DATE", 'XAU': "GOLD"})

    return df_history

def createFig():
    df = cleanData()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = df['index'], 
        y=df['CORN'] * 56,
        name = 'Pounds of Corn'))

    fig.add_trace(go.Scatter(
        x=df['index'],
        y=df['SOYBEAN'] * 60, 
        name= 'Pounds of Soybeans'
    ))

    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['WHEAT'] * 2204.62,
        name = 'Pounds of Wheat'
    ))

    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['XAU'] * 28349.5,
        name = 'Milligrams of Gold'
    ))

    fig.update_layout(
        title='Price of Crops over Time',
        xaxis_title = 'Date',
        yaxis_title = 'Amount per 1 USD',
        legend_title = 'Units', 
    )

    return fig

app = dash.Dash(__name__)




#df3 = df[["Pregnancies", "Glucose"]]
#fig2 = px.scatter(df3, x="Pregnancies", y="Glucose", title="Pregancy versus Glucose")

app.layout = html.Div(children = [
    html.H1(children='Hi Classmates'),

    html.Div(children='''
        I think this is what I was supposed to do, please don't judge too harshly :)
        '''),
    
    dcc.Graph(
        id='CORN-VS-SOBEANS-VS-WHEAT',
        figure=createFig()
    ),

    #dcc.Graph(
    #        id='example-graph',
    #        figure=fig2
    #),

    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )
])

@app.callback(Output('CORN-VS-SOBEANS-VS-WHEAT', 'figure'),
              Input('interval-component', 'n_intervals'))
def UpdateData(n):
    df = cleanData()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = df['index'], 
        y=df['CORN'] * 56,
        name = 'Pounds of Corn'))

    fig.add_trace(go.Scatter(
        x=df['index'],
        y=df['SOYBEAN'] * 60, 
        name= 'Pounds of Soybeans'
    ))

    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['WHEAT'] * 2204.62,
        name = 'Pounds of Wheat'
    ))

    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['XAU'] * 28349.5,
        name = 'Milligrams of Gold'
    ))

    fig.update_layout(
        title='Price of Stuff over Time',
        xaxis_title = 'Date',
        yaxis_title = 'Amount per 1 USD',
        legend_title = 'Units of the Stuff', 
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


