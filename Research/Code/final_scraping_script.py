"""
Script de scraping The Motley Fool - Version Production S&P 500.
Fonctionnalités : Multi-Années, Anti-Popup, Human Scroll, Video Killer.
Modification : Gestion centralisée de la vitesse.
"""

import time
import random
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# --- CONFIGURATION ---
CSV_FILENAME = "sp500_transcripts_history.csv"
TARGET_YEARS = ["2025", "2024"]
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]

# --- CONFIGURATION DE LA VITESSE (Timing) ---
# "FAST"     : Pour tester le code (Risque de blocage élevé sur la durée)
# "MARATHON" : Pour tourner 24h/24 pendant 3 jours (Sécurisé)
MODE = "MARATHON" 

SPEED_PROFILES = {
    "FAST": {
        "google_search": (2, 3),   # Pause avant/après recherche
        "page_load": (3, 5),       # Temps de chargement page
        "inter_request": (5, 8)    # Pause entre deux entreprises
    },
    "MARATHON": {
        "google_search": (4, 7),   # On prend le temps de "taper"
        "page_load": (5, 10),      # On laisse la page charger tranquillement
        "inter_request": (15, 35)  # Longue pause pour refroidir l'anti-bot
    }
}

# On charge les délais du mode choisi
DELAYS = SPEED_PROFILES[MODE]

# Liste S&P 500 "Blue Chips"
COMPANIES = [
    # --- TECH & GAFAM ---
    "Apple Inc. (AAPL)", "Microsoft Corporation (MSFT)", "Nvidia Corporation (NVDA)",
    "Alphabet Inc. (GOOGL)", "Amazon.com Inc. (AMZN)", "Meta Platforms (META)",
    "Tesla Inc. (TSLA)", "Broadcom Inc. (AVGO)", "Adobe Inc. (ADBE)",
    "Salesforce (CRM)", "Cisco Systems (CSCO)", "Oracle Corporation (ORCL)",
    "Intel Corporation (INTC)", "AMD (AMD)", "Netflix (NFLX)", "IBM (IBM)",
    # --- FINANCE ---
    "Berkshire Hathaway (BRK-B)", "JPMorgan Chase (JPM)", "Visa Inc. (V)",
    "Mastercard (MA)", "Bank of America (BAC)", "Wells Fargo (WFC)",
    "Goldman Sachs (GS)", "Morgan Stanley (MS)", "American Express (AXP)",
    # --- CONSO ---
    "Walmart (WMT)", "Procter & Gamble (PG)", "Costco Wholesale (COST)",
    "Coca-Cola Company (KO)", "PepsiCo (PEP)", "McDonald's (MCD)",
    "Nike (NKE)", "Starbucks (SBUX)", "Home Depot (HD)", "Walt Disney (DIS)",
    # --- SANTÉ ---
    "Eli Lilly (LLY)", "UnitedHealth Group (UNH)", "Johnson & Johnson (JNJ)",
    "Merck & Co. (MRK)", "AbbVie (ABBV)", "Pfizer (PFE)",
    "Thermo Fisher Scientific (TMO)", "Abbott Laboratories (ABT)",
    # --- INDUSTRIE & ÉNERGIE ---
    "Exxon Mobil (XOM)", "Chevron (CVX)", "General Electric (GE)",
    "Caterpillar (CAT)", "Boeing (BA)", "Lockheed Martin (LMT)", "Honeywell (HON)"
]

def setup_driver():
    """Configure Chrome avec le driver local et options furtives."""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    current_folder = os.getcwd()
    if os.name == 'nt': driver_filename = "chromedriver.exe"
    else: driver_filename = "chromedriver"

    driver_path = os.path.join(current_folder, driver_filename)
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"Driver manquant : {driver_path}")

    service = Service(executable_path=driver_path)
    return webdriver.Chrome(service=service, options=options)

def human_scroll(driver):
    """Simule un humain qui descend la page."""
    print("[SCROLL] Défilement...")
    try:
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, 4):
            driver.execute_script(f"window.scrollTo(0, {total_height * i / 4});")
            time.sleep(random.uniform(0.5, 1.2))
        driver.execute_script("window.scrollBy(0, -300);")
        time.sleep(1)
    except: pass

def close_marketing_popup(driver):
    """Ferme les pubs intrusives."""
    try:
        time.sleep(1.5)
        selectors = [
            "button[aria-label='Close']", "button[class*='close']", 
            "div[class*='modal'] button", "svg[data-icon='times']", 
            ".inf-close-icon", "button#onetrust-close-btn-handler"
        ]
        for selector in selectors:
            try:
                btn = driver.find_element(By.CSS_SELECTOR, selector)
                if btn.is_displayed():
                    btn.click()
                    time.sleep(0.5)
                    return True
            except: continue
    except: pass
    return False

def check_for_captcha(driver):
    """Détecte les blocages via le TITRE."""
    try:
        page_title = driver.title.lower()
        block_words = ["just a moment", "attention required", "security check", "access denied", "verify you are human"]
        
        if any(x in page_title for x in block_words):
            print(f"\n[ALERTE] Captcha détecté (Titre: {driver.title})")
            input(">>> Résolvez le CAPTCHA manuellement puis appuyez sur ENTREE <<<")
            time.sleep(2)
            return True
            
        h1s = [h.text.lower() for h in driver.find_elements(By.TAG_NAME, "h1")]
        if any("challenge" in h or "turnstile" in h for h in h1s):
            print("\n[ALERTE] Captcha détecté (H1)")
            input(">>> Résolvez le CAPTCHA manuellement puis appuyez sur ENTREE <<<")
            return True
            
    except Exception: pass
    return False

def load_existing_data():
    if os.path.exists(CSV_FILENAME):
        try:
            df = pd.read_csv(CSV_FILENAME)
            if df.empty: return [], set()
            records = df.to_dict('records')
            done_set = set(f"{row['company']}_{row['year']}_{row['quarter']}" for row in records)
            print(f"[INFO] Historique chargé : {len(records)} entrées.")
            return records, done_set
        except: return [], set()
    return [], set()

def save_data_safely(data):
    temp = CSV_FILENAME + ".tmp"
    try:
        df = pd.DataFrame(data)
        df.to_csv(temp, index=False)
        os.replace(temp, CSV_FILENAME)
    except Exception as e:
        print(f"[ERREUR SAVE] {e}")

def google_search_quarter_fool(driver, company_full_name, quarter, year):
    search_name = company_full_name.split('(')[0].strip()
    ticker = company_full_name.split('(')[1].replace(')', '').strip()

    query = f'site:fool.com {search_name} {quarter} {year} "Earnings Call Transcript"'
    print(f"[RECHERCHE] {ticker} {quarter} {year}...")

    try:
        driver.get("https://www.google.com")
        # Délai dynamique selon configuration
        time.sleep(random.uniform(*DELAYS['google_search']))
        
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "tout accepter" in btn.text.lower() or "accept all" in btn.text.lower():
                    driver.execute_script("arguments[0].click();", btn)
                    break
        except: pass

        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Délai post-recherche
        time.sleep(random.uniform(*DELAYS['google_search']))
        check_for_captcha(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links_found = []
        
        for h3 in soup.find_all('h3'):
            link_tag = h3.find_parent('a')
            if link_tag and 'href' in link_tag.attrs:
                url = link_tag['href']
                title = h3.get_text()
                
                if "fool.com" not in url: continue
                if "transcript" not in title.lower(): continue
                if quarter.lower() not in title.lower(): continue
                if str(year) not in title: continue
                if ticker.lower() not in title.lower() and search_name.lower() not in title.lower():
                    continue

                links_found.append({
                    "company": company_full_name,
                    "quarter": quarter,
                    "year": year,
                    "title": title,
                    "url": url
                })
        return links_found[:1]

    except Exception as e:
        print(f"[ERREUR GOOGLE] {e}")
        return []

def extract_content_fool(driver, url):
    try:
        driver.get(url)
        # Délai de chargement page selon configuration
        time.sleep(random.uniform(*DELAYS['page_load']))

        try:
            driver.execute_script("""
                var videos = document.querySelectorAll('video, iframe[src*="youtube"], iframe[src*="vimeo"], .video-player');
                videos.forEach(function(v) { v.remove(); });
            """)
        except: pass

        human_scroll(driver)
        check_for_captcha(driver)
        
        try: driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except: pass
        close_marketing_popup(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', id='article-body-transcript')
        if not content: content = soup.find('div', class_='article-body')

        if content:
            for el in content.find_all(string=lambda t: t and "Image source:" in t): el.extract()
            for tag in content.select(".ticker-widget, .promo, script, style, .video-container"):
                tag.decompose()
            
            full_text = content.get_text(separator="\n", strip=True)
            if "Should you invest" in full_text: 
                full_text = full_text.split("Should you invest")[0]
            
            return full_text
            
    except Exception as e:
        print(f"[EXTRACT ERROR] {e}")
    return None

def main():
    print(f"--- Scraping S&P 500 (Mode: {MODE}) ---")
    all_data, done_set = load_existing_data()
    driver = setup_driver()
    
    try:
        for year in TARGET_YEARS:
            print(f"\n>>> TRAITEMENT ANNÉE : {year} <<<\n")
            for company in COMPANIES:
                for quarter in QUARTERS:
                    task_key = f"{company}_{year}_{quarter}"
                    if task_key in done_set: continue 

                    results = google_search_quarter_fool(driver, company, quarter, year)
                    
                    if not results:
                        print(f"[SKIP] Introuvable : {company} {quarter} {year}")
                        time.sleep(1)
                        continue

                    item = results[0]
                    text = extract_content_fool(driver, item['url'])
                    
                    if text and len(text) > 2000:
                        item['content'] = text
                        all_data.append(item)
                        done_set.add(task_key)
                        save_data_safely(all_data)
                        print(f"[OK] {company} {quarter} {year} ({len(text)} cars).")
                    else:
                        print(f"[WARN] Contenu vide/court : {item['title']}")

                    # PAUSE CRITIQUE : C'est ici que se joue l'endurance
                    delay_min, delay_max = DELAYS['inter_request']
                    sleep_time = random.uniform(delay_min, delay_max)
                    print(f"   ... Pause de sécurité de {int(sleep_time)}s ...")
                    time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[STOP] Arrêt manuel. Données sauvegardées.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()