import requests
import concurrent.futures
import threading
from tkinter import Tk, filedialog
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

_LOCK = threading.Lock()
TIMEOUT = 5
RETRY = 2
URL_TO_CHECK = 'https://inventories.cs.money/5.0/load_bots_inventory/730?isMarket=false&limit=60&maxPrice=0.01&offset=0&priceWithBonus=30&sort=botFirst&sticker=ib%20h%20ka%2014&withStack=true'
THREADS_NUM = 250

root = Tk()
root.withdraw()

def check_proxy(proxy, f):
    try:
        for _ in range(RETRY):
            response = requests.get(URL_TO_CHECK, proxies={'https': proxy}, timeout=TIMEOUT, verify=False)
            if response.status_code in (200, 429):
                with _LOCK:
                    f.write(proxy + '\n')
                    f.flush()
                break
    except: pass

def main():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    with open(file_path, 'r') as f: proxies = [line.strip() for line in f]
    with open('working_proxies.txt', 'w') as f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS_NUM) as executor:
            futures = [executor.submit(check_proxy, proxy, f) for proxy in proxies]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                future.result()

if __name__ == '__main__': main()