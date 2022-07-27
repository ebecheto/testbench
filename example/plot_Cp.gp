set ylabel "Cp [pF]"
set y2label "Zin [Ohm] = 1/(2.pi.Cp.Freq)"
set xlabel "Frequency [Hz]"
set logscale x
set logscale y2
#"cap_"+capa+"_injection.dat"
files=system("ls cap_*_injection.dat")

#plot for [file in files] file w l u 1:2 t file

plot for [file in files] file u 1:(abs($3)) w lp t file
