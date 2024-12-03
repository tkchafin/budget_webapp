import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table

# Initialize the app with a custom stylesheet
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout
app.layout = html.Div(children=[
    html.H1(children="Budgeting Dashboard", style={'text-align': 'center', 'font-family': 'Arial, sans-serif', 'margin-bottom': '20px'}),

    html.Div(children='''
        Explore different income and expense scenarios to achieve your homeownership goals.
    ''', style={'text-align': 'center', 'font-family': 'Arial, sans-serif', 'margin-bottom': '30px'}),

    html.Div(className='row', children=[
        html.Div(className='six columns', style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '5px'}, children=[
            html.H2("Variable Parameters", style={'font-family': 'Arial, sans-serif'}),
            html.Div([
                html.Label("Buy/build mortgage cost ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='mortgage-cost', value=600000, type='number', step=10000),
                html.Span(" - Total mortgage amount", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Target Down Payment (%)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='down-payment-percent', value=25, type='number', step=1),
                html.Span(" - Percentage of mortgage", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Rental Cost ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='rental-cost', value=1800, type='number', step=100),
                html.Span(" - Monthly rent", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Utilities ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='utilities', value=300, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Phone/Internet ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='phone-internet', value=150, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Food ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='food', value=400, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Insurances ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='insurances', value=400, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Vehicles ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='vehicles', value=400, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Childcare ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='childcare', value=300, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label("Other ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='other', value=500, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),
            html.P("Vary these and re-generate estimates", style={'color': 'red', 'font-family': 'Arial, sans-serif'})
        ]),

        html.Div(className='six columns', style={'padding': '20px'}, children=[
            html.Button('Estimate!', id='estimate-button', n_clicks=0, style={'background-color': 'gray', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'text-align': 'center', 'text-decoration': 'none', 'display': 'inline-block', 'font-size': '16px', 'border-radius': '5px', 'margin-bottom': '20px'}),

            dcc.Graph(id='estimate-chart'),
        ])
    ]),

    html.Div(id='estimate-table', className='row', style={'margin-top': '20px'})
])

# Define the callback for the button click and initial loading
@app.callback(
    Output('estimate-chart', 'figure'),
    Output('estimate-table', 'children'),
    Input('estimate-button', 'n_clicks'),
    Input('mortgage-cost', 'value'),
    Input('down-payment-percent', 'value'),
    Input('rental-cost', 'value'),
    Input('utilities', 'value'),
    Input('phone-internet', 'value'),
    Input('food', 'value'),
    Input('insurances', 'value'),
    Input('vehicles', 'value'),
    Input('childcare', 'value'),
    Input('other', 'value')
)
def update_estimate(n_clicks, mortgage_cost, down_payment_percent, rental_cost, utilities, phone_internet, food, insurances, vehicles, childcare, other):
    # This function now updates on button click OR initial load
    
    def calculate_months_to_save(annual_income, mortgage_cost, down_payment_percent, rental_cost, utilities, phone_internet, food, insurances, vehicles, childcare, other):
        down_payment = mortgage_cost * (down_payment_percent / 100)
        monthly_income = annual_income / 12
        monthly_expenses = rental_cost + utilities + phone_internet + food + insurances + vehicles + childcare + other
        months_to_save = down_payment / (monthly_income - monthly_expenses)
        return months_to_save

    income_levels = range(60000, 255000, 5000)
    df = pd.DataFrame({
        "Annual Income (After Tax)": income_levels,
        "Months to Down Payment": [calculate_months_to_save(income, mortgage_cost, down_payment_percent, rental_cost, utilities, phone_internet, food, insurances, vehicles, childcare, other) for income in income_levels]
    })

    # ggplot-style chart
    fig = px.line(df, 
                  x="Annual Income (After Tax)", 
                  y="Months to Down Payment", 
                  title="Months to Down Payment vs. Annual Income",
                  template="simple_white") 
    fig.update_traces(line=dict(color="#007bff"))
    fig.update_layout(
        xaxis_title="Annual Income (After Tax)",
        yaxis_title="Months to Down Payment",
        font_family="Arial",
        title_font_family="Arial"
    )

    # Create a Dash table from the DataFrame (with styling)
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left', 'font-family': 'Arial'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )

    return fig, table  # Return the figure and table even on initial load

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)