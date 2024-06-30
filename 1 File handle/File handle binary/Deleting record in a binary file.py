import pickle
import os
print(os.getcwd())

def bdelete():
    # 打开文件并加载数据
    with open("1 File handle/File handle binary/studrec.dat", "rb") as F:
        stud = pickle.load(F)
        print(stud)

    # 删除用户输入的学号
    rno = int(input("请输入要删除的学号："))
    with open("1 File handle/File handle binary/studrec.dat", "wb") as F:
        rec = [i for i in stud if i[0] != rno]
        pickle.dump(rec, F)

bdelete()
