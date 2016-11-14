# -*-coding: utf-8 -*-
# Create by Jiang Tao on 2016/10/22
from scipy.linalg import norm
from PIL import Image, ImageDraw

def make_list(obj):
    if isinstance(obj, list):
        return obj
    return [obj]

class Node(object):
    def __init__(self, fea, gnd, left=None, right=None, children_dist=1):
        self.__fea = make_list(fea)
        self.__gnd = make_list(gnd)
        self.left = left
        self.right = right
        self.children_dist = children_dist

        self.depth = self.__calc_depth()
        self.height = self.__calc_height()

    def to_dendrogram(self, filename):
        height_factor = 3
        depth_factor = 20
        total_height = int(self.height*height_factor)
        total_depth = int(self.depth*depth_factor) + depth_factor
        im = Image.new('RGBA', (total_depth, total_height))
        draw = ImageDraw.Draw(im)
        self.draw_dendrogram(draw, depth_factor, total_height/2,
                             depth_factor, height_factor, total_depth)
        im.save(filename)


    def draw_dendrogram(self,draw,x,y,depth_factor,height_factor,total_depth):
        if self.is_terminal():
            color_self = ((255,0,0), (0,255,0), (0,0,255))[int(self.__gnd[0])]
            draw.line((x, y, total_depth, y), fill=color_self)
            return color_self
        else:
            y1 = int(y-self.right.height*height_factor/2)
            y2 = int(y+self.left.height*height_factor/2)
            xc = int(x + self.children_dist*depth_factor)
            color_left = self.left.draw_dendrogram(draw, xc, y1, depth_factor,
                                                   height_factor, total_depth)
            color_right = self.right.draw_dendrogram(draw, xc, y2, depth_factor,
                                                     height_factor, total_depth)

            left_depth = self.left.depth
            right_depth = self.right.depth
            sum_depth = left_depth + right_depth
            if sum_depth == 0:
                sum_depth = 1
                left_depth = 0.5
                right_depth = 0.5
            color_self = tuple([int((a*left_depth+b*right_depth)/sum_depth)
                                for a, b in zip(color_left, color_right)])
            draw.line((xc, y1, xc, y2), fill=color_self)
            draw.line((x, y, xc, y), fill=color_self)
            return color_self


    # use Group Average to calculate distance
    def distance(self, other):
        return sum([norm(x1-x2)
                    for x1 in self.__fea
                    for x2 in other.__fea]) \
               / (len(self.__fea)*len(other.__fea))

    def is_terminal(self):
        return self.left is None and self.right is None

    def __calc_depth(self):
        if self.is_terminal():
            return 0
        return max(self.left.depth, self.right.depth) + self.children_dist

    def __calc_height(self):
        if self.is_terminal():
            return 1
        return self.left.height + self.right.height

    def merge(self, other, distance):
        return Node(self.__fea + other.__fea,
                    self.__gnd + other.__gnd,
                    self, other, distance)


def do_clustering(nodes):
    # make a copy, do not touch the original list
    nodes = nodes[:]
    while len(nodes) > 1:
        print("Clustering [%d]..." % len(nodes))
        min_distance = float('inf')
        min_pair = (-1, -1)
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                distance = nodes[i].distance(nodes[j])
                if distance < min_distance:
                    min_distance = distance
                    min_pair = (i, j)
        i, j = min_pair
        node1 = nodes[i]
        node2 = nodes[j]
        del nodes[j] # note should del j first (j > i)
        del nodes[i]
        nodes.append(node1.merge(node2, min_distance))

    return nodes[0]