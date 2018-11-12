from __future__ import print_function
import requests
import sys
import time
import json
from requests.exceptions import ConnectionError

def main():
	url = "http://129.187.88.30:4567/observedVariables"
	try:
		client = requests.get(url, timeout=10)
	except ConnectionError:
		print("failed ")
	else:
		if client.status_code == 200:
			print("connect successfully")
			print(client.json())
			jdata = client.json()
			with open('../log_file/log_json', 'w') as outfile:
				json.dump(jdata, outfile)
			ljdata = list(jdata)
			lljdata = list(ljdata)
			for idx in lljdata:
				for time in list(jdata[idx]):
					#print("Observervariables: " + idx)
					#print("last change time: " + time)
					#print("value: " + str(jdata[idx][time]))
					if jdata[idx][time] == False:
						del jdata[idx][time]
                        #with open('../log_file/log_json123', 'w') as outfile:
                                #json.dump(jdata, outfile)
			#print(jdata)

			jPusher1 = jdata['GVL.Pusher1']
			jPusher2 = jdata['GVL.Pusher2']
			jBase = jdata['GVL.Base_End_Sensor']
			ljPusher1 = list(jPusher1)
			ljPusher2 = list(jPusher2)
			ljBase = list(jBase)
			ljPusher1.sort()
			ljPusher2.sort()
			ljBase.sort()
			
			if len(ljPusher1) > 0:
				print(ljPusher1[-1])
			else:
				print("")
			#print(len(ljPusher1))
			#print(ljPusher1[-1])
			#print(ljPusher2[-1])
			#print(ljBase[-1])
			#print(type(ljPusher1[0]))
			lj = []
			#actually time 10/12/18 13:48:54.4030000 GMT
			t1 = unicode('10/12/18 13:48:54.4030000 GMT')
			t2 = unicode('11/12/18 13:48:54.4030000 GMT')
			t3 = unicode('10/15/18 13:48:54.4030000 GMT')
			t4 = unicode('10/12/19 13:48:54.4030000 GMT')
			t5 = unicode('10/12/18 14:48:54.4030000 GMT')
			t6 = unicode('10/12/18 13:58:54.4030000 GMT')
			t7 = unicode('10/12/18 13:48:54.6030000 GMT')
			t8 = unicode('10/12/18 13:48:54.6030000 FMT')
			lj.append(t1)
                        lj.append(t2)
                        lj.append(t3)
                        lj.append(t4)
                        lj.append(t5)
                        lj.append(t6)
                        lj.append(t7)
			lj.append(t8)
			for i in range(1, 8):
				if lj[0] > lj[i]:
					print('False')
					break
				else:
					#sys.stdout.flush()
					st = "True" + str(i)
					#sys.stdout.write('%s\r'% st)
					sys.stdout.flush()
					print(st, end=" ")
					#print('True'+str(i), end='\r', flush=True)
			print("")

if __name__=="__main__":
	main()
