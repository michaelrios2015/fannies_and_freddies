# so this  is what I will use to first read in the freddies
# it will sepreate out the pools and plats just by the fd document
# it will out them in temp tables
# then it will run the sql quiery that uses ecs file
# and spit out the false platinum cusips

import csv
import psycopg2

# connects to database
conn = psycopg2.connect(
    database="fannies", user='postgres',
    password='JerryPine', host='localhost', port='5432'
)


# change this monthly
data_path = 'cvs_readers/data/input/fd220204.txt'

# fd211206.txt looks like it is YY MM DD need to redo it so it is read like that

date = "20" + data_path[-10:-8] + "-" + \
    data_path[-8:-6] + "-" + data_path[-6:-4]

# print(date)

with open(data_path, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter='|')
    headers = next(data)

    head = []

    headplats = []

    for row in data:

        try:
            cusip = row[2]

# so we read in the fd file and sepearte pools and plats just by SRC and SRC - Mirros
            if row[34].startswith('SCR') or row[37].startswith('SCR'):

                headplats.append([cusip])

            else:

                head.append([cusip])

        except Exception as e:
            # we seem to get a couple of very new supers (like platinums) each month
            print(row)
            print(e)

headfields = ["cusip"]

# we put them both in cvs files
with open('cvs_readers/data/output/freddiesstepone.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(head)

headfields = ["cusip"]


with open('cvs_readers/data/output/freddieplatsstepone.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(headplats)


# connecting to database
# what is autocommit
conn.autocommit = True
cursor = conn.cursor()
# we put the pools and plats in temp table
sql = '''
create temporary table freddiestemp (cusip varchar);
'''
cursor.execute(sql)

# maybe there is an easier way to do this but I don't know it
csv_file_name = 'cvs_readers/data/output/freddiesstepone.cvs'
sql = "COPY freddiestemp FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


sql = '''
create temporary table freddieplatstemp (cusip varchar);
'''
cursor.execute(sql)

# maybe there is an easier way to do this but I don't know it
csv_file_name = 'cvs_readers/data/output/freddieplatsstepone.cvs'
sql = "COPY freddieplatstemp FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


# we use the ecs table to see when we have pools that have been mirrored into plats
# that is incorrect the mirrors are also pools they were just inccorectly labled
# i might need to worry about the ecs date at some point....
sql = '''
CREATE TEMP TABLE aretheseplats AS
SELECT p.cusip
FROM ecs e
INNER JOIN freddiestemp f
ON f.cusip = e.fdonecusip
INNER JOIN freddieplatstemp p
ON p.cusip = e.fdtwocusip;
'''

cursor.execute(sql)

# so we make a new cvs files with the incorrectly labbled ones
csv_file_name = 'cvs_readers/data/output/aretheseplats.cvs'
sql = "COPY aretheseplats to STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "w"))

# not sure if this is neccesary
sql = '''
DROP TABLE freddiestemp, freddieplatstemp, aretheseplats;
'''

cursor.execute(sql)

conn.commit()
conn.close()
