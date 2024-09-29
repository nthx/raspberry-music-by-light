# raspberry-music-by-light
Plays music when light sensor detects light.

## Hardware
* Tested with Raspberry 4
* Tested with GPIO light sensor
* Tested with any speaker connected to analog mini jack output.

## Software
* Tested and run with fairly old Debian/Raspbian
```
10.0
# /etc/apt/sources.list
# deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
```

* Tested with fairly old Python:

```
Python 2.7.16
```

* Needs music player with MP3 files in its library
```
apt-get install mpd

# /var/lib/mpd/music/
```

## Configuration

* download the repository
```sh
cd /home/pi/
git clone git@github.com:nthx/raspberry-music-by-light.git
```

* Populate MPD with any supported music files
```sh
cp *.mp3 /var/lib/mpd/music/
```

* Configure Crontab to run the script at OS startup:
```
crontab -e
```

```
# crontab
@reboot cd /home/pi/rpi-music-by-light/; sh rpi-music-by-light.sh | tee log/log.log 2>&1
```

* reboot
```
reboot
```
