from preprocess import preprocess
from produceTrainSet import produceTrainSet


def main():
    # 数据预处理
    preprocess()

    # 数据集划分
    produceTrainSet()


if __name__ == '__main__':
    main()
