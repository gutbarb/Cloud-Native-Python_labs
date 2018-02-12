'''
Cloud Native Python - Chapter 02 - coding-lab

HTTP Method   URI                               Actions
GET           http://localhost:5000/api/v1/info  This responds back with the version
GET           http://localhost:5000/api/v1/users This responds with the user list
GET           http://localhost:5000/api/v1/users/[user_id]  The response will be the user details of the specified user_id
POST          http://localhost:5000/api/v1/users This resource will create new users in the backend server with values from the object passed
DELETE        http://localhost:5000/api/v1/users This resource will delete the user with the specified username passed in JSON format
PUT           http://localhost:5000/api/v1/users/[user_id] This resource updates the user information of the specific user_id based on the JSON object passed as part of the API call.
'''

from flask import Flask, jsonify, make_response, abort, request
#from flask import jsonify
#from flask import make_response
import json
import sqlite3

app = Flask (__name__)



'''
 /api/v1/info ==> GET method - returns api's version information.
'''
@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT buildtime, version, methods, links from apirelease")
    for row in cursor:
        a_dict = {}
        a_dict['version'] = row[0]
        a_dict['buildtime'] = row[1]
        a_dict['methods'] = row[2]
        a_dict['links'] = row[3]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'api_version': api_list}), 200

'''
 /api/v1/users ==> GET method - shows the list of all users.
'''
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()

def list_users():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT username, full_name, email, password, id from users")
    for row in cursor:
        a_dict = {}
        a_dict['username'] = row[0]
        a_dict['name'] = row[1]
        a_dict['email'] = row[2]
        a_dict['password'] = row[3]
        a_dict['id'] = row[4]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'user_list': api_list})

'''
 /api/v1/users/[user_id] ==> GET method - shows the user details defined by user_id.
'''
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

def list_user(user_id):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT * from users where id=?",(user_id,))
    data = cursor.fetchall()
    if len(data) == 0:
        abort(404) # Resource not found
    else:
        user = {}
        user['username'] = data[0][0]
        user['name'] = data[0][1]
        user['email'] = data[0][2]
        user['password'] = data[0][3]
        user['id'] = data[0][4]
    conn.close()
    return jsonify(user)

'''
 /api/v1/users ==> POST method - function to update the user record to the database file
'''
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not password in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name',""),
        'password': request.json['password']
    }
    return jsonify({'status': add_user(user)}), 201

def add_user(new_user): # to update the new user record
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? or email=?",(new_user['username'],new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cursor.execute("insert into users (username, email, password, full_name) values(?,?,?,?)",(new_user['username'],new_user['email'], new_user['password'], new_user['name']))
        conn.commit()
        return "Success"
    conn.close()
    return jsonify(a_dict)




'''
 ERROR HANDLER section
'''
@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)


'''
Basic structure to run an application using Flask. It basically
initializes the Flask variable and runs on port 5000 , which is accessible from anywhere
( 0.0.0.0 )
'''
# app is a Flask object
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
