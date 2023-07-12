import tkinter as tk
from tkinter import messagebox
import json

class Producto:
    def __init__(self, nombre, stock, precio):
        self.nombre = nombre
        self.stock = stock
        self.precio = precio

class ComercioApp:
    def __init__(self, root):
        self.root = root
        self.productos = []
        self.root.title("Gestión de Comercio")

        # Crear widgets de la primera interfaz
        self.label_nombre = tk.Label(root, text="Nombre:")
        self.label_stock = tk.Label(root, text="Stock:")
        self.label_precio = tk.Label(root, text="Precio:")
        self.entry_nombre = tk.Entry(root)
        self.entry_stock = tk.Entry(root)
        self.entry_precio = tk.Entry(root)
        self.button_agregar = tk.Button(root, text="Agregar", command=self.agregar_producto)
        self.button_modificar = tk.Button(root, text="Modificar", command=self.modificar_producto)
        self.button_borrar = tk.Button(root, text="Borrar", command=self.borrar_producto)
        self.button_buscar = tk.Button(root, text="Buscar", command=self.buscar_producto)
        self.listbox_productos = tk.Listbox(root)
        self.listbox_productos.bind('<<ListboxSelect>>', self.mostrar_detalles)

        # Posicionar widgets de la primera interfaz en la ventana principal
        self.label_nombre.grid(row=0, column=0)
        self.label_stock.grid(row=1, column=0)
        self.label_precio.grid(row=2, column=0)
        self.entry_nombre.grid(row=0, column=1)
        self.entry_stock.grid(row=1, column=1)
        self.entry_precio.grid(row=2, column=1)
        self.button_agregar.grid(row=3, column=0)
        self.button_modificar.grid(row=3, column=1)
        self.button_borrar.grid(row=3, column=2)
        self.button_buscar.grid(row=4, column=0)
        self.listbox_productos.grid(row=5, column=0, columnspan=3)

        # Crear widgets de la segunda interfaz
        self.label_buscar = tk.Label(root, text="Buscar producto:")
        self.entry_buscar = tk.Entry(root)
        self.button_buscar_2 = tk.Button(root, text="Buscar", command=self.buscar_producto_2)
        self.listbox_productos_2 = tk.Listbox(root)

        # Posicionar widgets de la segunda interfaz en la ventana principal
        self.label_buscar.grid(row=6, column=0, sticky="w")
        self.entry_buscar.grid(row=6, column=1)
        self.button_buscar_2.grid(row=7, column=0)
        self.listbox_productos_2.grid(row=8, column=0, columnspan=2)

        # Cargar productos guardados
        self.cargar_productos_guardados()

        # Guardar productos al cerrar el programa
        root.protocol("WM_DELETE_WINDOW", self.guardar_productos)

    def agregar_producto(self):
        nombre = self.entry_nombre.get()
        stock = int(self.entry_stock.get())
        precio = float(self.entry_precio.get())

        producto = Producto(nombre, stock, precio)
        self.productos.append(producto)
        self.actualizar_listbox()
        self.actualizar_listbox_2()

        self.entry_nombre.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def modificar_producto(self):
        seleccionado = self.listbox_productos.curselection()
        if seleccionado:
            index = seleccionado[0]
            producto = self.productos[index]
            producto.nombre = self.entry_nombre.get()
            producto.stock = int(self.entry_stock.get())
            producto.precio = float(self.entry_precio.get())
            self.actualizar_listbox()
            self.actualizar_listbox_2()
            self.mostrar_detalles(None)

    def borrar_producto(self):
        seleccionado = self.listbox_productos.curselection()
        if seleccionado:
            index = seleccionado[0]
            del self.productos[index]
            self.actualizar_listbox()
            self.actualizar_listbox_2()

    def buscar_producto(self):
        nombre_buscado = self.entry_nombre.get()
        for producto in self.productos:
            if producto.nombre.lower() == nombre_buscado.lower():
                messagebox.showinfo("Producto Encontrado", f"El producto {producto.nombre} está disponible.")
                return
        messagebox.showinfo("Producto No Encontrado", f"No se encontró el producto {nombre_buscado}.")

    def buscar_producto_2(self):
        nombre_buscado = self.entry_buscar.get()
        self.listbox_productos_2.delete(0, tk.END)
        for producto in self.productos:
            if producto.nombre.lower().startswith(nombre_buscado.lower()):
                self.listbox_productos_2.insert(tk.END, f"{producto.nombre} - ${producto.precio}")

    def mostrar_detalles(self, event):
        seleccionado = self.listbox_productos.curselection()
        if seleccionado:
            index = seleccionado[0]
            producto = self.productos[index]
            self.entry_nombre.delete(0, tk.END)
            self.entry_stock.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
            self.entry_nombre.insert(tk.END, producto.nombre)
            self.entry_stock.insert(tk.END, producto.stock)
            self.entry_precio.insert(tk.END, producto.precio)

    def actualizar_listbox(self):
        self.listbox_productos.delete(0, tk.END)
        productos_ordenados = sorted(self.productos, key=lambda p: p.nombre)
        for producto in productos_ordenados:
            self.listbox_productos.insert(tk.END, producto.nombre)

    def actualizar_listbox_2(self):
        self.listbox_productos_2.delete(0, tk.END)
        productos_ordenados = sorted(self.productos, key=lambda p: p.nombre)
        for producto in productos_ordenados:
            self.listbox_productos_2.insert(tk.END, f"{producto.nombre} - ${producto.precio}")

    def cargar_productos_guardados(self):
        try:
            with open("productos.json", "r") as file:
                data = json.load(file)
                for item in data:
                    producto = Producto(item["nombre"], item["stock"], item["precio"])
                    self.productos.append(producto)
                self.actualizar_listbox()
                self.actualizar_listbox_2()
        except FileNotFoundError:
            messagebox.showinfo("Archivo no encontrado", "No se encontró el archivo 'productos.json'.")

    def guardar_productos(self):
        data = []
        for producto in self.productos:
            item = {
                "nombre": producto.nombre,
                "stock": producto.stock,
                "precio": producto.precio
            }
            data.append(item)
        with open("productos.json", "w") as file:
            json.dump(data, file)
        self.root.destroy()

# Iniciar la aplicación
root = tk.Tk()
app = ComercioApp(root)
root.mainloop()