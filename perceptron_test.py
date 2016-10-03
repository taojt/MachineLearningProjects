# -*-coding: utf-8 -*-
# Create by Jiang Tao on 2016/10/3
'''模仿《统计学习方法》中例题2.1，构建从训练数据集合求解感知机的例子，
构建一个三维特征空间，取正例（1，1，1）（2，5，7），负例（-2，-1，-1）
使用原始感知机形式求解'''
import random

if __name__ == '__main__':
    print(__doc__)
    train_set = [(1, 1, -1, 1), (1, -4, 7, 1), (-2, 1, -8, -1)]
    w1 = w2 = w3 = b = 0;
    n = 1  # learning rate = 1
    count = 0  # counters

while True:
    count += 1
    flag = False
    for choice in range(3):
        if train_set[choice][3] * (
                                w1 * train_set[choice][0] + w2 * train_set[choice][1] + w3 * train_set[choice][
                        2] + b) <= 0:
            flag = True
            break

            # flag 为False表明已经收敛不需要再迭代，跳出循环
    if flag is False:
        break

        # 随机选择点迭代
    choice = random.randint(0, 2)

    if train_set[choice][3] * (
                            w1 * train_set[choice][0] + w2 * train_set[choice][1] + w3 * train_set[choice][2] + b) <= 0:
        w1 += n * train_set[choice][3] * train_set[choice][0]
        w2 += n * train_set[choice][3] * train_set[choice][1]
        w3 += n * train_set[choice][3] * train_set[choice][2]
        b += n * train_set[choice][3]

        # print current values
    print('Round: ', count, ':', 'False Classified Point: ', choice + 1, 'w1: ', w1, 'w2: ', w2, 'w3: ', w3, 'b: ', b)

print('The Perceptron model learned is:  sign(%d*x1+ %d*x2 + %d*x3 + %d) ' % (w1, w2, w3, b))
