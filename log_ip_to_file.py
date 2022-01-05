#!/usr/bin/env python3

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

DEBUG = False

MESSAGE_FORMAT = '%(asctime)s id:%(process)d %(levelname)s: %(message)s'

if DEBUG:
    logging.basicConfig(stream=sys.stdout, format=MESSAGE_FORMAT, level=logging.INFO)
else:
    logging.basicConfig(filename='log_ip.log', format=MESSAGE_FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)

last_ip_file = 'last_ip.txt'
log_ip_file = 'logged_ip.csv'

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'


def get_last_ip():
    filename = Path(dir_path + last_ip_file)
    filename.touch(exist_ok=True)
    file = open(dir_path + last_ip_file, 'r+')
    return file.read()


def get_current_ip():
    # curl -s http://ipv4.icanhazip.com
    # curl -s http://checkip.dyndns.com
    # http://ifconfig.me/ip
    # http://icanhazip.com
    logger.debug("Detecting IP...")
    res = requests.get('http://ipinfo.io/json')
    if res.status_code == 200:
        return res.json()
    res = requests.get('https://api.ipify.org?format=json')
    if res.status_code == 200:
        return res.json()
    res = requests.get('http://ipv4.icanhazip.com')
    if res.status_code == 200:
        return {'ip': res.text.strip()}
    else:
        logger.error("cant detect ip address..")
        return {'ip': ''}


def update_last_ip(real_ip: str):
    logger.debug("write to file %s", real_ip)
    with open(dir_path + last_ip_file, 'w') as text_file:
        text_file.write(real_ip)


def add_new_ip_to_log(ip: str):
    with open(dir_path + log_ip_file, 'a') as text_file:
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text_file.write(f"{ip},{curr_time}\n")


def main():
    last_ip = get_last_ip()
    current_ip = get_current_ip()['ip']

    if len(current_ip) == 0:
        logger.debug("No update. Exit...")
        return

    if last_ip == current_ip:
        # pass
        logger.info("Current IP is the same, no update!")
    else:
        logger.info("IP has been changed to '%s'", current_ip)
        add_new_ip_to_log(current_ip)
        update_last_ip(current_ip)


if __name__ == "__main__":
    main()
