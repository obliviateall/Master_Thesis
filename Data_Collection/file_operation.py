import os

def read_file(filename):
    elements = []
    with open(filename, 'r',encoding='utf8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n')
            elements.append(line)
    return elements

def write_file(filename,data_list):
    #os.makedirs('Doc_processing')
    file = open(filename,'w',encoding='utf8')
    for i in data_list:
        file.write(i)
        file.write('\n')
    file.close()