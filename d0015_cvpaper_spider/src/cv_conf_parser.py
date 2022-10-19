# encoding: utf-8

import utils


class CVConfParser:
    def __init__(self, conf_name, year) -> None:
        """CV会议解析基类初始化

        Args:
            conf_name: str, 会议名称，必须与url.json配置文件中一致
            year: int, 年份
        """
        # 获取 Schedule 网址
        html_url = utils.load_cvconf_url(year, conf_name)
        # 下载页面
        html_str = utils.download_html(html_url)
        # 解析dom结构
        self.dom = utils.parse_dom(html_str)
