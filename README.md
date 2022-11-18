# RoomCal
Python script that fetches your public Google or iCloud calendar and creates an html display web page that can be displayed on screens, such as an iPad in your office window.

![ipad1](https://user-images.githubusercontent.com/10948066/202680351-7f7d3b5a-7f0a-4b9e-a5cc-cdd5f232ae67.jpg)


## What is this? And what does it do?
This is a project that has been showing my calendar, availability and whereabouts on my office door (on an old iPad) since 2018.
The script queries my public iCloud calendar about my current activity and the next 6 upcoming activities. Based on keywords - e.g. 'lunch' in activity, 'outside the office' in location, 'meeting' in activity and more - the script sets my status as 'busy', 'available' and more.
Lastly it creates an updated html file, which get uploaded to my server.

[You can watch it live here](https://mickekring.se/stats/room/b212a/)

## Disclaimer
__I'm not a coder!__ I just like to create stuff. :)

## Built with
* Python 3.x
* Bootstrap

## Want to run it yourself?

If you'd like to run it yourself, there are some things to modify. I'll try to make this short and sweet.

#### Web server with SFTP access
The script uploads your html files to your web server via SFTP.

#### Public calendar
You need a public iCloud or Google calendar. After that, copy the adress and paste in the config.yml (see below). If you use an iCloud calendar, replace webdav:// for https://

#### Install Python modules
pytz, paramiko, pyyaml, datetime, icalevents, locale, signal, time

#### Files
* Download all files
* Open __config.yml__
  - Change the settings, such as localization, paths to directories, address to your calendar and more
* Open __main.py__
  - __check_time_to_run()__ | a function that sets when the script can actually run. Change the variables __off_hours__ and __off_days__ so that the script runs when you want it to
  - __calendar()__ | is the main function that queries your calendar. You set your keywords in the if-statements about line 140-190.

A tip is to comment out the __file_upload()__ function in the __Main()__ loop at the bottom and just check that everything works in the terminal or whatever you run your code in.

![command](https://user-images.githubusercontent.com/10948066/202698325-528b5178-741b-4d38-897e-a555dadc6c83.jpg)

* Open __index.php__ in the folder __upload_to_webserver__ directory
  - Change headlines and static text
  - Change the paths so that they point to your files on your server
  - If you don't want the video background of me waving to y'all, you can change that too. :)
  
* Upload the files in __upload_to_webserver__ to your webserver

* If you commented out the __file_upload()__ function in the __Main()__ loop, undo that and try the whole script.


## Version History
1.0 Initial upload
