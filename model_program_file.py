import pandas as pd #библеотека работы с таблицами
import numpy as np #библеотека для быстрых математических операций
import matplotlib.pyplot as plt #библеотека для построения графиков
%matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_excel('data_set.xlsx') #открываем файл с таблицей

teams_list = df['opponent'].unique().tolist() #присваиваем каждой команде свой id
team_to_id = {team: idx for idx, team in enumerate(teams_list)}
df['opponent_id'] = df['opponent'].map(team_to_id)

df_for_model = df.drop(['date', 'opponent', 'opp_goals_count'], axis=1)

x = df_for_model.drop(['win(0)/lose(1)'], axis=1)
y = df_for_model['win(0)/lose(1)']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print(y_pred[:10])
print(y_test.values[:10])

accuracy = accuracy_score(y_test, y_pred)
print(f"\nТочность модели: {accuracy:.2f}")
