from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return(render_template('index.html', title='Home'))

@app.route('/learning')
def learn_something():
	return(render_template('learn_something.html', title='Let Me Tell You What to Learn Today!'))


@app.route('/test')
def test_knowledge():
	return(render_template('test_knowledge.html', title='Find out what you don\'t know here'))

@app.route('/settings')
def manage_settings():
	return(render_template('manage_settings.html', title='Make adjustements to your course'))