import os
from random import sample


def produceTrainSet():
    print("Producing training set...")
    path = "./dataset"  # 数据集的路径
    files = os.listdir(path)
    files.sort()

    completeSet = []  # 全集
    for file in files:
        filePath = path + '/' + file
        if os.path.isfile(filePath):
            if os.path.splitext(filePath)[1] == ".jpg":  # 判断是否为jpg文件
                newFilePath = "data/custom/images/" + file  # 生成要在YOLO中使用的路径
                completeSet.append(newFilePath)
    trainSet = sample(completeSet, int(0.8 * len(completeSet)))  # 按照80%的比例生成训练集
    validSet = list(set(completeSet) - set(trainSet))
    validSet = sample(validSet, int(0.5 * len(validSet)))  # 按照10%的比例生成验证集
    # testSet = list(set(completeSet) - set(trainSet) - set(validSet))  # 按照10%的比例生成测试集

    # 写入train.txt
    file = open("./config/train.txt", "w")
    for item in trainSet:
        file.write(str(item) + "\n")
    file.close()

    # 写入valid.txt
    file = open("./config/valid.txt", "w")
    for item in validSet:
        file.write(str(item) + "\n")
    file.close()

    print("Training set produced.")
    return

# produceTrainSet()
