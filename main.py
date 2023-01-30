import dns.resolver
import yaml
import time
import logging

from datetime import datetime

# Global variable for logging
LOGGER = None


def check_txt_record(url: str, substring: str) -> bool:
    """
    Takes a url and queries the TXT files for that domain. If the substring is found in the TXT
    entries it returns True, otherwise it returns false
    :param url: URL to query
    :param substring: Substring to look for in TXT entries
    :return: bool
    """
    try:
        answers = dns.resolver.resolve(url, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if substring in txt_string.decode():
                    return True
        return False
    except Exception as e:
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        global LOGGER
        LOGGER.debug(f" {dt_string} Error: {e}")
        return False


def load_variables(cfg: dict) -> (str, str, int):
    """
    Loads values for url, substring and time interval to query. If config is empty (or if the
    value is missing from the config) it will load default values and write to the logfile
    :param cfg: Dictionary created from default configuration file
    :return: tuple containing url, substring and time interval
    """
    # Default values. Will be overwritten if present in "config.yml"
    hostname = "futurestay.com"
    substring = "google-site"
    seconds = 5

    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    if "hostname" in cfg:
        hostname = cfg["hostname"]
    else:
        LOGGER.debug(f" {dt_string} Using default value for hostname")

    if "substring" in cfg:
        substring = cfg["substring"]
    else:
        LOGGER.debug(f" {dt_string} Using default value for substring")

    if "seconds" in cfg:
        seconds = cfg["seconds"]
    else:
        LOGGER.debug(f" {dt_string} Using default value for seconds")

    return (hostname, substring, seconds)


def init_logfile(cfg: dict) -> None:
    """
    Initialize logfile. Note - any application can write to the log using
    the global variable: LOGGER
    :param cfg: Dictionary containing configuration file settings used to determine
    name of logfile
    """
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    logfile = cfg["logfile"]

    try:
        logging.basicConfig(filename=logfile, level=logging.DEBUG)
    except Exception as e:
        print(f" {dt_string} Problem while writing to log file {logfile}")

    global LOGGER
    LOGGER = logging

    LOGGER.debug(f" {dt_string} Starting log file ")


def main():
    # Default config file
    CONFIG_FILE = "config.yml"

    ymlConfigFile = open(CONFIG_FILE, "r")
    cfg = yaml.safe_load(ymlConfigFile)

    # initialize the global LOGGER variable
    init_logfile(cfg)

    url, substring, seconds = load_variables(cfg)

    while True:
        if check_txt_record(url, substring):
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print(dt_string)
        time.sleep(float(seconds))


if __name__ == "__main__":
    main()
