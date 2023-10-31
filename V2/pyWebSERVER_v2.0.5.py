from http.server import SimpleHTTPRequestHandler, test
import http.server
from functools import partial
import socketserver
import socket
import os
import base64
from netifaces import interfaces, ifaddresses, AF_INET
import time
from art import text2art
import colorama
from colorama import Fore, Style

# ///////////////////////////////////////////////////////////////////////////////////////
# Developer: Tobias Haueter
# Use Case: Web testing and file share solution
# ------------
# Changelog:
# 2.0.0: added authentication option and cli redesign
# 2.0.1: optimized UI/UX in cli, added timestamps whene server started
# 2.0.2: Bugfix text color with RESET
# 2.0.3: Error handling server functions
# 2.0.4: changed msg color
# 2.0.5: Capital letter input bugfix
# ------------
# Reference:
# https://github.com/tobias-haueter/pyWebSERVER
# https://www.pythonpool.com/python-http-server/
# ///////////////////////////////////////////////////////////////////////////////////////

# Resize Windows CMD Windows ------------------------------------------------------------
os.system('mode con: cols=90 lines=50')  # cols=wide / lines=height


# Class definition ----------------------------------------------------------------------
class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Main class to present webpages and authentication."""

    def __init__(self, *args, **kwargs):
        username = kwargs.pop("username")
        password = kwargs.pop("password")
        directory = kwargs.pop("directory")
        self._auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        super().__init__(*args, **kwargs)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Present frontpage with user authentication."""
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(b"no auth header received")
        elif self.headers.get("Authorization") == "Basic " + self._auth:
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get("Authorization").encode())
            self.wfile.write(b"not authenticated")


# Functions -----------------------------------------------------------------------------
def base_server(IP, PORT):
    try:
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer((IP, int(PORT)), Handler) as httpd:
            print(f"Serving HTTP on {IP} port {PORT} (http://{IP}:{PORT}/) ...")
            httpd.serve_forever()

    except Exception as e:
        print(Fore.LIGHTRED_EX + '-- ERROR -- ')
        print(e)
        input('press [enter] to exit...')


def auth_server(IP, PORT, USER, PWD):
    try:
        import argparse
        parser = argparse.ArgumentParser()
        handler_class = partial(
            AuthHTTPRequestHandler,
            username=USER,
            password=PWD,
            directory=os.getcwd(),
        )
        test(HandlerClass=handler_class, port=PORT, bind=IP)

    except Exception as e:
        print(Fore.LIGHTRED_EX + '-- ERROR -- ')
        print(e)
        input('press [enter] to exit...')


# START ---------------------------------------------------------------------------------
if __name__ == "__main__":

    # APP Specs -------------------------------------------------------------------------
    cli_length = 88
    version = 'v2.0.5'

    # Init
    colorama.init(autoreset=True)

    # find network sockets, name, ip and current directory ------------------------------
    hostname = socket.gethostname()
    fqdn = socket.getfqdn()
    ip_address = socket.gethostbyname(hostname)
    cwd = str(os.getcwd())

    # CLI PRINT
    print('─' * cli_length)
    print(Fore.LIGHTRED_EX + ' pyWebSERVER' + ' ' + f'[{version}]' + '\n')
    print(' * Web testing and file share solution.')
    print('─' * cli_length)
    print(Fore.CYAN + text2art("pyWebSERVER"))
    print(Fore.CYAN + ' 2023 by Tobias Haueter')
    print('─' * cli_length)
    print(Fore.YELLOW + ' Your Current Working Directory:')
    print(f' {cwd}')
    print('')
    print(Fore.YELLOW + f" Your FQDN (Full Qualified Domain Name):")
    print(f' {fqdn}')
    print('─' * cli_length)

    print(Fore.YELLOW + ' Your IP Address:')
    i = 0
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        addr = ''.join(addresses)
        print(f' {addr}')
    print('─' * cli_length)

    print(Fore.YELLOW + ' SERVER SETUP:')
    IP = input(Fore.CYAN + ' IP Address (default = localhost): ')
    if not IP:
        IP = '127.0.0.1'

    print(Fore.RESET + ' >> %s' % IP)

    PORT = input(Fore.CYAN + ' PORT Number (default = 8080):')
    if not PORT:
        PORT = 8080

    print(Fore.RESET + ' >> %s' % PORT)

    print('')
    AUTH = input(Fore.YELLOW + ' SERVER AUTHENTICATION (recommended)? [y/n]: ')
    if AUTH.lower() == 'y':
        USER = input(Fore.GREEN + ' USERNAME (default = user): ')
        if not USER:
            USER = 'user'
        print(Fore.RESET + ' >> %s' % USER)

        PWD = input(Fore.GREEN + ' PASSWORD (default = pyserver): ')
        if not PWD:
            PWD = 'pyserver'
        print(Fore.RESET + ' >> %s' % PWD)

        print(Fore.LIGHTGREEN_EX + '─' * cli_length)
        input(Fore.LIGHTGREEN_EX + ' >> authentication set --> press [enter] to START...')
        print(Fore.LIGHTGREEN_EX + '─' * cli_length)
        print('')
        print(Fore.YELLOW + ' Server started at ' + time.asctime())
        auth_server(IP, PORT, USER, PWD)

    if AUTH.lower() == 'n':
        print(Fore.LIGHTRED_EX + '─' * cli_length)
        input(Fore.LIGHTRED_EX + ' >> no authentication set --> press [enter] to START...')
        print(Fore.LIGHTRED_EX + '─' * cli_length)
        print('')
        print(Fore.YELLOW + ' Server started at ' + time.asctime())
        base_server(IP, PORT)

    else:
        exit()
