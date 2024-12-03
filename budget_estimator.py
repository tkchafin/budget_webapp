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
        html.Div(className='twelve columns', style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '5px'}, children=[
            html.H2("Variable Parameters", style={'font-family': 'Arial, sans-serif'}),

            # Mortgage Cost
            html.Div([
                html.Label("Buy/build mortgage cost ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='mortgage-cost', value=600000, type='number', step=10000),
                html.Span(" - Total mortgage amount", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Down Payment Percentage
            html.Div([
                html.Label("Target Down Payment (%)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='down-payment-percent', value=25, type='number', step=1),
                html.Span(" - Percentage of mortgage", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Minimum Annual Income
            html.Div([
                html.Label("Minimum Annual Income ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='min-annual-income', value=60000, type='number', step=1000),
                html.Span(" - Minimum combined annual income (post-tax)", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Maximum Annual Income
            html.Div([
                html.Label("Maximum Annual Income ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='max-annual-income', value=250000, type='number', step=1000),
                html.Span(" - Maximum combined annual income (post-tax)", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Rental Cost
            html.Div([
                html.Label("Rental Cost ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='rental-cost', value=1800, type='number', step=100),
                html.Span(" - Monthly rent", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Utilities
            html.Div([
                html.Label("Utilities ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='utilities', value=300, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Phone/Internet
            html.Div([
                html.Label("Phone/Internet ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='phone-internet', value=150, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Food
            html.Div([
                html.Label("Food ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='food', value=400, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Insurances
            html.Div([
                html.Label("Insurances ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='insurances', value=400, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Vehicles
            html.Div([
                html.Label("Vehicles ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='vehicles', value=400, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Childcare
            html.Div([
                html.Label("Childcare ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='childcare', value=300, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            # Other
            html.Div([
                html.Label("Other ($)", style={'font-family': 'Arial, sans-serif'}),
                dcc.Input(id='other', value=500, type='number', step=10),
                html.Span(" - Monthly cost", style={'color': 'gray', 'font-size': '12px', 'margin-left': '10px'})
            ], style={'margin-bottom': '10px'}),

            html.P("Vary these and re-generate estimates", style={'color': 'red', 'font-family': 'Arial, sans-serif'})
        ]),
    ]),

    dcc.Graph(id='estimate-chart', style={'margin-top': '20px'}),

    html.Div(id='estimate-table', className='row', style={'margin-top': '20px', 'display': 'none'})
])

# Define the callback for updating the chart and table
@app.callback(
    Output('estimate-chart', 'figure'),
    Output('estimate-table', 'children'),
    Input('mortgage-cost', 'value'),
    Input('down-payment-percent', 'value'),
    Input('min-annual-income', 'value'),  # Included here
    Input('max-annual-income', 'value'),  # Included here
    Input('rental-cost', 'value'),
    Input('utilities', 'value'),
    Input('phone-internet', 'value'),
    Input('food', 'value'),
    Input('insurances', 'value'),
    Input('vehicles', 'value'),
    Input('childcare', 'value'),
    Input('other', 'value')
)
def update_estimate(mortgage_cost, down_payment_percent, min_annual_income, max_annual_income, rental_cost, utilities, phone_internet, food, insurances, vehicles, childcare, other):
    # Ensure all input values are numeric
    mortgage_cost = float(mortgage_cost) if mortgage_cost is not None else 600000.0
    down_payment_percent = float(down_payment_percent) if down_payment_percent is not None else 25.0
    min_annual_income = float(min_annual_income) if min_annual_income is not None else 60000.0
    max_annual_income = float(max_annual_income) if max_annual_income is not None else 250000.0
    rental_cost = float(rental_cost) if rental_cost is not None else 1800.0
    utilities = float(utilities) if utilities is not None else 300.0
    phone_internet = float(phone_internet) if phone_internet is not None else 150.0
    food = float(food) if food is not None else 400.0
    insurances = float(insurances) if insurances is not None else 400.0
    vehicles = float(vehicles) if vehicles is not None else 400.0
    childcare = float(childcare) if childcare is not None else 300.0
    other = float(other) if other is not None else 500.0

    def calculate_months_to_save(annual_income):
        down_payment = mortgage_cost * (down_payment_percent / 100)
        monthly_income = annual_income / 12
        monthly_expenses = rental_cost + utilities + phone_internet + food + insurances + vehicles + childcare + other
        
        # Catch the case where income is not enough
        if monthly_income <= monthly_expenses:
            return None  # Or you could return 0 or another value indicating insufficient income
        else:
            months_to_save = down_payment / (monthly_income - monthly_expenses)
            return months_to_save

    income_levels = range(int(min_annual_income), int(max_annual_income) + 1, 5000)
    
    # Calculate months to save and filter out None values
    months_to_save_list = [calculate_months_to_save(income) for income in income_levels]
    valid_months_to_save = [months for months in months_to_save_list if months is not None]
    valid_income_levels = [income for i, income in enumerate(income_levels) if months_to_save_list[i] is not None]

    df = pd.DataFrame({
        "Annual Income (After Tax)": valid_income_levels,
        "Months to Down Payment": valid_months_to_save
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

    return fig, table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)