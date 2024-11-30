import psycopg2

class Database:
    def __init__(self, host, database, user, password, cursorFactory):
        self.connection = None
        self.cursor = None
        self.error = None
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.cursorFactory = cursorFactory
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=self.cursorFactory,
            )
            print("Connected to database")
            self.cursor = self.connection.cursor()

        except Exception as error:
            print("Cannot connect to database")
            self.connection.close()
            self.error = error

    def getDatabaseConnection(self):
        return self.connection

    def getDatabaseCursor(self):
        return self.cursor
