#! /usr/bin/env python

import getopt, sys
import dataproc

def mainProc(v_id):
	g_level_tree = dataproc.buildLevelTree(v_id)
	dataproc.setValue2LevelTree(v_id, g_level_tree)
	dataproc.calculateAndSetWeight2LevelTree(v_id, g_level_tree)
	g_B = dataproc.fuzzySyntheticEvaluation(v_id, g_level_tree)
	print(dataproc.calculateFinalScore(v_id, g_B))

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:v", ["help", "vid="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for op, value in opts:
		if op == "-i":
			v_id = int(value)
			mainProc(v_id);
		elif op == "-v":
			print("Version: 1.0.0")
		elif op == "-h":
			usage()

def usage():
	print("Use like this : ./riskeval -i 1 .")

if __name__ == "__main__":
	main()
