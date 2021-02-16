#!/usr/bin/env python3
import math

# this script calculates the solar position for a given time of the year
# it can also calculate sunset and sunrise time

# source: https://www.esrl.noaa.gov/gmd/grad/solcalc/solareqns.PDF

dayOfTheYear = 45  # equals february 15
hour = 20
mn = 24
sc = 00
latitude = 24.792493
longitude = -107.4051
timezone = -7

# first we need to calculate the fractional year, this returns a result in radians
# for leap years use 366 instead of 365
fractionalYear = ((2*math.pi)/365)*((dayOfTheYear - 1) + ((hour-12) / 24))

# from the fractional year we can estimate the equation of time (in minutes)
# and the solar declination angle (in radians).

eqtime = 229.18 * (0.000075 +
                   0.001868 * math.cos(fractionalYear) -
                   0.032077 * math.sin(fractionalYear) -
                   0.014615 * math.cos(2*fractionalYear) -
                   0.040849 * math.sin(2*fractionalYear))

declination = math.radians(0.006918 - 0.399912 * math.cos(fractionalYear) +
                           0.070257 * math.sin(fractionalYear) -
                           0.006758 * math.cos(2*fractionalYear) +
                           0.000907 * math.sin(2*fractionalYear) -
                           0.002697 * math.cos(3*fractionalYear) +
                           0.00148 * math.sin(3*fractionalYear))

# now it's time to calculate the true solar time, first we need to find the time offset
time_offset = eqtime + (4*longitude) - (60*timezone)

tst = hour * 60 + mn + sc/60 + time_offset

# solar hour angle, in degrees is:
ha = (tst/4)-180

# the solar zenith angle can then be found for the hour angle (ha), latitude
# and solar declination using the following eq
zenith = math.sin(latitude)*math.sin(declination) + \
    math.cos(latitude) * math.cos(declination) * math.cos(ha)

# and now the solar azimuth, degrees clowise from north is found from
solar_azimuth = -((math.sin(latitude)*math.cos(zenith)-math.sin(declination)) /
                  (math.cos(latitude)*math.sin(zenith)))

print(f'fractionalYear: {fractionalYear}')
print(f'eqtime: {eqtime}')
print(f'declination: {declination}')
print(f'time_offset: {time_offset}')
print(f'tst: {tst}')
print(f'ha: {ha}')
print(f'solar_azimuth: {solar_azimuth}')
