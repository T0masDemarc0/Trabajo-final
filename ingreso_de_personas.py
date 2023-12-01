import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import mysql.connector
#cd C:\Program Files\MySQL\MySQL Server 8.0\bin
class Persona:
    def __init__(self, nombre, apellido, edad, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.dni = dni

    def obtener_informacion(self):
        return f"Nombre: {self.nombre}\nApellido: {self.apellido}\nEdad: {self.edad}\nDni: {self.dni}"
   

class Ventana_Buscar_Editar_Eliminar(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscar Persona")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        mensaje_label = QLabel("Para buscar una persona, completa solo el DNI.")
        self.layout.addWidget(mensaje_label)

        self.label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        self.layout.addWidget(self.label_nombre)
        self.layout.addWidget(self.input_nombre)

        self.label_apellido = QLabel("Apellido:")
        self.input_apellido = QLineEdit()
        self.layout.addWidget(self.label_apellido)
        self.layout.addWidget(self.input_apellido)

        self.label_edad = QLabel("EDAD:")
        self.input_edad = QLineEdit()
        self.layout.addWidget(self.label_edad)
        self.layout.addWidget(self.input_edad)

        self.label_dni = QLabel("Dni:")
        self.input_dni = QLineEdit()
        self.layout.addWidget(self.label_dni)
        self.layout.addWidget(self.input_dni)

        self.buscar_button = QPushButton("Buscar Persona")
        self.buscar_button.clicked.connect(self.buscar_persona)
        self.layout.addWidget(self.buscar_button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.editar_button = QPushButton("Editar Información")
        self.editar_button.clicked.connect(self.editar_persona)
        self.layout.addWidget(self.editar_button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.eliminar_button = QPushButton("Eliminar Persona")
        self.eliminar_button.clicked.connect(self.eliminar_persona)
        self.layout.addWidget(self.eliminar_button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.crear_button = QPushButton("Crear Persona")
        self.crear_button.clicked.connect(self.crear_persona)
        self.layout.addWidget(self.crear_button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.volver_button = QPushButton("cerrar programa")
        self.volver_button.clicked.connect(self.close)
        self.layout.addWidget(self.volver_button)

        self.central_widget.setLayout(self.layout)

    def buscar_persona(self):
        dni_a_buscar = self.input_dni.text()

        conector_bd = mysql.connector.connect(
            host="localhost", user="root1", password="Soydeunion17", database="pyside6"
        )
        cursor = conector_bd.cursor()

        consulta = "select * from personas where dni = %s"
        valores = (dni_a_buscar,)
        cursor.execute(consulta, valores)
        resultado = cursor.fetchone()

        if resultado:
            edad = resultado[3]
            nombre = resultado[1]
            apellido = resultado[2]
            dni = resultado[4]
            self.result_label.setText(f"Edad: {edad}\nNombre: {nombre}\nApellido: {apellido}\nDni: {dni}")
        else:
            self.result_label.setText("Persona no encontrada.")

        cursor.close()
        conector_bd.close()

    def editar_persona(self):
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        dni = self.input_dni.text()
        try:
            edad = int(self.input_edad.text())
        except ValueError:
            self.result_label.setText("La edad debe ser un número entero.")
            return

        conector_bd = mysql.connector.connect(
            host="localhost", user="root1", password="Soydeunion17", database="pyside6"
        )
        cursor = conector_bd.cursor()

        consulta_obtener_persona = "SELECT * FROM personas WHERE dni = %s"
        cursor.execute(consulta_obtener_persona, (dni,))
        resultado = cursor.fetchone()

        if resultado:
            consulta_actualizar_persona = "UPDATE personas SET nombre = %s, apellido = %s, edad = %s WHERE dni = %s"
            valores = (nombre, apellido, edad, dni)
            cursor.execute(consulta_actualizar_persona, valores)
            conector_bd.commit()
            self.result_label.setText("Persona editada correctamente.")
        else:
            self.result_label.setText("Persona no encontrada.")

        cursor.close()
        conector_bd.close()

    def eliminar_persona(self):
        dni_a_eliminar = self.input_dni.text()

        conector_bd = mysql.connector.connect(
            host="localhost", user="root1", password="Soydeunion17", database="pyside6"
        )
        cursor = conector_bd.cursor()

        consulta = "DELETE FROM personas WHERE dni = %s"
        valores = (dni_a_eliminar,)
        cursor.execute(consulta, valores)
        conector_bd.commit()

        cursor.close()
        conector_bd.close()

        self.result_label.setText(f"Persona con dni {dni_a_eliminar} eliminada.")
    
    def crear_persona(self):
        conector_bd = mysql.connector.connect(
        host = "localhost", user="root1", password="Soydeunion17", database="pyside6"
        )
        cursor = conector_bd.cursor()
        crear_la_tabla = """
        CREATE TABLE IF NOT EXISTS personas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(250) NOT NULL,
            edad INT,
            dni VARCHAR(50) NOT NULL
        )
        """       
        cursor.execute(crear_la_tabla)
        conector_bd.commit()
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        dni = self.input_dni.text()
        try:
            edad = int(self.input_edad.text())
            persona = Persona(nombre, apellido, edad, dni)
            informacion = persona.obtener_informacion()
            self.result_label.setText(informacion)
            consulta = "INSERT INTO personas (nombre, apellido, edad, dni) VALUES (%s, %s, %s, %s)"
            valores = (nombre, apellido, edad, dni)
            cursor.execute(consulta, valores)
            conector_bd.commit()
        except ValueError:
            self.result_label.setText("La edad/dni debe ser un número entero.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana_Buscar_Editar_Eliminar()
    ventana.show()
    sys.exit(app.exec_())

