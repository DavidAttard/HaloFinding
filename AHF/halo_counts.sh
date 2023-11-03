#!/bin/bash
#
# Count the number of haloes in every _halos file of the CURRENT DIRECTORY
#

out="halonumber.dat"
rm -f $out
touch $out
for file in `ls *_halos`
do
    hnum=`wc -l $file | awk '{print ($1-1)}'`
    zred=`echo $file | awk 'BEGIN{FS="."}{print $2 "." $3}' | sed 's/.*z//g'`
    echo "$zred   $hnum" >> $out 
done
sort -rn $out > $out.tmp
mv $out.tmp $out

echo "Data written to $out ."
exit
