#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import flask

app = flask.Flask(__name__, template_folder='.')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
  html_code = flask.render_template('index.html')
  response = flask.make_response(html_code)
  print(response)
  return response

@app.route('/regdetails', methods=['GET'])
def regdetails():
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
      # class_details = regdetails.get_details(class_id)
      class_details = ""

      if isinstance(class_details, str):
          html_code = flask.render_template('error.html',
          error=class_details)
          response = flask.make_response(html_code)
          # handle errors

      else:
          cookie = flask.request.cookies.get('prev_search')

          html_code = flask.render_template('regdetails.html',
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