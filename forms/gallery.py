from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired


class AddImage(FlaskForm):
    file = wtforms.FileField()
    # file = wtforms.FileField('Вберете файл', validators=[DataRequired())

    # submit = wtforms.SubmitField('Отправить')
