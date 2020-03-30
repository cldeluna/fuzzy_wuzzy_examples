#!/usr/bin/python -tt
# Project: fuzzy_wuzzy_examples
# Filename: match_addr.py
# claudia
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "3/21/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import pandas as pd
import re
import os
from fuzzywuzzy import fuzz, process


def df_from_excel(path):
    """
    Create Pandas Data Frame from given Excel file
    :param path:
    :return:  Pandas Data Frame from Excel file
    """

    try:
        data_frame = pd.read_excel(path)

    except IOError:
        exit(f"ERROR!!! Failed to read Excel file: \n\t{path}\nABORTING PROGRAM Execution."
             f"\nConfirm a valid file and correct path have been provided.")

    # Return the data frame object created from the Excel file
    return(data_frame)


def get_series_match(row_val, args=[]):
    """
    This function takes in the current value of the pandas series and lookup series cast as a list in args
    The function iterates over the provided series in args and looks for a fuzzy match with the provided row_val
    If a token sort match is found greater than or equal to a score of 50 that match value is returned 
    """
    match_value = ''
    stdout_details = True
    # print(f"args is {args} \n len of args is {len(args)}")

    for s in args:
        if stdout_details:
            print(f">>>>>>>>>>>>> Comparing row value {row_val} with additional detail series value {s}\n")
        if re.search(s, row_val , re.IGNORECASE):
            if stdout_details:
                print(f"\tExact Match Found for row value {row_val} with series value {s}!")
            match_value = s
            # You found an exact match, break out of the for loop
            break
        # Assuming and exact match failed, proceed with the basic fuzzy wuzzy comparisons
        ratio = fuzz.ratio(s.lower(), row_val.lower())
        pratio = fuzz.partial_ratio(s.lower(), row_val.lower())
        token_sort_ratio = fuzz.token_sort_ratio(s.lower(), row_val.lower())
        if stdout_details:
            print(f"\t\tFuzzy Ratio: \t{ratio}")
            print(f"\t\tFuzzy Partial Ratio: \t{pratio}")
            print(f"\t\tFuzzy Token Sort Ratio: \t{token_sort_ratio} of type {type(token_sort_ratio)}\n")

        if token_sort_ratio >= 50:
            if stdout_details:
                print(f"\n\tFuzzy Match Found for row: \n\t\t{row_val} \n\twith series value:\n\t\t{s} \n\twith Fuzzy Token Sort Ratio of {token_sort_ratio}!")
            match_value = s
            # You found a match, break out of the for loop
            # break
    if not match_value:
        print(f"\n\tNo match found for {s}")
        match_value = "No match found"
    else:
        print(f"Match Value is: {match_value}")

    return match_value


def main():

    # Set a variable to enable print statements
    stdout_details = False

    # Create a Data Frame from the Source Excel File
    df_src = df_from_excel(arguments.source_file)
    # Create a Data Frame from the Additional Details Excel File
    df_det = df_from_excel(arguments.detail_file)

    # Print the resulting data frames
    if stdout_details:
        print(f"\n=======================\nDisplay the two data frames...")
        # Print the Source Data Frame
        print(f"\nSource Data Frame from {arguments.source_file}")
        print(df_src)
        # print(df_src.describe())
        print(f"Columns: {df_src.columns.values}")

        # Print the Details data frame
        print(f"\nDetails Data Frame from {arguments.detail_file}")
        print(df_det)
        # print(df_det.describe())
        print(f"Columns: {df_det.columns.values}")
        print(f"\n=======END of DATA FRAME DISPLAY================\n")

    # Add a new column "Full_Address" to the Source data frame which has the "Address" information form the additional details data frame
    # This new column will be used in the Pandas merge 
    df_src['Full_Address'] = df_src['Address'].apply(get_series_match, args=[df_det['Address']])
    # print(df_src)
    #
    # Create a new data frame df_merged which combines the src and det data frames and uses the "Full_Address" column in the source data frame and the
    # "Address" column in the additional details data as keys to merge the data frames. 
    # The "how" option tells the merge action to merge based on keys in the "left" or df_src data frame.  This is effectively saying look up all the rows in the left (df_src) data frame in the right (df_det) data frame
    # The suffix option (default is suffixes=('_x', '_y')) will apply the suffix you provde so you the data frame origin of any duplicat columns
    # df_merged = pd.merge(df_src, df_det[['Address','Complex Name','Postal Code', 'State_Province', 'URL']], left_on="Full_Address", right_on="Address", how="left", suffixes=('_src', '_det'))
    df_merged = pd.merge(df_src, df_det, left_on="Full_Address", right_on="Address", how="left", suffixes=('_src', '_det'))
    #
    if stdout_details:
        # Set the display options so that all columns print
        pd.set_option('display.max_columns', None)
        print(f"\n\n+++++++++++++++++++++++++++\n++++ Merged Data Frames\n")
        print(df_merged)
        print("\n\n++++ Display Key Columns Only\n")
        print(df_merged[["Complex Name", "Full_Address", "URL"]])
        print(f"\n+++++++++++END OF MERGED DISPLAY++++++++++++++++\n")

    # Save output to an Excel file
    all_data_fn = "DSN_Complex_Lists_COMBINED"
    cwd = os.getcwd()
    df_merged.to_excel(f"{all_data_fn}.xlsx")
    df_merged.to_json(f"{all_data_fn}.json", orient="records")

    print(f"\nJSON file {all_data_fn}.json")
    print(f"\nExcel file {all_data_fn}.xlsx")
    print(f"\nSAVED in: {cwd}\n")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python lookup_details.py' ")

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-s', '--source_file', help='Source Excel File',
                        action='store',
                        default="DSN_Complex_List.xlsx")
    parser.add_argument('-d', '--detail_file', help='Excel File with additional details needed in Source Data',
                        action='store',
                        default="DSN_Complex_Details.xlsx")
    arguments = parser.parse_args()
    main()
