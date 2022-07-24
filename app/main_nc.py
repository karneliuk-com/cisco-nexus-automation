"""
Tool to work with Nexus over NETCONF
"""

# Modules
import json
from scrapli_netconf import NetconfDriver
import bin.filter as bf


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

    conn = NetconfDriver(**inventory)
    conn.open()
    # response = conn.get_config(source="running", filter_=bf.COLLECT_ALL)
    response = conn.get(filter_=bf.COLLECT_CDP)
    print(response.result)
