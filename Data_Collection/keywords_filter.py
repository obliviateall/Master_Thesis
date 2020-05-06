from file_operation import read_file,write_file
from keywords_clean import Deduplication
import copy

keywords = read_file('Doc_processing/keywords_from_articles.txt')
keywords_origin = read_file('Doc_processing/keywords_clean.txt')
keywords_copy = copy.deepcopy(keywords)
print(len(keywords))
for k in range(len(keywords_copy)):
    keywords_copy[k] = keywords_copy[k].lower()
    keywords_copy[k] = keywords_copy[k].strip()
    keywords_copy[k] = ''.join(e for e in keywords_copy[k] if e.isalnum())

index = []
counts = []
for i in range(len(keywords_copy)):
    for j in range(i+1,len(keywords_copy)):
        if keywords_copy[j] in keywords_copy[i]:
            counts.append(j)
index = Deduplication(counts)

for k in range(len(index)):
    keywords.remove(keywords[k])
print(len(keywords))
#the code above aims at deleting the same phrases

for q in range(len(keywords)):
    # print(q,keywords[q])
    keywords[q] = keywords[q].lower()
    keywords[q] = keywords[q].strip()

for l in keywords_origin:
    l = l.lower()
    for m in keywords:
        if l in m:
            keywords.remove(m)
print(len(keywords))
#delete those phrases with the original keywords

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
    for n in keywords:
        if v in n:
            keywords.remove(n)
print(len(keywords))
filename = 'Doc_processing/keywords_filter.txt'
write_file(filename,keywords)