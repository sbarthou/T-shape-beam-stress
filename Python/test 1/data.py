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
    'Wpp viga (ton/m)': [],
    'Sigma max (ton/m^2)': [],
    'Sigma adm (ton/m^2)': []
}


def l_l(valor, medida1, medida2):
    # Transforma mm a m
    if medida1 == 'mm' and medida2 == 'm':
        return valor/1000   # m

def m_l(valor, medida1, medida2):
    # Transforma kg/m a ton/m
    if medida1 == 'kg' and medida2 == 'ton':
        return valor/1000   # ton/m
    
def l4(valor, medida1, medida2):
    # Transforma mm^4 a m^4
    if medida1 == 'mm' and medida2 == 'm':
        return valor*(10**-12)

        
lista = [6, 8, 10, 12, 14, 16, 20, 22, 25, 28, 32]
dimensiones = list(itertools.product(lista, repeat=2))    


for dim1, dim2 in dimensiones:
    # largo viga
    L = 10   # m
    # ancho viga
    b_viga = 500   # mm
    b_viga_m = l_l(b_viga, 'mm', 'm')
    dicc['Ancho viga (mm)'].append(b_viga)
    # altura viga
    h_viga = 1000   # mm
    h_viga_m = l_l(h_viga, 'mm', 'm')
    dicc['Altura viga (mm)'].append(h_viga)

    # ancho ala
    b_ala = 500   # mm
    b_ala_m = l_l(b_ala, 'mm', 'm')   # m
    dicc['Ancho ala (mm)'].append(b_ala)
    # altura ala
    h_ala = dim1   # mm
    h_ala_m = l_l(h_ala, 'mm', 'm')   # m
    dicc['Altura ala (mm)'].append(h_ala)
    # ancho alma
    b_alma = dim2   # mm
    b_alma_m = l_l(b_alma, 'mm', 'm')   # m
    dicc['Ancho alma (mm)'].append(b_alma)
    # altura alma
    h_alma = h_viga - 2*h_ala   # mm
    h_alma_m = l_l(h_alma, 'mm', 'm')   # m
    dicc['Altura alma (mm)'].append(h_alma)

    # area viga
    A_viga = (b_ala_m * h_ala_m) * 2 + h_alma_m * b_alma_m   # m^2
    dicc['Área viga (m^2)'].append(A_viga)

    # gamma steel
    A36_gamma = 7850   # kg/m^3
    # peso propio
    w_pp = A36_gamma * A_viga   # kg/m
    w_pp = m_l(w_pp, 'kg', 'ton')   # ton/m
    dicc['Wpp viga (ton/m)'].append(w_pp)
    # carga sobre viga
    P = 50   # ton

    # Momento maximo
    M_max = (w_pp*(L**2))/8 + (P*L)/4   # ton/m

    # Momento de inercia
    I_z = ((1/12)*b_viga*(h_viga**3)) - 2*((1/12)*((b_viga-b_alma)/2)*(h_alma**3))   # mm^4
    I_z = l4(I_z, 'mm', 'm')   # m^4

    # sigma max
    sigma_max = (M_max/I_z)*(h_viga_m/2)   # ton/m^2
    dicc['Sigma max (ton/m^2)'].append(sigma_max)
    # sigma y
    sigma_y = 2530   # kg/cm^2
    # sigma a
    sigma_a = 0.6 * sigma_y   # kg/cm^2
    sigma_a = sigma_a*10   # ton/m^2
    dicc['Sigma adm (ton/m^2)'].append(sigma_a)


df = pd.DataFrame(dicc)
df.to_excel('test 1/data.xlsx', index=False)