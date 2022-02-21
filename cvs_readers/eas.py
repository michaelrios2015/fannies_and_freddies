import csv
from datetime import datetime
import psycopg2

# connects to database
conn = psycopg2.connect(
    database="fannies", user='postgres',
    password='JerryPine', host='localhost', port='5432'
)

# change this monthly
data_path = 'cvs_readers/data/input/ec220204.txt'


with open(data_path, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter='|')
    headers = next(data)

    head = []

    for row in data:

        try:
            fdonename = row[0]
            fdonecusip = row[1]
            fdtwoename = row[2]
            fdtwocusip = row[3]
            exchangeable = row[4]
            exchanged = row[5]
            date = row[6][4:8] + '-' + row[6][0:2] + '-' + row[6][2:4]

            # print(date)

            head.append([fdonename, fdonecusip, fdtwoename,
                        fdtwocusip, exchangeable, exchanged, date])

        except Exception as e:
            # we seem to get a couple of very new supers (like platinums) each month
            print(row)
            print(e)

headfields = ["fdonename", "fdonecusip", "fdtwoename", "fdtwocusip",
              "exchangeable", "exchanged", "date"]

with open('cvs_readers/data/output/eas.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(head)


# connecting to database
# what is autocommit
conn.autocommit = True
cursor = conn.cursor()

csv_file_name = 'cvs_readers/data/output/eas.cvs'
sql = "COPY eas FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))

# not sure if these are ncessary but I think they help
conn.commit()
conn.close()
