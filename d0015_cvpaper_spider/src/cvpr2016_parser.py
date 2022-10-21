# encoding: utf-8

from ctypes import util
import json
import re
import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2016)
        logger.info("origin html contains special characters, load again and process")
        html_str = utils.download_html(self.url)
        p = re.compile(r"&#\d*")
        html_str = p.sub("_XoX_", html_str)
        self.dom = utils.parse_dom(html_str)

    def _parse_session(self, tag, paper_type):
        papers = []
        sess_title = ""
        sess_tag = "6"
        daytime_tag = ""
        if "oral" == paper_type or "poster" == paper_type:
            paper_type = paper_type + "s"
        while tag.name != "hr":  # tag != None and
            if tag.name == "h4":
                sess_title = utils.strip_html_text(tag.get_text())
            elif tag.name == "h5":
                daytime_tag = utils.strip_html_text(tag.get_text())
                items = daytime_tag.split(",")
                date = items[1].strip().split()[-1]
                daytime = "a" if "AM" in items[2] else "b"
                sess_tag = date[0:2] + "-" + daytime
            elif tag.name == "ul":
                title_tag = tag.select("strong")[0]
                author_tag = tag.select("p")[0]
                poster_id = tag.get_text().strip().split()[0].strip()
                # print(title_tag)
                title = utils.strip_html_text(title_tag.get_text())
                authors = utils.strip_html_text(author_tag.get_text())
                papers.append(
                    {
                        "type": paper_type,
                        "sess_title": sess_title,
                        "poster_id": sess_tag + "-" + poster_id,
                        "paper_id": "",
                        "title": title,
                        "authors": [
                            " ".join(author.strip().split())
                            for author in authors.split(",")
                        ],
                    }
                )
                # print("ul", poster_id)
            # print(tag.name)
            nexttag = tag.find_next_sibling()
            if nexttag is None:
                print(daytime_tag, "poster_id:", poster_id)
                print("not found next")
                break
            tag = nexttag
        return papers

    def parse_pages(self):
        """bs4似乎解析html存在问题"""
        all_headers = self.dom.select("h3.programheader")
        # print(len(all_headers))
        all_papers = []
        for header in all_headers:
            h3 = header
            paper_type = utils.strip_html_text(h3.get_text()).split("SESSION")[0]
            paper_type = paper_type.strip().lower()
            tag = header.find_next_sibling()
            papers = self._parse_session(tag, paper_type)
            # print("number:", len(papers))
            # for paper in papers:
            all_papers.extend(papers)
        return all_papers


def main():
    cvpr = CVPRParser()
    all_papers = cvpr.parse_pages()
    print("number of papers: {}".format(len(all_papers)))
    # 写入到文件
    with open("output/cvpr2016.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
