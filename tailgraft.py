#!/usr/bin/env python3

import json
import os
import sys


flags = [
    "tailscale",
    "up",
    "--ssh",
]
hostname = ""


def lsblk_linux():
    return json.loads(os.popen("lsblk --json").read())


def find_user_data():
    if sys.platform == 'darwin':
        for root, dirs, files in os.walk('/Volumes'):
            for dir in dirs:
                if os.path.isfile(os.path.join(root, dir, 'user-data')):
                    return os.path.join(root, dir, 'user-data')        
    elif sys.platform == 'linux':
        devices = lsblk_linux()['blockdevices']

        for dev in devices:
            for mountpoint in dev["mountpoints"]:
                if mountpoint is not None and os.path.isfile(os.path.join(mountpoint, 'user-data')):
                    return os.path.join(mountpoint, 'user-data')
    
            if dev.get("children", None) is not None:
                for child in dev["children"]:
                    for mountpoint in child["mountpoints"]:
                        if mountpoint is not None and os.path.isfile(os.path.join(mountpoint, 'user-data')):
                            return os.path.join(mountpoint, 'user-data')

    for root, dirs, files in os.walk('/Volumes'):
        for dir in dirs:
            if os.path.isfile(os.path.join(root, dir, 'user-data')):
                return os.path.join(root, dir, 'user-data')
    return None


def prompt_user(prompt, allowed_replies = []):
    while True:
        reply = input(prompt)
        if allowed_replies != [] and reply in allowed_replies:
            return reply
        else:
            print("Invalid reply. Please try again.")


def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root. Re-executing with sudo...")
        os.execvp('sudo', ['sudo', 'python3'] + sys.argv)


def main():
    check_root()
    user_data_fname = find_user_data()
    if user_data_fname is None:
        print("Could not find user-data file. Please try removing your SD card and re-inserting it.")
        sys.exit(1)

    print("Found user-data file at {}".format(user_data_fname))

    be_exit_node = prompt_user("Would you like this device to be an exit node? (y/n): ", ['y', 'n']) == 'y'
    if be_exit_node:
        flags.append("--advertise-exit-node")
        print("This device will be an exit node.")

    authkey = input("Please enter your Tailscale authkey: ")
    flags.append("--authkey={}".format(authkey))

    hostname = input("Please enter a hostname for this device: ")
    if hostname != "":
        flags.append("--hostname={}".format(hostname))

    print("Adding Tailscale to user-data file...")

    with open(user_data_fname, 'a') as f:
        f.write("runcmd:\n")
        f.write("""  - [ "sh", "-c", "curl -fsSL https://tailscale.com/install.sh | sh" ]""")
        f.write("\n")
        f.write("""  - [ "sh", "-c", "echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf && echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf && sudo sysctl -p /etc/sysctl.d/99-tailscale.conf" ]""")
        f.write("\n")
        f.write("  - {}\n".format(json.dumps(flags)))
        if hostname != "":
            f.write("""  - [ "sh", "-c", "sudo hostnamectl hostname {}" ]""".format(hostname))
            f.write("\n")

    print("Tailscale will be installed on boot. Please eject your SD card and boot your raspi.")
    print("Good luck!")


if __name__ == "__main__":
    main()
