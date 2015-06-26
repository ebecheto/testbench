#! /bin/bash
# ./allInOne.sh Larzic__MAX

if [ $# -eq 0 ]; then     pattern="MAX"; else   pattern=$1; fi

if [ ! -f $pattern$()0.png ]; then  mv $pattern.png $pattern$()0.png; else   pattern=$1; fi


mvCropRect () {
if [ $# -eq 0 ]; then file=ln22arzic_MAX1.png; else file=$1 ;fi

echo "input file : $file"
Y0=35
Y1=565
Yc1=$(($Y1-Y0))

# boite de dialog statistique ON ? ou OFF
#SON=0
SON=230
# expression parameter (P1 MAX) : measure box, 
YMe=$((343+$SON))
XMe=270  # 270 si deux P1 P2, 200 sinon
# C1/C2 scale mV/div AC1M ...
YC1=$((470+$SON))
XC1=200  # 200 si deux C1 C2, 100 sinon
# redBox
Yb1=$((300+$SON))
yb2=$((355+$SON))


convert $file \
\( -clone 0 -crop $XMe$()x30+0+$YMe  -repage +0-185\! \) \
\( -clone 0 -crop $XC1$()x45+3+$YC1  -repage +0-185\! \) \
\( -clone 0 -crop 220x45+1060+$YC1  -repage +0-185\! \) \
\( -stroke Red  -fill none  -strokewidth 2  -draw "roundRectangle 0,500 $XC1,560 11,11" \) \
-flatten \
\( -crop 1280x$Yc1+0+$Y0 \) \
t_$file
}  #<== define local function


# filename=$(basename $file)
# extension="${filename##*.}"
#pattern=${filename%[0-9].*}

beg=0
end=$(($(ls $pattern* |wc -l) -1))
echo " $beg $end"

for ((i=$beg;i<=$end;i++)); do mvCropRect $pattern$i.png;done

echo "concat [$beg $end].png to gif may take a while..."

convert -loop 0 t_$pattern%d.png[$beg-$end] ramp.gif

echo "optimize size try 1"

convert ramp.gif -layers OptimizeTransparency +map ramp2.gif

echo "optimize size try 2"
# convert ramp.gif -layers OptimizeFrame rampF.gif
# convert  ramp2.gif +repage  rampc.gif
# rm ramp2.gif ramp.gif
