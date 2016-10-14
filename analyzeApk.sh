#!/bin/sh
# @Author: anchen
# @Date:   2016-08-23 15:33:15
# @Last Modified by:   anchen
# @Last Modified time: 2016-10-14 16:32:18
xml_exist=1
xml_noHas=0
out_log='log/virus_analyze.log'
key_code_block='result/key_codeblock.txt'
action_permission_report='result/act_permis.txt'
temp_log='temp/temp.txt'
decode_time_log='log/decode_time.log'
key_codeblock_temp='temp/key_codeblock_temp.txt'
act_permis_temp='temp/act_permis_temp.txt'
apk_tell_out='result/apk_tell_report.txt'
database_data_out_path='result/apk_data.txt'
apk_log_temp='temp/apk_log_temp.txt'

DecompilingApk()
{
    JAVA_OPTS="-Xmx4G" jadx -j 1 -d $2 $1 > $temp_log
}

getFileNameFromPath()
{
    get=$1
    div=($(tr "/" " " <<< $get))
    sum=${#div[@]}
    let index=$sum-1
    tar=${div[$index]}
    echo $tar 
}

dir=$1
tar=${dir%%.*}
apk_md5=$(getFileNameFromPath $tar)

#$1 APK文件路径 $2 源码包输出路径
msg=':begin to decode apk.............'
echo $apk_md5$msg
DecompilingApk $1  $2
#解析APK反编译日志文件
echo 'begin to analyze decode apk log.............'
python ApkDecodeLogHandler.py $temp_log  $out_log  $apk_md5
#解析APK反编译消耗时间
python decodeTimeCouter.py  $temp_log   $decode_time_log   $apk_md5
#检索关键代码段
echo 'begin to find key codeblock........................'
python codeSort.py $2  $apk_md5   $key_code_block  $out_log  $key_codeblock_temp
#计算源码包文件个数
fileNum=`ls -lR  $2 | grep "^-" | wc -l`
echo "fileNum:"$fileNum  >>  $decode_time_log
#检索权限和action
xml_file_name=/AndroidManifest.xml
xml_path=$2$xml_file_name
echo 'begin to find action and permission........................'

detect_xml()
{
    python actionPraser.py $xml_path $apk_md5  $action_permission_report $out_log  $act_permis_temp
    ret=$?
    if test $[ret] -eq 1
    then
        echo $xml_exist
    else
        echo $xml_noHas  
    fi
}

ret=$(detect_xml)
if test $[ret] -eq  1                                
then
    #分析APK病毒系数
    echo 'begin to tell apk.................................................'
    python virus_apk_tell.py $apk_md5 $key_codeblock_temp $act_permis_temp $apk_tell_out
    #生成入库数据文件
    echo 'begin to generator datafile for database..............................'
    python database_data_sort.py $apk_log_temp $apk_tell_out $database_data_out_path 
    #把数据导入数据库
    echo 'push data to database......................................................'
    bcp SMMC4DB..virus_apk_info in $database_data_out_path -Usmmcuser -Ptrustelsmmc -SSMMCASE -c -t'|' -r'\n' -Y
    echo '...................................finish......................................'
else
    echo 'xml is no exist,stop all step!'
fi 