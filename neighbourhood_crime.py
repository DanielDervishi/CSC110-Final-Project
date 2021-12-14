"""A class to store neighbourhood crime data for CSC110 final project.
David, Daniel, Martin
"""

from stat_analysis import gen_linear_regression, gen_rmsd, gen_z, gen_p, gen_pindex


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
    Stores number of crime occurrences in a neighbourhood for a certain crime in a given year and
    month.

    Instance Attributes:
        - occurrences: maps year to a dictionary of months and the dictionary of months maps to the
        number of crime occurrences in this month.
    Representation Invariants:
        - all(occurrences >= 0 for month_dict in self.occurrences.values() for occurrences in
        month_dict.values())
    """
    occurrences: dict[int, dict[int, int]]

    def __init__(self, neighbourhood: str, crime_type: str) -> None:
        """Initialize this NeighbourhoodCrimeOccurrences object with the neighbourhood and crime
        type
        """
        NeighbourhoodCrime.__init__(self, neighbourhood=neighbourhood, crime_type=crime_type)

        self.occurrences = {}

    def set_data(self, year: int, month: int, occurrences: int) -> None:
        """Add a record of the number of occurrences of the crime in a given month and year.

        If there was already data for that year and month, it will be overridden.

        Preconditions:
            - year >= 0
            - 1 <= month <= 12
            - occurrences >= 1
        """
        if year not in self.occurrences:
            self.occurrences[year] = {}
        self.occurrences[year][month] = occurrences

    def increment_data(self, year: int, month: int, occurrences: int) -> None:
        """Increment the number of occurrences in the given year and month by occurrences.

        If occurrences currently does not map year to a dictionary of months or if there is no value
        mapping month to number of occurrences, the occurrences dict is updated to be able to store
        the new data.

        Preconditions:
            - year >= 0
            - 1 <= month <= 12
            - occurrences >= 1
        """
        if year not in self.occurrences:
            self.occurrences[year] = {}

        if month not in self.occurrences[year]:
            self.occurrences[year][month] = occurrences
        else:
            self.occurrences[year][month] += occurrences

    def get_occurrences(self, month: int, years_to_get: tuple[int, int]) -> list[tuple[int, int]]:
        """Get the number of occurrences of the crime for each year in the given month. Formatted
        as a list of tuples in the form (year, occurrences).
        """
        month_data = []
        for year in range(years_to_get[0], years_to_get[1] + 1):

            # if this year has data for this month
            if month in self.occurrences[year]:

                # add the month's data to the month_data list
                month_data.append((year, self.occurrences[year][month]))
        return month_data


class NeighbourhoodCrimePIndex(NeighbourhoodCrime):
    """
    Stores p-index in a neighbourhood for a certain crime in a given year and month.

    Note:
        - P-Indexes are in the range of -100 to 100 exclusive
        - -100 represents an unexpected decrease in crime
        - 100 represents an unexpected increase in crime
        - 0 represents expected

    Instance Attributes:
        - p_index_dict: dictionary that maps a specific year to a dictionary of months which map to
        the p-value associated with this month.

    Preconditions:
        - all(-100 < p_value < 100 for month_dict in self.occurrences.values() for p_value in \
        month_dict.values())
    """
    p_index_dict: dict[int, dict[int, float]]

    def __init__(self, neighbourhood: str, crime_type: str,
                 neighbourhood_crime_occurrences: NeighbourhoodCrimeOccurrences,
                 fit_range: tuple[int, int], predict_range: tuple[int, int]) -> None:
        """Initialize this NeighbourhoodCrimePIndex object with the neighbourhood, crime_type and
        build the p_index_dict using the neighbourhood_crime_occurrences data, fit_range and
        predict_range.

        Parameters:
            - fit_range: range of years used to make the model
            - predict_range: range of years to make predictions with the model

        Preconditions
            - fit_range[1] < predict_range[0] (Predict range starts after the fit range.)

        Neighbourhood_crime_occurrences contains contiguous data from the beginning of the
        fit range to the end of the fit range.
        All months within predict_range in neighbourhood_crime_occurrences must contain entries.
        """
        NeighbourhoodCrime.__init__(self, neighbourhood=neighbourhood, crime_type=crime_type)

        self.p_index_dict = {}

        for month in range(1, 12 + 1):
            monthly_occurrences = neighbourhood_crime_occurences.get_occurrences(month, fit_range)
            month_model = gen_linear_regression(monthly_occurrences)
            rmsd = gen_rmsd(monthly_occurrences, month_model)

            for year in range(predict_range[0], predict_range[1] + 1):

                if month in neighbourhood_crime_occurrences.occurrences[year]:

                    z = gen_z(
                        neighbourhood_crime_occurrences.occurrences[year][month],
                        month_model.predict([[year]]), rmsd)

                    p = gen_p(z[0])

                    p_index = gen_pindex(p, z[1])

                    if year not in self.p_index_dict:
                        self.p_index_dict[year] = {}
                    self.p_index_dict[year][month] = p_index

    def get_data(self, year: int, month: int) -> float:
        """Returns p-index of a given year and month

        Preconditions:
            - year >= 0
            - 1 <= month <= 12
        """
        return self.p_index_dict[year][month]


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
