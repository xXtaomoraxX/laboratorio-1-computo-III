#comenzamos a importar las librerias principales para manejar nuestro sistema bancario de forma segura
import sqlite3 #SQlite se encarga de almacenar la informacion en una base de datos
import bcrypt #sera nuestro encriptador para mantener la seguridad en nuestro sistema
import sys #aqui empezaremos a importar los atributos para nuestra interfaz grafica en el programa para
#mostrar en pantalla la interfaz para que el usuario interactue con ella
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from datetime import datetime#es una biblioteca para manejar el tiempo y fechas, para mantener en constante
#vigilancia las transacciones y cambios hechos en la base de datos 

# Función para insertar un nuevo usuario
def insertar_usuario(nombre, contrasena, saldo):
    # Conexión a la base de datos
    conn = sqlite3.connect('banco.db')#necesitaremos crear una base de datos primero
    c = conn.cursor()
    
    # Hash de la contraseña
    hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
    
    # Inserción del usuario
    c.execute('''INSERT INTO usuarios (nombre, contrasena, saldo) 
                 VALUES (?, ?, ?)''', (nombre, hashed_contrasena, saldo))#importaremos los valores
    
    conn.commit()
    conn.close()




#crearemos el encriptado para nuestra contraseña, para que los datos esten asegurados
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

#empezamos a desarrollar nuestra interfaz grafica que se mostrara en pantalla, con la cual los clientes 
#interactuaran para realizar sus transacciones

#declaramos la clase
class BancoApp(QWidget):
    def __init__(self): #inicializaremos la clase junto a sus atributos
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sistema Bancario')#se imprimira en pantalla junto a la ventana
        self.setGeometry(100, 100, 280, 170)#las dimensiones de la ventana en pantalla
        
        layout = QVBoxLayout()

        self.registro_button = QPushButton('Registrarse')#comenzamos a crear el boton de registrarse
        self.registro_button.clicked.connect(self.open_registro_window)#metodo para conectar el boton
        layout.addWidget(self.registro_button)

        self.login_button = QPushButton('Iniciar Sesión')#creamos el boton para iniciar sesion
        self.login_button.clicked.connect(self.open_login_window)#metodo para conectar el boton
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def open_registro_window(self):#ventana que aparecera luego de dar clic en registrar
        self.registro_window = RegistroWindow()#en esta interfaz se registraran los clientes
        self.registro_window.show()
        self.close()

    def open_login_window(self):#ventana que aparece para iniciar sesion en el login
        self.login_window = LoginWindow()#aca iniciaran sesion los clientes introduciendo sus credenciales
        self.login_window.show()
        self.close()
#declaramos la clase para registrar
class RegistroWindow(QWidget):
    def __init__(self):#inicializamos la clase con sus atributos
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Registro de Usuario')#mensaje que aparecera en la ventana de registro
        self.setGeometry(100, 100, 280, 220)#dimensiones que tendra la ventana
        
        layout = QVBoxLayout()

        self.nombre_label = QLabel('Nombre:')#creamos la casilla para introducir el nombre
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)

        self.contrasena_label = QLabel('Contraseña:')#casilla para crear la contraseña
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.Password)#recordemos que no se debe mostrar
        layout.addWidget(self.contrasena_label)
        layout.addWidget(self.contrasena_input)

        self.saldo_label = QLabel('Saldo Inicial:')#casilla para introducir el monto a guardar
        self.saldo_input = QLineEdit()
        layout.addWidget(self.saldo_label)
        layout.addWidget(self.saldo_input)

        self.registrar_button = QPushButton('Registrar')#este boton registrara los datos una vez el cliente
        #los haya introducido todos
        self.registrar_button.clicked.connect(self.registrar)#metodo para conectar el boton
        layout.addWidget(self.registrar_button)

        self.setLayout(layout)

    def registrar(self):#aca definiremos el tipo de datos a guardoar
        nombre = self.nombre_input.text()
        contrasena = self.contrasena_input.text()
        saldo = float(self.saldo_input.text())#recordemos que el dinero es un numero de valor decimal
        #en muchas ocasiones

        # Conexión a la base de datos
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()
        
        # Hash de la contraseña
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        
        # Inserción del usuario
        c.execute('''INSERT INTO usuarios (nombre, contrasena, saldo) 
                     VALUES (?, ?, ?)''', (nombre, hashed_contrasena, saldo))
        
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Registro', 'Usuario registrado con éxito!')#mensaje que aparecera en pantalla
        #que indicara que se guardo con exito el registro
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
#creamos la clase para el login
class LoginWindow(QWidget):
    def __init__(self):#inciializamos la clase con sus atributos
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Iniciar Sesión')#mensaje que aparece en pantalla en el login
        self.setGeometry(100, 100, 280, 170)#dimensiones que tendra la ventana
        
        layout = QVBoxLayout()

        self.nombre_label = QLabel('Nombre:')#casilla para introducir el nombre
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)

        self.contrasena_label = QLabel('Contraseña:')#casilla para introducir la contraseña
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.contrasena_label)
        layout.addWidget(self.contrasena_input)

        self.login_button = QPushButton('Iniciar Sesión')#creamos un boton para iniciar sesion
        #luego de que el usuario introduzca por completo las credenciales
        self.login_button.clicked.connect(self.login)#metodo para conectar el boton
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):#definimos el tipo de dato a intorducir
        nombre = self.nombre_input.text()
        contrasena = self.contrasena_input.text()
        
        # Conexión a la base de datos
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()
        
        # Buscar el usuario en la base de datos
        c.execute('SELECT contrasena FROM usuarios WHERE nombre = ?', (nombre,))
        result = c.fetchone()
        #crearemos un bucle el cual verificara si las credenciales son correctas
        if result and bcrypt.checkpw(contrasena.encode('utf-8'), result[0]):
            QMessageBox.information(self, 'Login', f'Bienvenido, {nombre}!')
            self.open_transaccion_window()
        else:#caso contrario dira esto si son incorrectas las credenciales introducidas
            QMessageBox.warning(self, 'Login', 'Nombre o contraseña incorrectos')
        
        conn.close()

    def open_transaccion_window(self):#definimos la interfaz de transacciones
        self.transaccion_window = TransaccionWindow()
        self.transaccion_window.show()
        self.close()
#creamos la clase para transacciones
class TransaccionWindow(QWidget):
    def __init__(self):#inicializamos la clase con sus atributos
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Realizar Transacción')#mensaje que aparecera en pantalla en la interfaz
        self.setGeometry(100, 100, 280, 170)#dimensiones de la ventana de transacciones
        
        layout = QVBoxLayout()

        self.monto_label = QLabel('Monto:')#creamos una casilla para introducir el monto a enviar
        #segun el monto guardado por el cliente
        self.monto_input = QLineEdit()
        layout.addWidget(self.monto_label)
        layout.addWidget(self.monto_input)

        self.transaccion_button = QPushButton('Realizar Transacción')#creamos un boton para enviar
        #la transaccion una vez el cliente introduzca el monto
        self.transaccion_button.clicked.connect(self.realizar_transaccion)#metodo para conectar el boton
        layout.addWidget(self.transaccion_button)

        self.setLayout(layout)

    def realizar_transaccion(self):
        monto = float(self.monto_input.text())
        # Aquí iría la lógica para realizar la transacción
        QMessageBox.information(self, 'Transacción', f'Transacción de {monto} realizada con éxito!')
#mantendra activa las interfacez hasta que decidamos cerrarlas
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BancoApp()
    ex.show()
    sys.exit(app.exec_())



# Ejemplo de uso de datetime
now = datetime.now()
print(f'Fecha y hora actual: {now}')
