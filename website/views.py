from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from sqlalchemy.sql import func
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route("/edit-note/<int:nid>/", methods=["POST"])
def edit_note(nid):
    newNote = request.form
    newText = newNote.get("text")
    note = Note.query.get(nid)
    if note:
        if note.user_id == current_user.id:
            note.data = newText
            note.date = func.now()
            db.session.commit()
            flash("Note modified!", category='success')
        else:
            flash("The note is not owned by you!", category="error")
    else:
        flash("An error occured!", category="error")
    return redirect('/')

