import ThermalEnclosureWTL64

wt = ThermalEnclosureWTL64.ThermalEnclosureWTL64('169.254.222.44')
wt.start=True
wt.setTemp(10)
wt.getTemp()

# stop
# wt.start = False
# wt.setState()

