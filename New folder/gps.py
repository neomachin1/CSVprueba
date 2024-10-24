from datetime import datetime, timedelta, timezone
from nmeasim.models import GpsReceiver
gps = GpsReceiver(
    date_time=datetime(2020, 1, 1, 12, 34, 56, tzinfo=timezone.utc),
    output=('RMC',)
)
for i in range(3):
    gps.date_time += timedelta(seconds=1)
    print(gps.get_output())
print()
print()

from datetime import datetime
from pprint import pprint
from nmeasim.models import TZ_LOCAL
from nmeasim.simulator import Simulator
sim = Simulator()

with sim.lock:
    # Can re-order or drop some
    sim.gps.output = ('RMC', )
    sim.gps.num_sats = 14
    sim.gps.lat = 12.56
    sim.gps.lon = 30.12
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

print()
print()

import sys
from nmeasim.simulator import Simulator
sim = Simulator()
sim.generate(3, output=sys.stdout)