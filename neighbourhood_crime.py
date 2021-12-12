"""A class to store neighbourhood crime data for CSC110 final project.
David, Daniel, Martin
"""
import datetime
from dateutil import relativedelta


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
    Stores number of crime occurrences in a neighbourhood for a certain crime in a given year and month.
    """
    occurrences: dict[int, dict[int, int]]

    def __init__(self, neighbourhood: str, crime_type: str, start_year_month: tuple[int, int],
                 end_year_month: tuple[int, int]) -> None:
        """Initialize this NeighbourhoodCrimeOccurrences object with the neighbourhood, crime_type,
        optionally, the occurrences data.

        Initializes the occurrences dictionary with initial values of zero for each year and month
    within a specified range (inclusive) by mutating it from (start_year_month, end_year_month)
        """
        NeighbourhoodCrime.__init__(self, neighbourhood=neighbourhood, crime_type=crime_type)

        self.occurrences = {}
        start_date = datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
        end_date = datetime.date(year=end_year_month[0], month=end_year_month[1], day=1)

        date_so_far = start_date

        while date_so_far <= end_date:
            if date_so_far.year not in self.occurrences:
                self.occurrences[date_so_far.year] = {}
            self.occurrences[date_so_far.year][date_so_far.month] = 0
            date_so_far += relativedelta.relativedelta(months=1)

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


import stat_analysis


class NeighbourhoodCrimePIndex(NeighbourhoodCrime):
    """
    Stores p-index in a neighbourhood for a certain crime in a given year and month.

    Note:
        - P-Indexes are in the range of -100 to 100 exclusive
        - -100 represents an unexpected decrease in crime
        - 100 represents an unexpected increase in crime
        - 0 represents expected
    """
    p_index_dict: dict[int, dict[int, float]]

    def __init__(self, neighbourhood: str, crime_type: str,
                 neighbourhood_crime_occurrences: NeighbourhoodCrimeOccurrences, fit_range: tuple[int, int],
                 predict_range: tuple[int, int]) -> None:
        """Initialize this NeighbourhoodCrimePIndex object with the neighbourhood, crime_type and build the
        p_index_dict using the neighbourhood_crime_occurrences data, fit_range and predict_range.

        Parameters:
            - fit_range: range of years used to make the model
            - predict_range: range of years to make predictions with the model

        Preconditions
            - fit_range[1] < predict_range[0]

        Predict range starts after the fit range.

        ADD PRECONDITIONS
        """
        NeighbourhoodCrime.__init__(self, neighbourhood=neighbourhood, crime_type=crime_type)

        self.p_index_dict = {}

        for month in range(1, 12 + 1):
            month_model = stat_analysis.gen_linear_regression(neighbourhood_crime_occurrences, month, fit_range)
            rmsd = stat_analysis.gen_rmsd(neighbourhood_crime_occurrences, month, fit_range, month_model)
            for year in range(predict_range[0], predict_range[1] + 1):
                if month in neighbourhood_crime_occurrences.occurrences[year]:
                    z = stat_analysis.gen_z(neighbourhood_crime_occurrences.occurrences[year][month],
                              month_model.predict([[year]]), rmsd)
                    p = stat_analysis.gen_p(z[0])
                    p_index = stat_analysis.gen_pindex(p, z[1])
                    if year not in self.p_index_dict:
                        self.p_index_dict[year] = {}
                    self.p_index_dict[year][month] = p_index

    def create_list_of_range(self, start: int, end: int) -> list[int]:
        """Creates a list of consecutive integers from start to end inclusive.
        """
        lst = []

        for i in range(start, end + 1):
            lst.append(i)

        return lst

    def set_data(self, year: int, month: int, p_index: int) -> None:
        """Record p_index of a given year and month.

        If there was already data for that year and month, it will be overridden.
        """
        if year not in self.p_index_dict:
            self.p_index_dict[year] = {}
        self.p_index_dict[year][month] = p_index

    def get_data(self, year: int, month: int) -> int:
        """Returns p-index of a given year and month
        """
        return self.p_index_dict[year][month]
