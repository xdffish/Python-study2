"""Amit 是十二年级A班的班长，他将班上所有学生的记录存储在一个名为“class.dat”的文件中。
记录的结构是[学号, 姓名, 成绩百分比]。他的计算机老师分配给Amit以下任务：

编写一个函数 remcount() 来计算需要补习课的学生数量（成绩低于40%的学生）

 """
# 同时找出获得最高分的学生数量

import pickle

# 学生数据列表
students_list = [
    [1, "Ramya", 30],
    [2, "vaishnavi", 60],
    [3, "anuya", 40],
    [4, "kamala", 30],
    [5, "anuraag", 10],
    [6, "Reshi", 77],
    [7, "Biancaa.R", 100],
    [8, "sandhya", 65],
]

# 将学生数据序列化后存储到文件
with open("class.dat", "ab") as file:
    pickle.dump(students_list, file)
    file.close()

# 计算需要补习的学生数量
def remcount():
    with open("class.dat", "rb") as file:
        students_data = pickle.load(file)
        remedial_count = 0

        # 遍历学生数据，统计成绩低于或等于40%的学生
        for student in students_data:
            if student[2] <= 40:
                print(f"{student} eligible for remedial")
                remedial_count += 1
        print(f"the total number of students are {remedial_count}")

remcount()

# 查找获得最高分的学生
def firstmark():
    with open("class.dat", "rb") as file:
        students_data = pickle.load(file)
        top_marks_count = 0
        scores = [student[2] for student in students_data]

        # 获取最高分
        highest_score = max(scores)
        print(highest_score, "is the first mark")

        file.seek(0)
        # 遍历学生数据，找出获得最高分的学生
        for student in students_data:
            if highest_score == student[2]:
                print(f"{student}\ncongrats")
                top_marks_count += 1

        print("the total number of students who secured top marks are", top_marks_count)

firstmark()

# 读取并打印所有学生数据
with open("class.dat", "rb") as file:
    all_students_data = pickle.load(file)
    print(all_students_data)
