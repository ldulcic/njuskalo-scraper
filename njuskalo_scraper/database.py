from peewee import SqliteDatabase, Model, CharField, IntegerField

database = SqliteDatabase('njuskalo_ads.db')


def init_database():
    database.create_tables([NjuskaloAdDB])


class NjuskaloAdDB(Model):
    title = CharField()
    link = CharField(unique=True)
    description = CharField()
    published = CharField()
    price = IntegerField()  # in euros

    class Meta:
        database = database
