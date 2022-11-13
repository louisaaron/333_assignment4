#!/usr/bin/env python

#-----------------------------------------------------------------------
# registrar.py
# Authors: Max Chan, Louis Aaron
#-----------------------------------------------------------------------

from urllib.parse import urlencode
import flask
import regdetails
import old_reg

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    dept = flask.request.args.get('dept')
    if dept is None:
        dept=""

    coursenum = flask.request.args.get('coursenum')
    if coursenum is None:
        coursenum=""

    area = flask.request.args.get('area')
    if area is None:
        area=""

    title = flask.request.args.get('title')
    if title is None:
        title=""

    try:
        class_list = old_reg.get_classlist({'d': dept, 'n': coursenum,
        'a': area, 't': title})

        search_dict = {"dept": dept, "coursenum": coursenum,
        "area": area, "title": title}
        search = urlencode(search_dict)

        html_code = flask.render_template('index.html',
        classes=class_list, dept=dept, coursenum=coursenum, area=area,
        title=title)

        response = flask.make_response(html_code)

        response.set_cookie('prev_search', search)

        return response

    except:
        err = "A server error occured. Please contact the system "
        err += "administrator."
        html_code = flask.render_template('error.html', error=err)

        response = flask.make_response(html_code)
        return response

#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def search_results():
    class_id = flask.request.args.get('classid')

    if not isinstance(class_id, str) or class_id == "":
        err = "missing classid"
        html_code = flask.render_template('error.html', error=err)
        response = flask.make_response(html_code)
        return response

    if not class_id.isnumeric():
        err = "non-integer classid"
        html_code = flask.render_template('error.html', error=err)
        response = flask.make_response(html_code)
        return response
    try:
        class_details = regdetails.get_details(class_id)

        if isinstance(class_details, str):
            html_code = flask.render_template('error.html',
            error=class_details)
            response = flask.make_response(html_code)
            # handle errors

        else:
            print('hie')
            cookie = flask.request.cookies.get('prev_search')
            html_code = flask.render_template('search_results.html',
            class_details=class_details, class_id=class_id,
            cookie=cookie)
            response = flask.make_response(html_code)

        return response

    except Exception:
        err = "A server error occured. Please contact the system "
        err += "administrator."
        html_code = flask.render_template('error.html', error=err)

        response = flask.make_response(html_code)
        return response
