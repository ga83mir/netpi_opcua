import sys
import os
import json
sys.path.insert(0, "./module")

import time
from opcua import ua
from client_http import hClient
from client_opc_ua import opc_ua_client
from datetime import datetime

def add_logfile(hstatus, pro_type):
	ctime = str(datetime.now())
	chstatus = ', http server status: ' + str(hstatus)
	cpt = ', product type: ' + str(pro_type)
	data = ctime + chstatus + cpt + '\n'
	with open('./log_file/log_history', 'a') as appfile:
		appfile.write(data)

def report_error(hstatus, hI, ostatus, oI):
	if not (hstatus and ostatus):
		ctime = str(datetime.now())
		err = ""
		if not hstatus:
			if hI:
				err += " http connect(Interrupt)"
			else:
				err += " http connect(Failure)"
		if not ostatus:
			if oI:
				opc_inter = "(Interrupt)"
			else:
				opc_inter = "(Failure)"
			if err == "":
				err += "opcua connect"
				err += opc_inter
			else:
				err += " and opcua connect"
				err += opc_inter
		data = ctime + ", error from" + err + "\n"
		with open('./log_file/log_error', 'a') as appfile:
			appfile.write(data)

def initialization():
	path = './log_file'
	fd = False
	log_data = {u'GVL.Base_End_Sensor': {}, u'GVL.Pusher2':{},
			u'GVL.Pusher1':{}}

	for file in os.listdir(path):
		if file == 'log_json':
			open_path = path + "/" + file
			with open(open_path) as infile:
				jdata = json.load(infile)
			for data in list(log_data):
				if data not in list(jdata):
					fd = False
					break
				fd = True
	if fd == False:
		print('log file is miss or broken, new log file')
		log_data = {u'GVL.Base_End_Sensor': {"0": True},  u'GVL.Pusher2':{"0": True},
				u'GVL.Pusher1':{"0": True}}
		with open('./log_file/log_json', 'w') as outfile:
			json.dump(log_data, outfile)

def main():
	#set parameters to connect with http server(default server is online)
	http_url = "http://129.187.88.30:4567/observedVariables"
	http_client = hClient(http_url)
	make_connection = True

	#set parameters to connect with local codesys plc
	opc_url = "opc.tcp://localhost:4840"
	opc_client = opc_ua_client(opc_url)

	#set somne variables for counter and production type
	pro_type = -1
	init_status = True
	CRED = '\33[31m'
	CGREEN  = '\33[32m'
	CEND = '\033[0m'

	#start with a endless loop
	while True:
		#try to get connect with http server
		make_connection = True
		sys.stdout.flush()
		while make_connection:
			if init_status:
				print("connecting to the http server ", end="")
				sys.stdout.flush()
				http_status, make_connection = http_client.connect()
			else:
				http_status = http_client.reconn(http_status)
				make_connection = False

		#If http connect, get product type. If not product type will be$
		if http_status:
			#get information from previous process or not
			if init_status:
				sys.stdout.flush()
				print("start under" + CGREEN + " online" + CEND + " mode")
			last = http_client.get_last()

			#wait, till the log file changed
			log = False
			print("Getting type from http server...", end="\r")
			sys.stdout.flush()
			try:
				while not log:
					http_status = http_client.reconn(http_status)
					#print(last)
					http_pro_type, log = http_client.get_recently_value(http_status, last)
					if log==None:
						http_status = False
						break
			except KeyboardInterrupt:
				sys.stdout.write('\x1b[2K')
				http_status = False
				http_pro_type = pro_type + 1
				print("\rPress Interrupt and change to "+CRED+"offline"+CEND+ " mode")
				http_inter = True

			sys.stdout.write('\x1b[2K')
			if log==None:
				print(CRED+"Connection break off"+CEND)
				http_pro_type = pro_type + 1
			if log==True:
				http_client.write_logfile()

		else:
			if init_status:
				sys.stdout.flush()
				print("start under"+ CRED + " offline" + CEND + " mode")
			http_pro_type = pro_type + 1
			if http_pro_type == 3:
				http_pro_type = 0

		#try to get connect with opc server
		opc_status = opc_client.connect('opcua', init_status)
		if opc_status:
			opc_get_nodeIds = ['Application.PLC_PRG.fb_opc_get.b_opc_request',
						'Application.PLC_PRG.fb_opc_get.b_opc_answer',
						'Application.PLC_PRG.fb_opc_get.i_opc_type',
						'Application.PLC_PRG.fb_opc_get.b_http',]

			opc_send_nodeIds = ['Application.PLC_PRG.fb_opc_send.b_opc_process',
						'Application.PLC_PRG.fb_opc_send.i_opc_counter',]

			opc_get_nodes = opc_client.get_nodes(opc_get_nodeIds)
			opc_send_nodes = opc_client.get_nodes(opc_send_nodeIds)
			pro_type = http_pro_type

			while not opc_client.get_value('b_opc_request'):
				print("wait opc server requests")
				time.sleep(1)

			if http_status:
				print("Producting(" + CGREEN+"online"+CEND+") with type: " + str(http_pro_type), end=" ")
			else:
				print("Producting(" + CRED +"offline"+CEND+") with type: " + str(http_pro_type), end=" ")
			sys.stdout.flush()

			pro_type = http_pro_type
			opc_client.set_value('b_http', http_status, ua.VariantType.Boolean)
			opc_client.set_value('i_opc_type', pro_type, ua.VariantType.Int16)
			opc_client.set_value('b_opc_answer', True, ua.VariantType.Boolean)


			try:
				opc_b_opc_process = False
				while not opc_b_opc_process:
					opc_b_opc_process = opc_client.get_value('b_opc_process')
				while opc_b_opc_process:
					opc_b_opc_process = opc_client.get_value('b_opc_process')
				opc_client.set_value('b_opc_answer', False, ua.VariantType.Boolean)
				sys.stdout.flush()
				print(CGREEN + '     ...done' + CEND)
			except KeyboardInterrupt:
				retry = None
				opc_inter = True
				opc_status = False
				opc_client.set_value('b_opc_answer', False, ua.VariantType.Boolean)
				sys.stdout.flush()
				print(CRED + '     ...Interrupt' + CEND)
				while retry != 'True' and retry != 'False':
					retry = input('Do you want to retry?[True/False]: ')
				if retry == 'True':
					retry = True
				if retry == 'False':
					retry = False
				opc_client.disconnect()
				report_error(http_status, http_inter, opc_status, opc_inter)
				return retry
			opc_counter = opc_client.get_value('i_opc_counter')
			opc_client.disconnect()
			init_status = False

			# write plc log file
			add_logfile(http_status, pro_type)
			report_error(http_status, http_inter, opc_status, False)

		else:
			init_status = False
			while True:
				retry = input("Do you want to connect with opcua server again?[True/False]: ")
				if retry == 'True':
					retry = True
					break
				if retry == 'False':
					retry = False
					break

			report_error(http_status, http_inter, opc_status, False)
			if not retry:
				print("please checkt the PLC and Ethernet and restart the program")
				return retry
			time.sleep(1)

def  key_exit():
	opc_url = "opc.tcp://localhost:4840"
	opc_client = opc_ua_client(opc_url)
	opc_status = opc_client.connect('opcua', False)
	if opc_status:
		opc_spec_nodeIds = ['Application.PLC_PRG.fb_opc_get.b_opc_answer',]
		opc_spec_nodes = opc_client.get_nodes(opc_spec_nodeIds)
		opc_client.set_value('b_opc_answer', False, ua.VariantType.Boolean)
		opc_client.disconnect()
		sys.stdout.flush()
	print('Program Exit')

if __name__=='__main__':
	initialization()
	retry = True
	try:
		while retry:
			retry = main()
	except KeyboardInterrupt:
		pass
	finally:
		key_exit()
		exit()
