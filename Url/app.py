import string,pyshorteners,os,random
from random import choice
import string
from flask import Flask, render_template, request, flash, redirect, url_for
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))
path = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key = True)
    long_url = db.Column(db.Text)
    short_url = db.Column(db.Text)
    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url
    def __repr__(self) -> str:
        return f"{self.long_url} - {self.short_url}"
    
###############################################################################################

def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route('/', methods=['POST','GET'])
def home_page():
    if request.method == "POST":
        url = request.form['url']
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(url)
        db.session.add(Url(long_url=url, short_url=short_url))
        db.session.commit()
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')
        

@app.route('/display')
def display_all():
    urls = Url.query.all()
    return render_template('display.html',urls=urls)


@app.route('/delete/<int:id>')
def delete(id):
    url = Url.query.filter_by(id=id).first()
    db.session.delete(url)
    db.session.commit()
    return redirect("/display")



if __name__ == '__main__':
    app.run(debug=True)