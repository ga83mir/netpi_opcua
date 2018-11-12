from opcua import Client
from opcua import ua
import socket
import time

class opc_ua_client(object):
	def __init__(self, url):
		self.client = None
		self.nodes = {}
		self.values = {}
		self.url = url
	
	def connect(self, opc_name, init_status):
		self.client = Client(self.url)
		CRED = '\33[31m'
		CGREEN = '\33[32m'
		CEND = '\033[0m'
		try:
			self.client.connect()
		except socket.error:
			connect_status = False
			print(opc_name + CRED + " disconnected" + CEND)
			time.sleep(1)
		else:
			if init_status:
				print(opc_name + CGREEN + " connected" + CEND)
			connect_status = True
		return connect_status

	def get_nodes(self, nodeIds):
		nodeId_header = 'ns=4;s=|var|CODESYS Control for Raspberry Pi SL.'
		local_nodes = {}
		for idx in nodeIds:
			var_name = idx.split(".")[-1]
			nodeId = nodeId_header + idx
			local_nodes[var_name] = self.client.get_node(nodeId)
			self.nodes[var_name] = self.client.get_node(nodeId)
		return local_nodes

	def get_value(self, var_name):
		try:
			value = self.nodes[var_name].get_value()
		except socket.error:
			print("can not get value because of no variable there")
			value = None
		return value

	def set_value(self, var_name, value, var_type):
		#""val type must be ua.VariantType, for example ua.VariantType.Boolean")
		try:
			self.nodes[var_name].set_value(value, var_type)
		except socket.error:
			print("can not set value because of no variable there")

	def disconnect(self):
		self.client.disconnect()
