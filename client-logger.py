from datetime import date, timedelta

import eel

from database import MyDatabase

today = date.today()
database_date = today.strftime("client_%Y_%m")
today_date = today.strftime("%d")

table_name = database_date
eel.init("web")


def start():
    last_month_database_name = ((today.replace(day=1)) - (timedelta(days=1))).strftime("client_%Y_%m")
    with MyDatabase() as md:
        md.clone_previous_table_to_new(last_month_database_name, database_date)


start()


@eel.expose
def get_current_date():
    date_for_web_calendar = today.strftime("%Y-%m")
    return date_for_web_calendar


@eel.expose
def get_the_query_data_from_database():
    with MyDatabase() as md:
        query_data = md.get_all_the_query_data(table_name)
    return query_data


@eel.expose
def get_data_from_js(data):
    row_data = tuple(val for val in data.values())
    with MyDatabase() as md:
        md.add_new_row(table_name, row_data)
        row_query = md.get_last_row_data(table_name)
    return row_query


@eel.expose
def update_row_item(update_item_value, row_id):
    with MyDatabase() as md:
        md.update_row_item(table_name, update_item_value, row_id)


@eel.expose
def delete_row(row_id):
    with MyDatabase() as md:
        md.delete_row(table_name, row_id)


@eel.expose
def search_for_table(search_name):
    name = search_name.split("-")
    search_table_name = f"client_{name[0]}_{name[1]}"
    with MyDatabase() as md:
        query = md.get_all_the_query_data(search_table_name)
    return query


@eel.expose
def clone_data_base(clone_tables_names):
    # taking the dict object from js and formatting in to list of tuples.
    table_name_data = [tuple(val.split("-")) for val in clone_tables_names.values()]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    clone_from_table = f"client_{table_name_data[0][0]}_{table_name_data[0][1]}"
    if table_name_data[1][1] and table_name_data[2][1] in months:
        # convert month number from str to int for indexing.
        first_month = int(table_name_data[1][1]) - 1
        last_month = int(int(table_name_data[2][1]))
        # getting all months from months list.
        get_months = months[first_month:last_month]
        # formatting all the months in the table name format.
        all_months = [f"client_{table_name_data[1][0]}_{num}" for num in get_months]
        with MyDatabase() as md:
            for new_table_names in all_months:
                if new_table_names != clone_from_table:
                    md.clone_previous_table_to_new(clone_from_table, new_table_names)
                    md.reset_row_item(new_table_names, ["filling_state", "no"])
                    md.reset_row_item(new_table_names, ["payment_state", "no"])


eel.start("index.html", size=(1366, 768))
