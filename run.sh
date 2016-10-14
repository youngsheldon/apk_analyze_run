#!/bin/sh
# @Author: anchen
# @Date:   2016-10-13 16:45:05
# @Last Modified by:   anchen
# @Last Modified time: 2016-10-14 18:40:21
md5_exist=1
md5_noHas=0
decoded_log=md5_log.txt 
decode_time_log='log/decode_time.log'

new_apk_log_path=/opt/smmc/data_backup/compilation/
mv_path=/opt/smmc/data_backup/compilation/backup/
apk_log_temp='temp/apk_log_temp.txt'
apk_file_path=/opt/smmc/data_backup/apk/
bigApk=/opt/smmc/apk_parse/big_apk/

getFileSize()
{
    dir=$(du -a $1)
    var1=`echo $dir | awk -F ' ' '{print $1}'`
    echo $var1   
}

checkMd5()
{
    md5=$1
    python findMd5.py $md5
    ret=$?
    if test $[ret] -eq 1
    then
        echo $md5_exist
    else
        echo $md5_noHas  
    fi
}

DecompilingApkList()
{
    fileNmae=$1
    apk_endpoint=.apk 
    filePath=$apk_file_path$fileNmae$apk_endpoint
    sourcePath=/opt/smmc/apk_parse/apk_source/$fileNmae
    file_size=$(getFileSize $filePath)
    ret=$(checkMd5 $fileNmae)
    if test $[ret] -eq  0                                
    then
        if test $[file_size] -lt 800000
        then
            ./analyzeApk.sh $filePath $sourcePath
            echo $fileNmae >> $decoded_log
            echo 'fileSize:'$file_size >> $decode_time_log
        else
            mv $filePath $bigApk
        fi
    else
        echo $fileNmae':file had been handled'
    fi 
}

run()
{
    filelist=`ls -Sr $new_apk_log_path | grep apk_.*`
    for file in $filelist
    do 
        cat $new_apk_log_path$file | while read line
        do
        echo $line > $apk_log_temp
        apk_md5=`echo $line | awk -F  ',' '{print $3}'`
        echo $apk_md5
        DecompilingApkList $apk_md5
        done
        mv $new_apk_log_path$file $mv_path 
    done
}

while true
do
    filelist=`ls -Sr $new_apk_log_path | grep apk_.*`
    if [ "$filelist" = "" ]
    then
        echo 'the str is None'
    else
        run
    fi 
    sleep 3600 
done

