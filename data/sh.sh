#!/bin/bash

for f in `ls`
do
[ $f == "sh.sh" ] && continue
sed '/Shepherd/d' $f >temp
mv temp $f
done
