import requests
import os
import sys
import random
import uuid
import urllib.parse
import hashlib
import json
import base64
import time
import threading
from typing import Tuple, Dict, Any, List
from collections import OrderedDict
from queue import Queue
import secrets
import re
import warnings
import threading
from queue import Queue
import signal
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


version = {
	"aid":"1223",
	"signal":True,
	"region":"IQ",
	"hash":"aea615ab910015038f73c47e4179z17z",
	"active":True
	}
	
print("""
╔══════════════════════════════════════════════════════╗
║     TikTok Device Generator - Proxy Checker         ║            
╚══════════════════════════════════════════════════════╝
    """)
    
class XGorgon:
    @staticmethod
    def generate(params: str, data: str, cookies: str) -> Tuple[str, str]:
        timestamp = int(time.time())
        
        url_md5 = XGorgon._md5_hash(params)
        data_md5 = XGorgon._md5_hash(data) if data else "0"*32
        cookie_md5 = XGorgon._md5_hash(cookies) if cookies else "0"*32
        
        gorgon_hex = XGorgon._calculate_gorgon(url_md5, data_md5, cookie_md5, timestamp)
        
        return f"0404{gorgon_hex}", str(timestamp)
    
    @staticmethod
    def _md5_hash(data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()
    
    @staticmethod
    def _calculate_gorgon(url_md5: str, data_md5: str, cookie_md5: str, timestamp: int) -> str:
        hex_values = []
        
        for i in range(4):
            hex_values.append(int(url_md5[2*i:2*i+2], 16))
        
        for i in range(4):
            hex_values.append(int(data_md5[2*i:2*i+2], 16))
        
        for i in range(4):
            hex_values.append(int(cookie_md5[2*i:2*i+2], 16))
        
        hex_values.extend([0x0, 0x8, 0x10, 0x9])
        
        time_hex = format(timestamp, '08x')
        for i in range(4):
            hex_values.append(int(time_hex[2*i:2*i+2], 16))
        
        magic_bytes = [0x05, 0x00, 0x50, random.randint(0, 255), 0x47, 0x1E, 0x00, random.randint(0, 31) * 8]
        
        s_box = list(range(256))
        j = 0
        for i in range(256):
            a = s_box[i-1] if i > 0 else 0
            b = magic_bytes[i % 8]
            if a == 0x05 and i != 1 and j != 0x05:
                a = 0
            c = (a + i + b) % 256
            j = c if c < i else j
            s_box[i], s_box[c] = s_box[c], s_box[i]
        
        result = [0] * 20
        temp = 0
        for i in range(20):
            if i < len(hex_values):
                a = hex_values[i]
            else:
                a = 0
            
            b = temp
            c = (s_box[i+1] + b) % 256
            temp = c
            d = s_box[c]
            s_box[i+1] = d
            
            e = (d * 2) % 256
            f = s_box[e]
            
            result[i] = a ^ f
        
        for i in range(20):
            a = result[i]
            b = ((a & 0xF) << 4) | ((a & 0xF0) >> 4)
            c = result[(i+1) % 20]
            d = b ^ c
            e = int(bin(d)[2:].zfill(8)[::-1], 2)
            f = e ^ 20
            g = (~f + (1 << 32)) & 0xFF
            result[i] = g
        
        hex_result = ''.join([format(x, '02x') for x in result])
        magic_hex = ''.join([format(x, '02x') for x in [magic_bytes[7], magic_bytes[3], magic_bytes[1], magic_bytes[6]]])
        
        return f"{magic_hex}{hex_result}"


class XLadon:
    @staticmethod
    def encrypt(khronos: int, lc_id: str = "1611921764", aid: str = "1233") -> str:
        def _ror(value: int, count: int, bits: int = 64) -> int:
            count %= bits
            return ((value >> count) | (value << (bits - count))) & ((1 << bits) - 1)
        
        random_bytes = os.urandom(4)
        data = f"{khronos}-{lc_id}-{aid}"
        
        key = random_bytes + aid.encode()
        key_md5 = hashlib.md5(key).digest()
        
        hash_table = bytearray(272)
        hash_table[:32] = key_md5
        
        v0 = int.from_bytes(key_md5[:8], 'little')
        v1 = int.from_bytes(key_md5[8:16], 'little')
        v2 = int.from_bytes(key_md5[16:24], 'little')
        v3 = int.from_bytes(key_md5[24:32], 'little')
        
        temp_values = [v2, v3]
        
        for i in range(34):
            x = v0
            y = v1
            y = _ror(y, 8)
            y = (y + x) & ((1 << 64) - 1)
            y = y ^ i
            temp_values.append(y)
            y = y ^ _ror(x, 61)
            
            start_idx = (i + 1) * 8
            hash_table[start_idx:start_idx+8] = y.to_bytes(8, 'little')
            
            v0 = y
            v1 = temp_values.pop(0)
        
        data_bytes = data.encode()
        padded_size = (len(data_bytes) + 15) // 16 * 16
        padded_data = bytearray(padded_size)
        padded_data[:len(data_bytes)] = data_bytes
        
        pad_value = 16 - (len(data_bytes) % 16)
        for i in range(pad_value):
            padded_data[len(data_bytes) + i] = pad_value
        
        encrypted = bytearray(padded_size)
        
        for i in range(0, padded_size, 16):
            block = padded_data[i:i+16]
            
            d0 = int.from_bytes(block[:8], 'little')
            d1 = int.from_bytes(block[8:], 'little')
            
            for j in range(34):
                hash_val = int.from_bytes(hash_table[j*8:j*8+8], 'little')
                d1 = (hash_val ^ (d0 + _ror(d1, 8))) & ((1 << 64) - 1)
                d0 = (d1 ^ _ror(d0, 61)) & ((1 << 64) - 1)
            
            encrypted[i:i+8] = d0.to_bytes(8, 'little')
            encrypted[i+8:i+16] = d1.to_bytes(8, 'little')
        
        output = bytearray(padded_size + 4)
        output[:4] = random_bytes
        output[4:] = encrypted
        
        return base64.b64encode(output).decode()


class TikTokSignature:
    @staticmethod
    def generate_signatures(params: str, payload: dict, cookies: dict) -> dict:
        cookies_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
        payload_str = json.dumps(payload) if isinstance(payload, dict) else str(payload)        
        x_gorgon, x_khronos = XGorgon.generate(params, payload_str, cookies_str)
        x_ladon = XLadon.encrypt(int(x_khronos))        
        stub = hashlib.md5(payload_str.encode()).hexdigest().upper()        
        timestamp = int(time.time())        
        return {
            'X-Gorgon': x_gorgon,
            'X-Khronos': x_khronos,
            'X-Ladon': x_ladon,
            'x-ss-stub': stub,            
            'x-ss-req-ticket': str(timestamp * 1000)
        }


class TikTokDevice:
    def __init__(self):
        self.device_id = None
        self.install_id = None
        
        self.mac_address = self._generate_unique_mac()
        self.cdid = str(uuid.uuid4())
        
        self.did_c = str(random.randint(100000000000000, 999999999999999))
        self.openudid = str(random.randint(1000000000000000, 9999999999999999))
        
        android_versions = [
            ("4.4", 19), ("5.0", 21), ("5.1", 22), ("6.0", 23), 
            ("7.0", 24), ("7.1", 25), ("8.0", 26), ("8.1", 27),
            ("9.0", 28), ("10.0", 29), ("11.0", 30), ("12.0", 31),
            ("13.0", 33)
        ]
        selected_version = random.choice(android_versions)
        self.osversion = selected_version[0]
        self.os_api = selected_version[1]
        
        app_versions = [
            ("19.3.3", "2021903030"),
            ("20.1.2", "2022001020"),
            ("21.4.5", "2022104050"),
            ("22.6.7", "2022206070"),
            ("23.8.9", "2022308090"),
            ("24.1.0", "2022401000"),
            ("25.2.3", "2022502030"),
            ("26.4.5", "2022604050"),
            ("27.1.0", "2022701000"),
            ("28.0.0", "2022800000")
        ]
        selected_app = random.choice(app_versions)
        self.appversion = selected_app[0]
        self.version_code = selected_app[1]
        
        devices = [
            ("samsung", "Galaxy S22 Ultra", "SM-S908B"),
            ("samsung", "Galaxy S21", "SM-G991B"),
            ("samsung", "Galaxy A52", "SM-A525F"),
            ("xiaomi", "Mi 11", "M2011K2G"),
            ("xiaomi", "Redmi Note 10", "M2101K7AG"),
            ("xiaomi", "Poco X3", "M2007J20CG"),
            ("huawei", "P40 Pro", "ELS-NX9"),
            ("huawei", "Mate 30 Pro", "LIO-NX9"),
            ("oneplus", "9 Pro", "LE2123"),
            ("oneplus", "8T", "KB2003"),
            ("oppo", "Find X3 Pro", "CPH2173"),
            ("oppo", "Reno 6", "CPH2235"),
            ("vivo", "X70 Pro", "V2105"),
            ("realme", "GT Neo2", "RMX3370"),
            ("google", "Pixel 6 Pro", "GLU0G"),
            ("motorola", "Edge 20", "XT2143-1"),
            ("nokia", "G50", "TA-1394"),
            ("sony", "Xperia 1 III", "XQ-BC52"),
            ("lg", "Wing", "LM-F100N")
        ]
        selected_device = random.choice(devices)
        self.device_brand = selected_device[0]
        self.device_model = selected_device[1]
        self.device_code = selected_device[2]
        
        self.aid = "1233"
        
        regions = ["US", "GB", "DE", "FR", "IT", "ES", "JP", "KR", "RU", "BR", "IN", "AE", "SA", "EG", "TR", "IQ", "JO", "LB", "SY"]
        self.region = random.choice(regions)
        
        timezones = {
            "US": "America/New_York",
            "GB": "Europe/London", 
            "DE": "Europe/Berlin",
            "FR": "Europe/Paris",
            "IT": "Europe/Rome",
            "JP": "Asia/Tokyo",
            "KR": "Asia/Seoul",
            "RU": "Europe/Moscow",
            "AE": "Asia/Dubai",
            "SA": "Asia/Riyadh",
            "EG": "Africa/Cairo",
            "TR": "Europe/Istanbul",
            "IQ": "Asia/Baghdad"
        }
        self.timezone = timezones.get(self.region, "Asia/Dubai")
        
        languages = {
            "US": "en",
            "GB": "en",
            "DE": "de",
            "FR": "fr", 
            "IT": "it",
            "ES": "es",
            "JP": "ja",
            "KR": "ko",
            "RU": "ru",
            "BR": "pt",
            "IN": "hi",
            "AE": "ar",
            "SA": "ar",
            "EG": "ar",
            "TR": "tr",
            "IQ": "ar",
            "JO": "ar",
            "LB": "ar",
            "SY": "ar"
        }
        self.lang = languages.get(self.region, "en")
        
        dpis = ["240", "320", "480", "560", "640"]
        self.dpi = random.choice(dpis)
        
        resolutions = [
            "720x1280", "1080x1920", "1080x2340", "1440x2560",
            "1440x3040", "1440x3120", "1080x2400", "1176x2400"
        ]
        self.resolution = random.choice(resolutions)
        
        self.build = f"{self.device_code}.{random.randint(1, 9)}"
        
        self.host_list = [
            'rtlog19-normal.tiktokv.com', 'rtlog19-normal-alisg.tiktokv.com',
            'rtlog19-normal-zr.tiktokv.com', 'rtlog19-normal-zr-alisg.tiktokv.com',
            'rtlog22-normal-zr.tiktokv.com', 'rtlog22-normal-zr-alisg.tiktokv.com',
            'log16-normal.tiktokv.com', 'log16-normal-alisg.tiktokv.com',
            'log16-normal-zr.tiktokv.com', 'log16-normal-zr-alisg.tiktokv.com',
            'rtlog17-normal.tiktokv.com', 'rtlog17-normal-alisg.tiktokv.com',
            'log.tiktokv.com', 'log22-normal.tiktokv.com',
            'log22-normal-alisg.tiktokv.com', 'rtlog32-normal-zr.tiktokv.com',
            'rtlog32-normal-zr-alisg.tiktokv.com', 'log-va.tiktokv.com',
            'rtlog31-normal-zr.tiktokv.com', 'rtlog31-normal-zr-alisg.tiktokv.com',
            'log15-normal.tiktokv.com', 'log15-normal-alisg.tiktokv.com',
            'rtlog31-normal.tiktokv.com', 'rtlog31-normal-alisg.tiktokv.com',
            'rtlog-va.tiktokv.com', 'rtlog16-normal.tiktokv.com',
            'rtlog16-normal-alisg.tiktokv.com', 'log31-normal.tiktokv.com',
            'log31-normal-alisg.tiktokv.com', 'rtlog15-normal.tiktokv.com',
            'rtlog15-normal-alisg.tiktokv.com', 'log31-normal-zr.tiktokv.com',
            'log31-normal-zr-alisg.tiktokv.com', 'log16-normal-c-useast2a.ttapis.com',
            'rtlog16-normal-zr.tiktokv.com', 'rtlog16-normal-zr-alisg.tiktokv.com',
            'log19-normal-zr.tiktokv.com', 'log19-normal-zr-alisg.tiktokv.com',
            'log22-normal-zr.tiktokv.com', 'log22-normal-zr-alisg.tiktokv.com',
            'log23-normal-zr.tiktokv.com', 'log23-normal-zr-alisg.tiktokv.com',
            'rtlog.tiktokv.com', 'log19-normal.tiktokv.com',
            'log19-normal-alisg.tiktokv.com', 'log17-normal.tiktokv.com',
            'log17-normal-alisg.tiktokv.com', 'log32-normal-zr.tiktokv.com',
            'log32-normal-zr-alisg.tiktokv.com', 'mcs-va.tiktokv.com',
            'mcs-sg.tiktokv.com', 'rtlog22-normal.tiktokv.com',
            'log32-normal.tiktokv.com', 'log32-normal-alisg.tiktokv.com',
            'rtlog23-normal-zr.tiktokv.com', 'rtlog23-normal-zr-alisg.tiktokv.com',
            'aggr32-normal.tiktokv.com', 'log16-normal-useast1a.tiktokv.com',
            'log19-normal-useast1a.tiktokv.com', 'log22-normal-useast1a.tiktokv.com',
            'log31-normal-useast1a.tiktokv.com', 'log32-normal-useast1a.tiktokv.com'
        ]
        self.host = list(OrderedDict.fromkeys(self.host_list))
        
        self.session = requests.Session()
        self.session.verify = False
        self.running = True
    
    def _generate_unique_mac(self):
        oui_list = [
            "00:1A:11", "00:23:45", "00:50:56", "00:0C:29", "00:1B:44",
            "00:1C:42", "00:1D:72", "00:1E:68", "00:1F:29", "00:21:5A",
            "00:22:64", "00:24:E8", "00:25:64", "00:26:5D", "00:27:19"
        ]
        manufacturer = random.choice(oui_list)
        random_octets = ":".join([f"{random.randint(0, 255):02X}" for _ in range(3)])
        return f"{manufacturer}:{random_octets}"
        
    def __intxlog__(self,device_data):
    	params = {
    	     "mac"    :_generate_unique_mac(),
    	     "a1"     :device_data["device_id"],   
    	     "a2"     :device_data["install_id"],
    	     "a3"     :device_data["server_time"],
    	     "h"      :self.host,
    	     "fp"     :secrets.token_hex(15),
    	     "ccw"    :-1,    	     
    	     "t"      :int(time.time())*2,
    	     "p"      :self.req_params(),
    	     "ca"     : 310,                
           "hos_abi": "armeabi-v7a",
    	     "string":{
    	     	"wifi":"mobile",
    	     	"httpx":"False",
    	     	"download":"False",
    	     	"verify":"True",
    	     	},
    	     	"paradox":"",
    	     	}
    	     
    	     
    	params["sig"] == version["hash"]
    	params["aid"] == version["aid"]
    	response = self.session.post("https://xlog-va.byteoversea.com/v2/active/?",params=params)
    	if response.json()["data"]["is_activated"] == 1:
    		return True
    def xlog_verify(self, device_data):
        try:
            params = {
               "device_id"     : str(device_data["device_id"]),
               "install_id"    : str(device_data["install_id"]),
               "did": str(device_data["device_id"]),
               "verify_host"   : random.choice(self.host),
               "sdk-version"   : "1",
               "verify_url"    : "xlog_v5",
               "mc"            : str(self.mac_address),
               "server_time"   :  str(device_data.get("server_time", int(time.time()))),
               "msToken"       : "Cilent",
               "version_code"  : str(self.version_code),
               "device_type"   : str(self.device_model),
               "device_brand"  : str(self.device_brand),
               "os"            : "0.6",
               "region"        : str(self.region),
               "proxy": "1"
            }
            
            response = self.session.get('https://xlog-va.byteoversea.com/v2/xlog_devices?', params=params,timeout=10).text
            url = f"https://applog.musical.ly/service/2/app_alert_check/?iid={device_data['install_id']}&device_id={device_data['device_id']}&version_code=16.9.4"
            headers = {
                    "accept-encoding": "gzip",
                    "x-ss-req-ticket": str(int(time.time())) + "000",
                    "sdk-version"    : "1",
                    "user-agent"     : "okhttp/3.10.0.1",
                }
            response2 = self.session.get(url, headers=headers, timeout=10)
            response_json = response2.json()
            if response_json['message'] == "success": 
            	return True            	                                                                                                                                                                                                    
            return False
        except Exception as e:
            return False
    def http_requests(self, proxy) -> bool:
        try:
            payload_data = self.req_payload()
            params_str = self.req_params()
            cookies_dict = self.req_cookies()
            headers_dict = self.req_headers()
            
            if not all([params_str, cookies_dict, headers_dict, payload_data]):
                return False
            
            host = random.choice(self.host)
            url = f"http://{host}/service/2/device_register/?{params_str}"
            headers_dict['host'] = host
            
            proxies = {
                "http": f"http://{proxy}", 
                "https": f"http://{proxy}"
            }
            
            response = requests.post(
                url, 
                headers=headers_dict, 
                cookies=cookies_dict, 
                data=payload_data, 
                proxies=proxies,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)
                    if 'device_id' in data and int(data['device_id']) > 0:
                        self.device_id = data['device_id']
                        self.install_id = data['install_id']
                        device_data = data
                        
                                               
                        result_data = {
                            "device_id": str(data["device_id"]),
                            "install_id": str(data["install_id"]),
                            "device_brand": self.device_brand,
                            "device_model": self.device_model,
                            "os_version": self.osversion,
                            "app_version": self.appversion,
                            "region": self.region,
                            "xlog_activated":self.xlog_verify(device_data),
                            "proxy": proxy,
                            "timestamp": int(time.time()),
                            "cdid": self.cdid,
                            "openudid": self.openudid,
                            "device_data": {
                                "resolution": self.resolution,
                                "dpi": self.dpi,
                                "language": self.lang,
                                "timezone": self.timezone,
                                "build": self.build
                            }
                        }
                        
                        with open("devices_active.txt", "a", encoding="utf-8") as f:
                            json.dump(result_data, f)
                            f.write("\n")
                        
                        return True
                except Exception as e:
                    return False
        except Exception as e:
            pass
        
        return False
    
    def req_payload(self) -> str:
        serial_number = f'{random.randint(1,9)}{random.randint(1,9)}{random.randint(1,9)}{random.randint(1,9)}{random.randint(1,9)}'
        build_serial = f'{random.randint(1000000, 9999999)}'
        display_name = random.choice(["musical_ly", "tiktok", "tiktoklite"])
        
        carrier_choices = ["Vodafone", "Verizon", "AT&T", "T-Mobile", "Orange", "EE", "O2", "Telefonica", "Deutsche Telekom", "Etisalat", "STC", "Zain"]
        carrier = random.choice(carrier_choices)
        
        return json.dumps({
            "header": {
                "serial_number"       : serial_number,
                "display_density"     : "mdpi",
                "tz_name"             : self.timezone,
                "resolution"          : self.resolution.replace('x', '/'),
                "timezone"            : "1",
                "carrier"             : carrier,
                "sim_serial_number"   : [],
                "rom_version"         : self.build,
                "density_dpi"         : self.dpi,
                "device_brand"        : self.device_brand,
                "manifest_version_code": self.version_code,
                "device_manufacturer" : self.device_brand,
                "clientudid"          : self.did_c,
                "openudid"            : self.openudid,
                "update_version_code" : self.version_code,
                "os_api"              : str(self.os_api),
                "display_name"        : display_name,
                "app_version"         : self.appversion,
                "version_code"        : str(self.appversion).replace(".", "0"),
                "mc"                  : self.mac_address,
                "language"            : self.lang,
                "build_serial"        : build_serial,
                "device_model"        : self.device_model,
                "google_aid"          : self.cdid,
                "region"              : self.region,
                "package"             : "com.zhiliaoapp.musically",
                "tz_offset"           : "3600",
                "sim_region"          : self.region.lower(),
                "access"              : random.choice(["wifi", "mobile"]),
                "os_version"          : self.osversion,
                "sdk_version"         : str(random.randint(2, 5)),
                "cpu_abi"             : random.choice(["armeabi-v7a", "arm64-v8a"]),
                "aid"                 : self.aid,
                "os"                  : "Android",
                "not_request_sender"  : 0,
                "channel"             : random.choice(["googleplay", "wandoujia", "huawei", "xiaomi"])
            },
            "_gen_time": int(time.time()),
            "magic_tag": "ss_app_log"
        })
    
    def req_cookies(self) -> Dict[str, str]:
        current_time = int(time.time())
        
        cookies = {}
        cookies['passport_csrf_token'] = secrets.token_hex(16) + secrets.token_hex(8)
        cookies['passport_csrf_token_default'] = secrets.token_hex(16)
        cookies['tiktok_webapp_theme'] = random.choice(['dark', 'light'])
        cookies['cookie-consent'] = '{"ga":true,"af":true,"fbp":true,"lip":true,"bing":true,"ttads":true,"reddit":true,"version":"v8"}'
        cookies['_ttp'] = secrets.token_hex(16)
        
        user_unique_id = secrets.token_hex(16)
        cookies['__tea_cache_tokens_1988'] = f'{{"user_unique_id":"{user_unique_id}","timestamp":{current_time},"_type_":"default"}}'
        
        cookies['passport_auth_status'] = secrets.token_hex(32)
        cookies['passport_auth_status_ss'] = secrets.token_hex(32)
        cookies['tt_csrf_token'] = secrets.token_hex(16)
        cookies['tt_chain_token'] = secrets.token_hex(8) + "=="
        
        abck_parts = [
            secrets.token_hex(16).upper(),
            "~0~YAAQ",
            secrets.token_hex(40),
            secrets.token_hex(40),
            secrets.token_hex(40),
            secrets.token_hex(40),
            "~-1~-1~-1"
        ]
        cookies['_abck'] = ''.join(abck_parts)
        
        bm_sz_parts = [
            secrets.token_hex(16).upper(),
            "~YAAQ",
            secrets.token_hex(40),
            secrets.token_hex(40),
            secrets.token_hex(40),
            secrets.token_hex(40),
            f"~{random.randint(4000000, 5000000)}~{random.randint(4000000, 5000000)}"
        ]
        cookies['bm_sz'] = ''.join(bm_sz_parts)
        
        ak_bmsc_parts = [
            secrets.token_hex(16).upper(),
            "~000000000000000000000000000000~YAAQ",
            secrets.token_hex(100),
            secrets.token_hex(100),
            secrets.token_hex(100),
            secrets.token_hex(100)
        ]
        cookies['ak_bmsc'] = ''.join(ak_bmsc_parts)
        
        sid_guard_time = current_time - random.randint(0, 86400)
        cookies['sid_guard'] = f'{secrets.token_hex(16)}|{sid_guard_time}|21600|Fri,+23-Dec-2022+17:14:48+GMT'
        
        cookies['uid_tt'] = secrets.token_hex(16)
        cookies['uid_tt_ss'] = secrets.token_hex(16)
        cookies['sid_tt'] = secrets.token_hex(16)
        cookies['sessionid'] = secrets.token_hex(32)
        cookies['sessionid_ss'] = secrets.token_hex(32)
        
        ucp_token = secrets.token_hex(32)
        cookies['sid_ucp_v1'] = f'1.0.0-{base64.b64encode(ucp_token.encode()).decode()}'
        cookies['ssid_ucp_v1'] = f'1.0.0-{base64.b64encode(ucp_token.encode()).decode()}'
        
        bm_sv_parts = [
            secrets.token_hex(16).upper(),
            "~YAAQ",
            secrets.token_hex(40),
            "~1"
        ]
        cookies['bm_sv'] = ''.join(bm_sv_parts)
        
        return cookies
    
    def req_params(self) -> str:
        return urllib.parse.urlencode({
            "ac"               : random.choice(["wifi", "mobile"]),   
            "channel"          : random.choice(["googleplay", "huawei", "xiaomi", "oppo", "vivo"]),
            "aid"              : self.aid,
            "app_name"         : random.choice(["musical_ly", "tiktok"]),
            "version_code"     : str(self.appversion).replace('.', '0'),
            "version_name"     : self.appversion,
            "device_platform"  : "android",
            "ab_version"       : self.appversion,
            "ssmix"            : "a",
            "device_type"      : self.device_model,
            "device_brand"     : self.device_brand,
            "language"         : self.lang,
            "os_api"           : str(self.os_api),
            "os_version"       : self.osversion,
            "openudid"         : self.openudid,
            "manifest_version_code": self.version_code,
            "resolution"       : self.resolution.replace('x', '*'),
            "dpi"              : self.dpi,
            "update_version_code": self.version_code,
            "_rticket"         : str(int(time.time())) + str(random.randint(100, 999)),
            "app_type"         : "normal",
            "sys_region"       : self.region,
            "timezone_name"    : self.timezone,
            "ts"               : int(time.time()),
            "timezone_offset"  : str(random.choice([3600, 7200, 10800, -14400, -18000])),
            "build_number"     : self.appversion,
            "region"           : self.region,
            "uoo"              : "1",
            "app_language"     : self.lang,
            "locale"           : f"{self.lang}-{self.region}",
            "op_region"        : self.region,
            "ac2"              : random.choice(["wifi", "mobile"]),
            "cdid"             : self.cdid
        })
    
    def req_headers(self):
        builds = [
            'RP1A.200720.012', 'SP1A.210812.016', 'TP1A.220624.014',
            'RQ3A.210805.001', 'SQ3A.220705.003', 'TQ3A.230805.001'
        ]
        
        headers = {
            "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android {self.osversion}; {self.device_model} Build/{random.choice(builds)})",
            "Connection": "Keep-Alive",
            "X-Tt-Dm-Status": "login=1;ct=1;rt=1",
            "X-Tt-Trace-Id": hashlib.md5(str(uuid.uuid4()).encode()).hexdigest(),
            "X-Tt-Request-Tag": f"t={time.time()}",
            "X-Tt-Store-ID": str(random.randint(10000, 99999)),
            "X-Tt-Env": "boe_tiktok_ttserver_aweme_me",
            "X-Tt-Token": "",
            "X-Vc-Bdturing-Sdk-Version": "2.2.1",
            "X-Bd-Kmsv": "1",
            "Passport-Sdk-Version": "19",
            "Sdk-Version": "2"
        }
        
        headers.update(TikTokSignature.generate_signatures(
            params=self.req_params(),
            payload=json.loads(self.req_payload()),
            cookies=self.req_cookies()
        ))
        
        return headers




class ProxyManager:
    def __init__(self, max_threads: int = 200, max_proxies: int = 100000):
        self.running = True
        self.count = 0
        self.success = 0
        self.failed = 0
        self.max_proxies = max_proxies
        self.max_threads = max_threads
        self.checked_proxies = set()
        self.proxy_queue = Queue()
        self.working_proxies = []
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.nno = TikTokDevice()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=2000",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt",
            "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.proxy-list.download/api/v1/get?type=https",
            "https://api.openproxylist.xyz/http.txt",
            "https://api.openproxylist.xyz/https.txt",
            "https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=2000&page=1&sort_by=lastChecked&sort_type=desc",
            "https://proxylist.geonode.com/api/proxy-list?protocols=https&limit=2000&page=1&sort_by=lastChecked&sort_type=desc",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
            "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/ProxyScraper/ProxyScrape/main/proxies.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=text",
            "https://openproxylist.xyz/http.txt",
            "https://openproxylist.xyz/https.txt",
            "https://multiproxy.org/txt_all/proxy.txt",
            "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
            "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
            "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/http/global/http_checked.txt",
            "https://spys.me/proxy.txt",
            "https://www.proxy-list.download/api/v0/get?l=en&t=http",
            "https://www.proxy-list.download/api/v0/get?l=en&t=https",
            "https://api.proxyscrape.com/proxytable.php",
            "http://pubproxy.com/api/proxy?limit=50&format=txt",
            "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/https.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/https.txt",
            "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/https.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/https.txt",
            "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTP.txt",
            "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTPS.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/https.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/https.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/proxy-list.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/proxy_list.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy-list.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt",
            "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/all/global/all_checked.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/all.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/all.txt",
        ]

    def signal_handler(self, sig, frame):      
        self.running = False
        self.print_stats()
        sys.exit(0)

    def proxy_stringers(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', response.text)
                with self.lock:
                    for proxy in proxies:
                        if self.count < self.max_proxies and proxy not in self.checked_proxies:
                            self.proxy_queue.put(proxy)
                            self.checked_proxies.add(proxy)
                            self.count += 1
        except Exception:
            pass

    def proxies_all(self):              
        threads = []
        for url in self.proxy_sources:
            if not self.running:
                break
                
            thread = threading.Thread(target=self.proxy_stringers, args=(url,))
            threads.append(thread)
            thread.start()
            
            if len(threads) >= 10:
                for t in threads:
                    t.join(timeout=5)
                threads = []
                
            
        
        for thread in threads:
            thread.join(timeout=5)
        
        

    def process_proxy(self, proxy):
        try:
            result = self.nno.http_requests(proxy)
            with self.lock:
                if result:
                    self.success += 1
                    self.working_proxies.append(proxy)
                else:
                    self.failed += 1
                    
                self.print_stats()
                    
                
                    
        except Exception:
            with self.lock:
                self.failed += 1

    def print_stats(self):        
        print(f"\r[+] Success: {self.success} | Failed: {self.failed} | Total: {self.count} | Proxies : {self.count}",end="", flush=True)

    def check_proxies(self):
        self.proxies_all()
        
        if self.count == 0:
            exit("[-] No proxies found")
            
        
            
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            while self.running:
                try:
                    if self.proxy_queue.empty():
                        time.sleep(1)
                        continue
                    
                    proxy = self.proxy_queue.get(timeout=2)
                    future = executor.submit(self.process_proxy, proxy)
                    futures.append(future)
                    
                    if len(futures) >= 1000:
                        for f in as_completed(futures):
                            try:
                                f.result(timeout=30)
                            except:
                                pass
                        futures = futures
                        
                except Exception:
                    if not self.running:
                        break
                    
            
            for future in as_completed(futures):
                try:
                    future.result(timeout=10)
                except:
                    pass
        
        
        
        return self.working_proxies

    def get_proxies(self):
        try:                                    	               
            
            return self.check_proxies()
        except KeyboardInterrupt:            
            self.running = False
            return self.working_proxies
        except Exception as e:           
            return self.working_proxies
    
    
            

def main():
    try:                     
        proxy_manager = ProxyManager(
            max_threads=300,
            max_proxies=200000
        )
        
        proxy_manager.get_proxies()
    except KeyboardInterrupt:
        pass
        

if __name__ == "__main__":
    main()
