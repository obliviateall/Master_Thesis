from file_operation import read_file,write_file
from keywords_clean import Deduplication
from crawler import extract_html_code
from article_extraction import generate_research_url,generate_pages,get_articles
from keywords_extraction import keywords_extraction

#step1：repeat extracting articles and new keywords
# keywords = read_file('Doc_processing/keywords_filter.txt')
# article_orig = read_file('Doc_processing/articles.txt')
# links_orig = read_file('Doc_processing/articles_link.txt')
# print("Starting researching:")
# re_pages = generate_research_url(keywords)
# all = generate_pages(re_pages)
# article,link = get_articles(all)
# print("Extraction End!")
# print("Deduplication")
#
# articles = []
# links = []
# for i in range(len(link)):
#     if link[i] not in links:
#         articles.append(article[i])
#         links.append(link[i])
#
# print("End!")
# A = []
# L = []
# print("Additional articles:")
# for a in range(len(articles)):
#     if links[a] not in links_orig:
#         if links[a] not in L:
#             A.append(articles[a])
#             L.append(links[a])
# print(len(A),len(L))
# write_file('Doc_processing/additional articles.txt',A)
# write_file('Doc_processing/additional_articles_links.txt',L)
#
# url_list = read_file('Doc_processing/additional_articles_links.txt')
# res = []
# K = keywords_extraction(url_list)
# K = Deduplication(K)
# for k in K:
#     k = k.lower()
#     k = k.strip()
#     if k not in res:
#         if k not in keywords:
#             res.append(k)
# print(len(res))
# write_file('Doc_processing/additional_keywords.txt',res)

#step2:deduplication of new keywords and extract articles
new_keywords = read_file('Doc_processing/additional_keywords.txt')
print(len(new_keywords))
un_relevant = ['algorithm','learning','data','design','calculation','neural network',
               'model','simulation','structure','cluster','regression','system','prediction',
               'throughput','theory','analysis','monte carlo','function','pca','comput','equation',
               'lead','feature extraction','technique','loop','interface','software','matrix',
               'network','drying','thermodynamics','monte-carlo','method','popcorn failure',
               'statistics','coefficient','classification','estimation','sampling',
               'modul','search','k-points','probability','probabilistic','dft','software','matlab',
               'eulerian','first-principles','gga','first principles','experiments','approach',
               'mbj','lsda','strategy','rbfnns','lda','gw','lmto','aim','dna','gpu','pbe',
               'bte','fea','test','rdf','cpa','grain','program','cpu','measurement','newton','negf']
for v in un_relevant:
    for n in new_keywords:
        if v in n:
            new_keywords.remove(n)
print(len(new_keywords))
write_file('Doc_processing/additional_keywords.txt',new_keywords)
articles12 = read_file('Doc_processing/articles.txt')+read_file('Doc_processing/additional articles.txt')
links12 = read_file('Doc_processing/articles_link.txt')+read_file('Doc_processing/additional_articles_links.txt')

print(len(articles12),len(links12))
n_articles,n_links = get_articles(generate_pages(generate_research_url(new_keywords)))
new_articles = []
new_articles_links = []
for n in range(len(n_links)):
    if n_links[n] not in n_links:
        new_articles.append(n_articles[n])
        new_articles_links.append(n_links[n])
print(len(new_articles))

