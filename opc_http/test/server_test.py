from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class Server_handler(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('content_type', 'text/json')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
                data = {u'GVL.Pusher2': {u'10/24/18 08:04:40.3800000 GMT': False, u'10/24/18 19:45:33.0760000 GMT': False}, u'GVL.Pusher1': {u'10/24/18 09:45:33.0760000 GMT': False, u'10/24/18 10:45:33.0760000 GMT': False}}
                parsed = json.dumps(data)
                print(parsed)
                self.wfile.write(parsed)		

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		data = "{u'foo': u'bar', u'baz': u'far'}"
		parsed = json.dumps(data)
		print(parsed)
		self.wfile.write(parsed)
		self._set_headers()

def run(server_class=HTTPServer, handler_class=Server_handler, port=1234):
	server_address = ("127.0.0.1", port)
	httpd = server_class(server_address, handler_class)
	print('starting httpd...')
	httpd.serve_forever()


if __name__=="__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()

