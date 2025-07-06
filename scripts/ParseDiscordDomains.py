#!/usr/bin/env python3

import os
import sys
import subprocess
import threading
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Цвета
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
BOLD = '\033[1m'
NC = '\033[0m'

lock = threading.Lock()

def line_skip():
    print(". . .")

def log_info(message):
    print(f"{CYAN}[INFO]{NC} {message}")

def log_success(message):
    print(f"{GREEN}[OK]{NC} {message}")

DEFAULT_REGIONS = ["bucharest", "finland", "frankfurt", "madrid", "milan", "rotterdam", "stockholm", "warsaw", "russia"]
TOTAL_DOMAINS = 15000
PARALLEL_JOBS = int(os.environ.get("PARALLEL_JOBS", 500))

ALL_IP_LIST = "./discord-voice-ip-list.text"

def resolve_domain(domain):

    try:
        result = subprocess.run(['dig', '+short', 'A', domain],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=10)
        ips = [line.strip() for line in result.stdout.splitlines()
               if line.strip() and not line.strip().startswith(';;')]

        log_info("Проверяем домен " + domain)

    except subprocess.TimeoutExpired:
        ips = []

    return ips

open(ALL_IP_LIST, 'w').close()

iplist = []

for region in DEFAULT_REGIONS:
    line_skip()

    start_time = time.time()
    start_date = datetime.now().strftime("%d.%m.%Y в %H:%M:%S")

    domains = [f"{region}{i}.discord.gg" for i in range(1, TOTAL_DOMAINS + 1)]
    log_info(f"Резолвим домены региона {region}...")

    with ThreadPoolExecutor(max_workers=PARALLEL_JOBS) as executor:
        futures = [executor.submit(resolve_domain, domain) for domain in domains]
        for future in futures:
            results = future.result()
            iplist.extend(results)



    end_time = time.time()
    execution_time = int(end_time - start_time)

    log_info(f"Время запуска: {MAGENTA}{start_date}{NC}")
    log_info(f"Время выполнения: {MAGENTA}{time.strftime('%H:%M:%S', time.gmtime(execution_time))}{NC}")

iplist.sort()

with open(ALL_IP_LIST, 'a') as f_out:
    f_out.write('\n'.join(iplist) + '\n')

ip_count = 0
if os.path.isfile(ALL_IP_LIST):
    with open(ALL_IP_LIST) as f:
        ip_count = sum(1 for _ in f)

line_skip()
log_success(f'Обновлён список "{YELLOW}{BOLD}{ALL_IP_LIST}{NC}"')
log_success(f"Всего адресов зарезолвили: {MAGENTA}{ip_count}{NC}")
