import sys
sys.path.insert(0, "./module")

from client_opc_ua import opc_ua_client
<<<<<<< HEAD
=======
from opcua import ua
>>>>>>> 8ff01c3e76c5bef8fc6fa8bc950344d6edf2e2a8

def opcua_exit():
	opc_url = "opc.tcp://localhost:4840"
	opc_client = opc_ua_client(opc_url)
<<<<<<< HEAD

	opc_status = opc_client.connect('opcua', False)
	if opc_status:
		opcId = ['Application.PLC_PRG.fb_opc_get.b_opc_answer',]
		opc_client.set_value('b_opc_answer', False, ua.VariantType.Boolean)

if __name__ == '__main__':
	opcua_exit()
	exit()
=======
	opc_status = opc_client.connect('opcua', False)
	
	if opc_status:
		opcId = ['Application.PLC_PRG.fb_opc_get.b_opc_answer',]
		opcnodeId = opc_client.get_nodes(opcId)
		opc_client.set_value('b_opc_answer', False, ua.VariantType.Boolean)
		opc_client.disconnect()
		print("Program exit")

if __name__ =='__main__':
	opcua_exit()
	exit()
>>>>>>> 8ff01c3e76c5bef8fc6fa8bc950344d6edf2e2a8
