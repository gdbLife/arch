import argparse
import json
from utils.logger import Print
from utils.debug import Debug
from modules import disk, check, packages, setup

def load_config(file_path):
    with open("configs/" + file_path + ".json", "r") as f:
        return json.load(f)

def customize_config(config):
    config["disk"] = Print.input(f"Disk [{config.get('disk', '/dev/sda')}]: ") or config["disk"]
    config["hostname"] = Print.input(f"Hostname [{config.get('hostname', 'archlinux')}]: ") or config["hostname"]
    config["username"] = Print.input(f"Username [{config.get('username', 'user')}]: ") or config["username"]
    config["locale"] = Print.input(f"Locale [{config.get('locale', 'en_US')}]: ") or config["locale"]

    packages = Print.input(f"Add packages [{', '.join(config.get('packages', []))}]: ")
    if packages:
        config["packages"].extend(packages.split(","))

    services = Print.input(f"Enable services [{', '.join(config.get('enable_services', []))}]: ")
    if services:
        config["enable_services"].extend(services.split(","))

    return config

def print_config_data(config_data):
    Print.info(f"Disk: {config_data["disk"]}")
    Print.info(f"Hostname: {config_data["hostname"]}")
    Print.info(f"Username: {config_data["username"]}")
    Print.info(f"Packages: {config_data["packages"]}")
    Print.info(f"Locale:   {config_data["locale"]}")
    Print.info(f"Services: {config_data["enable_services"]}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Arch Installer: auto isntall Arch Linux")
    parser.add_argument("--config", type=str, help="path to configuration file")
    parser.add_argument("-c", "--custom", action="store_true", help="customize configuration")
    parser.add_argument("-d", "--debug", action="store_true", help="show debug information")
    parser.add_argument("-t", "--test", action="store_true", help="test mode")
    args = parser.parse_args()

    if args.debug:
            Debug.DEBUG = True

    if args.config:
        config_data = load_config(args.config)
        print_config_data(config_data)
        
        if args.custom:
            config_data = customize_config(config_data)

        check.check_dependencies()
        Print.info("The following updates will be made on the image")
        check.pacman_keys()
        check.pacman_mirrors()

        disk.markup(config_data["disk"])
        disk.format(config_data["disk"])
        disk.mount(config_data["disk"])

        packages.install_packages(config_data["packages"])

        setup.install_grub(config_data["disk"])
        setup.configure_system(config_data["hostname"], config_data["locale"])
        setup.create_user(config_data["username"])
        setup.enable_services(config_data["enable_services"])
        setup.finish()

    elif args.test:
        check.check_dependencies()
        check.pacman_keys()
        check.pacman_mirrors()

    else:
        Print.error("No configuration file provided. Use --config to specify a configuration")
        exit(1)

if __name__ == "__main__":
    main()