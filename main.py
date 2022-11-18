from icalevents.icalevents import events
from datetime import datetime, timedelta
import pytz
import locale
import yaml
import paramiko
import signal
import time


## GLOBAL VARS 

# Load config-file
yaml.warnings({'YAMLLoadWarning': False})
conf = yaml.load(open('config.yml'), Loader=yaml.FullLoader)

# Set locale to SE 
locale.setlocale(locale.LC_ALL, conf['local']['locale'])

# Init Color HTML
style_color_html = "green"
style_message_html ="ledigt"

# Colors
red = "red"
green = "green"
blue = "#44aabd"
grey = "#222122"

# Init Messages HTML
status_calender_now = "Kalendern är tom"
statusDay = "Kalendern är tom"

# Paths and directories if running local or production
# Setup in config.yml
path = conf['run_fromo_device']['local_or_prod'] 

# Init variable
nowEvent = 1



# Timeout

class TimeOutException(Exception):
	pass

def alarm_handler(signum, frame):
	print("ALARM signal received")
	raise TimeOutException()

signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(30)



# Checks if script should be running or not

def check_time_to_run(hour, day):

	global go_live
	
	off_hours = ["18", "19", "20", "21", "22", "23", "24", "00", "01", "02", "03", "04", "05", "06"]
	off_days = ["Lördag", "Söndag"]

	if hour in off_hours or day in off_days:
		print("Script outside running hours / days")
		go_live = 0

	else:
		print("Script within running hours / days")
		go_live = 1



# Current time and status

def time_available():

	now = datetime.now()
	year = now.strftime("%Y")
	month = now.strftime("%B")
	date = now.strftime("%d")
	day = now.strftime("%A")
	time = now.strftime("%H:%M")
	hour = now.strftime("%H")

	print("\n\n\n--- --- --- ---\n")
	print("Time now: " + time)
	print("Date: " + day + " | " + date + " " + month + " " + year)

	style_clock = '<style type="text/css">.div1-half-top {background-color: ' + style_color_html + ';}</style>'

	with open("web/kl.php", "w") as f1:
		f1.write(style_clock + '<h1 class="clock"><i class="far fa-clock" aria-hidden="true"></i> ' + time 
			+ '</h1><h4>' + day + ' | ' + date + ' ' + month + ' ' + year + '</h4>' + '<h1 class="available" style="color: ' 
			+ style_color_html + '">' + style_message_html + '</h1>')

	check_time_to_run(hour, day)



# Main function that fetches both current activity and a listing of
# future activities

def calendar():

	global style_color_html
	global style_message_html

	url = conf['urlcalendar']['link_url']

	my_timezone = pytz.timezone(conf['local']['timezone'])
	now = datetime.now().astimezone(pytz.timezone('UTC'))
	future = (now + timedelta(minutes=1)).astimezone(pytz.timezone('UTC'))

	es = events(url, start=now, end=future)
	
	# Return start date from event
	
	def get_start(event):
		return event.start.astimezone(my_timezone)

	# Sort events earliest to latest
	
	es.sort(key=get_start)


	# Current activity
	
	for e in es:
				
		activity_now = e.summary
		location = e.location
		start = e.start.astimezone(my_timezone)
		start_time = (start.strftime("%H:%M"))
		end = e.end.astimezone(my_timezone)
		end_time = (end.strftime("%H:%M"))
	

	try:
		status_calender_now = ((start_time) + " - " + (end_time) + " | " + (activity_now))
		print("--- Activity now\n")
		print(status_calender_now)
		
		if "ej på skolan" in location.lower(): # translation EN "not at school"
			style_color_html = blue
			style_message_html = "EJ PÅ SKOLAN" # translation EN "not at school"
			nowEvent = 1

		elif "möte" in activity_now.lower(): # translation EN "meeting"
			style_color_html = red
			style_message_html = "UPPTAGET" # translation EN "busy"
			nowEvent = 0

		elif "semester" in activity_now.lower(): # translation EN "vacation"
			style_color_html = blue
			style_message_html = "SEMESTER" # translation EN "vacation"
			nowEvent = 1

		elif "sjuk" in activity_now.lower(): # translation EN "ill"
			style_color_html = blue
			style_message_html = "SJUK" # translation EN "ill"
			nowEvent = 1

		elif "upptaget" in activity_now.lower(): # translation EN "busy"
			style_color_html = red
			style_message_html = "UPPTAGET" # translation EN "busy"
			nowEvent = 1

		elif "ledig" in activity_now.lower(): # translation EN "vacant"
			style_color_html = blue
			style_message_html = "SEMESTER" # translation EN "vacation"
			nowEvent = 1

		elif "lunch" in activity_now.lower(): # translation EN "lunch"
			style_color_html = blue
			style_message_html = "LUNCH" # translation EN "lunch"
			nowEvent = 1

		elif "b212a" not in location.lower(): # my room number at work
			style_color_html = grey
			style_message_html = "INGEN INNE" # translation EN "no one in"
			nowEvent = 1

		else:
			style_color_html = green
			style_message_html = "VÄLKOMMEN IN" # translation EN "welcome"
			nowEvent = 0
			pass

		print("Style HTML Color: " + style_color_html)
		print("Style HTML Message: " + style_message_html)
		print("\n--- Upcoming activities\n")

	except:

		print("NOTHING GOING ON RIGHT NOW")
		style_color_html = grey
		style_message_html = "ingen inne" # translation EN "no one in"
		nowEvent = 1

	

	# List future activities

	time.sleep(conf['config']['sleep_time'])

	my_timezone = pytz.timezone(conf['local']['timezone'])
	now = datetime.now().astimezone(pytz.timezone('UTC'))
	future = (now + timedelta(hours=72)).astimezone(pytz.timezone('UTC'))

	es = events(url, start=now, end=future)

	
	# Return start date from event
	
	def get_start(event):
		return event.start.astimezone(my_timezone)

	# Sort events earliest to latest
	
	es.sort(key=get_start)


	list_future_activities = []

	
	count = 0
	
	for e in es:

		if count < 6:
				
			activity_day = e.summary
			activity_day_trunc = (activity_day[:21] + '...') if len(activity_day) > 21 else activity_day		
			location = e.location
			start = e.start.astimezone(my_timezone)
			start_time = (start.strftime("%H:%M"))
			start_date_day = (start.strftime("%a"))
			end = e.end.astimezone(my_timezone)
			end_time = (end.strftime("%H:%M"))

			try:
				if "teams" in location.lower():
					location = "Videomöte Teams" # translation EN "video meeting teams"
				elif "meet" in location.lower():
					location = "Videomöte Google meet" # translation EN "video meeting google meet"
				elif "zoom" in location.lower():
					location = "Videomöte Zoom" # translation EN "video meeting zoom"
			except:
				location = "Okänt"

			if nowEvent == 0:
				list_future_activities.append('<tr><th class="first"><p class="calfont' + style_color_html +'">' 
					+ (start_date_day.capitalize()) + '</p></th><th class="second"><p class="calfont' + style_color_html +'">' 
					+ (start_time) + " - " + (end_time) + '</p></th><th class="third"><p class="calfont' + style_color_html +'">' 
					+ (activity_day_trunc) + '<br/><span class="testing">Plats: ' + location + '</span></p></th></tr>')
				nowEvent = 1

			else:
				list_future_activities.append('<tr><th class="first"><p class="calfont">' + (start_date_day.capitalize()) 
					+ '</p></th><th class="second"><p class="calfont">' + (start_time) + " - " + (end_time) 
					+ '</p></th><th class="third"><p class="calfont">' + (activity_day_trunc) + '<br/><span class="testing">Plats: ' 
					+ location + '</span></p></th></tr>')
			
			print(activity_day + " | " + start_date_day + " | " + start_time + " | " + end_time)

		count += 1

	statusDay = ("".join(list_future_activities))

	with open("web/day.php", "w") as f2:
		f2.write(statusDay)

	

# File uploads to SFTP-server #

def file_upload():
	try:
		host = conf['sftp_user']['host']
		port = conf['sftp_user']['port']
		transport = paramiko.Transport((host, port))

		password = conf['sftp_user']['password']
		username = conf['sftp_user']['username']
		transport.connect(username = username, password = password)

		sftp = paramiko.SFTPClient.from_transport(transport)

		sftp.chdir(conf['sftp_user']['remote_server_path'])

		filepath = "kl.php"
		filepath2 = "day.php"

		if path == "local":
			localpath = conf['path_local']['localpath']
			localpath2 = conf['path_local']['localpath2']
		else:
			localpath = conf['path_prod']['localpath']
			localpath2 = conf['path_prod']['localpath2']

		sftp.put(localpath, filepath)
		sftp.put(localpath2, filepath2)

		sftp.close()
		transport.close()
		print("\nFiles uploaded to server\n")
	
	except:
		print("\nError. Files not uploaded to server\n")
		pass

###########################

def Main():

	try:
		
		print("\nSystem start\n")

		while True:

			time_available()
			file_upload()
			signal.alarm(30)

			if go_live == 1:
			
				try:
					calendar()
				except TimeOutException as ex:
					print(ex)
			else:
				pass

			signal.alarm(0)
			file_upload()
			time.sleep(conf['config']['sleep_time'])

	finally:
		print("End game...")

### MAIN PROGRAM ###

if __name__ == "__main__":
	Main()
