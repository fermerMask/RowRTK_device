import xml.sax.handler
import subprocess
from subprocess import PIPE
import threading
import time, datetime
import serial


class NMEA:
    mode_names = {0: 'No Fix', 1: 'Standalone', 2: 'DGNSS', 4: 'RTK Fixed', 5: 'RTK Float'}

    @classmethod
    def dm_to_sd(cls, dm):
        x = float(dm)
        d = x // 100
        m = (x - d * 100) / 60
        return d + m

    @classmethod
    def hms_to_sec(cls, hms):
        d = [int(c) for c in hms if c != '.']
        h = d[0] * 10 + d[1]
        m = d[2] * 10 + d[3]
        s = d[4] * 10 + d[5] + d[6] * 0.1 + d[7] * 0.01
        t = h * 3600 + m * 60 + s
        return t

    @classmethod
    def mile_to_meter(cls, mile):
        v = float(mile) * 1.852 * 1000 / 3600
        return v

    @classmethod
    def parse_GGA(cls, line):
        ds = line.strip().split(',')
        if len(ds) == 15 and (ds[0] == '$GNGGA' or ds[0] == '$GPGGA') and ds[1] != '' and ds[2] != '' and ds[
            4] != '' and ds[6] != '' and ds[9] != '':
            t = NMEA.hms_to_sec(ds[1])
            lat = NMEA.dm_to_sd(ds[2])
            lon = NMEA.dm_to_sd(ds[4])
            mode = int(ds[6])
            alt = float(ds[9])
            return t, lat, lon, mode, alt
        else:
            return None

    @classmethod
    def parse_RMC(cls, line):
        ds = line.strip().split(',')
        if len(ds) == 14 and (ds[0] == '$GNRMC' or ds[0] == '$GPRMC') and ds[3] != '' and ds[5] != '' and ds[7] != '':
            t = NMEA.hms_to_sec(ds[1])
            lat = NMEA.dm_to_sd(ds[3])
            lon = NMEA.dm_to_sd(ds[5])
            vel = float(ds[7])
            return t, lat, lon, vel
        else:
            return None
        

class Logger(threading.Thread):
    def __init__(self, p_rtk, logfile):
        threading.Thread.__init__(self)
        self.daemon = True
        self.kill = False
        self.p_rtk = p_rtk
        d = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        self.logfile = f'{logfile}-{d.year}-{d.month:02d}-{d.day:02d}-{d.hour:02d}-{d.minute:02d}-{d.second:02d}.nmea'
        self.t, self.lat, self.lon, self.mode, self.alt, self.vel = 0, 0, 0, 0, 0, 0

    def run(self):
        with open(self.logfile, 'w') as f:
            while not self.kill:
                line = self.p_rtk.stdout.readline()
                if line[3:6] == 'GGA':
                    r = NMEA.parse_GGA(line)
                    if r:
                        self.t, self.lat, self.lon, self.mode, self.alt = r
                elif line[3:6] == 'RMC':
                    r = NMEA.parse_RMC(line)
                    if r:
                        self.t, self.lat, self.lon, self.vel = r

                f.write(line)

class RTKController:
    base_cq = 'guest:guest@160.16.134.72:80/CQ-F9P'
    base_hosei = 'guest:guest@133.25.86.45:443/HOSEI-F9P'
    rover_to_f9p = 'ttyACM0:115200'
    rover_from_f9p = 'ttyACM0:115200'
    rover_to_mosaicx5 = 'ttyACM1:230400'
    rover_from_mosaicx5 = 'ttyACM0:230400'

    base = base_cq
    rover_to = rover_to_mosaicx5
    rover_from = rover_from_mosaicx5
    # rover_to = rover_to_f9p
    # rover_from = rover_from_f9p

    def connect_base(self,base,rover_to):
        cmd = f'exec{self.str2str} -in ntrip://{base} -out serial://{rover_to}'
        self.info(cmd + '\n')
        self.p_base = subprocess.Popen(cmd,shell=True,stderr=PIPE,text=True)
        for i in range(3):
            line = self.p_base.stderr.readline()
            if line is not None:
                self.info(line)
        self.info(f'connection established.\n')
    
    def disconnect_base(self):
        self.p_base.kill()
        self.info(f'base station disconnected.\n')
    
    def start(self):
        pass
    

