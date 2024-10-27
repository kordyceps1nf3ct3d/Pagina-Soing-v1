from flask import *
from flask import flash
import mysql.connector 
ip = "192.168.1.84" #Aqui se debe reemplazar por la ip local
user_p = 'root'
passw = 'Soing1214'

user_cbd = ''
pass_cbd = ''
app = Flask(__name__)
app.secret_key = "Z3J6eWIga29yZHljZXBz"
conn = mysql.connector.connect(
    host = ip,
    user = user_p,
    password = passw
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS data_base")
cursor.close()
conn.close()

conn = mysql.connector.connect(
    host = ip, 
    user = user_p,
    password = passw,
    database ='data_base'
)
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS producto (
               ID_PD INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
               NOMBRE_PD VARCHAR(255) NOT NULL,
               CANTIDAD INT NOT NULL,
               TIPO VARCHAR(255) NOT NULL,
               TIPO_EXTRA VARCHAR(255),
               TIPO_EXTRA2 INT
               )''')
cursor.execute('''
               CREATE TABLE IF NOT EXISTS Usuarios (
               ID_US INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
               NOMBRE_US VARCHAR(255) NOT NULL,
               CONTRASENA VARCHAR(255) NOT NULL
               )''')
cursor.execute('''
               CREATE TABLE IF NOT EXISTS CAMBIOS (
               ID_CB INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
               Nombre_Producto VARCHAR(255) NOT NULL,
               ID_US INT,
               ID_PD INT,
               N_TICKET INT NOT NULL,
               CANTIDAD_CB INT NOT NULL,
               FOREIGN KEY (ID_US) REFERENCES Usuarios(ID_US),
               FOREIGN KEY (ID_PD) REFERENCES producto(ID_PD)
               )''')
conn.commit()
cursor.close()
conn.close()


@app.route("/")
def inicio():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user_cbd = request.form['username']
    pass_cbd = request.form['passwd']

    try: 
        conn = mysql.connector.connect(
                host = ip, 
                user = user_p,
                password = passw,
                database ='data_base'
        )
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Usuarios WHERE NOMBRE_US = %s AND CONTRASENA = %s"
        cursor.execute(query,(user_cbd, pass_cbd))
        varuser = cursor.fetchone()
        cursor.close()
        conn.close()

        if varuser:
            session['username'] = user_cbd
            return redirect(url_for('Productos'))
        else:
            return render_template('index.html', error=True)    
    except mysql.connector.Error as err:
        return f"Error: {err}", 500
@app.route("/Productos")
def Productos():
    return render_template('Productos.html')







if __name__ == '__main__':
    app.run(host='192.168.1.84', port= 80, debug=True)
