import pandas as pd #библеотека работы с таблицами
import numpy as np #библеотека для быстрых математических операций
import matplotlib.pyplot as plt #библеотека для построения графиков
%matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_excel('data_set.xlsx') #открываем файл с таблицей

df_for_model = df.drop(['date', 'opponent'], axis=1)

#выводится результат последней введенной команды
#df.head() #смотрим первые 5 строк, чтобы удебиться, что файл открыт корректно
#df.shape #показывает сколько строк и столбцов таблице
#df.describe() #получим основную статистику по числовым столбцам: среднее, мин, макс и т.д.
#df.isnull().sum() #показывает пропуски каждого столбца

x = df_for_model.drop(['win(0)/lose(1)', 'goals_count', 'opp_goals_count'], axis=1)
y = df_for_model['win(0)/lose(1)']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)
#print("Типы данных в DataFrame:")
#print(x_train.head())

#print("Типы данных в DataFrame:")
#print(x_train.dtypes)
y_pred = model.predict(x_test)
print(y_pred[:10])
print(y_test.values[:10])

accuracy = accuracy_score(y_test, y_pred)
print(f"\nТочность модели: {accuracy:.2f}")

#Для первого раза неплохо, но надо увеличить датасет и переработать признаки
