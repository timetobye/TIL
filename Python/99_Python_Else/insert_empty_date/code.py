import csv
from datetime import datetime
from datetime import timedelta

# print(datetime.today())
# print(type(datetime.today()))
# print(datetime(2012, 3, 23, 23, 24, 55, 173504))
# print(datetime.today().weekday())
#
# 0, 1, 2, 3, 4, 5, 6
print(datetime.strptime("2020/12/21", "%Y/%m/%d").weekday())
print(datetime.strptime("2020/12/22", "%Y/%m/%d").weekday())
print(datetime.strptime("2020/12/23", "%Y/%m/%d").weekday())
print(datetime.strptime("2020/12/23", "%Y/%m/%d") + timedelta(days=1))


def get_weekday_number(string_date):
    weekday_number = datetime.strptime(string_date,"%Y/%m/%d").weekday()

    return weekday_number


def get_weekend_date(string_date):
    saturday_datetime = datetime.strptime(string_date, "%Y/%m/%d") + timedelta(days=1)
    string_saturday_date = datetime.strftime(saturday_datetime, "%Y/%m/%d")

    sunday_datetime = datetime.strptime(string_date, "%Y/%m/%d") + timedelta(days=2)
    string_sunday_datetime = datetime.strftime(sunday_datetime, "%Y/%m/%d")

    return string_saturday_date, string_sunday_datetime


def get_date_list():
    date_list = []
    kospi_start_date = "1980/01/04"
    current_date = datetime.strftime(datetime.now(), "%Y/%m/%d")

    number = 0
    while True:
        add_one_day_datetime = datetime.strptime(kospi_start_date, "%Y/%m/%d") + timedelta(days=number)
        result_date = datetime.strftime(add_one_day_datetime, "%Y/%m/%d")

        date_list.append(result_date)
        number += 1

        if current_date == result_date:
            break

    return date_list



with open("kospi_history_1980_2018.csv", "r", encoding="cp949") as read_file, \
        open("new_kospi_history_1980_2018.csv", "w", encoding="utf-8") as write_file:
    csv_file_read_lines = csv.reader(read_file)
    next(csv_file_read_lines)
    writer = csv.writer(write_file)

    kospi_date_list = get_date_list()

    count = 1

    new_kospi_data = []
    for line, kospi_date in zip(csv_file_read_lines, kospi_date_list):

        print(line, kospi_date)

        if line[0] == kospi_date:
            writer.writerow(line)
        else:
            temp_list = ['' for _ in range(12)]
            temp_list.insert(0, kospi_date)
            writer.writerow(temp_list)
            writer.writerow(line)


        if count == 10:
            break

        count += 1