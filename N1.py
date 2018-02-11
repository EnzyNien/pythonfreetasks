import os
import tempfile
import json
import argparse


def Actions(key=None,value=None,filename='storage.data'):

	storage_path = os.path.join(tempfile.gettempdir(), filename)

	if os.path.exists(storage_path):
		with open(storage_path, "r") as f:
			readJson = json.load(f)
	else:
		with open(storage_path, "w") as f:
			readJson = {"keys":[],"values":{}}
			json.dump(readJson,f)

	if value is None:
		values = readJson['values'].get(key,[])
		print("key {}, values: {}". format(key,", ".join([str(i) for i in values])))
		return

	if key in readJson['keys']:
		valuesList = readJson['values'][key]
		valuesList.append(value)
		readJson['values'][key] = valuesList
	else:
		keysList = readJson['keys']
		keysList.append(key)
		readJson['keys'] = keysList
		readJson['values'].update({key:[value]})
	
	with open(storage_path, "w") as f:
		json.dump(readJson,f)


def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-key","-k", type = str, help ="parameters - key. type - str")
	parser.add_argument("-value","-v", type = str, help ="parameters - value. type - str")
	
	args= parser.parse_args()
	if args.key is None:
		print("Error. -key is not defined")
		return
	_key = str(args.key)
	_value = args.value
	Actions(_key,_value)


if __name__ == '__main__':
	main()
