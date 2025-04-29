import socket
import sqlite3
import threading
from datetime import datetime
import sys
import os

# Clase para manejar la base de datos del chat con sus configuraciones
class ChatDatabase:
    def __init__(self, db_path='chat_messages.db'):
        try:
            db_exists = os.path.exists(db_path)
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.connection.cursor()
            if not db_exists:
                self.create_tables()
                print("Base de datos creada correctamente")
            else:
                print("Conexión a base de datos existente establecida")
                
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            sys.exit(1)
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        self.connection.commit()
    
    def save_message(self, contenido, ip_cliente):
        try:
            fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO messages (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                (contenido, fecha_envio, ip_cliente)
            )
            self.connection.commit()
            return fecha_envio
        except sqlite3.Error as e:
            print(f"Error al guardar mensaje: {e}")
            return None
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión a la base de datos cerrada")

# Clase para manejar el servidor de chat
class ChatServer: 
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.database = ChatDatabase()
        self.clients = [] 
    
    def initialize_socket(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            
            print(f"Servidor de chat iniciado en {self.host}:{self.port}")
            return True
        except OSError as e:
            print(f"Error al inicializar el socket: {e}")
            return False
    
    def handle_client(self, client_socket, client_address):
        ip_cliente = client_address[0]
        print(f"Cliente conectado desde {ip_cliente}")
        
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"Mensaje recibido de {ip_cliente}: {data}")
                timestamp = self.database.save_message(data, ip_cliente)
                response = f"Mensaje recibido: {timestamp}"
                client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error en la comunicación con el cliente {ip_cliente}: {e}")
        finally:
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            print(f"Cliente {ip_cliente} desconectado")
    
    def start(self):
        if not self.initialize_socket():
            return
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario")
        except Exception as e:
            print(f"Error en el servidor: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        if self.server_socket:
            self.server_socket.close()
            print("Socket del servidor cerrado")
        self.database.close()
        print("Servidor detenido correctamente")


# Punto de entrada para ejecutar el servidor
if __name__ == "__main__":
    server = ChatServer()
    server.start()