# Archivo menu.py

import pymongo
from functions import Restaurante

def mostrar_menu():
    print("----- Menú del Restaurante -----")
    print("1. Insertar un nuevo pedido")
    print("2. Buscar pedidos por nombre de cliente")
    print("3. Buscar pedidos por total")
    print("4. Eliminar pedidos por nombre de cliente")
    print("5. Insertar varias órdenes")
    print("6. Modificar el total de un pedido")
    print("7. Marcar todos los pedidos como entregados")
    print("8. Borrar la base de datos completa")
    print("9. Mostrar todos los pedidos")
    print("-------------------------------")

def main():
    restaurante = Restaurante()
    sw = True

    while sw:
        mostrar_menu()
        opcion = input('Ingrese su opción: ')

        if opcion == '1':
            restaurante.insertar_pedido()
        elif opcion == '2':
            nombre_cliente = input('Ingrese el nombre del cliente: ')
            restaurante.pedido_cliente(nombre_cliente)
        elif opcion == '3':
            total_ = int(input('Ingrese el total del pedido: '))
            restaurante.pedido_total(total_)
        elif opcion == '4':
            nombre_cliente = input('Ingrese el nombre del cliente: ')
            restaurante.del_many_byclient(nombre_cliente)
        elif opcion == '5':
            num_ordenes_a_ingresar = int(input("Ingrese el número de órdenes que desea agregar: "))
            restaurante.insertar_varias_ordenes(num_ordenes_a_ingresar)
        elif opcion == '6':
            pedido_id = int(input('Ingrese la ID del pedido a modificar: '))
            restaurante.look_by_id(pedido_id)
            nuevo_total = int(input('Ingrese el nuevo valor total: '))
            restaurante.actualizar_total_por_id(pedido_id, nuevo_total)
        elif opcion == '7':
            restaurante.agregar_entregado_a_todos()
        elif opcion == '8':
            restaurante.borrar_base_de_datos()
        elif opcion == '9':
            restaurante.find_all()

        user_ans = int(input('¿Desea realizar otra opción? Si=1 No=0: '))
        if user_ans == 0:
            sw = False
            print('Gracias por su preferencia')

if __name__ == "__main__":
    main()
