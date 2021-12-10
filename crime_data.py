"""A class to store all crime data for CSC110 final project.
"""
from neighbourhood_crime import NeighbourhoodCrimePIndex, NeighbourhoodCrimeOccurrences


class CrimeData:
    """Aggregation of neighbourhood crime data objects.

    Instance Attributes:
        - crime_type: dict mapping crime type to dict of neighbourhood crime data objects.
    """

    crime_occurrences: dict[str, dict[str, NeighbourhoodCrimeOccurrences]]
    crime_pindex: dict[str, dict[str, NeighbourhoodCrimePIndex]]

    def __init__(self, crime_data_param=None) -> None:
        """
        Innitializes a CrimeData object with crime_data_param if entered or with empty dict
        otherwise
        """
        if crime_data_param is None:
            self.crime_occurrences = {}
        else:
            self.crime_occurrences = crime_data_param

    def increment_crime(self, crime: str, neighbourhood: str, year: int, month: int, occurences: int) -> None:
        """Increments the number of crimes of a specific type in a specific neighbourhood in the
        given year and month by a specified amount.

        If the crime or neighbourhood has not been entered before, they are added into the crime_data dictionary.
        """

        if crime not in self.crime_occurrences:
            self.crime_occurrences[crime] = {}

        if neighbourhood not in self.crime_occurrences[crime]:
            self.crime_occurrences[crime][neighbourhood] = NeighbourhoodCrimeOccurrences(neighbourhood, crime)
            self.crime_occurrences[crime][neighbourhood].set_data(year, month, 0)

        self.crime_occurrences[crime][neighbourhood].increment_data(year, month, occurences)

    def create_pindex_data(self) -> None:
        """
        creates all the data that goes into the p-index dict
        """
