import requests
import time
from requests.exceptions import ConnectionError

def main():
		while True:
		t0 = time.time()
		url = "http://129.187.88.40:4567/observedVariables"
		try:
			client = requests.get(url)
		except ConnectionError:
			ft = time.time() - t0
			print(ft)
		else:
			st = time.time() - t0
			print(st)


if __name__ =="__main__":
	main()
