import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from src.helpers import (
    calculate_sir_curve,
    chart_sir
)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Initial Infected: "),
                dcc.Input(id='I0', value=0.00001, type='number'),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Beta (Infection Rate): "),
                dcc.Input(id='beta', value=2.0, step=0.01, type='number'),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Gamma (Recovery Rate): "),
                dcc.Input(id='gamma', value=1.0, step=0.01, type='number'),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Time Period: "),
                dcc.Input(id='time-period', value=50, step=5, type='number'),
            ]
        )
    ],
    body=True
)


app.layout = dbc.Container(
    [
        html.H1("Basic SIR Curve"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md = 3),
                dbc.Col(dcc.Graph(id='sir-chart'), md=6)
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output(component_id='sir-chart', component_property='figure'),
    [Input(component_id='I0', component_property='value'),
     Input(component_id='beta', component_property='value'),
     Input(component_id='gamma', component_property='value'),
     Input(component_id='time-period', component_property='value')]
)
def update_sir_chart(initial_infected, selected_beta, selected_gamma, time_period):

    # Cast to float as per: https://dash.plotly.com/dash-core-components/input
    initial_infected = float(initial_infected)
    selected_beta = float(selected_beta)
    selected_gamma = float(selected_gamma)
    time_period = float(time_period)
    
    # Run Simulation
    RES, time_range, reproductive_ratio = calculate_sir_curve(I0=initial_infected,
                                                              beta=selected_beta,
                                                              gamma=selected_gamma,
                                                              ND = time_period
                                                              )

    # Generate Chart
    figure = chart_sir(simulation_results = RES,
                       time_range = time_range,
                       reproductive_ratio = reproductive_ratio
                       )

    # Return Simulation Chart
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
