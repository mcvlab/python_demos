# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2019)

    def parse_pages(self):
        # 获取paper type
        type_h = self.dom.select("h4")
        type_heads = []
        for head in type_h:
            cont = head.get_text()
            if "Oral" in cont or "Poster" in cont:
                type_heads.append(head)
        # print(type_heads)
        # 获取表格所在对象
        paper_tabs = self.dom.select("table")
        if len(type_heads) != len(paper_tabs):
            raise ValueError(
                "type heads and tables not agree.head {} but table {}".format(
                    len(type_heads), len(paper_tabs)
                )
            )
        all_papers = []
        for idx, head in enumerate(type_heads):
            # paper type
            cont = head.get_text().replace("\n", " ")
            cont = " ".join(cont.strip().split())
            if "Oral" in cont:
                paper_type = "orals"
                tag = cont.split("Oral")[-1].strip().split()[0]
            elif "Poster" in cont:
                paper_type = "posters"
                tag = cont.split("Poster")[-1].strip().split()[0]
            else:
                raise ValueError("unknown paper type in {}".format(cont))
            # print(paper_type, tag)
            # 提取表格内容
            tab = paper_tabs[idx]
            rows = tab.select("tr")
            cur_sess_title = ""
            for row in rows[1:]:
                cols = row.select("td")
                # 获取session title
                sess_title = utils.strip_html_text(cols[0].get_text())
                if sess_title == "":
                    sess_title = cur_sess_title
                else:
                    cur_sess_title = sess_title
                poster_id = cols[1].get_text().strip()
                poster_id = tag.lower() + "-" + poster_id
                title = utils.strip_html_text(cols[3].get_text())
                authors = utils.strip_html_text(cols[4].get_text())
                paper_id = utils.strip_html_text(cols[5].get_text())
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
                            for author in authors.split(";")
                        ],
                    }
                )
        return all_papers


def main():
    cvpr = CVPRParser()
    all_papers = cvpr.parse_pages()
    print("number of papers: {}".format(len(all_papers)))
    # 写入到文件
    with open("output/cvpr2019.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
