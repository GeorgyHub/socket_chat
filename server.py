import socket
import threading
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# config = dotenv_values(".env")
clients = {}

def mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Включение безопасности TLS
    server.login(LOGIN, PASSWORD)

def handle_client(client_socket):
    try:
        # первое сообщение — имя
        name = client_socket.recv(1024).decode()
        clients[client_socket] = name
        print(f"{name} подключился")

        broadcast(f"🔔 {name} вошел в чат!", client_socket)

        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            text = message.decode()
            print(f"{name}: {text}")
            broadcast(f"{name}: {text}", client_socket)
    except:
        pass
    finally:
        if client_socket in clients:
            name = clients[client_socket]
            print(f"{name} отключился")
            broadcast(f"❌ {name} покинул чат", client_socket)
            del clients[client_socket]
        client_socket.close()


def broadcast(message, sender_socket=None):
    """Рассылка сообщения всем, кроме отправителя"""
    for client in clients.keys():
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                del clients[client]


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()
    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()


if __name__ == "__main__":
    start_server()