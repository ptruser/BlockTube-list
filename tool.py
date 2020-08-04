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

def merge_elements(lhs_l, rhs_l):
	return lhs_l + [x for x in rhs_l if x not in lhs_l]

def remove_file(path):
	os.remove(path)

prefix = '' # Maybe will be using in the future
original_backup_filepath = prefix + 'blocktube_backup.json'
old_backup_filepath      = prefix + '1nfdev_blocktube_backup.json'
new_backup_filepath      = prefix + '1nfdev_blocktube_backup.temp.json'
output_backup_filepath   = prefix + '1nfdev_blocktube_backup.json'

os.rename(old_backup_filepath, new_backup_filepath)

with open(original_backup_filepath, 'r', encoding="utf8") as File:
	original_data = json.loads(File.read())

original_channels = original_data["filterData"]["channelId"]
original_videos   = original_data["filterData"]["videoId"]

with open(new_backup_filepath, 'r', encoding="utf8") as File:
	Data = json.loads(File.read())

channels = Data["filterData"]["channelId"]
videos   = Data["filterData"]["videoId"]

channels = merge_elements(channels, original_channels)
print('ChannelID field merged')
videos   = merge_elements(videos, original_videos)
print('VideoID field merged')

clear_empty_elements(channels)
print('ChannelID field cleared of empty elements')
clear_empty_elements(videos)
print('VideoID field cleared of empty elements')

beautify_comments(channels)
print('ChannelID comments was be beautified')
beautify_comments(videos)
print('VideoID comments was be beautified')

Data["filterData"]["channelId"] = channels
Data["filterData"]["videoId"]   = videos

with open(output_backup_filepath, 'w', encoding="utf8") as File:
	File.write(json.dumps(Data, indent=2, ensure_ascii=False))

print('Backup file created')

remove_file(new_backup_filepath)
remove_file(original_backup_filepath)

print('Old backup deleted')
print('Done!')