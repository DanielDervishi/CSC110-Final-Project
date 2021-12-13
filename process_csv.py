""" Daniel Dervishi
Processes the csv for faster computations.
"""
from crime_data import CrimeData
import pandas as pd
import datetime


def get_vancouver_data(path: str, start_year_month: tuple[int, int], end_year_month: tuple[int, int]) -> CrimeData:
    """
    Return data formatted using CrimeData from crime_data_vancouver.csv.
    Data lies within the range start_year_month and end_year_month inclusive.
    Data from path must exist for all months between start_year_month and end_year_month inclusive.

    Preconditions:
        - Only to be called using a file path that was built using create_csv.
        - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    """
    df = pd.read_csv(path)
    return dataframe_to_crime_data(df, 0, 1, 2, 3, 4, start_year_month, end_year_month)


def create_csv(raw_path: str, processed_path: str, necessary_columns: list, start_year_month: tuple[int, int],
               end_year_month: tuple[int, int], remove_nan=True, fill_gaps=False) -> None:
    """
    Converts pre-processed-crime-data-vancouver.csv to a proccessed data frame with path processed_path.
    User can specify if they want gaps in data filled.
    User must specify the range of the data that they would like to collect.
    The range of the data must be within the time frame that the data was collected. In our case from
    (2003, 1) to (2021, 11) inclusive.

    Preconditions:
        - raw path is './pre-processed-crime-data-vancouver.csv'
        - necessary_columns == ['TYPE','NEIGHBOURHOOD', 'YEAR', 'MONTH']

    Code used to create 'crime_data_vancouver.csv'.
    >>> create_csv('./pre-processed-crime-data-vancouver.csv', './crime_data_vancouver.csv',\
    ['TYPE','NEIGHBOURHOOD', 'YEAR', 'MONTH'], fill_gaps=True, start_year_month=(2003,1), end_year_month=(2021,11))


    """
    # filter to only include necessary columns
    df = pd.read_csv(raw_path, usecols=necessary_columns)

    # remove all rows with empty entries
    if remove_nan:
        df.dropna(inplace=True)

    # count number occurrences for a given crimetype -> neighbourhood -> year -> month
    df = df.value_counts().reset_index().rename(columns={0: 'COUNT'})
    df = df.filter(items=['TYPE', 'NEIGHBOURHOOD', 'YEAR', 'MONTH', 'COUNT'])

    df = dataframe_to_crime_data(df, 0, 1, 2, 3, 4, start_year_month, end_year_month)

    # fill in values that have no occurrences
    if fill_gaps:
        df.fill_gaps(start_year_month, end_year_month)

    # convert the crimedata back into a dataframe
    df = crime_data_to_dataframe(df)

    # write to csv
    df.to_csv(processed_path, index=False)


def crime_data_to_dataframe(crime_data: CrimeData) -> pd.DataFrame:
    """
    Converts a CrimeData object to a pd.Dataframe object.
    """
    # create a dictionary to properly format data before converting it to csv
    formatted_dict = {'crime_type': [], 'neighbourhood': [], 'year': [], 'month': [], 'count': []}
    for crime in crime_data.crime_occurrences:
        for neighbourhood in crime_data.crime_occurrences[crime]:
            for year in crime_data.crime_occurrences[crime][neighbourhood].occurrences:
                for month in crime_data.crime_occurrences[crime][neighbourhood].occurrences[year]:
                    count = crime_data.crime_occurrences[crime][neighbourhood].occurrences[year][month]
                    if isinstance(crime, str) and isinstance(neighbourhood, str) and isinstance(year, int) \
                            and isinstance(month, int) and isinstance(count, int):
                        formatted_dict['crime_type'].append(crime)
                        formatted_dict['neighbourhood'].append(neighbourhood)
                        formatted_dict['year'].append(year)
                        formatted_dict['month'].append(month)
                        formatted_dict['count'].append(count)

    # convert the dictionary to a dataframe
    return pd.DataFrame(formatted_dict)


def dataframe_to_crime_data(df: pd.DataFrame, col_num_crime_type: int, col_num_neighbourhood: int,
                            col_num_year: int, col_num_month: int, col_num_occurrences: int,
                            start_year_month: tuple[int, int], end_year_month: tuple[int, int]) -> CrimeData:
    """
    Creates a CrimeData object using a pandas dataframe with all data available in the specified range.
    
    The dataframe must contain a corresponding column to each variables with the col_num prefix.
    Each variable with the prefix col_num must be unique.
    Each variable with the prefix col_num must be assigned to the column number that has the corresponding title
    in the dataframe.
    
    Preconditions:
        - len({col_num_crime_type, col_num_neighbourhood, col_num_year, col_num_month, col_num_occurrences}) == 5
        - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
        
    """
    crime_data = CrimeData()
    for _, row in df.iterrows():
        if date_in_range(start_year_month, end_year_month, (row[col_num_year], row[col_num_month])):
            crime_data.increment_crime(row[col_num_crime_type], row[col_num_neighbourhood],
                                       row[col_num_year], row[col_num_month], row[col_num_occurrences])

    return crime_data


def date_in_range(start_year_month: tuple[int, int],
                        end_year_month: tuple[int, int], date_year_month: tuple[int, int]) -> bool:
    """Checks if a date is between start_year_month and end_year_month inclusive

    Preconditions:
        - datetime.date(year=start_year_month[0], month=start_year_month[1], day=1) < \
        datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    """
    start = datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    end = datetime.date(year=end_year_month[0], month=end_year_month[1], day=1)
    date = datetime.date(year=date_year_month[0], month=date_year_month[1], day=1)
    return start <= date <= end
