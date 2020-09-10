"""

Using Data From National Grid UK:
    https://carbonintensity.org.uk/
    https://carbon-intensity.github.io/api-definitions/#region-list

How I would improve this project:
    1. Performance: Use Numpy package to extract data more efficiently (if possible)
    2. User Interface: Create user input that lets user choose which energy source(s) to analyse and adjusts graphs accordingly
    3. Data Visualization:
        a. Major and minor ticks on the xaxis that avoid repetition, displaying only significant changes in time and adjusting depending on time range
        b. Allow event handling and picking to easily take values from the graphs

NOTE: All Regional Carbon Intensity Values are Forecasts. The Regional Data API is in Beta.
"""
from astropy.table import Table
import astropy.units as u
import numpy as np
import requests
import statistics
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt

while True:
    frm = input('Start date (YYYY-MM-DDThh:mmZ): ')
    to = input('End date (YYYY-MM-DDThh:mmZ): ')
    postcode = input('Postcode: ')

    nat_data = 'https://api.carbonintensity.org.uk/intensity/{}/{}'.format(frm,to)
    nat_gen = 'https://api.carbonintensity.org.uk/generation/{}/{}'.format(frm,to)
    reg_data = 'https://api.carbonintensity.org.uk/regional/intensity/{}/{}/postcode/{}'.format(frm,to,postcode)

    nat_data_r = requests.get(nat_data).json()
    nat_gen_r = requests.get(nat_gen).json()
    reg_data_r = requests.get(reg_data).json()

    def natread(number,carbon = None):
        nat_length = len(nat_gen_r['data'])
        if carbon == 'carbon':
            list = [nat_data_r['data'][n]['intensity']['actual'] for n in range(nat_length)]
        else:
            list = [nat_gen_r['data'][n]['generationmix'][number]['perc'] for n in range(nat_length)]
        return list

    def regread(number,carbon = None):
        reg_length = len(reg_data_r['data']['data'])
        if carbon == 'carbon':
            list = [reg_data_r['data']['data'][n]['intensity']['forecast'] for n in range(reg_length)]
        else:
            list = [reg_data_r['data']['data'][n]['generationmix'][number]['perc'] for n in range(reg_length)]
        return list

    nat_CO2 =       natread(None,'carbon')
    nat_bm =        natread(0)
    nat_coal =      natread(1)
    nat_imports =   natread(2)
    nat_gas =       natread(3)
    nat_nuclear =   natread(4)
    nat_other =     natread(5)
    nat_hydro =     natread(6)
    nat_solar =     natread(7)
    nat_wind =      natread(8)

    reg_CO2 =        regread(None,'carbon')
    reg_bm =         regread(0)
    reg_coal =       regread(1)
    reg_imports =    regread(2)
    reg_gas =        regread(3)
    reg_nuclear =    regread(4)
    reg_other =      regread(5)
    reg_hydro =      regread(6)
    reg_solar =      regread(7)
    reg_wind =       regread(8)

    """DATA TABLES"""
    
    a = ['Maximum','Average','Minimum']
    b = [max(reg_CO2),round(sum(reg_CO2)/len(reg_CO2),1),min(reg_CO2)]
    c = [max(nat_CO2),round(sum(nat_CO2)/len(nat_CO2),1),min(nat_CO2)]

    t1 = Table([a,b,c],names=('Statistic','National','{}'.format(reg_data_r['data']['shortname'])))

    d = ["Biomass", "Coal","Imports","Gas","Nuclear","Other","Hydro","Solar","Wind"]
    e = [statistics.mean(reg_bm),
         statistics.mean(reg_coal),
         statistics.mean(reg_imports),
         statistics.mean(reg_gas),
         statistics.mean(reg_nuclear),
         statistics.mean(reg_other),
         statistics.mean(reg_hydro),
         statistics.mean(reg_solar),
         statistics.mean(reg_wind)] *u.percent
    f = [statistics.mean(nat_bm),
         statistics.mean(nat_coal),
         statistics.mean(nat_imports),
         statistics.mean(nat_gas),
         statistics.mean(nat_nuclear),
         statistics.mean(nat_other),
         statistics.mean(nat_hydro),
         statistics.mean(nat_solar),
         statistics.mean(nat_wind)] *u.percent

    t2 = Table([d,e,f],names=('Energy Sources', '{}'.format(reg_data_r['data']['shortname']), 'National'))

    for col in t2.itercols():
        if col.info.dtype.kind == 'f':
            np.around(col, decimals=2, out=col)

    print('\nCarbon intensity Statistics(in gCO2/kWh):\n')
    t1.pprint(align=['<','<','<'])
    print('\n\nAverage Energy Production Breakdown:\n')
    t2.pprint(align=['<','<','<'])

    """DATA ANALYSIS"""

    t_length =  len(reg_data_r['data']['data'])

    time = [reg_data_r['data']['data'][n]['from'][5:10] for n in range(t_length)]
    time_raw = [reg_data_r['data']['data'][n]['from'] for n in range(t_length)]

    if reg_data_r['data']['data'][t_length-1]['from'][5:10] == reg_data_r['data']['data'][0]['from'][5:10]:
        time = [reg_data_r['data']['data'][n]['from'][11:16] for n in range(t_length)]
    
    df_reg = pd.DataFrame({
        #'Biomass'         : reg_bm,
        #'Coal'            : reg_coal,
        #'Imports'         : reg_imports,
        #'Gas'             : reg_gas,
        #'Nuclear'         : reg_nuclear,
        #'Other'           : reg_other,
        'Hydro'            : reg_hydro,
        'Solar'            : reg_solar,
        'Wind'             : reg_wind,
        'Carbon Intensity' : reg_CO2
        },index = time)

    df_nat = pd.DataFrame({
        #'Biomass'         : reg_bm,
        #'Coal'            : reg_coal,
        #'Imports'         : reg_imports,
        #'Gas'             : reg_gas,
        #'Nuclear'         : reg_nuclear,
        #'Other'           : reg_other,
        'Hydro'            : nat_hydro,
        'Solar'            : nat_solar,
        'Wind'             : nat_wind,
        'Carbon Intensity' : nat_CO2
        },index = time)

    #"""Big Plot Regional"""
    fig1 = df_reg.plot(secondary_y=['Carbon Intensity'],grid=True)
    fig1.set_ylabel('percent')
    fig1.set_xlabel('Time')
    fig1.right_ax.set_ylabel('gCO2/kWh')
    plt.title('Correlation between Carbon Intensity\n and Energy Generated in {}'.format(reg_data_r['data']['shortname']))

    #"""Sub Plot Regional"""
    fig2 = df_reg.plot(subplots=True,title='Subplots {}'.format(reg_data_r['data']['shortname']),grid=True)
    fig2[0].set_ylabel('percent')
    fig2[1].set_ylabel('percent')
    fig2[2].set_ylabel('percent')
    fig2[3].set_ylabel('CO2/kWh')
    fig2[3].set_xlabel('Time')

    #"""Regional Stacked Plot"""
    labels = ["Hydro ", "Solar", "Wind"]
    fig3, ax3 = plt.subplots()
    ax3.stackplot(time_raw, reg_hydro, reg_solar, reg_wind,labels=labels)
    fig3.suptitle('Accumulative {}'.format(reg_data_r['data']['shortname']))
    ax3.tick_params(axis='y',which='major',labelsize=7)
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    plt.ylabel('percent')

    #"""Big Plot National"""
    fig4 = df_nat.plot(secondary_y=['Carbon Intensity'],grid=True )
    fig4.set_ylabel('percent')
    fig4.set_xlabel('Time')
    fig4.right_ax.set_ylabel('gCO2/kWh')
    plt.title('Correlation between Carbon Intensity\n and Energy Generated Nationally')

    #"""Sub Plot National"""
    fig5 = df_nat.plot(subplots=True,title='Subplots National',grid=True)
    fig5[0].set_ylabel('percent')
    fig5[1].set_ylabel('percent')
    fig5[2].set_ylabel('percent')
    fig5[3].set_ylabel('CO2/kWh')
    fig5[3].set_xlabel('Time')

    #"""National Stacked Plot"""
    labels = ["Hydro ", "Solar", "Wind"]
    fig6, ax6 = plt.subplots()
    ax6.stackplot(time_raw, nat_hydro, nat_solar, nat_wind,labels=labels)
    fig6.suptitle('Accumulative National')
    ax6.tick_params(axis='y',which='major',labelsize=7)
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    plt.ylabel('percent')

    plt.show()

    while True:
        answer = input('Run again? (Y/N): ')
        if answer in ('Y', 'N'):
            break
        print ('Invalid input.')
    if answer == 'Y':
        continue
    else:
        print('Goodbye')
        break
