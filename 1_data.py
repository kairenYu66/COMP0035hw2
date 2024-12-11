import pandas as pd
import matplotlib.pyplot as plt

def load_and_clean_data():
    df = pd.read_excel('Energy consumption.xlsx', header=[0, 1,2], index_col=0)
    df = df.drop('Year')
    return df
df = load_and_clean_data()

def explore_data(df):
    print('################ df head #######################')
    print(df.head(5))
    print('################ df tail #######################')
    print(df.tail(5))
    print('################ df info ######################')
    print(df.info())
    print('################ df index ######################')
    print(df.index)
    print('################ df describe ######################')
    print(df.iloc[:-3,:].describe())
def missing_data_check(df):
    missing_values_per_row = df.isnull().sum(axis=1)
    bads = missing_values_per_row[missing_values_per_row > 0]
    print(f"Rows with missing values:")
    if not bads.empty:
        print(bads)
    else:
        print("ALL good. \n")
def boxplot(x, save_file_name, x_name='domenstic total consumption'):
    plt.figure(figsize=(3, 4))
    plt.boxplot(x)  
    #plt.ylabel('Value')
    plt.xticks([1],[x_name])
    #plt.show()
    plt.savefig(save_file_name+'.png', bbox_inches='tight')


missing_data_check(df)

explore_data(df)

df_boroughs = df.iloc[:-3,:]

boxplot(df_boroughs['Sector']['Domestic']['Total'], 'section1-pic1')

df.head()

################### 1.2 #####################

def sort_and_calculate_percentage(df):
    df = df.sort_values(by=[('Grand Total','Unnamed: 21_level_1' , 'Unnamed: 21_level_2')], ascending=False)
    df = pd.concat([df[('Sector','Domestic' , 'Total')], df[('Sector','Industrial and Commercial' , 'Total')], df[('Sector','Transport' , 'Total')],df[('Grand Total','Unnamed: 21_level_1' , 'Unnamed: 21_level_2')]],axis=1)
    df.columns = columns=['Domestic','Industrial and Commercial','Transport','Total']
    df = df.div(df['Total'], axis=0)
    return df
q1 = sort_and_calculate_percentage(df_boroughs)
q1.to_csv('q1.csv', index=True)

def find_main_cause(q1):
    plt.figure(figsize=(10, 6))
    plt.boxplot(q1.iloc[:,:3], patch_artist=True)
    plt.ylabel('percentage')
    plt.xticks([1, 2, 3], q1.columns[:3]) 
    plt.savefig('q3.png', bbox_inches='tight')

find_main_cause(q1)

q2 = df_boroughs['Sector']['Domestic'].iloc[:,:-1]
q2_2 = df_boroughs['Sector']['Industrial and Commercial'].drop(['Electricity w/o transport','Total'], axis=1)

q2_2.to_csv('q2-IC.csv', index=True)
q2.to_csv('q2-domestic.csv', index=True)

def correlation_explore(q2, save_name='q2-domestic'):
    col_names = q2.columns[1:]
    for i,col in enumerate(col_names):
        plt.scatter(q2['Electricity'], q2[col])
        plt.xlabel('Electricity')
        plt.ylabel(col)
        plt.savefig(f'{save_name}-{i}.png')
        plt.show()
correlation_explore(q2)
correlation_explore(q2_2, 'q2-IC')





