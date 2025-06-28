#!/usr/bin/env python3
# Authored by: eat-correctly

from subprocess import Popen, PIPE, call
from json import loads

# If K0s:
ALLOWED_ADDRESSES = ["10.96.0.0/12", "10.244.0.0/16"]

# If K3s:
# ALLOWED_ADDRESSES = ["10.42.0.0/16", "10.43.0.0/16"]


def main():
    with Popen(("mullvad", "status", "--json", "listen"), stdout=PIPE) as mullvad:
        while line := mullvad.stdout.readline():
            status = loads(line)

            if status.get("state", None) != "connected":
                continue

            if "details" not in status:
                continue

            if "location" not in status["details"]:
                continue

            if not status["details"]["location"].get("ipv4", None):
                continue

            for chain in ("forward", "output"):
                for ip in ALLOWED_ADDRESSES:
                    call(f"nft insert rule inet mullvad {chain} ip daddr {ip} accept".split())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye!")
