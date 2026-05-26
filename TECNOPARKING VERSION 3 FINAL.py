import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import math
import os

# =================================================================
# Proyecto: Sistema de Parqueo Automatizado Hexagonal Colmena
# Autor: Juan Fernando Rios
# =================================================================

FILE_NAME = "tecnoparking_activos.txt"
LOG_FILE = "tecnoparking_historial.txt" 
CAR_RATE = 4000
MOTO_RATE = 2000

# Paleta de colores - Panal Azul
BG_BASE = "#07172F"       # Azul muy oscuro (Fondo profundo)
BG_PANAL = "#0B2447"      # Azul celda
FG_TEXT = "#E0F2FE"       # Texto azul claro/blanco
BTN_BLUE = "#19376D"      # Azul medio para botones
BTN_HOVER = "#576CBC"     # Azul brillante para interacciones
ACCENT = "#38BDF8"        # Azul eléctrico brillante

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        pass

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        pass

# --- FUNCIONES LÓGICAS (BACKEND) ---

def park_vehicle(plate, user_id, v_type):
    plate = plate.upper()
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        for line in f:
            if plate in line:
                return False, "El vehículo ya se encuentra en el sistema Colmena."
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(plate + "|" + user_id + "|" + v_type + "|" + current_time + "\n")
        
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{current_time} | INGRESO | Placa: {plate} | Cédula: {user_id} | Tipo: {v_type}\n")
    
    return True, f"Vehículo {plate} ingresado al elevador.\nHora: {current_time}"

def retrieve_vehicle(plate):
    plate = plate.upper()
    found = False
    lines = []
    message = ""
    
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for line in lines:
            data = line.strip().split("|")
            if len(data) == 4 and data[0] == plate:
                found = True
                saved_plate = data[0]
                user_id = data[1]
                v_type = data[2]
                time_str = data[3]
                
                entry_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                exit_time = datetime.datetime.now()
                time_diff = exit_time - entry_time
                
                hours_parked = math.ceil(time_diff.total_seconds() / 3600)
                if hours_parked == 0:
                    hours_parked = 1
                
                rate = CAR_RATE if v_type == "Carro" else MOTO_RATE
                total_cost = hours_parked * rate
                
                message = (f"⬢ RECIBO COLMENA ⬢\n"
                           f"Placa: {saved_plate}\n"
                           f"Cédula: {user_id}\n"
                           f"Tipo: {v_type}\n"
                           f"Tiempo facturado: {hours_parked} hora(s)\n"
                           f"TOTAL A PAGAR: ${total_cost} COP\n\n"
                           f"Extrayendo vehículo de la celda hexagonal...")
                
                exit_time_str = exit_time.strftime("%Y-%m-%d %H:%M:%S")
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"{exit_time_str} | SALIDA  | Placa: {saved_plate} | Cédula: {user_id} | Cobro: ${total_cost} COP\n")
            else:
                f.write(line)
                
    if found == True:
        return True, message
    else:
        return False, "Placa no encontrada en el sistema."

def get_active_vehicles():
    vehicles = []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                vehicles.append(line.strip())
    return vehicles

# --- ESTILOS COMPARTIDOS ---
def style_button(btn):
    btn.configure(bg=BTN_BLUE, fg=FG_TEXT, activebackground=BTN_HOVER, activeforeground="white", relief="flat", bd=0)

def style_entry(entry):
    entry.configure(bg=BG_BASE, fg=ACCENT, insertbackground=ACCENT, relief="solid", bd=1, highlightbackground=BTN_BLUE, highlightcolor=ACCENT)

# --- INTERFAZ GRÁFICA (FRONTEND CON TKINTER) ---

def open_user_window():
    user_win = tk.Toplevel(root)
    user_win.title("TecnoParking - Terminal de Usuario")
    user_win.geometry("400x550")
    user_win.configure(bg=BG_PANAL)
    
    tk.Label(user_win, text="⬢ TERMINAL AUTOMÁTICA ⬢", font=("Arial", 16, "bold"), bg=BG_PANAL, fg=ACCENT).pack(pady=15)
    
    tk.Label(user_win, text="⬡ INGRESAR VEHÍCULO ⬡", font=("Arial", 10, "bold"), bg=BG_PANAL, fg=FG_TEXT).pack()
    
    tk.Label(user_win, text="Placa:", bg=BG_PANAL, fg=FG_TEXT).pack()
    entry_plate_in = tk.Entry(user_win, font=("Arial", 12, "bold"), justify="center")
    style_entry(entry_plate_in)
    entry_plate_in.pack(pady=5)
    
    tk.Label(user_win, text="Cédula:", bg=BG_PANAL, fg=FG_TEXT).pack()
    entry_id = tk.Entry(user_win, font=("Arial", 12, "bold"), justify="center")
    style_entry(entry_id)
    entry_id.pack(pady=5)
    
    v_type_var = tk.StringVar(value="Carro")
    tk.Radiobutton(user_win, text="Carro ($4000/h)", variable=v_type_var, value="Carro", bg=BG_PANAL, fg=FG_TEXT, selectcolor=BG_BASE, activebackground=BG_PANAL, activeforeground=ACCENT).pack()
    tk.Radiobutton(user_win, text="Moto ($2000/h)", variable=v_type_var, value="Moto", bg=BG_PANAL, fg=FG_TEXT, selectcolor=BG_BASE, activebackground=BG_PANAL, activeforeground=ACCENT).pack()
    
    def btn_park():
        plate = entry_plate_in.get().strip()
        user_id = entry_id.get().strip()
        v_type = v_type_var.get()
        
        if plate == "" or user_id == "":
            messagebox.showwarning("Error", "Debe llenar placa y cédula.")
            return
            
        # Validación modificada según tu requerimiento
        if not user_id.isdigit() or len(user_id) > 10:
            messagebox.showwarning("Error", "Ingrese nuevamente la cédula.")
            return
            
        success, msg = park_vehicle(plate, user_id, v_type)
        if success == True:
            messagebox.showinfo("Éxito", msg)
            entry_plate_in.delete(0, tk.END)
            entry_id.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)
            
    btn_p = tk.Button(user_win, text="PARQUEAR", font=("Arial", 10, "bold"), command=btn_park, width=20, pady=5)
    style_button(btn_p)
    btn_p.configure(bg="#0284C7") # Un azul más brillante para la acción principal
    btn_p.pack(pady=15)
    
    tk.Label(user_win, text="⬢ ⬢ ⬢ ⬢ ⬢ ⬢ ⬢ ⬢ ⬢", bg=BG_PANAL, fg=BTN_BLUE).pack(pady=10)
    
    tk.Label(user_win, text="⬡ RETIRAR VEHÍCULO ⬡", font=("Arial", 10, "bold"), bg=BG_PANAL, fg=FG_TEXT).pack()
    tk.Label(user_win, text="Placa a retirar:", bg=BG_PANAL, fg=FG_TEXT).pack()
    entry_plate_out = tk.Entry(user_win, font=("Arial", 12, "bold"), justify="center")
    style_entry(entry_plate_out)
    entry_plate_out.pack(pady=5)
    
    def btn_retrieve():
        plate = entry_plate_out.get().strip()
        if plate == "":
            messagebox.showwarning("Error", "Debe ingresar la placa para retirar.")
            return
            
        success, msg = retrieve_vehicle(plate)
        if success == True:
            messagebox.showinfo("Ticket de Salida", msg)
            entry_plate_out.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)

    btn_r = tk.Button(user_win, text="SOLICITAR AL ELEVADOR", font=("Arial", 10, "bold"), command=btn_retrieve, width=25, pady=5)
    style_button(btn_r)
    btn_r.pack(pady=10)

def open_admin_window():
    password = simpledialog.askstring("Seguridad", "Ingrese clave de administrador:", show='*')
    if password != "admin":
        messagebox.showerror("Acceso Denegado", "Clave incorrecta.")
        return
        
    admin_win = tk.Toplevel(root)
    admin_win.title("TecnoParking - Panel de Control")
    admin_win.geometry("550x450")
    admin_win.configure(bg=BG_PANAL)
    
    tk.Label(admin_win, text="⬢ CELDAS ACTIVAS EN LA COLMENA ⬢", font=("Arial", 14, "bold"), bg=BG_PANAL, fg=ACCENT).pack(pady=15)
    
    listbox = tk.Listbox(admin_win, width=65, height=12, bg=BG_BASE, fg=FG_TEXT, selectbackground=ACCENT, selectforeground="white", bd=0, highlightthickness=1, highlightbackground=BTN_BLUE)
    listbox.pack(pady=10)
    
    vehicles = get_active_vehicles()
    if len(vehicles) == 0:
        listbox.insert(tk.END, "El panal está completamente vacío.")
    else:
        for v in vehicles:
            listbox.insert(tk.END, f"⬡ {v}")
            
    def download_daily_report():
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        report_name = f"reporte_ingresos_salidas_{today_str}.txt"
        
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as log:
                lines = log.readlines()
                
            with open(report_name, "w", encoding="utf-8") as rep:
                rep.write(f"--- REPORTE DIARIO TECNOPARKING ({today_str}) ---\n\n")
                found_records = False
                for line in lines:
                    if line.startswith(today_str):
                        rep.write(line)
                        found_records = True
                        
            if found_records:
                messagebox.showinfo("Reporte Generado", f"El registro de hoy se descargó exitosamente como:\n{report_name}")
            else:
                messagebox.showinfo("Aviso", "No hay registros de ingresos ni salidas para el día de hoy.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al generar el reporte: {e}")
            
    btn_report = tk.Button(admin_win, text="Descargar Registro del Día (.txt)", font=("Arial", 10, "bold"), command=download_daily_report, width=30, pady=5)
    style_button(btn_report)
    btn_report.configure(bg="#0284C7")
    btn_report.pack(pady=5)
    
    btn_close = tk.Button(admin_win, text="Cerrar Panel", command=admin_win.destroy, width=20, pady=5)
    style_button(btn_close)
    btn_close.pack(pady=10)

def show_help():
    messagebox.showinfo("Soporte Tecnoparking", "Llamar a 3105510718")

# --- VENTANA PRINCIPAL (FRONTEND) ---
root = tk.Tk()
root.title("TecnoParking System")
root.geometry("320x350") 
root.configure(bg=BG_BASE)

tk.Label(root, text="⬢ TECNOPARKING ⬢", font=("Arial", 18, "bold"), bg=BG_BASE, fg=ACCENT).pack(pady=25)
tk.Label(root, text="Seleccione su rol en la Colmena:", bg=BG_BASE, fg=FG_TEXT).pack(pady=10)

btn_user = tk.Button(root, text="Modo Usuario (Terminal)", width=25, pady=8, command=open_user_window)
style_button(btn_user)
btn_user.pack(pady=5)

btn_admin = tk.Button(root, text="Modo Administrador", width=25, pady=8, command=open_admin_window)
style_button(btn_admin)
btn_admin.pack(pady=5)

btn_help = tk.Button(root, text="Ayuda", width=25, pady=8, command=show_help)
style_button(btn_help)
btn_help.configure(bg="#0EA5E9") # Azul un poco más claro para diferenciarlo
btn_help.pack(pady=15)

# =================================================================
# EL CICLO INFINITO MANUAL (REQUISITO DE CLASE)
# =================================================================
programa_activo = True

while programa_activo == True:
    try:
        root.update_idletasks()
        root.update()
    except tk.TclError:
        programa_activo = False
        print("Sistema TecnoParking cerrado exitosamente.")
        break