import csv
from datetime import datetime
import psycopg2

# connects to database
conn = psycopg2.connect(
    database="fannies", user='postgres',
    password='JerryPine', host='localhost', port='5432'
)

# change this monthly will they always be named for this
data_path = ['cvs_readers/data/input/collateral_items_giant_FHR.csv',
             'cvs_readers\data\input\collateral_items_mega_FNM.csv',
             'cvs_readers\data\input\collateral_items_super_FHR.csv',
             'cvs_readers\data\input\collateral_items_super_FNM.csv']

date = '2021-06-01'

####################################################################
# changes stop
####################################

for file in data_path:

    filename = file[-13:-4]

    if filename[0] == '_':
        filename = filename[1:]

    print(filename)

    with open(file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        # just skips the head I believe
        headers = next(data)

        body = []

        for row in data:

            try:
                platcusip = row[0]
                poolcusip = row[3]
                ofinplat = row[9]

                # print(date)

                body.append([platcusip, poolcusip, ofinplat, date])

            except Exception as e:
                # we seem to get a couple of very new supers (like platinums) each month
                print(row)
                print(e)

    headfields = ["platcusip", "poolcusip", "ofinplat", "date"]

    with open('cvs_readers/data/output/' + filename, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(headfields)

        # writing the data rows
        csvwriter.writerows(body)


# connecting to database
# what is autocommit
conn.autocommit = True
cursor = conn.cursor()


sql = '''
CREATE TEMP TABLE  platinumsreader (
    platcusip VARCHAR,
    poolcusip VARCHAR,
    ofinplat DOUBLE PRECISION, 
    date DATE
);
'''

cursor.execute(sql)


csv_file_name = 'cvs_readers/data/output/giant_FHR'
sql = "COPY platinumsreader FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


csv_file_name = 'cvs_readers/data/output/mega_FNM'
sql = "COPY platinumsreader FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


csv_file_name = 'cvs_readers/data/output/super_FHR'
sql = "COPY platinumsreader FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


csv_file_name = 'cvs_readers/data/output/super_FNM'
sql = "COPY platinumsreader FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


sql = '''
INSERT INTO platinums
SELECT * 
FROM platinumsreader
ON CONFLICT
DO NOTHING;
'''

cursor.execute(sql)


# not sure if these are ncessary but I think they help
conn.commit()
conn.close()
