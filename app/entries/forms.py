import wtforms
from wtforms.validators import DataRequired
from models import Entry

class EntryForm(wtforms.Form):
    title = wtforms.StringField('Title', validators=[DataRequired('Please enter a title')])
    body = wtforms.StringField('Body', validators=[DataRequired('Please enter body')])
    status = wtforms.SelectField('Entry status',
                                 choices=((Entry.STATUS_PUBLIC, 'Public'),
                                         (Entry.STATUS_DRAFT, 'Draft')),
                                         coerce = int)

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry