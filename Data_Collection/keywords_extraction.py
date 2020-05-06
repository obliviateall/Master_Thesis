from file_operation import read_file,write_file
from crawler import extract_html_code
from keywords_clean import Deduplication

def keywords_extraction(urllist):
    print("Starting extracting keywords from articles:")
    all = []
    for i in range(len(urllist)):
        article_page = extract_html_code(urllist[i],'.//div/h2[text()="Keywords"]/../div/span')

        for k in range(len(article_page)):
            article_page[k] = article_page[k].xpath('string(.)').strip()
            if not article_page[k] in all:
                all.append(article_page[k])
    print("End")
    return all
# urllist = read_file('Doc_processing/articles_link.txt')
# all = keywords_extraction(urllist)
# all = Deduplication(all)
# write_file('Doc_processing/keywords_from_articles.txt',all)