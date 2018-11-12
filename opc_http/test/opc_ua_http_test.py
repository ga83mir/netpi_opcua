from __future__ import print_function
import sys
sys.path.insert(0, "../module")

import time
import logging
from opcua import ua
from client_http import hClient
from client_opc_ua import opc_ua_client

def main():

		#set parameters to connect with http server(default server is online)
		http_url = "http://129.187.88.30:4567/observedVariables"
		http_client = hClient(http_url)
		make_connection = True

		#set parameters to connect with local codesys plc
		opc_url = "opc.tcp://localhost:4840"
		opc_client = opc_ua_client(opc_url)

		#set somne variables for counter and production type
		http_pro_type = -1
		init_status = True
		not_use_init = True
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
					lt_Pusher1, lt_Pusher2, len1, len2 = http_client.get_init()
					sys.stdout.flush()
					print("start under" + CGREEN + " online" + CEND + " mode")
				if not_use_init:
					lt_Pusher1 = 0
					lt_Pusher2 = 0
					len1 = 0
					len2 = 0
					not_use_init = False
					#print('not use init process')

				#wait, till the log file changed
				log = False
				tcounter = 0
				print("Getting type from http server", end="\r")
				sys.stdout.flush()
				tt0 = time.time()
				while not log:
					http_status = http_client.reconn(http_status)
					if time.time()-tt0 > 5:
						http_status = False
					http_pro_type, lt_Pusher1, lt_Pusher2, log = http_client.get_recently_value(http_status, lt_Pusher1, lt_Pusher2)
					if log==None:
						http_status = False
						break
				sys.stdout.write('\x1b[2K')
				if log==None:
					print(CRED+"Connection break off"+CEND)

			else:
				if init_status:
					sys.stdout.flush()
					print("start under"+ CRED + " offline" + CEND + " mode")
				http_pro_type += 1
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

				while not opc_client.get_value('b_opc_request'):
					print("wait opc server requests")
					time.sleep(1)

				if http_status:
					print("Product(" + CGREEN+"online"+CEND+") with type: " + str(http_pro_type), end=" ")
					make_connection = True
				else:
					print("Product(" + CRED +"offline"+CEND+") with type: " + str(http_pro_type), end=" ")
					make_connection = False
				sys.stdout.flush()

				opc_client.set_value('b_http', http_status, ua.VariantType.Boolean)
				opc_client.set_value('i_opc_type', http_pro_type, ua.VariantType.Int16)
				opc_client.set_value('b_opc_answer', True, ua.VariantType.Boolean)

				opc_b_opc_process = False
				while not opc_b_opc_process:
					opc_b_opc_process = opc_client.get_value('b_opc_process')
				while opc_b_opc_process:
					opc_b_opc_process = opc_client.get_value('b_opc_process')
				opc_client.set_value('b_opc_answer', False, ua.VariantType.Boolean)
				sys.stdout.flush()
				print('     ...done')

				opc_counter = opc_client.get_value('i_opc_counter')
				opc_client.disconnect()
				init_status = False
				if http_url == "http://129.187.88.30:4567/observedVariables":
					http_url = "http://129.187.8.30:4567/observedVariables"
					http_client = hClient(http_url)
				else:
					http_url = "http://129.187.88.30:4567/observedVariables"
			                http_client = hClient(http_url)
			
			else:
				retry = None
				init_status = False
				while retry != False and retry != True:
					retry = input("Do you want to connect with opcua server again?[True/False]: ")
				if not retry:
					print("please checkt the PLC and Ethernet and restart the program")
					break
				time.sleep(1)
if __name__=='__main__':
	main()
	quit()
