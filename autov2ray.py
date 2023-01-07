#!/usr/bin/python3

import os
import subprocess
import sys

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
        os.system(f"git clone https://github.com/MrParhamDev/V2ray_configs {main_path}/configs &> /dev/null ")
    else:
        os.system(f"rm -rf {main_path}/configs/.git")
        print(f"{color_bold}Cloning V2ray json Configs ... {color_reset}", "\n")
        os.system(f"git clone https://github.com/MrParhamDev/V2ray_configs {main_path}/configs &> /dev/null")



# find fast server From json configs
def mac_find_fast_server():
    print(f"{color_bold}Testing the Servers ... {color_reset}")
    list_server = subprocess.check_output(f"ls {main_path}/configs",shell=True,encoding='utf-8').replace(".json","").replace(" ",'').split()
    avrs = []
    for i in list_server:
        if os.system(f"ping -c1 {i} &> /dev/null") == 0:            
            a = subprocess.check_output(f"ping -c 3 {i} | tail -n1 | cut -d' ' -f4 | cut -d'/' -f2",shell=True,encoding="utf-8").replace("\n" , "")
            avrs.append(float(a))
            print(f"{i} {color_green}OK{color_reset}   Speed:{color_yellow} {a} {color_reset}ms")
        else:
            print(f"{i} {color_red} Not Working!{color_reset}")
            list_server.remove(i)
    print(color_reset)

    global fast_server
    fast_server = list_server[0]
    min = avrs[0]
    for i in range(1, len(avrs)):
        if avrs[i] < min:
            min = avrs[i]
            fast_server = list_server[i]
    


# check the successful Get tun2socks or not
def recheckTun2socksZIP():
    if mac_checkExistDir(f"{main_path}/tun2socks/*") == 0:
        print(f"{color_green}Downloading tun2socks Zip File successfuly {color_reset}")
    else:
        print(f"{color_red}Downloading tun2socks Zip File Failed {color_reset}")
        

# Running the v2ray
def mac_run_v2ray():
    if os.system(f"pgrep v2ray &> /dev/null") == 0:
        v2ray_pid = subprocess.check_output("pgrep v2ray" , shell=True , encoding="utf-8").replace("\n" , "")
        print(f"{color_red}V2ray Already Runned{color_reset}   ProcessID: {color_yellow}{v2ray_pid}{color_reset}")
    else:
        print(f"{color_green} v2ray Successfully running {color_reset}")
        os.system(f"v2ray -c {main_path}/configs/{fast_server}.json &> /dev/null &")



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


def linux_run_v2ray():
	print("running v2ray...")

	if linux_cmd_status(f"ls {main_path}/pid {go_null}") == 0:
		print(f"{color_red}v2ray already running{color_reset}")
	else:
		print(f"{color_green}v2ray Successfully running {color_reset}")
		os.system(f"{linux_v2ray_dir}/v2ray run -c {linux_config_dir}/{linux_fast_server} {go_null} & echo $! > {main_path}/pid ")

def linux_find_fast_server():
	print("\nfind fast server...")

	list_server =  subprocess.check_output(f"ls {linux_config_dir}",
				shell=True,
				encoding='utf-8').replace(".json","").replace(" ",'').split()
	avrs = []
	for i in list_server:
		if linux_cmd_status(f"ping -c1 {i} {go_null}") == 0:			

			get_avr =  subprocess.check_output(f"ping -c 3 {i} | tail -n1 | cut -d' ' -f4 | cut -d'/' -f2",
									shell=True,
									encoding="utf-8").replace("\n" , "")
			
			avrs.append(float(get_avr))
			print(f"{i} {color_green} work! {color_reset} speed: {color_yellow} {get_avr} {color_reset}")

		else:
			print(f"{i} {color_red}not work{color_reset}")
			list_server.remove(i)
	print(color_reset)
	global linux_fast_server
	linux_fast_server = list_server[0]
	min = avrs[0]
	for i in range(1, len(avrs)):
		if avrs[i] < min:
			min = avrs[i]
			linux_fast_server = list_server[i]

	linux_fast_server += ".json"
	
def linux_config_download():
	print("\ninstall configs...", end='')

	
	len_files =  subprocess.check_output("", shell=True, encoding="utf-8")

	if linux_cmd_status(f"ls {linux_config_dir} {go_null}") == 1 :
		os.mkdir(f"{linux_config_dir}")
		os.system(f"git clone https://github.com/MrParhamDev/\
V2ray_configs.git {linux_config_dir} {go_null}")

	elif linux_cmd_status(f"ls {linux_config_dir}/* {go_null}") == 0:
		os.system(f"rm -rf {linux_config_dir}/* {linux_config_dir}/.git")
		os.system(f"git clone https://github.com/MrParhamDev/\
V2ray_configs.git {linux_config_dir} {go_null}")

	else:
		os.system(f"git clone https://github.com/MrParhamDev/\
V2ray_configs.git {linux_config_dir} {go_null}")

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
			break

def linux_cmd_status(cmd):
	stat = os.system(cmd)
	if stat == 0:
		return 0
	else:
		return 1

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
	print(f"\n{color_green}complete!{color_reset}")

def linux_setall():
	linux_depends()
	linux_v2ray_download()
	linux_v2ray_extract()
	linux_config_download()
	linux_find_fast_server()
	linux_run_v2ray()

def linux_start():
	linux_find_fast_server()
	linux_run_v2ray()

def linux_stop():

	if linux_cmd_status(f"ls {main_path}/pid {go_null}") == 0:
		os.system(f"kill $(cat {main_path}/pid)")
		os.system(f"rm {main_path}/pid")
		print(f"{color_red}Stopped{color_reset}")
	else:
		print(f"{color_red}script already not running{color_reset}")

# mac functions
def mac_download():
	mac_dependencies()
	mac_createPATH()
	mac_clone_gitrepo()
	print(f"{color_green}complete!{color_reset}")

def mac_setall():
	mac_dependencies()
	mac_createPATH()
	mac_clone_gitrepo()
	mac_find_fast_server()
	mac_run_v2ray()

def mac_start():
	mac_find_fast_server()
	mac_run_v2ray()

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
			help()

	# arguments for macOS
	elif sys.platform == "darwin":
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
			help()

	else:
		print(f"{color_red} script dosn't support your os {color_reset}")
		exit(1)
else:
	help()
