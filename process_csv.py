""" Daniel Dervishi
Processes the csv for faster computations.
"""
import datetime
import pandas as pd
from crime_data import CrimeData
from neighbourhood_crime import NeighbourhoodCrimeOccurrences


def get_vancouver_data(path: str, start_year_month: tuple[int, int],
                       end_year_month: tuple[int, int]) -> CrimeData:
    """
    Return data formatted using CrimeData from crime_data_vancouver.csv.
    Data lies within the range start_year_month and end_year_month inclusive.

    Data from path must exist for all months between start_year_month and end_year_month inclusive.
    Only to be called using a file path that was built using the create_csv function.

    Preconditions:
        - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    """
    df = pd.read_csv(path)
    return dataframe_to_crime_data(df, (0, 1, 2, 3, 4), start_year_month, end_year_month)


def create_csv(raw_path: str, processed_path: str, necessary_columns: list,
               start_year_month: tuple[int, int], end_year_month: tuple[int, int]) -> None:
    """
    Converts pre-processed-crime-data-vancouver.csv to a processed data frame with path
    processed_path.
    Gaps in data filled (set occurrences in a certain month to 0 if there are not previously
    recorded observations for this month).
    Observations that include empty values are not added to the new csv.

    User must specify the range of the data that they would like to collect.
    start_year_month is the beginning of the range and has the form (year, month)
    end_year_month is the end of the range and has the form (year, month)
    start_year_month must be before end_year_month
    The range of the data must be within the time frame that the data was collected. In our case
    from (2003, 1) to (2021, 11) inclusive.


    Preconditions:
        - raw_path == './pre-processed-crime-data-vancouver.csv'
        - necessary_columns == ['TYPE','NEIGHBOURHOOD', 'YEAR', 'MONTH']
        - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)

    Code used to create 'crime_data_vancouver.csv'. CAUTION: This will cause crime_data_vancouver
    to be updated when running doctests.
    >>> create_csv('./pre-processed-crime-data-vancouver.csv', './crime_data_vancouver.csv',\
    ['TYPE','NEIGHBOURHOOD', 'YEAR', 'MONTH'], start_year_month=(2003,1), \
    end_year_month=(2021,11))
    """

    # filter to only include necessary columns
    df = pd.read_csv(raw_path, usecols=necessary_columns)

    # remove all rows with empty entries
    df.dropna(inplace=True)

    # count number occurrences for a given crimetype -> neighbourhood -> year -> month
    df = df.value_counts().reset_index().rename(columns={0: 'COUNT'})
    df = df.filter(items=['TYPE', 'NEIGHBOURHOOD', 'YEAR', 'MONTH', 'COUNT'])

    df = dataframe_to_crime_data(df, (0, 1, 2, 3, 4), start_year_month, end_year_month)

    # fill in values that have no occurrences
    df.fill_gaps(start_year_month, end_year_month)

    # convert the crimedata back into a dataframe
    df = crime_data_to_dataframe(df)

    # write to csv
    df.to_csv(processed_path, index=False)


def crime_data_to_dataframe(crime_data: CrimeData) -> pd.DataFrame:
    """
    Converts a CrimeData object to a pd.Dataframe object and removes observations with empty values.
    """
    # create a dictionary to properly format data before converting it to csv
    formatted_dict = {'crime_type': [], 'neighbourhood': [], 'year': [], 'month': [], 'count': []}
    for crime in crime_data.crime_occurrences:
        for neighbourhood in crime_data.crime_occurrences[crime]:
            format_neighbourhood_data(crime_data.crime_occurrences[crime][neighbourhood],
                                      (crime, neighbourhood), formatted_dict)

    # convert the dictionary to a dataframe
    return pd.DataFrame(formatted_dict)


def dataframe_to_crime_data(df: pd.DataFrame, observation: tuple[int, int, int, int, int],
                            start_year_month: tuple[int, int], end_year_month: tuple[int, int]) \
        -> CrimeData:
    """
    Creates a CrimeData object using a pandas dataframe with all data that is available in the
    specified time frame.

    col_num_crime_type = observation[0]
    col_num_neighbourhood = observation[1]
    col_num_year = observation[2]
    col_num_month = observation[3]
    col_num_occurrences = observation[4]

    The dataframe must contain a corresponding column to each variables with the col_num prefix.
    Each variable with the prefix col_num must have a unique value.
    Each variable with the prefix col_num must be assigned to the column number that has the
    corresponding title in the dataframe.

    Preconditions:
        - len({observation[0], observation[1], observation[2], observation[3], \
        observation[4]}) == 5
        - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    """
    col_num_crime_type = observation[0]
    col_num_neighbourhood = observation[1]
    col_num_year = observation[2]
    col_num_month = observation[3]
    col_num_occurrences = observation[4]

    crime_data = CrimeData()
    for _, row in df.iterrows():
        if date_in_range(start_year_month, end_year_month, (row[col_num_year], row[col_num_month])):
            crime_data.increment_crime((row[col_num_crime_type], row[col_num_neighbourhood],
                                       row[col_num_year], row[col_num_month]),
                                       row[col_num_occurrences])

    return crime_data


def date_in_range(start_year_month: tuple[int, int],
                  end_year_month: tuple[int, int], date_year_month: tuple[int, int]) -> bool:
    """Checks if a date is between start_year_month and end_year_month inclusive

    Preconditions:
        - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)

    >>> date_in_range((2003,1), (2003,1), (2003, 1))
    True

    >>> date_in_range((2003,1), (2003, 11), (2003,12))
    False

    >>> date_in_range((2003,1), (2003, 11), (2003,2))
    True
    """
    start = datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    end = datetime.date(year=end_year_month[0], month=end_year_month[1], day=1)
    date = datetime.date(year=date_year_month[0], month=date_year_month[1], day=1)
    return start <= date <= end


def insert_non_nan(observation: tuple[str, str, int, int, int],
                   formatted_dict: dict[str, list]) -> None:
    """
    Mutates the formatted_dict to add a new observation if all entries have the correct type
    (done to remove null observations)
    Only to be used as a helper function to crime_data_to_dataframe

    Parameters:
        - observation[0]: crime name
        - observation[1]: neighbourhood
        - observation[2]: year
        - observation[3]: month
        - observation[4]: count
        - formatted_dict: properly formatted dictionary that is about to be converted to a dataframe
    """
    crime = observation[0]
    neighbourhood = observation[1]
    year = observation[2]
    month = observation[3]
    count = observation[4]
    if isinstance(crime, str) and isinstance(neighbourhood, str) and \
            isinstance(year, int) and isinstance(month, int) and \
            isinstance(count, int):
        formatted_dict['crime_type'].append(crime)
        formatted_dict['neighbourhood'].append(neighbourhood)
        formatted_dict['year'].append(year)
        formatted_dict['month'].append(month)
        formatted_dict['count'].append(count)


def format_neighbourhood_data(neighbourhood: NeighbourhoodCrimeOccurrences,
                              observation: tuple[str, str],
                              formatted_dict: dict[str, list]) -> None:
    """
    Takes the neighbourhood occurrences object and formatted dict and mutates it to ensure
    formatted dict has the proper format such that it can be converted to a dataframe.

    Helper function for crime_data_to_dataframe.

    Parameters:
        - observation[0]: crime name
        - observation[1]: neighbourhood
        - formatted_dict: properly formatted dictionary that is about to be converted to a dataframe
    """

    crime = observation[0]
    neighbourhood_name = observation[1]
    for year in neighbourhood.occurrences:
        for month in neighbourhood.occurrences[year]:
            count = \
                neighbourhood.occurrences[year][month]
            insert_non_nan((crime, neighbourhood_name, year, month, count), formatted_dict)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['datetime', 'crime_data', 'pandas', 'neighbourhood_crime'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
