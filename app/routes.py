from app import app, db
from flask import render_template, url_for, redirect, request
from app.forms import AddSubjectForm, RemoveSubjectForm, NoteForm
import random
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
from app.note_controller import note_controller, subject_selector

@app.route('/')
@app.route('/index')
def index():
    return(render_template('index.html', title='Home'))

@app.route('/learning', methods=['GET', 'POST'])
def learn_something():
	return(render_template('learn_something.html',\
		title='Let Me Tell You What to Learn Today!'))

@app.route('/note', methods=['GET', 'POST'])
def note():
	if request.args.get('learning_session_id'):
		print('this is the learning ID ' + request.args.get('learning_session_id')) 
		session = LearningSession.query.filter_by(id = request.args.get('learning_session_id')).first()
		return note_controller(learning_session_id = request.args.get('learning_session_id'))
	else:
		session = LearningSession(start_time=datetime.now())
		session.subject.append(subject_selector())
		db.session.commit()
		print(session)
		return note_controller()
	

@app.route('/_close_learning_session')
def _close_learning_session():
	if request.args.get('learning_session_id'):
		session = LearningSession.query.filter_by(id = request.args.get('learning_session_id')).first()
		session.end_time = datetime.now()
		db.session.commit()
	return(redirect(url_for('session_results', learning_session_id=session.id)))

@app.route('/session_results')
def session_results():


	return 'donezore'

@app.route('/test')
def test_knowledge():
	return(render_template('test_knowledge.html', title='Find out what you don\'t know here'))

@app.route('/settings', methods=['GET', 'POST'])
def manage_settings():
	subject_form = AddSubjectForm()
	remove_subject_form = RemoveSubjectForm()
	remove_subject_form.subject_text.query = Subject.query.all()
	# print(remove_subject_form.subject_text.data.id)
	if request.method == 'POST' and subject_form.validate_on_submit():
		db.session.add(Subject(subject = subject_form.subject_field.data))
		db.session.commit()
		return(redirect(url_for('manage_settings')))
	if request.method == 'POST' and remove_subject_form.validate_on_submit():
		print(remove_subject_form.subject_text.data)
		db.session.delete(remove_subject_form.subject_text.data)
		db.session.commit()
		return(redirect(url_for('manage_settings')))

	if len(Subject.query.all()) > 0:
		remove_subject_form.subject_text.query = Subject.query.all()
		return(render_template('manage_settings.html', \
			title='Make adjustements to your course', \
			add_sub_form=subject_form, \
			remove_sub_form=remove_subject_form))
	else:
		return(render_template('manage_settings.html', \
			title='Make adjustements to your course', \
			add_sub_form=subject_form, \
			remove_sub_form=None))



###########################################
#########  HELPER FUNCTIONS  ##############
###########################################

# def suggest_subject():
# 	all_subjects = Subject.query.all()
# 	selection_idx = random.randint(0,len(all_subjects) - 1)
# 	selected_subject = all_subjects[selection_idx]
# 	return(selected_subject)

# def verify_subject(subject):
# 	try:
# 		last_two_learning_sessions = LearningSession.query.all()[-2:]
# 		last_two_subjects = [last_two_learning_sessions[0].subject.all()[0], last_two_learning_sessions[1].subject.all()[0]]
# 		return([subject] * 2 == last_two_subjects)
# 	except:
# 		return False

# def subject_selector():
# 	subject = suggest_subject()
# 	while verify_subject(subject):
# 		subject = suggest_subject()
# 	return(subject)

