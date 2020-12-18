from fileOperation import readFile,writeFile,writeFileDic,write2dList
from nltk.corpus import stopwords
import re
from nltk import pos_tag


def clean(path):
    corpus = readFile(path)
    phrases = []
    words = []
    for title in corpus:
        if '[Comput. Mater. Sci.' in title:
            index = title.index('[')
            title = title[:index]
        title_lower = title.lower()
        sentences_no_punc = re.sub(r"[^0-9A-Za-z\u0370-\u03ff]",' ', title_lower)
        titles = sentences_no_punc.split()
        words = words + titles
        phrases.append(titles)
    #writeFile('unfinished_files/words.txt',words)
    words_tag = pos_tag(words)
    return phrases,words

def dictionary_op(list):
    dic = {}
    for phrase in list:
        if phrase not in dic:
            dic[phrase.strip()] = 1
        else:
            dic[phrase.strip()] = dic[phrase.strip()] + 1
    return dic

def phrases_frequencies(phrases,words):
    stop = stopwords.words('english')
    stop = stop + ['A', 'a', 'A:', 'the', 'The', 'using', 'determining','many','much',
                   'few','some','via','based','like','towards','vs','regarding','considering',
                   'within','au','al','mg','cu','co','mg','ni','ag','al','zr']
    count = 0
    phrases_indices = []
    dic = dictionary_op(words)
    #writeFileDic('unfinished_files/frequencies.txt', dic)

    for i in range(len(phrases)):
        title_index = [0] * len(phrases[i])
        phrases_indices.append(title_index)
        for j in range(len(phrases[i])):
            count = count + 1
            if dic.__contains__(phrases[i][j]):
                value = dic.get(phrases[i][j])
                if value >= 10 and phrases[i][j] not in stop:
                    phrases_indices[i][j] = value
                else:
                    phrases_indices[i][j] = -1
                    phrases[i][j] = ''
    # writeFile('unfinished_files/words_frequencies.txt', phrases_indices)
    # writeFile('unfinished_files/uncompleted_titles.txt',phrases)
    return phrases,dic

def get_phrases(phrases,words):#
    UN = ['RB', 'RBR','JJ','JJR','IN']
    results = []
    docs = []
    phrase = ''
    for title in phrases:
        r = []
        title.append('')
        for each_word in title:
            if each_word and len(each_word)>1:
                phrase = phrase + each_word + ' '
            elif len(phrase.split()) > 1:
                r.append(phrase)
                results.append(phrase.strip())
                phrase = ''
            else:
                phrase = ''
        docs.append(r)
        #phrase = ''
    # writeFile('unfinished_files/uncompleted_phrases.txt', results)
    # write2dList('unfinished_files/docs.txt',docs)

    words_tag = pos_tag(words)
    words_tags = {}
    for m in words_tag:
        words_tags[m[0]]=m[1]

    t = []
    dic = dictionary_op(results)
    sorted_phrases = sorted(dic.items(), key=lambda e: e[1], reverse=True)
    for tuple in sorted_phrases:
        if tuple[-1] < 10:
            t.append(tuple[0])
    for p in t:
        if len(p.split())>2:
            if words_tags[(p.split()[:-1])[-1]] not in UN:
                t.append(' '.join(p.split()[:-1]).strip())
            t.append(' '.join(p.split()[1:]).strip())
    results.extend(t)
    dict = dictionary_op(results)

    #writeFileDic('phrases_dic.txt',dict)
    sorted_phrases = sorted(dict.items(),key=lambda e: e[1],reverse = True)
    final_res = []
    for tuple in sorted_phrases:
        if tuple[-1] >= 10:
            final_res.append(tuple[0])
    return final_res,dict,docs

def final_processing(lists,dic):
    delete = []
    for i in lists:
        if i.replace(' ','').isdigit():
            delete.append(i)
    for j in delete:
        lists.remove(j)
    fin = {}
    freq = []
    for k in lists:
        v = dic[k]
        fin[k] = v
        freq.append(v)
    # writeFileDic('phrases_frequencies.txt',fin)
    # writeFile('phrases.txt', lists)

    return lists,freq
