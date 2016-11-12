import json, sys, os

def is_json(myjson):
  try:
  	with open(myjson) as data_file:    
		json_object = json.load(data_file)
		print("JSON file check passed: "+myjson)
  except ValueError, e:
    print("One of your JSON task definition files has an error: " + myjson)
    print(e)
    print("Try python -m json.tool < THE_FILE_WITH_THE_ERROR for more info.")

if __name__=="__main__":
	json_file_to_check=sys.argv[1]
	is_json(json_file_to_check)