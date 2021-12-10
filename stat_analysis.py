"""
statistical analysis
Martin and Daniel
"""
from neighbourhood_crime import NeighbourhoodCrimeOccurrences, NeighbourhoodCrimePIndex, NeighbourhoodCrime
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go
import math


def gen_linear_regression(occurences: NeighbourhoodCrimeOccurrences, month: int,
                          include: list[int]) -> LinearRegression:
    """Print the linear regression for this data for the given month."""
    # Initialize the model
    model = LinearRegression()

    raw_data = occurences.get_occurrences(month)
    x_train = [[t[0]] for t in raw_data if t[0] in include]
    y_train = [t[1] for t in raw_data if t[0] in include]

    # Train the model
    model.fit(x_train, y_train)

    return model


#         # Print the model.
#         print("h(x) = {} + {}*x".format(np.round(model.intercept_, 3), np.round(model.coef_[0], 3)))

#         # Get points for the line
#         lower = x_train[0][0] - 1
#         min_val = lower * model.coef_[0] + model.intercept_
#         upper = x_train[-1][0] + 1
#         max_val = upper * model.coef_[0] + model.intercept_

#         # Create the figure
#         scatter1 = go.Scatter(x=[t[0] for t in raw_data], y=y_train, mode='markers',
#                               name=f'{self.neighbourhood} occurrences', fillcolor='green')
#         scatter2 = go.Scatter(x=[lower, upper], y=[min_val, max_val], mode='lines',
#                               name='Linear regression')

#         fig = go.Figure()
#         fig.add_trace(scatter1)
#         fig.add_trace(scatter2)

#         # Configure the figure
#         fig.update_layout(title=f'Linear regression of number of occurrences of {self.crime_type} '
#                                 f'in {self.neighbourhood} in {self.month_to_str(month)}',
#                           xaxis_title='Year', yaxis_title='Num occurrences')

#         # Show the figure in the browser
#         fig.show()
def gen_error(occurences: NeighbourhoodCrimeOccurrences, month: int, include: list[int],
              model: LinearRegression) -> float:
    """Return the error of the linear regression given the month of the data
    and years that should be excluded from the calculation.
    Thus method uses the RMSE."""
    squared_sum, count = 0, 0

    for x, y in occurences.get_occurrences(month):
        if x in include:
            squared_sum += (y - model.predict(x)) ** 2
            count += 1

    return math.sqrt(squared_sum / count)


def gen_z() -> None:
    """
    generate z value
    """


def gen_p() -> None:
    """
    generates p
    :return:
    """


def gen_pindex() -> None:
    """
    generates p-index
    """
