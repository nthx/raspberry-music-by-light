# raspberry-music-by-light
Plays music when the sensor detects light.

It is designed with simple functionality in mind, perfect for a restroom setting XD
* Recommended to use with a dedicated Raspberry Pi
* Fire and forget
* Plays songs while skipping the first few seconds — usually nothing audible at that time anyway
* Continues playing the same song after a quick light toggle

## Hardware
* Tested with Raspberry Pi 4
* Tested with a GPIO light sensor
* Tested with any speaker connected to the analog mini jack output

## Software
* Tested and running on an older version of Debian/Raspbian:
    ```
    10.0+
    # /etc/apt/sources.list
    # deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
    ```

* Tested with an older version of Python:
    ```
    Python 2.7.16
    ```

* Requires a music player with MP3 files in its library:
    ```
    apt-get install mpc mpd

    # example of: /var/lib/mpd/music/ (extra files allowed)
    /var/lib/mpd/music/rod_s/00_never.sfv
    /var/lib/mpd/music/rod_s/01_blind.mp3
    /var/lib/mpd/music/rod_s/07_swar.mp3
    /var/lib/mpd/music/rod_s/05_angel.mp3
    ...
    ```

    Run after uploading mp3s:
    ```
    mpc update
    mpc ls
    ```
    This should list all available audio files to play

    Enable Alsa output in `/etc/mpd.conf`:
    ```
    audio_output {
        type            "alsa"
        name            "My ALSA Device"
    }
    ```


## Configuration

* Download the repository:
    ```sh
    cd /home/pi/
    sudo apt-get install python python-rpi.gpio
    git clone git@github.com:nthx/raspberry-music-by-light.git
    ```

* Populate MPD with any supported music files:
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

* Reboot:
    ```
    reboot
    ```

