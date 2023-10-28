import tinytuya
import argparse
import json
import os

def read_device(name):
    """
    Reads the configuration for a specific device from ~/.config/light/light.json.

    Expected JSON format:
    {
        "livingroom": {
            "device_id": "device_id_1",
            "ip_address": "ip_address_1",
            "local_key": "local_key_1"
        },
        "bedroom": {
            "device_id": "device_id_2",
            "ip_address": "ip_address_2",
            "local_key": "local_key_2"
        },
        // ... more devices
    }

    Parameters:
        name (str): The name of the device (e.g., "LivingRoom", "BedRoom").

    Returns:
        tuple: DEVICE_ID, IP_ADDRESS, LOCAL_KEY for the specified device
    """
    config_path = os.path.expanduser("~/.config/light/light.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    device_config = config.get(name)
    
    if device_config is None:
        raise KeyError(f"No configuration found for device named {name}")
        
    return device_config['device_id'], device_config['ip_address'], device_config['local_key']


def turn_off(d):
    d.set_status({'dps': {'1': False}})
    print(f"after set_status\n{d.status()}")

def debug():
    tinytuya.set_debug(True)

def turn_on(d):
    d.turn_on()

def purple(d):
    d.set_colour(221, 186, 255)

def yellow(d):
    d.set_colour(255, 255, 0)

def dim(d):
    d.set_brightness(10)

def bright(d):
    d.set_brightness(1000)

def main():
    parser = argparse.ArgumentParser(description='Control Tuya smart bulb.')
    parser.add_argument('--name', help='device name from ~/.config/light/light.json')
    parser.add_argument('--off', action='store_true', help='Turn off the bulb')
    parser.add_argument('--on', action='store_true', help='Turn on the bulb')
    parser.add_argument('--purple', action='store_true', help='Set the bulb to purple')
    parser.add_argument('--yellow', action='store_true', help='Set the bulb to yellow')
    parser.add_argument('--dim', action='store_true', help='Dim the bulb')
    parser.add_argument('--bright', action='store_true', help='Brighten the bulb')
    parser.add_argument('--debug', action='store_true', help='Enable debugging')
    
    args = parser.parse_args()

    device_id, ip_address, local_key = read_device(args.name)

    d = tinytuya.BulbDevice(device_id, ip_address, local_key, version=3.3)
    print(f"before:\n{d.status()}")

    if args.debug:
        debug()
    
    if args.off:
        turn_off(d)
    elif args.on:
        turn_on(d)
    elif args.purple:
        purple(d)
    elif args.yellow:
        yellow(d)
    elif args.dim:
        dim(d)
    elif args.bright:
        bright(d)

    print(f"after:\n{d.status()}")

if __name__ == '__main__':
    main()

