#!/bin/sh

BASEFILE="./core-sounds-ja.csv"
TEMPLATE="./template.json"

mkdir -p ja
mkdir -p ja/digits
mkdir -p ja/letters
mkdir -p ja/phonetic

while read i
do
    TLINE=`echo $i | sed  's/"//g'`
    FNAME=`echo $TLINE | cut -f2,2 -d','`
    TTEXT=`echo $TLINE | cut -f3,3 -d',' | sed 's/\r//g'`
    cat $TEMPLATE  | sed s/###TEXTHERE###/$TTEXT/ > ja/$FNAME.json
    echo $FNAME

done < $BASEFILE
