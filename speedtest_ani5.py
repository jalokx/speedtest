import importlib
import subprocess

# Cek apakah modul tqdm sudah terpasang
try:
    importlib.import_module('alive_progress')
except ImportError:
    # Jika belum terpasang, lakukan instalasi
    subprocess.check_call(["pip", "install", "alive_progress"])
    importlib.import_module('alive_progress')

# Cek apakah modul speedtest-cli sudah terpasang
try:
    importlib.import_module('speedtest')
except ImportError:
    # Jika belum terpasang, lakukan instalasi
    subprocess.check_call(["pip", "install", "speedtest-cli"])
    importlib.import_module('speedtest')

# Cek apakah modul requests sudah terpasang
try:
    importlib.import_module('requests')
except ImportError:
    # Jika belum terpasang, lakukan instalasi
    subprocess.check_call(["pip", "install", "requests"])
    importlib.import_module('requests')

# Cek apakah modul json sudah terpasang
try:
    importlib.import_module('json')
except ImportError:
    # Jika belum terpasang, lakukan instalasi
    subprocess.check_call(["pip", "install", "json"])
    importlib.import_module('json')

import speedtest
import socket
import json
import requests
import time
import shutil
from tqdm import tqdm
from alive_progress import alive_bar

# Mendapatkan informasi IP
ip_info = json.loads(requests.get('https://ipapi.co/json/').text)
ip_address = ip_info['ip']
city = ip_info['city']
country = ip_info['country_name']
isp = ip_info['org']

terminal_width, _ = shutil.get_terminal_size()
bar_width = min(terminal_width - 10, 100) # buat panjang progress bar

# Mendapatkan nama perangkat
device_name = socket.gethostname()

# Menghitung panjang garis putus-putus
dash_line_length = max(len(device_name) + 14, 31)

print()
print('-' * shutil.get_terminal_size().columns)
print(f"\nThis Device: {device_name}")
# print("-"*20)
print("-" * dash_line_length)
print(f"# ISP         : {isp}")
print(f"# IP Address  : {ip_address}")
print(f"# Location    : {city}, {country}\n")

# Mendapatkan informasi server untuk speedtest
# import speedtest

servers = []
threads = None

s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
s.download(threads=threads)
s.upload(threads=threads)
results_dict = s.results.dict()


# ======== Server Mulai dari sini ========
# Get server details
server_download = results_dict["server"]["sponsor"]
server_download_location = results_dict["server"]["name"]
download_server_ip = socket.gethostbyname(results_dict["server"]["url"].split("//")[1].split(":")[0])
dash_line_length = max(len(server_download) + 14, 31)

# Print server details
print(f"Test Server: {server_download}")
print("-" * dash_line_length)
# print("-"*20)
# print(f"# ISP         : {server_download}")
print(f"# IP Address  : {download_server_ip}")
print(f"# Location    : {server_download_location}")

# Lakukan speedtest PING
# ping = round(results_dict["ping"], 2)
# print("\n>> Calculating ping...")
# with tqdm(total=100) as pbar:
#     for i in range(10):
#         s.results.ping
#         time.sleep(0.1)
#         pbar.update(10)

# ping = s.results.ping
print("\n>> Calculating ping...")
ping = round(results_dict["ping"], 2)
# with alive_bar(100, bar = bar_width) as pbar:
with alive_bar(100) as pbar:
    for i in range(100):
        s.results.ping
        time.sleep(0.1)
        pbar()

ping = s.results.ping

# Lakukan speedtest Download
print("\n>> Calculating download speed...")
download_speed = round(results_dict["download"] / 1_000_000, 2)
with alive_bar(100) as pbar:
    for i in range(100):
        s.results.download
        time.sleep(0.1)
        pbar()
# with tqdm(total=100) as pbar:
#     for i in range(10):
#         s.download(threads=threads)
#         time.sleep(0.1)
#         pbar.update(10)
download_speed = s.results.download / 1000000  # dalam Mbps


# Lakukan speedtest Upload
print("\n>> Calculating upload speed...")
upload_speed = round(results_dict["upload"] / 1_000_000, 2)
with alive_bar(100) as pbar:
    for i in range(100):
        s.results.upload
        time.sleep(0.1)
        pbar()
# with tqdm(total=100) as pbar:
#     for i in range(10):
#         s.upload(threads=threads)
#         time.sleep(0.1)
#         pbar.update(10)
upload_speed = s.results.upload / 1000000  # dalam Mbps


# Tampilkan hasil speedtest
print("\nSpeedtest Result:")
print("-"*20)
print(f"# Ping           : {ping:.2f} ms")
if download_speed >= 1024:
    download_speed /= 1024
    print(f"# Download speed : {download_speed:.2f} Gbps")
else:
    print(f"# Download speed : {download_speed:.2f} Mbps")
if upload_speed >= 1024:
    upload_speed /= 1024
    print(f"# Upload speed   : {upload_speed:.2f} Gbps")
else:
    print(f"# Upload speed   : {upload_speed:.2f} Mbps")
print('=' * shutil.get_terminal_size().columns)
print()