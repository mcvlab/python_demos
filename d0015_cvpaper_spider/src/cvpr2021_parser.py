# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2021)

    def _find_all_pages(self):
        """

        Returns:
            page_urls, dict, {类型-月份日期-上下午: url}
        """
        nav_schedule = self.dom.select(".sidebar_first nav ul")[1]
        page_items = nav_schedule.select("ul li")
        page_url = {}
        for item in page_items:
            a_tag = item.select("li>a")[0]
            p_url = a_tag["href"]
            page_url[p_url[1:]] = self.root_url + p_url
        return page_url

    def parse_poster_page(self, dom):
        poster_tab = dom.select("#block-cvpr-content table", border=1)[0]
        rows = poster_tab.select("tbody tr")
        all_posters = []
        for row in rows[1:]:
            cols = row.select("td")
            paper_id = cols[0].get_text().strip()
            poster_id = paper_id
            title = cols[1].get_text().replace("\n", " ")
            title = " ".join(title.strip().split())
            authors = cols[2].get_text().replace("\n", " ").strip()
            # print(sess_title, poster_id, title, authors)
            all_posters.append(
                {
                    "type": "posters",
                    "sess_title": "",
                    "poster_id": poster_id,
                    "paper_id": paper_id,
                    "title": title,
                    "authors": [
                        " ".join(author.strip().split())
                        for author in authors.split(";")
                    ],
                }
            )
        return all_posters

    def parse_pages(self):
        urls = self._find_all_pages()
        all_papers = []
        for k, url in urls.items():
            items = k.split("/")
            sess_id = items[-1]
            # 获取网页内容
            if url == self.url:
                dom = self.dom
            else:
                # logger.info("download {} ...".format(url))
                html_str = utils.download_html(url)
                dom = utils.parse_dom(html_str)
            # 提取所有的文章
            papers = self.parse_poster_page(dom)
            # 记录
            for paper in papers:
                paper["poster_id"] = sess_id + "-" + paper["poster_id"]
                all_papers.append(paper)
        return all_papers


def main():
    cvpr = CVPRParser()
    urls = cvpr._find_all_pages()
    print(urls)
    # papers = cvpr.parse_poster_page(cvpr.dom)
    all_papers = cvpr.parse_pages()
    print("number of papers: {}".format(len(all_papers)))
    # 写入到文件
    with open("output/cvpr2021.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
