import sqlite3
import socket
import threading
import _thread



conn_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('127.0.0.1', 8888)


def thread_tcp():
    conn_tcp.bind(server_addr)
    conn_tcp.listen(5)
    print('Waiting for connection...')

    while True:
        conn, addr = conn_tcp.accept()
        _thread.start_new_thread(thread_connection, (conn, addr))


def thread_connection(client_socket, client_addr):
    try:
        while True:
            data = client_socket.recv(2048)
            if not data:
                break
            else:
                # Тут логика на обработку инфы с клиента
                print(data)

            client_socket.sendall(str(data).encode())
    finally:
        client_socket.close()
        print('CLOSE! Address:', client_addr)


if __name__ == '__main__':
    t_server = threading.Thread(target=thread_tcp)
    t_server.start()
    t_server.join()
