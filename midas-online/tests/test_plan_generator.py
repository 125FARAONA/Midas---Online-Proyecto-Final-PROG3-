
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


evidence_folder = "evidence"
os.makedirs(evidence_folder, exist_ok=True)

capturas = []

def capture(name):
    path = os.path.join(evidence_folder, f"{name}.png")
    driver.save_screenshot(path)
    capturas.append((name, path))
    return path

try:
   
    index_file = os.path.abspath("index.html")
    driver.get(f"file:///{index_file.replace(os.sep, '/')}")
    time.sleep(1)
    capture("index_page")

   
    try:
        usar_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Usar Midas Online')]")
        usar_btn.click()
        time.sleep(1)
        capture("midas_online")
    except Exception as e:
        print("No se encontró el botón 'Usar Midas Online':", e)

   
    driver.get(f"file:///{os.path.abspath('login.html').replace(os.sep, '/')}")
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys("rozenny@example.com")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    capture("login_correcto")

   
    driver.get(f"file:///{os.path.abspath('dashboard.html').replace(os.sep, '/')}")
    time.sleep(1)
    capture("dashboard")

   
    secciones = ["overview", "transactions", "insights"]
    for sec in secciones:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, f"button[data-section='{sec}']")
            btn.click()
            time.sleep(1)
            capture(f"seccion_{sec}")
        except Exception as e:
            print(f"No se pudo clicar la sección {sec}: {e}")

    
    try:
        driver.find_element(By.ID, "logoutBtn").click()
        time.sleep(1)
        capture("cerrar_sesion")
    except:
        print("No se encontró el botón 'Cerrar sesión'")

finally:
    driver.quit()


html_path = os.path.join(evidence_folder, "evidencia_midas.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(f"""
<html>
<head>
    <title>Proyecto Final MIDAS - ONLINE</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 20px; }}
        h1, h2, h3, h4 {{ text-align: center; margin: 5px; }}
        hr {{ border: 2px solid #333; margin: 20px 0; }}
        .capture, .plan {{ border: 2px solid #555; padding: 10px; background-color: #fff; margin: 20px auto; width: 90%; }}
        .capture img {{ width: 100%; max-width: 800px; display: block; margin: 0 auto; }}
        .capture-title, .plan-title {{ font-weight: bold; margin-bottom: 10px; text-align: center; font-size: 18px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 15px; }}
        th, td {{ border: 1px solid #333; padding: 5px; text-align: left; }}
        th {{ background-color: #ddd; }}
        ul {{ margin-left: 20px; }}
    </style>
</head>
<body>
    <h1>PROGRAMACIÓN III (TDS 007)</h1>
    <h2>Proyecto Final MIDAS - ONLINE</h2>
    <h3>PROF. Kelyn Tejada Belliard</h3>
    <h3>18/08/2025</h3>
    <h3>ROZENNY P. VALENTIN 2021-0685</h3>
    <hr>

    <h2>Plan de Pruebas</h2>

    <div class="plan">
        <div class="plan-title">1. Requerimientos Funcionales y No Funcionales</div>
        <h4>Funcionales:</h4>
        <ul>
            <li>Login seguro con validación de usuario y contraseña</li>
            <li>Dashboard con balances y transacciones ficticias</li>
            <li>Gráficos dinámicos de gastos e ingresos</li>
            <li>Botones interactivos: Depositar, Transferir, Pagar, Transacciones, Insights</li>
            <li>Modo claro y oscuro</li>
            <li>Panel de navegación lateral</li>
            <li>Cierre de sesión seguro</li>
        </ul>
        <h4>No funcionales:</h4>
        <ul>
            <li>Responsividad en PC, tablet y móvil</li>
            <li>Accesibilidad con contraste y legibilidad</li>
            <li>Carga rápida y sin errores visibles</li>
            <li>Interfaz intuitiva con animaciones optimizadas</li>
            <li>Seguridad de interfaz (datos ficticios)</li>
        </ul>
    </div>

    <div class="plan">
        <div class="plan-title">2. Criterios de Aceptación y Rechazo</div>
        <table>
            <tr><th>Prueba</th><th>Aceptación</th><th>Rechazo</th></tr>
            <tr><td>Login</td><td>Acceso al dashboard con credenciales válidas</td><td>Mensaje de error o fallo de acceso</td></tr>
            <tr><td>Dashboard</td><td>Botones y gráficos visibles y funcionales</td><td>Algún botón no responde o gráficos no cargan</td></tr>
            <tr><td>Gráficos</td><td>Información dinámica correcta en Chart.js</td><td>Gráficos no cargan o se ven mal</td></tr>
            <tr><td>Modo Claro/Oscuro</td><td>Cambio aplicado sin romper layout</td><td>Elementos superpuestos o sin efecto</td></tr>
            <tr><td>Cierre de sesión</td><td>Redirige a login correctamente</td><td>Sesión permanece activa o redirección falla</td></tr>
        </table>
    </div>

    <div class="plan">
        <div class="plan-title">3. Herramientas de Pruebas</div>
        <ul>
            <li>Selenium + WebDriver Manager: Automatización de UI</li>
            <li>VS Code: Desarrollo y depuración de scripts</li>
            <li>Capturas de pantalla: Evidencia visual de resultados</li>
            <li>Navegadores modernos (Chrome/Edge): Ejecución manual de pruebas</li>
            <li>HTML de evidencia: Documentación completa</li>
        </ul>
    </div>

    <div class="plan">
        <div class="plan-title">4. Cronograma de Ejecución de Pruebas (13/08-17/08)</div>
        <table>
            <tr><th>Fecha</th><th>Tipo de Prueba</th><th>Actividad</th></tr>
            <tr><td>13/08</td><td>Manual</td><td>Validación de login y navegación inicial</td></tr>
            <tr><td>14/08</td><td>Manual</td><td>Pruebas de dashboard y botones</td></tr>
            <tr><td>15/08</td><td>Automatizada</td><td>Automatización de login, navegación y capturas</td></tr>
            <tr><td>16/08</td><td>Manual/Automatizada</td><td>Pruebas de gráficos y modo claro/oscuro</td></tr>
            <tr><td>17/08</td><td>Automatizada</td><td>Generación de evidencia y cierre de sesión</td></tr>
        </table>
    </div>

    <div class="plan">
        <div class="plan-title">5. Casos de Prueba</div>
        <table>
            <tr><th>ID</th><th>Funcionalidad</th><th>Paso</th><th>Datos</th><th>Esperado</th></tr>
            <tr><td>CP01</td><td>Login</td><td>Abrir login.html, ingresar email/pass, click login</td><td>rozenny@example.com / 123456</td><td>Dashboard visible</td></tr>
            <tr><td>CP02</td><td>Dashboard</td><td>Explorar secciones Overview, Transactions, Insights</td><td>N/A</td><td>Secciones visibles y funcionales</td></tr>
            <tr><td>CP03</td><td>Modo Claro/Oscuro</td><td>Activar switch de modo</td><td>N/A</td><td>Interfaz cambia correctamente</td></tr>
            <tr><td>CP04</td><td>Cierre de sesión</td><td>Click en logout</td><td>N/A</td><td>Redirige a login</td></tr>
        </table>
    </div>

    <div class="plan">
        <div class="plan-title">6. Equipos de Pruebas y Responsabilidades</div>
        <ul>
            <li>Rozenny: Ejecución de pruebas manuales y automatizadas</li>
            <li>QA Tester (simulado): Revisión de dashboard y gráficos</li>
            <li>Project Manager (Rozenny): Validación final y generación de evidencia</li>
        </ul>
    </div>

    <div class="plan">
        <div class="plan-title">7. Plan de Automatización de Pruebas</div>
        <ul>
            <li>Herramientas: Selenium, WebDriver Manager, Python</li>
            <li>Estrategia: Automatización de login, navegación por secciones, capturas de evidencia</li>
            <li>Objetivo: Generar evidencia visual para todos los flujos críticos</li>
            <li>Frecuencia: Durante el desarrollo y antes de la entrega final</li>
        </ul>
    </div>

""")

   
    for title, img in capturas:
        f.write(f"""
    <div class="capture">
        <div class="capture-title">{title.replace('_', ' ').title()}</div>
        <img src="{os.path.basename(img)}">
    </div>
""")

    f.write("""
</body>
</html>
""")

print(f"Evidencia visual generada en: {html_path}")
