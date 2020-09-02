from eu4 import log
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    SubmitField
)
from eu4.endpoints.paradox import DIFFICULT


levels =[(x[1],x[1]) for x in DIFFICULT.items()]
levels.append(("None", ""))
log.info(f"LEVELS: {levels}")

class FilteresForm(FlaskForm):
    achieved = StringField("achieved")
    difficult = SelectField("difficult", choices=levels)
    version = StringField("version")
    random = BooleanField("random", default=False)
    submit = SubmitField("Filter")
    word = StringField("achieved")