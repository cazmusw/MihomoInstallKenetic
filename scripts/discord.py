#!/usr/bin/env python3

import os
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import socket
import time
from tqdm.asyncio import tqdm as atqdm

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
BOLD = '\033[1m'
NC = '\033[0m'


def log_success(message):
    print(f"{GREEN}[OK]{NC} {message}")


DEFAULT_REGIONS = [
    "bucharest", "finland", "frankfurt", "madrid", "milan", "rotterdam",
    "stockholm", "warsaw", "russia", "brazil", "hongkong", "india", "japan",
    "singapore", "southafrica", "sydney", "us-central", "us-west", "us-east",
    "us-south", "london", "paris", "dubai", "chile", "mexico", "south-korea",
    "canada", "seattle", "atlanta", "chicago", "newark", "dallas", "miami",
    "losangeles", "toronto", "santiago", "manila", "jakarta", "taiwan",
    "istanbul", "riyadh", "uae", "auckland"
]

TOTAL_DOMAINS = 18000
PARALLEL_JOBS = os.cpu_count() * 40
ALL_IP_LIST = "./ip-sets/discord-voice-ip-list.text"
HISTORY_FILE = "./ip-sets/discord-voice-ip-history.text"

dns_executor = ThreadPoolExecutor(max_workers=PARALLEL_JOBS)


def blocking_resolve(domain):
    try:
        result = socket.getaddrinfo(domain, None, socket.AF_INET)
        return [item[4][0] for item in result]
    except (socket.gaierror, OSError):
        return []


async def resolve_domain_async(domain):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(dns_executor, blocking_resolve, domain)


async def resolve_batch_fast(domains):
    tasks = [resolve_domain_async(domain) for domain in domains]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    ips = []
    for result in results:
        if isinstance(result, list):
            ips.extend(result)
    return ips


async def process_region(region, semaphore, pbar):
    batch_size = 50
    domains = [f"{region}{i}.discord.gg" for i in range(1, TOTAL_DOMAINS + 1)]

    all_ips = []

    async with semaphore:
        for i in range(0, len(domains), batch_size):
            batch = domains[i:i + batch_size]
            try:
                ips = await asyncio.wait_for(
                    resolve_batch_fast(batch),
                    timeout=5.0
                )
                all_ips.extend(ips)
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                pass

            pbar.update(len(batch))

    return all_ips


async def main():
    start_time = time.time()

    old_ips = set()
    if os.path.exists(HISTORY_FILE):
        try:
            async with aiofiles.open(HISTORY_FILE, 'r') as f:
                async for line in f:
                    ip = line.strip()
                    if ip:
                        old_ips.add(ip)
        except:
            pass

    async with aiofiles.open(HISTORY_FILE, 'w') as f:
        pass

    semaphore = asyncio.Semaphore(min(10, len(DEFAULT_REGIONS)))

    total_domains = len(DEFAULT_REGIONS) * TOTAL_DOMAINS

    with atqdm(total=total_domains, desc=">> DNS access", unit=" domain") as pbar:
        tasks = [
            process_region(region, semaphore, pbar)
            for region in DEFAULT_REGIONS
        ]
        results = await asyncio.gather(*tasks)

    all_ips = []
    for region_ips in results:
        all_ips.extend(region_ips)

    unique_ips = sorted(set(all_ips))


    merged_ips = sorted(old_ips.union(unique_ips))
    async with aiofiles.open(HISTORY_FILE, 'w') as f:
        await f.write('\n'.join(merged_ips) + '\n')

    elapsed = time.time() - start_time
    ip_count = len(unique_ips)

    print()
    log_success(f">> New ip IP count: {MAGENTA}{ip_count:,}{NC}")
    log_success(f">> All IP count: {MAGENTA}{len(merged_ips):,}{NC}")
    log_success(f">> Time left: {MAGENTA}{elapsed:.1f}с{NC}")
    log_success(f">> Speed: {MAGENTA}{ip_count / elapsed:.0f} IP/с{NC}")

    dns_executor.shutdown(wait=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        dns_executor.shutdown(wait=False)
