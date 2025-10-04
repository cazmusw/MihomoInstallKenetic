#!/usr/bin/env python3

import os
import threading
from concurrent.futures import ThreadPoolExecutor

import dns.resolver
from tqdm import tqdm

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


def log_success(message):
    print(f"{GREEN}[OK]{NC} {message}")

DEFAULT_REGIONS = [
    "bucharest", "finland", "frankfurt", "madrid", "milan", "rotterdam", "stockholm", "warsaw", "russia",
    "brazil", "hongkong", "india", "japan", "singapore", "southafrica", "sydney",
    "us-central", "us-west", "us-east", "us-south",
    "london", "paris", "dubai", "chile", "mexico", "south-korea", "canada",

    # на будущее
    "seattle", "atlanta", "chicago", "newark", "dallas", "miami", "losangeles", "toronto", "santiago",
    "manila", "jakarta", "taiwan", "istanbul", "riyadh", "uae", "auckland"
]
TOTAL_DOMAINS = 18000
PARALLEL_JOBS = int(os.environ.get("PARALLEL_JOBS", min(200, os.cpu_count() * 10)))

ALL_IP_LIST = "./ip-sets/discord-voice-ip-list.text"
HISTORY_FILE = "./ip-sets/discord-voice-ip-history.text"

old_ips = set()
if os.path.isfile(HISTORY_FILE):
    with open(HISTORY_FILE, 'r') as f_in:
        old_ips = set(line.strip() for line in f_in if line.strip())
open(HISTORY_FILE, 'w').close()


def resolve_domain(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return [str(rdata) for rdata in answers]
    except Exception:
        return []

open(ALL_IP_LIST, 'w').close()

iplist = []

for region in tqdm(DEFAULT_REGIONS):
    domains = [f"{region}{i}.discord.gg" for i in range(1, TOTAL_DOMAINS + 1)]

    with ThreadPoolExecutor(max_workers=PARALLEL_JOBS) as executor:
        futures = [executor.submit(resolve_domain, domain) for domain in domains]
        for future in tqdm(futures, ascii=True, desc=f"Parsing Discord {region}: "):
            results = future.result()
            iplist.extend(results)


unique_ips = sorted(set(iplist))
with open(ALL_IP_LIST, 'w') as f_out:
    f_out.write('\n'.join(unique_ips) + '\n')

merged_ips = sorted(set(unique_ips).union(old_ips))

with open(HISTORY_FILE, 'w') as f_out:
    f_out.write('\n'.join(merged_ips) + '\n')

ip_count = 0
if os.path.isfile(ALL_IP_LIST):
    with open(ALL_IP_LIST) as f:
        ip_count = sum(1 for _ in f)

log_success(f'Обновлён список "{YELLOW}{BOLD}{ALL_IP_LIST}{NC}"')
log_success(f"Всего адресов зарезолвили: {MAGENTA}{ip_count}{NC}")
