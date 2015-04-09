import ThermalEnclosureWTL64

wt = ThermalEnclosureWTL64.ThermalEnclosureWTL64('192.168.0.44')
wt.start=True
wt.setTemp(10)

## wt.start = False
## wt.setState()

