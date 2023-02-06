#!/usr/bin/python3

import os
import subprocess
import sys
import base64
import json

# global variable for linux, macOS
main_path=os.path.expanduser("~/Desktop/ProxyProject")
go_null="1>/dev/null 2>&1"

# global variable for linux
linux_config_dir = f"{main_path}/config"
linux_v2ray_file= "v2ray-linux-64.zip"
linux_v2ray_dir = f"{main_path}/v2ray"

# color
color_reset = "\033[0m"
color_green = "\33[32m"
color_yellow = "\033[33m"
color_red = "\33[91m"
color_bold = "\033[1m"

def banner():
	os.system("clear")
	say_hi = (f"""{color_green}
██████╗░█████╗░██████╗░
██╔════╝██╔══██╗██╔══██╗
█████╗░░██║░░██║██████╔╝
██╔══╝░░██║░░██║██╔══██╗
██║░░░░░╚█████╔╝██║░░██║
╚═╝░░░░░░╚════╝░╚═╝░░╚═╝{color_reset}""","""

███████╗██████╗░███████╗███████╗██████╗░░█████╗░███╗░░░███╗
██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗████╗░████║
█████╗░░██████╔╝█████╗░░█████╗░░██║░░██║██║░░██║██╔████╔██║
██╔══╝░░██╔══██╗██╔══╝░░██╔══╝░░██║░░██║██║░░██║██║╚██╔╝██║
██║░░░░░██║░░██║███████╗███████╗██████╔╝╚█████╔╝██║░╚═╝░██║
╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚══════╝╚═════╝░░╚════╝░╚═╝░░░░░╚═╝""",f"""{color_red}

██╗███╗░░██╗████████╗███████╗██████╗░███╗░░██╗███████╗████████╗
██║████╗░██║╚══██╔══╝██╔════╝██╔══██╗████╗░██║██╔════╝╚══██╔══╝
██║██╔██╗██║░░░██║░░░█████╗░░██████╔╝██╔██╗██║█████╗░░░░░██║░░░
██║██║╚████║░░░██║░░░██╔══╝░░██╔══██╗██║╚████║██╔══╝░░░░░██║░░░
██║██║░╚███║░░░██║░░░███████╗██║░░██║██║░╚███║███████╗░░░██║░░░
╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝░░░╚═╝░░░ {color_reset}""")
	for i in say_hi:
		print(i)
		os.system("sleep 1")
	os.system("clear")

def linux_speed_test(conf_name):
	addr = str(subprocess.check_output(f"cat {linux_config_dir}/{conf_name} | grep outbounds -A100 | grep address", shell=True, encoding='utf-8')).split("\"")[-2]
	
	get_speed =  subprocess.check_output(f"ping -c 1 {addr} | tail -n1 | cut -d' ' -f4 | cut -d'/' -f2",
									shell=True,
									encoding="utf-8").replace("\n" , "")
	if get_speed:
		return get_speed
	else:
		return 0


def new_func():
	line_len = subprocess.check_output(f"ls -1 {linux_config_dir} | wc -l",
					shell=True,
					encoding='utf-8')

	print(f"{color_yellow}Configs: {color_reset}")
	for i in range(1, int(line_len) +1):
		cfg = subprocess.check_output(f"ls -1 {linux_config_dir} | head -n {i} | tail -n 1",
			shell=True,
			encoding='utf-8').strip()

		conf_speed = linux_speed_test(cfg)

		print(f"\t {color_bold}{i}{color_reset} {color_yellow}:{color_reset} {cfg} {color_green} {conf_speed}{color_reset}ms")	

	user_conf = int(input(f"{color_yellow}Enter Number Of Config: {color_reset}"))
	selected_config = str(subprocess.check_output(f"ls -1 {linux_config_dir} | head -n {user_conf} | tail -n1",
		 	shell=True,
		 	encoding='utf-8')).replace("\n","")
	return selected_config	
	


def mac_speed_test(conf_name):
	addr = str(subprocess.check_output(f"cat {main_path}/configs/{conf_name} | grep outbounds -A100 | grep address", shell=True, encoding='utf-8')).split("\"")[-2]
	
	get_speed =  subprocess.check_output(f"ping -c 1 {addr} | tail -n1 | cut -d' ' -f4 | cut -d'/' -f2",
									shell=True,
									encoding="utf-8").replace("\n" , "")
	return get_speed


def mac_new_func():
	line_len = subprocess.check_output(f"ls -1 {main_path}/configs | wc -l",
					shell=True,
					encoding='utf-8')

	print(f"{color_yellow}Configs: {color_reset}")
	for i in range(1, int(line_len) +1):
		cfg = subprocess.check_output(f"ls -1 {main_path}/configs | head -n {i} | tail -n 1",
			shell=True,
			encoding='utf-8').strip()

		conf_speed = mac_speed_test(cfg)

		print(f"\t {color_bold}{i}{color_reset} {color_yellow}:{color_reset} {cfg} {color_green} {conf_speed}{color_reset}ms")	

	user_conf = int(input(f"{color_yellow}Enter Number Of Config: {color_reset}"))
	selected_config = str(subprocess.check_output(f"ls -1 {main_path}/configs | head -n {user_conf} | tail -n1",
		 	shell=True,
		 	encoding='utf-8')).replace("\n","")
	return selected_config	
	




# This Function For Checking The existence of the directory
def mac_checkinstall(arg):
    program = os.system(f"which {arg} &> /dev/null")
    if program == 0:
        return 0
    else:
        return 1


# cloning the json configs from GitHub
def mac_clone_gitrepo():
    if mac_checkExistDir(f"{main_path}/configs/*") == 0:
        os.system(f"rm -rf {main_path}/configs/*")
        os.system(f"rm -rf {main_path}/configs/.git")
        print(f"{color_bold}cloning v2ray json configs ... {color_reset}" , "\n")
        os.system(f"git clone https://github.com/MrParhamDev/v2configs {main_path}/configs &> /dev/null ")
    else:
        os.system(f"rm -rf {main_path}/configs/.git")
        print(f"{color_bold}Cloning V2ray json Configs ... {color_reset}", "\n")
        os.system(f"git clone https://github.com/MrParhamDev/v2configs {main_path}/configs &> /dev/null")



# Running the v2ray
def mac_run_v2ray():
	func = mac_new_func()
	if os.system(f"pgrep v2ray &> /dev/null") == 0:
		v2ray_pid = subprocess.check_output("pgrep v2ray" , shell=True , encoding="utf-8").replace("\n" , "")
		print(f"{color_red}V2ray Already Runned{color_reset}   ProcessID: {color_yellow}{v2ray_pid}{color_reset}")
	else:
		print(f"{color_green} v2ray Successfully running {color_reset}")
		os.system(f"v2ray -c {main_path}/configs/{func} &> /dev/null &")
		print(f"{color_yellow}Proxy: socks://127.0.0.1:10808{color_reset}")



# Check if a directory exists or not
def mac_checkExistDir(arg):
    program = os.system(f"ls {arg} &> /dev/null")
    if program == 0:
        return 0
    else:
        return 1


# check and install dependencies
def mac_dependencies():
    # check brew install details
    if mac_checkinstall("brew") == 0:
        print("Brew Already Installed")
    else:
        print(f"{color_red}Brew is Not Installed Your System {color_reset}")
        tmp = input(f"{color_bold}Do You Like install Brew? Y/N: {color_reset}")
        if tmp == "Y" or tmp == "y":
            os.system(f"/usr/bin/ruby -e curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install")
        elif tmp == "N" or tmp == "n":
            print(f"{color_red}Exit The Script ... {color_reset}")
            exit()
    # check wget install details
    if mac_checkinstall("wget") == 0:
        print("wget Already Installed")
    else:
        print(f"{color_bold}Installing wget ... {color_reset}")
        os.system("brew install wget &> /dev/null")
    # check v2ray install details
    if mac_checkinstall("v2ray") == 0:
        print("V2ray Already Installed")
    else:
        print(f"{color_bold}Installing V2ray ... {color_reset}")
        os.system("brew install v2ray &> /dev/null")
    # check unzip install details
    if mac_checkinstall("unzip") == 0:
        print("unzip Already Installed")
    else:
        print(f"{color_bold}Installing unzip ... {color_reset}")
        os.system("brew install unzip &> /dev/null")


# this function for createPATH Project
def mac_createPATH():
    createConfigs = (os.path.expanduser(f"{main_path}/configs"))
    if mac_checkExistDir(main_path) == 0:
        print("ProxyProject Directory Already exist")
        # check Exist Configs Directory
        if mac_checkExistDir(createConfigs) == 0:
            print("Configs sub Directory Already exist")
        else:
            os.mkdir(createConfigs)
    else:
        print(f"{color_bold}Creating PATH with sub Directory ... {color_reset}")
        os.mkdir(main_path)
        os.mkdir(createConfigs)

def mac_sub_setall():
	mac_createsublink = (os.path.expanduser(f"{main_path}/subscriptions"))

	subdir = int(os.system(f"ls {main_path}/subscriptions {go_null}"))
	if subdir == 0:
		print(f"{color_red}Subscriptions link Directory Already exist {color_reset}")
	else:
		os.mkdir(f"{main_path}/subscriptions")
	mac_suburl =  input(f"{color_yellow}Enter Subscriptions URL: {color_reset}")
	print(f"{color_bold}Getting Subscriptios URL ...{color_reset}")

	if linux_cmd_status(f"ls {main_path}/subscriptions/* {go_null}") == 0:
		os.system(f"rm -rf {main_path}/subscriptions/*")
		os.system(f"wget -O {main_path}/subscriptions/subscription.html {mac_suburl} {go_null}")
	else:
		os.system(f"wget -O {main_path}/subscriptions/subscription.html {mac_suburl} {go_null}")

	if linux_cmd_status(f"ls {main_path}/subscriptions/* {go_null}") == 0:
		print(f"{color_green} Getting Subscriptions URL Successfully {color_reset}")
	else:
		print(f"{color_red}Getting Subscriptions URL Faild {color_reset}")
		mac_sub_setall()
	mac_decode_sub(mac_createsublink, "subscription.html")


def mac_sub_start():
	path_sub = f"{main_path}/subscriptions/sub_conf"

	lines = subprocess.check_output(f"ls -1 {path_sub} | wc -l", shell=True, encoding='utf-8')
	if lines:
		print("configs: ")
		for i in range(1 , int(lines)+1):
			sub_conf = subprocess.check_output(f"ls -1 {path_sub} | head -n{i} | tail -n1", shell=True,encoding='utf-8')
			print(f"\t{color_bold}{i}{color_reset}{color_red}:{color_reset}\t {sub_conf}", end='')
			print("\t\t",f"{color_green}-{color_reset}"*20)
		sub_select = int(input(f"{color_yellow}enter number of config: {color_reset}"))
		selected_sub = subprocess.check_output(f"ls -1 {path_sub} | head -n{sub_select} | tail -n1", shell=True,encoding='utf-8')
		
		if os.system(f"pgrep v2ray &> /dev/null") == 0:
			print(f"{color_red}v2ray already running{color_reset}")
		else:
			print(f"{color_green}v2ray Successfully running {color_reset}")
			subprocess.run(f"bash -c \"v2ray -c {path_sub}/{selected_sub}\" & ", shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
			print(f"{color_yellow}Proxy: socks:127.0.0.1:10808{color_reset}")
	else:
		print(f"{color_red}no config found{color_reset}")


def linux_sub_setall():
	linux_createsublink = (os.path.expanduser(f"{main_path}/subscriptions"))

	subdir = int(os.system(f"ls {main_path}/subscriptions {go_null}"))
	if subdir == 0:
		print(f"{color_red}Subscriptions link Directory Already exist {color_reset}")
	else:
		os.mkdir(f"{main_path}/subscriptions")
	linux_suburl =  input(f"{color_yellow}Enter Subscriptions URL: {color_reset}")
	print(f"{color_bold}Getting Subscriptios URL ...{color_reset}")

	if linux_cmd_status(f"ls {main_path}/subscriptions/* {go_null}") == 0:
		os.system(f"rm -rf {main_path}/subscriptions/*")
		os.system(f"wget -O {main_path}/subscriptions/subscription.html {linux_suburl} {go_null}")
	else:
		os.system(f"wget -O {main_path}/subscriptions/subscription.html {linux_suburl} {go_null}")

	if linux_cmd_status(f"ls {main_path}/subscriptions/* {go_null}") == 0:
		print(f"{color_green} Getting Subscriptions URL Successfully {color_reset}")
	else:
		print(f"{color_red}Getting Subscriptions URL Faild {color_reset}")
		linux_sub_setall()
	decode_sub(linux_createsublink, "subscription.html")

def linux_sub_start():
	path_sub = f"{main_path}/subscriptions/sub_conf"

	lines = subprocess.check_output(f"ls -1 {path_sub} | wc -l", shell=True, encoding='utf-8')
	if lines:
		print("configs: ")
		for i in range(1 , int(lines)+1):
			sub_conf = subprocess.check_output(f"ls -1 {path_sub} | head -n{i} | tail -n1", shell=True,encoding='utf-8')
			print(f"\t{color_bold}{i}{color_reset}{color_red}:{color_reset}\t {sub_conf}", end='')
			print("\t\t",f"{color_green}-{color_reset}"*20)
		sub_select = int(input(f"{color_yellow}enter number of config: {color_reset}"))
		selected_sub = subprocess.check_output(f"ls -1 {path_sub} | head -n{sub_select} | tail -n1", shell=True,encoding='utf-8')
		if linux_cmd_status(f"ls {main_path}/.pid {go_null}") == 0:
			print(f"{color_red}v2ray already running{color_reset}")
		else:
			print(f"{color_green}v2ray Successfully running {color_reset}")
			subprocess.run(f"bash -c \"{linux_v2ray_dir}/v2ray run -c {path_sub}/{selected_sub}\" & echo $! > {main_path}/.pid",
				shell=True,
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL)
			print(f"Proxy: socks:127.0.0.1:10808")
	else:
		print(f"{color_red}no config found{color_reset}")

def linux_run_v2ray():
	print("running v2ray...")
	func = new_func()
	if linux_cmd_status(f"ls {main_path}/.pid {go_null}") == 0:
		print(f"{color_red}v2ray already running{color_reset}")
	else:
		print(f"{color_green}v2ray Successfully running {color_reset}")
		os.system(f"{linux_v2ray_dir}/v2ray run -c {linux_config_dir}/{func} {go_null} & echo $! > {main_path}/.pid ")
		print(f"Proxy: socks:127.0.0.1:10808")



def linux_config_download():
	print("\ninstall configs...", end='')

	
	len_files =  subprocess.check_output("", shell=True, encoding="utf-8")

	if linux_cmd_status(f"ls {linux_config_dir} {go_null}") == 1 :
		os.mkdir(f"{linux_config_dir}")
		os.system(f"git clone https://github.com/MrParhamDev/\
v2configs.git {linux_config_dir} {go_null}")

	elif linux_cmd_status(f"ls {linux_config_dir}/* {go_null}") == 0:
		os.system(f"rm -rf {linux_config_dir}/* {linux_config_dir}/.git")
		os.system(f"git clone https://github.com/MrParhamDev/\
v2configs.git {linux_config_dir} {go_null}")

	else:
		os.system(f"git clone https://github.com/MrParhamDev/\
v2configs.git {linux_config_dir} {go_null}")

def linux_v2ray_download():
	print("\ninstall v2ray core...", end='')

	v2ray_link = "https://github.com/v2fly/v2ray-core/\
releases/download/v5.1.0/v2ray-linux-64.zip"

	if linux_cmd_status(f"ls {linux_v2ray_dir} {go_null}") == 1:
		os.mkdir(f"{linux_v2ray_dir}")
		os.system(f"wget -P {linux_v2ray_dir} {v2ray_link} {go_null}")

	elif linux_cmd_status(f"ls {linux_v2ray_dir} {go_null}") == 0 and \
		linux_cmd_status(f"ls {linux_v2ray_dir}/{linux_v2ray_file} {go_null}") == 0:
		if linux_v2ray_checksum() == 0:
			return 0
		else:
			os.system(f"wget --continue -P {linux_v2ray_dir} {v2ray_link} {go_null}")

	else:
		os.system(f"wget -P {linux_v2ray_dir} {v2ray_link} {go_null}")

def linux_v2ray_checksum():
	sha256="e670334a1734b37361f5a1f12d79e98\
9944b0f9556322f1ae710c2db16528e6a"

	sha256sum= subprocess.check_output(f"sha256sum \"{linux_v2ray_dir}/{linux_v2ray_file}\" |\
cut -d' ' -f1", shell=True, encoding="utf-8").replace("\n","")

	if sha256 == sha256sum :
		return 0
	else:
		return 1

def linux_v2ray_extract():
		os.system(f"unzip -n {linux_v2ray_dir}/{linux_v2ray_file} -d {linux_v2ray_dir} {go_null}")

def linux_depends():
	print("install dependecies...", end='')	

	if linux_cmd_status(f"ls {main_path} {go_null}") == 1:
		os.mkdir(main_path)
	need = ("wget", "unzip")
	for i in need:
		linux_pkg_mgrs(i)

def linux_pkg_mgrs(name):
	pkg_mgrs_list = ("apt-get install","yum install",
		"zypper install","nix-env -i",
		"dnf install","equo install",
		"rpm -i","pacman -S")

	for i in range(len(pkg_mgrs_list)):
		pkg_name = pkg_mgrs_list[i].split()[0]
		if linux_cmd_status(f"which {pkg_name} {go_null}") == 0:
			os.system(f"yes 2>/dev/null | sudo {pkg_mgrs_list[i]} {name} {go_null}")
			

def linux_cmd_status(cmd):
	stat = os.system(cmd)
	if stat == 0:
		return 0
	else:
		return 1

def dns_check():
	len_resolv = subprocess.check_output("cat /etc/resolv.conf | wc -l", shell=True, encoding='utf-8')
	for i in range(1, int(len_resolv)+1):
		line = str(subprocess.check_output(f"cat /etc/resolv.conf | head -n{i} | tail -n1", shell=True, encoding='utf-8'))
		if line.strip() == "nameserver 1.1.1.1" or line.strip()	== "nameserver 8.8.8.8":
			return 0
	os.system(f"echo -e \"nameserver 1.1.1.1\nnameserver 8.8.8.8\" | sudo tee -a /etc/resolv.conf {go_null}")

def decode_sub(conf_path, conf_file):
	if os.system(f"ls {conf_path}/sub_conf {go_null}") == 0:
		os.system(f"rm -rf {conf_path}/sub_conf")
		os.system(f"mkdir {conf_path}/sub_conf")
	else:
		os.system(f"mkdir {conf_path}/sub_conf {go_null}")

	b64 = open(f"{conf_path}/{conf_file}", "r").readline()
	conf = str(base64.b64decode(b64).decode('utf-8')).split()
	
	for i in range(len(conf)):
		stat = config_convert(conf[i], f"config_{i}_vless", f"{conf_path}/sub_conf")
		if stat != 1:
			os.system(f"sed -i 's/\"false\"/false/g' {conf_path}/sub_conf/config_{i}_vless.json")
			os.system(f"sed -i 's/\"true\"/true/g' {conf_path}/sub_conf/config_{i}_vless.json")
		


def mac_decode_sub(conf_path, conf_file):
	if os.system(f"ls {conf_path}/sub_conf {go_null}") == 0:
		os.system(f"rm -rf {conf_path}/sub_conf")
		os.system(f"mkdir {conf_path}/sub_conf")
	else:
		os.system(f"mkdir {conf_path}/sub_conf {go_null}")

	b64 = open(f"{conf_path}/{conf_file}", "r").readline()
	conf = str(base64.b64decode(b64).decode('utf-8')).split()
	
	for i in range(len(conf)):
		stat = config_convert(conf[i], f"config_{i}_vless", f"{conf_path}/sub_conf")
		if stat != 1:
			os.system(f" cat {conf_path}/sub_conf/config_{i}_vless.json | sed 's/\"true\"/true/g' | tee  {conf_path}/sub_conf/config_{i}_vless.json &> /dev/null")
			os.system(f" cat {conf_path}/sub_conf/config_{i}_vless.json | sed 's/\"false\"/false/g' | tee  {conf_path}/sub_conf/config_{i}_vless.json &> /dev/null")
		



def find_name(name):
	for i in range(len(config_down)):
		if config_down[i].split("=")[0] == f"{name}":
			return config_down[i].split("=")[1]

def config_convert(config, json_file_name, path_dir):

	config_top = config.split("#")[0].split("?")[0]

	config_protocol = config_top.split("://")[0]
	
	if config_protocol != "vless":
		return 1

	config_id = config_top.split("://")[1].split(":")[0].split("@")[0]
	config_addr = config_top.split("://")[1].split(":")[0].split("@")[1]
	config_port = config_top.split("://")[1].split(":")[1]


	global config_down
	config_down = config.split("#")[0].split("?")[1].split("&")

	global mirror_name
	mirror_name = {
	"sni"        : "serverName",
	"type"       : "network",
	"serviceName": "serviceName",
	"alpn"       : "alpn",
	"security"   : "security",
	"flow"		 : "flow"
	}

	conf_serverName = find_name("sni")
	conf_type = find_name("type")
	conf_serviceName = find_name("serviceName")
	conf_alpn = find_name("alpn")
	conf_security = find_name("security")
	conf_flow = find_name("flow")

	settings_type = {
	"tls" : "tlsSettings" ,
    "tcp" : "tcpSettings",
    "kcp" : "kcpSettings",
    "ws"  : "wsSettings",
    "http": "httpSettings",
    "quic": "quicSettings",
    "ds"  : "dsSettings",
    "grpc": "grpcSettings"
	}

	type_of_setting = str()
	for i in range(len(config_down)):
		if config_down[i].split("=")[0] == "type":
			for j in settings_type.keys():
				if j == config_down[i].split("=")[1]:
					type_of_setting = settings_type[j]


	all_config = {

	  "dns": {
	    "hosts": {
	      "domain:googleapis.cn": "googleapis.com"
	    },
	    "servers": [
	      "1.1.1.1"
	    ]
	  },
	  "inbounds": [
	    {
	      "listen": "127.0.0.1",
	      "port": 10808,
	      "protocol": "socks",
	      "settings": {
	        "auth": "noauth",
	        "udp": "true",
	        "userLevel": 8
	      },
	      "sniffing": {

	      "destOverride": [
          "http",
          "tls"
        	],
        "enabled": "true"
      	  },
	      "tag": "socks"
	    },
	    {
	      "listen": "127.0.0.1",
	      "port": 10809,
	      "protocol": "http",
	      "settings": {
	        "userLevel": 8
	      },
	      "tag": "http"
	    }
	  ],
	  "log": {
	    "loglevel": "warning"
	  },
	  "outbounds": [
	    {
	      "mux": {
	        "concurrency": 8,
	        "enabled": "false"
	      },
	      "protocol": f"{config_protocol}",
	      "settings": {
	        "vnext": [
	          {
	            "address": f"{config_addr}",
	            "port": int(f"{config_port}"),
	            "users": [
	              {
	                "encryption": "none",
	                "flow": f"{conf_flow}",
	                "id": f"{config_id}",
	                "level": 8,
	                "security": "auto"
	              }
	            ]
	          }
	        ]
	      },
	      "streamSettings": {
	        f"{type_of_setting}": {
	          "multiMode": "false",
	          "serviceName": f"{conf_serviceName}"
	        },
	        "network": f"{conf_type}",
	        "security": f"{conf_security}",
	        "tlsSettings": {
	          "allowInsecure": "false",
	          "alpn": [
	            f"{conf_alpn}"
	          ],
	          "serverName": f"{conf_serverName}"
	        }
	      },
	      "tag": "proxy"
	    },
	    {
	      "protocol": "freedom",
	      "settings": {},
	      "tag": "direct"
	    },
	    {
	      "protocol": "blackhole",
	      "settings": {
	        "response": {
	          "type": "http"
	        }
	      },
	      "tag": "block"
	    }
	  ],
	  "routing": {
	    "domainMatcher": "mph",
	    "domainStrategy": "IPIfNonMatch",
	    "rules": [
	      {
	        "ip": [
	          "1.1.1.1"
	        ],
	        "outboundTag": "proxy",
	        "port": 53,
	        "type": "field"
	      }
	    ]
	  }
	}
	real_file_name = f"{path_dir}/{json_file_name}.json"
	with open(real_file_name, "w") as f:
		f.write(json.dumps(all_config))

def help():
	print(\
f"""{color_bold}Usage{color_reset}: autov2ray [OPTION]...
Setup and Manage System for v2ray Protocol

{color_bold}OPTIONS{color_reset}
\t {color_green}start{color_reset} : Running Script in Background 
\t {color_green}stop{color_reset} : Kill the Script From Process List 
\t {color_green}setall{color_reset} : Download Dependencies and Running Script in Background 
\t {color_green}download{color_reset} : just Download Dependencies 
\t {color_green}help{color_reset} : show this Help Page 
{color_bold}FILES{color_reset}
\t {color_yellow}~/Desktop/ProxyProject/*{color_reset}
{color_bold}AUTHOR{color_reset}
\t {color_yellow}https://github.com/MrParhamDev{color_reset}
""")

# linux functions
def linux_download():
	linux_depends()
	linux_v2ray_download()
	linux_v2ray_extract()
	linux_config_download()
	download_sub = int(input(f"{color_yellow}\nYou want using subscription links? (YES:1 , NO):2): {color_reset}"))
	if download_sub == 1:
		linux_sub_setall()
	print(f"\n{color_green}complete!{color_reset}")

def linux_setall():
	linux_depends()
	linux_v2ray_download()
	linux_v2ray_extract()
	linux_config_download()
	dns_check()
	linux_setall_sub = int(input(f"{color_yellow}\nUsing default configurations or subscription links? (Defualt:1 , Sub Link:2): {color_reset}"))
	if linux_setall_sub == 1:
		linux_run_v2ray()
	elif linux_setall_sub == 2:
		linux_sub_setall()
	else:
		print(f"{color_red}Wrong selection, try again{color_reset}")
		linux_setall()

def linux_start():
	dns_check()
	linux_start_sub = int(input(f"{color_yellow}Using default configurations or subscription links? (Defualt:1 , Sub Link:2): {color_reset}"))
	if linux_start_sub == 1:
		linux_run_v2ray()
	elif linux_start_sub == 2:
		linux_sub_start()
	else:
		print(f"{color_red}Wrong selection, try again{color_reset}")
		linux_start()

def linux_stop():

	if linux_cmd_status(f"ls {main_path}/.pid {go_null}") == 0:
		os.system(f"kill $(cat {main_path}/.pid)")
		os.system(f"rm {main_path}/.pid")
		print(f"{color_red}Stopped{color_reset}")
	else:
		print(f"{color_red}script already not running{color_reset}")

# mac functions
def mac_download():
	mac_dependencies()
	mac_createPATH()
	mac_clone_gitrepo()
	download_sub = int(input(f"{color_yellow}\nYou want using subscription links? (YES:1 , NO):2): {color_reset}"))
	if download_sub == 1:
		mac_sub_setall()
	print(f"{color_green}complete!{color_reset}")

def mac_setall():
	mac_dependencies()
	mac_createPATH()
	mac_clone_gitrepo()
	dns_check()
	mac_setall_sub = int(input(f"{color_yellow}Using default configurations or subscription links? (Defualt:1 , Sub Link:2): {color_reset}"))
	if mac_setall_sub == 1:
		mac_run_v2ray()
	elif mac_setall_sub == 2:
		mac_sub_setall()
	else:
		print(f"{color_red}Wrong selection, try again{color_reset}")
		mac_setall()

def mac_start():
	dns_check()
	mac_start_sub = int(input(f"{color_yellow}Using default configurations or subscription links? (Defualt:1 , Sub Link:2): {color_reset}"))
	if mac_start_sub == 1:
		mac_run_v2ray()
	elif mac_start_sub == 2:
		mac_sub_start()
	else:
		print(f"{color_red}Wrong selection, try again{color_reset}")
		mac_start()
	

def mac_stop():
	os.system("sudo kill -9 $(pgrep v2ray)")
	print(f"{color_red}V2ray Successfuly Stopped {color_reset}")

# script start from here
# check python version
python_version = int(sys.version[0])
if python_version != 3:
	print("update your python version")
	exit(1)


if len(sys.argv) > 1:
	arg = sys.argv[1]

	# arguments for Gnu/Linux
	if sys.platform == "linux":
		banner()
		if arg == "help":
			help()
		elif arg == "setall":
			linux_setall()
		elif arg == "download":
			linux_download()
		elif arg == "start":
			linux_start()
		elif arg == "stop":
			linux_stop()
		else:
			banner()
			help()

	# arguments for macOS
	elif sys.platform == "darwin":
		banner()
		if arg == "help":
			help()
		elif arg == "download":
			mac_download()		
		elif arg == "setall":
			mac_setall()
		elif arg == "start":
			mac_start()		
		elif arg == "stop":
			mac_stop()
		else:
			banner()
			help()

	else:
		print(f"{color_red} this script dosn't support your os {color_reset}")
		exit(1)
else:
	banner()
	help()
