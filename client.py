import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            break


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8000))

    # ввод имени
    name_user = input("Введите свое имя: ")
    client_socket.send(name_user.encode())

    # поток для получения сообщений
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    try:
        while True:
            message = input(">")
            if message.lower() in ("exit", "выход", "quit"):
                break
            client_socket.send(message.encode())
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()