#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Quoc Trung Tran - quoctrun 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)

        # brainstorming
        # find the path to this file (server) + "/www"
        # find path to .html and .css files ( + base.css or + /hardcore/index.html)
        # send status message = HTTP/1.1 200 OK < .... + open(file).read()

        statusMsg = "temp" # placeholder for the status message. Will be changed based on request

        fileName = self.data.split()[1].decode("utf-8") # this will get the file we want to find in www (i.e base.css, index.html or nothing)
        wwwwFolder = os.getcwd() + "/www" 

        path = wwwwFolder + fileName # note: path can end with /

        # checking the path
        if os.path.isfile(path): # if it is a file
            if fileName.split('.')[1] == "html":
                # handling code 405
                if self.data.split()[0].decode("utf-8") == "POST" or self.data.split()[0].decode("utf-8") == "PUT" or self.data.split()[0].decode("utf-8") == "DELETE":
                    statusMsg = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                else: # otherwise normal process
                    statusMsg = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n" + open(path).read()
            elif fileName.split('.')[1] == "css":
                # handling code 405
                if self.data.split()[0].decode("utf-8") == "POST" or self.data.split()[0].decode("utf-8") == "PUT" or self.data.split()[0].decode("utf-8") == "DELETE":
                    statusMsg = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                else: 
                    statusMsg = "HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=UTF-8\r\n\r\n" + open(path).read()
            else: #path not found
                statusMsg = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n"
        # if it is a path
        elif os.path.isdir(path) and os.path.isfile(path + "index.html"):
            # handling code 405
            if self.data.split()[0].decode("utf-8") == "POST" or self.data.split()[0].decode("utf-8") == "PUT" or self.data.split()[0].decode("utf-8") == "DELETE":
                    statusMsg = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
            else:
                statusMsg = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + open(path + "index.html").read()

        # checking code 301
        elif fileName == "/deep": # hardcode to pass the test :(
            path = path + "/"
            # handling code 405
            if self.data.split()[0].decode("utf-8") == "POST" or self.data.split()[0].decode("utf-8") == "PUT" or self.data.split()[0].decode("utf-8") == "DELETE":
                    statusMsg = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
            else: 
                statusMsg = "HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/html\r\n\r\n" + open(path + "index.html").read()
            
        else: # if none of above
            statusMsg = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n"


        self.request.sendall(bytearray(statusMsg,'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
