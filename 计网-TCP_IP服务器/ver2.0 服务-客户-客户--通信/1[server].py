import socket
import threading
from cryServer import *

def start_server():
    # 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定
    ip = 'nianis.cn'
    port = 9910
    server_add = (ip, port)
    server_socket.bind(server_add)

    # 监听，至多两个客户端连接
    server_socket.listen(2)
    print("服务器已启动，等待连接...")

    connection1 = None
    connection2 = None

    cookies = {
        "conn1": "",
        "conn2": ""
    }  # 保存用户信息，但这不是真正的cookie，xixi

    while True:
        # 等待客户端连接
        connection, client_add = server_socket.accept()
        cookie = connection.recv(1024).decode()
        print(f"连接来自 {client_add}, 身份验证: {cookie}")

        if connection1 is None:
            connection1 = connection
            cookies['conn1'] = cookie
            print(f"{cookies['conn1']} 已连接")
            connection1.sendall(b"single-player mode (waiting for second player)")
            continue  # 等待第二个连接

        if connection2 is None:
            connection2 = connection
            cookies['conn2'] = cookie
            print(f"{cookies['conn2']} 已连接")

            # 发送提示信息
            double = f"welcome {cookies['conn1']} and {cookies['conn2']}"
            print(double)
            connection1.sendall(double.encode())
            connection2.sendall(double.encode())


            # 开始处理两个客户端的双向通信
            thread1 = threading.Thread(target=check, args=(connection1, connection2, cookies, "conn1", "conn2"))
            thread2 = threading.Thread(target=check, args=(connection2, connection1, cookies, "conn2", "conn1"))

            # 启动两个线程
            thread1.start()
            thread2.start()

        else:
            connection.sendall(b"who are you?")
            connection.close()

def check(self_client, other_client, cookies, self_key,other_key):

    """处理单个客户端的消息收发"""
    try:
        while True:
            data = self_client.recv(1024)
            if data:
                decrypted_data = decrypt(data)
                if not decrypted_data:
                    print(f"没有接收到{cookies[self_key]}数据，关闭连接")
                    break
                if decrypted_data == b'exit':
                    print(f"{cookies[self_key]} 关闭连接")
                    self_client.sendall(b'byebye')
                    break
                print(f"{decrypted_data.decode()}")

                # 转发数据给另一个客户端
                other_client.sendall(encrypt(decrypted_data))
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭连接
        self_client.close()

if __name__ == "__main__":
    start_server()
