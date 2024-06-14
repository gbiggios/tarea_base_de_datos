import pedidos
import os

with open('contador.txt', 'r') as file:
    x = int(file.read())

print(x)