import csv
import os
from typing import List, Optional

class Contacto:
    """Clase que representa un contacto con nombre, email y teléfono."""
    
    def __init__(self, nombre: str, email: str, telefono: str):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
    
    def __str__(self):
        return f"{self.nombre} - {self.email} - {self.telefono}"
    
    def to_dict(self):
        """Convierte el contacto a un diccionario para CSV."""
        return {
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un contacto desde un diccionario de CSV."""
        return cls(data['nombre'], data['email'], data['telefono'])


class GestorContactos:
    """Clase principal para gestionar los contactos."""
    
    def __init__(self, archivo_csv: str = 'contactos.csv'):
        self.archivo_csv = archivo_csv
        self.contactos: List[Contacto] = []
        self.cargar_contactos()
    
    def cargar_contactos(self):
        """Carga los contactos desde el archivo CSV."""
        if os.path.exists(self.archivo_csv):
            try:
                with open(self.archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
                    reader = csv.DictReader(archivo)
                    self.contactos = [Contacto.from_dict(fila) for fila in reader]
                print(f"Se cargaron {len(self.contactos)} contactos desde {self.archivo_csv}")
            except Exception as e:
                print(f"Error al cargar contactos: {e}")
                self.contactos = []
        else:
            print(f"Archivo {self.archivo_csv} no encontrado. Se creará uno nuevo.")
            self.contactos = []
    
    def guardar_contactos(self):
        """Guarda todos los contactos en el archivo CSV."""
        try:
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
                if self.contactos:
                    fieldnames = ['nombre', 'email', 'telefono']
                    writer = csv.DictWriter(archivo, fieldnames=fieldnames)
                    writer.writeheader()
                    for contacto in self.contactos:
                        writer.writerow(contacto.to_dict())
                print(f"Contactos guardados exitosamente en {self.archivo_csv}")
        except Exception as e:
            print(f"Error al guardar contactos: {e}")
    
    def agregar_contacto(self, nombre: str, email: str, telefono: str):
        """Agrega un nuevo contacto."""
        # Verificar si ya existe un contacto con el mismo nombre
        if self.buscar_contacto_por_nombre(nombre):
            print(f"Ya existe un contacto con el nombre '{nombre}'")
            return False
        
        nuevo_contacto = Contacto(nombre, email, telefono)
        self.contactos.append(nuevo_contacto)
        self.guardar_contactos()
        print(f"Contacto '{nombre}' agregado exitosamente")
        return True
    
    def listar_contactos(self):
        """Lista todos los contactos."""
        if not self.contactos:
            print("No hay contactos registrados")
            return
        
        print("\n" + "="*60)
        print("LISTA DE CONTACTOS")
        print("="*60)
        for i, contacto in enumerate(self.contactos, 1):
            print(f"{i}. {contacto}")
        print("="*60)
    
    def buscar_contacto_por_nombre(self, nombre: str) -> Optional[Contacto]:
        """Busca un contacto por nombre."""
        for contacto in self.contactos:
            if contacto.nombre.lower() == nombre.lower():
                return contacto
        return None
    
    def editar_contacto(self, nombre: str, nuevo_email: str = None, nuevo_telefono: str = None):
        """Edita un contacto existente."""
        contacto = self.buscar_contacto_por_nombre(nombre)
        if not contacto:
            print(f"No se encontró el contacto '{nombre}'")
            return False
        
        if nuevo_email:
            contacto.email = nuevo_email
        if nuevo_telefono:
            contacto.telefono = nuevo_telefono
        
        self.guardar_contactos()
        print(f"Contacto '{nombre}' editado exitosamente")
        return True
    
    def eliminar_contacto(self, nombre: str):
        """Elimina un contacto por nombre."""
        contacto = self.buscar_contacto_por_nombre(nombre)
        if not contacto:
            print(f"No se encontró el contacto '{nombre}'")
            return False
        
        self.contactos.remove(contacto)
        self.guardar_contactos()
        print(f"Contacto '{nombre}' eliminado exitosamente")
        return True


class AplicacionContactos:
    """Clase principal de la aplicación de consola."""
    
    def __init__(self):
        self.gestor = GestorContactos()
    
    def mostrar_menu(self):
        """Muestra el menú principal."""
        print("\n" + "="*50)
        print("    GESTIÓN DE CONTACTOS")
        print("="*50)
        print("1. Agregar contacto")
        print("2. Listar contactos")
        print("3. Editar contacto")
        print("4. Eliminar contacto")
        print("5. Buscar contacto")
        print("6. Salir")
        print("="*50)
    
    def validar_email(self, email: str) -> bool:
        """Validación básica de email."""
        return "@" in email and "." in email.split("@")[1]
    
    def validar_telefono(self, telefono: str) -> bool:
        """Validación básica de teléfono."""
        return telefono.replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit()
    
    def obtener_datos_contacto(self):
        """Obtiene los datos de un nuevo contacto con validación."""
        while True:
            nombre = input("Ingrese el nombre: ").strip()
            if nombre:
                break
            print("El nombre no puede estar vacío")
        
        while True:
            email = input("Ingrese el email: ").strip()
            if email and self.validar_email(email):
                break
            print("Ingrese un email válido")
        
        while True:
            telefono = input("Ingrese el teléfono: ").strip()
            if telefono and self.validar_telefono(telefono):
                break
            print("Ingrese un teléfono válido (solo números, espacios, guiones y paréntesis)")
        
        return nombre, email, telefono
    
    def agregar_contacto_interfaz(self):
        """Interfaz para agregar un contacto."""
        print("\n--- AGREGAR CONTACTO ---")
        nombre, email, telefono = self.obtener_datos_contacto()
        self.gestor.agregar_contacto(nombre, email, telefono)
    
    def editar_contacto_interfaz(self):
        """Interfaz para editar un contacto."""
        print("\n--- EDITAR CONTACTO ---")
        nombre = input("Ingrese el nombre del contacto a editar: ").strip()
        
        contacto = self.gestor.buscar_contacto_por_nombre(nombre)
        if not contacto:
            print(f"No se encontró el contacto '{nombre}'")
            return
        
        print(f"Contacto actual: {contacto}")
        
        nuevo_email = input(f"Nuevo email (actual: {contacto.email}) [Enter para mantener]: ").strip()
        nuevo_telefono = input(f"Nuevo teléfono (actual: {contacto.telefono}) [Enter para mantener]: ").strip()
        
        # Validar nuevos datos si se proporcionaron
        if nuevo_email and not self.validar_email(nuevo_email):
            print("Email inválido. No se realizaron cambios.")
            return
        
        if nuevo_telefono and not self.validar_telefono(nuevo_telefono):
            print("Teléfono inválido. No se realizaron cambios.")
            return
        
        # Solo pasar los valores que no están vacíos
        self.gestor.editar_contacto(
            nombre, 
            nuevo_email if nuevo_email else None,
            nuevo_telefono if nuevo_telefono else None
        )
    
    def eliminar_contacto_interfaz(self):
        """Interfaz para eliminar un contacto."""
        print("\n--- ELIMINAR CONTACTO ---")
        nombre = input("Ingrese el nombre del contacto a eliminar: ").strip()
        
        contacto = self.gestor.buscar_contacto_por_nombre(nombre)
        if not contacto:
            print(f"No se encontró el contacto '{nombre}'")
            return
        
        print(f"Contacto a eliminar: {contacto}")
        confirmacion = input("¿Está seguro? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            self.gestor.eliminar_contacto(nombre)
        else:
            print("Eliminación cancelada")
    
    def buscar_contacto_interfaz(self):
        """Interfaz para buscar un contacto."""
        print("\n--- BUSCAR CONTACTO ---")
        nombre = input("Ingrese el nombre del contacto a buscar: ").strip()
        
        contacto = self.gestor.buscar_contacto_por_nombre(nombre)
        if contacto:
            print(f"Contacto encontrado: {contacto}")
        else:
            print(f"No se encontró el contacto '{nombre}'")
    
    def ejecutar(self):
        """Ejecuta la aplicación principal."""
        print("¡Bienvenido a la Gestión de Contactos!")
        
        while True:
            self.mostrar_menu()
            
            try:
                opcion = input("Seleccione una opción (1-6): ").strip()
                
                if opcion == '1':
                    self.agregar_contacto_interfaz()
                elif opcion == '2':
                    self.gestor.listar_contactos()
                elif opcion == '3':
                    self.editar_contacto_interfaz()
                elif opcion == '4':
                    self.eliminar_contacto_interfaz()
                elif opcion == '5':
                    self.buscar_contacto_interfaz()
                elif opcion == '6':
                    print("¡Gracias por usar la Gestión de Contactos!")
                    break
                else:
                    print("Opción inválida. Por favor seleccione una opción del 1 al 6.")
                
                # Pausa para que el usuario pueda leer el resultado
                input("\nPresione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n¡Gracias por usar la Gestión de Contactos!")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")


# Función para crear contactos de ejemplo
def crear_contactos_ejemplo():
    """Crea algunos contactos de ejemplo para probar la aplicación."""
    gestor = GestorContactos()
    
    # Solo crear contactos si no existen ya
    if len(gestor.contactos) == 0:
        contactos_ejemplo = [
            ("Juan Pérez", "juan.perez@email.com", "+57 311 234 5678"),
            ("María García", "maria.garcia@email.com", "+57 320 987 6543"),
            ("Carlos López", "carlos.lopez@email.com", "+57 315 456 7890"),
            ("Ana Martínez", "ana.martinez@email.com", "+57 301 789 0123"),
            ("Luis Rodríguez", "luis.rodriguez@email.com", "+57 312 345 6789")
        ]
        
        for nombre, email, telefono in contactos_ejemplo:
            gestor.agregar_contacto(nombre, email, telefono)
        
        print("Se han creado contactos de ejemplo")


# Función principal
def main():
    """Función principal del programa."""
    # Crear contactos de ejemplo si no existen
    crear_contactos_ejemplo()
    
    # Iniciar la aplicación
    app = AplicacionContactos()
    app.ejecutar()


if __name__ == "__main__":
    main()