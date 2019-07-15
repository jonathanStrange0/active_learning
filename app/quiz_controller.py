# quiz_controller.py
from flask import render_template, url_for, redirect, request, jsonify
from app.models import Subject, Note, Answer, LearningSession, Bin
from datetime import datetime
import random, re
from app import db, quiz_or_test_list

def quiz_controller(learning_session_id=None):
	learning_session = LearningSession.query.filter_by(id = learning_session_id).first()
	subject = learning_session.subject.first()
	last_question = False
	global quiz_or_test_list
	if len(quiz_or_test_list):
		current_question = quiz_or_test_list.pop()
		if len(quiz_or_test_list) == 0:
			# this is the last question of the quiz
			last_question = True
	elif not last_question:
		# this query will get the notes of a particular subject in bin_1
		bin1 = Bin.query.filter_by(bin_name = "Bin 1").first()
		quiz_or_test_list = random.sample(db.session.query(Note).\
															join(Note.bin).\
															filter(Note.subject == subject, Note.bin == bin1).all(), k=5)
		current_question = quiz_or_test_list.pop()
	print(current_question, last_question)
	return(render_template('quiz.html', learning_session=learning_session,\
										 subject=subject, \
										 question = current_question, \
										 last_question=last_question))

def record_quiz_answer(correct):
	"""
		if the quiz question is answered correctly, move it into the next bin up

		otherwise, move it back to bin 1

		Also keep track of if this is the last question in the quiz or not.
		If it is, return the quiz_results.html template instead of another question.
	"""
	last_question = request.args.get('last_question', type=bool)
	# print(request.args.get('last_question', type=bool))
	question_id = request.args.get('question_id', type=int)
	session_id = request.args.get('session_id', type=int)
	note =  Note.query.filter_by(id=question_id).first()
	bin_name = note.bin.bin_name
	if correct:
		# save new answer to answers for this note
		# move question to next bin up
		move_note_bin(note, up=True)

	else:
		# move question to bin 1
		move_note_bin(note, up=False)

	if last_question:
		# print('last question = ',last_question)
		return jsonify(result=url_for('quiz_results', learning_session_id = session_id))
	else:
		# print('last question = False',last_question)
		return jsonify(result=url_for('quiz', learning_session_id = session_id))

def move_note_bin(note, up=True):
	"""
		give a note, and if the question needs to be moved into the next 
		bin or not, remove the note from it's current bin, and place it 
		in the next bin.

		if the question was answered incorrectly (up = False), drop the
		note down into bin 1 for further study.
	"""
	bin_name = note.bin.bin_name
	bin_num = int(re.findall(r'(\d+)', bin_name)[0])

	if up: 
		if bin_num == 1:
			bin_1 = note.bin
			bin_1.notes.remove(note)
			bin_2 = Bin.query.filter_by(bin_name = 'Bin 2').first()
			if bin_2:
				bin_2.notes.append(note)
			else:
				bin_2 = Bin(bin_name='Bin 2')
				bin_2.notes.append(note)
		elif bin_num == 2:
			bin_2 = note.bin
			bin_2.notes.remove(note)
			bin_3 = Bin.query.filter_by(bin_name = 'Bin 2').first()
			if bin_3:
				bin_3.notes.append(note)
			else:
				bin_3 = Bin(bin_name='Bin 3')
				bin_3.append(note)
		elif bin_num == 3:
			bin_3 = note.bin
			bin_3.notes.remove(note)
			bin_4 = Bin.query.filter_by(bin_name = 'Bin 4').first()
			if bin_4:
				bin_4.notes.append(note)
			else:
				bin_4 = Bin(bin_name='Bin 4')
				bin_4.append(note)
	else:
		any_bin = note.bin
		any_bin.notes.remove(note)
		bin_1 = Bin.query.filter_by(bin_name = 'Bin 1').first()
		bin_1.notes.append(note)

	db.session.commit()


