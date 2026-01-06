import os

def quick_fix_ip():
    """Actualizar IP rápidamente en el archivo actual"""
    filename = "system_optimized.py"
    
    if not os.path.exists(filename):
        print("ERROR: system_optimized.py no encontrado")
        return
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Actualizar IP
        old_ip = "172.10.0.66"
        new_ip = "172.10.1.62"
        
        if old_ip in content:
            content = content.replace(old_ip, new_ip)
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"IP actualizada de {old_ip} a {new_ip}")
            print("Ahora ejecuta: python system_optimized.py")
        else:
            print("IP ya está actualizada")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    quick_fix_ip()