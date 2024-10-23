from .app import db,login_manager
from flask_login import UserMixin

# Table d'association pour la relation ManyToMany entre Books et Genres
book_genre = db.Table('book_genre',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('genres_id', db.Integer, db.ForeignKey('genres.id'))
)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Author ({self.id}) {self.name}>"

class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<genres ({self.id}) {self.name}>"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    price = db.Column(db.Float)
    url = db.Column(db.String(500))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    genres_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    author = db.relationship('Author', backref=db.backref('books', lazy='dynamic'))
    genres = db.relationship('Genres', backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return f"<Book ({self.id}) {self.title}>"

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
