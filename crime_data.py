"""A class to store all crime data for CSC110 final project.
Daniel, Martin
"""
from neighbourhood_crime import NeighbourhoodCrimePIndex, NeighbourhoodCrimeOccurrences
import datetime
from dateutil import relativedelta


class CrimeData:
    """Aggregation of neighbourhood crime data objects.

    Instance Attributes:
        - crime_occurrences: dict mapping crime type to dict of neighbourhood crime occurrences objects.
        - crime_pindex: dict mapping crime type to dict of neighbourhood crime p-index objects.
    """

    crime_occurrences: dict[str, dict[str, NeighbourhoodCrimeOccurrences]]
    crime_pindex: dict[str, dict[str, NeighbourhoodCrimePIndex]]

    def __init__(self) -> None:
        """
        Initializes the CrimeData object with attributes crime_occurrences: empty dict and crime_pindex:
        empty dict.
        """

        self.crime_occurrences = {}
        self.crime_pindex = {}

    def increment_crime(self, crime: str, neighbourhood: str, year: int, month: int, occurrences: int) -> None:
        """Increments the number of crime occurrences of a specific type in a specific neighbourhood in the
        given year and month by a specified amount.

        If the crime or neighbourhood has not been entered before, they are added into the
        crime_occurrences dictionary
        and the NeighbourhoodCrimeOccurrences object that contains a dictionary that maps year and
        month to number of occurrences is initialized so that all values are zero.

        Preconditions:
            - year >= 1
            - 1 <= month <= 12
            - occurrences >= 1
        """
        if crime not in self.crime_occurrences:
            self.crime_occurrences[crime] = {}

        if neighbourhood not in self.crime_occurrences[crime]:
            self.crime_occurrences[crime][neighbourhood] = \
                NeighbourhoodCrimeOccurrences(neighbourhood, crime)
            self.crime_occurrences[crime][neighbourhood].set_data(year, month, 0)

        self.crime_occurrences[crime][neighbourhood].increment_data(year, month, occurrences)

    def fill_gaps(self, start_year_month: tuple[int, int], end_year_month: tuple[int, int]):
        """
        For each crime and neighbourhood, the years and months that have no occurrences within the range
        specified as start_year_month - end_year_month have the value of the occurrences dictionary at
        each of these years and months set to zero.

        Preconditions:
            - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)

        Only fill gaps that are within the timeframe the data was collected. Only
        (2003, 01) - (2021, 11) can be filled in our case.
        """
        for crime in self.crime_occurrences.values():
            for neighbourhood in crime.values():
                set_null_in_range_to_zero(start_year_month, end_year_month, neighbourhood.occurrences)

    def create_pindex_data(self, fit_range: tuple[int, int], predict_range: tuple[int, int]) -> None:
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
                    NeighbourhoodCrimePIndex(neighbourhood, crime_type,
                                             self.crime_occurrences[crime_type][neighbourhood],
                                             fit_range, predict_range)

    def average_pindexes(self) -> float:
        """
        Returns average of the absolute value of all p-indexes
        """
        sum = 0
        count = 0
        for crime in self.crime_pindex.values():
            for neighbourhood in crime.values():
                for year in neighbourhood.p_index_dict:
                    for p_value in neighbourhood.p_index_dict[year].values():
                        sum += p_value
                        count += 1
        return sum/count

    def average_per_crime_pindexes(self) -> list[tuple[str, float]]:
        """
        Returns average of the absolute value of all p-indexes
        """
        sum = 0
        count = 0
        p_value_list = []
        for crime in self.crime_pindex:
            for neighbourhood in self.crime_pindex[crime].values():
                for year in neighbourhood.p_index_dict:
                    for p_value in neighbourhood.p_index_dict[year].values():
                        sum += p_value
                        count += 1
            p_value_list.append((crime, sum / count))
            sum = 0
            count = 0
        return p_value_list

    def average_per_crime_per_neighbourhood_pindexes(self) -> dict[str, list[tuple[str, float]]]:
        """
        Returns average of the absolute value of all p-indexes
        """
        sum = 0
        count = 0
        p_value_dict = {}
        for crime in self.crime_pindex:
            for neighbourhood in self.crime_pindex[crime].values():
                for year in neighbourhood.p_index_dict:
                    for p_value in neighbourhood.p_index_dict[year].values():
                        sum += p_value
                        count += 1
                if crime not in p_value_dict:
                    p_value_dict[crime] = []
                p_value_dict[crime].append((neighbourhood.neighbourhood, sum / count))
                sum = 0
                count = 0
        return p_value_dict


def set_null_in_range_to_zero(start_year_month: tuple[int, int], end_year_month: tuple[int, int], occurrences_dict: dict[int, dict[int, int]]) -> None:
    """
    Mutates the occurrences dictionary by setting values to zero for each year and month
    within a specified range (start_year_month, end_year_month) (inclusive) where that month
    and year does not already have a value for occurrences.
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
