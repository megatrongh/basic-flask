from api.utils.db import db
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow.fields import Integer, Nested, String


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    author = db.relationship('Author', back_populates='books')

    def __init__(self, title, year, author_id=None):
        self.title = title
        self.year = year
        self.author_id = author_id

    def __repr__(self):
        return f'{self.title}'

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = Integer(dump_only=True)
    title = String(required=True)
    year = Integer(required=True)
    author_id = Integer()
    author = Nested("AuthorSchema", only=['id', 'first_name'])
