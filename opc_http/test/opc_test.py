import requests
import opcua
from opcua import ua
import time
import socket
from random import randint


def main():
	http_url = "http://129.187.88.30:4567/observedVariables"
	#opc_url = "opc.tcp://localhost:4840"
	opc_url = "opc.tcp://localhost:4888"
	pro_type = -1

	#first try to get connect with http server
	http_status = True
	while True:	
		if http_status:
		        try:
        		        http_client = requests.get(http_url)
	        	except requests.exceptions.ConnectionError:
        	        	#print("http connect failed")
				http_status = False
		        else:
        		        print("connect succssfully")
				http_status = True
	
		try:	
			opc_client = opcua.Client(opc_url)
			opc_client.connect()
		except socket.error:
			print("opo ua server connect failed")
			opc_status = False
			time.sleep(5)
		else:
			print("opc ua server connect successfully")
			nodeId_header = 'ns=4;s=|var|CODESYS Control for Raspberry Pi SL.'	
                	opc_get_nodeIds = ['Application.PLC_PRG.fb_opc_get.b_opc_request', 
                        	           'Application.PLC_PRG.fb_opc_get.b_opc_answer',
                                	   'Application.PLC_PRG.fb_opc_get.i_opc_type',
                                    	   'Application.PLC_PRG.fb_opc_get.b_http',]
	                opc_send_nodeIds = ['Application.PLC_PRG.fb_opc_send.b_opc_process',
        	                            'Application.PLC_PRG.fb_opc_send.i_opc_counter',]
			opc_gvl = ['Application.GVL_Inputs.b_i_workpiece_at_beginning',]
			nodeIds = {}
			for idx in opc_get_nodeIds:
				var_name = idx.split(".")[-1]
				nodeId = nodeId_header + idx
				nodeIds[var_name] = opc_client.get_node(nodeId)
			for idx in opc_send_nodeIds:
				var_name = idx.split(".")[-1]
				nodeId = nodeId_header + idx
				nodeIds[var_name] = opc_client.get_node(nodeId)
			for idx in opc_gvl:
				var_name = idx.split(".")[-1]
				nodeId = nodeId_header + idx
				nodeIds[var_name] = opc_client.get_node(nodeId)
			#print(nodeIds['b_request'].get_value())
			
			print(nodeIds['b_opc_request'].get_value())
			http_status = False
			if nodeIds['b_opc_request'].get_value():
				if not http_status:
					#pro_type = randint(0, 2)
					pro_type += 1
					if pro_type == 3:
						pro_type = 0
					print("get request and product type: " + str(pro_type))
				
				#print("get request from opcua server and product type: " + str(pro_type))
				nodeIds['b_http'].set_value(http_status, ua.VariantType.Boolean)
				nodeIds['i_opc_type'].set_value(pro_type, ua.VariantType.Int16)
				nodeIds['b_opc_answer'].set_value(True, ua.VariantType.Boolean)
				b_opc_process = False
				while not b_opc_process:
					b_opc_process = nodeIds['b_opc_process'].get_value()
				nodeIds['b_opc_answer'].set_value(False, ua.VariantType.Boolean)
				print('     ...done')
			else:
				#print("get no request from opc ua server")
				time.sleep(1)
				nodeIds['b_opc_answer'].set_value(False, ua.VariantType.Boolean)

			opc_counter = nodeIds['i_opc_counter'].get_value()
			opc_client.disconnect()

if __name__=="__main__":
        main()
       	exit()
