import matplotlib.pyplot as plt
import numpy as np
from exercice1 import f1, f2
# Definition of the plotting domain
xmin, xmax, nx = -4, 4, 41
ymin, ymax, ny = -4, 4, 41
# Discretization of the plotting domain
x1d = np.linspace(xmin,xmax,nx)
y1d = np.linspace(ymin,ymax,ny)
x2d, y2d = np.meshgrid(x1d, y1d)

# Plot contour lines (isovalues) of f1
nIso = 21
plt.contour(x2d,y2d,f1(x2d,y2d),nIso)
plt.title('Contour Lines')
plt.xlabel('x values')
plt.ylabel('y values')
plt.grid()
plt.axis('square')

#3.2 On the contour line representation of $f_1$, locate the critical points calculated in exercise 1. It will likely be necessary to adjust the contour plot parameters.

xmin, xmax, nx = -3, 3, 201
ymin, ymax, ny = -3, 3, 201

x1d = np.linspace(xmin, xmax, nx)
y1d =np.linspace(ymin, ymax, ny)
x2d, y2d =np.meshgrid(x1d, y1d)

Z = f1(x2d,y2d)

nIso = 20
plt.figure(figsize=(8, 8))
cs = plt.contour(x2d,y2d,Z,nIso)
plt.clabel(cs, inline=True, fontsize=8)

crit_x = [1,1,-1,-1]
crit_y = [2,-2,2,-2]

plt.scatter(crit_x, crit_y, c='blue', s=60, marker='o', label='Critical points')

#3.3

def df1(x,y):
    #Partial derivative with respect to x
    df_dx = (3*x)**2 -3
    df_dy= (3*y)**2 -12
    return [df_dx,df_dy]

#for the gradient 

critical_points=[(1,2),(1,-2),(-1,2),(-1,-2)]
for (x,y) in critical_points:
    print('The gradient of f1 is ', df1(x,y))

#3.4

def d2f1(x,y):
    d2f_dxdx = 6*x
    d2f_dxdy=0
    d2f_dydy=6*y

    return [[d2f_dxdx,d2f_dxdy ],[d2f_dxdy,d2f_dydy]]


matrice = [[1,2],[3,4]]
valProp = np.linalg.eigvals(matrice)
print('Eigenvalues of the matrix {} :'.format(matrice))
print('  vp1 = {}'.format(valProp[0]))
print('  vp2 = {}'.format(valProp[1]))

# Calculate the Hessian matrix
matrice1 = d2f1 (-1,-2)
# Calculate the eigenvalues of the Hessian matrix, then test their sign
valProp = np.linalg.eigvals(matrice1)
print('Eigenvalues of the matrix {} :'.format(matrice1))
print('  vp1 = {}'.format(valProp[0]))
print('  vp2 = {}'.format(valProp[1]))


for (x, y) in critical_points:
    H =d2f1(x, y)
    eigvals = np.linalg.eigvals(H)
    print(f"Point ({x},{y})")
    print("Hessian =", H)
    print("Eigenvalues =", eigvals, "\n")


#3.5 

xmin, xmax, nx = -3, 4, 201
ymin, ymax, ny = -3, 4, 201

x1d = np.linspace(xmin, xmax, nx)
y1d = np.linspace(ymin, ymax, ny)
x2d, y2d = np.meshgrid(x1d, y1d)

Z = f2(x2d, y2d)


nIso = 20  # number of contour lines
plt.figure(figsize=(6, 5))
cs = plt.contour(x2d, y2d, Z, nIso)
plt.clabel(cs, inline=True, fontsize=8)

#Critical points of f2 
crit_x = [0,2]
crit_y = [0,1]
plt.scatter(crit_x, crit_y, c='red', s=60, marker='o', label='Critical points')

def df2(x, y):
    # Partial derivatives of f2
    df_dx = 3*x**2 - 12*y         
    df_dy = -12*x + 24*y**2      
    return [df_dx, df_dy]

crit_points_f2 = [(0, 0), (2, 1)]

for (x, y) in crit_points_f2:
    grad = df2(x, y)
    print(f"Gradient of f2 at ({x}, {y}) =", grad)

def d2f2(x, y):
    d2f_dxdx = 6 * x      # f_xx
    d2f_dxdy = -12        # f_xy = f_yx
    d2f_dydy = 48 * y     # f_yy
    return [[d2f_dxdx, d2f_dxdy],
            [d2f_dxdy, d2f_dydy]]

crit_points_f2 = [(0, 0), (2, 1)]

for (x, y) in crit_points_f2:
    H = d2f2(x, y)
    eigvals = np.linalg.eigvals(H)
    print(f"Point ({x}, {y})")
    print("  Hessian =", H)
    print("  eigenvalues =", eigvals)

