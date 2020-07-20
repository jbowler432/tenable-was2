import requests
import json
import time
import os.path
from datetime import datetime


# globals

def read_keys():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    print(fileDir)
    f=open(keys_dir+"keys.json","r")
    keys=json.load(f)
    return keys

# sub routines

def export_workbench(id):
	url = "https://cloud.tenable.com/scans/"+id+"/export"
	querystring = {"type":"web-app"}
	payload="{\"format\":\"csv\"}"
	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
	decoded = json.loads(response.text)
	myfile=str(decoded['file'])
	print("File to download = "+myfile)
	f = open("export_workbench.txt","w")
	f.write(myfile)

def check_workbench(id):
	f=open("export_workbench.txt","r")
	mystring=f.read()
	url = "https://cloud.tenable.com/scans/"+id+"/export/"+mystring+"/status"
	querystring={"type":"web-app"}
	response = requests.request("GET", url, headers=headers, params=querystring)
	decoded = json.loads(response.text)
	try:
		return decoded['status']
	except:
		return "error"

def download_workbench(id):
	fread=open("export_workbench.txt","r")
	mystring=fread.read()
	url = "https://cloud.tenable.com/scans/"+id+"/export/"+mystring+"/download"
	querystring={"type":"web-app"}
	response = requests.request("GET", url, headers=headers, params=querystring)
	f=open(id+"_webapp_export.csv","w")
	f.write(response.text.encode('utf8'))

def getit(scanID):
	ready=0
	while ready==0:
		status=check_workbench(scanID)
		print("Job status = "+status)
		if status=="ready":
			ready=1
			print("downloading scan results.....")
			download_workbench(scanID)
			print("download complete")
		elif status=="error":
			ready=100
			print("check status job returned error")
		time.sleep(5)


def getscandetails(id):
	url = "https://cloud.tenable.com/scans/"+id
	response = requests.request("GET", url, headers=headers)
	decoded = json.loads(response.text)
	name=decoded['info']['name']
	owner=decoded['info']['owner']
	targets=decoded['info']['targets']
	if targets is None:
		return "skip" #these are imported web scans. No real interest
	history_id=decoded['history'][0]['history_id']
	history_uuid=decoded['history'][0]['uuid']
	timestamp=decoded['history'][0]['creation_date']
	scan_date=datetime.utcfromtimestamp(int(decoded['history'][0]['creation_date'])).strftime('%Y-%m-%d %H:%M:%S')
	results_file=id+"_webapp_export.csv"
	print(id, owner, name, scan_date, targets, results_file)
	mystring=id.encode('utf8')+"|"+owner.encode('utf8')+"|"+name.encode('utf8')+"|"+scan_date.encode('utf8')+"|"+targets.encode('utf8')+"|"+results_file.encode('utf8')+"|"
	return mystring


def getscans():
	url = "https://cloud.tenable.com/scans"
	response = requests.request("GET", url, headers=headers)
	decoded = json.loads(response.text)
	f = open("scan_list.txt","w")
	lst=[]
	for x in decoded['scans']:
		scanID=str(x['id'])
		owner=str(x['owner'])
		name=str(x['name'])
		type=str(x['type'])
		status=str(x['status'])
		if type=="webapp" and status!="imported":
			mystring=getscandetails(scanID)
			# print mystring
			if (mystring!="skip"):
				print(mystring)
				f.write(mystring+"\n")
				lst.append(mystring)
	return lst

def getscans_was2():
    url = "https://cloud.tenable.com/was/v2/scans"
    querystring = {"ordering":"asc","page":"0","size":"10"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    decoded = json.loads(response.text)
    num_vulns = decoded["total_size"]
    querystring = {"ordering":"asc","page":"0","size":num_vulns}
    response = requests.request("GET", url, headers=headers, params=querystring)
    decoded = json.loads(response.text)
    f = open(results_dir+"scan_list.json","w")
    lst=[]
    for x in decoded['data']:
        scanID=str(x['scan_id'])
        userID=str(x['user_id'])
        target=str(x['application_uri'])
        status=str(x['status'])
        finalised=str(x['finalized_at'])
        configID=str(x['config_id'])
        scan_name=get_scanname(configID)
        time.sleep(1)
        crawled="N/A"
        audited="N/A"
        request_count="N/A"
        if x['metadata'] is not None:
            if "crawled_urls" in x['metadata']:
                crawled=str(x['metadata']['crawled_urls'])
            if "audited_pages" in x['metadata']:
                audited=str(x['metadata']['audited_pages'])
            if "request_count" in x['metadata']:
                request_count=str(x['metadata']['request_count'])
        if status=="completed":
            print(scanID, target, status)
            lst.append({"scanID":scanID,"userID":userID,"target":target,"status":status,"finalised":finalised,"scan_name":scan_name,"crawled":crawled,"audited":audited,"request_count":request_count})
    json_dump=json.dumps(lst)
    f.write(json_dump)
    f.close()
    return lst

def get_scanname(configID):
	url = "https://cloud.tenable.com/was/v2/configs/"+configID
	response = requests.request("GET", url, headers=headers)
	decoded = json.loads(response.text)
	scan_name="Unkown"
	if "name" in decoded:
		scan_name=decoded["name"]
	return scan_name


def get_vulns(scanid):
    myfile=results_dir+str(scanid)+".json"
    if not os.path.isfile(myfile): #only get new scan results
    	print("Getting vulns for scan_uuid = "+scanid)
    	url = "https://cloud.tenable.com/was/v2/scans/"+scanid+"/vulnerabilities"
    	querystring = {"ordering":"asc","page":"0","size":"10"}
    	response = requests.request("GET", url, headers=headers, params=querystring)
    	decoded = json.loads(response.text)
    	num_vulns = decoded["total_size"]
    	querystring = {"ordering":"asc","page":"0","size":num_vulns}
    	response = requests.request("GET", url, headers=headers, params=querystring)
    	decoded = json.loads(response.text)
    	dict_lst=[]
    	for x in decoded["data"]:
    		dict_lst.append(x)
    		pluginID=x["plugin_id"]
    		get_plugin_details(pluginID)
    	f=open(results_dir+scanid+".json","w+")
    	json_dump=json.dumps(dict_lst)
    	f.write(json_dump)
    	f.close()

def get_plugin_details(pluginid):
	myfile=results_dir+str(pluginid)+".json"
	if not os.path.isfile(myfile):
		url = "https://cloud.tenable.com/was/v2/plugins/"+str(pluginid)
		response = requests.request("GET", url, headers=headers)
		decoded = json.loads(response.text)
		f=open(results_dir+str(pluginid)+".json","w+")
		json_dump=json.dumps(decoded)
		f.write(json_dump)
		f.close()
		print("Plugin ID = "+str(pluginid))


def get_report(scanid):
    myfile=results_dir+"report_"+str(scanid)+".json"
    if not os.path.isfile(myfile): #only get new scan results
    	print("Getting report for scan_uuid = "+scanid)
    	url = "https://cloud.tenable.com/was/v2/scans/"+scanid+"/report"
    	response = requests.request("GET", url, headers=headers)
    	decoded = json.loads(response.text)
    	f=open(myfile,"w+")
    	json_dump=json.dumps(decoded)
    	f.write(json_dump)
    	f.close()


# main program
results_dir="../results/"
keys_dir="../"

keys=read_keys()
tio_AK=keys["tio_AK"]
tio_SK=keys["tio_SK"]

api_keys="accessKey="+tio_AK+";secretKey="+tio_SK

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'X-APIKeys': api_keys
    }


scan_lst=getscans_was2()


for x in scan_lst:
	scanID=x["scanID"]
	print("scanID = "+scanID)
	# get_vulns is the old method written before the json export was available
	#get_vulns(scanID)
	# new method based on json report extract
	get_report(scanID)
	time.sleep(1)
