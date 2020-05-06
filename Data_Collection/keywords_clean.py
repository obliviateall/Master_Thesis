#delete those keywords with no relevant articles in the database

from crawler import extract_html_code
from file_operation import read_file,write_file

website = "https://www.sciencedirect.com/search/advanced?pub=Computational%20Materials%20Science&cid=271513&tak="

def keywords_cleaning(filename):
    keywords = read_file(filename)
    keywords_url = []
    keywords_filter = []
    for i in range(len(keywords)):
        keywords_url.append(website + keywords[i] +'&show=100')

    print("Cleaning Start!")
    for j in range(len(keywords_url)):
        article_num = extract_html_code(keywords_url[j],"//title/text()")
        article_num = article_num[0].split(' ')[0]
        article_num = int(article_num.replace(',', ''))

        if article_num == 0:
            keywords_filter.append(keywords[j])
    for k in keywords_filter:
        keywords.remove(k)
    keywords.remove('code')
    keywords.remove('files')
    return keywords
# delete the keywords without any relevant article
# keywords = keywords_cleaning('Doc_processing/keywords.txt')
# filename = 'Doc_processing/keywords_clean.txt'
# write_file(filename,keywords)

def Deduplication(list):
    res = []
    for i in range(len(list)):
        if not list[i] in res:
            res.append(list[i])
    return res


