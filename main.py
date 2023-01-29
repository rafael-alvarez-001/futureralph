import dns.resolver
import yaml
import time
import logging

from datetime import datetime

LOGGER = None


def check_txt_record(domain: str, record: str) -> bool:
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if record in txt_string.decode():
                    return True
        return False
    except Exception as e:
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        global LOGGER
        LOGGER.debug(f"{dt_string} Error: {e}")
        return False


def load_variables(cfg: dict) -> (str, str, int):
    # Default values. Will be overwritten if present in "config.yml"
    hostname = "futurestay.com"
    substring = "google-site"
    seconds = 5

    if "hostname" in cfg:
        hostname = cfg["hostname"]
    if "substring" in cfg:
        substring = cfg["substring"]
    if "seconds" in cfg:
        seconds = cfg["seconds"]

    return (hostname, substring, seconds)


def init_logfile(cfg: dict):
    logfile = cfg["logfile"]
    logging.basicConfig(filename=logfile, level=logging.DEBUG)

    global LOGGER
    LOGGER = logging

    # TODO check logfile is writable


def main():
    # Default config file
    CONFIG_FILE = "config.yml"

    ymlConfigFile = open(CONFIG_FILE, "r")
    cfg = yaml.safe_load(ymlConfigFile)

    # initialize the global LOGGER variable
    init_logfile(cfg)
    # initialize
    url, substring, seconds = load_variables(cfg)

    while True:
        if check_txt_record(url, substring):
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print(dt_string)
        time.sleep(float(seconds))


if __name__ == "__main__":
    main()
