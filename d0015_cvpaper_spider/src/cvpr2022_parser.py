# encoding: utf-8

import json

import utils
from loguru import logger
from cv_conf_parser import CVConfParser


class CVPRParser(CVConfParser):
    def __init__(self) -> None:
        super().__init__("cvpr", 2022)

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
                    "type": "posters",
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
        # 获取session title所在的对象
        oral_h4 = dom.select("#block-cvpr-content h4")
        oral_heads = []
        for head in oral_h4:
            if "Session Title:" in head.get_text():
                oral_heads.append(head)
        # 获取表格所在对象
        oral_tabs = dom.select("#block-cvpr-content table")
        if len(oral_heads) != len(oral_tabs):
            raise ValueError(
                "oral heads and tables not agree.head {} but table {}".format(
                    len(oral_heads), len(oral_tabs)
                )
            )
        all_orals = []
        for idx, head in enumerate(oral_heads):
            # 提取session title
            text = head.get_text()
            text = text.split("Session Title:")[-1]
            text = text.split("Session Chairs:")[0]
            sess_title = " ".join(text.replace("\n", " ").split())
            # 提取表格内容
            tab = oral_tabs[idx]
            rows = tab.select("tbody tr")
            for row in rows[1:]:
                cols = row.select("td")
                if len(cols) > 3:
                    cols = cols[len(cols) - 3 :]
                poster_id = cols[0].get_text().strip()
                title = cols[1].get_text().replace("\n", " ")
                title = " ".join(title.strip().split())
                authors = cols[2].get_text().replace("\n", " ").strip()
                # print(sess_title, poster_id, title, authors)
                all_orals.append(
                    {
                        "type": "orals",
                        "sess_title": sess_title,
                        "poster_id": poster_id,
                        "title": title,
                        "authors": [
                            " ".join(author.strip().split())
                            for author in authors.split(";")
                        ],
                    }
                )
        return all_orals

    def parse_pages(self):
        urls = self._find_all_pages()
        all_papers = []
        for k, url in urls.items():
            items = k.split("-")
            paper_type = items[0].strip()
            date = items[1].strip()
            daytime = items[2].strip()
            # 获取网页内容
            if url == self.url:
                dom = self.dom
            else:
                logger.info("download {} ...".format(url))
                html_str = utils.download_html(url)
                dom = utils.parse_dom(html_str)
            # 提取所有的文章
            if "posters" == paper_type:
                papers = self.parse_poster_page(dom)
            elif "orals" == paper_type:
                papers = self.parse_oral_page(dom)
            else:
                raise ValueError("not exist paper type: {}".format(paper_type))
            # 记录
            for paper in papers:
                paper["poster_id"] = date + "-" + paper["poster_id"]
                all_papers.append(paper)
        return all_papers


def test_parse_oral_page():
    cvpr = CVPRParser()
    oral_url = "https://cvpr2022.thecvf.com/orals-621-pm"
    dom = utils.parse_dom(utils.download_html(oral_url))
    orals = cvpr.parse_oral_page(dom)
    print(orals)


def main():
    cvpr = CVPRParser()
    all_papers = cvpr.parse_pages()
    # for paper in all_papers:
    #     print(paper["poster_id"])
    print("number of papers: {}".format(len(all_papers)))
    # 写入到文件
    with open("output/cvpr2022.json", "w") as fid:
        json.dump(all_papers, fid, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    main()
