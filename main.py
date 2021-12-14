"""
main file for final project
"""
import process_csv
import heatmap_generation

if __name__ == '__main__':
    crime_data = process_csv.get_vancouver_data('./crime_data_vancouver.csv',
                                                start_year_month=(2003, 1),
                                                end_year_month=(2021, 11))
    crime_data.create_pindex_data((2014, 2019), (2020, 2021))
    heatmap_generation.generate_heatmap(crime_data)
