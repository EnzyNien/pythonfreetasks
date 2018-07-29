import pandas as pd
import hh

#areas_list=[
#    'Москва',
#    'Москва и Московская область',
#    10002])
#data = hh(
#    title='python',
#    areas_list=['Москва',])
#data.get_data()

##сохранение в json для примера
#data.main_df.to_json('main_df.json')
#data.skills_df.to_json('skills_df.json')
#data.spec_df.to_json('spec_df.json')

def result_ptint(df, col_name):

    min_ = df[col_name].min()
    max_ =df[col_name].max()
    mean_ = df[col_name].mean()
    median_ = df[col_name].median()

    print(col_name.upper())
    print(f'min:    {min_:.2f}')
    print(f'max:    {max_:.2f}')
    print(f'mean:   {mean_:.2f}')
    print(f'median: {median_:.2f}')

def exchange_func(row, exc_dict):
   
    curr = row['currency']
    course = exc_dict[curr]
    ndfl = (1 - 0.18) if row['gross'] == 1 else 1
    row['from'] = 0 if pd.isnull(row['from']) else row['from'] * course * ndfl
    row['to'] = row['from'] if pd.isnull(row['to']) else row['to'] * course * ndfl
    row['currency'] = 'RUR'
    return row

main_df = pd.read_json('main_df.json')

# получим уникальные значениz валют как массив numpy
print(main_df['currency'].unique())

# словарь с курсами обмена
exchange = {'USD':62.78,'RUR':1,'EUR':73.29,'KZT':0.18, None:0}

# получим уникальные значения опыта как массив numpy
exp_ = main_df['experience'].unique()
print(exp_)


for item in exp_.tolist():
    # выберем строки для текущего опыта работы
    cur_exp_ = main_df[main_df['experience']==item]

    # преобразуем значение зарплат к валюте rub
    # axis=1 - переберем все строки
    # **kwgs (в нашем случае это exc_dict) - дополнительный параметр передаваемый
    # в функцию exchange_func
    cur_exp_ = cur_exp_.apply(exchange_func, axis=1, exc_dict=exchange)
    cur_exp_ = cur_exp_[cur_exp_['from'] != 0]

    cur_exp_.sort_values('to', inplace=True)

    # обрежем последние и первые значение на 5 элементов 
    # дабы избежать рудиментарных высоких зарплат 
    cur_exp_ = cur_exp_[5:-5]
    print('='*10)
    print(f'{item}:')
    result_ptint(cur_exp_,'from')
    result_ptint(cur_exp_,'to')
    print('\n')

##################################################
# тоже самое, но через метод groupby
# проанализируем зарплаты по типу графика работы
# fullDay - Полный день
# shift - Сменный график
# flexible - Гибкий график
# remote - Удаленная работа
type_='schedule'
grouped = main_df.groupby(by=type_)
for item, group in grouped:
    cur_exp_ = main_df[main_df[type_]==item]
    cur_exp_ = cur_exp_.apply(exchange_func, axis=1, exc_dict=exchange)
    cur_exp_ = cur_exp_[cur_exp_['from'] != 0]
    cur_exp_.sort_values('to', inplace=True)
    cur_exp_ = cur_exp_[5:-5]
    print('='*10)
    print(f'{item}:')
    result_ptint(cur_exp_,'from')
    result_ptint(cur_exp_,'to')
    print('\n')
