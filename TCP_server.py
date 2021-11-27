import socket, select
import sys

from discord import client

MAX_DEVICES = 10
WELCOME_MESS = "Hello everyone"

def tcp_server_func(shared_list, connection_list):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.bind(("localhost", 10000))
            s.listen(MAX_DEVICES)
            inputs = [s]
            # Main loop #
            while(1):
                infds, outfds, errfds = select.select(inputs, inputs, [], MAX_DEVICES)
                if len(infds) != 0:
                    for fds in infds:
                        if fds is s:
                            conn, addr = fds.accept()
                            inputs.append(conn)
                            conn.sendall(WELCOME_MESS.encode())
                            connection_list.append(conn)
                        else:
                            data = fds.recv(1024)    
                            cli_sock = inputs[inputs.index(fds)]
                            cli_addr = cli_sock.getpeername()
                            
                            if data:
                                print(data)
                                if str(data).find("exit") > 0:
                                    print("Client disconnected")
                                    connection_list.pop(0)
                                    cli_sock.close()
                                    inputs.remove(cli_sock)
                            if not data:
                                inputs.remove(fds)

