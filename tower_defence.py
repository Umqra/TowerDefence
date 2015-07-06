from Model.game_map import GameMap

__author__ = 'umqra'

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Tower defence game")
    parser.add_argument("-c", "--console", help="Turn on console mode", action="store_true")
    return parser.parse_args()

def main():
    args = parse_arguments()


if __name__ == "__main__":
    main()