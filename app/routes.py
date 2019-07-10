from app import app, db
from flask import render_template, url_for, redirect, request, jsonify
from app.forms import AddSubjectForm, RemoveSubjectForm, NoteForm
import random
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
from app.note_controller import note_controller, subject_selector
from app.results_controller import results_controller
from app.quiz_controller import quiz_controller
from app.quiz_results_controller import quiz_results_controller


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

@app.route('/test')
def test_knowledge():
	return(render_template('test_knowledge.html', title='Find out what you don\'t know here'))

@app.route('/quiz')
def quiz():
	if request.args.get('learning_session_id'):
		session = LearningSession.query.filter_by(id = request.args.get('learning_session_id')).first()
	return(quiz_controller(learning_session_id = session.id))

@app.route('/quiz_results/<learning_session_id>')
def quiz_results(learning_session_id):

	return(quiz_results_controller(learning_session_id))

@app.route('/_correct_quiz_answer')
def correct_quiz_answer():
	last_question = request.args.get('last_question', type=bool)
	# last_question = bool(last_question)
	print(request.args.get('last_question', type=bool))
	question_id = request.args.get('question_id', type=int)
	session_id = request.args.get('session_id', type=int)
	note =  Note.query.filter_by(id=question_id).first()

	if last_question:
		print('last question = ',last_question)
		# return(redirect(url_for('quiz_results', learning_session_id = session_id)))
		return jsonify(result=url_for('quiz_results', learning_session_id = session_id))
	else:
		print('last question = False',last_question)
		# return(redirect(url_for('quiz', learning_session_id = session_id)))
		return jsonify(result=url_for('quiz', learning_session_id = session_id))

	

@app.route('/_incorrect_quiz_answer')
def incorrect_quiz_answer():
	last_question = request.args.get('last_question', 0, type=str)
	last_question = bool(last_question)
	print('request data: ', request.args)
	question_id = request.args.get('question_id', 0, type=int)
	session_id = request.args.get('session_id', 0, type=int)
	note =  Note.query.filter_by(id=question_id).first()

	if last_question:
		print('last question = True')
		return(quiz_results_controller(session_id))
	else:
		print('last question = False')
		return(quiz_controller(session_id = session_id))



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
