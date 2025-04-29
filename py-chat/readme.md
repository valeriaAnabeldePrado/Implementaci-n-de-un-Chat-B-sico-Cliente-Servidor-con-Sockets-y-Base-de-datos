# Chat Básico Cliente-Servidor con Sockets y Base de Datos

Un sistema simple de chat que implementa un servidor y un cliente utilizando sockets TCP/IP y almacena los mensajes en una base de datos SQLite.

## Características

- Servidor que escucha en localhost:5000
- Cliente con interfaz de usuario de consola mejorada
- Almacenamiento de mensajes en base de datos SQLite
- Soporte para múltiples clientes simultáneos (multithreading)
- Visualizador de mensajes almacenados

## Estructura del Proyecto

El proyecto está compuesto por tres archivos principales:

1. `server.py`: Implementación del servidor de chat
2. `client.py`: Cliente de chat con interfaz de consola
3. `view_messages.py`: Visualizador de mensajes almacenados

## Requisitos

- Python 3.6 o superior
- Módulos estándar de Python:
  - socket
  - sqlite3
  - threading
  - datetime
  - os
  - sys

## Cómo usar

### 1. Iniciar el servidor

Primero, inicia el servidor para que pueda recibir conexiones:

```bash
python server.py
```

El servidor se iniciará en localhost:5000 y estará listo para aceptar conexiones.

### 2. Ejecutar el cliente

En una nueva terminal, inicia el cliente:

```bash
python client.py
```

El cliente se conectará automáticamente al servidor y mostrará un menú interactivo.

### 3. Visualizar mensajes almacenados

Para ver los mensajes almacenados en la base de datos:

```bash
python view_messages.py
```


