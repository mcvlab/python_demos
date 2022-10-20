# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2020)

    def parse_pages(self):
        # 获取session title所在的对象
        sess_p = self.dom.select("#block-cvpr-content p")
        sess_heads = []
        for head in sess_p:
            if "Session:" in head.get_text():
                sess_heads.append(head)
        # 获取表格所在对象
        paper_tabs = self.dom.select("#block-cvpr-content table")
        if len(sess_heads) != len(paper_tabs):
            raise ValueError(
                "oral heads and tables not agree.head {} but table {}".format(
                    len(sess_heads), len(paper_tabs)
                )
            )
        all_papers = []
        for idx, head in enumerate(sess_heads):
            #  提取session title以及paper type
            sess = head.get_text().replace("\n", " ")
            sess = " ".join(sess.strip().split())
            sess = sess.split("Session:")[-1].strip()
            # print(sess)
            items = sess.split("—")
            paper_type = items[0].lower().strip()
            sess_title = items[1].strip()
            items = paper_type.split()
            paper_type = items[0].strip() + "s"
            sess_tag = items[1].strip()
            # print(paper_type, sess_tag, sess_title)
            # 提取表格内容
            tab = paper_tabs[idx]
            rows = tab.select("tbody tr")
            for row in rows[1:]:
                cols = row.select("td")
                poster_id = cols[0].get_text().strip()
                poster_id = sess_tag + "-" + poster_id
                title = cols[3].get_text().replace("\n", " ")
                title = " ".join(title.strip().split())
                authors = cols[4].get_text().replace("\n", " ").strip()
                paper_id = cols[5].get_text().replace("\n", " ").strip()
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
    with open("output/cvpr2020.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
