#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
import json
import icmp
from icmp import ApiRos
import socket

app = Flask(__name__)
auth = HTTPBasicAuth()

roo = icmp.ApiRos(ApiRos)

@app.route('/mikrotik/rules', methods=['GET'])
def get_rule():
	return jsonify({roo, roo.printRule()})

@app.route('/mikrotik/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
	rule = [rule for rule in rules if rule['.id'] == rule_id]
	print "hello world"
	if len(rule) == 0:
		abort(404)
	icmp.deleteRule(rule[0])
	return jsonify({'result': True})

if __name__ == '__main__':
	app.run(debug=True)



