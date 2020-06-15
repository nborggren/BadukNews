#!/bin/bash
for ((i=$1;i<=$2;i++));do
    ./grab2.sh $i
    echo $i
done 


