import csv
from datetime import datetime
# import psycopg2

# # connects to database
# conn = psycopg2.connect(
#     database="cmos_builder", user='postgres',
#     password='JerryPine', host='localhost', port='5432'
# )

# change this monthly
data_path = 'cvs_readers/data/input/FNM_MF_202112.txt'

date = data_path[-10:-6] + "-" + data_path[-6:-4] + "-01"

with open(data_path, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter='|')
    headers = next(data)

    head = []
    body = []

    for row in data:

        cusip = row[2]
        name = row[1]
        indicator = row[0]
        issuedate = row[11]
        maturitydate = row[12]
        originalface = row[14]

        print(cusip)
        print(name)
        print(indicator)
        print(issuedate)
        print(maturitydate)
        print(originalface)

        # end_date = datetime(int(maturitydate[0:4]), int(
        #     maturitydate[4:6]), int(maturitydate[6:8]))

        start_date = datetime(int(issuedate[4:8]), int(
            issuedate[0:2]), int(issuedate[2:4]))

        # print(start_date)

        print(start_date.strftime("%c"))

        break
#         num_months = (end_date.year - start_date.year) * \
#             12 + (end_date.month - start_date.month)

#         istbaelig = False

#         indicator = row[3]
#         type = row[4]
#         originalface = int(row[8])

#         if originalface >= 250000 and type == 'SF' and (indicator == 'X' or indicator == 'M') and num_months >= 336:

#             istbaelig = True

#         head.append([row[1], row[2], indicator, type,
#                     row[5], row[7], originalface, istbaelig])

#         body.append([row[1], row[6], row[9], row[10],
#                     row[17], row[18], row[19], date])


# headfields = ["cusip", "name", "indicator", "type",
#               "issuedate", "maturitydate", "originalface", "istbaelig"]

# with open('data/output/pools.cvs', 'w', newline='') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile)

#     # writing the fields
#     csvwriter.writerow(headfields)

#     # writing the data rows
#     csvwriter.writerows(head)


# bodyFields = ["cusip", "interestrate", "remainingbalance",
#               "factor", "gwac", "wam", "wala", "date"]

# with open('data/output/poolbodies.cvs', 'w', newline='') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile)

#     # writing the fields
#     csvwriter.writerow(bodyFields)

#     # writing the data rows
#     csvwriter.writerows(body)


# # connecting to database
# # what is autocommit
# conn.autocommit = True
# cursor = conn.cursor()

# csv_file_name = 'data\output\poolbodies.cvs'
# sql = "COPY poolbodies FROM STDIN DELIMITER ',' CSV HEADER"
# cursor.copy_expert(sql, open(csv_file_name, "r"))

# sql = '''
# create temporary table poolstemp (cusip varchar, name varchar , indicator varchar, type varchar, issuedate integer, maturitydate integer, originalface double precision, istbaelig boolean);
# '''
# cursor.execute(sql)

# # maybe there is an easier way to do this but I don't know it
# csv_file_name = 'data\output\pools.cvs'
# sql = "COPY poolstemp FROM STDIN DELIMITER ',' CSV HEADER"
# cursor.copy_expert(sql, open(csv_file_name, "r"))


# sql = '''
# INSERT INTO pools (cusip, name, indicator, type, issuedate, maturitydate, originalface, istbaelig)
# SELECT cusip, name, indicator, type, issuedate, maturitydate, originalface, istbaelig
# FROM poolstemp
# ON CONFLICT (cusip)
# DO NOTHING;

# DROP TABLE poolstemp;
# '''

# cursor.execute(sql)


# conn.commit()
# conn.close()
