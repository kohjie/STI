#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import os, firewallcrud, csv, json, subprocess

mikrotik = Flask(__name__)

@mikrotik.route('/todo/api/mikrotik/firewallrule/create', methods=['POST'])
def create_rule():
	chain = request.json['chain']
	action = request.json['action']
	rejectw = request.json['rejectw']
	protocol = request.json['protocol']
	src = request.json['src']
	dst = request.json['dst']
	log = request.json['log']

	subprocess.call(['./test.sh', 'create', chain, action, rejectw, protocol, src, dst, log])

	with open('file.txt') as f:
		output = f.read()

	return jsonify({'chain': chain, 'action': action, 'reject-with': rejectw, 'protocol': protocol, 'source address': src, 'destination address': dst, 'log': log})

#curl -i -H "Content-Type: application/json" -X POST -d '{"chain":"input", "action":"accept", "rejectw":"icmp-network-unreachable", "protocol":"icmp", "src":"10.10.10.0/24", "dst":"10.10.10.0/24", "log":"no"}' http://localhost:5000/todo/api/mikrotik/firewallrule/create 

@mikrotik.route('/todo/api/mikrotik/firewallrule/print', methods=['GET'])
def get_rule():
	subprocess.call(['./test.sh', 'print'])

	with open('file.txt') as f:
		output = f.read()

	return jsonify({'rules': output})

#curl -i http://localhost:5000/todo/api/mikrotik/firewallrule/print

@mikrotik.route('/todo/api/mikrotik/firewallrule/update/<numbers>', methods=['PUT'])
def update_rule(numbers):
    	chain = request.json['chain']
	action = request.json['action']
	rejectw = request.json['rejectw']
	protocol = request.json['protocol']
	src = request.json['src']
	dst = request.json['dst']
	log = request.json['log']

    	subprocess.call(['./test.sh', 'update', numbers, chain, action, rejectw, protocol, src, dst, log])

    	with open('file.txt') as f:
		output = f.read()

    	return jsonify({'rule': output})

#curl -i -H "Content-Type: application/json" -X PUT -d '{"action":"reject"}' http://localhost:5000/todo/api/mikrotik/firewallrule/update/<numbers>
#curl -i -H "Content-Type: application/json" -X PUT -d '{"chain":"input", "action":"drop", "rejectw":"icmp-network-unreachable", "protocol":"icmp", "src":"10.10.10.0/24", "dst":"10.10.10.0/24", "log":"no"}' http://localhost:5000/todo/api/mikrotik/firewallrule/update/1


@mikrotik.route('/todo/api/mikrotik/firewallrule/delete/<numbers>', methods=['DELETE'])
def delete_rule(numbers):
	subprocess.call(['./test.sh', 'delete', numbers])

	with open('file.txt') as f:
		output = f.read()

	return jsonify({'rules': output, 'delete': True})

#curl -i http://localhost:5000/todo/api/mikrotik/firewallrule/delete/<numbers>

if __name__ == '__main__':
	mikrotik.run(debug=True)



