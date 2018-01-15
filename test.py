#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from pprint import pprint
import platform

def setupOsVariables(jsondata):
	if VERBOSE:
		print("process os variables")

	loop = 0
	for item in jsondata:

		name = list(item.keys())[0]
		
		if VERBOSE:
			print("name is:", name)
		path = jsondata[loop][name]
		os.environ[name] = path
		loop+=1

def setupCgruVariables(jsondata):
	print("process cgruvariables: \n")
	print(jsondata)

def jsonAssemble_path():
	print("process path")

def jsonAssemble_env(item):

	name = list(item.keys())[0]
	path = item[name]

	if VERBOSE:
		print("env item is:", item)
		print("env name is:", name)
		print("env data is:", path)

	try:
		result = os.environ["OTL"] 		
	except:
		result = None
		print("env not exist ")
	
	return result

def jsonAssemble_folders():
	print("process folders")	

file_directory = "/nas/MainProjects/TarranoBattle/Episodes/36/36-203/Work/Shading-ligting/settings/config.json"
VERBOSE = 0

with open(file_directory, 'r') as f:
    data = json.load(f)

data = data["envvariables"]

for group,items in data.items():
#	print("name of group is:", group)
	if group == 'osvariables':

		setupOsVariables(items[platform.system()])

		if VERBOSE:
			print("process osvariables: \n")
			print("contest:", items)
			print("number of elements:", len(items))
			print("LC_ALL is:", os.environ["LC_ALL"])
			print("LANG is:", os.environ["LANG"])
			print("CGRU_LOCATION is:", os.environ["CGRU_LOCATION"])

	if group == 'cgruvariables':
		setupCgruVariables(items)
				



### Complex env
#for k,v in env_for_system.items():
#	print("name of variable is:", k)
#	print("contest:", v)
#	print("number of elements:", len(v))
#
#	for key in v:
#		print(key)
#		name = list(key.keys())[0]
#		print(name)
#
#		if (name == "path"):
#			print(">>>key length:", key.items())
#
#			for q,w in key.items():
#				print("q is:", q)
#				print("w is:", w[1])
#
#			jsonAssemble_path()
#
#		if(name == "env"):
#			jsonAssemble_env(key)			
#
#loop = 0
#for item in env_for_system:
#	for p in env_for_system[item]:
#		print("item is:", p)
#		print("item type:", type(p))
#		name = list(p.keys())[0]
#		print("name is:", name)
#		path = p[loop][name]
#		#pprint(path)
#		loop+=1
#
#	os.environ[name] = path

