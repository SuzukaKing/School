import socket
from cryServer import *


def start_server():
    # 创建TCP/IP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定套接字到主机和端口
    ip  = 'localhost'
    port  = 9910
    server_address = (ip, port)
    server_socket.bind(server_address)
    
    # 监听连接
    server_socket.listen(2)
    print("服务器已启动，等待连接...")
    
    while True:
        # 等待客户端连接
        connection, client_address = server_socket.accept()
        try:
            cookie = connection.recv(1024)
            print(f"连接来自 {client_address},身份验证:{cookie.decode()}")
            while True:
                # 接收数据
                data = connection.recv(1024)
                decrypted_data = data
                if not data:
                    print("没有接收到数据，关闭连接")
                    break
                if decrypted_data == b'exit' :
                    print(f"{cookie.decode()}关闭连接")
                    connection.sendall(b'byebye')
                    break

                print(decrypted_data)
                
                # 将数据回射给客户端
                connection.sendall(encrypt(decrypted_data))
        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            # 关闭连接
            connection.close()

start_server()

if __name__ == "__main__":
    start_server()
