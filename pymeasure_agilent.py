
import pymeasure
#pymeasure.__version_

from pymeasure.instruments.agilent import agilent34410A

pymeasure.instruments.list_resources()
pymeasure.instruments.resources[0]  

class pymeasure.instruments.agilent.Agilent34410A(adapter, **kwargs)
    property current_ac
    AC current, in Amps
    property current_dc
    DC current, in Amps
    property resistance
    Resistance, in Ohms
    property resistance_4w
    Four-wires (remote sensing) resistance, in Ohms
    property voltage_ac
    AC voltage, in Volts


dmm = Agilent34450A("USB0::...")
dmm.reset()
dmm.configure_voltage()
print(dmm.voltage)
dmm.shutdown()

from pymeasure.adapters import VISAAdapter

0 : USB0::0x0957::0x0607::MY47002100::INSTR : Agilent Technologies,34410A,MY47002100,2.35-2.35-0.09-46-09    
USB0::0x0957

pymeasure.instruments.agilent.Agilent34410A("USB0::0x0957")
pymeasure.instruments.agilent.Agilent34410A("0 : USB0::0x0957::0x0607::MY47002100::INSTR : Agilent Technologies,34410A,MY47002100,2.35-2.35-0.09-46-09")


