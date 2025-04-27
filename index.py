import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import threading

class JuegoAdivinanza:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Adivinanza de Números")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Variables del juego
        self.numero_secreto = None
        self.intentos = []
        self.intentos_maximos = 0
        self.intentos_restantes = 0
        self.limite_inferior = 0
        self.limite_superior = 0
        self.jugando = False
        self.puntuacion = 0
        
        # Inicializar la variable sonidos_activados ANTES de usarla
        self.sonidos_activados = tk.BooleanVar(value=True)
        
        # Colores
        self.color_primario = "#4a7abc"
        self.color_secundario = "#3a5a8c"
        self.color_acento = "#ff9500"
        self.color_texto = "#333333"
        self.color_fondo = "#f0f0f0"
        
        # Crear frames principales
        self.frame_menu = tk.Frame(root, bg=self.color_fondo)
        self.frame_configuracion = tk.Frame(root, bg=self.color_fondo)
        self.frame_juego = tk.Frame(root, bg=self.color_fondo)
        self.frame_demo = tk.Frame(root, bg=self.color_fondo)
        
        # Inicializar interfaz
        self.configurar_estilos()
        self.crear_menu_principal()
        self.crear_pantalla_configuracion()
        self.crear_pantalla_juego()
        self.crear_pantalla_demo()
        
        # Mostrar pantalla inicial
        self.mostrar_frame(self.frame_menu)
        
    def configurar_estilos(self):
        # Configurar estilos personalizados
        estilo = ttk.Style()
        estilo.configure("TButton", 
                        font=("Helvetica", 12, "bold"), 
                        background=self.color_primario,
                        foreground="white")
        
        estilo.configure("Grande.TButton", 
                        font=("Helvetica", 14, "bold"), 
                        padding=10)
                        
        estilo.configure("TLabel", 
                        font=("Helvetica", 12),
                        background=self.color_fondo,
                        foreground=self.color_texto)
                        
        estilo.configure("Titulo.TLabel", 
                        font=("Helvetica", 24, "bold"),
                        foreground=self.color_primario,
                        background=self.color_fondo)
                        
        estilo.configure("Subtitulo.TLabel", 
                        font=("Helvetica", 16, "bold"),
                        foreground=self.color_secundario,
                        background=self.color_fondo)
                        
        estilo.configure("Info.TLabel", 
                        font=("Helvetica", 12, "italic"),
                        foreground=self.color_secundario,
                        background=self.color_fondo)
    
    def mostrar_frame(self, frame):
        # Ocultar todos los frames
        for f in [self.frame_menu, self.frame_configuracion, self.frame_juego, self.frame_demo]:
            f.pack_forget()
        
        # Mostrar el frame seleccionado
        frame.pack(fill="both", expand=True)
    
    def crear_menu_principal(self):
        # Frame del menú principal
        frame_titulo = tk.Frame(self.frame_menu, bg=self.color_fondo)
        frame_titulo.pack(pady=40)
        
        titulo = ttk.Label(frame_titulo, text="JUEGO DE ADIVINANZA", style="Titulo.TLabel")
        titulo.pack()
        
        subtitulo = ttk.Label(frame_titulo, text="¡Demuestra tu habilidad para adivinar números!", style="Subtitulo.TLabel")
        subtitulo.pack(pady=10)
        
        # Frame de botones
        frame_botones = tk.Frame(self.frame_menu, bg=self.color_fondo)
        frame_botones.pack(pady=40)
        
        btn_jugar = ttk.Button(frame_botones, text="Jugar", style="Grande.TButton", 
                              command=lambda: self.mostrar_frame(self.frame_configuracion))
        btn_jugar.pack(pady=15, ipadx=30, ipady=10)
        
        btn_demo = ttk.Button(frame_botones, text="Ver Demostración de Búsqueda Binaria", style="Grande.TButton",
                             command=self.iniciar_demo)
        btn_demo.pack(pady=15, ipadx=30, ipady=10)
        
        # Opciones
        frame_opciones = tk.Frame(self.frame_menu, bg=self.color_fondo)
        frame_opciones.pack(pady=20, side="bottom", fill="x")
        
        check_sonido = ttk.Checkbutton(frame_opciones, text="Sonidos", variable=self.sonidos_activados)
        check_sonido.pack(side="left", padx=20)
        
        btn_salir = ttk.Button(frame_opciones, text="Salir", command=self.root.destroy)
        btn_salir.pack(side="right", padx=20)
        
        # Información
        info = ttk.Label(frame_opciones, text="© 2025 - Juego Educativo", style="Info.TLabel")
        info.pack(side="bottom", pady=10)
    
    def crear_pantalla_configuracion(self):
        # Título
        titulo = ttk.Label(self.frame_configuracion, text="CONFIGURACIÓN DEL JUEGO", style="Titulo.TLabel")
        titulo.pack(pady=30)
        
        # Frame para los controles
        frame_controles = tk.Frame(self.frame_configuracion, bg=self.color_fondo)
        frame_controles.pack(pady=20)
        
        # Rango de números
        ttk.Label(frame_controles, text="Selecciona el rango de números:", style="Subtitulo.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame_controles, text="Mínimo:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.min_var = tk.StringVar(value="1")
        min_entry = ttk.Entry(frame_controles, textvariable=self.min_var, width=10)
        min_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(frame_controles, text="Máximo:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.max_var = tk.StringVar(value="100")
        max_entry = ttk.Entry(frame_controles, textvariable=self.max_var, width=10)
        max_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Número de intentos
        ttk.Label(frame_controles, text="Número de intentos:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.intentos_var = tk.StringVar(value="10")
        intentos_entry = ttk.Entry(frame_controles, textvariable=self.intentos_var, width=10)
        intentos_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Dificultad (decorativo)
        ttk.Label(frame_controles, text="Dificultad:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        dificultades = ["Fácil", "Normal", "Difícil", "Extremo"]
        self.dificultad_var = tk.StringVar(value="Normal")
        dificultad_combo = ttk.Combobox(frame_controles, textvariable=self.dificultad_var, 
                                       values=dificultades, state="readonly", width=10)
        dificultad_combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # Botones de acción
        frame_botones = tk.Frame(self.frame_configuracion, bg=self.color_fondo)
        frame_botones.pack(pady=30)
        
        btn_volver = ttk.Button(frame_botones, text="Volver", 
                              command=lambda: self.mostrar_frame(self.frame_menu))
        btn_volver.grid(row=0, column=0, padx=20)
        
        btn_comenzar = ttk.Button(frame_botones, text="¡Comenzar Juego!", style="Grande.TButton",
                                command=self.iniciar_juego)
        btn_comenzar.grid(row=0, column=1, padx=20)
    
    def crear_pantalla_juego(self):
        # Panel superior - Información
        panel_info = tk.Frame(self.frame_juego, bg=self.color_secundario, height=60)
        panel_info.pack(fill="x")
        panel_info.pack_propagate(False)
        
        self.lbl_rango = ttk.Label(panel_info, text="Rango: 1-100", foreground="white", background=self.color_secundario)
        self.lbl_rango.pack(side="left", padx=20)
        
        self.lbl_intentos = ttk.Label(panel_info, text="Intentos: 10/10", foreground="white", background=self.color_secundario)
        self.lbl_intentos.pack(side="right", padx=20)
        
        # Panel central - Juego
        panel_central = tk.Frame(self.frame_juego, bg=self.color_fondo)
        panel_central.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ingreso de número
        frame_ingreso = tk.Frame(panel_central, bg=self.color_fondo)
        frame_ingreso.pack(pady=20)
        
        self.lbl_mensaje = ttk.Label(frame_ingreso, text="¡Adivina el número secreto!", style="Subtitulo.TLabel")
        self.lbl_mensaje.pack(pady=10)
        
        self.lbl_pista = ttk.Label(frame_ingreso, text="Ingresa un número y presiona 'Adivinar'")
        self.lbl_pista.pack(pady=5)
        
        frame_entrada = tk.Frame(frame_ingreso, bg=self.color_fondo)
        frame_entrada.pack(pady=20)
        
        self.entrada_numero = ttk.Entry(frame_entrada, width=15, font=("Helvetica", 18))
        self.entrada_numero.pack(side="left", padx=10)
        self.entrada_numero.bind("<Return>", lambda e: self.verificar_intento())
        
        btn_adivinar = ttk.Button(frame_entrada, text="Adivinar", 
                                command=self.verificar_intento)
        btn_adivinar.pack(side="left", padx=10)
        
        # Historial de intentos
        frame_historial = tk.Frame(panel_central, bg="white", bd=1, relief="solid")
        frame_historial.pack(fill="both", expand=True, pady=20)
        
        ttk.Label(frame_historial, text="Historial de intentos:", background="white").pack(anchor="w", padx=10, pady=5)
        
        self.historial_text = tk.Text(frame_historial, height=8, width=40, state="disabled", font=("Helvetica", 10))
        self.historial_text.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Panel inferior - Botones
        panel_botones = tk.Frame(self.frame_juego, bg=self.color_fondo)
        panel_botones.pack(fill="x", pady=10)
        
        btn_volver_menu = ttk.Button(panel_botones, text="Abandonar Juego", 
                                   command=self.volver_al_menu)
        btn_volver_menu.pack(side="left", padx=20)
        
        btn_pista = ttk.Button(panel_botones, text="Obtener Pista", 
                             command=self.dar_pista)
        btn_pista.pack(side="right", padx=20)
    
    def crear_pantalla_demo(self):
        # Título
        titulo = ttk.Label(self.frame_demo, text="DEMOSTRACIÓN DE BÚSQUEDA BINARIA", style="Titulo.TLabel")
        titulo.pack(pady=20)
        
        # Panel de visualización
        panel_visual = tk.Frame(self.frame_demo, bg="white", bd=1, relief="solid")
        panel_visual.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas para visualización
        self.canvas = tk.Canvas(panel_visual, bg="white", height=200)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la búsqueda
        frame_info = tk.Frame(self.frame_demo, bg=self.color_fondo)
        frame_info.pack(fill="x", padx=20, pady=10)
        
        self.lbl_demo_info = ttk.Label(frame_info, text="La búsqueda binaria es un algoritmo eficiente para encontrar un valor en una lista ordenada.",
                                     wraplength=700, justify="center")
        self.lbl_demo_info.pack()
        
        self.lbl_demo_status = ttk.Label(frame_info, text="Presiona 'Iniciar' para comenzar la demostración", 
                                       style="Subtitulo.TLabel")
        self.lbl_demo_status.pack(pady=10)
        
        # Controles
        frame_controles = tk.Frame(self.frame_demo, bg=self.color_fondo)
        frame_controles.pack(pady=20)
        
        btn_volver = ttk.Button(frame_controles, text="Volver al Menú", 
                              command=lambda: self.mostrar_frame(self.frame_menu))
        btn_volver.pack(side="left", padx=10)
        
        self.btn_iniciar_demo = ttk.Button(frame_controles, text="Iniciar Demostración", 
                                        command=self.ejecutar_demo)
        self.btn_iniciar_demo.pack(side="left", padx=10)
        
    def iniciar_juego(self):
        try:
            # Obtener configuración
            self.limite_inferior = int(self.min_var.get())
            self.limite_superior = int(self.max_var.get())
            self.intentos_maximos = int(self.intentos_var.get())
            
            # Validaciones
            if self.limite_inferior >= self.limite_superior:
                messagebox.showerror("Error", "El límite inferior debe ser menor que el límite superior.")
                return
                
            if self.intentos_maximos <= 0:
                messagebox.showerror("Error", "El número de intentos debe ser mayor que cero.")
                return
                
            # Inicializar juego
            self.numero_secreto = random.randint(self.limite_inferior, self.limite_superior)
            self.intentos = []
            self.intentos_restantes = self.intentos_maximos
            self.jugando = True
            
            # Actualizar interfaz
            self.lbl_rango.config(text=f"Rango: {self.limite_inferior}-{self.limite_superior}")
            self.lbl_intentos.config(text=f"Intentos: {self.intentos_restantes}/{self.intentos_maximos}")
            self.lbl_mensaje.config(text="¡Adivina el número secreto!")
            self.lbl_pista.config(text="Ingresa un número y presiona 'Adivinar'")
            
            # Limpiar historial
            self.historial_text.config(state="normal")
            self.historial_text.delete("1.0", tk.END)
            self.historial_text.config(state="disabled")
            
            # Cambiar a pantalla de juego
            self.mostrar_frame(self.frame_juego)
            self.entrada_numero.focus()
            
            # Efecto de inicio
            self.mostrar_animacion("¡COMIENZA EL JUEGO!")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
    
    def verificar_intento(self):
        if not self.jugando:
            return
            
        try:
            intento = int(self.entrada_numero.get())
            self.entrada_numero.delete(0, tk.END)
            
            # Verificar si el número está en el rango
            if intento < self.limite_inferior or intento > self.limite_superior:
                messagebox.showwarning("Fuera de rango", 
                                      f"Por favor, ingresa un número entre {self.limite_inferior} y {self.limite_superior}.")
                return
                
            # Registrar intento
            self.intentos.append(intento)
            self.intentos_restantes -= 1
            
            # Actualizar interfaz
            self.lbl_intentos.config(text=f"Intentos: {self.intentos_restantes}/{self.intentos_maximos}")
            
            # Añadir al historial
            self.historial_text.config(state="normal")
            if intento < self.numero_secreto:
                self.historial_text.insert(tk.END, f"#{len(self.intentos)}: {intento} → Muy bajo\n")
                self.lbl_pista.config(text="El número secreto es MAYOR que tu intento")
            elif intento > self.numero_secreto:
                self.historial_text.insert(tk.END, f"#{len(self.intentos)}: {intento} → Muy alto\n")
                self.lbl_pista.config(text="El número secreto es MENOR que tu intento")
            else:
                self.historial_text.insert(tk.END, f"#{len(self.intentos)}: {intento} → ¡CORRECTO!\n")
            self.historial_text.see(tk.END)
            self.historial_text.config(state="disabled")
            
            # Verificar resultado
            if intento == self.numero_secreto:
                self.jugando = False
                intentos_usados = self.intentos_maximos - self.intentos_restantes
                factor_dificultad = (self.limite_superior - self.limite_inferior) / 100
                self.puntuacion = int((1000 / self.intentos_maximos) * (self.intentos_maximos - intentos_usados + 1) * factor_dificultad)
                
                mensaje = f"¡FELICIDADES! Has adivinado el número en {intentos_usados} intentos.\n"
                mensaje += f"Tu puntuación es: {self.puntuacion} puntos."
                
                self.lbl_mensaje.config(text="¡HAS GANADO!")
                
                # Animación de victoria
                self.mostrar_animacion("¡VICTORIA!")
                
                # Mostrar diálogo después de la animación
                self.root.after(2000, lambda: messagebox.showinfo("¡Felicidades!", mensaje))
                
            elif self.intentos_restantes == 0:
                self.jugando = False
                self.lbl_mensaje.config(text="¡JUEGO TERMINADO!")
                self.lbl_pista.config(text=f"El número secreto era: {self.numero_secreto}")
                
                messagebox.showinfo("Fin del juego", 
                                  f"Se han agotado tus intentos.\nEl número secreto era: {self.numero_secreto}")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido.")
    
    def dar_pista(self):
        if not self.jugando or len(self.intentos) == 0:
            return
            
        # Calcular pista basada en búsqueda binaria
        intentos_validos = [i for i in self.intentos]
        min_actual = self.limite_inferior
        max_actual = self.limite_superior
        
        for intento in intentos_validos:
            if intento < self.numero_secreto:
                min_actual = max(min_actual, intento + 1)
            elif intento > self.numero_secreto:
                max_actual = min(max_actual, intento - 1)
        
        sugerencia = (min_actual + max_actual) // 2
        
        messagebox.showinfo("Pista de búsqueda binaria", 
                          f"Considerando tus intentos anteriores, te sugiero probar con el número {sugerencia}.\n\n"
                          f"Este número está en medio del rango posible actual ({min_actual}-{max_actual}).")
    
    def mostrar_animacion(self, texto):
        def animar():
            # Crear overlay
            overlay = tk.Toplevel(self.root)
            overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")
            overlay.overrideredirect(True)
            overlay.attributes('-alpha', 0.7)
            overlay.configure(bg="black")
            
            # Etiqueta de texto
            lbl = tk.Label(overlay, text=texto, font=("Helvetica", 36, "bold"), fg=self.color_acento, bg="black")
            lbl.place(relx=0.5, rely=0.5, anchor="center")
            
            # Cerrar después de un tiempo
            self.root.after(1500, overlay.destroy)
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        animation_thread = threading.Thread(target=animar)
        animation_thread.daemon = True
        animation_thread.start()
    
    def iniciar_demo(self):
        self.mostrar_frame(self.frame_demo)
        
        # Resetear canvas
        self.canvas.delete("all")
        
        # Configurar valores para la demostración
        self.demo_min = 1
        self.demo_max = 100
        self.demo_secreto = random.randint(self.demo_min, self.demo_max)
        
        # Dibujar línea base
        self.canvas.create_line(50, 100, 750, 100, width=2)
        
        # Marcar límites
        self.canvas.create_text(50, 120, text=str(self.demo_min))
        self.canvas.create_text(750, 120, text=str(self.demo_max))
        
        self.lbl_demo_status.config(text=f"Se ha generado un número secreto entre {self.demo_min} y {self.demo_max}")
    
    def ejecutar_demo(self):
        # Deshabilitar botón durante la demo
        self.btn_iniciar_demo.config(state="disabled")
        
        # Iniciar demo
        self.ejecutar_paso_demo(self.demo_min, self.demo_max, 1)
        
    def ejecutar_paso_demo(self, min_actual, max_actual, paso):
        # Calcular intento actual (búsqueda binaria)
        intento = (min_actual + max_actual) // 2
        
        # Actualizar info
        self.lbl_demo_status.config(text=f"Paso #{paso}: Probando con {intento}")
        
        # Dibujar marcador del intento actual
        x_pos = 50 + (intento - self.demo_min) * (700 / (self.demo_max - self.demo_min))
        
        # Limpiar marcadores anteriores
        self.canvas.delete("marcador")
        
        # Dibujar nuevo marcador
        self.canvas.create_oval(x_pos-10, 90, x_pos+10, 110, fill=self.color_acento, tags="marcador")
        self.canvas.create_text(x_pos, 70, text=str(intento), tags="marcador")
        
        # Pausar para efecto visual
        self.root.update()
        self.root.after(1000)
        
        # Verificar resultado
        if intento == self.demo_secreto:
            self.lbl_demo_status.config(text=f"¡Encontrado! El número secreto es {intento} (en {paso} pasos)")
            self.canvas.create_text(400, 30, text="¡NÚMERO ENCONTRADO!", font=("Helvetica", 16, "bold"), fill="green")
            self.btn_iniciar_demo.config(state="normal")
        elif intento < self.demo_secreto:
            # Dibujar flecha hacia la derecha
            self.canvas.create_line(x_pos, 130, x_pos+50, 130, arrow=tk.LAST, tags="marcador")
            self.lbl_demo_info.config(text="El número es MAYOR. Descartamos todos los números menores o iguales al intento actual.")
            
            # Colorear área descartada
            self.canvas.create_rectangle(50, 150, x_pos, 180, fill="lightgray", tags="marcador")
            self.canvas.create_text((50+x_pos)/2, 165, text="Descartado", tags="marcador")
            
            # Siguiente paso
            self.root.after(1500, lambda: self.ejecutar_paso_demo(intento + 1, max_actual, paso + 1))
        else:  # intento > self.demo_secreto
            # Dibujar flecha hacia la izquierda
            self.canvas.create_line(x_pos, 130, x_pos-50, 130, arrow=tk.LAST, tags="marcador")
            self.lbl_demo_info.config(text="El número es MENOR. Descartamos todos los números mayores o iguales al intento actual.")
            
            # Colorear área descartada
            self.canvas.create_rectangle(x_pos, 150, 750, 180, fill="lightgray", tags="marcador")
            self.canvas.create_text((x_pos+750)/2, 165, text="Descartado", tags="marcador")
            
            # Siguiente paso
            self.root.after(1500, lambda: self.ejecutar_paso_demo(min_actual, intento - 1, paso + 1))
    
    def volver_al_menu(self):
        if self.jugando:
            respuesta = messagebox.askyesno("Abandonar juego", 
                                          "¿Estás seguro de que quieres abandonar el juego actual?")
            if not respuesta:
                return
        
        self.jugando = False
        self.mostrar_frame(self.frame_menu)

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoAdivinanza(root)
    root.mainloop()