import urllib2, json, time, sys, getopt, datetime
from dateutil import parser

loop_interval_secs = 10
now = datetime.datetime.now().replace(tzinfo=None)
last_time = now
event_time = now
found_events = False

print ''
print 'Ploggly started'
print 'Polling for events every ' + str(loop_interval_secs) + ' seconds.'
print ''

def call_loggly():
	print 'checking for new events...'
	global last_time, event_time, found_events
	username = '<loggly_un>'
	password = '<loggly_pw>'
	url = 'https://<loggly_subdomain>.loggly.com/api/search?q=*&from=NOW-5MINUTES'
	p = urllib2.HTTPPasswordMgrWithDefaultRealm()
	p.add_password(None, url, username, password)
	handler = urllib2.HTTPBasicAuthHandler(p)
	opener = urllib2.build_opener(handler)
	urllib2.install_opener(opener)
	page = urllib2.urlopen(url)
	json_data = json.load(page)
	found_events = False
	for r in json_data["data"]:
		if r["inputname"] in ('<loggly_input_name>'):
			if "datetime" in r["json"]:
				event_time = parser.parse(r["json"]["datetime"]).replace(tzinfo=None)
				#print str(event_time) + ' > ' + str(last_time)
				if "host" in r["json"] and event_time > last_time:
					found_events = True
					print ''
					print '----------------------------------------------------------------'
					print '|' + r["json"]["datetime"] + ' | ' + r["inputname"] + ' | ' + r["ip"] + '|'
					print 'Message:  ' + r["json"]["message"]
					print 'level:    ' + r["json"]["level"]
					print 'host:     ' + r["json"]["host"]
					print 'datetime: ' + r["json"]["datetime"]
					print '----------------------------------------------------------------'

	if found_events == True:
		last_time = datetime.datetime.now().replace(tzinfo=None)	
	return True # do ur work here, but not for long

while True:
	call_loggly()
	time.sleep(loop_interval_secs)
