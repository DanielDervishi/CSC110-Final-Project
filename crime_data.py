"""
A class to store crime data both of occurrences of certain crime types
and pindex data for the data visualization and analysis.
"""
import datetime
from dateutil import relativedelta
from neighbourhood_crime import NeighbourhoodCrimePIndex, NeighbourhoodCrimeOccurrences


class CrimeData:
    """Aggregation of neighbourhood crime data objects.

    Instance Attributes:
        - crime_occurrences: dict mapping crime type to dict of neighbourhood crime occurrences
        objects.
        - crime_pindex: dict mapping crime type to dict of neighbourhood crime p-index objects.
    """

    crime_occurrences: dict[str, dict[str, NeighbourhoodCrimeOccurrences]]
    crime_pindex: dict[str, dict[str, NeighbourhoodCrimePIndex]]

    def __init__(self) -> None:
        """
        Initializes the CrimeData object with attributes crime_occurrences: empty dict and
        crime_pindex: empty dict.
        """

        self.crime_occurrences = {}
        self.crime_pindex = {}

    def increment_crime(self, observation: tuple[str, str, int, int], occurrences: int) -> None:
        """Increments the number of crime occurrences of a specific type in a specific neighbourhood
        in the given year and month by a specified amount.

        observation[0]: crime type
        observation[1]: neighbourhood
        observation[2]: year
        observation[3]: month

        If the crime/neighbourhood/year/month has not been entered before, they are added into the
        crime_occurrences dictionary.

        Preconditions:
            - observation[2] >= 1
            - 1 <= observation[3] <= 12
            - occurrences >= 1
        """
        crime = observation[0]
        neighbourhood = observation[1]
        year = observation[2]
        month = observation[3]
        occurrences: int
        if crime not in self.crime_occurrences:
            self.crime_occurrences[crime] = {}

        if neighbourhood not in self.crime_occurrences[crime]:
            self.crime_occurrences[crime][neighbourhood] = \
                NeighbourhoodCrimeOccurrences(neighbourhood, crime)
            self.crime_occurrences[crime][neighbourhood].set_data(year, month, 0)

        self.crime_occurrences[crime][neighbourhood].increment_data(year, month, occurrences)

    def fill_gaps(self, start_year_month: tuple[int, int], end_year_month: tuple[int, int]) -> None:
        """
        For each crime and neighbourhood, the years and months that have no occurrences within the
        range specified as start_year_month - end_year_month have the value of the occurrences
        dictionary at each of these years and months set to zero.

        Preconditions:
            - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)

        Only fill gaps that are within the timeframe the data was collected. Only
        (2003, 01) - (2021, 11) can be filled in our case.
        """
        for crime in self.crime_occurrences.values():
            for neighbourhood in crime.values():
                set_null_in_range_to_zero(start_year_month, end_year_month,
                                          neighbourhood.occurrences)

    def create_pindex_data(self, fit_range: tuple[int, int],
                           predict_range: tuple[int, int]) -> None:
        """
        Creates all the data that goes into the p-index dict.

        Preconditions:
            - fit_range[1] < predict_range[0]

        Each crime and neighbourhood contains contiguous occurrences data from the beginning of the
        fit range to the end of the fit range inclusive.

        For all crimes and neighbourhoods as well as all months within predict_range in the
        occurrences data must contain entries.
        """
        for crime_type in self.crime_occurrences:
            for neighbourhood in self.crime_occurrences[crime_type]:
                if crime_type not in self.crime_pindex:
                    self.crime_pindex[crime_type] = {}
                self.crime_pindex[crime_type][neighbourhood] = \
                    NeighbourhoodCrimePIndex((neighbourhood, crime_type),
                                             self.crime_occurrences[crime_type][neighbourhood],
                                             fit_range, predict_range)


def set_null_in_range_to_zero(start_year_month: tuple[int, int], end_year_month: tuple[int, int],
                              occurrences_dict: dict[int, dict[int, int]]) -> None:
    """
    Mutates the occurrences dictionary by setting values to zero for each year and month
    within a specified range (start_year_month, end_year_month) (inclusive) where that month
    and year does not already have a value for occurrences.

    >>> test_dict = {}
    >>> set_null_in_range_to_zero((2003,1),(2003,4), test_dict)
    >>> test_dict == {2003: {1: 0, 2 : 0, 3 : 0, 4: 0}}
    True

    >>> test_dict = {2003: {1: 10, 2: 5}}
    >>> set_null_in_range_to_zero((2003,1), (2003,4), test_dict)
    >>> test_dict == {2003: {1: 10, 2 : 5, 3 : 0, 4: 0}}
    True

    """
    start_date = datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    end_date = datetime.date(year=end_year_month[0], month=end_year_month[1], day=1)

    date_so_far = start_date

    while date_so_far <= end_date:

        if date_so_far.year not in occurrences_dict:
            occurrences_dict[date_so_far.year] = {}

        if date_so_far.month not in occurrences_dict[date_so_far.year]:
            occurrences_dict[date_so_far.year][date_so_far.month] = 0
        date_so_far += relativedelta.relativedelta(months=1)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['datetime', 'dateutil', 'neighbourhood_crime'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
