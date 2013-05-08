#!/usr/bin/env python

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'


import dataaccess
import numpy
import json
import ahp


def check(data):
	#check the data
	pass


def build_json_result(results=[]):
	pass


def build_level_tree(data):
	_level_data = dataaccess.get_level_data(data)
	_level_tree = {}
	for _each in _level_data:
		_level_node = {}
		_level_node["id"] = _each[0]
		_level_node["pid"] = _each[1]
		_level_node["eval"] = []
		_level_node["weight"] = 0.0
		_level_node["cid"] = []
		_level_tree[_level_node["id"]] = _level_node

	_root_node = {}
	_root_node["id"] = -1
	_root_node["pid"] = None
	_root_node["eval"] = []
	_root_node["cid"] = []
	_level_tree[_root_node["id"]] = _root_node

	for _item in _level_tree:
		if _level_tree[_item]["pid"] is not None:
			_level_tree[_level_tree[_item]["pid"]]["cid"].append(_item)
	return _level_tree


def set_value2level_tree(data, level_tree={}):
	#Get the experts' evaluations.
	_evals = dataaccess.get_evals(data)
	_classes = dataaccess.get_classes(data)
	_count = {}
	_fids = set()

	for _eval in _evals:
		_fids.add(_eval[0])

	#Initialize
	for _fid in _fids:
		_count[_fid] = {}
		_count[_fid]['total'] = 0
		for _class in _classes:
			_count[_fid][_class[0]] = 0

	#calculate the evaluation
	for _each in _evals:
		_count[_each[0]][_each[1]] += 1
		_count[_each[0]]["total"] += 1

	#Set the evaluations to the level tree
	for _item in _count:
		for _cla in _classes:
			level_tree[_item]["eval"].append(float(_count[_item][_cla[0]]) / float(_count[_item]["total"]))


def fuzzy_synthetic_evaluation(data, level_tree={}):
	return aor(level_tree[-1], level_tree)


def aor(root_node={}, level_tree={}):
	if root_node["cid"]:
		_A = []
		_R = []
		for _cid in root_node["cid"]:
			_A.append(level_tree[_cid]["weight"])
			_r = AoR(level_tree[_cid], level_tree)
			_R.append(_r)
		root_node["eval"] = numpy.dot(_A, _R)
	return root_node["eval"]


def calculate_and_set_weight2level_tree(data, level_tree={}):
	_weight_result = dataaccess.get_weight_result(data)
	_fids = get_fids(level_tree)
	_result, _new_weight_result = build_new_result(_weight_result, _fids, level_tree)
	_matrixs = build_matrixs(_result, _fids, _new_weight_result)
	
	for _item in _matrixs:
		weight, eigenvalues, eigenvector = ahp.calculate_weight(_matrixs[_item])
		_fids[_item]["result"] = weight

	for _each in _fids:
		for _cid in level_tree[_each]["cid"]:
			level_tree[_cid]["weight"] = _fids[_each]["result"][_new_weight_result[_cid]]
	

def get_fids(level_tree={}):
	'''Get All parents' id.'''
	fids = {}
	for _id in level_tree:
		if level_tree[_id]["cid"]:
			fids[_id] = {}
			fids[_id]["count"] = 0
			fids[_id]["result"] = []
	return fids
	

def build_matrixs(result={}, fids={}, new_weight_result={}):
	matrixs = {}
	for _each in result:
		matrixs[_each] = numpy.ones(shape=(fids[_each]["count"], fids[_each]["count"]))
		for _item in result[_each]:
			matrixs[_each][_item[0]][_item[1]] = float(_item[2])
	return matrixs


def build_new_result(weight_result=[], fids={}, level_tree={}):
	result = {}
	#Store the sub index
	new_weight_result = {}
	for _each in weight_result:
		if level_tree[_each[0]]["pid"] in fids:
			if _each[0] not in new_weight_result:
				__x = fids[level_tree[_each[0]]["pid"]]["count"]
				new_weight_result[_each[0]] = __x
				fids[level_tree[_each[0]]["pid"]]["count"] += 1
			else:
				__x = new_weight_result[_each[0]]

			if _each[1] not in new_weight_result:
				__y = fids[level_tree[_each[1]]["pid"]]["count"]
				new_weight_result[_each[1]] = __y
				fids[level_tree[_each[1]]["pid"]]["count"] += 1
			else:
				__y = new_weight_result[_each[1]]
	
			if level_tree[_each[0]]["pid"] in result:
				result[level_tree[_each[0]]["pid"]].append([__x, __y, _each[2]])
			else:
				result[level_tree[_each[0]]["pid"]] = []
				result[level_tree[_each[0]]["pid"]].append([__x, __y, _each[2]])
	return result, new_weight_result


def calculate_final_score(data, weights=[]):
	return numpy.dot(weights, [each[1] for each in dataaccess.get_classes(data)])
