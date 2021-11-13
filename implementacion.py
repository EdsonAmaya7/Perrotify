from perrotify import *
opcion = Usuario()
print()
ans=True
while ans:
    print('----Menu----'.center(100,"="))
    print("""\n
                                          ---Opciones---
1.- Canciones Top
2.- Aristas Top

--- Consutas de la BD ---

3.- Seleccionar Usuario
4.- Seleccionar Canciones
5.- Ordenar por Genero
6.- --- Exit ---
""")
    ans=input("Ingresa la opcion que deseas: ")
    if ans=="1":
      print("\n---Canciones Top---")

    elif ans=="2":
      print("\n---Artistas Top---")

    elif ans=="3":
      print("\n---Seleccionar Usuario---")
      opcion.get_usuario()

    elif ans=="4":
      print("\n---Seleccionar Canciones---")
      opcion.get_songs()

    elif ans=="5":
      print("\n---Ordenar por Genero---")

    elif ans=="6":
      print("\n Adios!!!")
      ans = None
    else:
       print("\n Opcion no valida reintente otro valor")