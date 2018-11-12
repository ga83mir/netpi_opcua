import requests

def run():
	url = "http://127.0.0.1:1234"
	client = requests.get(url)
	
	while True:
		client.json()
		if client.status_code == 200:
			pro_type = input("please input the production type: ")
			requests.post(url, str(pro_type))

if __name__=="__main__":
	run()
