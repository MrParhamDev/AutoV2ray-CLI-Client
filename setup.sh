#! /bin/bash

color_green="\33[32m"
color_reset="\033[0m"
color_bold="\033[1m"

scr_run(){
		user_name=$USER
		mkdir -p $HOME/.config/autoV2ray
		cp ./autoV2ray.py $HOME/.config/autoV2ray
		sudo chmod 755 $HOME/.config/autoV2ray/autoV2ray.py

		printf "#!/bin/bash\npython3 /home/$user_name/.config/autoV2ray/autoV2ray.py \$1" > autoV2ray	
		sudo chmod 755 autoV2ray
		sudo mv autoV2ray /bin/
		
		printf "$color_green"		
		printf "Now do this:\n"
		printf "$color_reset"
		printf "\t$color_bold\$ autoV2ray help\n"
		printf "$color_reset"
}	

scr_help(){
	printf "$color_green"
	printf "Make life easier for users\n"
	printf "$color_reset"
	printf "After running this script you can run autoV2ray every where\n"
	printf "Run this script like this:\n"
	printf "\t$color_bold\$ bash setup.sh run\n"
	printf "$color_reset"
}

if [[ $1 = "run" ]]; then
	scr_run
else
	scr_help
fi
