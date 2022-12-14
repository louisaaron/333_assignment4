#!/usr/bin/env python

#-----------------------------------------------------------------------
# registrar.py
# Authors: Max Chan, Louis Aaron
#-----------------------------------------------------------------------

import flask
import regdetails
import old_reg

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results():

    dept = flask.request.args.get('dept')
    coursenum = flask.request.args.get('coursenum')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')

    try:
        print("registrar try")
        class_list = old_reg.get_classlist({'d': dept, 'n': coursenum,
        'a': area, 't': title})
        print("registar after query")

        html_code = '<table class="table table-striped table-fit"><tbod'

        html_code += 'y><tr><th scope="col">ClassId</th><th scope="col"'
        html_code += '>Dept</th><th scope="col">Num</th><th scope="col"'
        html_code += '>Area</th><th scope="col">Title</th></tr>'

        pattern = '<tr><td><a href="/regdetails?classid=%s" target="_'
        pattern += 'blank">%s</th><td>%s</td><td>%s</td><td>%s</td><td>'
        pattern += '%s</td></tr>'

        print('before for loop')

        for singular_class in class_list:
            html_code += pattern % (singular_class['id'],
            singular_class['id'], singular_class['dept'],
            singular_class['num'], singular_class['area'],
            singular_class['title'])

        html_code += '</tbody></table>'

        print('before response')

        response = flask.make_response(html_code)

        print('do we get to response?')

        return response

    except Exception:
        print("registar.py error handling")
        err = "A server error occured. Please contact the system "
        err += "administrator."

        html_code = '<div class="container-fluid m-0 p-0">'
        html_code += '<p class="p-0 m-0">'
        html_code += err
        html_code += '</p></div>'

        response = flask.make_response(html_code)
        return response
#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def reg_details():
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

    # class_details = regdetails.get_details(class_id)
    try:
        class_details = regdetails.get_details(class_id)

        if isinstance(class_details, str):
            html_code = flask.render_template('error.html',
            error=class_details)
            response = flask.make_response(html_code)
            # handle errors

        else:
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
