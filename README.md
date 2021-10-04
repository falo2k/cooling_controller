# cooling_controller
Scripts for controlling a 5V PWM driven fan from my Voron 2.4 Klipper host via a logic level converter.  I use this to keep my always-on Pi cool as it was starting to get a bit toasty inside the enclosure (I might have bad airflow in there).

I am using this with a NF-A6x25 PWM in one of the skirt fan spaces, with the 5V meanwell PSU next to it and the Raspberry Pi in a Pibow Coupe case + Heatsink the other side of that.  In this setup my Pi has settled out at around 51 degrees while the printer is off, with a ~30% fan speed.  It's nice and quiet.

The fan is powered via a direct connection to the 5V PSU, and then a bog standard bidirectional [logic level converter](https://www.amazon.co.uk/gp/product/B07RDHR315) is used to shift the PWM/RPM signals between 3.3v (Pi) and 5V (Noctua).

Example service file provided to get systemd to run this script when checked out in the home directory.
