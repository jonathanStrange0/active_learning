from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectField, SubmitField, StringField, FloatField, BooleanField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Optional
from app import db
from app.models import Subject

class AddSubjectForm(FlaskForm):
	subject_field = StringField('New Subject', validators=[DataRequired()])
	subject_submit = SubmitField('Add Study Subject')

class RemoveSubjectForm(FlaskForm):
	subject = QuerySelectField(get_label='subject')
	subject_submit = SubmitField('Delete Study Subject')

class NoteForm(FlaskForm):
	question_field = StringField('Question', validators=[DataRequired()])
	answer_field = StringField('Answer', validators=[DataRequired()])
	submit_question = SubmitField('Save Note')