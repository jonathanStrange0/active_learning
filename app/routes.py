from app import app, db
from flask import render_template, url_for, redirect, request
from app.forms import AddSubjectForm, RemoveSubjectForm, NoteForm
import random
from app.models import Subject, Note, Answer, LearningSession

@app.route('/')
@app.route('/index')
def index():
    return(render_template('index.html', title='Home'))

@app.route('/learning', methods=['GET', 'POST'])
def learn_something():
	# learn_w_notes_form = LearnWithNotesForm()
	# learn_lazy_form = LearnLazyForm()
	# if request.method == 'POST' and learn_w_notes_form.start_leaning_with_notes.validate(learn_w_notes_form):
	# 	print("with notes button pressed")
	# if request.method == 'POST' and learn_lazy_form.start_leaning_without_notes.validate(learn_lazy_form):
	# 	print("without notes button pressed")
	return(render_template('learn_something.html',\
		title='Let Me Tell You What to Learn Today!'))#,\
		# wn_form=learn_w_notes_form,\
		# won_form=learn_lazy_form))

@app.route('/note/<session>', methods=['GET', 'POST'])
def note(session):
	note_form = NoteForm()
	return(render_template('note.html', title='Add Note', note_form=note_form))


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
#####   HELPER FUNCTIONS ##################
###########################################

def subject_selector():
	all_subjects = Subject.query.all()
	selection_idx = random.randint(0,len(all_subjects) - 1)
	selected_subject = all_subjects[selection_idx]
	