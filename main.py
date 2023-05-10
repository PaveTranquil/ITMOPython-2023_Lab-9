import flask
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(512), nullable=False)
    __table_args__ = (db.UniqueConstraint('author', 'name', name='_author_name_uc'),
                     )

    def __init__(self, author, title):
        self.author = author
        self.name = title


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html', books=list(reversed(Book.query.all())))


@app.route('/add_book', methods=['POST'])
def add_book():
    author = flask.request.form['author']
    title = flask.request.form['title']
    db.session.add(Book(author, title))
    db.session.commit()

    return flask.redirect(flask.url_for('index'))


@app.route('/delete_all', methods=['GET'])
def delete_all():
    db.session.execute('DELETE FROM book')
    db.session.commit()
    
    return flask.redirect(flask.url_for('index'))

with app.app_context():
    db.create_all()
app.run()