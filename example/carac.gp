file=  './DONE_data_ISMN0D.txt' 
splot file with lines
# set xtics 0.2; set xlabel rotate parallel;replot <= pas bon
# set ytics 0.2 rotate by 90 right;replot

Xmax=GPVAL_DATA_X_MAX;Xmin=GPVAL_DATA_X_MIN;Ymax=GPVAL_DATA_Y_MAX
Ymin=GPVAL_DATA_Y_MIN;Zmax=GPVAL_DATA_Z_MAX;Zmin=GPVAL_DATA_Z_MIN
set xrange[Xmin:Xmax];set yrange[Ymin:Ymax];set zrange[Zmin:Zmax]

set style line 81 lt 0 lc rgb "#808080" lw 0.5
# Draw the grid lines for both the major and minor tics
set grid xtics
set grid ytics
set grid mxtics
set grid mytics
set grid back ls 81;replot
set mxtics; set mytics

Vth=0.6
# ($2==vgs;$1==vds)
splot file u 1:2:($2>=Vth/2 && $2<=Vth ? $3:1/0) with lines,\
  file u 1:2:($2>=$1+Vth ? $3 : 1/0) with lines,\
  file u 1:2:($2<=$1+Vth && $2>=Vth ? $3:1/0) with lines,\
  file u 1:2:($2<=Vth/2.0 ? $3 : 1/0) with lines

set grid
set xlabel 'vds';set ylabel 'vgs';set zlabel 'IS(/MN0/D)@0' offset 4,4;replot
pause -1 'pressReturn'

set contour; replot
pause -1 'pressRet'
set cntrparam levels auto 30; replot
pause -1 'pressReturn'
pr '[OK]'#<== permit to bypass interactiv without error
unset contour;set view 90,90;replot;
pause -1 'Y axis'
pr '[OK]'
set view 90,0; replot;
pause -1 'X axis'
pr '[OK]'
set view map; replot;
pause -1 'view map axis';pr '[OK]'
#set view 60, 90, 0.5,1;replot;
set view 65, 342, 1,1;replot;
set view 77, 338, 1,1;replot;

# set ticslevel <frac>
# set xyplane <frac>
# set xyplane at <zvalue>
# show xyplane

zval=-0.004

set xyplane at zval
# varval= sprintf("%s",file)(1,1,1)
# varval= sprintf("%s",file)(1,1)
# varval = "/home/validmgr/ebecheto/Work/IC6/ams410/xv2/c35b4/DONE_data_ISMN0D.txt" (1,1)

#my_val = "/home/validmgr/ebecheto/Work/IC6/ams410/xv2/c35b4/DONE_data_ISMN0D.txt"[1][2]     # get value in 1st row and 2nd column
# pr my_val

# # stats file index 2 using 1:2 prefix "A"
# # array Data[A_records]
# set term push
# set term unknown
# # record two value of th file
# plot file every :::0::0 using (a=$1):(b=$2)
# set term pop
# stats file every :::0::0 using 1:2

# array=system(sprintf("cat %s", file))
# pr strlen(array) #=> 22268
# S=strstrt(array,"\n")
# pr S
# while(strlen(array) {
# }

# http://stackoverflow.com/questions/30749160/how-to-define-and-access-array-in-gnuplot
# aGet(name, i) = value(sprintf("_%s_%i", name, i)) 
# aSet(name, i, value) = sprintf("_%s_%i = %.16e", name, i, value)
# To assign and retrieve values on the array A you do
# eval aSet("A",2,3)
# print aGet("A",2)

set table "diod.dat"
splot  file  u 1:2:($1==$2 ? $3:1/0) with lines
unset table

set table "vdsat.dat"
splot  file  u 1:2:(abs($1-($2-Vth))<0.001 ? (Zlast=$3, $3):1/0) with lines
unset table
#pr Zlast

set arrow 9 from 3.3,3.3,zval to 3.3,3.3,GPVAL_Z_MAX nohead lt 1 lc rgb '0xD3D3D3';#<=

set arrow 11 from 0,Vth,zval to 3.3-Vth,3.3,zval nohead;replot#<=vdsat projection
set arrow 12 from 0,Vth,zval to 3.3,Vth,zval nohead;replot#<= sat/subth limit
set arrow 13 from 0,Vth/2,zval to 3.3,Vth/2,zval nohead;replot#<= subth/blocked limit
set arrow 14 from 0,Vth,zval to 0,Vth,0 lt 5 nohead dt 3;replot
set arrow 15 from 3.3-Vth,3.3,zval to 3.3-Vth,3.3,Zlast nohead lt 5 dt 3;replot



# set term unknown #This terminal will not attempt to plot anything
# plot 'myfile.dat' index 0 every 1:1:0:0:0:0 u (var=$1):1
# set term unknown #This terminal will not attempt to plot anything
# plot file index 0 every 1:1:0:0:0:0 u (var=$1):1


# Syntax: u 0:($0==RowIndex?(VariableName=$ColumnIndex):$ColumnIndex)
# RowIndex starts with 0, ColumnIndex starts with 1
# 'u' is an abbreviation for the 'using' modifier 

# file has 34 block of 34 lines ==>1156 points
block=34
position(x,y)=x*block+y
# CHOIX : A en position 28,20 GP>pr position(28,30)
# pr words("A B C D E")#=> 5
#do for [i=1:words("A B C D E")]{eval sprintf("%s = %.16e", word(i), position())}
XA=26;XB=19
pr nbA=position(XA,XB)
pr nbB=position(XA,XB+1)
pr nbC=position(XA+1,XB)
pr nbD=position(XA,XB-1)
pr nbE=position(XA-1,XB)

set table
plot file u 0:($0==nbA?(Ax=$1, Ay=$2, Az=$3):$0==nbB?(Bx=$1, By=$2, Bz=$3):$0==nbC?(Cx=$1, Cy=$2, Cz=$3):$0==nbD?(Dx=$1, Dy=$2, Dz=$3):$0==nbE?(Ex=$1, Ey=$2, Ez=$3):$3)
unset table
pr Ax, Ay, Az, Bx, By, Bz

pr A=sprintf("%.1f,%.1f,%.1g" ,Ax,Ay,Az)
pr gds=sprintf("%.1f,%.1f,%.1g" ,Ax+Bx-Dx,Ay+By-Dy,Az+Bz-Dz)
pr gm=sprintf("%.1f,%.1f,%.1g" ,Ax+Cx-Ex,Ay+Cy-Ey,Az+Cz-Ez)
#set label 20 'gm' at @gm right offset 0.1,0.1,0.001;replot
# set label 20 'gm' at @gm left;replot
# set label 21 'gds' at @gds right;replot
set arrow 16 from Ax,Ay,Az to Ax+Bx-Dx,Ay+By-Dy,Az+Bz-Dz lw 2 lc rgb 'red';replot
set arrow 17 from Ax,Ay,Az to Ax+Cx-Ex,Ay+Cy-Ey,Az+Cz-Ez lw 3 lc rgb 'red';replot
#set arrow 16 from Ax,Ay,Az rto Bx-Dx,By-Dy,Bz-Dz  lw 2 ;replot
#print 'from ',Ax,',',Ay,',',Az,' to ', Ax+Bx-Dx,',',Ay+By-Dy,',',Az+Bz-Dz 

#set arrow 17 from 0,0,0 to 1,1,0.002  ;replot
#set arrow 18 from 2.8, 3.0, 0.0086426 to  2.8, 3.2, 0.0095871 nohead;replot
#set arrow 18 from 2.6,1.9,0.0036478 to 2.6,2.1,0.0044748 head lw 4;replot
# gm=B-C en A
# gds=C-B en A

# set table # A point numero 835
# plot file u 0:($0==835?(Ax=$1, Ay=$2, Az=$3):$3)
# unset table
# x,y,z value of the 500th point
pr Ax, Ay, Az
set label 1 at Ax, Ay, Az "" point pointtype 2 pointsize 2;replot
set label 2 at Ax*.9, Ay*.9, Az*.9 " A" font 'Verdana,12' ;replot
# set label 2 at Ax*.9, Ay*.9, Az*.9 sprintf(" A(%g,%g,%g)",@A) font 'Verdana,12' ;replot

set style line 82 pointtype 7 linecolor rgb '#22aa22' pointsize 2


#splot  file  with lines, "vdsat.dat", "diod.dat"
splot file u 1:2:($2>=Vth/2 && $2<=Vth ? $3:1/0) with lines,\
  file u 1:2:($2>=$1+Vth ? $3:1/0) with lines,\
  file u 1:2:($2<=$1+Vth && $2>=Vth ? $3:1/0) with lines,\
  file u 1:2:($2<=Vth/2.0 ? $3:1/0) with lines, "vdsat.dat" title 'vds=vgs-vth' ps 0.5, "diod.dat" title 'vds=vgs' ps 0.2

#   ,\
# '+' using ($1 == Ax ? Ax : NaN):Ay:Az:(sprintf('A(%.1f,%.1f,%.1f)', Ax,Ay,Az)) \
#      with labels offset char 1,-0.2 left textcolor rgb 'blue' \
#      point linestyle 82 notitle
# http://stackoverflow.com/questions/19452516/add-a-single-point-at-an-existing-plot
# replot '-' using Ax:Ay:Az
#set label 1 at Ax, Ay, Az "A" point pointtype 2 pointsize 2

XAA=3;XB=30
nbAA=position(XAA,XB)
nbB=position(XAA,XB+1)
nbC=position(XAA+1,XB)
nbD=position(XAA,XB-1)
nbE=position(XAA-1,XB)
set table
plot file u 0:($0==nbAA?(AAx=$1, AAy=$2, AAz=$3):$0==nbB?(Bx=$1, By=$2, Bz=$3):$0==nbC?(Cx=$1, Cy=$2, Cz=$3):$0==nbD?(Dx=$1, Dy=$2, Dz=$3):$0==nbE?(Ex=$1, Ey=$2, Ez=$3):$3); unset table

pr AA=sprintf("%.1f,%.1f,%.1g" ,AAx,AAy,AAz)
pr gds=sprintf("%.1f,%.1f,%.1g" ,AAx+Bx-Dx,AAy+By-Dy,AAz+Bz-Dz)
pr gm=sprintf("%.1f,%.1f,%.1g" ,AAx+Cx-Ex,AAy+Cy-Ey,AAz+Cz-Ez)
set arrow 18 from AAx,AAy,AAz to AAx+Bx-Dx,AAy+By-Dy,AAz+Bz-Dz lw 3 lc rgb '0xFF1493';replot
set arrow 19 from AAx,AAy,AAz to AAx+Cx-Ex,AAy+Cy-Ey,AAz+Cz-Ez lw 2 lc rgb '0xFF1493';replot
set label 3 at AAx, AAy, AAz " B" font 'Verdana,12' ;replot


#splot  file  with lines, "vdsat.dat", "diod.dat"
splot file u 1:2:($2>=Vth/2 && $2<=Vth ? $3:1/0) with lines,\
  file u 1:2:($2>=$1+Vth ? $3:1/0) with lines,\
  file u 1:2:($2<=$1+Vth && $2>=Vth ? $3:1/0) with lines,\
  file u 1:2:($2<=Vth/2.0 ? $3:1/0) with lines, "vdsat.dat" title 'vds=vgs-vth' ps 0.5, "diod.dat" title 'vds=vgs' ps 0.2,\


# # PROJECTIONS :
# splot file u 1:2:($2>=Vth/2 && $2<=Vth ? (0):1/0) with lines,\
#   file u 1:2:($2>=$1+Vth-0.01 ? (0):1/0) with lines,\
#   file u 1:2:($2<=$1+Vth+0.01  && $2>=Vth ? (0):1/0) with lines,\
#   file u 1:2:($2<=Vth/2.0 ? $3:1/0) with lines,\
#   file u 1:(3.3):($3) w l lt 3 lc "black" notitle,\
#   file u (3.3):2:($3) w l  lt 3 lc "black" notitle

# set arrow 9 from 3.3,3.3,0to 3.3,3.3,GPVAL_Z_MAX nohead lw 4lc rgb 'black';#<=
# set xyplane at 0
set view 77, 338, 1,1;replot