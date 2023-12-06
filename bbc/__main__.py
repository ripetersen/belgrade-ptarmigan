import argparse
import importlib
import logging
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scraper', help='scraper module to run')
    parser.add_argument('action', help='action to perform') 
    args, scraper_args = parser.parse_known_args()
    print(args)
    print(scraper_args)

    # configure logging
    logging.basicConfig(level=logging.DEBUG)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    n=0
    while os.path.exists(f"log/bbc_{n:04d}.log"):
        n += 1
    fileHandler = logging.FileHandler(f"log/bbc_{n:04d}.log")
    fileHandler.setFormatter(logFormatter)
    logging.getLogger().addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logging.getLogger().addHandler(consoleHandler)

    scraper_module = importlib.import_module(args.scraper)
    if args.action in scraper_module.EXPORT:
        getattr(scraper_module, args.action)(scraper_args=scraper_args)
    else:
        parser.error(f"scraper module '{args.scraper}' does not support action '{args.action}'")
    
if __name__ == '__main__':
    main()