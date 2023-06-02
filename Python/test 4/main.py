import pandas as pd
import itertools


dicc = {
    'Ancho viga (mm)': [],
    'Altura viga (mm)': [],
    'Ancho ala (mm)': [],
    'Altura ala (mm)': [],
    'Ancho alma (mm)': [],
    'Altura alma (mm)': [],
    'Área viga (m^2)': [],
    'Wpp (ton/m)': [],
    'Sigma C (ton/m^2)': [],
    'Sigma T (ton/m^2)': [],
    'Sigma a (ton/m^2)': [],
    'Dif T-a (ton/m^2)': []
}


def l_l(valor):
    # Transforma mm a m
    return valor/1000   # m

def m_l(valor):
    # Transforma kg/m a ton/m
    return valor/1000   # ton/m
    
def l4(valor):
    # Transforma mm^4 a m^4
    return valor*(10**-12)

        
lista = [6, 8, 10, 12, 14, 16, 20, 22, 25, 28, 32]
dimensiones = list(itertools.product(lista, repeat=2))


# # datos que dieron el menor valor para Wpp y menor diferencia entre sigma tension y sigma a
# ancho = 13
# alto = 3800

# dim1 = 
# dim2 = 


for alto in range(3000, 4000, 1):
    for ancho in range(1, 50, 1):
        for dim1, dim2 in dimensiones:
            # largo viga
            L = 11   # m
            # ancho viga
            B = ancho   # mm
            B_m = l_l(B)
            dicc['Ancho viga (mm)'].append(B)
            # altura viga
            H = alto   # mm
            H_m = l_l(H)
            dicc['Altura viga (mm)'].append(H)

            # ancho ala
            b_ala = B   # mm
            b_ala_m = l_l(b_ala)   # m
            dicc['Ancho ala (mm)'].append(b_ala)
            # altura ala
            l = dim1   # mm
            l_m = l_l(l)   # m
            dicc['Altura ala (mm)'].append(l)
            # area ala
            a_ala = b_ala * l   # mm^2

            # ancho alma
            t = dim2   # mm
            t_m = l_l(t)   # m
            dicc['Ancho alma (mm)'].append(t)
            # altura alma
            h_alma = H - l   # mm
            h_alma_m = l_l(h_alma)   # m
            dicc['Altura alma (mm)'].append(h_alma)
            # area alma
            a_alma = h_alma * t

            # area viga
            A_viga = (b_ala_m*l_m) + (h_alma_m*t_m)   # m^2
            dicc['Área viga (m^2)'].append(A_viga)

            # centroide ala
            c_ala = H - (l/2)
            # centroide alma
            c_alma = h_alma/2
            # centroide viga
            c = ((c_ala*a_ala) + (c_alma*a_alma))/(a_ala + a_alma)   # mm

            # Momento de inercia
            I = (((1/12)*b_ala*(l**3)) + a_ala*((c_ala-c)**2)) + (((1/12)*t*(h_alma**3)) + a_alma*((c-c_alma)**2))   # mm^4
            I = l4(I)   # m^4

            # gamma steel
            A36_gamma = 7850   # kg/m^3
            # peso propio
            w_pp = A36_gamma * A_viga   # kg/m
            w_pp = m_l(w_pp)   # ton/m
            dicc['Wpp (ton/m)'].append(w_pp)

            # Momento maximo
            M_max = 220   # ton/m

            # sigma compresion max
            sigmaC_max = (M_max/I)*(l_l(H-c))   # ton/m^2
            dicc['Sigma C (ton/m^2)'].append(sigmaC_max)
            # sigma tension max
            sigmaT_max = (M_max/I)*(l_l(c))   # ton/m^2
            dicc['Sigma T (ton/m^2)'].append(sigmaT_max)
            # sigma a
            sigma_a = 15180   # ton/m^2
            dicc['Sigma a (ton/m^2)'].append(sigma_a)
            # diferencia entre sigma tension y sigma a
            diferencia = abs(sigmaT_max - sigma_a)   # ton/m^2
            dicc['Dif T-a (ton/m^2)'].append(diferencia)


df = pd.DataFrame(dicc)

# filtrar valores de sigma max (tension) menores o iguales a sigma adm
df = df[df['Sigma T (ton/m^2)'] <= df['Sigma a (ton/m^2)']]

# df.to_excel('data7.xlsx', index=False)

# guardar datos con Wpp mas pequelos
smallest = df.loc[df['Wpp (ton/m)'].nsmallest(500).index]
smallest.to_excel('test 4/data.xlsx', index=False)