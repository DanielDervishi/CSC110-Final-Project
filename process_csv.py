""" Daniel Dervishi
Processes the csv for faster computations.
"""
from crime_data import CrimeData
import pandas as pd
import datetime


def get_vancouver_data(path: str, start_year_month: tuple[int, int], end_year_month: tuple[int, int]) -> CrimeData:
    """
    Return data formatted using CrimeData from crime_data_vancouver.csv.
    """
    df = pd.read_csv(path)
    return dataframe_to_crime_data(df, 0, 1, 2, 3, 4, start_year_month, end_year_month)


def create_csv(raw_path: str, processed_path: str, necessary_columns: list, remove_nan=True, fill_gaps=False,
                 start_year_month=None, end_year_month=None) -> None:
    """
    code to create a new csv
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
    if start_year_month is None or end_year_month is None and fill_gaps:
        raise FillRangeNotSpecifiedError
    elif fill_gaps:
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
    creates a dataframe using the crimeData whith all data availible in the specified range.
    """
    crime_data = CrimeData()
    for _, row in df.iterrows():
        if date_in_range(start_year_month, end_year_month, (row[col_num_year], row[col_num_month])):
            crime_data.increment_crime(row[col_num_crime_type], row[col_num_neighbourhood],
                                       row[col_num_year], row[col_num_month], row[col_num_occurrences])

    return crime_data


class FillRangeNotSpecifiedError(Exception):
    """
    When creating the csv, it was specified that user wanted to fill values between start_year_month
    and end_year_month that did not already have values for number of occurrences with 0, but one or
    more of these variables was not defined.
    """


def date_in_range(start_year_month: tuple[int, int],
                        end_year_month: tuple[int, int], date_year_month: tuple[int, int]) -> bool:
    """Checks if a date is between start_year_month and end_year_month inclusive
    """
    start = datetime.date(year=start_year_month[0], month=start_year_month[1], day=1)
    end = datetime.date(year=end_year_month[0], month=end_year_month[1], day=1)
    date = datetime.date(year=date_year_month[0], month=date_year_month[1], day=1)
    return start <= date <= end
