"""A class to store all crime data for CSC110 final project.
"""
from neighbourhood_crime_data import NeighbourhoodCrimeData


class CrimeData:
    """Aggregation of neighbourhood crime data objects.

    Instance Attributes:
        - crime_type: dict mapping crime type to dict of neighbourhood crime data objects.
    """

    crime_data: dict[str, dict[str, NeighbourhoodCrimeData]]

    def __init__(self, crime_data_param=None) -> None:
        """
        Innitializes a CrimeData object with crime_data_param if entered or with empty dict
        otherwise
        """
        if crime_data_param is None:
            self.crime_data = {}
        else:
            self.crime_data = crime_data_param

    def increment_crime(self, crime: str, neighbourhood: str, year: int, month: int, occurences: int) -> None:
        """Increments the number of crimes of a specific type in a specific neighbourhood in the
        given year and month by a specified amount.

        If the crime or neighbourhood has not been entered before, they are added into the crime_data dictionary.
        """

        if crime not in self.crime_data[crime]:
            self.crime_data[crime] = {}

        if neighbourhood not in self.crime_data[crime]:
            self.crime_data[crime][neighbourhood] = NeighbourhoodCrimeData(neighbourhood)
            self.crime_data[crime][neighbourhood].add_data(year, month, 0)

        self.crime_data[crime][neighbourhood].add_data(year, month, occurences)

    # def get_occurences(self, crime: str, neighbourhood: str, year: int, month: int) -> int:
    #     """
    #     Returns number of occurences of a crime in the path (crime -> neighbourhood -> year -> month) in crime_data.
    #     """
    #     return (crime, neighbourhood, self.crime_data[crime][neighbourhood].get_occurrences(year, month))
