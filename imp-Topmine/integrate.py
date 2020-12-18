for i in range(20):
    filename = '20topics_1.5/topic'+str(i)+'.txt'
    with open(filename,'r',encoding='utf8')as f:
        line = f.readline()
        lines = f.readlines()
        f.close()

    new_file = '20topics_1.5/final_topics_1.5.txt'
    with open(new_file,'a+',encoding='utf8')as file:
        file.write(line)
        file.close()
    total_file = "20topics_1.5/all_phrases_1.5.txt"
    with open(total_file,'a+',encoding='utf8')as t:
        t.write(str(i))
        t.write('\n')
        for i in lines:
            t.write(i)
        t.write('\n')
        t.close()

