"""
statistical analysis
Martin and Daniel
"""
import math
from sklearn.linear_model import LinearRegression


def gen_linear_regression(raw_data: list[tuple[int, int]]) -> LinearRegression:
    """Print the linear regression for this data for the given month."""
    # Initialize the model
    model = LinearRegression()

    x_train = [[t[0]] for t in raw_data]
    y_train = [t[1] for t in raw_data]

    # Train the model
    model.fit(x_train, y_train)

    return model


def gen_rmsd(occurrences: list[tuple[int, int]], model: LinearRegression) -> float:
    """Return the RMSD of the linear regression given the month of the data
    and years that should be excluded from the calculation.

    RMSD is the standard deviation of the residuals around a regression line.
    """
    squared_sum, count = 0, 0

    for (year, num_occurrences) in occurrences:
        squared_sum += (num_occurrences - model.predict([[year]])) ** 2
        count += 1

    return math.sqrt(squared_sum / count)


def gen_z(observation: float, prediction: float, standard_deviation: float) -> tuple[float, bool]:
    """
    Generate a tuple containing:
     - A z-value based on the model's prediction and the actual observation. (How many standard
     deviations off the prediction was from the actual value)
     - Whether or not the model overestimated the result (meaning the actual value is
     less than the predicted value).
     
     observation: the actual value
     prediction: the predicted value
     standard_deviation: the standard deviation of an actual value from the corresponding predicted value

     Preconditions:
        - standard_deviation > 0

    >>> z1, overestimated1 = gen_z(5.0, 3.0, 1.0)
    >>> math.isclose(z1, 2.0) and not overestimated1
    True

    >>> z2, overestimated2 = gen_z(998.9, 1000.0, 5.0)
    >>> math.isclose(z2, 0.22) and overestimated2
    True
    """
    z = 0
    # Whether or not the observation was overestimated
    overestimated = False

    # How far off the prediction was from the observation
    deviation = observation - prediction

    # If there is standard deviation, calculate z, how many standard deviations off the prediction
    # was.
    if standard_deviation > 0:
        z = abs(deviation) / standard_deviation

    # if the observation is less than the prediction...
    if observation < prediction:
        # the observation was overestimated.
        overestimated = True

    return (z, overestimated)


def gen_p(z: float) -> float:
    """
    Generates p, the probability that the model would have predicted a result as least as extreme as
    that observed. A low p value indicates a low chance the observed result would be a predicted,
    meaning the model is likely innacurate.
    
    z: the z value to compute the p value of

    Preconditions:
        - z >= 0

    Use the empirical rule to test the correctness of the function (rounding to 1 decimal place):
    >>> p1 = gen_p(1)
    >>> math.isclose(p1 * 100, 100 - 68.27, abs_tol=0.05)
    True
    >>> p2 = gen_p(2)
    >>> math.isclose(p2 * 100, 100 - 95.45, abs_tol=0.05)
    True
    >>> p3 = gen_p(3)
    >>> math.isclose(p3 * 100, 100 - 99.74, abs_tol=0.05)
    True
    """
    #compute p using twice (times 2) the complimentary cumulative function
    p = 1 - math.erf(z / (2 ** (1 / 2)))

    return p


def gen_pindex(p: float, overestimated: bool) -> float:
    """
    Generate an index based on 1 - p to measure the probability the model is innacurate.
    p values measure the probability the model is accurate, so 1 - p is the opposite.
    Whether or not the observed value was overestimated is taken into account in order
    to make the index more dynamic; the magnitude of the index represents the probability
    the model is innacurate, and the sign of the index represents whether the innacuracy
    is due to over or underestimation.
    
    p: the p value for an observation that was compared against a predictive model/average
    overestimated: whether or not the observation the p value is based off of was over or 
    under estimated

    Example: a p value of 0.2 indicates there is a 20% chance the model is correct for that
    observation. Assume the observation value is less than the model's prediction.
    This means the model overestimated the observation.
    Computation: take the compliment of the p value, convert it into a percentage, and
    make it negative (due to overestimeation)
    Thus, the p index is -80.0
    
    Preconditions:
        - 0 <= p < 1

    >>> pindex1 = gen_pindex(0.1, False)
    >>> math.isclose(pindex1, 90.0)
    True

    >>> pindex2 = gen_pindex(0.2, True)
    >>> math.isclose(pindex2, -80.0)
    True
    """
    # take the complimentary value of the p value and convert it into the percentage
    pindex = (1 - p) * 100

    # make the p index negative if the observation it is based off of was overestimated
    if overestimated:
        pindex *= -1

    return pindex


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['neighbourhood_crime', 'sklearn.linear_model', 'math'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
