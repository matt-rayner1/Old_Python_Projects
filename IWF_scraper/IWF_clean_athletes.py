import csv
import pandas as pd

'''
PROGRAM NAME:       IWF_clean_athletes.py
AUTHOR:             Matthew Rayner
DEPENDENCIES:       pandas, csv
DESCRIPTION:        Cleans individual athlete .csvs produced by IWF_scrape_*.py
                    (This code is a complete mess but it does what it needs to.)
                    WARNING: only run it once per data set. Otherwise it will corrupt the data.
'''

def clean_athlete(gender, category, name):
    filename = '{}_{}_{}.csv'.format(gender, category, name)
    csvfile = open(filename)
    rows = csvfile.read().split('\n')[:-1]

    needle1 = ',Name,Class,Agegrp.,Nat.,City,Cat.,Category,Sn.,CJ.,Tot.,RPoints'
    for row in rows:
        if needle1 in row:
            rows.remove(row)

    rows.insert(0, ',Name,Class,Agegrp.,Nat.,City,Cat.,Category,Sn.,CJ.,Tot.,RPoints,Period')

    for i in range(1, len(rows)):
        rows[i] += ",0"

    for i in range(1, 4):
        needle = "Period,-,{}".format(i)
        for j in range(len(rows)-1):
            if needle in rows[j]:
                rows.remove(rows[j])
                for k in range(j, len(rows)):
                    rows[k] = rows[k][:-2]
                    rows[k] += ',{}'.format(i)

    for i in range(1,4):
        needle = "Period,-,{}".format(i)
        for row in rows:
            if needle in row:
                rows.remove(row)

    for i in range(len(rows)):
        rows[i] = rows[i][1:]

    with open(filename, 'w', newline='') as csvfile:
        for row in rows:
            csvfile.write(row + '\n')

    df = pd.read_csv(filename)
    df.rename(columns={"Name":"Competition Name", 
                    "Class":"Competition Class", 
                    "Agegrp.":"Age Group", 
                    "Nat.":"Nation", 
                    "Cat.":"Medal", 
                    "Category":"Weight Class", 
                    "Sn.":"Snatch", 
                    "CJ.":"C&J", 
                    "Tot.":"Total"}, inplace=True)
    df.to_csv(filename, index=False)

def get_names(gender, category):
    filename = filename = '{}_{}_0[OVERVIEW].csv'.format(gender, category)
    ret_file = pd.read_csv(filename)
    return ret_file.Name

genders = ["Men","Women"]
men_categs = ["55kg","61kg","67kg","73kg","81kg","89kg","96kg","102kg","109kg","+109kg"]
women_categs = ["45kg","49kg","55kg","59kg","64kg","71kg","76kg","81kg","87kg","+87kg"]

#--------------------DRIVER-------------------
for gender in genders:
    if gender == "Men":
        for man_categ in men_categs:
            names = get_names(gender, man_categ)
            for name in names:
                clean_athlete(gender, man_categ, name)
                print("cleaned '{}_{}_{}.csv'".format(gender, man_categ, name))
    if gender == "Women":
        for woman_categ in women_categs:
            names = get_names(gender, woman_categ)
            for name in names:
                clean_athlete(gender, woman_categ, name)
                print("cleaned '{}_{}_{}.csv'".format(gender, woman_categ, name))

print("Athletes are now squeaky clean")