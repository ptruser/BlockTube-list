#!python3
# -*- coding: utf-8 -*-

import json
import os
import difflib

from rich import print

def diff(orig_data, diff_data):
	minuses = 0
	position = 0
	stdout = ""
	for i, s in enumerate(difflib.ndiff(orig_data, diff_data)):
		# if s[0] == ' ':
		# 	stdout += diff_data[i-minuses]
		# elif s[0] == '-':
		# 	minuses += 1
		if s[0] == '+':
			stdout += f'[bold green]{diff_data[i-minuses]}[/bold green]\n'

	print(stdout)

# -------------------------- #

def clear_empty_elements(l):
	for index, line in enumerate(l):
		if line == '':
			del l[index]

def beautify_comments(l):
	for index, line in enumerate(l):
		if line.startswith('//'):
			l[index] = line[27:]

def merge_elements(old, new):
	print('Diff:')
	r = old + [x for x in new if x not in old]
	diff(old, r)
	return r

# -------------------------- #

def remove_file(path):
	os.remove(path)

# -------------------------- #

prefix = '' # Maybe will be using in the future
current_backup_filepath = prefix + 'blocktube_backup.json'
old_backup_filepath      = prefix + '1nfdev_blocktube_backup.json'
new_backup_filepath      = prefix + '1nfdev_blocktube_backup.temp.json'
output_backup_filepath   = prefix + '1nfdev_blocktube_backup.json'

os.rename(old_backup_filepath, new_backup_filepath)

# ----- Current config ----- #

with open(current_backup_filepath, 'r', encoding="utf8") as File:
	current_data = json.loads(File.read())

current_channels = current_data["filterData"]["channelId"]
current_videos   = current_data["filterData"]["videoId"]

print('[bold cyan]Processing current configuration...[/bold cyan]')

clear_empty_elements(current_channels)
print('ChannelID field cleared of empty elements')
clear_empty_elements(current_videos)
print('VideoID field cleared of empty elements')

beautify_comments(current_channels)
print('ChannelID comments was be beautified')
beautify_comments(current_videos)
print('VideoID comments was be beautified')

# ----- Latest backup ----- #

with open(new_backup_filepath, 'r', encoding="utf8") as File:
	Data = json.loads(File.read())

channels = Data["filterData"]["channelId"]; lbc = channels
videos   = Data["filterData"]["videoId"]; lbv = videos

print('[bold cyan]Processing latest backup configuration...[/bold cyan]')

channels = merge_elements(channels, current_channels)
print('ChannelID field merged')
videos   = merge_elements(videos, current_videos)
print('VideoID field merged')

clear_empty_elements(channels)
print('ChannelID field cleared of empty elements')
clear_empty_elements(videos)
print('VideoID field cleared of empty elements')

beautify_comments(channels)
print('ChannelID comments was be beautified')
beautify_comments(videos)
print('VideoID comments was be beautified')

# -------------------------- #

Data["filterData"]["channelId"] = channels
Data["filterData"]["videoId"]   = videos

with open(output_backup_filepath, 'w', encoding="utf8") as File:
	File.write(json.dumps(Data, indent=2, ensure_ascii=False))

print('[green]Backup file created[/green]')

remove_file(new_backup_filepath)
remove_file(current_backup_filepath)

print('[red]Old backup deleted[/red]')
print('[bold green]Done![/bold green]')