#! /usr/bin/env python
#coding=utf-8

'''
本模块实现模糊综合评估算法的计算。
信息安全因素层次划分表采用树数据结构来保存。
每个因素分别对应树结构中的一个节点。

节点格式说明如下：
{
 id: 标识符,
 pid: 父节点id,
 eval: 专家评价值,
 weight: 权重值,
 cid: 子节点id,
}
'''

__author__ = 'hstaos@gmail.com (Huang Shitao)'

from dataaccess import DataAccess
import numpy
import ahp


class ElementTree:

    def __init__(self, elements):
        self.nodes = {}
        '''初始化树结构'''
        for _each in elements:
            node = {}
            node["id"] = _each[0]
            node["pid"] = _each[1]
            node["eval"] = []
            node["weight"] = 0.0
            node["cid"] = []
            self.nodes[node["id"]] = node
        root = {}
        root["id"] = -1
        root["pid"] = None
        root["eval"] = []
        root["cid"] = []
        self.nodes[root["id"]] = root

        # 建立各个节点间的父子关系
        for _item in self.nodes:
            if self.nodes[_item]["pid"] is not None:
                self.nodes[self.nodes[_item]["pid"]]["cid"].append(_item)

    def set_membership_grade(self, grades):
        for _each in grades:
            self.nodes[_each]["eval"] = grades[_each]

    def set_weight(self, weights):
        for weight in weights:
            self.nodes[weight[0]]["weight"] = weight[1]

    def get_pids(self):
        '''获取所有父节点ID（即所有有子节点的节点）。'''
        pids = {}
        for _id in self.nodes:
            if self.nodes[_id]["cid"]:
                pids[_id] = {}
                pids[_id]["count"] = 0
                pids[_id]["result"] = []
        return pids

    def get_nodes(self):
        return self.nodes

    def fuzzy_synthetic_evaluation(self):
        '''模糊综合评估法'''
        return self.AoR(self.nodes[-1])

    def AoR(self, root={}):
        if root["cid"]:
            _A = []
            _R = []
            for _cid in root["cid"]:
                _A.append(self.nodes[_cid]["weight"])
                _r = self.AoR(self.nodes[_cid])
                _R.append(_r)
            root["eval"] = numpy.dot(_A, _R)
        return root["eval"]


def proc(raw):
    dataaccess = DataAccess(raw)

    elements = dataaccess.get_level_data()
    evals = dataaccess.get_evals()
    classes = dataaccess.get_classes()
    relative_weights = dataaccess.get_weight_result()

    mem_grades = calculate_membership_grade(evals, classes)
    tree = ElementTree(elements)
    tree.set_membership_grade(mem_grades)
    weights = calculate_weight(relative_weights, tree.get_pids(), tree.get_nodes())
    tree.set_weight(weights)
    final_weight = tree.fuzzy_synthetic_evaluation()
    final_score = calculate_final_score(final_weight, classes)
    res = {}
    res["_result"] = final_score
    res["_errorno"] = 0

    return res


def calculate_final_score(final_weight, classes):
        return numpy.dot(final_weight, [each[1] for each in classes])


def calculate_membership_grade(evals, classes):
    '''
    根据专家对叶子因素的安全级别打分，计算每个因素的隶属度。
    （注：仅有叶子节点有专家评估值，也就是说专家只对叶子节点
    所对应的安全因素进行打分。）
    '''
    # uni_ids store the unique element id.
    uni_ids = set()
    for _eval in evals:
        uni_ids.add(_eval[0])

    count = {}
    # Initialize the count.
    for _id in uni_ids:
        count[_id] = {}
        count[_id]["total"] = 0
        for _class in classes:
            count[_id][_class[0]] = 0

    for _each in evals:
        count[_each[0]][_each[1]] += 1
        count[_each[0]]["total"] += 1

    mem_grades = {}
    for _item in count:
        mem_grades[_item] = []
        for _cla in classes:
            eval = count[_item][_cla[0]]/float(count[_item]["total"])
            mem_grades[_item].append(eval)
    return mem_grades


def calculate_weight(relative_weights, pids, nodes):
    '''调用层次分析法来计算各个树节点的权值。'''
    _result, _new_weight_result = build_new_result(relative_weights, pids, nodes)
    _matrixs = build_matrixs(_result, pids, _new_weight_result)
    for _item in _matrixs:
        weight, eigenvalues, eigenvector = ahp.calculate_weight(_matrixs[_item])
        pids[_item]["result"] = weight

    weights = []
    for _each in pids:
        for _cid in nodes[_each]["cid"]:
            weights.append((nodes[_cid]["id"],
                        pids[_each]["result"][_new_weight_result[_cid]]))
    return weights


def build_new_result(relative_weights, pids, nodes):
    result = {}
    #Store the sub index
    new_weight_result = {}
    for _each in relative_weights:
        if nodes[_each[0]]["pid"] in pids:
            if _each[0] not in new_weight_result:
                __x = pids[nodes[_each[0]]["pid"]]["count"]
                new_weight_result[_each[0]] = __x
                pids[nodes[_each[0]]["pid"]]["count"] += 1
            else:
                __x = new_weight_result[_each[0]]

            if _each[1] not in new_weight_result:
                __y = pids[nodes[_each[1]]["pid"]]["count"]
                new_weight_result[_each[1]] = __y
                pids[nodes[_each[1]]["pid"]]["count"] += 1
            else:
                __y = new_weight_result[_each[1]]

            if nodes[_each[0]]["pid"] in result:
                result[nodes[_each[0]]["pid"]].append([__x, __y, _each[2]])
            else:
                result[nodes[_each[0]]["pid"]] = []
                result[nodes[_each[0]]["pid"]].append([__x, __y, _each[2]])
    return result, new_weight_result


def build_matrixs(result, pids, new_weight_result):
    assert isinstance(result, dict)
    assert isinstance(pids, dict)
    assert isinstance(new_weight_result, dict)
    matrixs = {}
    for _each in result:
        matrixs[_each] = numpy.ones(shape=(pids[_each]["count"], pids[_each]["count"]))
        for _item in result[_each]:
            matrixs[_each][_item[0]][_item[1]] = float(_item[2])
    return matrixs
