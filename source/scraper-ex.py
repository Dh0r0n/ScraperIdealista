import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

options = Options()
options.add_argument(f"user-agent={user_agent}")
# Las siguientes dos opciones evitarán que seamos detectado como un bot
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Solo recogeremos información de las primeras 60 páginas ya que
# Cuando llegas a 60 la página te detiene.
n_pages = 60 

# Se podría buscar más si fuese necesario
# como si el lugar está ocupado ilegalmente o entrar en cada link por más información.
titles, prices, links = [], [], []
rooms_list, sqm_list, floor_list, agency_list, garaje_list = [], [], [], [], []

for page in range(1, n_pages + 1):
    if page == 1:
        url = "https://www.idealista.com/venta-viviendas/valencia-valencia/"
    else:
        url = f"https://www.idealista.com/venta-viviendas/valencia-valencia/pagina-{page}.htm"
    
    print(f"\nScrapeando página {page}...")
    driver.get(url)
    # Intentaremos imitar el comportamiento humano entre peticiones
    time.sleep(random.uniform(1, 3))

    # Buscamos el botón para aceptar las cookies 
    # (lo dejamos comentado ya que no es necesario)
    """try:
        cookie_button = driver.find_element(By.CLASS_NAME, "didomi-accept-button")
        cookie_button.click()
        time.sleep(1)
    except:
        pass  # Si no aparece, seguimos"""

    # Encontrar los anuncios de las viviendas
    ads = driver.find_elements(By.CLASS_NAME, "item-info-container")

    for ad in ads:
        # Información básica del anuncio
        try:
            title_el = ad.find_element(By.CLASS_NAME, "item-link")
            title = title_el.text

            price = ad.find_element(By.CLASS_NAME, "item-price").text

            link = title_el.get_attribute("href")
            try:
                garaje = ad.find_element(By.CLASS_NAME, "item-parking").text
            except:
                garaje = "No incluye garaje"
                
            # Extraemos las características de cada vivienda
            details = ad.find_elements(By.CLASS_NAME, "item-detail")
            info_texts = [d.text.lower() for d in details]

            rooms = next((txt for txt in info_texts if "hab" in txt), "")
            sqm = next((txt for txt in info_texts if "m²" in txt), "")
            floor = next((txt for txt in info_texts if "planta" in txt or "bajo" in txt or "ascensor" in txt), "")
            
            # Agencia (puede estar en la esquina o en la parte inferior del anuncio)
            try:
                agency = ad.find_element(By.CLASS_NAME, "hightop-agent-name").text
            except:
                try:
                    agency_el = ad.find_element(By.CSS_SELECTOR, 'a[data-markup="listado::logo-agencia"]')
                    agency = agency_el.get_attribute("title")
                except:
                    agency = "Particular o sin info"
           
            titles.append(title)
            prices.append(price)
            links.append(link)
            rooms_list.append(rooms)
            sqm_list.append(sqm)
            floor_list.append(floor)
            agency_list.append(agency)
            garaje_list.append(garaje)

            # Mostrar los datos para verificar
            # print(f"{title} | {price} | {rooms} | {sqm} | {floor} | {agency} | {link} | {garaje}")

            # time.sleep(random.uniform(1, 2))  # Delay entre anuncios

        except Exception as e:
            print("Error en anuncio:", e)

driver.quit()

# Guardamos la información a CSV
df = pd.DataFrame({
    "Título": titles,
    "Precio": prices,
    "Habitaciones": rooms_list,
    "Metros cuadrados": sqm_list,
    "Planta": floor_list,
    "Comercializado por": agency_list,
    "Link": links,
    "Garaje": garaje_list
})

# Añadimos un ID único a los registros
df.reset_index(drop=True, inplace=True)
df.insert(0, "ID", df.index + 1)

output_folder = "dataset"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "idealista_valencia_full.csv")

df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(df)
print(f"\n CSV guardado en '{os.path.abspath(output_folder)}'")