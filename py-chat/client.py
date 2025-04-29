import socket
import sys
import os

# clase Cliente para el servidor de chat
class ChatClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Conectado al servidor en {self.host}:{self.port}")
            return True
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor")
            return False
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            return False
    
    def send_message(self, message):
        if not self.connected:
            print("No estás conectado al servidor.")
            return None
        
        try:
            self.socket.send(message.encode('utf-8'))
            response = self.socket.recv(1024).decode('utf-8')
            return response
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            self.connected = False
            return None
    
    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.connected = False
            print("Desconectado del servidor")
    
    def run(self):
        if not self.connect():
            return
        self.show_welcome_message()
        
        try:
            while True:
                choice = self.show_menu() 
                if choice == '1':
                    self.send_message_interaction()
                elif choice == '2':
                    self.show_connection_info()
                elif choice == '3':
                    print("Cerrando cliente de chat...")
                    break
                else:
                    print("Opción no válida. Intenta de nuevo.")
                input("\nPresiona Enter para continuar...")
                self.clear_screen()
                
        except KeyboardInterrupt:
            print("\nCliente detenido por el usuario")
        finally:
            self.disconnect()
    
    def send_message_interaction(self):
        print("\n=== ENVIAR MENSAJE ===")
        print("Escribe 'éxito' para volver al menú principal")
        
        while True:
            message = input("\nTú: ")  
            if message.lower() == 'éxito':
                print("Volviendo al menú principal...")
                break     
            if not message.strip():
                print("El mensaje no puede estar vacío")
                continue 
            response = self.send_message(message)
            if response:
                print(f"Servidor: {response}")
            else:
                print("No se recibió respuesta del servidor")
                break
    
    def show_connection_info(self):
        print("\n=== INFORMACIÓN DE CONEXIÓN ===")
        print(f"Servidor: {self.host}:{self.port}")
        print(f"Estado: {'Conectado' if self.connected else 'Desconectado'}")
    
    def show_welcome_message(self):
        self.clear_screen()
        print("=" * 50)
        print("         CLIENTE DE CHAT SIMPLE          ")
        print("=" * 50)
        print("\nBienvenido al cliente de chat!")
        print("Este cliente te permite enviar mensajes a un servidor.")
    
    def show_menu(self):
        print("\n" + "=" * 30)
        print("      MENÚ PRINCIPAL      ")
        print("=" * 30)
        print("1. Enviar un mensaje")
        print("2. Información de conexión")
        print("3. Salir")
        
        return input("\nSelecciona una opción (1-3): ")
    
    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


# Punto de entrada para ejecutar el cliente
if __name__ == "__main__":
    client = ChatClient()
    client.run()