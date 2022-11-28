# so this only works for the two big files fannie_cmos.csv and freddie_cmos.csv that david gave me
# it will not be hard to copy and modifit it for the monthly ones... but it does need to be done

import csv
from datetime import datetime
import psycopg2

# connects to database
conn = psycopg2.connect(
    database="fannies", user='postgres',
    password='JerryPine', host='localhost', port='5432'
)

# we will only use this code once
data_path = 'cvs_readers/data/input/Fannie_Big.csv'

with open(data_path, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    headers = next(data)

    head = []

    for row in data:

        try:
            cmo = row[2][4:]
            date = row[6]
            of = row[7]

            head.append([cmo, date, of])

        except Exception as e:
            # we seem to get a couple of very new supers (like platinums) each month
            print(row)
            print(e)

headfields = ['cmo', 'date', 'original face']


# # we will only use this code once
data_path_2 = 'cvs_readers/data/input/biglist.csv'

with open(data_path_2, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    headers = next(data)

    freddie_cmos = []

    for row in data:

        try:
            cmo = row[1][4:]
            date = row[5]
            of = row[6]

            # print(cmo)
            # print(date)
            # print(of)

            freddie_cmos.append([cmo, date, of])

        except Exception as e:
            # we seem to get a couple of very new supers (like platinums) each month
            print(row)
            print(e)


with open('cvs_readers/data/output/cmos_date.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    # csvwriter.writerows(head)

    # writing the data rows
    csvwriter.writerows(freddie_cmos)


# ###############################################################

# data_path = 'cvs_readers/data/input/freddie_cmos.csv'


# with open(data_path, newline='') as csvfile:
#     data = csv.reader(csvfile, delimiter=',')
#     headers = next(data)

#     # head = []

#     for row in data:

#         try:
#             cmo = row[0].lstrip("0") + '-' + row[1]
#             cusip = row[2]
#             ofincmo = row[10]

#             # print(cmo)
#             # print(cusip)
#             # print(ofincmo)

#         # break
#             head.append([cmo, cusip, ofincmo, date])

#         except Exception as e:
#             # we seem to get a couple of very new supers (like platinums) each month
#             print(row)
#             print(e)

# headfields = ['cmo', 'cusip', 'ofincmo', 'date']

# with open('cvs_readers/data/output/cmos.cvs', 'w', newline='') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile)

#     # writing the fields
#     csvwriter.writerow(headfields)

#     # writing the data rows
#     csvwriter.writerows(head)


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
