#!/usr/bin/python3

import argparse
import subprocess as sb

OFFLINE_UPDATER_PATH="/home/lely/offline_updater/extras"
RUNNERS = [
    "192.168.100.61",
    "192.168.100.62",
    "192.168.100.63",
    "192.168.100.64",
    "192.168.100.71",
    "192.168.100.72",
    "192.168.100.73",
    "192.168.100.74",
]

parser = argparse.ArgumentParser(
    description="Replace the Recovery Updater CLI on all runners"
)
parser.add_argument(
    '-p',
    '--path',
    required=True,
    help="local path to the Recovery Updater"
)
parser.add_argument(
    '-u',
    '--user',
    required=True,
    help="your username on the runners"
)

args=parser.parse_args()
local_path = args.path
user = args.user


def copy_and_chown(runner_ip):
    print(f'=> Copying to {runner_ip}')
    remote_dest=f"{user}@{runner_ip}:{OFFLINE_UPDATER_PATH}"
    res = sb.run(["rsync", "--progress", local_path, remote_dest])
    
    if res.returncode != 0:
        print(f'Something went wrong copying to {runner_ip}!')
        exit(1)

def print_end():
    end = '\n' + 35 * '=' + "\n" + \
        "= All done!\n" + \
        "= Please chown the tool manually!\n" + 35 * "="
    print(end)



if __name__ == "__main__":
    for runner in RUNNERS:
        copy_and_chown(runner)
    print_end()
