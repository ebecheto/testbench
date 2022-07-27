set ylabel "Cp [pF]"
set y2label "Zin [Ohm] = 1/(2.pi.Cp.Freq)"
set xlabel "Frequency [Hz]"
set logscale x
set logscale y2
plot 'cap_injection.dat' u 1:(abs($3)) w lp,\
     '' u 1:(1/2.0/3.14/abs($3)/$1) w lp axis x1y2
