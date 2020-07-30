import numpy as np
import scipy.integrate as spi
import plotly.graph_objects as go


def calculate_sir_curve(I0: float,
                        beta: float,
                        gamma: float,
                        TS=1.0,
                        ND=70.0) -> (np.array, np.array, float):
    """Runs SIR simulation for given parameters

    From: http://epirecip.es/epicookbook/chapters/kr08/2_1/python_original

    Args:
        I0 (float): Initial proportion of infected individuals
        beta (float): Infection rate
        gamma (float): Recovery rate
        TS (float, optional): Step size in days/periods. Defaults to 1.0.
        ND (float, optional): Number of days/periods. Defaults to 70.0.

    Returns:
        np.array, np.array, float: [description]
    """    

    # Initial susceptibles
    S0 = 1 - I0
    INPUT = (S0, I0, 0.0)

    def diff_eqs(INP, t):
        '''The main set of equations'''
        Y = np.zeros((3))
        V = INP
        Y[0] = - beta * V[0] * V[1]
        Y[1] = beta * V[0] * V[1] - gamma * V[1]
        Y[2] = gamma * V[1]
        return Y   # For odeint

    try:
        r0 = beta / gamma
    except Exception as ex:
        r0 = 0
    t_start = 0.0
    t_end = ND
    t_inc = TS
    t_range = np.arange(t_start, t_end + t_inc, t_inc)

    return spi.odeint(diff_eqs, INPUT, t_range), t_range, r0


def chart_sir(simulation_results: np.array, time_range: np.array, reproductive_ratio: float):
    """Plot Simulation Results

    Args:
        simulation_results (np.array): 3D array where each item corresponds to simulation results for:
                                            - Susceptible
                                            - Infected
                                            - Recovered
        time_range (np.array): Time periods
        reproductive_ratio (float): R0 value

    Returns:
        go.figure: Chart visualising simulation results
    """

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = time_range,
                   y = simulation_results[:, 0],
                   name = 'Susceptible'
                   )
                   )

    fig.add_trace(go.Scatter(x = time_range,
                   y = simulation_results[:, 1],
                   name = 'Infected'
                   )
                   )

    fig.add_trace(go.Scatter(x = time_range,
                   y = simulation_results[:, 2],
                   name = 'Recovered'
                   )
                   )

    fig.update_layout(
        title={
            'text': f'Reproduction Number (R0): {round(reproductive_ratio, 2)}',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title = "Time (t)",
        yaxis_title = "Population Proportion"
    )

    return fig