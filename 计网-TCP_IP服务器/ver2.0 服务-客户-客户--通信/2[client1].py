import socket
import threading
from cryClient import *
from colorama import init, Fore

cookie = b'Suzuka'  # 不是真正意义的cookie，xixi

# 颜色
init(autoreset=True)
color_red = Fore.LIGHTRED_EX
color_yellow = Fore.LIGHTYELLOW_EX
def start_client():
    # 创建TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    # 连接到服务器
    ip = 'localhost'  # 可以修改为实际的服务器IP
    port = 9910
    server_address = (ip, port)
    print(f"正在请求连接 {server_address}")
    client_socket.connect(server_address)
    client_socket.sendall(cookie)

    # 启动发送和接收线程
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

    # 等待两个线程结束
    send_thread.join()
    receive_thread.join()

    client_socket.close()
    print("All of clients,over")

def send_messages(client_socket):
    """发送消息给服务器"""
    try:
        while True:
            message = (color_red+cookie.decode()+':'+input()).encode()
            encrypted_message = encrypt(message)
            client_socket.sendall(encrypted_message)

            if message == b'exit':
                break
    except Exception as e:
        print(f"发送错误: {e}")
    finally:
        print("发送,over")

def receive_messages(client_socket):
    """接收来自服务器的消息"""
    try:
        while True:
            data = client_socket.recv(1024)

            if data:
                decrypted_message = decrypt(data).decode()
                print(f'{decrypted_message}')
            else:
                print("服务器已关闭连接。")
                break
    except Exception as e:
        print(f"接收,失败: {e}")
    finally:
        print("接收,over")

if __name__ == "__main__":
    start_client()
