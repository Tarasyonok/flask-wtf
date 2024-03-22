import datetime
import os
import json


import flask
from werkzeug.utils import secure_filename

from forms.gallery import AddImage

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(400)
def bad_request(_):
    return flask.make_response(flask.jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(_):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


def main():
    app.run()


@app.route("/index/<title>/")
def index(title):
    param = {}
    param['title'] = title
    return flask.render_template('base.html', **param)


@app.route("/training/<prof>/")
def training(prof):
    param = {}
    param['title'] = prof
    if 'инженер' in prof.lower():
        param['prof'] = 'Инженерные тренажеры'
        param['img'] = 'engineer.png'
    else:
        param['prof'] = 'Научные симуляторы'
        param['img'] = 'science.png'
    return flask.render_template('training.html', **param)


@app.route("/list_prof/<list_type>/")
def list_prof(list_type):
    param = {}
    param['title'] = list_prof
    param['list_prof'] = ['Инженер-исследователь', 'Пилот', 'Строитель', 'Врач', 'Штурман']
    param['list_type'] = list_type

    return flask.render_template('list_prof.html', **param)


@app.route("/answer/")
@app.route("/auto_answer/")
def auto_answer():
    param = {}
    param['title'] = 'Анкета'
    param['fields'] = [
        ['title', 'test'],
        ['surname', 'test'],
        ['name', 'test'],
        ['education', 'test'],
        ['profession', 'test'],
        ['sex', 'test'],
        ['motivation', 'test'],
        ['ready to stay on mars', 'test'],
    ]

    return flask.render_template('auto_answer.html', **param)

@app.route("/double_check/")
def double_check():
    param = {}
    return flask.render_template('double_check.html', **param)


@app.route("/distribution/")
def distribution():
    param = {}
    param['names'] = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Шон Бин']
    return flask.render_template('distribution.html', **param)


@app.route("/table/<gender>/<int:age>/")
def table(gender, age):
    param = {}
    color = ''
    if gender == "male":
        color += 'm'
    else:
        color += 'f'

    if age <= 21:
        color += 'y'
        param['image'] = 's'
    else:
        color += 'a'
        param['image'] = 'b'

    param['walls_color'] = color

    return flask.render_template('table.html', **param)


images = []


@app.route("/gallery/",  methods=['GET', 'POST'])
def gallery():

    form = AddImage()
    if form.validate_on_submit():

        filename = secure_filename(form.file.data.filename)
        now = str(datetime.datetime.now())
        now_name = now.split(".")[0].replace("-", ".").replace(":", "-")
        file_name = f'static/images/gallery/{now_name}.png'
        images.append("{{ url_for('static', filename='" + file_name + ".jpg') }}")
        form.file.data.save(file_name)
        # images.append('uploads/' + filename)
        print(filename)

        # form.file.data.save('uploads/' + filename)

        return flask.redirect('/gallery/')

    param = {}
    param['images'] = []
    for f_name in next(os.walk('static/images/gallery'))[2]:
        param['images'].append("/static/images/gallery/" + f_name)
    print(param['images'])

    param['title'] = 'Галерея'
    param['form'] = form





    return flask.render_template('gallery.html', **param)

@app.route("/member/")
def member():
    param = {}

    with open('templates/members_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        param['members'] = data

    return flask.render_template('member.html', **param)

main()
