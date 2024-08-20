import os
import requests
import time
from urllib.error import HTTPError, URLError

import signal

def handler(signum, frame):
    msg = "Ctrl-c was pressed, exiting !"
    print(msg)
    print("")
    exit(1)

signal.signal(signal.SIGINT, handler)

BASE_URL = os.environ.get('RI_BASE_URL', 'http://redis-insight:5540')
#BASE_URL = os.environ.get('RI_BASE_URL', 'http://localhost:5540')
ACCEPT_EULA = os.environ.get('RI_ACCEPT_EULA', False)
DB_NAME = os.environ.get('RI_CONNECTION_NAME', 'Docker (redis)')
DB_HOST = os.environ.get('REDIS_HOST', 'redis')
DB_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Wait for service

URL = f"{BASE_URL}/api/health"

print(f"Checking if redis insight is running ...")
print("")

worked = False
retry = 60
while not worked and retry > 0:
    print(f"GET {URL} ...")
    try:
        res = requests.get(URL, timeout=2)
        worked = True
    except Exception as ex:
        print(f"Connection error: {ex.__class__.__name__} {str(ex)}")
        retry -= 1

        if retry > 0:
            print(f"Waiting to retry ({retry} tries left) ...")
            print(f"")
            time.sleep(3)

if worked:
    resCode = res.status_code
    print(f"Status code: {resCode}")

    resBody = res.text
    print(f"Response has {len(resBody)} bytes.")
    print("")

    # Accept user agreement
    if ACCEPT_EULA:
        URL = f"{BASE_URL}/api/settings"

        print(f"Accepting user agreement ...")
        print("")

        print(f"PATCH {URL} ...")
        data = {
            "agreements": {
                "analytics": False,
                "notifications": False,
                "encryption": False,
                "eula": True
            }
        }

        res = requests.patch(URL, json=data, timeout=2)

        resCode = res.status_code
        print(f"Status code: {resCode}")

        resBody = res.text
        print(f"Response has {len(resBody)} bytes.")
        print("")

    # Get connections

    URL = f"{BASE_URL}/api/databases"

    print(f"Checking if connection already exists ...")
    print("")

    print(f"GET {URL} ...")
    res = requests.get(URL, timeout=2)

    resCode = res.status_code
    print(f"Status code: {resCode}")

    resBody = res.text
    print(f"Response has {len(resBody)} bytes.")
    print("")

    print(f"Decoding response ...")
    conns = res.json()
    print(f"Found {len(conns)} connections.")
    print("")

    print(f"Searching for expected connection ...")
    found = False
    if len(conns) == 0:
        print("No connection to look into.")
    else:
        for conn in conns:
            dbName = conn['name']
            dbHost = conn['host']
            dbPort = conn['port']

            msg = "other"
            if dbName == DB_NAME:
                found = True
                msg = 'EXPECTED'

            print(f"Found {msg} connection \"{dbName}\" for host \"{dbHost}\" on port {dbPort}.")

    print("")

    if found:
        print("Expected connection was found, nothing to do !")
    else:
        print("Expected connection was NOT found, creating it ...")
        print("")

        # Create connection
        print(f"POST {URL} ...")
        data = {
            "name": DB_NAME,
            "host": DB_HOST,
            "port": DB_PORT,
            "db": 0,
            "tls": False
        }

        res = requests.post(URL, json=data, timeout=2)

        resCode = res.status_code
        print(f"Status code: {resCode}")

        resBody = res.text
        print(f"Response has {len(resBody)} bytes.")
        print("")

        if resCode == 201:
            print(f"Connection created successfully !")
        else:
            print(f"Connection creation FAILED !")
            print(resBody)

        print("")
