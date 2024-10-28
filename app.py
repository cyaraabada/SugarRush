from flask import *

import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root",
	database="SUGAR_RUSH"
)
cursor = conexion.cursor()

app = Flask(__name__)

#página principal
@app.route('/')
def index():
  return render_template('index.html')


#menu menu
@app.route('/menu')
def menu():
  pass

#menu clientes
@app.route('/clientes')
def clientes():
  pass

#menu productos
@app.route('/productos')
def productos():
  query = "SELECT * FROM Producto"
  cursor.execute(query)
  productos = cursor.fetchall()
  return render_template('productos.html',productos=productos)

@app.route('/agregar_productos', methods=['POST'])
def agregar_productos():
  #Obtengo los datos del formulario
  descripcion = request.form.get('descripcion')
  precio = request.form.get('precio')

  #los agrego a la base de datos
  query = 'INSERT INTO Producto (descripcion, precio) VALUES (%s, %s)'
  cursor.execute(query, (descripcion,precio))
  conexion.commit()
  return redirect(url_for('productos'))

@app.route('/modificar_productos')
def modificar_productos():
  pass

@app.route('/eliminar_productos')
def eliminar_productos():
  pass

import mysql.connector
from datetime import date

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="usuario",
    password="contraseña",
    database="tienda"
)

cursor = conexion.cursor()

# Función para agregar un cliente
def alta_cliente(dni, nombre, apellido):
    query = "INSERT INTO Cliente (dni, nombre, apellido) VALUES (%s, %s, %s)"
    cursor.execute(query, (dni, nombre, apellido))
    conexion.commit()
    print("Cliente agregado con éxito")

# Función para listar clientes
def listar_clientes():
    query = "SELECT * FROM Cliente"
    cursor.execute(query)
    clientes = cursor.fetchall()
    if clientes:
        print("Listado de clientes:")
        for cliente in clientes:
            print(f"DNI: {cliente[0]}, Nombre: {cliente[1]}, Apellido: {cliente[2]}")
    else:
        print("No hay clientes en la base de datos")

# Función para agregar un producto
def alta_producto(nombre, precio):
    query = "INSERT INTO Producto (nombre, precio) VALUES (%s, %s)"
    cursor.execute(query, (nombre, precio))
    conexion.commit()
    print("Producto agregado con éxito")

# Función para listar productos
def listar_productos():
    query = "SELECT * FROM Producto"
    cursor.execute(query)
    productos = cursor.fetchall()
    if productos:
        print("Listado de productos:")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}")
    else:
        print("No hay productos en la base de datos")


#_____________________________________________________________________________________________________________________


# -------------------------- CLIENTES ----------------------------

# Listar clientes
@app.route('/clientes')
def listar_clientes():
    query = "SELECT * FROM Cliente"
    cursor.execute(query)
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=clientes)

# Agregar cliente
@app.route('/alta_cliente', methods=['POST'])
def alta_cliente():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    query = "INSERT INTO Cliente (dni, nombre, apellido) VALUES (%s, %s, %s)"
    cursor.execute(query, (dni, nombre, apellido))
    conexion.commit()
    return redirect(url_for('listar_clientes'))

# Editar cliente - mostrar el formulario con los datos actuales
@app.route('/editar_cliente/<int:dni>')
def editar_cliente(dni):
    query = "SELECT * FROM Cliente WHERE dni = %s"
    cursor.execute(query, (dni,))
    cliente = cursor.fetchone()
    return render_template('editar_cliente.html', cliente=cliente)

# Guardar cambios del cliente
@app.route('/modificar_cliente/<int:dni>', methods=['POST'])
def modificar_cliente(dni):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    query = "UPDATE Cliente SET nombre = %s, apellido = %s WHERE dni = %s"
    cursor.execute(query, (nombre, apellido, dni))
    conexion.commit()
    return redirect(url_for('listar_clientes'))

# Eliminar cliente
@app.route('/eliminar_cliente/<int:dni>')
def eliminar_cliente(dni):
    query = "DELETE FROM Cliente WHERE dni = %s"
    cursor.execute(query, (dni,))
    conexion.commit()
    return redirect(url_for('listar_clientes'))

# -------------------------- PRODUCTOS ----------------------------

# Listar productos
@app.route('/productos')
def listar_productos():
    query = "SELECT * FROM Producto"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

# Agregar producto
@app.route('/alta_producto', methods=['POST'])
def alta_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    query = "INSERT INTO Producto (nombre, precio) VALUES (%s, %s)"
    cursor.execute(query, (nombre, precio))
    conexion.commit()
    return redirect(url_for('listar_productos'))

# Editar producto
@app.route('/editar_producto/<int:id>')
def editar_producto(id):
    query = "SELECT * FROM Producto WHERE id = %s"
    cursor.execute(query, (id,))
    producto = cursor.fetchone()
    return render_template('editar_producto.html', producto=producto)

# Guardar cambios del producto
@app.route('/modificar_producto/<int:id>', methods=['POST'])
def modificar_producto(id):
    nombre = request.form['nombre']
    precio = request.form['precio']
    query = "UPDATE Producto SET nombre = %s, precio = %s WHERE id = %s"
    cursor.execute(query, (nombre, precio, id))
    conexion.commit()
    return redirect(url_for('listar_productos'))

# Eliminar producto
@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    query = "DELETE FROM Producto WHERE id = %s"
    cursor.execute(query, (id,))
    conexion.commit()
    return redirect(url_for('listar_productos'))

# -------------------------- PEDIDOS ----------------------------

# Listar pedidos
@app.route('/pedidos')
def listar_pedidos():
    query = "SELECT * FROM Pedido"
    cursor.execute(query)
    pedidos = cursor.fetchall()
    return render_template('pedidos.html', pedidos=pedidos)

# Agregar pedido
@app.route('/alta_pedido', methods=['POST'])
def alta_pedido():
    dni_cliente = request.form['dni_cliente']
    productos = request.form.getlist('productos')  # Lista de IDs de productos seleccionados
    cantidades = request.form.getlist('cantidades')  # Lista de cantidades
    productos_cantidades = {int(producto): int(cantidad) for producto, cantidad in zip(productos, cantidades)}

    total = 0
    for id_producto, cantidad in productos_cantidades.items():
        cursor.execute("SELECT precio FROM Producto WHERE id = %s", (id_producto,))
        precio = cursor.fetchone()[0]
        total += precio * cantidad
    
    query = "INSERT INTO Pedido (fecha, dni_cliente, total) VALUES (CURDATE(), %s, %s)"
    cursor.execute(query, (dni_cliente, total))
    id_pedido = cursor.lastrowid

    for id_producto, cantidad in productos_cantidades.items():
        cursor.execute("SELECT precio FROM Producto WHERE id = %s", (id_producto,))
        precio = cursor.fetchone()[0]
        subtotal = precio * cantidad
        query = "INSERT INTO DetallePedido (id_pedido, id_producto, cantidad, subtotal) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_pedido, id_producto, cantidad, subtotal))

    conexion.commit()
    return redirect(url_for('listar_pedidos'))

# Eliminar pedido
@app.route('/eliminar_pedido/<int:id>')
def eliminar_pedido(id):
    query = "DELETE FROM Pedido WHERE id = %s"
    cursor.execute(query, (id,))
    conexion.commit()
    return redirect(url_for('listar_pedidos'))

if __name__ == '__main__':
    app.run(debug=True)
# Cierre de la conexión
conexion.close()














if __name__ == '__main__':
  app.run(debug=True)