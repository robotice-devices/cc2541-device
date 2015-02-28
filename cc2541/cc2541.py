
import logging
import pexpect

LOG = logging.getLogger(__name__)

from .utils import *


class CC2541(object):


    def __init__(self, address=None, *args, **kwargs):
        super(CC2541, self).__init__(*args, **kwargs)
        self.address = address

    def char_write_cmd( self, handle, value ):
        # The 0%x for value is VERY naughty!  Fix this!
        cmd = 'char-write-cmd 0x%02x 0%x' % (handle, value)
        LOG.debug(cmd)
        return self.connection.sendline(cmd)

    def char_read_hnd( self, handle ):
        self.connection.sendline('char-read-hnd 0x%02x' % handle)
        self.connection.expect('descriptor: .*? \r')
        after = self.connection.after
        rval = after.split()[1:]
        return [long(float.fromhex(n)) for n in rval]

    def connect(self, address=None):
        bluetooth_adr = getattr(self, "address", None)
        if address:
            bluetooth_adr = address
        tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
        tool.expect('\[LE\]>')
        print "Preparing to connect. You might need to press the side button..."
        tool.sendline('connect')
        tool.expect('\[CON\].*>')
        tool.sendline('char-write-cmd 0x29 01')
        tool.expect('\[LE\]>')
        return tool        

    @property
    def connection(self):
        con = getattr(self, "_connection", None)
        if not con:
            self._connection = self.connect()
        return self._connection

    @property
    def temperature(self):
        LOG.debug("Start reading temperature")
        self.connection.sendline('char-read-hnd 0x25')
        self.connection.expect('descriptor: .*')
        rval = self.connection.after.split()
        objT = floatfromhex(rval[2] + rval[1])
        ambT = floatfromhex(rval[4] + rval[3])
        return calcTmpTarget(objT, ambT)

    @property
    def accelerometer(self):
        # enable accelerometer
        self.char_write_cmd(0x31,0x01)
        self.char_write_cmd(0x2e,0x0100)
        v = self.char_read_hnd(0x2d)
        (xyz,mag) = calcAccel(v[0],v[1],v[2])
        return xyz

    @property
    def gyroscope(self):
        # enable gyroscope
        self.char_write_cmd(0x5b,0x07)
        self.char_write_cmd(0x58,0x0100)
        return self.char_read_hnd(0x57)

    @property
    def humidity(self):
        self.char_write_cmd(0x3c,0x01)
        self.char_write_cmd(0x39,0x0100)
        v = self.char_read_hnd(0x38)
        rawT = (v[1]<<8)+v[0]
        rawH = (v[3]<<8)+v[2]
        (t, rh) = calcHum(rawT, rawH)
        return rh

    @property
    def barometer(self):
        # fetch barometer calibration
        self.char_write_cmd(0x4f,0x02)
        rawcal = self.char_read_hnd(0x52)
        barometer = Barometer( rawcal )
        # enable barometer
        self.char_write_cmd(0x4f,0x01)
        self.char_write_cmd(0x4c,0x0100)
        v = self.char_read_hnd(0x4b)
        rawT = (v[1]<<8)+v[0]
        rawP = (v[3]<<8)+v[2]
        (temp, pres) = barometer.calc(rawT, rawP)
        return temp, pres

    @property
    def magnet(self):
        self.char_write_cmd(0x44,0x01)
        self.char_write_cmd(0x41,0x0100)
        v = self.char_read_hnd(0x40)
        x = (v[1]<<8)+v[0]
        y = (v[3]<<8)+v[2]
        z = (v[5]<<8)+v[4]
        xyz = calcMagn(x, y, z)
        return xyz