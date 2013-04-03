#! /usr/bin/env python

from database import execute

def getLevelData(v_id):
	sql = "SELECT id, level, pid " \
	+"FROM t_level "  \
	+ "WHERE v_id = " + str(v_id) 
	return execute(sql)

def getEvals(v_id):
	sql = "SELECT t1.fid, t1.cid "\
			+" FROM t_eval_res t1, t_class t2 "\
			+" WHERE t2.v_id = " + str(v_id) \
			+" AND t1.cid = t2.id ;"
	return execute(sql)

def getClasses(v_id):
	sql = "SELECT id, value"\
			+" FROM t_class"\
			+" WHERE v_id = " + str(v_id)\
			+" ORDER BY value DESC"
	return execute(sql)

def getWeightResult(v_id):
	sql = "SELECT fid1, fid2, value" \
			+" FROM t_weight_res"\
			+" WHERE v_id=" + str(v_id)
	return execute(sql)
