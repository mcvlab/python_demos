# encoding: utf-8

import pikepdf

# 删除奇数页
with pikepdf.open("./book.pdf") as pdf:
    num_pages = len(pdf.pages)
    # 必须逆序删除，否则索引错乱
    for i in reversed(range(1, num_pages-1, 2)):
        try:
            # 删除页
            del pdf.pages[i]
            #if i % 10 == 1:
            #    print("delete {}-th page".format(i))
        except Exception as e:
            print(e)
    # 保存为新的文件
    pdf.save("new.pdf")
print("process finished.")
