import random
import re
from PyRoxy import ProxyChecker, ProxyUtiles
from colorama import Fore, init
import requests

prx = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/https/data.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/elliottophellia/proxylist/refs/heads/master/results/http/global/phttp_checked.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/http_proxies.txt",
    "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/refs/heads/main/http.txt"
]
session = requests.Session()
init()

all_proxies = set()

send = 0
for url in prx:
    send += 1
    try:
        req_text = session.get(url, timeout=10).text
        req_list = re.sub(r"^\s+|\s+$", "", re.sub(r"^\s*$\n?", "", req_text, flags=re.MULTILINE), flags=re.MULTILINE).splitlines()

        processed_proxies = []
        if "socks5" in url:
            processed_proxies = ["socks5://" + prox.lstrip("socks5://") for prox in req_list]
        elif "socks4" in url:
            processed_proxies = ["socks4://" + prox.lstrip("socks4://") for prox in req_list]
        elif "https_proxies" in url or "/https/" in url:
            processed_proxies = ["https://" + prox.lstrip("https://") for prox in req_list]
        elif "http" in url:
            processed_proxies = ["http://" + prox.lstrip("http://") for prox in req_list]

        all_proxies.update(processed_proxies)
        print(Fore.YELLOW + f"[{send}]" + Fore.GREEN, url, f"| {len(req_list)}" + Fore.RESET)
    except:
        print(Fore.YELLOW + f"[{send}]" + Fore.RED, f"FAIL {url}" + Fore.RESET)

total = len(all_proxies)
print(Fore.BLUE + f"total {total}\n" + Fore.RESET)

naxui = random.randint(1000, 9999)
temp_file = f"bazadian{naxui}.txt"

with open(temp_file, "w", encoding="utf-8") as f:
    f.write("\n".join([re.sub(r"^(([^:]+:){2}[^:]+):.*$", r"\1", prox) for prox in all_proxies]) + "\n")

proxies = ProxyUtiles.readFromFile(temp_file)
result = ProxyChecker.checkAll(proxies)

blyat = "eax"
with open(f"{blyat}.txt", "a", encoding="utf-8") as f:
    for proxy in result:
        f.write(f"{proxy.type.name.lower()}://{proxy.host}:{proxy.port}\n")

with open(f"{blyat}.txt", encoding="utf-8") as f:
    print(Fore.RED + f"file {blyat}.txt | success {len(f.readlines()) - 1}" + Fore.RESET)
