import peewee

db = peewee.SqliteDatabase("database.db")


class BaseTable(peewee.Model):
    class Meta:
        database = db


class DatabaseUpdater(BaseTable):
    Date = peewee.TextField(unique=True)
    Min_temp = peewee.TextField()
    Max_temp = peewee.TextField()
    Day_details = peewee.TextField()


db.create_tables([DatabaseUpdater])
