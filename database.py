import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class MyDatabase(object):
    """
    It's a wrapper for the SQLITE3 database.

    Parameters
    ----------
    (None)

    Returns
    -------
    Returns a self object to the with.
    """

    def __init__(self):
        try:
            self.conn = sqlite3.connect("client_data.db")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!:", e)

    def __enter__(self):
        return self

    def close(self):
        """
        Closes the connection to the database.
        """
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def create_data_base_table(self, table_name):
        """
        This function create a new database table.
        Args:
            table_name(str):It takes a str of date(yyyy,mm) to creat new date base.
        """
        command = f"""CREATE TABLE
        {table_name} (  
                        name TEXT,
                        gstin TEXT,
                        company_name TEXT,
                        filling_state TEXT,
                        payment_state TEXT,
                        gstin_login_id TEXT,
                        gstin_password TEXT)"""
        self.cursor.execute(command)

    def clone_previous_table_to_new(self, pre_table_name, new_table_name):
        """
        This function fetches a specific database table and clones it to new database table.
        If the new table already exists  it just pass.
        Args:
            pre_table_name (str):It takes a str of date(yyyy,mm) to query old database table.
            new_table_name (str):It takes a str of date(yyyy,mm) to creat new date base.
        """
        try:
            query = f"SELECT * FROM {pre_table_name};"
            self.cursor.execute(query)
            query_data = self.cursor.fetchall()
            self.create_data_base_table(new_table_name)
            self.add_new_row(new_table_name, query_data, True)
        except sqlite3.OperationalError:
            pass

    def add_new_row(self, table_name, data, executemany=False):
        """
        This function adds a new row to the specified table.
        Args:
            table_name(str):It takes a str of date(yyyy,mm) to query specified table.
            data():It takes "list|or|tuple" to create a new table.
            executemany(:obj:`bool`,optional):It takes a bool to executemany time or not (optional).
        """
        command = f"""INSERT INTO {table_name} VALUES (?,?,?,?,?,?,?)"""
        if executemany:
            self.cursor.executemany(command, data)
        else:
            try:
                self.cursor.execute(command, data)
            except sqlite3.OperationalError:
                self.create_data_base_table(table_name)
                self.cursor.execute(command, data)

    def get_all_the_query_data(self, table_name):
        """
        This function "Returns" the queried database table.

        Args:
            table_name(str):It takes a str of date(yyyy,mm) to query specified table.
        Returns:
            list:The return value. List of dict with key as column name and value as row item.

        """
        try:
            self.conn.row_factory = dict_factory
            cur = self.conn.cursor()
            cur.execute(f"SELECT ROWID,* FROM {table_name};")
            result = cur.fetchall()
        except sqlite3.OperationalError:
            result = False
        return result

    def get_last_row_data(self, table_name):
        """
        This function get the last row of the given table.
        Args:
            table_name(str):It takes a str of date(yyyy,mm) to query specified table.
        Returns:
            dict:The return value. Dict of the with key as column name and value as row item.
        """
        command = f"""SELECT ROWID, *FROM {table_name} ORDER BY ROWID desc limit 1 """
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        cur.execute(command)
        row = cur.fetchone()
        return row

    def update_row_item(self, table_name, row_item, row_id):
        """
        This function update particular item in the row.
        Args:
            table_name(str):It takes a str of date(yyyy,mm) to query specified table.
            row_item(list):It takes  list of str. Which contains column name and value two be updated.
            row_id(str):It takes str od number. to reference the row with.
        """
        command = f"""update {table_name} set {row_item[0]} = "{row_item[1]}" where ROWID = {row_id}"""
        self.cursor.execute(command)

    def reset_row_item(self, table_name, row_item):
        """
        This function resets particular item in the row.
        Args:
            table_name(str):It takes a str of date(yyyy,mm) to query specified table.
            row_item(list):It takes  list of str. Which contains column name and value two be updated.
        """
        command = f"""update {table_name} set {row_item[0]} = "{row_item[1]}" where {row_item[0]} = "yes"; """
        try:
            self.cursor.execute(command)
        except sqlite3.OperationalError:
            pass

    def delete_row(self, table_name, row_id):
        """
        This function Deletes the row from the table.
        Args:
            table_name(str):It takes a str of date(yyyy,mm) to query specified table
            row_id(str):It takes str od number. to reference the row with.
        """
        command = f"""DELETE FROM {table_name} WHERE ROWID = {row_id}"""
        self.cursor.execute(command)
