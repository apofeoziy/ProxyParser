import requests
import random
import uuid
from itertools import cycle
import os

# Конфигурация
PROXY_FILE = 'proxy.txt'
USER_AGENTS_FILE = 'user_agents.txt'
URL_FILE = 'url.txt'
BASE_URL = 'https://drive.google.com/drive/folders/'
ERROR_TEXT = '<body><main id="af-error-container" role="main"><a href="//www.google.com"><span id="logo" aria-label="Google" role="img"></span></a><p><b>404.</b> <ins>That’s an error.</ins></p><p>The requested URL was not found on this server. <ins>That’s all we know.</ins></p></main></body>'

def generate_user_agents(num=100):
    """Генерация случайных User-Agent"""
    agents = []
    chrome_versions = range(90, 123)
    firefox_versions = range(90, 121)
    android_versions = [10, 11, 12, 13]
    ios_versions = [14, 15, 16, 17]

    for _ in range(num):
        browser_type = random.choice(['chrome', 'firefox', 'safari', 'mobile'])
        
        if browser_type == 'chrome':
            template = random.choice([
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)}.0.{random.randint(1000, 9999)}. Safari/537.36",
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)}.0.0.0 Safari/537.36",
                f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)}.0.0.0 Safari/537.36",
            ])
        
        elif browser_type == 'firefox':
            template = f"Mozilla/5.0 ({random.choice(['Windows NT 10.0; Win64; x64', 'Macintosh; Intel Mac OS X 10.15', 'X11; Linux x86_64'])}; rv:{random.choice(firefox_versions)}.0) Gecko/20100101 Firefox/{random.choice(firefox_versions)}.0"
        
        elif browser_type == 'safari':
            template = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.choice([15, 16])}.0 Safari/605.1.15"
        
        else:  # mobile
            if random.choice([True, False]):
                template = f"Mozilla/5.0 (Linux; Android {random.choice(android_versions)}; {random.choice(['Mobile', 'Tablet'])}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)}.0.0.0 Mobile Safari/537.36"
            else:
                template = f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.choice(ios_versions)}_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.choice([15, 16])}.0 Mobile/15E148 Safari/604.1"
        
        agents.append(template)
    
    return agents

def load_resources():
    """Загрузка или генерация User-Agents и прокси"""
    # Обработка User-Agents
    user_agents = []
    if os.path.exists(USER_AGENTS_FILE):
        with open(USER_AGENTS_FILE, 'r') as f:
            user_agents = [line.strip() for line in f if line.strip()]
    
    if not user_agents:
        user_agents = generate_user_agents(100)
        print(f"Сгенерировано {len(user_agents)} User-Agents")
    
    # Обработка прокси
    proxies = []
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'r') as f:
            proxies = [line.strip() for line in f if ':' in line.strip()]
    
    return user_agents, cycle(proxies) if proxies else None

# Остальной код без изменений
def generate_uuid():
    while True:
        yield str(uuid.uuid4()).replace('-', '')[:32]

def check_url(session, folder_id, proxy, user_agent):
    try:
        response = session.get(
            BASE_URL + folder_id,
            proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None,
            headers={'User-Agent': user_agent},
            timeout=10
        )
        return ERROR_TEXT not in response.text
    except:
        return False

def main():
    user_agents, proxies = load_resources()
    folder_gen = generate_uuid()
    session = requests.Session()
    
    while True:
        folder_id = next(folder_gen)
        proxy = next(proxies) if proxies else None
        user_agent = random.choice(user_agents)
        
        if check_url(session, folder_id, proxy, user_agent):
            with open(URL_FILE, 'a') as f:
                f.write(BASE_URL + folder_id + '\n')
            print(f'Found valid URL: {BASE_URL}{folder_id}')

if __name__ == '__main__':
    main()