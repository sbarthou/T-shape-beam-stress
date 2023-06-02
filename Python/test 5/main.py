import pandas as pd
import itertools


dicc = {
    'Ancho viga (mm)': [],
    'Altura viga (mm)': [],
    'Ancho ala (mm)': [],
    'Altura ala (mm)': [],
    'Ancho alma (mm)': [],
    'Altura alma (mm)': [],
    'Área viga (mm^2)': [],
    'Wpp (ton/m)': [],
    'Sigma C (ton/m^2)': [],
    'Sigma T (ton/m^2)': [],
    'Sigma a (ton/m^2)': [],
    'Dif C-a (ton/m^2)': []
}


def l_l(valor):
    # Transforma mm a m
    return valor/1000   # m
    
def l4(valor):
    # Transforma mm^4 a m^4
    return valor*(10**-12)

        
lista = [6, 8, 10, 12, 14, 16, 20, 22, 25, 28, 32]
dimensiones = list(itertools.product(lista, repeat=2))

ancho = 16
alto = 3810
dim1 = 10
dim2 = 6


# # entre este rango se encontraron los Wpp mas bajos
# for alto in range(3700, 3900, 1):
#     for ancho in range(7, 50, 1):
#         for dim1, dim2 in dimensiones:

# largo viga
L = 11   # m
# ancho viga
B = ancho   # mm
dicc['Ancho viga (mm)'].append(B)
# altura viga
H = alto   # mm
dicc['Altura viga (mm)'].append(H)

# ancho ala
b_ala = B   # mm
dicc['Ancho ala (mm)'].append(b_ala)
# altura ala
l = dim1   # mm
dicc['Altura ala (mm)'].append(l)
# area ala
a_ala = b_ala * l   # mm^2

# ancho alma
t = dim2   # mm
dicc['Ancho alma (mm)'].append(t)
# altura alma
h_alma = H - l   # mm
dicc['Altura alma (mm)'].append(h_alma)
# area alma
a_alma = h_alma * t   # mm^2

# area viga
A_viga = (B*l + t*(H-l))   # mm^2
dicc['Área viga (mm^2)'].append(A_viga)

# centroide ala
c_ala = H - (l/2)
# centroide alma
c_alma = h_alma/2
# centroide viga
c = ((c_ala*a_ala) + (c_alma*a_alma))/(a_ala + a_alma)   # mm

# Momento de inercia
I = (((1/12)*b_ala*(l**3)) + a_ala*((c_ala-c)**2)) + (((1/12)*t*(h_alma**3)) + a_alma*((c-c_alma)**2))   # mm^4
I = l4(I)   # m^4

# peso propio
W = 7850*(A_viga/1000**2)*0.001   # ton/m
dicc['Wpp (ton/m)'].append(W)

# reacciones
Cy = (20*3 + W*11*(11/2) + 10*2*7 + 40*11 - 10)/6
Ay = abs(80 + W*11 - Cy)

# Momento maximo
M_max= -10 -Ay*6 -W*(6**2)/2 -20*(6-3)   # ton•m

# sigma tension max
sigmaT_max = (-M_max/I)*(l_l(H-c))   # ton/m^2
dicc['Sigma T (ton/m^2)'].append(sigmaT_max)
# sigma compresion max
sigmaC_max = (-M_max/I)*(l_l(c))   # ton/m^2
dicc['Sigma C (ton/m^2)'].append(sigmaC_max)
# sigma a
sigma_a = 15180   # ton/m^2
dicc['Sigma a (ton/m^2)'].append(sigma_a)
# diferencia entre sigma compresion y sigma a
diferencia = abs(sigmaC_max - sigma_a)   # ton/m^2
dicc['Dif C-a (ton/m^2)'].append(diferencia)


df = pd.DataFrame(dicc)

""" OJO: 
Debido a que el momento flector es siempre negativo, la viga se deforma hacia arriba (cara triste), 
por lo tanto desde el centroide hacia arriba habrá tensión y hacia abajo del centroide habrá compresión. 
Debido a esto si el ancho del ala es menor que el ancho del alma (sin forma T), el sigma max de tension (arriba) será mayor que el sigma max de compresion (abajo).
"""

# # Para que la viga tenga forma de T el ancho del ala debe que ser mayor al ancho del alma. Esto hará que el sigma max de compresion sea mayor que el sigma max de tension.
# df = df[df['Ancho ala (mm)'] > df['Ancho alma (mm)']]

# # filtrar valores de sigma max (compresion) menores o iguales a sigma adm
# df = df[df['Sigma C (ton/m^2)'] <= df['Sigma a (ton/m^2)']]

# smallest = df.loc[df['Wpp (ton/m)'].nsmallest(100).index]
# smallest.to_excel('test 5/data.xlsx', index=False)

print(df)