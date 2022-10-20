# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2017)

    def parse_pages(self):
        # 获取表格所在对象
        all_tabs = self.dom.select("table")
        for table in all_tabs:
            heads = table.select("tbody")
            if len(heads) == 0:
                continue
            heads = heads[0].select("th")
            # print(len(heads))
            if len(heads) == 9:
                paper_tab = table
                break
        # print(paper_tab.select("tr")[0])
        all_papers = []
        rows = paper_tab.select("tr")
        cur_sess_title = ""
        cur_paper_type = ""
        cur_tag = ""
        for row in rows[1:]:
            cols = row.select("td")
            # 获取paper type
            sess = utils.strip_html_text(cols[4].get_text())
            if sess == "":
                paper_type = cur_paper_type
                tag = cur_tag
            else:
                items = sess.split()
                paper_type = items[0].strip().lower()
                if "oral" == paper_type or "poster" == paper_type:
                    paper_type = paper_type + "s"
                tag = items[1].strip().lower()
                # 记录
                cur_paper_type = paper_type
                cur_tag = tag
            # 获取session title
            sess_title = utils.strip_html_text(cols[5].get_text())
            if sess_title == "":
                sess_title = cur_sess_title
            else:
                cur_sess_title = sess_title
            # 获取paper id，poster id， title， authors
            paper_id = utils.strip_html_text(cols[6].get_text())
            poster_id = tag.lower() + "-" + paper_id
            title = utils.strip_html_text(cols[7].get_text())
            authors = utils.strip_html_text(cols[8].get_text())
            # print(sess_title, poster_id, title, authors)
            all_papers.append(
                {
                    "type": paper_type,
                    "sess_title": sess_title,
                    "poster_id": poster_id,
                    "paper_id": paper_id,
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
    with open("output/cvpr2017.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
