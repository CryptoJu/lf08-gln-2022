from computer import Computer
import socket, sys                                                          
from datetime import datetime                                                 

class Server(Computer):                                                     

    _service = ''                                                           # These three lines are not needed but it fits better to the UML diagram...
    __sockIP = None                                                         # Preceding minus in UML Diagram: means private variable; __ in python                                                 
    __sockPort = None

    def __init__(self, cpu, cpuSpeed, ram, os, ip, service):
        super().__init__(cpu, cpuSpeed, ram, os, ip)                        # Call init method from parent class which contains everything we need except service
        self._service = service                                             # And add service; Preceding hashtag in UML Diagram: means protected variable; _ in python                                  

    def createSocket(self, sockIP, sockPort):

        try:
            server_socket = socket.socket()                                  # Create socket object
            self.__sockIP = str(sockIP); self.__sockPort = int(sockPort)     # Unneeded as you could just use the parameters directly in the next line but more accurate to the class diagram i guess                     
            server_socket.bind((self.__sockIP, self.__sockPort))             # Bind to IP and PORT given in parameter 
            self.__sock = server_socket                                      # Store server_socket in self.sock to make it available to following fuction without returning it
        except Exception as e:
            print(f'Error: {repr(e)}')
        

    def runningServer(self):
             
        try:
            server_socket = self.__sock                                     # Get server_socket back from self.sock
            server_socket.listen(2)                                         # Enable server to accept connections. Parameter specifies how many unaccepted connections server will allow before refusing new connections
            print('Server started...')
            conn, addr = server_socket.accept()                             # Accept incoming connection. Conn is the connection object and addr contains IP (addr[0]) and Port (addr[1])
            print(f"Client {str(addr[0])} has connected to the server over port {str(addr[1])}")
            clientmsg = 'Connection to server was successful.'
            conn.send(clientmsg.encode())                                   # Send connection succesful message to client

            while True:                                                     
                client_input = conn.recv(1024).decode()                     # Wait for incoming messages from client. Accept maximum 1024 bytes
                if client_input == 'shutdown':                              # If shutdown command is recognized
                    print("Receive remote-command: Server is shutting down")
                    conn.close()                                            # Close connection
                    sys.exit()                                              # Shutdown server (exit script)
                elif client_input == 'exit':                                # If exit command is recognized
                    print(f"Received Exit command from Client {str(addr[0])}. Restarting Listening for new Connections.")
                    conn.close()                                            # Close connection
                    self.runningServer()                                    # Start method anew (accept new connections)
                else:
                    if client_input:                                        # If no keyword is detected
                        print(f"{datetime.now().strftime('%H:%M:%S')} | {addr[0]} : {str(client_input)}")   # Print Timestamp (formatted to Hour:Minute:Second) | IP (addr[0]) and client message converted to string.
        except Exception as e:                                              # Again catching any errors that occur
            print(f'Error: {repr(e)}')                                      # And printing them


if __name__ == '__main__':
    server = Server('Generic CPU',292.3424, 420, 'Microsoft Windoof', '127.0.0.1', 'Socket Server') # Initialize with generic data
    server.getInfo()                                                        # get Actual hardware info
    print(f'\tService: {server._service}\n')
    server.createSocket('127.0.0.1',4444)                                   # Create socket on localhost on port 4444, if you want to accept connections from any device that can route to you, try ip 0.0.0.0
    server.runningServer()                                                  # Start listening for incoming connections
    
    

    