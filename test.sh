#!/bin/bash

choice=$1
arguement1=$2
arguement2=$3
arguement3=$4
arguement4=$5
arguement5=$6
arguement6=$7
arguement7=$8
arguement8=$9

if [ "$choice" == "print" ]
then
	python firewallcrud.py print > file.txt

elif [ "$choice" == "create" ]
then
	python firewallcrud.py create $arguement1 $arguement2 $arguement3 $arguement4 $arguement5 $arguement6 $arguement7 > file.txt

elif [ "$choice" == "update" ]
then
 	python firewallcrud.py update $arguement1 $arguement2 $arguement3 $arguement4 $arguement5 $arguement6 $arguement7 $arguement8 > file.txt

elif [ "$choice" == "delete" ]
then
	python firewallcrud.py delete $arguement1 > file.txt
fi
