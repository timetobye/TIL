import csv
from datetime import datetime
from datetime import timedelta


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
    end_date = "2018/11/09"

    number = 0
    while True:
        add_one_day_datetime = datetime.strptime(kospi_start_date, "%Y/%m/%d") + timedelta(days=number)
        result_date = datetime.strftime(add_one_day_datetime, "%Y/%m/%d")

        date_list.append(result_date)
        number += 1

        if end_date == result_date:
            break

    return date_list


with open("kospi_history_1980_2018.csv", "r", encoding="cp949") as read_file, \
        open("new_kospi_history_1980_2018.csv", "w", encoding="utf-8") as write_file:
    csv_file_reader = csv.reader(read_file)
    csv_file_writer = csv.writer(write_file)
    kospi_date_list = get_date_list()

    csv_file_dict = {}
    for idx, component_list in enumerate(csv_file_reader):
        if idx == 0:
            csv_file_writer.writerow(component_list)
            continue

        if component_list[0] not in csv_file_dict:
            csv_file_dict[component_list[0]] = component_list[1:]

    # print(csv_file_dict)

    empty_string_list = ['' for _ in range(12)]
    for kospi_date in kospi_date_list:
        if csv_file_dict.get(kospi_date, None):
            component_list = [kospi_date] + csv_file_dict[kospi_date]
            csv_file_writer.writerow(component_list)

        else:
            component_list = [kospi_date] + empty_string_list
            csv_file_writer.writerow(component_list)
