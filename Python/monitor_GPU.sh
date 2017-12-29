#!/bin/bash

# 监控本机的GPU使用情况,当存在使用率小于20%的GPU时,使用该GPUS执行预定的脚本
echo -e "Lock and load!\n"
declare -i i=-1
#存储统计出的本机GPU的使用量
GPUs=(False False False False)

#输出GPU当前状态
# usage=$(nvidia-smi | grep '\([0-9]\{1,5\}MiB./..[0-9]\{,5\}MiB\)' \
# | awk '{print $9 / $11 * 100 "%"}')

# echo 'The usage of each GPU is:'
# echo -e "$usage \n"

# for line in $usage
# do
#   i+=1;
#   flag=$(echo $line 20 $i | awk '{if($1<$2){print "true"} else{print "false"}}')
#   #echo $i:$flag 
#   if [[ $flag = "true" ]];then
#     #echo "yes"
#     GPUs[$i]=$flag
#   fi
# done

monitorGPU(){
  usage=$(nvidia-smi | grep '\([0-9]\{1,5\}MiB./..[0-9]\{,5\}MiB\)' \
           | awk '{print $9 / $11 * 100 "%"}')

  echo 'The usage of each GPU is:'
  echo -e "$usage \n"

  # 处理GPU状态
  for line in $usage
  do
    i+=1;
    flag=$(echo $line 20 $i | awk '{if($1<$2){print "true"} else{print "false"}}')
    #echo $i:$flag 
    if [[ $flag = "true" ]];then
      GPUs[$i]=$flag
    fi
   done                   
}

#cuda_device=False

gpu_stat="false"
while [[ $gpu_stat = "false" ]];do
  monitorGPU
  declare -i c=-1
  for f in ${GPUs[*]}
  do
    c+=1
    if [[ $f = "true" ]];then
      #cuda_device+=$c
      echo "GPU $c not Affirmative! Fire in the hole! "
      exec ./mission.sh $c
      gpu_stat=true
    else
      echo "CUDA device $c is negative! F.O will stay on mission!"
    fi
  done
  echo -e "\n"
  sleep 5
done

# for f in ${GPUs[*]}
# do
#   c+=1
#  # echo $c:$f
#   if [[ $f = "true" ]];then
#     cuda_device+=$c
#     echo "GPU $c Affirmative! Fire in the hole! "
#     # 传入设备号
#     exec ./mission.sh $c
#   else
#     echo "CUDA device $c is negative! F.O. will stay on mission!" 
#   fi
# done

#echo $cuda_device
#echo "Affirmative! Fire in the hole! "
#exec ./test.sh
#top
