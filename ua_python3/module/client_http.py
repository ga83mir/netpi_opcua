import requests
import time
import json
from requests.exceptions import ConnectionError
from datetime import datetime
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CEND = '\033[0m'


class hClient(object):

	def __init__(self, url):
		self.client = None
		self.variables = []
		self.time = []
		self.value = []
		self.var_val = {}
		self.url = url

	def connect(self):
		counter = 0
		status = False
		try:
			self.client = requests.get(self.url, timeout=5)
		except ConnectionError:
			status = False
			print(CRED + ":Failed with ConnectionError" + CEND)
			mk_connect = None
			while not( mk_connect == True or mk_connect == False):
				try:
					mk_connect = input("Do you want to connect with http server again?[True/False]: ")
				except NameError:
					sys.stdout.write('\x1b[1A')
					sys.stdout.write('\x1b[2K')
					print("Press True or False")
					time.sleep(1)
					sys.stdout.write('\x1b[1A')
					sys.stdout.write('\x1b[2K')
		else:
			if self.client.status_code == 200:
				print(CGREEN + ":successful" + CEND)
				status = True
				mk_connect = False
			else:
				print(CRED + ":Failed with Response Error: " + str(self.client.status_code) + CEND)
				mk_connect = input("Do you want to connect with http server agian?[True/False]: ")
		return status, mk_connect

	def reconn(self, hstatus):
		time.sleep(0.5)
		try:
			self.client = requests.get(self.url, timeout=1)
		except ConnectionError:
			status = False
		else:
			if self.client.status_code == 200:
				status = True
		if hstatus != status:
			if status:
				print("Http connection status changed: " + CGREEN + "successfully" + CEND)
			else:
				print("Http connection status changed: " + CRED + "failed" + CEND)
		return status

	def get_last(self):
		with open('./log_file/log_json') as infile:
			jdata = json.load(infile)
		#jdata = self.client.json()
		jPusher1 = jdata['GVL.Pusher1']
		jPusher2 = jdata['GVL.Pusher2']
		jBase = jdata['GVL.Base_End_Sensor']
		ljP1 = list(jPusher1)
		ljP2 = list(jPusher2)
		lB = list(jBase)
		ljP1.sort()
		ljP2.sort()
		lB.sort()
		if len(list(ljP1)) > 0:
			ljPusher1 = list(ljP1)[-1]
		else:
			ljPusher1 = None
		if len(list(ljP2)) > 0:
			ljPusher2 = list(ljP2)[-1]
		else:
			ljPusher2 = None
		if len(list(lB)) > 0:
			lBase = list(lB)[-1]
		else:
			lBase = None

		return [ljPusher1, ljPusher2, lBase]

	
	def get_recently_value(self, status, last):
		'''If the log file contains the most recent value of variables and last change time.
		   Because the log file changed, when a variable changed, even if it changed from true to false or from false to true. For now the last change time can be gotten and compared with the before process.
		   If the last changed time is different with the previous last change time, we can define the production type.
		'''
		if status:
			#time.sleep(2)
			jdata = self.client.json()
			jPusher1 = jdata['GVL.Pusher1']
			jPusher2 = jdata['GVL.Pusher2']
			jBase = jdata['GVL.Base_End_Sensor']
			ljPusher1 = list(jPusher1)
			ljPusher2 = list(jPusher2)
			ljBase = list(jBase)
			for i in ljPusher1:
				if jPusher1[i]==False:
					del jPusher1[i]
			for i in ljPusher2:
				if jPusher2[i]==False:
					del jPusher2[i]
			for i in ljBase:
				if jBase[i]==False:
					del jBase[i]
			ljPusher1 = list(jPusher1)
			ljPusher2 = list(jPusher2)
			ljBase = list(jBase)
			ljPusher1.sort()
			ljPusher2.sort()
			ljBase.sort()
			#print(type(ljBase[-1]))
			#print(type(last[2]))
			log = False
			pro_type = None

			if len(ljPusher1) > 0:
				if ljPusher1[-1] > last[0]:
					pro_type = 0
					log = True
			if len(ljPusher2) > 0:
				if ljPusher2[-1] > last[1]:
					pro_type = 1
					log = True
			if len(ljBase) > 0:
				if ljBase[-1] > last[2]:
					pro_type = 2
					log = True
		else:
			pro_type = 0
			log = None
						
		return pro_type, log

	def write_logfile(self):
		jdata = self.client.json()
		ljdata = list(jdata)
		lljdata = list(ljdata)
		for idx in lljdata:
			for time in list(jdata[idx]):
				if jdata[idx][time] == False:
					del jdata[idx][time]
		
		with open('./log_file/log_json', 'w') as outfile:
			json.dump(jdata, outfile)
