#!/usr/bin/env python
"""Returns table classes that fit user query"""

#-----------------------------------------------------------------------
# Authors:  Louis Aaron, Max Chan
#-----------------------------------------------------------------------

import sqlite3
import contextlib
import sys

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'
MAX_LINE_LEN = 72
INDENT_LEN = 23

#-----------------------------------------------------------------------

def get_classes(cursor, query):
    """Returns formatted table of classes"""
    print("entered get_classes")
    stmt_str = init_stmt_str()

    list_args=get_args(query)

    cursor.execute(stmt_str, list_args)

    row = cursor.fetchone()

    class_list = []

    while row is not None:
        class_list.append(format_row(row))
        row = cursor.fetchone()

    return class_list

#-----------------------------------------------------------------------

def format_row(row):
    """Convers list output from SQL row into dict"""

    row = ({'id': str(row[0]), 'dept': str(row[1]), 'num': str(row[2]),
    'area': str(row[3]), 'title': str(row[4])})

    return row

#-----------------------------------------------------------------------

def init_stmt_str():
    """Populates stmt_str with initial SQL query language"""

    stmt_str = "SELECT classid, dept, coursenum, area, title"
    stmt_str += " FROM classes, courses, crosslistings"
    stmt_str += " WHERE classes.courseid=courses.courseid"
    stmt_str += " AND courses.courseid=crosslistings.courseid"
    stmt_str += " AND classes.courseid=crosslistings.courseid"

    stmt_str += " AND lower(dept) LIKE ? ESCAPE '\\'"
    stmt_str += " AND lower(coursenum) LIKE ? ESCAPE '\\'"
    stmt_str += " AND lower(area) LIKE ? ESCAPE '\\'"
    stmt_str += " AND lower(title) LIKE ? ESCAPE '\\'"

    stmt_str += " ORDER BY dept, coursenum, classid"

    return stmt_str

#-----------------------------------------------------------------------

def get_args(args):
    """Populates args_list to fill in cmd line args for SQL query"""

    args_list = ['%', '%', '%', '%']

    if args['d']:
        args['d'] = args['d'].replace("%", r"\%")
        args['d'] = args['d'].replace("_", r"\_")
        args_list[0]="%" + args['d'].lower() + "%"
    if args['n']:
        args['n'] = args['n'].replace("%", r"\%")
        args['n'] = args['n'].replace("_", r"\_")
        args_list[1]="%" + args['n'].lower() + "%"
    if args['a']:
        args['a'] = args['a'].replace("%", r"\%")
        args['a'] = args['a'].replace("_", r"\_")
        args_list[2]="%" + args['a'].lower() + "%"
    if args['t']:
        args['t'] = args['t'].replace("%", r"\%")
        args['t'] = args['t'].replace("_", r"\_")
        args_list[3]="%" + args['t'].lower() + "%"

    return args_list

#-----------------------------------------------------------------------

def get_classlist(query):
    """Returns human readable table of classes that fit user query"""

    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                output = get_classes(cursor, query)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

    return output
#-----------------------------------------------------------------------
