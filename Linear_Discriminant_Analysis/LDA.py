import time

import numpy as np
from sklearn import preprocessing
from sklearn.datasets import load_digits  # 导入数据


def train(x0, x1):
    m0 = x0.mean(0)  # 求均值
    m1 = x1.mean(0)
    Sw = np.dot((x0 - m0).T, (x0 - m0)) + np.dot((x1 - m1).T, (x1 - m1))
    Sw = np.linalg.pinv(Sw)
    w = Sw.dot(m0 - m1)
    w0 = w.dot(-(m0 + m1) / 2)
    return w, w0


def test(x, w, w0):
    y = x.dot(w)
    flag = y - w0 > 0
    return flag


def run(label0, label1):
    digits = load_digits()
    data = digits.data
    target = digits.target
    # choose train sample:0--999
    train_x = data[0:1000]
    train_y = target[0:1000]
    test_x = data[1000:]
    test_y = target[1000:]
    train_x0 = train_x[train_y == label0, :]
    train_x1 = train_x[train_y == label1, :]
    test_x0 = test_x[test_y == label0, :]
    test_x1 = test_x[test_y == label1, :]

    # 数据标准化
    scaler = preprocessing.StandardScaler().fit(np.concatenate((train_x0, train_x1),
                                                               axis=0))  # preprocessing.StandardScaler().fit()函数用于计算数据的均值和方差,np.concatenate()函数用于将两组数据合并
    train_x0 = scaler.transform(train_x0)  # transform()函数用于将原数据替换为均值和方差
    train_x1 = scaler.transform(train_x1)
    test_x0 = scaler.transform(test_x0)
    test_x1 = scaler.transform(test_x1)

    # 训练模型
    w, w0 = train(train_x0, train_x1)

    # 测试模型
    test_y0 = test(test_x0, w, w0)
    test_y1 = test(test_x1, w, w0)

    # 计算准确率
    correct = np.sum(test_y0) + np.sum(1 - test_y1)
    correct_rate = correct / (test_x0.shape[0] + test_x1.shape[0])
    return correct_rate


a = time.time()
correct_rate = 0
# 将十个数字两两组合分别训练
for i in range(10):
    for j in range(i + 1, 10):
        correct_rate += run(i, j)
print('Correct rate is: {:.2f}%'.format(correct_rate * 100 / 45))
print('cost time is:{:.2f}s'.format(time.time() - a))
