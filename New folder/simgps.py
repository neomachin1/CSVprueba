from datetime import datetime
from pprint import pprint
from nmeasim.models import TZ_LOCAL
from nmeasim.simulator import Simulator
from time import sleep
print()
sim = Simulator()
with sim.lock:
    # Can re-order or drop some
    sim.gps.output = ('RMC',)
    sim.gps.num_sats = 14
    sim.gps.lat = 12.3456
    sim.gps.lon = 123.4567
    sim.gps.altitude = -13
    sim.gps.geoid_sep = -45.3
    sim.gps.mag_var = -1.1
    sim.gps.kph = 60.0
    sim.gps.heading = 90.0
    sim.gps.mag_heading = 90.1
    sim.gps.date_time = datetime.now(TZ_LOCAL)  # PC current time, local time zone
    sim.gps.hdop = 3.1
    sim.gps.vdop = 5.0
    sim.gps.pdop = (sim.gps.hdop ** 2 + sim.gps.vdop ** 2) ** 0.5
    # Precision decimal points for various measurements
    sim.gps.horizontal_dp = 4
    sim.gps.vertical_dp = 1
    sim.gps.speed_dp = 1
    sim.gps.time_dp = 2
    sim.gps.angle_dp = 1
    # Keep straight course for simulator - don't randomly change the heading
    sim.heading_variation = 0
pprint(list(sim.get_output(1)))
sleep(1)
pprint(list(sim.get_output(1)))
sleep(1)
pprint(list(sim.get_output(1)))
sleep(1)
pprint(list(sim.get_output(1)))
sleep(1)