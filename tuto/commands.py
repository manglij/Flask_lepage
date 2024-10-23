import click
from .app import app, db
from .models import Author, Book, User, Genres
from hashlib import sha256
import yaml

@app.cli.command()
def syncdb():
    """Crée toutes les tables manquantes."""
    db.create_all()

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Charge les données des livres depuis un fichier YAML."""
    db.create_all()
    books = yaml.safe_load(open(filename))
    authors = {}
    genres = {}
    for b in books:
        if b['author'] not in authors:
            a = Author(name=b['author'])
            db.session.add(a)
            authors[b['author']] = a
        if b['genres'] not in genres:
            g = Genres(name = b['genres'])
            db.session.add(g)
            genres[b["genres"]] = g
    db.session.commit()
    for b in books:
        a = authors[b['author']]
        g = genres[b['genres']]
        book = Book(title=b['title'], price=b['price'], url=b['url'], img=b['img'], author_id=a.id, genres_id = g.id)
        db.session.add(book)
    db.session.commit()
