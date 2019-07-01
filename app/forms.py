from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectField, SubmitField, StringField, FloatField, BooleanField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Optional
from app import db

class AddSubjectForm(FlaskForm):
	subject_field = StringField('New Subject')
	subject_submit = SubmitField('Add Study Subject')

class RemoveSubjectForm(FlaskForm):
	subject_text = QuerySelectField(get_label='subject')
	subject_submit = SubmitField('Delete Study Subject')
