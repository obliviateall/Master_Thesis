from file_operation import read_file,write_file
from crawler import extract_html_code
from keywords_clean import Deduplication

website = "https://www.sciencedirect.com/search/advanced?pub=Computational%20Materials%20Science&cid=271513&tak="
website2 = "https://www.nature.com/search?q="
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

def generate_research_url(list):#list为需要搜索的keyword列表
    print("Starting generating all research pages:")
    url_lists = []
    for i in range(len(list)):
        key = list[i]
        #website1
        url = website + key +'&show=100'#100 articles per page
        url_lists.append(url)
    print("End")
    return url_lists

def generate_pages(ResearchLink):
    print("Starting generating all pages:")
    links = []
    for i in range(len(ResearchLink)):
        page_num = extract_html_code(ResearchLink[i],"//div/ol[@class='Pagination hor-separated-list']/li/text()")
        if page_num:
            page_num = int(page_num[0].split()[-1])

        # get the all urls for the keyword
            for j in range(page_num):
                u = ResearchLink[i] + '&offset=' + str(j * 100)
                links.append(u)
    print("End")
    return links

def get_articles(links):
    print("Starting getting articles:")
    article = []
    article_link = []
    for i in range(len(links)):
        titles = extract_html_code(links[i],"//h2/span/a")
        title_url = extract_html_code(links[i],"//h2/span/a/@href")
        for j in range(len(titles)):
            title = titles[j].xpath('string(.)').strip()
            #print(title[0])
            article.append(title)
            link = 'https://www.sciencedirect.com' + title_url[j]
            title_url[j] = link
            article_link.append(title_url[j])
    print("End")
    return article,article_link

# keywords = read_file('Doc_processing/keywords_clean.txt')
# research_pages = generate_research_url(keywords)
# pages_all = generate_pages(research_pages)
# articles,articles_links = get_articles(pages_all)
# articles = Deduplication(articles)
# articles_links = Deduplication(articles_links)
#
# print("Starting writing into files.")
# filename_articles = 'Doc_processing/articles.txt'
# filename_links = 'Doc_processing/articles_link.txt'
# write_file(filename_articles,articles)
# write_file(filename_links,articles_links)
#
# print("End")