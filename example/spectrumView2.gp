# file="spectrumView.dat"
# plot file u 0:1 w lp
set tics format "%.1s%c"
# ':WFMOUTPRE:BYT_NR 8;BIT_NR 64;:WFMOUTPRE:ENCDG ASCII;BN_FMT FP;:WFMOUTPRE:ASC_FMT FP;BYT_OR LSB;:WFMOUTPRE:WFID "CH1_SV_NORMAL, 1901 points, Center Freq: 710.0737MHz, Span: 10MHz, FFTlength 0";NR_PT 1901;:WFMOUTPRE:PT_FMT Y;PT_ORDER LINEAR;:WFMOUTPRE:XUNIT "Hz";XINCR 5.2631578947368E+3;:WFMOUTPRE:XZERO 705.0736842000E+6;PT_OFF 0;:WFMOUTPRE:YUNIT "dBm";YMULT 1.0000;:WFMOUTPRE:YOFF 0.0E+0;YZERO 0.0E+0;:WFMOUTPRE:DOMAIN FREQUENCY;WFMTYPE RF_FD;:WFMOUTPRE:CENTERFREQUENCY 710.0737E+6;SPAN 10.0000E+6;:WFMOUTPRE:FFTLENGTH 9.91E+37;RESAMPLE 1'
YUNIT="dBm"
XUNIT="Hz"
XZERO=705.0736842000E+6
XINCR=5.2631578947368E+3
file="spectrumView.txt"
WFID="CH1_SV_NORMAL, 1901 points, Center Freq: 710.0737MHz, Span: 10MHz, FFTlength 0"
set xtics right rotate by 45 
set ylabel "[".YUNIT."]"
set xlabel "[".XUNIT."]"

plot file u (XZERO+$0*XINCR):1 w lp t WFID
