from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectMultipleField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256

from .app import app, db
from .models import Author, Book, User, Genres

class BookForm(FlaskForm):
    id = HiddenField('id')
    title = StringField('Title', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    genres = SelectMultipleField('Genres', coerce=int)  # liste déroulante pour genres

@app.route('/')
@app.route('/page/<int:page>')
def home(page=1):
    books = Book.query.order_by(Book.title.asc()).paginate(page=page, per_page=10)
    return render_template('home.html', books=books.items, pagination=books)

@app.route('/edit/book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.price = form.price.data
        book.genres = Genres.query.filter(Genres.id.in_(form.genres.data)).all()
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit-book.html', form=form, book=book)

@app.route('/delete/book/<int:id>', methods=['POST'])
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add/book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, price=form.price.data)
        new_book.genres = Genres.query.filter(Genres.id.in_(form.genres.data)).all()
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add-book.html', form=form)

@app.route('/search/author', methods=['GET', 'POST'])
def search_by_author():
    if request.method == 'POST':
        author_name = request.form['author']
        author = Author.query.filter_by(name=author_name).first()
        if author:
            books = author.books.all()
            return render_template('search-results.html', books=books)
        else:
            return "No author found"
    return render_template('search-author.html')

@app.route('/detail/<int:id>')
def detail(id):
    book = Book.query.get_or_404(id)
    return render_template('detail.html', book=book)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
