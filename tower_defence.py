from Gui import gui_tower_defence

__author__ = 'umqra'

import argparse

import logging
import logging.config

logging.config.fileConfig('logging.conf')


def parse_arguments():
    parser = argparse.ArgumentParser(description="Tower defence game")
    parser.add_argument("-c", "--console", help="Turn on console mode", action="store_true")
    return parser.parse_args()


def main():
    gui_tower_defence.run()

if __name__ == "__main__":
    main()