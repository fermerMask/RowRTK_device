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
        cmd = f'exec {self.str2str} -in ntrip://{base} -out serial://{rover_to}'
        self.info(cmd + '\n')
        self.p_base = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        for i in range(3):
            line = self.p_base.stderr.readline()
            if line is not None:
                self.info(line)
        self.button_disconnect['state'] = 'active'
        self.info(f'connection established.\n')

    def disconnect_base(self):
        self.button_disconnect['state'] = 'disabled'
        self.p_base.kill()
        # result = proc.communicate()[0].decode("utf-8")
        self.button_connect['state'] = 'active'
        self.info(f'base station disconnected.\n')

    def start(self):
        self.button_start['state'] = 'disabled'
        logfile = self.textbox_log.get()
        rover_from = self.textbox_rover_from.get()
        self.info(f'start GNSS positioning.\n')

        port, bps = rover_from.split(':')
        cmd = f'exec cu -s {bps} -l /dev/{port}'
        self.info(cmd + '\n')
        self.p_rtk = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
        self.th_logger = Logger(self.p_rtk, logfile)
        self.th_logger.start()

        self.th_updater = threading.Thread(target=self.update_status, daemon=True)
        self.kill_update = False
        self.th_updater.start()

        self.button_stop['state'] = 'active'

    def update_textbox(self, textbox, value):
        textbox.configure(state='normal')
        textbox.delete(0, tk.END)
        textbox.insert(0, value)
        textbox.configure(state='readonly')

    def update_status(self):
        logger = self.th_logger
        while not self.kill_update:
            t, lat, lon, mode, alt, vel = logger.t, logger.lat, logger.lon, logger.mode, logger.alt, logger.vel
            self.update_textbox(self.textbox_lat, f'{lat:.8f}')
            self.update_textbox(self.textbox_lon, f'{lon:.8f}')
            self.update_textbox(self.textbox_mode, NMEA.mode_names[mode])
            self.update_textbox(self.textbox_vel, f'{vel:.3f}')
            self.update_textbox(self.textbox_alt, f'{alt:.3f}')
            if mode == 0:
                self.textbox_mode.configure(readonlybackground='#E0E0E0')
            elif mode == 1:
                self.textbox_mode.configure(readonlybackground='#F1E5CF')
            elif mode == 2:
                self.textbox_mode.configure(readonlybackground='#FAC6F6')
            elif mode == 4:
                self.textbox_mode.configure(readonlybackground='#C6FDC3')
            elif mode == 5:
                self.textbox_mode.configure(readonlybackground='#D7C2FE')
            time.sleep(0.5)

    def stop(self):
        self.button_stop['state'] = 'disabled'
        self.kill_update = True
        self.th_updater.kill = True
        self.th_updater.join()

        self.th_logger.kill = True
        self.th_logger.join()

        self.p_rtk.stdin.write('~.')
        time.sleep(1)
        self.p_rtk.kill()

        self.button_start['state'] = 'active'
        self.info(f'stop GNSS positioning.\n')