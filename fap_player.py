import sqlite3
import time
import vlc
import re
import sys
import urllib2

conn=sqlite3.connect(":memory:")
c = conn.cursor()
event_id = '1'

def test_data():

	
	create_table="""CREATE TABLE events(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	serial_key CHAR(50),
	event_name CHAR(50),
	fb_url CHAR(50),
	current_event CHAR(50)
	);
	
	CREATE TABLE songlist(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	event_id,
	serial_key,
	title,
	source,
	url,
	requester,
	is_played,
	play_next,
	file_type);
	
	CREATE TABLE status(
	event_id,
	status);"""
	
	
	test_data = """
	INSERT into events(event_name, current_event) VALUES ('test_event','1');
	INSERT into songlist(event_id, url,is_played) VALUES ('1','http://www.youtube.com/watch?v=qzocxPC8wVQ', '0');
	INSERT into songlist(event_id, url,is_played) VALUES ('1','http://www.youtube.com/watch?v=aNnJimNsZjI', '0');
	INSERT into status(event_id, status) VALUES ('1','1');
	"""
	
	c.executescript(create_table)
	c.executescript(test_data)
	
def status_check(event_id):
	status_check = "SELECT * FROM status WHERE event_id = '"+event_id+"';"
	result1 = c.execute(status_check)
	for status in result1:
		if status[1] == "0":# Stop 
			return "Stop"
		if status[1] == "1":# Play
			return "Play"
		if status[1] == "2":# Next
			return "Next"
		
def song_play(event_id):
	play_check = "SELECT * FROM songlist WHERE is_played = '0' LIMIT 1"
	result2 = c.execute(play_check)
	for play in result2:
		return play[5]

def get_video_url(url):
	#urlname = url.split('&',1)[0]
	urlname = url
	resp = urllib2.urlopen(urlname)
	content = resp.read()
	fmtre = re.search('(?<=fmt_url_map=).*', content)
	grps = fmtre.group(0).split('&amp;')
	vurls = urllib2.unquote(grps[0])
	videoUrl = None
	for vurl in vurls.split('|'):
		if vurl.find('itag=5') > 0:
			return vurl
	return None
print get_video_url("http://www.youtube.com/watch?v=3v5ERX0wk18")
#test_data()
# use multiprocess for status check
#while True:
#	play_status = status_check(event_id)
#	print play_status
#	try:
#		play_status1 = play_status
#	except:
#	playstatus1 != 
#	break

#print song_play(event_id)
# check_table = "SELECT * FROM status;"
# result = c.execute(check_table)

# for i in result:
	# print i[1]