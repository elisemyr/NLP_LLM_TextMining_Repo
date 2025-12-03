import matplotlib as plt
import numpy as np
import math
from exercice1 import f2, f3, f1
xmin, xmax, nx = -4, 4, 41
ymin, ymax, ny = -4, 4, 41
# Discretization of the plotting domain
x1d = np.linspace(xmin,xmax,nx)
y1d = np.linspace(ymin,ymax,ny)
x2d, y2d = np.meshgrid(x1d, y1d)

# Plot contour lines (isovalues) of f1
nIso = 21
plt.contour(x2d,y2d,f2(x2d,y2d),nIso)
plt.title('Contour Lines')
plt.xlabel('x values')
plt.ylabel('y values')
plt.grid()
plt.axis('square')


# Definition of the plotting domain
xmin, xmax, nx = -4, 4, 41
ymin, ymax, ny = -4, 4, 41
# Discretization of the plotting domain
x1d = np.linspace(xmin,xmax,nx)
y1d = np.linspace(ymin,ymax,ny)
x2d, y2d = np.meshgrid(x1d, y1d)

# Plot contour lines (isovalues) of f1
nIso = 21
plt.contour(x2d,y2d,f3(x2d,y2d),nIso)
plt.title('Contour Lines')
plt.xlabel('x values')
plt.ylabel('y values')
plt.grid()
plt.axis('square')

# Create array of x samples
xmin, xmax, nx = -4, 4, 41
tab_x = np.linspace(xmin,xmax,nx)
# Calculate values of f(x,y) for x values in tab_x and different y values
tab_zm2 = f1(tab_x,-2)
tab_z0 = f1(tab_x,0)
tab_zp2 = f1(tab_x,2)
# Plot the graph
plt.plot(tab_x, tab_zm2,'k-',label='y = -2')
plt.plot(tab_x, tab_z0,'r-',label='y = 0')
plt.plot(tab_x, tab_zp2,'b-',label='y = +2')
plt.xlabel('x values')
plt.ylabel('f1(x,y=constant) values')
plt.legend()
plt.grid()

# Create array of y samples
ymin, ymax, ny = -4, 4, 41
tab_y = np.linspace(ymin,ymax,ny)
# Calculate values of f(x,y) for y values in tab_y and different x values
tab_zm2 = f1(-2,tab_y)
tab_z0 = f1(0,tab_y)
tab_zp2 = f1(2,tab_y)
# Plot the graph
plt.plot(tab_y, tab_zm2,'k-',label='x = -2')
plt.plot(tab_y, tab_z0,'r-',label='x = 0')
plt.plot(tab_y, tab_zp2,'b-',label='x = +2')
plt.xlabel('y values')
plt.ylabel('f1(x=constant,y) values')
plt.legend()
plt.grid()

# Create array of x samples
xmin, xmax, nx = -4, 4, 41
tab_x = np.linspace(xmin,xmax,nx)
# Calculate values of f(x,y) for x values in tab_x and different y values
tab_zm2 = f1(tab_x,tab_x*(1/math.sqrt(3)))
tab_z0 = f1(tab_x,tab_x)
tab_zp2 = f1(tab_x,tab_x*math.sqrt(3))
# Plot the graph
plt.plot(tab_x, tab_zm2,'k-',label='alpha =1/√3')
plt.plot(tab_x, tab_z0,'r-',label='alpha =1')
plt.plot(tab_x, tab_zp2,'b-',label='alpha = √3')
plt.xlabel('x values')
plt.ylabel('f1(x,y) values')
plt.legend()
plt.grid()



