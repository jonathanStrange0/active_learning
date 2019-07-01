from app import app, db
from flask import render_template, url_for, redirect, request
from app.forms import AddSubjectForm, RemoveSubjectForm
from app.models import Subject

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

@app.route('/settings', methods=['GET', 'POST'])
def manage_settings():
	subject_form = AddSubjectForm()
	remove_subject_form = RemoveSubjectForm()
	if request.method == 'POST' and subject_form.validate_on_submit():
		db.session.add(Subject(subject = subject_form.subject_field.data))
		db.session.commit()
		return(redirect(url_for('manage_settings')))
	if request.method == 'POST' and remove_subject_form.validate_on_submit():
		db.session.delete(Subject.query.filter_by(subject = remove_subject_form.subject_text.data))
		db.session.commit()
		return(redirect(url_for('manage_settings')))

	if len(Subject.query.all()) > 0:
		remove_subject_form.subject_text.query = Subject.query.all()
		return(render_template('manage_settings.html', title='Make adjustements to your course', add_sub_form=subject_form, remove_sub_form=remove_subject_form))
	else:
		return(render_template('manage_settings.html', title='Make adjustements to your course', add_sub_form=subject_form, remove_sub_form=None))