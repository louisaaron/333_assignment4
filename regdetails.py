#!/usr/bin/env python
"""Returns human readable table of classes based on classid"""

#-----------------------------------------------------------------------
# Authors:  Louis Aaron, Max Chan
#-----------------------------------------------------------------------

import sys
import sqlite3
import contextlib

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'
MAX_LINE_LEN = 72
INDENT_LEN = 23

#-----------------------------------------------------------------------

def get_class_details(cursor, classid):
    """Calls all other print fuctions to print all class info"""

    classid = int(classid)

    output = {}

    # getting schedule
    schedule = get_schedule(cursor, classid)
    key_list  = ['id', 'days', 'start', 'end', 'building', 'room']

    for i, key in enumerate(key_list):
        output[key] = schedule[i]

    # getting dept_num
    output['dept_num'] = get_coursenum(cursor, classid)

    # getting course_info
    courseinfo = get_courseinfo(cursor, classid)
    key_list  = ['area', 'title', 'description', 'prereqs']

    for i, key in enumerate(key_list):
        output[key] = courseinfo[i]

    # getting prof(s)
    output['profs'] = get_profs(cursor, classid)

    return output

#-----------------------------------------------------------------------

def get_schedule(cursor, classid):
    """Prints Course ID, Days, Start/End Time, Building, and Room"""

    stmt_str = "SELECT courseid, days, starttime, endtime,"
    stmt_str += " bldg, roomnum FROM classes WHERE classid="
    stmt_str += "? "

    cursor.execute(stmt_str, [classid])

    row = cursor.fetchone()
    row = [str(i) for i in row]

    # output_str = ""
    # output_str += "Course Id: " + str(row[0]) + "\n\n"
    # output_str += "Days: " + str(row[1]) + "\n"
    # output_str += "Start time: " + str(row[2]) + "\n"
    # output_str += "End time: " + str(row[3]) + "\n"
    # output_str += "Building: " + str(row[4]) + "\n"
    # output_str += "Room: " + str(row[5]) + "\n\n"

    return row

#-----------------------------------------------------------------------

def get_coursenum(cursor, classid):
    """Prints course department and course num"""

    stmt_str = "SELECT dept, coursenum "
    stmt_str += "FROM classes, crosslistings "
    stmt_str += "WHERE classes.courseid=crosslistings.courseid "
    stmt_str += "AND classid=?"
    stmt_str += "ORDER BY dept, coursenum"

    cursor.execute(stmt_str, [classid])

    row = cursor.fetchone()

    output = []
    while row is not None:
        row = [str(i) for i in row]
        output.append(str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()

    return output

#-----------------------------------------------------------------------

def get_profs(cursor, classid):
    """Prints professors"""

    stmt_str = "SELECT profname "
    stmt_str += "FROM profs, coursesprofs, classes "
    stmt_str += "WHERE classes.courseid=coursesprofs.courseid "
    stmt_str += "AND coursesprofs.profid=profs.profid "
    stmt_str += "AND classid=?"
    stmt_str += "ORDER BY profname"

    cursor.execute(stmt_str, [classid])

    row = cursor.fetchone()

    output = []
    while row is not None:
        row = [str(i) for i in row]
        output.append(str(row[0]))
        row = cursor.fetchone()

    return output
#-----------------------------------------------------------------------

def get_courseinfo(cursor, classid):
    """Prints course area, title, description, and prerequisites"""

    stmt_str = "SELECT area, title, descrip, prereqs "
    stmt_str += "FROM classes, courses "
    stmt_str += "WHERE classes.courseid=courses.courseid "
    stmt_str += "AND classid=?"

    cursor.execute(stmt_str, [classid])

    row = cursor.fetchone()
    row = [str(i) for i in row]
    #
    # output_str = ""
    # output_str += "Area: " + str(row[0]) + "\n\n"
    # output_str += "Title: " + row[1] + "\n\n"
    # output_str += "Description: " + row[2] + "\n\n"
    # output_str += "Prerequisites: " + row[3] + "\n\n"

    return row

#-----------------------------------------------------------------------

def get_details(classid):
    """Returns human readable table of classes based on classid"""

    output = ""

    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                output = get_class_details(cursor, classid)

    except TypeError:
        error_message = "no class with classid "
        error_message += str(classid) + " exists"
        print(error_message, file=sys.stderr)
        return error_message

    except Exception as ex:
        error_message = str(sys.argv[0]) + ": " + str(ex)
        print(error_message, file=sys.stderr)
        sys.exit(1)

    return output
