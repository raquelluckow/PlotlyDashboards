import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px
px.defaults.template = "plotly_dark"
import datetime as dt


app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'graph': '#1F3F49'
}

# styling the sidebar
HEADER_STYLE = {
    'background-color': colors['background'],
    'color': colors['text'],
    'font-family': 'Trebuchet MS',
    'text-align': 'center', 
    'margin': '0',
    'padding': '10px'
}

# styling the sidebar
SIDEBAR_STYLE = {
    'background-color': colors['background'],
    'color': colors['text'],
    'font-family': 'Trebuchet MS',
    'text-align': 'center', 
    'height': '120vh',
    'float': 'left',
    'flex': '1.5'
}

# Define the remaining vertical space for content
GRAPH_STYLE = {
    'background-color': colors['background'],
     'color': colors['text'],
     'height': '120vh',
     'flex': '8.5'
}

sidebar = html.Div([
    html.Div([
            html.Label("Initial Capital", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='initial-capital-1', type='number', value=20000, style={'width': '60px', 'margin': '0 auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
            html.Label("Interest Rate", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='interest-rate-1', type='number', value=13, style={'width': '60px', 'margin': '0 auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
            html.Label("Total Amount", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='total-amount-1', type='number', value=60000, style={'width': '60px', 'margin': '0 auto 10px auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
           html.Button("Calculate", id='generate-btn-1', n_clicks=0, style={'display': 'block', 'margin': '10px auto', 'color': colors['text'], 'background-color': '#1F3F49', 'border': 'none', 'padding': '10px 20px', 'font-size': '16px', 'font-family': 'Arial'}),
    ], style = {'padding': '30px'}),
        html.Div([
            html.Label("Initial Capital", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='initial-capital-2', type='number', value=15000, style={'width': '60px', 'margin': '0 auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
            html.Label("Interest Rate", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='interest-rate-2', type='number', value=13, style={'width': '60px', 'margin': '0 auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
            html.Label("Annual Input", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='annual-input', type='number', value=8000, style={'width': '60px', 'margin': '0 auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
            html.Label("Annual Withdrawal", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='annual-withdrawal', type='number', value=6000, style={'width': '60px', 'margin': '0 auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
            html.Label("Total Amount", style={'display': 'block', 'text-align': 'center', 'padding': '8px'}),
            dcc.Input(id='total-amount-2', type='number', value=60000, style={'width': '60px', 'margin': '0 auto 10px auto', 'display': 'block', 'text-align': 'center', 'border': '1px solid #ccc'}),
            
           html.Button("Calculate", id='generate-btn-2', n_clicks=0, style={'display': 'block', 'margin': '10px auto', 'color': colors['text'], 'background-color': '#1F3F49', 'border': 'none', 'padding': '10px 20px', 'font-size': '16px', 'font-family': 'Arial'}),
    ]),
    ],
    style = SIDEBAR_STYLE,
)

graph = html.Div([
    dcc.Graph(id ='bar-plot', style={'width': '80%', 'height': '360px'}),
    dcc.Graph(id ='bar-plot-2', style={'width': '80%', 'height': '360px'})
    ],
    style=GRAPH_STYLE)

app.layout = html.Div([
    html.H1(["Savings Calculator"], style = HEADER_STYLE),
    html.Div([
        sidebar,
        graph
    ], style = {'display': 'flex'}),
])

@app.callback(
    Output('bar-plot', 'figure'),
    [Input('generate-btn-1', 'n_clicks')],
    [State('initial-capital-1', 'value'),
     State('interest-rate-1', 'value'),
     State('total-amount-1', 'value')]
)

def update_graph(n_clicks, initial_capital, interest_rate, total_amount):
    if n_clicks is None:
        return {}  # This returns an empty figure if the button "Calculate" hasn't been clicked yet

    # Start the graph with today's date
    current_date = dt.datetime.now()

    # Convert the inserted interest rate to a decimal value
    interest_rate /= 100
    compounding_period = 12

    # Calculate the final values for each month
    values = [initial_capital]
    interests = [0]
    month_ratio = 12/compounding_period
    month_counter = 0
    while values[-1] < total_amount:
        final_value = values[-1] * (1 + interest_rate/compounding_period)
        interest = values[-1] * (interest_rate/compounding_period)
        values.append(final_value)
        interests.append(interest)
        month_counter += month_ratio

    # Create a DataFrame with calculated values and month numbers
    month_names = [(current_date.replace(month=(current_date.month + i - 1) % 12 + 1, year=current_date.year + ((current_date.month + i - 1) // 12)).strftime("%B %Y")) for i in range(int(month_counter) + 1)]
    data = {'Month': month_names, 'Value': values}
    df = pd.DataFrame(data)

    colors = {'Value': 'darkturquoise'}
    fig = px.line(df, x = 'Month', y = 'Value', labels = {'Value': 'Money'}, color_discrete_map = colors)
    fig.update_layout(legend_title_text = 'Payback options') 
    return fig

@app.callback(
    Output('bar-plot-2', 'figure'),
    [Input('generate-btn-2', 'n_clicks')],
    [State('initial-capital-2', 'value'),
     State('interest-rate-2', 'value'),
     State('annual-input', 'value'),
     State('annual-withdrawal', 'value'),
     State('total-amount-2', 'value')]
)

def update_graph_2(n_clicks, initial_capital, interest_rate, annual_input, annual_withdrawal, total_amount):
    if n_clicks is None:
        return {}  # This returns an empty figure if the button "Calculate" hasn't been clicked yet

    # Start the graph with today's date
    current_date = dt.datetime.now()

    # Convert the inserted interest rate to a decimal value
    interest_rate /= 100
    compounding_period = 12

    # Calculate the final values for each month
    values = [initial_capital]
    month_ratio = 12/compounding_period
    month_counter = 0
    while values[-1] < total_amount:
        final_value = values[-1] * (1 + interest_rate/compounding_period) + annual_input/12 - annual_withdrawal/12
        values.append(final_value)
        month_counter += month_ratio
        total_amount -= annual_withdrawal/12
        if values[-1] >= total_amount:
            break

    # Create a DataFrame with calculated values and month numbers
    month_names = [(current_date.replace(month=(current_date.month + i - 1) % 12 + 1, year = current_date.year + ((current_date.month + i - 1) // 12)).strftime("%B %Y")) for i in range(int(month_counter) + 1)]
    data = {'Month': month_names, 'Value': values}
    df = pd.DataFrame(data)

    colors = {'Value': 'lightseagreen'}
    fig = px.line(df, x = 'Month', y = 'Value', labels = {'Value': 'Money'})
    fig.update_traces(line = dict(color='darkturquoise'))
    fig.update_layout(legend_title_text = 'Payback options') 
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
