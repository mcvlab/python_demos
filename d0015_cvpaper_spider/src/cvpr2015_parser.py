# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2015)


def main():
    cvpr = CVPRParser()


if __name__ == "__main__":
    main()
