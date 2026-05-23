import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('CarsDataset.csv', encoding='latin1')

def changing_data_types_in_HorsePower(df):
    df['HorsePower'] = df['HorsePower'].str[:3] #обрезаем строки, где остаются только трёхзначные числа, а числа где ещё знаки в дальнейшем уберутся
    df['HorsePower'] = pd.to_numeric(df['HorsePower'], errors='coerce') #Этот метод берет строку, и если в ней цифры он переведет в int, но если есть намёк на тип str он его обратит в NaN
    df['HorsePower'] = df['HorsePower'].fillna(0).astype(int) #метод fillna(0) переведет все значения NaN в 0, но столец станет в типе float, поэтому метод astype(int) нужен для превращения всего столбца в int


def change_data_type_money(df):
    df['Cars Prices'] = df['Cars Prices'].str.replace(',', '', regex=False) #заменяем запятые на ничего
    df['Cars Prices'] = df['Cars Prices'].str[1:] #убираем доллар
    df['Cars Prices'] = pd.to_numeric(df['Cars Prices'], errors='coerce') 
    df['Cars Prices'] = df['Cars Prices'].fillna(0).astype(int)


def change_seats(df):
    df['Seats'] = pd.to_numeric(df['Seats'], errors='coerce')
    df['Seats'] = df['Seats'].fillna(0).astype(int) 


def changing_Total_Speed(df):
    df['Total Speed'] = df['Total Speed'].str[:3] #обрезаем строки, где остаются только трёхзначные числа, а числа где ещё знаки в дальнейшем уберутся
    df['Total Speed'] = pd.to_numeric(df['Total Speed'], errors='coerce')
    df['Total Speed'] = df['Total Speed'].fillna(0).astype(int)


def changing_Performance(df):
    df['Performance(0 - 100 )KM/H'] = df['Performance(0 - 100 )KM/H'].str[:3]
    df['Performance(0 - 100 )KM/H'] = pd.to_numeric(df['Performance(0 - 100 )KM/H'], errors='coerce') 
    df['Performance(0 - 100 )KM/H'] = df['Performance(0 - 100 )KM/H'].fillna(0.0).astype(float)#форматируем значения в тип float


def changing_Capacity(df):
    df['CC/Battery Capacity'] = df['CC/Battery Capacity'].str.replace(',', '', regex=False)
    df['CC/Battery Capacity'] = df['CC/Battery Capacity'].str[:4] #обрезаем строки, где остаются только четырёхзначные числа, а числа где ещё знаки в дальнейшем уберутся
    df['CC/Battery Capacity'] = pd.to_numeric(df['CC/Battery Capacity'], errors='coerce')
    df['CC/Battery Capacity'] = df['CC/Battery Capacity'].fillna(0).astype(int)


def change_torque(df):
    df['Torque'] = df['Torque'].str[:3] #обрезаем строки, где остаются только трёхзначные числа, а числа где ещё знаки в дальнейшем уберутся
    df['Torque'] = pd.to_numeric(df['Torque'], errors='coerce')
    df['Torque'] = df['Torque'].fillna(0).astype(int)


def clean_df(df):
    change_data_type_money(df)
    changing_data_types_in_HorsePower(df)
    change_seats(df)
    changing_Total_Speed(df)
    changing_Performance(df)
    changing_Capacity(df)
    change_torque(df)


def filter_family(df, price_index):
    match(price_index):
        # категория семейная, цена 1
        case 0: df_filtered = df[
            (df['Seats'] > 4) & 
            (df['Cars Prices'] > 20000) & 
            (df['Cars Prices'] < 25000)
            ]
        # категория семейная, цена 2
        case 1: df_filtered = df[
            (df['Seats'] > 5) & 
            (df['Cars Prices'] > 25000) & 
            (df['Cars Prices'] < 40000)
            ]
        # категория семейная, цена 3
        case 2: df_filtered = df[
            (df['Seats'] > 6) & 
            (df['Cars Prices'] > 40000) & 
            (df['Cars Prices'] < 55000)
            ]
    return df_filtered


def filter_SUV(df, price_index):
    match(price_index):
        #категория внедорожные, цена 1
        case 0: df_filtered = df[
            (df['Seats'] > 4) &
            (df['Cars Prices'] > 38000) & 
            (df['Cars Prices'] < 45000) & 
            (df['Total Speed'] >= 160) & 
            (df['Total Speed'] <= 220) &
            (df['HorsePower'] >= 130) & 
            (df['HorsePower'] <= 600) &
            (df['Performance(0 - 100 )KM/H'] >= 8.0) &    
            (df['Performance(0 - 100 )KM/H'] <= 13.0) &   
            (df['Torque'] >= 180) &                       
            (df['Torque'] <= 500) &
            (df['CC/Battery Capacity'] > 1900)
            ]

        #категория внедорожные, цена 2
        case 1: df_filtered = df[
            (df['Seats'] > 4) &
            (df['Cars Prices'] > 45000) & 
            (df['Cars Prices'] < 52000) & 
            (df['Total Speed'] >= 160) & 
            (df['Total Speed'] <= 220) &
            (df['HorsePower'] >= 130) & 
            (df['HorsePower'] <= 600) &
            (df['Performance(0 - 100 )KM/H'] >= 8.0) &    
            (df['Performance(0 - 100 )KM/H'] <= 13.0) &   
            (df['Torque'] >= 180) &                       
            (df['Torque'] <= 500) &
            (df['CC/Battery Capacity'] > 1900)
            ]

        #категория внедорожные, цена 3
        case 2: df_filtered = df[
            (df['Seats'] > 4) &
            (df['Cars Prices'] > 52000) & 
            (df['Cars Prices'] < 100000) & 
            (df['Total Speed'] >= 160) & 
            (df['Total Speed'] <= 220) &
            (df['HorsePower'] >= 130) & 
            (df['HorsePower'] <= 600) &
            (df['Performance(0 - 100 )KM/H'] >= 8.0) &    
            (df['Performance(0 - 100 )KM/H'] <= 13.0) &   
            (df['Torque'] >= 180) &                       
            (df['Torque'] <= 500) &
            (df['CC/Battery Capacity'] > 1900)
            ]
    return df_filtered


def filter_sport(df, price_index):
    match(price_index):
        #категория спорткары, цена 1
        case 0: df_filtered = df[
            (df['Cars Prices'] > 140000) &
            (df['Cars Prices'] < 220000) &
            (df['HorsePower'] >= 250) &                   
            (df['HorsePower'] <= 900) &                  
            (df['Total Speed'] >= 240) &           
            (df['Performance(0 - 100 )KM/H'] <= 5.5) &    
            (df['Performance(0 - 100 )KM/H'] >= 2.5) &     
            (df['Torque'] >= 300) &                     
            (df['Seats'] <= 4) &                          
            (df['CC/Battery Capacity'] > 1800)           
            ]

        #категория спорткары, цена 2
        case 1: df_filtered = df[
            (df['Cars Prices'] > 220000) &
            (df['Cars Prices'] < 350000) &
            (df['HorsePower'] >= 250) &                  
            (df['HorsePower'] <= 900) &                    
            (df['Total Speed'] >= 240) &                   
            (df['Performance(0 - 100 )KM/H'] <= 5.5) &    
            (df['Performance(0 - 100 )KM/H'] >= 2.5) & 
            (df['Torque'] >= 300) &                      
            (df['Seats'] <= 4) &                          
            (df['CC/Battery Capacity'] > 1800)             
            ]

        #категория спорткары, цена 3
        case 2: df_filtered = df[
            (df['Cars Prices'] > 350000) &
            (df['HorsePower'] >= 250) &                  
            (df['HorsePower'] <= 900) &                 
            (df['Total Speed'] >= 240) &                 
            (df['Performance(0 - 100 )KM/H'] <= 5.5) &     
            (df['Performance(0 - 100 )KM/H'] >= 2.5) &    
            (df['Torque'] >= 300) &                       
            (df['Seats'] <= 4) &                          
            (df['CC/Battery Capacity'] > 1800)             
            ]
    return df_filtered


def plot_family():
    plt.figure(figsize=(6, 5))
    plt.bar(df_filtered["Label"], df_filtered["Seats"])
    plt.xticks(rotation=90)#поворачиваем, чтобы было читаем
    plt.xlabel('Марка, модель машины')
    plt.ylabel('Кол-во сидений')
    plt.title('Семейный автомобиль, 20.000 - 25.000$', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout() #подбирает значения полей так, чтобы были видны заголовки
    plt.show()


def plot_SUV():
    plt.figure(figsize=(6, 5))
    plt.bar(df_filtered["Label"], df_filtered["CC/Battery Capacity"])
    plt.xticks(rotation=90)#поворачиваем, чтобы было читаем
    plt.xlabel('Марка, модель машины')
    plt.ylabel('Объем двигателя')
    plt.title('Внедорожный автомобиль, 38.000$ - 45.000$', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.show()


def plot_sport():
    plt.figure(figsize=(6, 5))
    plt.bar(df_filtered["Label"], df_filtered["HorsePower"])
    plt.xticks(rotation=90)#поворачиваем, чтобы было читаем
    plt.xlabel('Марка, модель машины')
    plt.ylabel('Кол-во лошадинных сил')
    plt.title('Спортивный автомобиль, 140.000$ - 220.000$', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.show()


def plot_edit(column):
    plt.figure(figsize=(6, 5))
    plt.bar(df_filtered["Label"], df_filtered[f"{column}"])
    plt.xticks(rotation = 90) 
    plt.xlabel('Марка, модель машины')
    match(column):
        case 'Seats' : plt.ylabel('Кол-во сидений'),
        case 'CC/Battery Capacity': plt.ylabel('Объем двигателя'),
        case 'HorsePower': plt.ylabel('Кол-во лошадинных сил')
    plt.tight_layout()
    plt.show()