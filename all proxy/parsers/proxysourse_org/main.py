import requests
import concurrent.futures
import threading
from tqdm import tqdm
import warnings
from datetime import datetime, timedelta
from time import sleep
from re import findall

warnings.filterwarnings('ignore')

_LOCK = threading.Lock()
URL_TO_PARSE = 'https://proxysource.org/ru/freeproxies/{}'
THREADS_NUM = 20

START_DATE = '2020-05-01'
END_DATE = '2022-8-26'
START_DATE = datetime.strptime(START_DATE, '%Y-%m-%d')
END_DATE = datetime.strptime(END_DATE, '%Y-%m-%d')
DATE_ARRAY = [START_DATE]
d = START_DATE
REGEX = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
while d != END_DATE:
    d = DATE_ARRAY[-1] + timedelta(days=1)
    DATE_ARRAY.append(d)
for i, elem in enumerate(DATE_ARRAY):
    DATE_ARRAY[i] = elem.strftime("%Y-%m-%d")

def parse_page(str_date, f):
    while True:
        try:
            response = requests.get(URL_TO_PARSE.format(str_date), verify=False)
            proxies = findall(REGEX, response.content.decode(errors='ignore'))
            with _LOCK:
                f.write('\n'.join(proxies) + '\n')
                f.flush()
                break
        except: pass

def main():
    with open('proxies.txt', 'w') as f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS_NUM) as executor:
            futures = [executor.submit(parse_page, d, f) for d in DATE_ARRAY]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                future.result()

if __name__ == '__main__':
    main()
    with open('proxies.txt') as f: proxies = list(dict.fromkeys(findall(REGEX, f.read())))
    with open('proxies.txt', 'w') as f: f.write('\n'.join(proxies))