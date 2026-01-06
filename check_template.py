print("Verificando template HTML...")

try:
    with open("templates/unified_dashboard.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Verificar si hay CSS visible después de <body>
    body_start = content.find("<body>")
    if body_start != -1:
        body_content = content[body_start:body_start + 500]
        if ".container {" in body_content:
            print("PROBLEMA: CSS visible en el body")
            print("Necesita corrección manual")
        else:
            print("Template parece correcto")
    
except Exception as e:
    print(f"Error: {e}")