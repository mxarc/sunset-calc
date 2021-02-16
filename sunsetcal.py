#!/usr/bin/env python3
# @author <Alfonso Reyes @mxarc>

import math
from datetime import date, datetime

# this script calculates the solar position for a given time of the year
# it can also calculate sunset and sunrise time

# source: https://www.esrl.noaa.gov/gmd/grad/solcalc/solareqns.PDF

date_object = datetime.now().timetuple()
day_of_year = 47
days_in_year = 365
hour = date_object.tm_hour
mn = date_object.tm_min
sc = date_object.tm_sec
latitude = 24.792493
longitude = -107.4051

# first we need to calculate the fractional year, this returns a result in radians
# for leap years use 366 instead of 365


def fractionalYear():
    return (2 * math.pi / days_in_year) * \
        (day_of_year - 1 + ((hour - 12) / 24))

# from the fractional year we can estimate the equation of time (in minutes)
# and the solar declination angle (in radians).


def eqTime():
    y = fractionalYear()
    a = 0.001868 * math.cos(y)
    b = 0.032077 * math.sin(y)
    c = 0.014615 * math.cos(2 * y)
    d = 0.040849 * math.sin(2 * y)
    return 229.18 * (0.000075 + a - b - c - d)


def declinationAngle():
    y = fractionalYear()
    a = 0.399912 * math.cos(y)
    b = 0.070257 * math.sin(y)
    c = 0.006758 * math.cos(2 * y)
    d = 0.000907 * math.sin(2 * y)
    e = 0.002697 * math.cos(3 * y)
    f = 0.00148 * math.sin(3 * y)
    return 0.006918 - a + b - c + d - e + f


# note: we won't be using these as they don't return standard date objects and
# they won't be needed for sunset calculation
# now it's time to calculate the true solar time, first we need to find the time offset
# def timeOffset():
#    return eqTime() + (4*longitude) - (60*timezone)
#
# def trueSolarTime():
#    return hour * 60 + mn + sc/60 + timeOffset()
# the solar zenith angle can then be found for the hour angle (ha), latitude
# and solar declination using the following equation
#ha = (trueSolarTime() / 4)-180
# def zenith():
#    global latitude
#    a = math.sin(latitude)
#    b = math.sin(declinationAngle())
#    c = math.cos(latitude)
#    d = math.cos(declinationAngle())
#    e = math.cos(ha())
#    return (a*b)+(c*d*e)

"""
Sunrise, sunset calculations
"""
# For the special case of sunrise or sunset, the zenith is set to 90.833°
# (the approximate correction for atmospheric refraction at sunrise and sunset,
# and the size of the solar disk), and the hour angle becomes


def hourAngle():
    global latitude, longitude
    # convert degrees to radians since math lib works that way
    zenith = 90.833 * (math.pi / 180)
    latitudeR = latitude * (math.pi / 180)
    a = math.cos(zenith) / (math.cos(latitudeR) * math.cos(declinationAngle()))
    b = math.tan(latitudeR) * math.tan(declinationAngle())
    return -1 * abs(math.acos(a-b))


# now for the UTC time is
sunsetUTC = 720 - 4 * (longitude + hourAngle()) - eqTime()

# Create time as a string
time_string = '{:02d}:{:02d}'.format(*divmod(int(sunsetUTC), 60))

print(f'fractionalYear: {fractionalYear()}')
print(f'eqtime: {eqTime()}')
print(f'declinationAngle: {declinationAngle()}')
print(f'time_string: {time_string}')
