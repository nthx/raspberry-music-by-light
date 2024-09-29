# 
# Plays music when light sensor finds light
# Uses MPD music player
#
# To prevent starting by launcher: 
#    touch DO_NOT_START

import RPi.GPIO as GPIO
import time
import datetime
import os
import signal
import sys
import random
import os.path

# GPIO SETUP: DATA PIN: 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

config_delay_to_start_after_light_on = 1 # seconds
config_when_to_stop_after_light_off = 0.1 # seconds
config_volume_day = '60'
config_volume_night = '45'
config_day_start = datetime.time(hour=7, minute=0)
config_night_start = datetime.time(hour=21, minute=00)
config_wait_to_next_song_after_playing_current = 600

config_seek_min_start = 0
config_seek_min_end = 3
config_seek_sec_start = 0
config_seek_sec_end = 59


def main():
    signal.signal(signal.SIGINT, signal_handler)

    # Configure MPD
    execute('/usr/bin/mpc repeat on')
    execute('/usr/bin/mpc random on')
    execute('/usr/bin/mpc clear')
    execute('/usr/bin/mpc ls | /usr/bin/mpc add')
    print
    print '*' * 50
    print execute('/usr/bin/mpc playlist')
    print '*' * 50

    light_on = False
    light_on_time = 0
    light_off_time = 0
    last_played_time = 0

    when_last_on = datetime.datetime.now() - datetime.timedelta(seconds=10)
    when_last_off = datetime.datetime.now() - datetime.timedelta(seconds=10)
    when_last_played = datetime.datetime.now() - datetime.timedelta(seconds=9999) # long time ago

    on_command_needed = True
    off_command_needed = True

    while True:
        try:
            sys.stdout.flush()
            exit_if_magic_file_found()

            light_on = True if GPIO.input(4) == 0 else False

            if light_on:
                when_last_on = datetime.datetime.now()
                off_command_needed = True
            else:
                when_last_off = datetime.datetime.now()
                on_command_needed = True

            light_off_time = (datetime.datetime.now() - when_last_on).seconds
            light_on_time = (datetime.datetime.now() - when_last_off).seconds
            last_played_time = (datetime.datetime.now() - when_last_played).seconds

            # START
            if light_on_time >= config_when_to_stop_after_light_off:
                if on_command_needed:

                    # lets restart and shuffle if nobody here for X mins LOL XD
                    if last_played_time > config_wait_to_next_song_after_playing_current:
                        execute('/usr/bin/mpc shuffle')
                        execute('/usr/bin/mpc volume 0')
                        execute('/usr/bin/mpc play')
                        execute('/usr/bin/mpc next')
                        random_start_minute, random_start_second = normal_song_start()
                        execute('/usr/bin/mpc seek 00:' + random_start_minute + ':' + random_start_second)
                    else:
                        execute('/usr/bin/mpc play')


                    execute('/usr/bin/mpc volume %s' % get_volume())

                    when_last_played = datetime.datetime.now()
                    on_command_needed = False

            # STOP
            if light_off_time >= config_when_to_stop_after_light_off:
                if off_command_needed:
                    execute('/usr/bin/mpc pause-if-playing')
                    off_command_needed = False
            

            log("Command: on: %s off: %s" % (on_command_needed, off_command_needed))
            log("Light: %s on for: %s off for: %s" % (light_on, light_on_time, light_off_time))
            time.sleep(1)
        except Exception as ex:
            log("error in main loop: %s" % ex)


# end of main
# ----------------------------------------------------
# Helper functions:

# Clean exit support
def signal_handler(sig, frame):
    log('You pressed Ctrl+C or magic DO_NOT_START file found!')
    execute('/usr/bin/mpc pause-if-playing')
    sys.exit(0)

def exit_if_magic_file_found():
    if os.path.isfile('DO_NOT_START'):
        signal_handler('', '')

def execute(cmd):
    try:
        log(cmd)
        return os.system(cmd)
    except Exception as ex:
        log("error on: %s from: %s" % (cmd, ex))
    
def normal_song_start():
    return ('00', '05')

# TODO: make better songs that start quicker
def random_start():
    # TODO: some fun, but only for this specific song
    random_start_minute = str(random.randint(config_seek_min_start, config_seek_min_end)).rjust(2, '0')
    random_start_second = str(random.randint(config_seek_sec_start, config_seek_sec_end)).rjust(2, '0')
    if random_start_minute == '00':
        random_start_second = '25'
    return (random_start_minute, random_start_second)

def get_volume():
    now = datetime.datetime.now()
    if now.time() >= config_day_start and now.time() <= config_night_start:
        return config_volume_day
    else:
        return config_volume_night

def log(msg):
    print "%s: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg)

main()
