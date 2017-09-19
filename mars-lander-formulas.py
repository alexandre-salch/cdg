import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def log(iText):
    print(iText,file=sys.stderr)


surface_n = int(input())  # the number of points used to draw the surface of Mars.
_surface = [[0,0] for i in range(surface_n)]
_landingLeftIndex = 0

for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    _surface[i][0] = land_x
    _surface[i][1] = land_y

for itPointIndex in range(surface_n-1):
    if _surface[itPointIndex][1]==_surface[itPointIndex+1][1] and _surface[itPointIndex+1][0]>=_surface[itPointIndex][0]+1000:
        _landingLeftIndex = itPointIndex

_g = 3.711
_angleMaxStep = 15
_angleStep = 5

def possibleInputs(power, angle):
    aRes = []
    minPower = max(0, power-1)
    maxPower = min(5, power+2) # 5=4+1 because of range end and range step == 1
    minAngle = max(-90, angle-_angleMaxStep)
    maxAngle = min(91, angle+_angleMaxStep+1) # 91 because range should exclude any value > 90
    for itPower in range(minPower,maxPower,1):
        for itAngle in range(minAngle, maxAngle, _angleStep):
            aRes.append((itPower, itAngle))
    return aRes

def possibleNextPositionsAndSpeed(power, angle, x0, y0, vx0, vy0):
    aRes = []
    for itInput in possibleInputs(power, angle):
        aRes.append((itInput, nextPosition(itInput[0], math.radians(itInput[1]), x0, y0, vx0, vy0), nextSpeed(itInput[0], math.radians(itInput[1]), vx0, vy0)))
    return aRes


def nextPosition(power, angle, x0, y0, vx0, vy0):
    return -power*math.sin(angle)/2 + vx0 + x0, (power*math.cos(angle)-_g)/2 + vy0 + y0

def nextSpeed(power, angle, vx0, vy0):
    return -power*math.sin(angle) + vx0, (power*math.cos(angle)-_g) + vy0

_maxAngle = 30
# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]



    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    aPower = 3
    aAngle = 0
    if x<_surface[_landingLeftIndex][0]:
        aAngle = -1*_maxAngle
    elif x>_surface[_landingLeftIndex+1][0]:
        aAngle = _maxAngle
    else:
        # If you're at the vertical of the landing zone, prepare landing
        # ie Reduce horizontal speed
        if h_speed>20:
            aAngle = _maxAngle
        elif h_speed<-20:
            aAngle = -1*_maxAngle
    if h_speed>40:
        aAngle = int(1.5*_maxAngle)
    elif h_speed<-40:
        aAngle = int(-1.5*_maxAngle)
    if v_speed<-35:
        aPower=4
    if v_speed<-40:
        aAngle = 0
    if y<_surface[_landingLeftIndex][1]:
        aPower=4


    # rotate power. rotate is the desired rotation angle. power is the desired thrust power.
    print(str(aAngle)+" "+str(aPower))
