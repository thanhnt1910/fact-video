# Tọa độ thế giới (1920x1080) trên map21.png, cùng công thức với mapink21.py
import math
LON0,LAT1,S=100.0,25.0,300;KX=S*math.cos(math.radians(23))
x0=(100.5-LON0)*KX;x1=(119.0-LON0)*KX;w=x1-x0;h=w*9/16;yc=(LAT1-19.2)*S;y0=yc-h/2
sc=2880/w
def xy(lon,lat): X=(lon-LON0)*KX;Y=(LAT1-lat)*S;return (X-x0)*sc/1.5,(Y-y0)*sc/1.5
