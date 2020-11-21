import json
import os


def classify(classStr):
    res = -1  # 返回classStr对应的标签在classes中的下标
    classes = ["Button", "CheckBox", "Chronometer", "EditText", "ImageButton", "ImageView", "ProgressBar",
               "RadioButton", "RatingBar", "SeekBar", "Spinner", "Switch", "ToggleButton", "VideoView", "TextView"]
    for cls in classes:
        if cls in classStr:  # 判断该classStr中是否包含cls，若是则认为属于该类
            res = classes.index(cls)
            if cls == "Button":  # 如果是Button类还需要进一步细分，防止因为顺序带来的"短路"
                if "ImageButton" in classStr:
                    res = classes.index("ImageButton")
                elif "RadioButton" in classStr:
                    res = classes.index("RadioButton")
                elif "ToggleButton" in classStr:
                    res = classes.index("ToggleButton")
            break
    print(classStr, "->", classes[res])
    if res == -1:
        print("Classify error!")
    return res


def lable(element):
    res = []  # 返回一个list，对应YOLO所需打好标签的格式
    lable_idx = -1

    # 去除不可见控件
    if element["visibility"] != "visible":
        return res
    # 去除坐标错误的控件
    classStr = element["class"]
    bounds = element["bounds"]
    if bounds[0] < 0 or bounds[1] < 0 or bounds[2] < 0 or bounds[3] < 0 or bounds[0] > 1440 or bounds[1] > 2560 or \
            bounds[2] > 1440 or bounds[3] > 2560:
        return res

    # 生成YOLO所需格式内容
    if classify(classStr) != -1:
        lable_idx = classify(classStr)
    x_center = ((bounds[0] + bounds[2]) / 2) / 1440
    y_center = ((bounds[1] + bounds[3]) / 2) / 2560
    width = abs((bounds[2] - bounds[0]) / 1440)  # 这个应该不用加abs，但是第一次height算错了，还是加上吧
    height = abs((bounds[1] - bounds[3]) / 2560)

    res = [lable_idx, x_center, y_center, width, height]
    return res


def getChildren(root):
    res = []  # 返回一个list，每个元素是一个有5个元素的list，符合YOLO所需格式
    if type(root) == dict:  # 解决NonType错误
        if "children" in root:
            children = root["children"]
            for i in range(len(children)):
                child = children[i]
                res = res + getChildren(child)  # 递归调用，获得子对象
        res.append(lable(root))
    return res


def parse(imgPath, jsonPath):  # 解析对应的一对jpg和json文件
    # 读取json文件
    file = open(jsonPath, "r")
    content = json.load(file)
    file.close()

    root = content["activity"]["root"]  # 假设所有的root的visibility字段都是"visible"
    children = getChildren(root)

    (path, filename) = os.path.split(jsonPath)
    txtPath = "./annotations" + "/" + os.path.splitext(filename)[0] + ".txt"

    # 将标记后的YOLO所需格式内容写入对应的txt文件
    file = open(txtPath, "w")
    for child in children:
        if len(child) != 0:
            if child[0] != -1:
                file.write(str(child[0]) + " " + str(child[1]) + " " + str(child[2]) + " " + str(child[3]) + " " + str(
                    child[4]) + "\n")
    file.close()


def preprocess():
    print("Preprocessing...")
    path = "./dataset"  # 数据集的路径
    files = os.listdir(path)
    files.sort()
    print("Dataset loaded.")

    for file in files:
        filePath = path + '/' + file
        if os.path.isfile(filePath):  # 判断是否为文件
            if os.path.splitext(filePath)[1] == ".jpg":  # 判断是否为jpg文件
                parse(filePath, os.path.splitext(filePath)[0] + ".json")
                print(file, "parsed.")
    print("All parsed.")

    return


preprocess()
