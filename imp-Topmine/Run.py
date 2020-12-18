import data_processing
import PhraseLDA
import fileOperation
from nltk import pos_tag
from copy import deepcopy

# parameters definition
num_topics = 20
iteration = 2000
optimization_burnin = 100
alpha = 4
optimization_iterations = 50
beta = 0.01
param = 1.5


def store_frequent_phrases(frequent_phrases, path='20topics_1.5/frequent_phrases.txt'):
    f = open(path, 'w')
    for phrase, val in enumerate(frequent_phrases):
        f.write(str.format("{0} {1}\n",phrase, val))
    f.close()

def store_most_frequent_topics(most_frequent_topics,dict, prefix_path="20topics_1.5/topic"):
    diction = [[] for __ in range(num_topics)]
    for topic_index,topic in enumerate(most_frequent_topics):
        file_name = prefix_path + str(topic_index)+".txt"
        f = open(file_name, 'w')
        diction[topic_index].append(str(topic_index)+' ')
        for phrase in topic:
            if len(phrase.split())>1:
                f.write(phrase+' ')
                f.write(str(dict[phrase]))
                f.write('\n')
                diction[topic_index].append(phrase+' '+ str(dict[phrase]))
        f.close()
    return diction

titles,words = data_processing.clean('corpus.txt')
phrasesINtitle,word_freq_dic = data_processing.phrases_frequencies(titles,words)
res,phrase_dict,doc = data_processing.get_phrases(phrasesINtitle,words)
fin,freq = data_processing.final_processing(res,phrase_dict)

word_freq_dic.update(phrase_dict)

docs = []
for w in fin:
    a = []
    a.append(w.strip())
    docs.append(a)

vocab = []
v=[]
voc = []
voc_dic = {}
for i in docs:
    v.extend(i)
for w in v:
    voc.extend(w.split())

for j in voc:
    voc_dic[j] = word_freq_dic[j]
    if j not in vocab:
        vocab.append(j.strip())
count = len(voc)

h = pos_tag(vocab)
VERB = ['VBP','VBD','VBG','VBZ','VBN','VB']
NOUN = ['NNS','NN']
AJ = ['RB','RBR','CD','MD','PRP']
AD = ['JJ','JJR']
PROP = ['IN']
vocab_list = []
vocab_tag = []
for i in h:
    vocab_list.append(i[0])
    vocab_tag.append(i[1])
score = []

for document in docs:
    wm=[]
    parameter = []
    for phrase in document:
        words_p = phrase.split()
        wf_list = []
        for f in words_p:
            wf = float(word_freq_dic[f])
            if vocab_tag[vocab_list.index(f)] in NOUN:
                wf = wf * 0.4
            elif vocab_tag[vocab_list.index(f)] in VERB:
                wf = wf * 0.3
            elif vocab_tag[vocab_list.index(f)] in AD:
                wf = wf * 0.2
            else :
                wf = wf * 0.1
            wf_list.append(wf)
        wm.append(wf_list.index(max(wf_list)))
    score.append(wm)

#print(vocab)
plda = PhraseLDA.LDA(docs, vocab, score, count, param, num_topics, alpha, beta, iteration, optimization_iterations, optimization_burnin)
document_phrase_topics, most_frequent_topics = plda.run()
# store_frequent_phrases(document_phrase_topics)
# d = store_most_frequent_topics(most_frequent_topics,word_freq_dic)
#print(end-start)
