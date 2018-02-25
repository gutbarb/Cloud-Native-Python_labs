'''
   Cloud Native Python - Chapter 02 - Building Microservices in Python
'''

from flask import Flask, jsonify, make_response, abort
from flask import request, render_template
import json
import sqlite3
from time import gmtime, strftime

app = Flask (__name__)

##### Version 1 APIs - Users - #######

'''
 /api/v1/info ==> GET method - returns api's version information.
'''
@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT buildtime, version, methods, links from\
    apirelease")
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
    cursor = conn.execute("SELECT username, full_name, email, password,\
    id from users")
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
 /api/v1/users/[user_id] ==> GET method - shows the user details defined
                                          by user_id.
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
 /api/v1/users ==> POST method - function to update the user record to
                                 the database file
'''
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email'\
     in request.json or not 'password' in request.json:
         abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name',""),
        'password': request.json['password']
    }
    return jsonify({'status': add_user(user)}), 201

def add_user(new_user):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? or email=?",\
    (new_user['username'],new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cursor.execute("insert into users (username, email, password,\
         full_name) values(?,?,?,?)",(new_user['username'],\
         new_user['email'], new_user['password'], new_user['name']))
        conn.commit()
        return "Success"
    conn.close()
    return jsonify(a_dict)


'''
 /api/v1/users ==> DELETE method - remove 1 record defined by username
'''
@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200

def del_user(del_user):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? ", (del_user,))
    data = cursor.fetchall()
    print("Data", data)
    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("delete from users where username=?", (del_user,))
        conn.commit()
    return "Success"

'''
 /api/v1/users ==> PUT method - update 1 record specified by user_id
'''
@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print (user)
    return jsonify({'status': upd_user(user)}), 200

def upd_user(user):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where id=?", (user['id'],))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
        abort(404)
    else:
        key_list=user.keys()
        for i in key_list:
            if i != "id":
                print (user, i)
                cursor.execute("""UPDATE users SET {0} = ? WHERE  id = \
                ?""".format(i),(user[i], user['id']))
                conn.commit()
        return "Success"


##### Version 2 APIs - Tweets - #######

'''
 /api/v2/tweets ==> GET method - lists all tweets from all users
'''
@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

def list_tweets():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT username, body, tweet_time, id from tweets")
    data = cursor.fetchall()
    if len(data) != 0:
        for row in data:
            tweets = {}
            tweets['Tweet By'] = row [0]
            tweets['Body'] = row [1]
            tweets['Timestamp'] = row [2]
            tweets['id'] = row[3]
            api_list.append(tweets)
    else:
        return api_list
    conn.close()
    return jsonify({'tweets_list': api_list})

'''
 /api/v2/tweets ==> POST method - adds new tweets by a specified user
'''
@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body'\
     in request.json:
         abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    print (user_tweet)
    return jsonify({'status': add_tweet(user_tweet)}), 200

def add_tweet(new_tweets):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where username=? ",\
     (new_tweets['username'],))
    data = cursor.fetchall()
#   print (">>>>>> user in db: ", data)
    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("INSERT into tweets (username, body, tweet_time)\
         values (?,?,?)", (new_tweets['username'], new_tweets['body'],\
          new_tweets['created_at']))
        conn.commit()
        print ("tweet added")
        return "Success"

'''
 /api/v2/tweets/[id] ==> GET method - shows the tweet specified by the ID 
'''
@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)

def list_tweet(user_id):
    print (user_id)
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list = []
    cursor = conn.cursor()
    cursor.execute("SELECT * from tweets where id=?", (user_id,))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
        abort(404)
    else:
        user = {}
        user['id'] = data[0][0]
        user['username'] = data[0][1]
        user['body'] = data[0][2]
        user['tweet_time'] = data[0][3]
    conn.close()
    return jsonify(user)


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
initializes the Flask variable and runs on port 5000 , which is 
accessible from anywhere ( 0.0.0.0 )
'''
# app is a Flask object
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
