from file_operation import read_file,write_file
from article_extraction import generate_research_url,generate_pages,get_articles
from keywords_clean import Deduplication,keywords_cleaning
from keywords_extraction import keywords_extraction

#1.get and clean the keywords from MAPI
keywords = keywords_cleaning('Doc_processing/keywords.txt')
filename = 'Doc_processing/keywords_clean.txt'
write_file(filename,keywords)

#2.extract articles
keywords = read_file('Doc_processing/keywords_clean.txt')
research_pages = generate_research_url(keywords)
pages_all = generate_pages(research_pages)
article,links = get_articles(pages_all)
articles = []
articles_links = []
for url in range(len(links)):
    if links[url] not in articles_links:
        articles_links.append(links[url])
        articles.append(article[url])
# articles = Deduplication(articles)
# articles_links = Deduplication(articles_links)

print("Starting writing into files.")
filename_articles = 'Doc_processing/articles.txt'
filename_links = 'Doc_processing/articles_link.txt'
write_file(filename_articles,articles)
write_file(filename_links,articles_links)
print("End")

#3.extract keywords from articles
urllist = read_file('Doc_processing/articles_link.txt')
all = keywords_extraction(urllist)
all = Deduplication(all)
write_file('Doc_processing/keywords_from_articles.txt',all)

