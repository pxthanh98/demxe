#!/bin/bash
for dir in /data/FairMOT/data/demxe/images/train/*
do
	cd "$dir"
	line=`ls img1/ | wc -l`
	name=`basename $PWD`
	echo "[Sequence]" >> seqinfo.ini
	echo "name=$name" >> seqinfo.ini
	echo "imgDir=img1" >> seqinfo.ini
	echo "frameRate=30" >> seqinfo.ini
	echo "seqLength=$line" >> seqinfo.ini
	echo "imWidth=1280" >> seqinfo.ini
	echo "imHeight=720" >> seqinfo.ini
	echo "imExt=.jpg" >> seqinfo.ini
done
