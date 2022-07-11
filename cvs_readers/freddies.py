import csv
from datetime import datetime
import psycopg2

# connects to database
conn = psycopg2.connect(
    database="fannies", user='postgres',
    password='JerryPine', host='localhost', port='5432'
)

# so I am not sure if this is the best place to put it our do this but here I am going read in all the cusips that have SRC - Mirrors but are not actually plats.. I will putr them into an array and use that array to make sure I do not accidently put them the plats..
# I assume I will need a way to update this mnthly but one step at a time for now :)

# so after I run freddies step one, I will have cusips in the below cvs file this puts them in an array and I use
# that to make sure none wind up in the plats
cusipscvs = 'cvs_readers/data/output/aretheseplats.cvs'

with open(cusipscvs, newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    headers = next(data)

    cusipsnotplats = []

    for row in data:
        cusipsnotplats.append(row[0])

# so this seems to work fine.. and yes I guess in theory each month I would run it normally than ceck it against the teh ecs file get these cusip and then rerun..
# print(len(cusipsnotplats))


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
    body = []

    headplats = []
    bodyplats = []

    for row in data:

        # print(row[17])
        # print(row[34])
        # print(row[37])
        # break

        try:
            cusip = row[2]
            name = row[1]
            indicator = row[0]
            issuedate = row[11]
            maturitydate = row[12]
            originalface = float(row[14])

            coupon = float(row[16])
            original_coupon = float(row[17])

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

            if (originalface >= 250000) and (num_months <= 181) and (indicator == 'CN' or indicator == 'CI') and (original_coupon - coupon >= .25):

                istbaelig = '15 year'

            elif (originalface >= 250000) and (num_months > 181) and (num_months <= 361) and (indicator == 'CL' or indicator == 'CT') and (original_coupon - coupon >= .25):

                istbaelig = '30 year'

#################################
            # print(istbaelig)
            remainingbalance = row[15]
            factor = row[4]
            gwac = row[18]
            wam = row[22]
            wala = row[23]

# we have two kinds of plats SCR or SCR - Mirrors so we are using starts with to find both of them
# the SCR - Mirror do not appear to be labeled correctly we will deal wih that later
# there are also some called the Multiples we briefly had them here now we do not
            if (row[34].startswith('SCR') or row[37].startswith('SCR')) and cusip not in cusipsnotplats:
                # I was looking for missing suips in our platinums table
                # if row[34] == 'SCR - Mirror' or row[37] == 'SCR - Mirror':

                headplats.append([cusip, name, indicator, start_date.date(),
                                  end_date.date(), originalface])

                bodyplats.append([cusip, coupon, remainingbalance,
                                  factor, gwac, wam, wala, date, None])

            else:

                head.append([cusip, name, indicator, start_date.date(),
                            end_date.date(), originalface, istbaelig])

                body.append([cusip, coupon, remainingbalance,
                            factor, gwac, wam, wala, date])

        except Exception as e:
            # we seem to get a couple of very new supers (like platinums) each month
            print(row)
            print(e)

headfields = ["cusip", "name", "indicator", "issuedate",
              "maturitydate", "originalface", "istbaelig"]

with open('cvs_readers/data/output/freddies.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(head)


bodyFields = ["cusip", "coupon", "remainingbalance",
              "factor", "gwac", "wam", "wala", "date"]

with open('cvs_readers/data/output/freddiebodies.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(bodyFields)

    # writing the data rows
    csvwriter.writerows(body)

headfields = ["cusip", "name", "indicator", "issuedate",
              "maturitydate", "originalface"]


with open('cvs_readers/data/output/freddieplats.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(headplats)


bodyFields = ["cusip", "coupon", "remainingbalance",
              "factor", "gwac", "wam", "wala", "date", "istbaelig"]

with open('cvs_readers/data/output/freddiebodieplats.cvs', 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(bodyFields)

    # writing the data rows
    csvwriter.writerows(bodyplats)


# connecting to database
# what is autocommit
conn.autocommit = True
cursor = conn.cursor()

csv_file_name = 'cvs_readers/data/output/freddiebodies.cvs'
sql = "COPY freddiebodies FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))

sql = '''
create temporary table freddiestemp (cusip varchar, name varchar , indicator varchar, issuedate date, maturitydate date, originalface double precision, istbaelig istbaelig_type);
'''
cursor.execute(sql)

# maybe there is an easier way to do this but I don't know it
csv_file_name = 'cvs_readers/data/output/freddies.cvs'
sql = "COPY freddiestemp FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


sql = '''
INSERT INTO freddies (cusip, name, indicator, issuedate, maturitydate, originalface, istbaelig)
SELECT cusip, name, indicator, issuedate, maturitydate, originalface, istbaelig
FROM freddiestemp
ON CONFLICT (cusip)
DO NOTHING;

DROP TABLE freddiestemp;
'''

cursor.execute(sql)

###################################################

csv_file_name = 'cvs_readers/data/output/freddiebodieplats.cvs'
sql = "COPY freddieplatbodies FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))

sql = '''
create temporary table freddieplatstemp (cusip varchar, name varchar , indicator varchar, issuedate date, maturitydate date, originalface double precision);
'''
cursor.execute(sql)

# maybe there is an easier way to do this but I don't know it
csv_file_name = 'cvs_readers/data/output/freddieplats.cvs'
sql = "COPY freddieplatstemp FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


sql = '''
INSERT INTO freddieplats (cusip, name, indicator, issuedate, maturitydate, originalface)
SELECT cusip, name, indicator, issuedate, maturitydate, originalface
FROM freddieplatstemp
ON CONFLICT (cusip)
DO NOTHING;

DROP TABLE freddieplatstemp;
'''

cursor.execute(sql)


conn.commit()
conn.close()
