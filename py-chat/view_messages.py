import sqlite3
import sys
import os
from datetime import datetime

class MessageViewer:
    #Visualizador de mensajes almacenados en la base de datos
    def __init__(self, db_path='chat_messages.db'):
        self.db_path = db_path
        self.connection = None
    
    def connect_to_database(self):
        try:
            if not os.path.exists(self.db_path):
                print(f"La base de datos {self.db_path} no existe.")
                return False
            self.connection = sqlite3.connect(self.db_path)
            print(f"Conexión establecida con {self.db_path}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")
    
    def display_all_messages(self):
        if not self.connection:
            print("No hay conexión con la base de datos")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, contenido, fecha_envio, ip_cliente FROM messages ORDER BY fecha_envio")
            messages = cursor.fetchall()
            
            if not messages:
                print("No hay mensajes almacenados en la base de datos")
                return
            
            print("\n" + "=" * 80)
            print(" " * 25 + "MENSAJES ALMACENADOS")
            print("=" * 80)
            print(f"{'ID':<5} | {'FECHA':<19} | {'IP CLIENTE':<15} | CONTENIDO")
            print("-" * 80)
            
            for msg_id, contenido, fecha, ip in messages:
                print(f"{msg_id:<5} | {fecha:<19} | {ip:<15} | {contenido}")
            
            print("-" * 80)
            print(f"Total de mensajes: {len(messages)}")
            
        except sqlite3.Error as e:
            print(f"Error al recuperar mensajes: {e}")
    
    def display_messages_by_ip(self, ip):
        if not self.connection:
            print("No hay conexión con la base de datos")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT id, contenido, fecha_envio FROM messages WHERE ip_cliente = ? ORDER BY fecha_envio",
                (ip,)
            )
            messages = cursor.fetchall()
            
            if not messages:
                print(f"No hay mensajes de la IP {ip}")
                return
            
            print(f"\nMensajes del cliente {ip}:")
            print("-" * 60)
            
            for msg_id, contenido, fecha in messages:
                print(f"{msg_id:<5} | {fecha:<19} | {contenido}")
            
            print("-" * 60)
            print(f"Total de mensajes: {len(messages)}")
            
        except sqlite3.Error as e:
            print(f"Error al recuperar mensajes: {e}")
    
    def run(self):
        if not self.connect_to_database():
            return
        
        try:
            while True:
                print("\n" + "=" * 30)
                print("  VISUALIZADOR DE MENSAJES  ")
                print("=" * 30)
                print("1. Ver todos los mensajes")
                print("2. Ver mensajes por IP")
                print("3. Salir")
                
                choice = input("\nSelecciona una opción (1-3): ")
                
                if choice == '1':
                    self.display_all_messages()
                elif choice == '2':
                    ip = input("Introduce la IP del cliente: ")
                    self.display_messages_by_ip(ip)
                elif choice == '3':
                    print("Cerrando visualizador...")
                    break
                else:
                    print("Opción no válida. Intenta de nuevo.")
                
                input("\nPresiona Enter para continuar...")
                self.clear_screen()
                
        except KeyboardInterrupt:
            print("\nVisualizador detenido por el usuario")
        finally:
            self.close_connection()
    
    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


# Punto de entrada para ejecutar el visualizador
if __name__ == "__main__":
    viewer = MessageViewer()
    viewer.run()