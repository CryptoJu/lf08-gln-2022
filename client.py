from computer import Computer
import socket

class Client(Computer):                                                         

    __remoteIP = None
    __remotePort: None

    def create_socket(self, remoteIP, remotePort):
        try:
            client_socket = socket.socket()                                     # Create socket object
            self.__remoteIP = remoteIP; self.__remotePort = remotePort          # Unneeded, as you could use the parameter directly, but more accurate to class diagramm i guess       
            client_socket.connect((self.__remoteIP,self.__remotePort))          # Connect to server socket
            print(f'{client_socket.recv(1024).decode()}')                       # Waits until received max. 1024 bytes from socket and decodes bytes. In this case connection successful mesage.
            
            self.__sock = client_socket                                         # Make client_socket available to other functions in the class by setting it to variable self.sock
        except Exception as e:                                                  # Any Exceptions that occur will get stored in variable e
            print(f'Error: {repr(e)}')                                          # repr() represents the error as string and print() prints the error.
        
    def sendData(self, string=None): # string = None sets the parameter
        client_socket = self.__sock                                             # Getting client socket back from self.sock

        if string == None:                                                      # If no string is given in sendData()
            while True:
                string = input('Enter message: ')                               # Ask for message
                if client_socket != None:                                       # Check if socket exists
                    if string == 'exit':                                        # Check for exit keyword
                        print('Exiting connection')
                        client_socket.send(string.encode())                     # Sends exit command to server. Commands get executed on serverside
                        break                                                   # Break to exit Loop so it won't ask for input again, because connection is closed now.
                    elif string == 'shutdown':                                  # Check for shutdown keyword
                        print('Send remote-command: Server is shutting down')
                        client_socket.send(string.encode())                     # Sends shutdown command to server. Commands get executed on serverside
                        client_socket.close()                                   # Closes client socket too, not really needed i guess
                        break                                                   # Break to exit Loop so it won't ask for input again, because connection is closed now.
                    else:
                        client_socket.send(string.encode())                     # if no keyword is detected, just send message encoded as bytes (only bytes can be sent and must be encoded on client side and decoded on server side)
        elif string != None:                                                    # If a string is given to sendData() instead
             if client_socket != None:                                          # Basically from here all the same except for loop asking for input
                if string == 'exit':                                            
                    print('Exiting connection')
                    client_socket.send(string.encode())
                if string == 'shutdown':
                    print('Send remote-command: Server is shutting down')
                    client_socket.send(string.encode())
                    client_socket.close() 
                else:
                    client_socket.send(string.encode())
                    client_socket.close()

if __name__ == '__main__':
    client = Client('Generic CPU',23.2482483,420,'Generic OS','127.0.0.1')          # generic information that get's overwritten
    client.getInfo()
    print('\n')                                                                     # Not needed but prettier
    client.create_socket('127.0.0.1',4444)                                          # try to connect to socket on localhost port 4444
    client.sendData()                                                               # Can be either used with a String given to send a message once or without parameters to ask for input in a loop (keep connection open)
    

