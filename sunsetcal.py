#!/usr/bin/env python3
import math
from datetime import date, datetime

# this script calculates the solar position for a given time of the year
# it can also calculate sunset and sunrise time

# source: https://www.esrl.noaa.gov/gmd/grad/solcalc/solareqns.PDF

date_object = datetime.now().timetuple()
day_of_year = date_object.tm_yday
days_in_year = 365
hour = date_object.tm_hour
mn = date_object.tm_min
sc = date_object.tm_sec
latitude = 24.792493
longitude = -107.4051
timezone = -7

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

# now it's time to calculate the true solar time, first we need to find the time offset


def timeOffset():
    return eqTime() + (4*longitude) - (60*timezone)


def trueSolarTime():
    return hour * 60 + mn + sc/60 + timeOffset()


# solar hour angle, in degrees is:
def solarHourAngle():
    return (trueSolarTime()/4)-180


# the solar zenith angle can then be found for the hour angle (ha), latitude
# and solar declination using the following eq
zenith = math.sin(latitude)*math.sin(declination) + \
    math.cos(latitude) * math.cos(declination) * math.cos(ha)


print(f'fractionalYear: {fractionalYear()}')
print(f'eqtime: {eqTime()}')
print(f'declinationAngle: {declinationAngle()}')
