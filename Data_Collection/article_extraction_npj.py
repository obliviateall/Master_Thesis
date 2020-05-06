from crawler import extract_html_code
from file_operation import read_file,write_file

website = "https://www.nature.com/search?journal=npjcompumats"
order = "//div//span[@class='text-gray-light']/text()"
page_num = extract_html_code(website,order)
links = []
if page_num:
    page_num = int(page_num[0].split()[-1])
    page_num = page_num//50 + 1
    for j in range(page_num):
        u = website + "&page=" + str(j+1)
        links.append(u)

article = []
for i in range(len(links)):
    titles = extract_html_code(links[i],"//h2/a")
    for j in range(len(titles)):
        title = titles[j].xpath('string(.)').strip()
        article.append(title)

print(len(article))
write_file('Doc_processing_npj/articels_npj.txt',article)
