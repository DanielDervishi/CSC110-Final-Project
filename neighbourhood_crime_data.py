"""A class to store neighbourhood crime data for CSC110 final project.
"""

from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go


class NeighbourhoodCrimeData:
    """A record of crime data of a specific crime for a given neighbourhood.

    Instance attributes:
        - neighbourhood: the name of the neighbourhood as a string
        - occurrences: a record of the number of occurrences of this crime by year and month.
        Formatted as a dictionary mapping years to dictionaries mapping months to occurrences
    """
    neighbourhood: str
    occurrences: dict[int, dict[int, int]]

    def __init__(self, neighbourhood: str, occurrences=None) -> None:
        """Initialize this NeighbourhoodCrimeData object with the neighbourhood and, optionally, the occurrences
        data.
        """
        self.neighbourhood = neighbourhood
        if occurrences is None:
            self.occurrences = {}
        else:
            self.occurrences = occurrences

    def add_data(self, year: int, month: int, occurrences: int) -> None:
        """Add a record of the number of occurrences of the crime in a given month and year.

        If there was already data for that year and month, it will be overridden.
        """
        if year not in self.occurrences:
            self.occurrences[year] = {}
        self.occurrences[year][month] = occurrences

    def increment_data(self, year: int, month: int, occurrences: int) -> None:
        """Increment the number of occurrences in the given year and month by occurrences."""
        if year not in self.occurrences:
            self.occurrences[year] = {}

        if month not in self.occurrences[year]:
            self.occurrences[year][month] = occurrences
        else:
            self.occurrences[year][month] += occurrences

    def get_occurrences(self, month: int) -> list[tuple[int, int]]:
        """Get the number of occurrences of the crime for each year in the given month. Formatted
        as a list of tuples in the form (year, occurrences)
        """
        data = []
        for year in self.occurrences:
            data.append((year, self.occurrences[year][month]))
        return data

    def get_linear_regression(self, month: int) -> None:
        """Print the linear regression for this data for the given month."""
        # Initialize the model
        model = LinearRegression()

        raw_data = self.get_occurrences(month)
        x_train = [[t[0]] for t in raw_data]
        y_train = [t[1] for t in raw_data]

        # Train the model
        model.fit(x_train, y_train)

        # Print the model.
        print("h(x) = {} + {}*x".format(np.round(model.intercept_, 3), np.round(model.coef_[0], 3)))

        # Get points for the line
        lower = x_train[0][0] - 1
        min_val = lower * model.coef_[0] + model.intercept_
        upper = x_train[-1][0] + 1
        max_val = upper * model.coef_[0] + model.intercept_

        # Create the figure
        scatter1 = go.Scatter(x=[t[0] for t in raw_data], y=y_train, mode='markers',
                              name=f'{self.neighbourhood} occurrences', fillcolor='green')
        scatter2 = go.Scatter(x=[lower, upper], y=[min_val, max_val], mode='lines',
                              name='Linear regression')

        fig = go.Figure()
        fig.add_trace(scatter1)
        fig.add_trace(scatter2)

        # Configure the figure
        fig.update_layout(title=f'Linear regression of number of occurrences of {self.crime_type} '
                                f'in {self.neighbourhood} in {self.month_to_str(month)}',
                          xaxis_title='Year', yaxis_title='Num occurrences')

        # Show the figure in the browser
        fig.show()
        
    
    def get_error(self, month: int, model: LinearRegression) -> float:
        """Return the error of the linear regression given the month of the data.
        Thus method uses the RMSE."""
        squared_sum, count = 0, 0

        for x, y in self.get_occurrences(month):
            squared_sum += (y - (x * model.coef_[0] + model.intercept_)) ** 2
            count += 1

        return math.sqrt(squared_sum / count)
