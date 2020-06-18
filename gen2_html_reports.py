import requests
import json
import sys
import time
import csv
from datetime import datetime, timedelta


def anychart(show_xaxis,stepy,maxy,type,xaxis_labels,data_lst,labels_lst,brcolors_lst,bgcolors_lst,fill_lst,chart_id):
	count=1
	last=len(data_lst)
	chart_string='<script>\n'\
	'var '+chart_id+' = document.getElementById("'+chart_id+'").getContext("2d");\n'\
	'var '+chart_id+' = new Chart('+chart_id+', \n'\
	'{\n'\
	'type: "'+type+'",\n'\
	' \n'\
	'// The data for our dataset\n'\
	'data: {\n'\
	'labels: '+xaxis_labels+',\n'\
	'datasets: [\n'
	for data in data_lst:
		labelStr='\n{\nlabel: "'+labels_lst[count-1]+'",\n'
		backColorStr='backgroundColor: "'+bgcolors_lst[count-1]+'",\n'
		borderColorStr='borderColor: "'+brcolors_lst[count-1]+'",\n'
		borderWidthStr='borderWidth: "2",\n'
		dataStr='data: '+data+',\n'
		fillStr='fill: '+fill_lst[count-1]+',\n'
		interp="cubicInterpolationMode: 'monotone'\n"
		chart_string=chart_string+labelStr+backColorStr+borderColorStr+borderWidthStr+dataStr+fillStr+interp
		if count==last:
			chart_string=chart_string+"\n}]\n"
		else:
			chart_string=chart_string+"\n},\n"
		count=count+1
	chart_string=chart_string+'\n},\n'\
	'options: {\n'\
	'	legend: {\n'\
	'	display: true,\n'\
	"	position: 'bottom'\n},\n"\
	'	scales: {\n'\
	'	yAxes: [{\n'\
	'		stacked: false,\n'\
	'		ticks: {\n'\
	'		beginAtZero: true,\n'\
	'		max: '+maxy+',\n'\
	'		stepSize: '+stepy+'\n'\
	'		}\n'\
	'		}],\n'\
	'	xAxes: [{\n'\
	'		display: '+show_xaxis+',\n'\
	'		}]\n'\
	'	}\n'\
	'}\n'\
	'});\n'\
	'</script>\n'
	return chart_string

def chartwithtitle(title,ces_color,show_xaxis,stepy,maxy,type,xaxis_labels,data_lst,labels_lst,brcolors_lst,bgcolors_lst,fill_lst,chart_id):
	count=1
	last=len(data_lst)
	chart_string='<script>\n'\
	'var '+chart_id+' = document.getElementById("'+chart_id+'").getContext("2d");\n'\
	'var '+chart_id+' = new Chart('+chart_id+', \n'\
	'{\n'\
	'type: "'+type+'",\n'\
	' \n'\
	'// The data for our dataset\n'\
	'data: {\n'\
	'labels: '+xaxis_labels+',\n'\
	'datasets: [\n'
	for data in data_lst:
		labelStr='\n{\nlabel: "'+labels_lst[count-1]+'",\n'
		backColorStr='backgroundColor: "'+bgcolors_lst[count-1]+'",\n'
		borderColorStr='borderColor: "'+brcolors_lst[count-1]+'",\n'
		borderWidthStr='borderWidth: "2",\n'
		dataStr='data: '+data+',\n'
		fillStr='fill: '+fill_lst[count-1]+',\n'
		interp="cubicInterpolationMode: 'monotone'\n"
		chart_string=chart_string+labelStr+backColorStr+borderColorStr+borderWidthStr+dataStr+fillStr+interp
		if count==last:
			chart_string=chart_string+"\n}]\n"
		else:
			chart_string=chart_string+"\n},\n"
		count=count+1
	chart_string=chart_string+'\n},\n'\
	'options: {\n'\
	'	legend: {\n'\
	'	display: true,\n'\
	"	position: 'bottom'\n},\n"\
	'	title: {\n'\
	'		display: true,\n'\
	'		fontSize: 24,\n'\
	"		fontColor: '"+ces_color+"',\n"\
	"		text: '"+title+"'\n"\
	'	},\n'\
	'	scales: {\n'\
	'	yAxes: [{\n'\
	'		stacked: false,\n'\
	'		ticks: {\n'\
	'		beginAtZero: true,\n'\
	'		max: '+maxy+',\n'\
	'		stepSize: '+stepy+'\n'\
	'		}\n'\
	'		}],\n'\
	'	xAxes: [{\n'\
	'		display: '+show_xaxis+',\n'\
	'		}]\n'\
	'	}\n'\
	'}\n'\
	'});\n'\
	'</script>\n'
	return chart_string

def doughchart(chart_id,dataset,colors,labels,title):
	count=1
#	last=len(data_lst)
	chart_string='<script>\n'\
	'var '+chart_id+' = document.getElementById("'+chart_id+'").getContext("2d");\n'\
	'var '+chart_id+' = new Chart('+chart_id+',\n'\
	'{\n'\
	'type: "doughnut",\n'\
	'data: {\n'\
	'	datasets: [{\n'\
	'		data: '+dataset+',\n'\
	'		backgroundColor: '+colors+',\n'\
	"		label: 'Dataset 1'\n"\
	'	}],\n'\
	"	labels: "+labels+"\n"\
	'},\n'\
	'options: {\n'\
	'	responsive: true,\n'\
	'	cutoutPercentage: 80,\n'\
	'	legend: {\n'\
	"		position: 'right',\n"\
	'	},\n'\
	'	title: {\n'\
	'		display: true,\n'\
	'		fontSize: 20,\n'\
	"		fontColor: '#000',\n"\
	"		text: "+title+"\n"\
	'	},\n'\
	'	animation: {\n'\
	'		animateScale: true,\n'\
	'		animateRotate: true\n'\
	'	}\n'\
	'}\n'\
	'});\n'\
	'</script>\n'
	return chart_string




def write_html_header(f):
	html_header='<html>\n'\
		'<head>\n'\
		'<title>WAS Report</title>\n'\
		'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n'\
		'<meta http-equiv="Pragma" content="no-cache" /><meta http-equiv="Expires" content="0" />\n'
	f.write(html_header)
	#
	# readin style sheet
	f2=open("style.css","r")
	for line in f2:
		f.write(line)
	f2.close()
	f.write('<script>\n')
	#
	# read in javascrip file for producing graphs
	f2=open("Chart.min.js","r")
	for line in f2:
		f.write(line)
	f2.close()
	f.write('</script>\n')
	#f2=open(input_dir+"insert_javascript.txt","r")
	#for line in f2:
	#	f.write(line)
	#f2.close()
	f.write('</head>\n<body>\n')

def clean_string(mystr):
	return_str=mystr.replace("<","&lt;")
	return_str=return_str.replace(">","&gt;")
	return_str=return_str.replace("\n","<br>")
	return return_str

def get_severity(pluginid):
	fin=open(results_dir+str(pluginid)+".json","r")
	data=json.load(fin)
	fin.close
	severity=data["risk_factor"]
	#print severity
	return severity

def get_name(pluginid):
	fin=open(results_dir+str(pluginid)+".json","r")
	data=json.load(fin)
	fin.close
	name=data["name"]
	#print severity
	return name

def print_plug_summary2(pluginid,vuln_count,fout):
        fin=open(results_dir+str(pluginid)+".json","r")
        data=json.load(fin)
        fin.close
        severity=data["risk_factor"]
        name=data["name"]
        family=data["family"]
        fout.write('<table width=900px>\n')
        fout.write("<tr><td align=left width=80px><b>Plugin ID</b></td><td width=80px align=center><b><a href='#"+pluginid+"'>"+pluginid+"</a></b></td><td width=100px align=center class="+severity+">"+severity+"</td><td width=20px>&nbsp;</td><td>"+name+"</td>\n")
        fout.write('</table>\n')


def print_plug_summary(pluginid,vuln_count,fout):
        fin=open(results_dir+str(pluginid)+".json","r")
        data=json.load(fin)
        fin.close
        severity=data["risk_factor"]
        name=data["name"]
        family=data["family"]
        fout.write("<tr><td class="+severity+">"+severity+"</td><td align=center><a href='#"+pluginid+"'>"+pluginid+"</a></yd><td>"+name+"</td><td>"+family+"</td><td align=center>"+str(vuln_count)+"</td>\n")



def print_plugin_data(pluginid,fout):
	fin=open(results_dir+str(pluginid)+".json","r")
	data=json.load(fin)
	fin.close
	fout.write('<table width=900px>\n')
	fout.write("<tr><td>&nbsp;</td>\n")
	fout.write("<tr><td><b>Description</b></td>\n")
	fout.write("<tr><td>"+clean_string(data["description"])+"</td>\n")
	if "solution" in data:
		if data["solution"] is not None:
			fout.write("<tr><td>&nbsp;</td>\n")
			fout.write("<tr><td><b>Solution</b></td>\n")
			fout.write("<tr><td>"+clean_string(str(data["solution"]))+"</td>\n")
	see_also=data["see_also"]
	if len(see_also)>0:
		fout.write("<tr><td>&nbsp;</td>\n")
		fout.write("<tr><td><b>See Also</b></td>\n")
		for x in see_also:
			fout.write("<tr><td>"+x+"</td>\n")
	fout.write('</table>\n')


def print_plugin_data2(data,fout):
	fout.write('<table width=900px>\n')
	fout.write("<tr><td>&nbsp;</td>\n")
	fout.write("<tr><td><b>Description</b></td>\n")
	fout.write("<tr><td>"+clean_string(data["description"])+"</td>\n")
	if "solution" in data:
		if data["solution"] is not None:
			fout.write("<tr><td>&nbsp;</td>\n")
			fout.write("<tr><td><b>Solution</b></td>\n")
			fout.write("<tr><td>"+clean_string(str(data["solution"]))+"</td>\n")
	see_also=data["see_also"]
	if len(see_also)>0:
		fout.write("<tr><td>&nbsp;</td>\n")
		fout.write("<tr><td><b>See Also</b></td>\n")
		for x in see_also:
			fout.write("<tr><td>"+x+"</td>\n")
	fout.write('</table>\n')


def plug_counts_detailed(scanid,fout,severity):
	fin=open(results_dir+str(scanid)+".json","r")
	data=json.load(fin)
	fin.close()
	plug_counts={}
	plug_uris={}

	for x in data:
		pluginID=str(x["plugin_id"])
		uri=str(x["uri"])
		vuln_id=x["vuln_id"]
		risk=get_severity(pluginID)
		if risk==severity:
			if pluginID in plug_counts:
				current_count=plug_counts[pluginID]
				new_count=current_count+1
				plug_counts.update({pluginID:new_count})
			else:
				plug_counts.update({pluginID:1})
			if pluginID in plug_uris:
				if uri is not None:
					lst=plug_uris[pluginID]
					mystring="<a href='#"+vuln_id+"'>"+uri+"</a>"
					lst.append(mystring)
					plug_uris.update({pluginID:lst})
			else:
				if uri is not None:
					lst=[]
					mystring="<a href='#"+vuln_id+"'>"+uri+"</a>"
					lst.append(mystring)
					plug_uris.update({pluginID:lst})
	sort_plugs=sorted(plug_counts.items(), key=lambda x: x[1], reverse=True)
	if len(sort_plugs)>0:
		for i in sort_plugs:
			fout.write('<div class=bar_chart_fl id="'+i[0]+'">\n')
			print_plug_summary2(i[0],i[1],fout)
			fout.write('<table width=900px>\n')
			fout.write("<tr><td>&nbsp;</td>\n")
			fout.write('<tr><td><b>Instances</b></td>\n')
			fout.write('</table>\n')
			fout.write('<table width=900px>\n')
			for y in plug_uris.items():
				if i[0]==y[0]:
					for j in y[1]:
						fout.write("<tr><td>"+j+"</td>\n")
			fout.write('</table>\n')
			print_plugin_data(i[0],fout)
			fout.write('</div>')
			fout.write('<table width=100%></table>')


def plug_counts_detailed2(data,fout,severity):
	plug_counts={}
	plug_uris={}
	plug_details=[]
	count=0
	for x in data["findings"]:
		pluginID=str(x["plugin_id"])
		uri=str(x["uri"])
		risk=x["risk_factor"]
		name=x["name"]
		family=x["family"]
		synopsis=x["synopsis"]
		see_also=x["see_also"]
		output=x["output"]
		solution=x["solution"]
		description=x["description"]
		plug_details.append({"pluginID":pluginID,"name":name,"family":family,"risk":risk,"synopsis":synopsis,"see_also":see_also,"output":output,"solution":solution,"description":description})
		vuln_id=str(count) # need to make up our own ID as its not in the json report export
		if risk==severity:
			if pluginID in plug_counts:
				current_count=plug_counts[pluginID]
				new_count=current_count+1
				plug_counts.update({pluginID:new_count})
			else:
				plug_counts.update({pluginID:1})
			if pluginID in plug_uris:
				if uri is not None:
					lst=plug_uris[pluginID]
					mystring="<a href='#"+vuln_id+"'>"+uri+"</a>"
					lst.append(mystring)
					plug_uris.update({pluginID:lst})
			else:
				if uri is not None:
					lst=[]
					mystring="<a href='#"+vuln_id+"'>"+uri+"</a>"
					lst.append(mystring)
					plug_uris.update({pluginID:lst})
		count=count+1
	sort_plugs=sorted(plug_counts.items(), key=lambda x: x[1], reverse=True)
	if len(sort_plugs)>0:
		for i in sort_plugs:
			vuln_count=i[1]
			pluginid=str(i[0])
			fout.write('<div class=bar_chart_fl id="'+i[0]+'">\n')
			for j in plug_details:
				if j["pluginID"]==i[0]:
					plug_data=j
					severity=j["risk"]
					name=j["name"]
					family=j["family"]
			fout.write('<table width=900px>\n')
			fout.write("<tr><td align=left width=80px><b>Plugin ID</b></td><td width=80px align=center><b><a href='#"+pluginid+"'>"+pluginid+"</a></b></td><td width=100px align=center class="+severity+">"+severity+"</td><td width=20px>&nbsp;</td><td>"+name+"</td>\n")
			fout.write('</table>\n')
			#print_plug_summary2(i[0],i[1],fout)
			fout.write('<table width=900px>\n')
			fout.write("<tr><td>&nbsp;</td>\n")
			fout.write('<tr><td><b>Instances</b></td>\n')
			fout.write('</table>\n')
			fout.write('<table width=900px>\n')
			for y in plug_uris.items():
				if i[0]==y[0]:
					for j in y[1]:
						fout.write("<tr><td>"+j+"</td>\n")
			fout.write('</table>\n')
			print_plugin_data2(plug_data,fout)
			fout.write('</div>')
			fout.write('<table width=100%></table>')


def plug_outputs(data,fout,severity):
	plug_counts={}
	plug_uris={}
	plug_details=[]
	count=0
	for x in data["findings"]:
		pluginID=str(x["plugin_id"])
		uri=str(x["uri"])
		risk=x["risk_factor"]
		name=x["name"]
		family=x["family"]
		synopsis=x["synopsis"]
		see_also=x["see_also"]
		output=x["output"]
		solution=x["solution"]
		description=x["description"]
		plug_details.append({"pluginID":pluginID,"name":name,"family":family,"risk":risk,"synopsis":synopsis,"see_also":see_also,"output":output,"solution":solution,"description":description})
		vuln_id=str(count) # need to make up our own ID as its not in the json report export
		if risk==severity:
			if pluginID in plug_counts:
				current_count=plug_counts[pluginID]
				new_count=current_count+1
				plug_counts.update({pluginID:new_count})
			else:
				plug_counts.update({pluginID:1})
			if pluginID in plug_uris:
				if uri is not None:
					lst=plug_uris[pluginID]
					sublst=[]
					uristring="<tr><td id="+vuln_id+">"+uri+"</td>\n"
					sublst.append(uristring)
					sublst.append(output)
					lst.append(sublst)
					plug_uris.update({pluginID:lst})
			else:
				if uri is not None:
					lst=[]
					sublst=[]
					uristring="<tr><td id="+vuln_id+">"+uri+"</td>\n"
					sublst.append(uristring)
					sublst.append(output)
					lst.append(sublst)
					plug_uris.update({pluginID:lst})
		count=count+1
	sort_plugs=sorted(plug_counts.items(), key=lambda x: x[1], reverse=True)
	if len(sort_plugs)>0:
		for i in sort_plugs:
			vuln_count=i[1]
			pluginid=str(i[0])
			fout.write('<div class=bar_chart_fl id="'+i[0]+'">\n')
			for j in plug_details:
				if j["pluginID"]==i[0]:
					plug_data=j
					severity=j["risk"]
					name=j["name"]
					family=j["family"]
			fout.write('<table width=900px>\n')
			fout.write("<tr><td align=left width=80px><b>Plugin ID</b></td><td width=80px align=center><b>"+pluginid+"</b></td><td width=100px align=center class="+severity+">"+severity+"</td><td width=20px>&nbsp;</td><td>"+name+"</td>\n")
			fout.write('</table>\n')
			#print_plug_summary2(i[0],i[1],fout)
			fout.write('<table width=900px>\n')
			fout.write("<tr><td>&nbsp;</td>\n")
			fout.write('<tr><td><b>Plugin Outputs</b></td>\n')
			fout.write('</table>\n')
			fout.write('<table width=900px>\n')
			for y in plug_uris.items():
				if i[0]==y[0]:
					for j in y[1]:
						fout.write(j[0])
						if j[1] is not None:
							fout.write('<tr><td class=plugout width=600px><pre>'+clean_string(j[1])+"</pre></td><td>&nbsp;</td>\n")
			fout.write('</table>\n')
			#print_plugin_data2(plug_data,fout)
			fout.write('</div>')
			fout.write('<table width=100%></table>')



def plug_counts(scanid,fout,severity):
	fin=open(results_dir+scanid+".json","r")
	data=json.load(fin)
	fin.close()
	plug_counts={}
	plug_uris={}

	for x in data:
		pluginID=str(x["plugin_id"])
		uri=str(x["uri"])
		risk=get_severity(pluginID)
		if risk==severity:
			if pluginID in plug_counts:
				current_count=plug_counts[pluginID]
				new_count=current_count+1
				plug_counts.update({pluginID:new_count})
			else:
				plug_counts.update({pluginID:1})
			if pluginID in plug_uris:
				if uri is not None:
					lst=plug_uris[pluginID]
					lst.append(uri)
					plug_uris.update({pluginID:lst})
			else:
				if uri is not None:
					lst=[]
					lst.append(uri)
					plug_uris.update({pluginID:lst})
	sort_plugs=sorted(plug_counts.items(), key=lambda x: x[1], reverse=True)
	if len(sort_plugs)>0:
		fout.write('<div class=bar_chart_fl>\n')
		fout.write('<table class=table1 width=900px>')
		fout.write('<tr><td width=10%>Severity</td><td width=15% align=center>Plugin ID</td><td width=45% align=center>Plugin Name</td><td width=25% align=center>Family</td><td align=center>Vulns</td>')
		for i in sort_plugs:
			print_plug_summary(i[0],i[1],fout)
		fout.write('</table>')
		fout.write('</div>')
		fout.write('<table width=100%></table>')



def plug_counts2(data,fout,severity):
	plug_counts={}
	plug_uris={}
	plug_details=[]
	for x in data["findings"]:
		pluginID=str(x["plugin_id"])
		uri=str(x["uri"])
		risk=x["risk_factor"]
		name=x["name"]
		family=x["family"]
		plug_details.append({"pluginID":pluginID,"name":name,"family":family,"risk":risk})
		if risk==severity:
			if pluginID in plug_counts:
				current_count=plug_counts[pluginID]
				new_count=current_count+1
				plug_counts.update({pluginID:new_count})
			else:
				plug_counts.update({pluginID:1})
			if pluginID in plug_uris:
				if uri is not None:
					lst=plug_uris[pluginID]
					lst.append(uri)
					plug_uris.update({pluginID:lst})
			else:
				if uri is not None:
					lst=[]
					lst.append(uri)
					plug_uris.update({pluginID:lst})
	sort_plugs=sorted(plug_counts.items(), key=lambda x: x[1], reverse=True)
	if len(sort_plugs)>0:
		fout.write('<div class=bar_chart_fl>\n')
		fout.write('<table class=table1 width=900px>')
		fout.write('<tr><td width=10%>Severity</td><td width=15% align=center>Plugin ID</td><td width=45% align=center>Plugin Name</td><td width=25% align=center>Family</td><td align=center>Vulns</td>')
		for i in sort_plugs:
			for j in plug_details:
				if j["pluginID"]==i[0]:
					risk=j["risk"]
					name=j["name"]
					family=j["family"]
			fout.write("<tr><td class="+risk+">"+risk+"</td><td align=center><a href='#"+str(i[0])+"'>"+str(i[0])+"</a></yd><td>"+name+"</td><td>"+family+"</td><td align=center>"+str(i[1])+"</td>\n")
		fout.write('</table>')
		fout.write('</div>')
		fout.write('<table width=100%></table>')



def print_vulns(scanid,fout,severity):
	fin=open(results_dir+scanid+".json","r")
	data=json.load(fin)
	fin.close()
	for x in data:
		vuln_id=x["vuln_id"]
		plugin_id=x["plugin_id"]
		risk=get_severity(plugin_id)
		name=get_name(plugin_id)
		if risk==severity:
			uri=x["uri"]
			details=x["details"]
			attachments=x["attachments"]
			fout.write('<div class=bar_chart_fl id='+vuln_id+'>\n')
			fout.write('<table width=900px>\n')
			fout.write('<tr><td width=70px><b>'+str(plugin_id)+'</b></td><td class='+severity+' width=100px>'+severity+'</td><td width=20px>&nbsp;</td><td>'+uri+'</td>\n')
			fout.write('<tr><td colspan=4>'+name+'</td>\n')
			fout.write('</table>\n')
			if "output" in details:
				fout.write('<table>\n')
				fout.write("<tr><td>&nbsp;</td>\n")
				fout.write('<tr><td><b>Plugin Output</b></td>\n')
				fout.write('</table>\n')
				fout.write('<table width=600px>\n')
				fout.write('<tr><td class=plugout><pre>'+clean_string(details["output"])+"</pre></td>\n")
				fout.write('</table>')
			if "proof" in details:
				fout.write('<table>\n')
				fout.write("<tr><td>&nbsp;</td>\n")
				fout.write('<tr><td><b>Proof</b></td>\n')
				fout.write('</table>\n')
				fout.write('<table width=600px>\n')
				fout.write('<tr><td class=plugout><pre>'+clean_string(details["proof"])+"</pre></td>\n")
				fout.write('</table>')
			fout.write('</div>')
			fout.write('<table width=100%></table>')


def print_summary(scanid,fout):
	fin=open(results_dir+scanid+".json","r")
	data=json.load(fin)
	fin.close()
	vuln_count=0
	high_count=0
	crit_count=0
	med_count=0
	low_count=0
	info_count=0
	for x in data:
		pluginID=x["plugin_id"]
		severity=get_severity(pluginID)
		if severity=="critical":
			crit_count=crit_count+1
		elif severity=="high":
			high_count=high_count+1
		elif severity=="medium":
			med_count=med_count+1
		elif severity=="low":
			low_count=low_count+1
		elif severity=="info":
			info_count=info_count+1
		vuln_count=vuln_count+1
	#
	fout.write('<div class=bar_chart_fl>\n')
	fout.write('<table width=300px><tr><td align=center><h2>Vulnerability Breakdown</h2></td></table>')
	fout.write('<table class=table1 width=300px>\n')
	fout.write('<tr><td width=200px>Critical Vulnerabilities</td><td class=critical width=50px align=center>'+str(crit_count)+'</td>\n')
	fout.write('<tr><td width=200px>High Vulnerabilities</td><td class=high width=50px align=center>'+str(high_count)+'</td>\n')
	fout.write('<tr><td width=200px>Medium Vulnerabilities</td><td class=medium width=50px align=center>'+str(med_count)+'</td>\n')
	fout.write('<tr><td width=200px>Low Vulnerabilities</td><td class=low width=50px align=center>'+str(low_count)+'</td>\n')
	fout.write('<tr><td width=200px>Informational Items</td><td class=info width=50px align=center>'+str(info_count)+'</td>\n')
	#fout.write('<tr><td width=200px>Total Vulnerabilities</td><td width=50px align=center>'+str(vuln_count)+'</td>\n')
	fout.write('</table>')
	fout.write('</div>')

def print_summary2(data,fout):
	vuln_count=0
	high_count=0
	crit_count=0
	med_count=0
	low_count=0
	info_count=0
	for x in data["findings"]:
		pluginID=x["plugin_id"]
		severity=x["risk_factor"]
		if severity=="critical":
			crit_count=crit_count+1
		elif severity=="high":
			high_count=high_count+1
		elif severity=="medium":
			med_count=med_count+1
		elif severity=="low":
			low_count=low_count+1
		elif severity=="info":
			info_count=info_count+1
		vuln_count=vuln_count+1
	#
	fout.write('<div class=bar_chart_fl>\n')
	fout.write('<table width=300px><tr><td align=center><h2>Vulnerability Breakdown</h2></td></table>')
	fout.write('<table class=table1 width=300px>\n')
	fout.write('<tr><td width=200px>Critical Vulnerabilities</td><td class=critical width=50px align=center>'+str(crit_count)+'</td>\n')
	fout.write('<tr><td width=200px>High Vulnerabilities</td><td class=high width=50px align=center>'+str(high_count)+'</td>\n')
	fout.write('<tr><td width=200px>Medium Vulnerabilities</td><td class=medium width=50px align=center>'+str(med_count)+'</td>\n')
	fout.write('<tr><td width=200px>Low Vulnerabilities</td><td class=low width=50px align=center>'+str(low_count)+'</td>\n')
	fout.write('<tr><td width=200px>Informational Items</td><td class=info width=50px align=center>'+str(info_count)+'</td>\n')
	#fout.write('<tr><td width=200px>Total Vulnerabilities</td><td width=50px align=center>'+str(vuln_count)+'</td>\n')
	fout.write('</table>')
	fout.write('</div>')




def print_report(x):
	scanid=x["scanID"]
	uri=x["target"]
	finalised=x["finalised"]
	scan_name=x["scan_name"]
	crawled=x["crawled"]
	audited=x["audited"]
	request_count=x["request_count"]
	fin=open(results_dir+scanid+".json","r")
	fout=open(reports_dir+scanid+".html","w+")
	data=json.load(fin)
	fin.close()
	write_html_header(fout)
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>WAS Report</h1>')
	fout.write('<table width=100%></table></div>')
	print_summary(scanid,fout)
	fout.write('<div class=bar_chart_fl>\n')
	fout.write('<table width=560px><tr><td><h2>Scan Job Information</h2></td></table>\n')
	fout.write('<table class=table1 width=560px>')
	fout.write('<tr><td>Scan Name</td><td>'+str(scan_name)+'</td>')
	fout.write('<tr><td>Target</td><td>'+str(uri)+'</td>')
	fout.write('<tr><td>Date</td><td>'+str(finalised)+'</td>')
	fout.write('<tr><td>Scan UUID</td><td>'+str(scanid)+'</td>')
	fout.write('<tr><td>Requests Made</td><td>'+str(request_count)+'</td>')
	fout.write('<tr><td>Pages Crawled</td><td>'+str(crawled)+'</td>')
	fout.write('<tr><td>Pages Audited</td><td>'+str(audited)+'</td>')
	fout.write('</table>')
	fout.write('</div>')
	fout.write('<table width=100%></table>')
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>Vulnerability Summary</h1>')
	fout.write('<table width=100%></table></div>')
	plug_counts(scanid,fout,"critical")
	plug_counts(scanid,fout,"high")
	plug_counts(scanid,fout,"medium")
	plug_counts(scanid,fout,"low")
	plug_counts(scanid,fout,"info")
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>Plugin Details</h1>')
	fout.write('<table width=100%></table></div>')
	plug_counts_detailed(scanid,fout,"critical")
	plug_counts_detailed(scanid,fout,"high")
	plug_counts_detailed(scanid,fout,"medium")
	plug_counts_detailed(scanid,fout,"low")
	plug_counts_detailed(scanid,fout,"info")
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>Additional Vulnerability Information</h1>')
	fout.write('<table width=100%></table></div>')
	print_vulns(scanid,fout,"critical")
	print_vulns(scanid,fout,"high")
	print_vulns(scanid,fout,"medium")
	print_vulns(scanid,fout,"low")
	print_vulns(scanid,fout,"info")
	fout.write('</html>')
	fout.close()

def print_report2(x):
	# works off the newer json report outputs
	scanid=x["scanID"]
	uri=x["target"]
	finalised=x["finalised"]
	scan_name=x["scan_name"]
	crawled=x["crawled"]
	audited=x["audited"]
	request_count=x["request_count"]
	fin=open(results_dir+"report_"+scanid+".json","r")
	fout=open(reports_dir+"v2_"+scanid+".html","w+")
	data=json.load(fin)
	fin.close()
	write_html_header(fout)
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>WAS Report</h1>')
	fout.write('<table width=100%></table></div>')
	print_summary2(data,fout)
	fout.write('<div class=bar_chart_fl>\n')
	fout.write('<table width=560px><tr><td><h2>Scan Job Information</h2></td></table>\n')
	fout.write('<table class=table1 width=560px>')
	fout.write('<tr><td>Scan Name</td><td>'+str(scan_name)+'</td>')
	fout.write('<tr><td>Target</td><td>'+str(uri)+'</td>')
	fout.write('<tr><td>Date</td><td>'+str(finalised)+'</td>')
	fout.write('<tr><td>Scan UUID</td><td>'+str(scanid)+'</td>')
	fout.write('<tr><td>Requests Made</td><td>'+str(request_count)+'</td>')
	fout.write('<tr><td>Pages Crawled</td><td>'+str(crawled)+'</td>')
	fout.write('<tr><td>Pages Audited</td><td>'+str(audited)+'</td>')
	fout.write('</table>')
	fout.write('</div>')
	fout.write('<table width=100%></table>')
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>Vulnerability Summary</h1>')
	fout.write('<table width=100%></table></div>')
	plug_counts2(data,fout,"critical")
	plug_counts2(data,fout,"high")
	plug_counts2(data,fout,"medium")
	plug_counts2(data,fout,"low")
	plug_counts2(data,fout,"info")
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>Plugin Details</h1>')
	fout.write('<table width=100%></table></div>')
	plug_counts_detailed2(data,fout,"critical")
	plug_counts_detailed2(data,fout,"high")
	plug_counts_detailed2(data,fout,"medium")
	plug_counts_detailed2(data,fout,"low")
	plug_counts_detailed2(data,fout,"info")
	fout.write('<div class=page_heading>\n')
	fout.write('<h1>Additional Vulnerability Information</h1>')
	fout.write('<table width=100%></table></div>')
	plug_outputs(data,fout,"critical")
	plug_outputs(data,fout,"high")
	plug_outputs(data,fout,"medium")
	plug_outputs(data,fout,"low")
	plug_outputs(data,fout,"info")
	fout.write('</html>')
	fout.close()


#
# Main
#
results_dir="../results/"
reports_dir="../reports/"
#reports_dir="/mnt/downloads/"
f=open(results_dir+"scan_list.json","r")
scan_lst=json.load(f)
for x in scan_lst:
	#print line
	scanID=x["scanID"]
	uri=x["target"]
	finalised=x["finalised"]
	scan_name=x["scan_name"]
	print(scanID, uri, finalised, scan_name)
	# older method off original APIs
	#print_report(x)
	# newer method off report API
	print_report2(x)
f.close()
