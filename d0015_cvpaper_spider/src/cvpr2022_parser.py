# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2022)

    def find_all_pages(self):
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
        head = rows[0]
        header_titles = head.select("td")
        num_cols = len(header_titles)
        cur_sess_title = ""
        all_posters = []
        for row in rows[1:]:
            cols = row.select("td")
            sess_title = cols[0].get_text().replace("\n", " ")
            sess_title = " ".join(sess_title.strip().split())
            if sess_title == "":
                sess_title = cur_sess_title
            else:
                cur_sess_title = sess_title
            poster_id = cols[1].get_text().strip()
            title = cols[2].get_text().replace("\n", " ")
            title = " ".join(title.strip().split())
            authors = cols[3].get_text().replace("\n", " ").strip()
            # print(sess_title, poster_id, title, authors)
            all_posters.append(
                {
                    "sess_title": sess_title,
                    "poster_id": poster_id,
                    "title": title,
                    "authors": [
                        " ".join(author.strip().split())
                        for author in authors.split(";")
                    ],
                }
            )
        return all_posters

    def parse_oral_page(self, dom):
        pass


def main():
    cvpr = CVPRParser()
    # cvpr.find_all_pages()
    posters = cvpr.parse_poster_page(cvpr.dom)
    print(posters)


if __name__ == "__main__":
    main()
