# results_controller.py
from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
import random
from app import db

# def results_controller(learning_session_id)