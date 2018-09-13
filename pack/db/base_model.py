from peewee import *

db = SqliteDatabase("postgresql://postgres:1234@localhost:5432/postgres")


class BaseModel(Model):
    class Meta:
        database = db