# encoding: utf-8

import json
import os
import requests
import hashlib
from loguru import logger
import bs4


def download_html(html_url):
    """下载html文件"""
    hash_val = hashlib.sha1(html_url.encode("utf-8")).hexdigest()
    cache_file = os.path.join("output", "cache", hash_val + ".html")
    #  检查缓存是否存在
    if os.path.isfile(cache_file):
        logger.info("load {} from cache {}.".format(html_url, cache_file))
        with open(cache_file) as fid:
            html_str = fid.read()
        return html_str
    # 下载
    try:
        # 发起请求
        response = requests.get(html_url)
        html_str = response.text
        # 保存到缓存文件
        if not os.path.isdir(os.path.dirname(cache_file)):
            os.makedirs(os.path.dirname(cache_file))
        with open(cache_file, "w") as fid:
            fid.write(html_str)
    except requests.RequestException:
        logger.warning("fail to request url: {}".format(html_url))
        html_str = ""
    return html_str


def parse_dom(html_str):
    """将html字符串解析为dom结构"""
    return bs4.BeautifulSoup(html_str, "html.parser")


def load_cvconf_url(year, conf_name="cvpr", config_file="config/url.json"):
    """从配置文件载入cv会议url"""
    html_url = None
    with open(config_file) as fid:
        all_configs = json.load(fid)
    for c in all_configs[conf_name]:
        if c["year"] == year:
            html_url = c["url"]
    if html_url is None:
        logger.error("not found {} url in {}".format(year, config_file))
        raise ValueError("failed to get html url from config file")
    return html_url


def main():
    html_url = "https://cvpr2022.thecvf.com/posters-621-am"
    html_str = download_html(html_url)
    soup = parse_dom(html_str)
    print(soup)


if __name__ == "__main__":
    main()
