from crime_data import CrimeData

"""
Processes the csv for faster computations.
"""
from crime_data import CrimeData
import pandas as pd

pre_processed_data = pd.read_csv('Pre-Processed-Crime-Data-Vancouver.csv')


def build_crime_data_class(pre_processed: pd.core.frame.DataFrame) -> CrimeData:
    """
    Converts the pre-processed data into data that is used to build another csv for faster
    processing.
    """
    post_processing_data = CrimeData()
    for _, row in pre_processed.iterrows():
        # row[0]: Crime Type
        # row[1]: Year
        # row[2]: Month
        # row[7]: Neighbourhood
        post_processing_data.increment_crime(row[0], row[7], row[1], row[2], 1)
    return post_processing_data

# def format_data():
#
#
# def create_csv() -> None:
