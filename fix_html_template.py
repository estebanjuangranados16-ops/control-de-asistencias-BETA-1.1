import re

def fix_html_template():
    """Corregir template HTML que muestra CSS como texto"""
    
    template_path = \"templates/unified_dashboard.html\"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si hay CSS visible en el body
        if '.container {' in content and '<body>' in content:
            print("Detectado CSS visible en el body - corrigiendo...")\n            
            # Encontrar donde termina el CSS y empieza el HTML del body\n            body_start = content.find('<body>')\n            if body_start != -1:\n                # Buscar el primer div después de <body>\n                first_div = content.find('<div', body_start)\n                if first_div != -1:\n                    # Extraer solo la parte del body válida\n                    body_content = content[first_div:]\n                    \n                    # Reconstruir el HTML completo\n                    fixed_content = content[:body_start + 6] + '\\n    ' + body_content\n                    \n                    # Guardar el archivo corregido\n                    with open(template_path, 'w', encoding='utf-8') as f:\n                        f.write(fixed_content)\n                    \n                    print("✅ Template HTML corregido")\n                    return True\n        \n        print("Template parece estar correcto")\n        return True\n        \n    except Exception as e:\n        print(f"Error: {e}")\n        return False\n\nif __name__ == \"__main__\":\n    fix_html_template()