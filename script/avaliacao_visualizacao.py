'''Esse módulo é destinado a fazer a visualização do preços de euro e dollar em relação ao real
com relação aos mandatos presidenciais que ocorreram de 1999 a 2021
@author Reyne e Diego'''

import matplotlib.style as style
import matplotlib.pyplot as plt
import pandas as pd

def see_rolling_mean(dataset):
    '''essa função faz um plot das médias móvies do dataset para valores de real para dolar'''
    plt.figure(figsize=(9,6))
    plt.subplot(3,2,1)
    plt.plot(dataset['Time'], dataset['real_dolar'])
    plt.title('Original values', weight='bold')
    for i, rolling_mean in zip([2, 3, 4, 5, 6],
                           [7, 30, 50, 100, 365]):
        plt.subplot(3,2,i)
        plt.plot(dataset['Time'],
                dataset['real_dolar'].rolling(rolling_mean).mean())
        plt.title('Rolling Window:' + str(rolling_mean), weight='bold')
    plt.tight_layout()
    plt.show()

def convert_column_to_float(dataset,name):
    '''essa função altera o valor - das colunas com "missing values"'''
    return pd.to_numeric(dataset[name].str.replace("-",'1'))

def see_dataset(dataset,value):
    '''essa função faz um plot do dataset com o eixo x sendo o tempo'''
    plt.plot(dataset['Time'], dataset[value])
    plt.show()

def set_subdataset(dataset):
    '''essa função gera um sub dataset'''
    presidents = dataset.copy(
                   )[(dataset['Time'].dt.year > 1995) & (dataset['Time'].dt.year <= 2021)]
    return presidents

### Adding the FiveThirtyEight style
def visualyze_presidents(fhc,lula,dilma_temer,bolso,moeda):
    '''Essa função faz o plot do valor do dolar e o valor do euro em relação ao real
    no decorrer dos anos'''
    style.use('fivethirtyeight')
    plt.figure(figsize=(18, 8))
    ax1 = plt.subplot(2,4,1)
    ax2 = plt.subplot(2,4,2)
    ax3 = plt.subplot(2,4,3)
    ax4 = plt.subplot(2,4,4)
    ax5 = plt.subplot(2,1,2)
    axes = [ax1, ax2, ax3, ax4, ax5]

    ### Changes to all the subplots
    for a_x in axes:
        a_x.set_ylim(0, 6)
        a_x.set_yticks([1.0, 3,5,7])
        a_x.set_yticklabels(['1.0', '3','5','7'],
                       alpha=0.3)
        a_x.grid(alpha=0.5)

    ax1.plot(fhc['Time'], fhc['rolling_mean'],
            color='#2A7E43')
    ax1.set_xticklabels(['1999','','','','2001','','','','2003'],
                       alpha=0.3)

    ax2.plot(lula['Time'], lula['rolling_mean'],
            color='#ffa500')
    ax2.set_xticklabels(['', '2004', '', '', '', '2008', '',
                         '', '', '2011'],
                       alpha=0.3)

    ### Ax3: DILMA _ TEMER
    ax3.plot(dilma_temer['Time'], dilma_temer['rolling_mean'],
            color='#00B2EE')
    ax3.set_xticklabels(['','2011', '','', '2014', '',
                         '2016', '','', '2019'],
                       alpha=0.3)

    ### Ax4: BOZO
    ax4.plot(bolso['Time'], bolso['rolling_mean'],
            color='#FFD600')
    ax4.set_xticklabels(['2019',"","","","2020","","","", '2021'],
                       alpha=0.3)

    ax5.plot(fhc['Time'], fhc['rolling_mean'],
            color='#2A7E43')
    ax5.plot(lula['Time'], lula['rolling_mean'],
            color='#ffa500')
    ax5.plot(dilma_temer['Time'], dilma_temer['rolling_mean'],
            color='#00B2EE')
    ax5.plot(bolso['Time'], bolso['rolling_mean'],
            color='#FFD600')
    ax5.grid(alpha=0.5)
    ax5.set_xticks([])
    plt.savefig('chart'+moeda+'.png', bbox_inches="tight")
def try_open_file(csv_file):
    '''Esta funcao tenta abrir um arquivo csv e retorna o True or false
    se o arquivo existir ou não respectivamente'''
    try:
        data = pd.read_csv(csv_file)
        print(data.head())
        return True
    except IOError:
        print("Arquivo não encontrado")
        return False
def convert_to_real(exchange):
    '''converte da cotacao de euro->dolar e euro->real para
    dolar->real'''
    try:
        exchange['real_dolar'] = exchange['BR_real']/exchange['US_dollar']
        return exchange
    except ZeroDivisionError:
        print("Divisão por zero")
        return None
CSV_FILE = 'euro-daily-hist_1999_2020.csv'

if try_open_file(CSV_FILE):
    exchange_rates = pd.read_csv(CSV_FILE)


exchange_rates.rename(columns={'[US dollar ]': 'US_dollar',
                               'Period\\Unit:': 'Time',
                               '[Brazilian real ]': "BR_real"},
                      inplace=True)
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True)
NAME_DOLAR = 'US_dollar'
exchange_rates['US_dollar'] = convert_column_to_float(exchange_rates,NAME_DOLAR)
NAME_REAL = 'BR_real'
exchange_rates['BR_real'] = convert_column_to_float(exchange_rates,NAME_REAL)

exchange_rates = convert_to_real(exchange_rates)

real_euro = exchange_rates[['Time', 'BR_real']].copy()
real_euro['rolling_mean'] = real_euro['BR_real'].rolling(30).mean()

dolar_real = exchange_rates[['Time','real_dolar']]
dolar_real['rolling_mean'] = dolar_real['real_dolar'].rolling(30).mean()

presidents_dolar = set_subdataset(dolar_real)
fhc_dolar = presidents_dolar.copy(
       )[presidents_dolar['Time'].dt.year < 2003]
lula_dolar = presidents_dolar.copy(
       )[(presidents_dolar['Time'].dt.year >= 2003) & (presidents_dolar['Time'].dt.year < 2011)]
dilma_temer_dolar = presidents_dolar.copy(
       )[(presidents_dolar['Time'].dt.year >= 2011) & (presidents_dolar['Time'].dt.year < 2019)]
bolso_dolar = presidents_dolar.copy(
       )[(presidents_dolar['Time'].dt.year >= 2019) & (presidents_dolar['Time'].dt.year <= 2021)]
MOEDA_DOLAR = "USD"
visualyze_presidents(fhc_dolar,lula_dolar,dilma_temer_dolar,bolso_dolar,MOEDA_DOLAR)

presidents_euro = set_subdataset(real_euro)
fhc_euro = presidents_euro.copy(
       )[presidents_euro['Time'].dt.year < 2003]
lula_euro = presidents_euro.copy(
       )[(presidents_euro['Time'].dt.year >= 2003) & (presidents_euro['Time'].dt.year < 2011)]
dilma_temer_euro = presidents_euro.copy(
       )[(presidents_euro['Time'].dt.year >= 2011) & (presidents_euro['Time'].dt.year < 2019)]
bolso_euro = presidents_euro.copy(
       )[(presidents_euro['Time'].dt.year >= 2019) & (presidents_euro['Time'].dt.year <= 2021)]
MOEDA_EURO = "EUR"
visualyze_presidents(fhc_euro,lula_euro,dilma_temer_euro,bolso_euro,MOEDA_EURO)
