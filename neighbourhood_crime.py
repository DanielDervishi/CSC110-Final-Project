"""A class to store neighbourhood crime data for CSC110 final project.
David, Daniel, Martin
"""


class NeighbourhoodCrime:
    """A record of crime data of a specific crime for a given neighbourhood.

    Instance attributes:
        - neighbourhood: the name of the neighbourhood as a string
        - crime_type: the crime type from this neighbourhood that we are considering
    """
    neighbourhood: str
    crime_type: str

    def __init__(self, neighbourhood: str, crime_type: str) -> None:
        """Initialize this NeighbourhoodCrimeData object with the neighbourhood and crime type.
        """
        self.neighbourhood = neighbourhood
        self.crime_type = crime_type


class NeighbourhoodCrimeOccurrences(NeighbourhoodCrime):
    """
    Stores number of crime occurrences in a neighbourhood for a certain crime in a given year and month
    """
    occurrences: dict[int, dict[int, int]]

    def __init__(self, neighbourhood: str, crime_type: str, occurrences=None) -> None:
        """Initialize this NeighbourhoodCrimeData object with the neighbourhood and, optionally, the occurrences
        data.
        """
        NeighbourhoodCrime.__init__(self, neighbourhood=neighbourhood, crime_type=crime_type)

        if occurrences is None:
            self.occurrences = {}
        else:
            self.occurrences = occurrences

    def set_data(self, year: int, month: int, occurrences: int) -> None:
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


class NeighbourhoodCrimePIndex(NeighbourhoodCrime):
    """
    Stores p-index in a neighbourhood for a certain crime in a given year and month

    Note:
        - P-Indexes are in the range of -100 to 100 exclusive.
        - -100 represents an unexpected decrease in crime
        - 100 represents an expected increase in crime
        - 0 represents expected
    """
    p_index_dict: dict[int, dict[int, int]]

    def __init__(self, neighbourhood: str, crime_type: str,
                 neighbourhood_crime_occurences: NeighbourhoodCrimeOccurrences, fit_range: tuple[int, int],
                 predict_range: tuple[int, int]) -> None:
        """Initialize this NeighbourhoodCrimePIndex object with the neighbourhood and, optionally, the occurrences
        data.

        Parameters:
            - fit_range: range of years used to make base the model
            - predict_range: range of years to make predictions with the model

        Preconditions
            - fit_range[1] < predict_range[0]

        Predict range starts after the fit range

        ADD PRECONDITIONS
        """
        NeighbourhoodCrime.__init__(self, neighbourhood=neighbourhood, crime_type=crime_type)

        self.p_index_dict = {}

        # Loop through the months
        # gen linear regression model
        # gen error
        # gen z
        # gen p
        # gen index
        # update p_index dict

    def create_list_of_range(self, start: int, end: int) -> list[int]:
        """Creates a list of consecutive integers from start to end inclusive.
        """
        lst = []

        for i in range(start, end + 1):
            lst.append(i)

        return lst

    def set_data(self, year: int, month: int, p_index: int) -> None:
        """Add a record of the number of occurrences of the crime in a given month and year.

        If there was already data for that year and month, it will be overridden.
        """
        if year not in self.p_index_dict:
            self.p_index_dict[year] = {}
        self.p_index_dict[year][month] = p_index

    def get_data(self, year: int, month: int) -> int:
        """Returns p-index of a given year and month
        """
        return self.p_index_dict[year][month]
