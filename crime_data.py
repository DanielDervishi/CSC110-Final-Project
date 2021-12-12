"""A class to store all crime data for CSC110 final project.
"""
from neighbourhood_crime import NeighbourhoodCrimePIndex, NeighbourhoodCrimeOccurrences


class CrimeData:
    """Aggregation of neighbourhood crime data objects.

    Instance Attributes:
        - crime_occurrences: dict mapping crime type to dict of neighbourhood crime occurrences objects.
        - crime_pindex: dict mapping crime type to dict of neighbourhood crime p-index objects.
    """

    crime_occurrences: dict[str, dict[str, NeighbourhoodCrimeOccurrences]]
    crime_pindex: dict[str, dict[str, NeighbourhoodCrimePIndex]]

    def __init__(self, crime_data_param=None) -> None:
        """
        Initializes the CrimeData object with crime_occurrences set to crime_data_param if entered or with empty dict
        otherwise.

        Parameters:
            - crime_data_param: initial value of crime_occurrences
        """
        if crime_data_param is None:
            self.crime_occurrences = {}
        else:
            self.crime_occurrences = crime_data_param
        self.crime_pindex = {}
    # def create_crime(self, crime: str, neighbourhood: str, year: int, month: int):
    #     if neighbourhood not in self.crime_occurrences[crime]:
    #         if crime not in self.crime_occurrences:
    #             self.crime_occurrences[crime] = {}
    #
    #         if neighbourhood not in self.crime_occurrences[crime]:

    def increment_crime(self, crime: str, neighbourhood: str, year: int, month: int, occurrences: int,
                        start_year_month=(2003, 1), end_year_month=(2021, 11)) -> None:
        """Increments the number of crime occurrences of a specific type in a specific neighbourhood in the
        given year and month by a specified amount.

        If the crime or neighbourhood has not been entered before, they are added into the crime_occurrences dictionary
        and the NeighbourhoodCrimeOccurrences dictionary that maps year and month to number of occurrences is
        initialized so that all values are zero.

        User can specify start_year_month and end_year_month if the range of dates in which data was collected is
        different than the range provided.

        Parameter:
            - start_year_month: tuple(int, int) in the form (year, month) where 1 <= month <= 12
            - end_year_month: tuple(int, int) in the form (year, month) where 1 <= month <= 12
        """
        if crime not in self.crime_occurrences:
            self.crime_occurrences[crime] = {}

        if neighbourhood not in self.crime_occurrences[crime]:
            self.crime_occurrences[crime][neighbourhood] = \
                NeighbourhoodCrimeOccurrences(neighbourhood, crime, start_year_month, end_year_month)
            self.crime_occurrences[crime][neighbourhood].set_data(year, month, 0)

        self.crime_occurrences[crime][neighbourhood].increment_data(year, month, occurrences)

    def create_pindex_data(self, fit_range: tuple[int, int], predict_range: tuple[int, int]) -> None:
        """
        Creates all the data that goes into the p-index dict.
        """
        for crime_type in self.crime_occurrences:
            for neighbourhood in self.crime_occurrences[crime_type]:
                if crime_type not in self.crime_pindex:
                    self.crime_pindex[crime_type] = {}
                self.crime_pindex[crime_type][neighbourhood] = \
                    NeighbourhoodCrimePIndex(neighbourhood, crime_type,
                                             self.crime_occurrences[crime_type][neighbourhood],
                                             fit_range, predict_range)
