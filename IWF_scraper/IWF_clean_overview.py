import pandas as pd

'''
PROGRAM NAME:       IWF_clean_overview.py
AUTHOR:             Matthew Rayner
DEPENDENCIES:       pandas
DESCRIPTION:        Cleans *_0[OVERVIEW].csv files produced by IWF_scrape_*.py
                    WARNING: only run it once per data set. Otherwise it will corrupt the data.
'''

genders = ["Men","Women"]
men_categs = ["55kg","61kg","67kg","73kg","81kg","89kg","96kg","102kg","109kg","+109kg"]
women_categs = ["45kg","49kg","55kg","59kg","64kg","71kg","76kg","81kg","87kg","+87kg"]

for gender in genders:
    if gender == "Men":
        for man_categ in men_categs:
            filename = "{}_{}_0[OVERVIEW].csv".format(gender, man_categ)
            df = pd.read_csv(filename)
            df.drop('Status', 1, inplace=True)
            df.drop(df.columns[0], 1, inplace=True)
            df.rename(columns={" ":"Rank"}, inplace=True)
            df.to_csv(filename, index=False)
            print("Formatted {}".format(filename))
    elif gender == "Women":
        for woman_categ in women_categs:
            filename = "{}_{}_0[OVERVIEW].csv".format(gender, woman_categ)
            df = pd.read_csv(filename)
            df.drop('Status', 1, inplace=True)
            df.drop(df.columns[0], 1, inplace=True)
            df.rename(columns={" ":"Rank"}, inplace=True)
            df.to_csv(filename, index=False)
            print("Formatted {}".format(filename))

print("Overviews formatted")