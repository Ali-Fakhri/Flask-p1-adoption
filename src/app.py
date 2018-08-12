import os
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


app.config['SECRET_KEY'] = 'MYSECRETKEYTOCONFIG'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


###############################
#### SQL TABLES SECTION #######
###############################


class Puppy(db.Model):

    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref='Puppy', uselist=False)

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return f"{self.id} {self.name}{self.owner}"


class Owner(db.Model):

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id


#################################
#### DONE SQL TABLES SECTION ####
#################################


###############################
#### ADD FORM SECION ##########
###############################


class AddForm(FlaskForm):
    name = StringField('What\'s The Puppy Name You Want to Add ?')
    submit_adding = SubmitField('Add Now')


class DelForm(FlaskForm):
    id = IntegerField('What\'s The id in DB of The Puppy You Want to Remove ?')
    submit_removing = SubmitField('Remove Now')


class OwnerForm(FlaskForm):
    o_name = StringField('Please Type The Owner Name You Want to Provide For a Puppy. ')
    o_id = IntegerField('Please Enter a Number of The id of The Puppy. ')
    submit_owner = SubmitField('Make Em Owner Now')


###############################
#### DN FORM SECION ###########
###############################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        pup_name = form.name.data
        puppy = Puppy(pup_name)
        db.session.add(puppy)
        db.session.commit()
        return redirect(url_for('list'))

    return render_template('add.html', form=form)


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    form = DelForm()
    if form.validate_on_submit():
        pup_id = form.id.data
        aimed_pup = Puppy.query.get(pup_id)
        db.session.delete(aimed_pup)
        db.session.commit()
        return redirect(url_for('list'))

    return render_template('remove.html', form=form)


@app.route('/owner', methods=['GET', 'POST'])
def owner():
    form = OwnerForm()
    if form.validate_on_submit():
        o_name = form.o_name.data
        pup_id = form.o_id.data
        new_owner = Owner(o_name, pup_id)
        db.session.add(new_owner)
        db.session.commit()
        return redirect(url_for('list'))

    return render_template('owner.html', form=form)



@app.route('/list')
def list():
    all_puppies = Puppy.query.all()

    return render_template('list.html', all_puppies=all_puppies)


if __name__ == '__main__':
    app.run(debug=True)
