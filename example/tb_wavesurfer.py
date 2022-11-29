#!/usr/bin/python2
import  OscilloWavePro

osc = OscilloWavePro.OscilloWavePro('192.168.0.41')
print "osc connected"
osc.send("vbs 'app.SystemControl.CloseDialog'")#<== ferme le panel si ouvert
osc.send("vbs? 'return=app.LogicAnalyzer.Digital1.Out.Result'")
osc.send("vbs? 'return=app.LogicAnalyzer.Digital1.Out.Result.BusName'")
osc.send("vbs? 'app.SerialDecode.Decode1.Out.Result.CellType(1, 1)'")
osc.send("vbs 'app.SerialDecode.Decode1.Out.Result.CellValue(0, 0)'")

osc.send("vbs 'Dim CellType As Integer'")
osc.send("CellType = app.SerialDecode.Decode1.Out.Result.CellType(1, 1)'")
osc.send("XYwform = app.Math.XY.Out.Result.DataArray'")
osc.send("VBS 'app.Measure.ShowMeasure = true")
osc.send("""VBS? 'app.Measure.P1.ParamEngine="Mean" ' """)
osc.send("VBS? 'return=app.Measure.P1.Out.Result.Value' ")
osc.send("vbs? 'Return = app.Acquisition.Horizontal.NumPoints'")
#VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(nr_samples, nr_lines, offset_samples, frameOffset, lineOffset)'
osc.send("VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,1,0,0)(0,0)'") #=> 0

osc.send("VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1)'")

#https://electronics.stackexchange.com/questions/430542/reading-digital-wafevorms-via-vxi11-from-the-lecroy-wavesurfer-510-ms-500

osc.send("VBS? 'return=app.Object.Item(\'Acquisition\')'")


osc.send("vbs? 'Dim BusName As String: BusName=app.LogicAnalyzer.Digital1.Out.Result.BusName: return=BusName'")

osc.send("vbs? return=app.LogicAnalyzer.Digital1.Out.Result.BusName")

# >>> osc.send("VBS? 'Dim return As String; return=app.LogicAnalyzer.Digital2.Out.Result.DataArray'")
# 'VBS Name redefined'
# BUG apres ca ...
osc.send("vbs? return=app.LogicAnalyzer.Digital1.Out.Result.Levels'")# => 2
osc.send("vbs? return=app.LogicAnalyzer.Digital2.Out.Result.Levels'")# => 2
osc.send("vbs? 'app.LogicAnalyzer.Digital1.Out.Result.LineAliasName(0)'")
#=> "VBS Object doesn't support this property or method: 'APP.LOGICANALYZER.DIGITAL1.OUT.RESULT.LINEALIASNAME'"
osc.send("vbs? app.LogicAnalyzer.Digital1.Out.Result.LineName(0)'")
#"VBS Object doesn't support this property or method: 'APP.LOGICANALYZER.DIGITAL1.OUT.RESULT.LINENAME'"
# https://www.e-sonic.com/Upload/LeaderBoard/175cd5ce-3151-44e4-8342-9290b11c9944.pdf
osc.send("vbs? 'app.Acquisition.TriggerMode = Stopped'")
osc.send("vbs  app.Acquisition.Acquire (10, True)")
osc.send("vbs? return=app.LogicAnalyzer.Digital1.Out.Result.Lines") #=> 16
osc.send("vbs? return=app.LogicAnalyzer.Digital1.Out.Result.Samples") #=> 100002
osc.send("vbs? return=app.Acquisition.C1.Out.Result.Sweeps") # =>'VBS 123606'
osc.send("vbs? return=app.Acquisition.Digital1.Out.Result.Top") # => NON
osc.send("vbs? ret=app.LogicAnalyzer.Digital1.Out.Result.Lines:return=2*ret") #=> 'VBS 32'
# wform = app.LogicAnalyzer.Digital1.Out.Result.DataArray(nSamples, nLines,startIndex, startLine)
osc.send("vbs? return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(-1,-1,0,0)") # LOO LONG ! BUG?

osc.send("vbs? return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,-1,0,0)") #


osc.send("VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,1,50000,0)(0,0)'") #=> 0
osc.send("VBS? data=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,1,50000,0):return=UBound(data)") #=> FAIL

osc.send("VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(-1,1,0,4)(1,0)'") #=> 1

osc.send("VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,-1,0,4)(1,0)'") #=> 1

osc.send("VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,-1,1,4)(0,0)'")

osc.send("VBS? 'return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,-1,1000,4)(0,0)'")


osc.send("vbs? return=app.LogicAnalyzer.Digital1.Out.Result.DataArray(1,-1,0,0)(0,0)") #

osc.getDigitalBus() #=> '16=0x10=0b0000000000010000'osc.getDigitalBus() #=> '16=0x10=0b0000000000010000'


self=osc
setup=1
sample=1000
cmd_line = ":".join(["VBS? '",
"lines = app.LogicAnalyzer.Digital{}.Out.Result.Lines".format(setup),
"val=0",   
"res = app.LogicAnalyzer.Digital{}.Out.Result.DataArray(1,-1,{},0)".format(setup, sample),
"for line = 0 To lines-1",
"val=val + res(0,line)*2^line",
"Next",
"return=val'"
])    
samples = self.send(cmd_line)
