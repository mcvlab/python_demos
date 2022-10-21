# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2018)

    def parse_pages(self):
        # 获取表格所在对象
        all_tags = self.dom.select("ul.publ-list li cite")
        all_papers = []
        idx = 0
        for tag in all_tags:
            idx += 1
            text = utils.strip_html_text(tag.get_text())
            authors = text.split(":")[0]
            text = text.replace(authors + ":", "")
            pages = text.split(".")[-1]
            title = text.replace(pages, "").strip()
            # print(authors, title)
            all_papers.append(
                {
                    "type": "posters",
                    "sess_title": "",
                    "poster_id": str(idx),
                    "paper_id": "",
                    "title": title,
                    "authors": [
                        " ".join(author.strip().split())
                        for author in authors.split(",")
                    ],
                }
            )
        return all_papers


def main():
    cvpr = CVPRParser()
    all_papers = cvpr.parse_pages()
    print("number of papers: {}".format(len(all_papers)))
    # 写入到文件
    with open("output/cvpr2018.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
