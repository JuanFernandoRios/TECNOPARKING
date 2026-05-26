import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import math
import os

# =================================================================
# Proyecto: Sistema de Parqueo Automatizado Hexagonal Colmena (TECNOPARKING)
# Autor: Juan Fernando Rios
# Persistencia con .txt y ventana controlada 
# manualmente por un ciclo While True.
# =================================================================

FILE_NAME = "tecnoparking_activos.txt"
CAR_RATE = 4000
MOTO_RATE = 2000

# Me aseguro de que el archivo exista al iniciar
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
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
                
                message = (f"--- RECIBO TECNOPARKING ---\n"
                           f"Placa: {saved_plate}\n"
                           f"Cédula: {user_id}\n"
                           f"Tipo: {v_type}\n"
                           f"Tiempo facturado: {hours_parked} hora(s)\n"
                           f"TOTAL A PAGAR: ${total_cost} COP\n\n"
                           f"El elevador hexagonal está entregando su vehículo...")
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

# --- INTERFAZ GRÁFICA (FRONTEND CON TKINTER) ---

def open_user_window():
    user_win = tk.Toplevel(root)
    user_win.title("TecnoParking - Terminal de Usuario")
    user_win.geometry("400x500")
    user_win.configure(bg="#f0f0f0")
    
    tk.Label(user_win, text="TERMINAL AUTOMÁTICA", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=15)
    
    tk.Label(user_win, text="--- INGRESAR VEHÍCULO ---", font=("Arial", 10, "bold"), bg="#f0f0f0").pack()
    tk.Label(user_win, text="Placa:", bg="#f0f0f0").pack()
    entry_plate_in = tk.Entry(user_win)
    entry_plate_in.pack(pady=5)
    
    tk.Label(user_win, text="Cédula:", bg="#f0f0f0").pack()
    entry_id = tk.Entry(user_win)
    entry_id.pack(pady=5)
    
    v_type_var = tk.StringVar(value="Carro")
    tk.Radiobutton(user_win, text="Carro ($4000/h)", variable=v_type_var, value="Carro", bg="#f0f0f0").pack()
    tk.Radiobutton(user_win, text="Moto ($2000/h)", variable=v_type_var, value="Moto", bg="#f0f0f0").pack()
    
    def btn_park():
        plate = entry_plate_in.get().strip()
        user_id = entry_id.get().strip()
        v_type = v_type_var.get()
        
        if plate == "" or user_id == "":
            messagebox.showwarning("Error", "Debe llenar placa y cédula.")
            return
            
        success, msg = park_vehicle(plate, user_id, v_type)
        if success == True:
            messagebox.showinfo("Éxito", msg)
            entry_plate_in.delete(0, tk.END)
            entry_id.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)
            
    tk.Button(user_win, text="PARQUEAR", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=btn_park).pack(pady=10)
    
    tk.Label(user_win, text="-------------------------", bg="#f0f0f0").pack(pady=5)
    
    tk.Label(user_win, text="--- RETIRAR VEHÍCULO ---", font=("Arial", 10, "bold"), bg="#f0f0f0").pack()
    tk.Label(user_win, text="Placa a retirar:", bg="#f0f0f0").pack()
    entry_plate_out = tk.Entry(user_win)
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

    tk.Button(user_win, text="SOLICITAR AL ELEVADOR", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=btn_retrieve).pack(pady=10)

def open_admin_window():
    password = simpledialog.askstring("Seguridad", "Ingrese clave de administrador:", show='*')
    if password != "admin":
        messagebox.showerror("Acceso Denegado", "Clave incorrecta.")
        return
        
    admin_win = tk.Toplevel(root)
    admin_win.title("TecnoParking - Panel de Control")
    admin_win.geometry("500x400")
    
    tk.Label(admin_win, text="VEHÍCULOS ACTIVOS EN LA COLMENA", font=("Arial", 14, "bold")).pack(pady=15)
    
    listbox = tk.Listbox(admin_win, width=60, height=15)
    listbox.pack(pady=10)
    
    vehicles = get_active_vehicles()
    if len(vehicles) == 0:
        listbox.insert(tk.END, "El parqueadero está completamente vacío.")
    else:
        for v in vehicles:
            listbox.insert(tk.END, v)
            
    tk.Button(admin_win, text="Cerrar Panel", command=admin_win.destroy).pack(pady=10)


# --- VENTANA PRINCIPAL (FRONTEND) ---
root = tk.Tk()
root.title("TecnoParking System")
root.geometry("300x250")
root.configure(bg="#2c3e50")

tk.Label(root, text="TECNOPARKING", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
tk.Label(root, text="Seleccione su rol:", bg="#2c3e50", fg="white").pack(pady=10)

tk.Button(root, text="Modo Usuario (Terminal)", width=25, bg="#ecf0f1", command=open_user_window).pack(pady=5)
tk.Button(root, text="Modo Administrador", width=25, bg="#ecf0f1", command=open_admin_window).pack(pady=5)


# =================================================================
# EL CICLO INFINITO MANUAL (REQUISITO DE CLASE)
# =================================================================
programa_activo = True

# Usamos nuestro propio ciclo While True para refrescar la ventana visual
while programa_activo == True:
    try:
        # Estas dos funciones redibujan la ventana y detectan los clics del mouse
        root.update_idletasks()
        root.update()
    except tk.TclError:
        # Si el usuario cierra la ventana principal en la "X" roja, el programa entra aquí
        programa_activo = False
        print("Sistema TecnoParking cerrado exitosamente.")
        break # Rompemos el ciclo infinito para apagar el programa