import requests
import time
from requests.exceptions import ConnectionError

def main():
	while True:
		init_status = True
		tc = 0
		pro_type = None
		dt = 0
		sdt = 0
		maxdt = 0
		mc = 0
		if init_status:
			url = "http://129.187.88.30:4567/observedVariables"
			client = requests.get(url)
		while tc < 500:
			t0 = time.time()
			jdata = client.json()
			jP1 = jdata['GVL.Pusher1']
			jP2 = jdata['GVL.Pusher2']
			lP1 = list(jP1)[0]
			lP2 = list(jP2)[0]
			if lP1 < 0:
				pro_type = 0
			if lP2 < 0:
				pro_type = 1
			dt = time.time() -t0
			if maxdt < dt:
				maxdt = dt
				mc = tc + 1
			sdt += dt
			tc += 1
		print(tc)
		print(maxdt, mc)
		print(sdt / 500)

if __name__=='__main__':
	main()


