from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession, Bin
from datetime import datetime
import random
from app import db
from app.forms import NoteForm

def note_controller(learning_session_id=None):

	"""
		handle the takinging and saving of notes that will later be used as questions on flash cards

		if there is a learning session already started, and passed along, append that note to the
		existing learning session

		Otherwise, this is the first note in a learning session, and a new one should be created.

		Return the template for creating notes.
	"""

	if learning_session_id is not None:
		session = LearningSession.query.filter_by(id = learning_session_id).first()
	else:
		session = LearningSession(start_time=datetime.now())
		session.subject.append(subject_selector())
		db.session.commit()
		print('learning session generated by blank url ls field', session)
		return(redirect(url_for('note', learning_session_id=session.id)))
	note_form = NoteForm()

	if request.method == 'POST' and note_form.validate_on_submit():
		note = Note(question = note_form.question_field.data)
		ans = Answer(answer = note_form.answer_field.data)
		if Bin.query.filter_by(bin_name = 'Bin 1').first():
			bin1 = Bin.query.filter_by(bin_name = 'Bin 1').first()
		else:
			bin1 = Bin(bin_name = 'Bin 1')
		note.answer.append(ans)
		session.notes.append(note)
		print('learning session in form submit:', session)
		note.subject = session.subject.first()
		bin1.notes.append(note)
		db.session.commit()
		return(redirect(url_for('note', learning_session_id=session.id)))

	return(render_template('note.html', title='Add Note', note_form=note_form, session=session))

def no_note_controller():

	"""
		Create a learning session and choose a subject to learn.

		When there is a situation that does not require notes to be taken on a subject
		this function starts a learning session and chooses a subject for the lazy learner

	"""

	session = LearningSession(start_time=datetime.now())
	session.subject.append(subject_selector())
	db.session.commit()
	print('learning session generated by blank url ls field', session)
	return(render_template('no_note_learning_session.html', title='No Notes to Take Today :(', learning_session = session))

def suggest_subject():
	"""
		Randomly select a subject out of all the subjects in the database

		Return that subject
	"""
	all_subjects = Subject.query.all()
	selection_idx = random.randint(0,len(all_subjects) - 1)
	selected_subject = all_subjects[selection_idx]
	return(selected_subject)

def verify_subject(subject):
	"""
		Confirm that the last two learning sessions have not been this subject

		Return true/false
	"""
	try:
		last_two_learning_sessions = LearningSession.query.all()[-2:]
		last_two_subjects = [last_two_learning_sessions[0].subject.all()[0], last_two_learning_sessions[1].subject.all()[0]]
		return([subject] * 2 == last_two_subjects)
	except:
		return False

def subject_selector():
	"""
		Generate a subject that hasn't been studied more than twice in a row

		Return that subject
	"""
	subject = suggest_subject()
	while verify_subject(subject):
		subject = suggest_subject()
	return(subject)