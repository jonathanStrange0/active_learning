from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
import random
from app import db
from app.forms import NoteForm

def note_controller(learning_session_id=None):

	if learning_session_id:
		session = LearningSession.query.filter_by(id = learning_session_id).first()

	note_form = NoteForm()

	if request.method == 'POST' and note_form.validate_on_submit():
		note = Note(question = note_form.question_field.data)
		ans = Answer(answer = note_form.answer_field.data)
		note.answer.append(ans)
		session.notes.append(note)
		db.session.commit()
		return(redirect(url_for('note', learning_session_id=session.id)))

	return(render_template('note.html', title='Add Note', note_form=note_form, session=session))

def suggest_subject():
	all_subjects = Subject.query.all()
	selection_idx = random.randint(0,len(all_subjects) - 1)
	selected_subject = all_subjects[selection_idx]
	return(selected_subject)

def verify_subject(subject):
	try:
		last_two_learning_sessions = LearningSession.query.all()[-2:]
		last_two_subjects = [last_two_learning_sessions[0].subject.all()[0], last_two_learning_sessions[1].subject.all()[0]]
		return([subject] * 2 == last_two_subjects)
	except:
		return False

def subject_selector():
	subject = suggest_subject()
	while verify_subject(subject):
		subject = suggest_subject()
	return(subject)