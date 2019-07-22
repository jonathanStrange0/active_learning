from app import app, db
from flask import render_template, url_for, redirect, request
from app.forms import AddSubjectForm, RemoveSubjectForm, NoteForm
import random
from app.models import Subject, Note, Answer, LearningSession, Quiz
from datetime import datetime
from app.note_controller import note_controller, subject_selector
from app.results_controller import results_controller
from app.quiz_controller import quiz_controller, record_quiz_answer, test_controller, record_test_answer
from app.quiz_results_controller import quiz_results_controller
from app.test_results_controller import test_results_controller


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
		# session = LearningSession(start_time=datetime.now())
		# session.subject.append(subject_selector())
		# db.session.commit()
		# print(session)
		return note_controller()

		# return note_controller(learning_session_id = session.id)
	

@app.route('/_close_learning_session')
def _close_learning_session():
	if request.args.get('learning_session_id'):
		session = LearningSession.query.filter_by(id = request.args.get('learning_session_id')).first()
		session.end_time = datetime.now()
		db.session.commit()
	return(redirect(url_for('session_results', learning_session_id=session.id)))

@app.route('/session_results')
def session_results():
	return results_controller(request.args.get('learning_session_id'))

@app.route('/test_selector')
def test_knowledge():
	return(render_template('test_knowledge.html', title='Find out what you don\'t know here'))

@app.route('/quiz')
def quiz():
	if request.args.get('learning_session_id'):
		# session = LearningSession.query.filter_by(id = request.args.get('learning_session_id')).first()
		learning_session_id = request.args.get('learning_session_id')
		if request.args.get('quiz_id'):
			# quiz = Quiz.query.filter_by(id = request.args.get('quiz_id')).first()
			quiz_id = request.args.get('quiz_id')
			return(quiz_controller(learning_session_id = learning_session_id, quiz_id = quiz_id))
		else:
			return(quiz_controller(learning_session_id = learning_session_id))

@app.route('/quiz_results/<learning_session_id>')
def quiz_results(learning_session_id):

	return(quiz_results_controller(learning_session_id))

@app.route('/_correct_quiz_answer')
def correct_quiz_answer():

	return(record_quiz_answer(True))

@app.route('/_incorrect_quiz_answer')
def incorrect_quiz_answer():

	return(record_quiz_answer(False))

@app.route('/test')
def test():
	if request.args.get('bin_name'):
		if request.args.get('test_id'):
			print('bin name ', request.args.get('bin_name'))
			print('test_id ', request.args.get('test_id'))
			return(test_controller(bin_name = request.args.get('bin_name'), \
									test_id = request.args.get('test_id') ))
		else:
			print('bin_name ', request.args.get('bin_name'))
			print('test_id ', request.args.get('test_id'))
			return(test_controller(bin_name = request.args.get('bin_name')))

	# else:
	# 	return(redirect(url_for('test')))

@app.route('/_correct_test_answer')
def correct_test_answer():

	return(record_test_answer(True))

@app.route('/_incorrect_test_answer')
def incorrect_test_answer():

	return(record_test_answer(False))

@app.route('/test_results')
def test_results():
	test_id = request.args.get('test_id')
	return(test_results_controller(test_id))

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
