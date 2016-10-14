#!/bin/sh
# @Author: anchen
# @Date:   2016-09-11 20:06:25
# @Last Modified by:   anchen
# @Last Modified time: 2016-10-10 10:24:06
cur_dir=$(pwd)
jadx_dir='/jadx/build/jadx/bin'
run_env=$cur_dir$jadx_dir

user_name=$(whoami)
setting_file=/home/$user_name/.bash_profile

env_setting='export PATH='$run_env':$PATH'
echo $env_setting >> $setting_file
source $setting_file