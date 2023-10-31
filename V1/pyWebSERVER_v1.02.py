import http.server
import socketserver
import socket
import os
from netifaces import interfaces, ifaddresses, AF_INET
import time
from art import *

hostname = socket.gethostname()
fqdn = socket.getfqdn()
ip_address = socket.gethostbyname(hostname)
cwd = str(os.getcwd())

print('v 1.02')
print(text2art("pyWebSERVER"))
print('Current Working Directory: ' + cwd)
print('------------------------------------------------------------------')

print(f"Your FQDN: {fqdn}")
print('------------------------------------------------------------------')
print('Your IP Address:')
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    print(' '.join(addresses))
print('------------------------------------------------------------------')



IP = input('Choose IP (default = localhost): ')
if not IP:
    IP = 'localhost'

print('---> %s' % IP)

PORT = input('Choose PORT (default = 8080): ')
if not PORT:
    PORT = 8080

print('---> %s' % PORT)
print('------------------------------------------------------------------')
print('EXIT / CLOSE with [Ctrl + C]')
print('------------------------------------------------------------------')
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((IP, int(PORT)), Handler) as httpd:
    print(time.asctime(), "--- Server UP at http://%s:%s" % (IP, PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "--- Server DOWN at http://%s:%s" % (IP, PORT))
