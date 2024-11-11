import csv
import tkinter as tk
from tkinter import messagebox

class Inventario:
    def __init__(self, archivo):
        self.archivo = archivo
        self.productos = self.cargar_productos()

    def cargar_productos(self):
        productos = []
        try:
            with open(self.archivo, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    productos.append(row)
        except FileNotFoundError:
            pass
        return productos

    def guardar_productos(self):
        with open(self.archivo, mode='w', newline='') as file:
            fieldnames = ['ID', 'Nombre', 'Cantidad', 'Precio']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for producto in self.productos:
                writer.writerow(producto)

    def agregar_producto(self, id, nombre, cantidad, precio):
        producto = {'ID': id, 'Nombre': nombre, 'Cantidad': cantidad, 'Precio': precio}
        self.productos.append(producto)
        self.guardar_productos()

    def buscar_producto(self, id):
        for producto in self.productos:
            if producto['ID'] == id:
                return producto
        return None

    def eliminar_producto(self, id):
        producto = self.buscar_producto(id)
        if producto:
            self.productos.remove(producto)
            self.guardar_productos()
            return True
        return False

    def actualizar_producto(self, id, nombre=None, cantidad=None, precio=None):
        producto = self.buscar_producto(id)
        if producto:
            if nombre:
                producto['Nombre'] = nombre
            if cantidad:
                producto['Cantidad'] = cantidad
            if precio:
                producto['Precio'] = precio
            self.guardar_productos()
            return True
        return False


class App:
    def __init__(self, root, inventario):
        self.inventario = inventario
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("400x400")

        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text="Menú de Inventario", font=("Helvetica", 16)).pack(pady=10)

        # Botones para cada acción
        tk.Button(self.root, text="Agregar producto", command=self.agregar_producto).pack(fill="x", padx=20, pady=5)
        tk.Button(self.root, text="Buscar producto", command=self.buscar_producto).pack(fill="x", padx=20, pady=5)
        tk.Button(self.root, text="Eliminar producto", command=self.eliminar_producto).pack(fill="x", padx=20, pady=5)
        tk.Button(self.root, text="Actualizar producto", command=self.actualizar_producto).pack(fill="x", padx=20,
                                                                                                pady=5)
        tk.Button(self.root, text="Ver todos los productos", command=self.ver_productos).pack(fill="x", padx=20, pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(fill="x", padx=20, pady=5)

    def agregar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto")

        tk.Label(ventana, text="ID").grid(row=0, column=0)
        id_entry = tk.Entry(ventana)
        id_entry.grid(row=0, column=1)

        tk.Label(ventana, text="Nombre").grid(row=1, column=0)
        nombre_entry = tk.Entry(ventana)
        nombre_entry.grid(row=1, column=1)

        tk.Label(ventana, text="Cantidad").grid(row=2, column=0)
        cantidad_entry = tk.Entry(ventana)
        cantidad_entry.grid(row=2, column=1)

        tk.Label(ventana, text="Precio").grid(row=3, column=0)
        precio_entry = tk.Entry(ventana)
        precio_entry.grid(row=3, column=1)

        def guardar():
            self.inventario.agregar_producto(id_entry.get(), nombre_entry.get(), cantidad_entry.get(),
                                             precio_entry.get())
            messagebox.showinfo("Producto agregado", "Producto agregado exitosamente")
            ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar).grid(row=4, columnspan=2, pady=10)

    def buscar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Buscar Producto")

        tk.Label(ventana, text="ID").grid(row=0, column=0)
        id_entry = tk.Entry(ventana)
        id_entry.grid(row=0, column=1)

        def buscar():
            producto = self.inventario.buscar_producto(id_entry.get())
            if producto:
                resultado = f"ID: {producto['ID']}\nNombre: {producto['Nombre']}\nCantidad: {producto['Cantidad']}\nPrecio: {producto['Precio']}"
            else:
                resultado = "Producto no encontrado."
            messagebox.showinfo("Resultado de Búsqueda", resultado)

        tk.Button(ventana, text="Buscar", command=buscar).grid(row=1, columnspan=2, pady=10)

    def eliminar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Eliminar Producto")

        tk.Label(ventana, text="ID").grid(row=0, column=0)
        id_entry = tk.Entry(ventana)
        id_entry.grid(row=0, column=1)

        def eliminar():
            if self.inventario.eliminar_producto(id_entry.get()):
                messagebox.showinfo("Eliminar Producto", "Producto eliminado exitosamente")
            else:
                messagebox.showwarning("Eliminar Producto", "Producto no encontrado")
            ventana.destroy()

        tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=1, columnspan=2, pady=10)

    def actualizar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Producto")

        tk.Label(ventana, text="ID").grid(row=0, column=0)
        id_entry = tk.Entry(ventana)
        id_entry.grid(row=0, column=1)

        tk.Label(ventana, text="Nuevo Nombre").grid(row=1, column=0)
        nombre_entry = tk.Entry(ventana)
        nombre_entry.grid(row=1, column=1)

        tk.Label(ventana, text="Nueva Cantidad").grid(row=2, column=0)
        cantidad_entry = tk.Entry(ventana)
        cantidad_entry.grid(row=2, column=1)

        tk.Label(ventana, text="Nuevo Precio").grid(row=3, column=0)
        precio_entry = tk.Entry(ventana)
        precio_entry.grid(row=3, column=1)

        def actualizar():
            if self.inventario.actualizar_producto(id_entry.get(), nombre_entry.get(), cantidad_entry.get(),
                                                   precio_entry.get()):
                messagebox.showinfo("Actualizar Producto", "Producto actualizado exitosamente")
            else:
                messagebox.showwarning("Actualizar Producto", "Producto no encontrado")
            ventana.destroy()

        tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=4, columnspan=2, pady=10)

    def ver_productos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Productos")

        for idx, producto in enumerate(self.inventario.productos, start=1):
            info = f"{idx}. ID: {producto['ID']}, Nombre: {producto['Nombre']}, Cantidad: {producto['Cantidad']}, Precio: {producto['Precio']}"
            tk.Label(ventana, text=info).pack()


if __name__ == "__main__":
    root = tk.Tk()
    inventario = Inventario("productos.csv")
    app = App(root, inventario)
    root.mainloop()