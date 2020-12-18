import codecs
import csv

def data_write_csv(file_name, datas):
    #file_name为写入CSV文件的路径，datas为要写入数据列
    file_csv = codecs.open(file_name,'w+','utf-8')
    writer = csv.writer(file_csv)
    for i in datas:
        for j in i[1:]:
            x = []
            x.append(i[0].strip())
            x.append(" ".join(j.split()[:-1]))
            x.append(j.split()[-1])
            writer.writerow(x)
    file_csv.close()


def readFile(path):
    with open(path,'r',encoding='utf8') as file:
        lines = file.readlines()
        file.close()
    phrases = []
    for p in lines:
        phrases.append(p.strip('\n'))

    return phrases


def writeFile(path,list):
    with open(path,'w',encoding='utf8')as file:
        for i in list[:-1]:
            file.write(str(i))
            file.write('\n')
        file.write(str(list[-1]))
        file.close()

def writeFileDic(path,dic):
    with open(path,'w',encoding='utf8')as f:
        for key in dic:
            f.writelines('"' + str(key) + '": ' + str(dic[key]))
            f.write('\n')
        f.write('\n')

def write2dList(path,list):
    with open(path,'w',encoding='utf8')as f:
        for i in list:
            if i:
                for j in range(len(i)-1):
                    f.write(i[j])
                    f.write(',')
                f.write(i[-1])
                f.write('\n')
            else:
                f.write('')
                f.write('\n')
        f.close()
