# -*- coding:utf-8 -*-

"""
地理信息库
"""
import math

PI = 3.1415926535897932
radian2degree = 180 / PI
degree2radian = PI / 180.0
NM2KM = 1.852  # 海里转千米

# WGS84 坐标系参数：
flattening = 1 / 298.257223563  # 扁率
EARTH_RADIUS_LONG = 6378137.0   # 地球长半轴 单位：米
EARTH_RADIUS_SHORT = EARTH_RADIUS_LONG - EARTH_RADIUS_LONG*flattening
# 6356752.3142451793
e_pow2 = 1 - (1 - flattening)*(1 - flattening) # 第一偏心率平方
EARTH_RADIUS = 6371137  # 地球平均半径



def get_geopoint_from_distance(geo_point, azimuth, distance_m):
    """
    从地球海拔水平上，选一角度出发一定距离后，获取新的点. 距离越远，精度越差
    :param geo_point: tuple, (float, float), (纬度, 经度)
    :param azimuth: float, 角度，0-360， 正北为0， 顺时针旋转360度
    :param distance_m: float, 距离，单位：m
    :return: tuple, (lat, lon)
    """
    lat = geo_point[0]
    lon = geo_point[1]
    a = EARTH_RADIUS_LONG
    b = EARTH_RADIUS_SHORT
    alpha1 = azimuth * PI / 180
    sinAlpha1 = math.sin(alpha1)
    cosAlpha1 = math.cos(alpha1)

    tanU1 = (1 - flattening) * math.tan(lat*PI/180)
    cosU1 = 1 / math.sqrt((1 + tanU1*tanU1))
    sinU1 = tanU1 * cosU1
    sigma1 = math.atan2(tanU1, cosAlpha1)
    sinAlpha = cosU1 * sinAlpha1
    cosSqAlpha = 1 - sinAlpha * sinAlpha
    uSq = cosSqAlpha * (a*a - b*b) / (b*b)
    A = 1 + uSq/16384*(4096 + uSq*(-768 + uSq*(320 - 175*uSq)))
    B = uSq/1024*(256 + uSq*(-128 + uSq*(74 - 47*uSq)))

    sigma = distance_m / (b * A)
    sigmaP = 2 * PI
    sinSigma = 0
    cosSigma = 0
    for i in range(8):
        if math.fabs(sigma - sigmaP) < 1e-12:
            break
        cos2SigmaM = math.cos(2*sigma1 + sigma)
        sinSigma = math.sin(sigma)
        cosSigma = math.cos(sigma)
        deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma*(-1 + 2*cos2SigmaM*cos2SigmaM)
                                                                        - B/6*cos2SigmaM*(-3 + 4 * sinSigma*sinSigma) * (-3 + 4*cos2SigmaM*cos2SigmaM)))
        sigmaP = sigma
        sigma = distance_m / (b*A) + deltaSigma

    tmp = sinU1*sinSigma - cosU1*cosSigma*cosAlpha1
    lat2 = math.atan2(sinU1*cosSigma + cosU1*sinSigma*cosAlpha1,
                      (1 - flattening) * math.sqrt(sinAlpha*sinAlpha + tmp*tmp))
    lon_span = math.atan2(sinSigma*sinAlpha1, cosU1*cosSigma - sinU1*sinSigma*cosAlpha1)
    C = flattening / 16 * cosSqAlpha*(4 + flattening*(4 - 3*cosSqAlpha))
    lon_diff = lon_span - (1 - C)*flattening*sinAlpha*(sigma + C*sinSigma*(cos2SigmaM + C*cosSigma*(-1 + 2*cos2SigmaM*cos2SigmaM)))
    return lat2*180/PI, lon+lon_diff*180/PI


