#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
import os, addrlistcrud, csv, json, subprocess, re

mikrotik = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'admin':
		return 'python'
	return None

#ERROR HANDLER 401/403
@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 403)

#ERROR HANDLER 400
@mikrotik.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

#ERROR HANDLER 404
@mikrotik.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

#CREATE LIST
#curl -u admin:python -i -H "Content-Type: application/json" -X POST -d '{"address":"20.20.20.0/24", "list":"20network"}' http://localhost:5000/todo/api/mikrotik/addrlist/create
@mikrotik.route('/todo/api/mikrotik/addrlist/create', methods=['POST'])
def create_rule():
	address = request.json['address']
	l = request.json['list']

	subprocess.call(['./test.sh', 'createlist', address, l])

	with open('file.txt') as f:
		output = f.read()
	
	return jsonify({'address': address, 'list': l})

#PRINT ALL LISTS
#curl -u admin:python -H "Content-Type: application/json" -i http://localhost:5000/todo/api/mikrotik/addrlist/print
@mikrotik.route('/todo/api/mikrotik/addrlist/print', methods=['GET'])
def get_rule():
	subprocess.call(['./test.sh', 'printlist'])

	with open('file.txt') as f:
		output = f.read()
		output2 = re.split('\n', output)

	return jsonify({'Created Address List(s)': output2})

#UPADTE LIST
#curl -u admin:python -i -H "Content-Type: application/json" -X PUT -d '{"address":"30.30.30.0/24", "list":"30network"}' http://localhost:5000/todo/api/mikrotik/addrlist/update/<numbers>
@mikrotik.route('/todo/api/mikrotik/addrlist/update/<numbers>', methods=['PUT'])
def update_rule(numbers):
    	address = request.json['address']
	l = request.json['list']

    	subprocess.call(['./test.sh', 'updatelist', numbers, address, l])

    	with open('file.txt') as f:
		output = f.read()
		output2 = re.split('\n', output)

	return jsonify({'Updated Address List': output2})

#DELETE LIST
#curl -u admin:python -H "Content-Type: application/json" -X DELETE -i http://localhost:5000/todo/api/mikrotik/addrlist/delete/<numbers>
@mikrotik.route('/todo/api/mikrotik/addrlist/delete/<numbers>', methods=['DELETE'])
def delete_rule(numbers):
	subprocess.call(['./test.sh', 'deletelist', numbers])

	with open('file.txt') as f:
		output = f.read()
		output2 = re.split('\n', output)
	return jsonify({'Deleted List': output2, 'delete': True})

if __name__ == '__main__':
	mikrotik.run(debug=True)



