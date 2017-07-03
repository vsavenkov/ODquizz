from datetime import datetime
# import json

from flask import Flask, request, url_for, redirect, g, session, flash, \
     abort, render_template, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.oauth import OAuth

from parse_table import csvclean_service

from settings import CONSUMER_KEY, CONSUMER_SECRET


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///odquizz.db',
    SECRET_KEY='development-key'
)
db = SQLAlchemy(app)
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    request_token_params={'scope': 'email'}
)


class QuizzQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    table = db.Column(db.Text)
    column = db.Column(db.Integer)
    row = db.Column(db.Integer)

    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, question, row, column):
        self.user = user
        self.question = question
        self.row = row
        self.column = column
        self.pub_date = datetime.utcnow()
        print "new question object created"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(120))
    fb_id = db.Column(db.String(30), unique=True)
    questions = db.relationship(QuizzQuestion, lazy='dynamic', backref='user')


@app.before_request
def check_user_status():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


def generate_table(request):
    url = request.form['url']
    if url:
        return csvclean_service(url)
    # run with default csv url
    return csvclean_service()


@app.route('/', methods=['GET', 'POST'])
def new_quiz():
    rows = None
    header = None
    if request.method == 'POST':
        table = generate_table(request)
        # table = csvclean_service(request.form['url'])
    # if request.method == 'POST' and request.form['code']:
    #     
        header = json.dumps(table.header_line)
        rows = json.dumps(table.sample[1:])
    return render_template('new_quiz.html', rows=rows, header=header)
    # return render_template('layout.html')

@app.route('/new_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        string = request.form['question']
        row = request.form['row']
        column = request.form['col']
        question_obj = QuizzQuestion(g.user, string, row, column)
        db.session.add(question_obj)
        db.session.commit()
        return redirect(url_for('show_question', question_id=question_obj.id))
    # return render_template('layout.html')


@app.route('/<int:question_id>')
def show_question(question_id):
    print "im showing the question:"
    question_obj = QuizzQuestion.query.get_or_404(question_id)
    print question_obj.question
    return render_template('show_question.html', question_obj=question_obj)


@app.route('/<int:question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    question_obj = QuizzQuestion.query.get_or_404(question_id)
    if g.user is None or g.user != question_obj.user:
        abort(401)
    if request.method == 'POST':
        if 'yes' in request.form:
            db.session.delete(question_obj)
            db.session.commit()
            flash('Question was deleted')
            return redirect(url_for('new_quiz'))
        else:
            return redirect(url_for('show_question', paste_id=paste.id))
    return render_template('delete_question.html', question_obj=question_obj)


@app.route('/my-questions')
def my_questions():
    if g.user is None:
        return redirect(url_for('login', next=request.url))
    question_objs = QuizzQuestion.query.filter_by(user=g.user).all()
    return render_template('my_questions.html', question_objs=question_objs)


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out')
    return redirect(url_for('new_quiz'))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('new_quiz')
    if resp is None:
        flash('You denied the login')
        return redirect(next_url)

    session['fb_access_token'] = (resp['access_token'], '')

    me = facebook.get('/me')
    user = User.query.filter_by(fb_id=me.data['id']).first()
    if user is None:
        user = User()
        user.fb_id = me.data['id']
        db.session.add(user)

    user.display_name = me.data['name']
    db.session.commit()
    session['user_id'] = user.id

    flash('You are now logged in as %s' % user.display_name)
    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('fb_access_token')


if __name__ == '__main__':
    app.run()
