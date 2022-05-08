import csv
from datetime import datetime
import psycopg2

# connects to database
conn = psycopg2.connect(
    database="fannies", user='postgres',
    password='JerryPine', host='localhost', port='5432'
)

# change this monthly
data_path = 'cvs_readers/data/input/FNM_MF_202204.txt'

date = data_path[-10:-6] + "-" + data_path[-6:-4] + "-01"

with open(data_path, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter='|')
    headers = next(data)

    head = []
    body = []

    for row in data:

        # this needs to be changed
        if row[34] != 'SCR' and row[37] != 'SCR':
            # row[34] != 'SCR' or row[37] != 'SCR':
            # print(row[34])
            # print(row[37])
            # i = 0
            # for part in row:
            #     print(i)
            #     print(part)
            #     i = i + 1
            # break

            try:
                cusip = row[2]
                name = row[1]
                indicator = row[0]
                issuedate = row[11]
                maturitydate = row[12]
                # if row[14] == '':
                #     originalface = 0
                # else:
                originalface = float(row[14])

                # print(cusip)
                # print(name)
                # print(indicator)
                # print(issuedate)
                # print(maturitydate)
                # print(originalface)

                end_date = datetime(int(maturitydate[2:6]), int(
                    maturitydate[0:2]), 1)

                start_date = datetime(int(issuedate[4:8]), int(
                    issuedate[0:2]), int(issuedate[2:4]))

                # print(start_date)

                # print(end_date)

                # print(end_date.strftime("%c"))

                num_months = (end_date.year - start_date.year) * \
                    12 + (end_date.month - start_date.month)

                # print(num_months)

                istbaelig = 'none'

                if originalface >= 250000 and num_months <= 181 and num_months > 120 and (indicator == 'CN' or indicator == 'CI'):

                    istbaelig = '15 year'

                elif originalface >= 250000 and num_months > 181 and num_months <= 361 and (indicator == 'CL' or indicator == 'CT'):

                    istbaelig = '30 year'

                # print(istbaelig)

                head.append([cusip, name, indicator, start_date.date(),
                            end_date.date(), originalface, istbaelig])

                coupon = row[16]
                remainingbalance = row[15]
                factor = row[4]
                gwac = row[18]
                wam = row[22]
                wala = row[23]

                body.append([cusip, coupon, remainingbalance,
                            factor, gwac, wam, wala, date, 0, 0])

            except Exception as e:
                # we seem to get a couple of very new supers (like platinums) each month
                print(row)
                print(e)

headfields = ["cusip", "name", "indicator", "issuedate",
              "maturitydate", "originalface", "istbaelig"]

with open('cvs_readers/data/output/fannies.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(head)


bodyFields = ["cusip", "coupon", "remainingbalance",
              "factor", "gwac", "wam", "wala", "date", 'cfincmos', 'cfinplats']

with open('cvs_readers/data/output/fanniebodies.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(bodyFields)

    # writing the data rows
    csvwriter.writerows(body)


# connecting to database
# what is autocommit
conn.autocommit = True
cursor = conn.cursor()

csv_file_name = 'cvs_readers/data/output/fanniebodies.cvs'
sql = "COPY fanniebodies FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))

sql = '''
create temporary table fanniestemp (cusip varchar, name varchar , indicator varchar, issuedate date, maturitydate date, originalface double precision, istbaelig istbaelig_type);
'''
cursor.execute(sql)

# maybe there is an easier way to do this but I don't know it
csv_file_name = 'cvs_readers/data/output/fannies.cvs'
sql = "COPY fanniestemp FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


sql = '''
INSERT INTO fannies (cusip, name, indicator, issuedate, maturitydate, originalface, istbaelig)
SELECT cusip, name, indicator, issuedate, maturitydate, originalface, istbaelig
FROM fanniestemp
ON CONFLICT (cusip)
DO NOTHING;

DROP TABLE fanniestemp;
'''

cursor.execute(sql)


conn.commit()
conn.close()
