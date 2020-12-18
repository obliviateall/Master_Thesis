# coding=utf-8
#from __future__ import division
import dirichlet
import random
import math
from collections import Counter

class LDA(object):
    def __init__(self, partitioned_docs, index_vocab,score,count, param, num_topics=20, alpha=4, beta=0.01,
                 iterations=2000,optimization_iterations=100, optimization_burnin=50):
        # initialize corpus
        self.documents = partitioned_docs
        self.num_documents = len(partitioned_docs)
        self.index_vocab = index_vocab
        self.num_words = len(index_vocab)
        self.num_topics = num_topics
        self.score = score
        self.count = count
        self.param = param


        # initialize hyperparameters超参数
        self.alpha = [alpha] * self.num_topics
        self.alpha_sum = alpha * num_topics
        self.beta = beta
        self.beta_sum = self.beta * self.num_words

        # gibbs sampling parameters
        self.iterations = iterations
        self.optimization_iterations = optimization_iterations
        self.optimization_burnin = optimization_burnin

    def _initialize(self):
        self._init_documents()
        # Array stores per topic counts
        self.n_t = [0] * self.num_topics
        # 2d array that stores document/topic counts by phrase, and word respectively
        self.n_d_t_phrases = [[0] * self.num_topics for __ in range(self.num_documents)]
        self.n_d_t_words = [[0] * self.num_topics for __ in range(self.num_documents)]
        self.n_t_w = [[0] * self.num_words for __ in range(self.num_topics)]
        # 主题数长度的列表，每个主题对应一个总词数大小的0列表

        self._init_documents_topics()
        self._init_histogram()

    def _init_documents(self):
        self.documents_words = []
        self.max_documents_phrases_count = 0 #docs中含有最多的短语数的一个doc的这个最多短语数
        self.max_documents_words_count = 0 #docs中含有最多的词数的一个doc的这个最多词数

        for document in self.documents:#document对应一个title
            document_words = []
            document_words_count = 0
            for phrase in document:#phrase对应document标题下的几个短语
                for word in phrase.split(): #word对应短语的每个词
                    document_words.append(word)
                    document_words_count += 1
            self.documents_words.append(document_words)
            self.max_documents_phrases_count = max(self.max_documents_phrases_count, len(document))
            self.max_documents_words_count = max(self.max_documents_words_count, document_words_count)


    def _init_documents_topics(self):
        # we assign a random topic to each phrase in the document
        self.documents_phrases_topic = []

        for document_index, document in enumerate(self.documents):
            document_phrases_topic = []
            for phrase_index, phrase in enumerate(document):# 遍历每一个短语

                document_phrase_topic = random.randint(0, self.num_topics - 1)# 在主题数范围内生成一个随机数，也就是为短语随机分配一个主题
                document_phrases_topic.append(document_phrase_topic)# 将分配的整个主题的序号存入列表中

                # Increase counts

                self.n_t[document_phrase_topic] += len(phrase.split())# 将这个短语的长度累加到所分配的主题序号对应的位置上
                self.n_d_t_phrases[document_index][document_phrase_topic] += 1# 对应该论文标题的，生成的随机主题位置上累加1
                self.n_d_t_words[document_index][document_phrase_topic] += len(phrase.split())# 对应该论文标题的，生成的随机主题位置上累加短语长度

                for word_index in phrase.split():# 遍历短语中的每个词
                    self.n_t_w[document_phrase_topic][self.index_vocab.index(word_index)] += 1 # 生成的随机主题上，对应的词的位置累加1
            self.documents_phrases_topic.append(document_phrases_topic) # 将每个论文标题对应的主题序号列表存入一个列表中，二维列表


    def _init_histogram(self):# 直方图
        self.document_length_histogram = [0] * (self.max_documents_words_count + 1)
        # 生成一个总词数（包括重复）+1 长度的0列表-直方图列表
        for document in self.documents_words:# 遍历每一个短语
            self.document_length_histogram[len(document)] += 1 # 直方图列表上词的长度对应的位置上累加1
        self._init_topic_document_histogram()

    def _init_topic_document_histogram(self):
        self.topic_document_histogram = [[int()] * (self.max_documents_words_count + 1)
                                         for __ in range(self.num_topics)]
        # 主题数长度的列表中，每一个主题对应总词数+1长度的0列表

    def _sample_topic(self, sampling_probabilities):
        threshold = random.uniform(0.0, 1.0) * sum(sampling_probabilities)
        # 在[0,1]间产生一个随机数 * 采样概率的和
        cumulative_sum = 0
        # 累计和

        for topic in range(self.num_topics):
            cumulative_sum += sampling_probabilities[topic]# 累加每一个topic的采样概率
            if cumulative_sum > threshold:
                break
        return topic,cumulative_sum

    def _calculate_topic_probabilities(self, document_index, phrase_index):
        topic_probabilities = []
        for topic_index in range(self.num_topics):
            # 遍历每一个主题序号
            left = self.alpha[topic_index] + self.n_d_t_phrases[document_index][topic_index]
            # left变量=该主题对应的alpha参数 + 该文章标题对应下的该主题序号的值
            right = 1.0
            for word_index in self.documents[document_index][phrase_index].split():
                # 遍历每篇文章的每一个主题中的词的索引

                if (self.documents[document_index][phrase_index].split()).index(word_index) == \
                        self.score[document_index][phrase_index]:
                    right *= (self.beta + self.n_t_w[topic_index][self.index_vocab.index(word_index)] * self.param) / (
                            self.beta_sum + (self.n_t[topic_index]))
                else:
                    right *= (self.beta + self.n_t_w[topic_index][self.index_vocab.index(word_index)]) / (
                            self.beta_sum + (self.n_t[topic_index]))
                # right变量=right*（beta参数+ 该主题下对应的该词出现次数）/（beta参数*主题数+（该主题所包含短语总长度））
            topic_probability = left * right
            topic_probabilities.append(topic_probability)
        return topic_probabilities

    def _should_optimize(self, iterations):
        if self.optimization_iterations is None:
            return False
        iterations_condition = ((iterations + 1) % self.optimization_iterations) == 0
        burnin_condition = ((iterations + 1) > self.optimization_burnin)
        return iterations_condition and burnin_condition

    def run(self):
        self._initialize()
        phrases_probabilities={}

        for iteration in range(self.iterations):
            if iteration % 100 == 0:
                print("iteration", iteration)
            sum = 0
            s=0

            for document_index, document in enumerate(self.documents):
                # document 是 partitioned_docs中对应题目的序号列表
                for phrase_index, phrase in enumerate(document):

                    document_phrase_topic = self.documents_phrases_topic[document_index][phrase_index]
                    # 将该文章标题中该短语被随机分配的主题数，赋值给document_phrase_topic

                    # reduce counts for sampling
                    self.n_t[document_phrase_topic] -= len(phrase.split())
                    self.n_d_t_phrases[document_index][document_phrase_topic] -= 1
                    self.n_d_t_words[document_index][document_phrase_topic] -= len(phrase.split())


                    for word_index in phrase.split():
                        self.n_t_w[document_phrase_topic][self.index_vocab.index(word_index)] -= 1

                    # 以上三条是初始化函数的反操作，初始化操作中为累加操

                    sampling_probabilities = self._calculate_topic_probabilities(document_index, phrase_index)
                    document_phrase_topic,prob = self._sample_topic(sampling_probabilities)

                    prob2 = sampling_probabilities[document_phrase_topic]
                    #print(document_phrase_topic,prob)
                    sum += math.log(prob)
                   # phrases_probabilities[phrase]=prob
                    self.documents_phrases_topic[document_index][phrase_index] = document_phrase_topic

                    self.n_t[document_phrase_topic] += len(phrase.split())
                    self.n_d_t_phrases[document_index][document_phrase_topic] += 1
                    self.n_d_t_words[document_index][document_phrase_topic] += len(phrase.split())
                    for word_index in phrase.split():
                        self.n_t_w[document_phrase_topic][self.index_vocab.index(word_index)] += 1


            if self._should_optimize(iteration):
                self._optimize_hyperparameters()



        perplexity = math.exp(-sum / self.count)
        print(perplexity)
        #perplexities.append(perplexity)

        topics = self._getTopics()
        return self.documents_phrases_topic, self._getMostFrequentPhrasalTopics(topics)

    def _optimize_hyperparameters(self):
        self._init_topic_document_histogram()
       # print(self.topic_document_histogram)
        for topic_index in range(self.num_topics):
            for document_index in range(len(self.documents)):
                self.topic_document_histogram[topic_index][self.n_d_t_words[document_index][topic_index]] += 1

        self.alpha_sum = dirichlet.learn_parameters(
            self.alpha, self.topic_document_histogram, self.document_length_histogram)
        max_topic_size = 0

        for topic_index in range(self.num_topics):
            if self.n_t[topic_index] > max_topic_size:
                max_topic_size = self.n_t[topic_index]

        topic_size_histogram = [0] * (max_topic_size + 1)
        count_histogram = [0] * (max_topic_size + 1)

        topic_index = 0
        for topic_index in range(self.num_topics):
            topic_size_histogram[self.n_t[topic_index]] += 1
            for word_index in range(self.num_words):
                count_histogram[self.n_t_w[topic_index][word_index]] += 1

        self.beta_sum = dirichlet.learn_symmetric_concentration(count_histogram, topic_size_histogram, self.num_words, self.beta_sum)
        self.beta = self.beta_sum / self.num_words

    def store_phrase_topics(self, path):
        f = open(path, 'w')
        for document in self.documents_phrases_topic:
            f.write(",".join(str(phrase) for phrase in document))
            f.write("\n")

    def _getTopics(self):
        """
        Returns the set of phrases modelling each document.
        """
        topics = {}

        for document_index, document in enumerate(self.documents_phrases_topic):
            for phrase_index, phrase_topic in enumerate(document):
                phrase = self.documents[document_index][phrase_index]
                topics[phrase] = phrase_topic
        return topics

    def _getMostFrequentPhrasalTopics(self, topics):
        output = [[] for __ in range(self.num_topics)]
        for i in range(self.num_topics):
            for key,value in topics.items():
                if value == i:
                    output[value].append(key)

        return output
