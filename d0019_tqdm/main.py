# encoding: utf-8

from math import sqrt
from time import sleep
from tqdm import tqdm, trange
from loguru import logger


def test_tqdm():
    """测试tqdm进度条"""
    for i in tqdm(range(1000)):
        sleep(0.1)
        # logger.info("step:{i}")
        tqdm.write("step:{}".format(i))


def test_trange():
    """测试trange定制进度条"""
    with trange(1000) as t:
        for i in t:
            t.set_description("step: {}".format(i))
            t.set_postfix(loss=sqrt(i))
            t.set_postfix(test_loss=sqrt(i))
            state_dict = {"loss": 12, "test_loss": 13}
            t.set_postfix(**state_dict)
            sleep(0.01)


def main():
    test_trange()


if __name__ == "__main__":
    main()
