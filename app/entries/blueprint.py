from flask import Blueprint
from helpers import object_list
from models import Entry, Tag
from entries.forms import EntryForm
from flask import render_template
from flask import request, redirect, url_for
from app import db

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    if (tags is None):
        return "No Tags"
    else:
        return object_list('entries/tag_index.html', tags)


@entries.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/tag_detail.html', entries, tag=tag)


@entries.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate() == False:
            return render_template('entries/create.html', form=form)
        else:
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.
            slug))
    else:
        form = EntryForm()
        return render_template('entries/create.html', form=form)


@entries.route('/<slug>')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)


@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    if request.method == 'POST':
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm(obj=entry)
        return render_template('entries/edit.html', entry=entry, form=form)


def entry_list(template, query, **context):
    search = request.args.get('q')
    if search:
        query = query.filter((Entry.body.contains(search))| (Entry.title.contains(search)))
    return object_list(template, query, **context)