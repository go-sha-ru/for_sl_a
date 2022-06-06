import socket
from message import Message


def main():
    sock = socket.socket()
    sock.bind(('', 8888))
    sock.listen(1)
    conn, address = sock.accept()
    msg = Message()

    print('connected:', address)
    is_connected = False

    while True:
        data = conn.recv(1024)
        print(data)
        if not data:
            break
        if is_connected:
            replay = msg(data)
        else:
            replay = 'Hello'
            is_connected = True

        if isinstance(replay, bool or bytes):
            conn.send(replay)
        else:
            conn.send(replay.encode())

    conn.close()


if __name__ == '__main__':
    main()
