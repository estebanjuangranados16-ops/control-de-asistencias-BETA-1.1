import sqlite3

def add_employee_manual():
    """Agregar empleado manualmente desde consola"""
    print("AGREGAR EMPLEADO MANUALMENTE")
    print("=" * 30)
    
    # Solicitar datos
    employee_id = input("ID del empleado: ").strip()
    name = input("Nombre completo: ").strip()
    department = input("Departamento (General/Reacondicionamiento/Ventas/etc): ").strip() or "General"
    
    print("\nHorarios disponibles:")
    print("1. Normal (estandar)")
    print("2. Reacondicionamiento")
    schedule_choice = input("Selecciona horario (1 o 2): ").strip()
    
    if schedule_choice == "2":
        schedule = "reacondicionamiento"
    else:
        schedule = "estandar"
    
    phone = input("Teléfono (opcional): ").strip()
    email = input("Email (opcional): ").strip()
    
    # Confirmar datos
    print(f"\nDatos a agregar:")
    print(f"ID: {employee_id}")
    print(f"Nombre: {name}")
    print(f"Departamento: {department}")
    print(f"Horario: {schedule}")
    print(f"Teléfono: {phone}")
    print(f"Email: {email}")
    
    confirm = input("\n¿Confirmar? (s/n): ").strip().lower()
    
    if confirm != 's':
        print("Cancelado")
        return
    
    # Agregar a base de datos
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO employees (employee_id, name, department, schedule, phone, email, active) 
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (employee_id, name, department, schedule, phone, email))
        
        conn.commit()
        print(f"\n✅ Empleado {name} agregado exitosamente!")
        print(f"ID: {employee_id} | Departamento: {department} | Horario: {schedule}")
        
    except sqlite3.IntegrityError:
        print(f"\n❌ Error: Ya existe un empleado con ID {employee_id}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        conn.close()

def list_employees():
    """Listar todos los empleados"""
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT employee_id, name, department, schedule, active 
        FROM employees 
        ORDER BY employee_id
    ''')
    
    employees = cursor.fetchall()
    conn.close()
    
    print("\nEMPLEADOS REGISTRADOS:")
    print("-" * 50)
    for emp in employees:
        status = "Activo" if emp[4] else "Inactivo"
        print(f"ID: {emp[0]:3} | {emp[1]:20} | {emp[2]:15} | {emp[3]:15} | {status}")

def main():
    while True:
        print("\n" + "="*40)
        print("GESTIÓN MANUAL DE EMPLEADOS")
        print("="*40)
        print("1. Agregar empleado")
        print("2. Listar empleados")
        print("3. Salir")
        
        choice = input("\nSelecciona opción: ").strip()
        
        if choice == "1":
            add_employee_manual()
        elif choice == "2":
            list_employees()
        elif choice == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()