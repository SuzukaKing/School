import socket  
from cryClient import *

cookie = b'Suzuka' # 不是真正意义的cookie，xixi
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


    try:  
        while True:  
            # 从标准输入读取数据  
            message =input("请输入要发送的消息: ").encode()  
            encrypted_message = encrypt(message)
            # 发送数据  
            client_socket.sendall(encrypted_message)  
              
            # 等待服务器回射数据  
            data = client_socket.recv(1024)  
            print(f"服务器回射: {decrypt(data).decode()}") 

            if message == b'exit':
                break 
            if not data:  # 检查是否收到空数据，可能是服务器已关闭连接  
                print("服务器已关闭连接。")  
                break  

    except Exception as e:  
        print(f"发生错误: {e}")  
    finally:  
        # 确保关闭连接  
        client_socket.close()  
        print("客户端已关闭连接。")  
  
if __name__ == "__main__":  
    start_client()