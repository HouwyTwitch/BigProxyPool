import requests
import concurrent.futures
import threading
from tqdm import tqdm
import warnings
from time import sleep
from re import findall

warnings.filterwarnings('ignore')

_LOCK = threading.Lock()
URL_TO_PARSE = 'https://www.xsdaili.cn/dayProxy/ip/{}.html'
THREADS_NUM = 20

START = 4
END = 2100
REGEX = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'

def parse_page(num, f):
    while True:
        try:
            response = requests.get(URL_TO_PARSE.format(str(num)), verify=False)
            proxies = findall(REGEX, response.content.decode(errors='ignore'))
            with _LOCK:
                f.write('\n'.join(proxies) + '\n')
                f.flush()
                break
        except: pass

def main():
    with open('proxies.txt', 'w') as f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS_NUM) as executor:
            futures = [executor.submit(parse_page, d, f) for d in range(START, END+1)]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                future.result()

if __name__ == '__main__':
    main()
    with open('proxies.txt') as f: proxies = list(dict.fromkeys(findall(REGEX, f.read())))
    with open('proxies.txt', 'w') as f: f.write('\n'.join(proxies))