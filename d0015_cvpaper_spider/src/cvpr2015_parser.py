# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2015)

    def parse_pages(self):
        time_tag = self.dom.select(".cvprparagraphheader")
        all_papers = []
        for tag in time_tag:
            # 从时间中解析tag
            time_str = utils.strip_html_text(tag.get_text()).split(",")[0]
            day = time_str.split()[-1]
            sess_tag = "6" + "%0*d" % (2, int(day))
            # print(sess_tag)
            # 解析table
            table_tag = tag.find_next_sibling("table")
            heads = table_tag.select("th")
            if len(heads) == 1:
                # 去掉speaker
                if "speaker" in heads[0].get_text().lower():
                    continue
                # 解析poster
                rows = table_tag.select("tr")
                for row in rows[3:]:
                    cols = row.select("td")
                    poster_id = utils.strip_html_text(cols[0].get_text())
                    title_tag = cols[1].select("b")[0]
                    title = utils.strip_html_text(title_tag.get_text())
                    authors = utils.strip_html_text(col.get_text().split("]")[-1])
                    all_papers.append(
                        {
                            "type": "posters",
                            "sess_title": "",
                            "poster_id": sess_tag + "-" + poster_id,
                            "paper_id": "",
                            "title": title,
                            "authors": [
                                " ".join(author.strip().split())
                                for author in authors.split(",")
                            ],
                        }
                    )
            elif len(heads) == 2:
                # 解析oral
                rows = table_tag.select("tr")
                idx = 0
                for row in rows[2:]:
                    cols = row.select("td")
                    for col in cols:
                        idx += 1
                        # print(col)
                        title_tag = col.select("b")
                        if len(title_tag) == 0:
                            continue
                        title = utils.strip_html_text(title_tag[0].get_text())
                        authors = utils.strip_html_text(col.get_text().split("]")[-1])
                        all_papers.append(
                            {
                                "type": "orals",
                                "sess_title": "",
                                "poster_id": sess_tag + "-" + str(idx),
                                "paper_id": "",
                                "title": title,
                                "authors": [
                                    " ".join(author.strip().split())
                                    for author in authors.split(",")
                                ],
                            }
                        )
            else:
                raise ValueError("not expect table")
        return all_papers


def main():
    cvpr = CVPRParser()
    all_papers = cvpr.parse_pages()
    print("number of papers: {}".format(len(all_papers)))
    # 写入到文件
    with open("output/cvpr2015.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
