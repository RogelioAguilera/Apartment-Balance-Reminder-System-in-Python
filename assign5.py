#!/usr/bin/env python3
import os
import re
import sys

def custom_template(first_name, last_name, lease_start, lease_end, apt_number, balance, template_file, output_dir):
	with open (template_file, 'r') as template_file_r:
		template= template_file_r.read()
		modified_template = re.sub(r'<<first_name>>', first_name, template)
		modified_template = re.sub(r'<<last_name>>', last_name, modified_template)
		modified_template = re.sub(r'<<lease_start>>', lease_start, modified_template)
		modified_template = re.sub(r'<<lease_end>>', lease_end, modified_template)
		modified_template = re.sub(r'<<apt_number>>', apt_number, modified_template)
		modified_template = re.sub(r'<<balance>>', str(balance), modified_template)

		last_name = last_name.replace(' ', '_') 
		output_file_name = last_name + ".mail"
		output_file_path = os.path.join(output_dir, output_file_name)

		count= 1
		while os.path.exists(output_file_path):
			output_file_name = "{}_{}.mail".format(last_name, count)
			output_file_path = os.path.join(output_dir, output_file_name)
			count += 1
		with open(output_file_path, 'w') as output_file:
    			output_file.write(modified_template)

def main(data_dir, template_file, date, output_dir):
	for file_ in os.listdir(data_dir):
		if file_.endswith('.apt'):
			with open(os.path.join(data_dir, file_), 'r') as data:
				lines=data.read().splitlines()
				balance=int(lines[2])
				if balance>0:
					first_name= lines[0].split()[0] 
					last_name= ' '.join(lines[0].split()[1:])
					lease_start= lines[1].split()[0]
					lease_end= lines[1].split()[1]
					apt_number= file_.split('.')[0]
					custom_template(first_name, last_name, lease_start, lease_end, apt_number, balance, template_file, output_dir)


if __name__ == '__main__':
	if len(sys.argv) != 5:
		print("Incorrect number of arguments, please try again")
		sys.exit(1)
	if not os.path.isdir(sys.argv[1]):
		print(sys.argv[1], "is not a directory")
		sys.exit(1)
	if not re.match(r'\d{2}/\d{2}/\d{4}', sys.argv[3]):
		print("Please make sure that the fourth aregument is a date in the DD/MM/YYYY format.")
		sys.exit(1)
	if not os.path.isdir(sys.argv[4]):
		output_dir=sys.argv[4]
		os.makedirs(output_dir)
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

