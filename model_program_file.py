import pandas as pd #библеотека работы с таблицами
import numpy as np #библеотека для быстрых математических операций
import matplotlib.pyplot as plt #библеотека для построения графиков
%matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier 
import warnings

df = pd.read_excel('cska_all_matches_results.xlsx') #открываем файл с таблицей
# Теперь надо поработать над Fuauture engeering

# Признак вин стрика

# Признак колличества голов за последние 5 игр

df_proceed = df.copy()
df_proceed['is_home'] = df_proceed.apply(
    lambda row: 1 if 'ЦСКА' in row['Team_1'] else 0,
    axis=1
)
df_proceed['match_ending'] = df_proceed['Match_status'].apply(
    lambda x: 0 if x in ['Б', 'ОТ'] else 1
)
df_proceed['CSKA_form_5'] = 0.0
for i in range(len(df_proceed)):
  if i < 5:
    continue
  else:
    last_5_games = df_proceed.iloc[i-5:i]
    wins = len(last_5_games[last_5_games['Target'] == 1])
    df_proceed.at[i, 'CSKA_form_5'] = wins / 5

df_proceed['CSKA_goals_avg_5'] = 0.0
for i in range(len(df_proceed)):
  if i < 5:
    continue
  else:
    last_5_games = df_proceed.iloc[i-5:i]
    goals = sum(last_5_games['CSKA_goals'])
    df_proceed.at[i, 'CSKA_goals_avg_5'] = goals / 5

df_encoded = pd.get_dummies(df_proceed, columns=['Opponent'], prefix='opp')
df_for_model = df_encoded.drop(['Date', 'Opponent_goals', 'CSKA_goals', 'Team_1', 'Team_2', 'Match_status'], axis=1)


x = df_for_model.drop(['Target'], axis=1)
y = df_for_model['Target']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print(y_pred[:10])
print(y_test.values[:10])

accuracy = accuracy_score(y_test, y_pred)
print(f"\nТочность модели: {accuracy:.2f}")
