# so this is slightly modified from the first script program that i use... probably did not need
# to make this it's own thing but it does not hurt

import csv
from datetime import datetime
import psycopg2

# connects to database
conn = psycopg2.connect(
    database="fannies", user='postgres',
    password='JerryPine', host='localhost', port='5432'
)


######################################################################
# changes monthly#################################################
###############################################################

data_path = 'cvs_readers/data/input/FNApril2022Collat.txt'

date = '2022-04-01'

############################################################

with open(data_path, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter='|')
    headers = next(data)

    head = []

    for row in data:

        try:

            if row[0] != 'Trust Identifier':
                cmo = row[0] + '-' + row[17]
                cusip = row[5]
                ofincmo = row[10]

                # print(cmo)
                # print(cusip)
                # print(ofincmo)

                head.append([cmo, cusip, ofincmo, date])

        except Exception as e:
            # we seem to get a couple of very new supers (like platinums) each month
            print(row)
            print(e)

# headfields = ['cmo', 'cusip', 'ofincmo']

# with open('cvs_readers/data/output/cmos.cvs', 'w', newline='') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile)

#     # writing the fields
#     csvwriter.writerow(headfields)

#     # writing the data rows
#     csvwriter.writerows(head)


###############################################################


######################################################################
# changes monthly#################################################
###############################################################


data_path = 'cvs_readers/data/input/FHApril2022Collat.txt'


with open(data_path, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter='|')
    headers = next(data)

    # head = []

    for row in data:

        try:

            if row[0] != 'Trust Identifier':

                # cmo = row[0].lstrip("0") + '-' + row[17]
                cmo = row[0] + '-' + row[17]
                cusip = row[5]
                ofincmo = row[10]

                # print(cmo)
                # print(cusip)
                # print(ofincmo)

            # break
                head.append([cmo, cusip, ofincmo, date])

        except Exception as e:
            # we seem to get a couple of very new supers (like platinums) each month
            print(row)
            print(e)

headfields = ['cmo', 'cusip', 'ofincmo', 'date']

with open('cvs_readers/data/output/cmos.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(head)


# # connecting to database
# # what is autocommit
# conn.autocommit = True
# cursor = conn.cursor()

# sql = '''
# CREATE TEMP TABLE cmosreader (
#     cmo VARCHAR,
#     cusip VARCHAR,
#     faceincmo DOUBLE PRECISION,
#     date Date
# );
# '''

# cursor.execute(sql)

# csv_file_name = 'cvs_readers/data/output/cmos.cvs'
# sql = "COPY cmosreader FROM STDIN DELIMITER ',' CSV HEADER"
# cursor.copy_expert(sql, open(csv_file_name, "r"))

# sql = '''
# INSERT INTO ofincmos
# SELECT *
# FROM cmosreader
# ON CONFLICT
# DO NOTHING;

# DROP TABLE IF EXISTS cmosreader;
# '''

# cursor.execute(sql)


# # not sure if these are ncessary but I think they help
# conn.commit()
# conn.close()
