from peewee import SqliteDatabase, Model, CharField, BlobField


def create_db(name: str):
    db = SqliteDatabase(name)

    class BaseModel(Model):
        class Meta:
            database = db

    class Image(BaseModel):
        image_hash = CharField(primary_key=True)
        image_data = BlobField()

    db.connect()
    db.create_tables([Image])

    class Res:
        database = db
        image = Image

    return Res()
