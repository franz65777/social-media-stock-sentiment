import mysql.connector


class Database:
    def __init__(self):
        self._conn = mysql.connector.connect(
            user="root",
            password="",
            host="127.0.0.1",
            port="3306",
            database="wall_street_bets",
        )
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


class Submission(Database):
    def __init__(self):
        super().__init__()

    def insert_submission(self, date, user, upvotes, text, ticker, sentiment, position):
        return self.execute(
            sql="""
            INSERT INTO submissions
            (__datetime, user, upvotes, submission_text, ticker, sentiment, position)
            VALUES(%s, %s, %s, %s, %s, %s, %s)""", params=(date, user, upvotes, text, ticker, sentiment, position,))

    def query_submission(self, ticker, start_date, end_date):
        return self.query(sql="""
        SELECT * FROM wall_street_bets.submissions
        WHERE
            ticker = %s
        AND
            __datetime BETWEEN %s and %s""", params=(ticker, start_date, end_date))
