import json
import sqlite3
from werkzeug.exceptions import HTTPException
import atexit
from flask import Flask, request, Response, render_template, jsonify
APP = Flask(__name__)


##################################################################
#   START/END FUNCTIONS                                          #
#################################################################

def startup():
    """
        Function to present the index page
        """
    json = {}
    results =[]
    temp = {}
    temp[[0][0]] = {}
    temp[[0][0]]["title"] = "Welcome to Selfieless Acts"
    results.append(temp[[0][0]])
    json["index"] = results
    return results

def shutdown():
    """
    Function to ensure the database is closed during app exit
    """
    global conn

    #close database
    conn.commit()
    conn.close()

##################################################################
#   DATABASE FUNCTIONS                                          #
#################################################################

def user_create(user_name, password):
    """
    This function creates a user

    :param user_name: user name
    :type user_name: str
    :param password: user password
    :type password: str
    """
    global conn
    global cursor

    try:
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute(
            """INSERT INTO users (usr_name, password)
            VALUES (?, ?)""",
            (user_name, password)
        )
        conn.commit()
        return True
    except Exception as err:
        return False

def user_remove(username):
    """
    This function removes a user.

    :param user_id: user ID
    :type user_id: int
    """
    global conn
    global cursor

    try:
        cursor.execute(
            "DELETE FROM users WHERE usr_name=?",
            (username,)
        )
        conn.commit()
        #check whether an user was removed
        if cursor.rowcount > 0:
            return True
        return False
    except:
        return False

##################################################################
#   FLASK FUNCTIONS                                              #
#################################################################

@APP.route("/")
def index():
    """
    This function presents the main page.
    """
    return jsonify(startup())

@APP.route("/api/v1/users", methods=["POST"])
def api_create_user():
    """
    This function creates a user
    """
        
    try:
        myname = request.form["name"]
        mypwd = request.form["password"]
    except:
        #400 Bad Request
        return jsonify(error=400), 400
    user=""
    password=""

    user+=(str(myname))
    password+=(str(mypwd))
    

    if(len(password)!=40):
        return jsonify(error=400), 400
        
    for char in password:
        if ((((char>='0' and char<='9') or (char>='A' and char<='F') or (char>='a' and char<='f'))) != True):
            return jsonify(error=400), 400

    if user_create(
                    request.form["name"], request.form["password"]
                    ):
        #201 Created
        return jsonify(success=201), 201
    return jsonify(error=400), 400

@APP.route("/api/v1/users/<path:username>", methods=["DELETE"])
def api_delete_user(username):
    """
    This function deletes a particular user.

    :param username: user name
    :type username: str
    """
    result = user_remove(username)
    if result:
        return jsonify(success=200), 200
    else:
        return jsonify(error=400), 400

@APP.errorhandler(HTTPException)
def handle_error(e):
    try:
        if e.code < 400:
            return flask.Response.force_type(e, flask.request.environ)
        elif e.code == 404:
            return jsonify(error=404), 404
        raise e
    except:
        return jsonify(error=405), 500

##################################################################
#   MAIN FUNCTION                                                #
#################################################################

if __name__ == "__main__":
    global conn
    global cursor

    # 'At exit' calls functions when a program is closing down
    # Here, the shutdown function is called on program exit
    atexit.register(shutdown)
    #Start the database
    #check_same_thread is set to False to allow the connection to run on multiple threads
    conn = sqlite3.connect("selfieless.db", check_same_thread=False)
    cursor = conn.cursor()
    APP.run(debug=False)
