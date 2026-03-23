from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///books.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Book {self.id} {self.title}>"


def create_tables():
    with app.app_context():
        db.create_all()


create_tables()


@app.route('/')
def index():
    books = Book.query.order_by(Book.id.desc()).all()
    return render_template('index.html', books=books)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        if not title:
            flash('Title is required', 'danger')
            return redirect(url_for('create'))
        book = Book(title=title, author=author, description=description)
        db.session.add(book)
        db.session.commit()
        flash('Book added', 'success')
        return redirect(url_for('index'))
    return render_template('form.html', action='Create', book=None)


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        if not title:
            flash('Title is required', 'danger')
            return redirect(url_for('edit', book_id=book_id))
        book.title = title
        book.author = author
        book.description = description
        db.session.commit()
        flash('Book updated', 'success')
        return redirect(url_for('index'))
    return render_template('form.html', action='Edit', book=book)


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
