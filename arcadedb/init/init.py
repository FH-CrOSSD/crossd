import base64
import json
import os
import time
import urllib.error
import urllib.request

ARCADEDB_URL = os.environ["ARCADEDB_URL"].rstrip("/")
ARCADEDB_ROOT_PASSWORD = os.environ["ROOT_PW"]
ARCADEDB_DATABASE = "crossd" # os.environ.get("ARCADEDB_DATABASE", "crossd")

_credentials = base64.b64encode(f"root:{ARCADEDB_ROOT_PASSWORD}".encode()).decode()
AUTH_HEADER = f"Basic {_credentials}"

USERS = [
    {
        "name": os.environ["FRONTEND_USER"],
        "password": os.environ["FRONTEND_PASSWORD"],
        "group": "readonly",
    },
    {
        "name": os.environ["WORKER_USER"],
        "password": os.environ["WORKER_PASSWORD"],
        "group": "readwrite",
    },
]


def wait_for_ready():
    print("Waiting for ArcadeDB to be ready...")
    while True:
        try:
            req = urllib.request.Request(f"{ARCADEDB_URL}/api/v1/ready")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 204:
                    print("ArcadeDB is ready.")
                    return
        except Exception as e:
            print(f"Not ready yet: {e}")
        time.sleep(2)


def create_user(name: str, password: str, group: str):
    command = f'create user {{"name": "{name}", "password": "{password}", "databases": {{"{ARCADEDB_DATABASE}": "{group}"}}}}'
    body = json.dumps({"command": command}).encode()
    req = urllib.request.Request(
        f"{ARCADEDB_URL}/api/v1/server",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": AUTH_HEADER},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"Created user '{name}': {resp.status}")
    except urllib.error.HTTPError as e:
        # return 403 for existing user... invalid credentials should already fail for db_exists check
        if e.code == 403:
            print(f"User '{name}' already exists, skipping.")
        else:
            raise

def db_exists(name: str) -> bool:
    req = urllib.request.Request(
        f"{ARCADEDB_URL}/api/v1/exists/{name}",
        headers={"Authorization": AUTH_HEADER},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())["result"]


def create_db(name: str):
    if db_exists(name):
        print(f"Database '{name}' already exists, skipping.")
        return
    command = f'create database {name}'
    body = json.dumps({"command": command}).encode()
    req = urllib.request.Request(
        f"{ARCADEDB_URL}/api/v1/server",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": AUTH_HEADER},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"Created database '{name}': {resp.status}")
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print(f"Database '{name}' already exists, skipping.")
        else:
            raise


def main():
    wait_for_ready()
    create_db(ARCADEDB_DATABASE)
    for user in USERS:
        create_user(user["name"], user["password"], user["group"])


if __name__ == "__main__":
    main()
