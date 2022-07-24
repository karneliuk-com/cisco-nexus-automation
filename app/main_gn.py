"""
Tool to work with Nexus over GNMI
"""

# Modules
import json
from pygnmi.client import gNMIclient


# Variables
INVENTORY_PATH = "./inventory/inventory.json"


# Body
if __name__ == "__main__":
    try:
        inventory_stream = open(file=INVENTORY_PATH, mode="rt", encoding="utf-8")
        inventory = json.loads(inventory_stream.read())

    except (FileNotFoundError, json.JSONDecodeError) as err:
        print(err)
        exit(err.errno)

    with gNMIclient(target=(inventory["host"], 50051),
                    username=inventory["auth_username"],
                    password=inventory["auth_password"],
                    path_cert="./cert.pem",
                    skip_verify=True) as gconn:
        gconn.capabilities()

        r1 = gconn.get(path=["/System/cdp-items"])
        print(json.dumps(r1, indent=4))
