import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

page_urls = ['https://www.championat.com/hockey/_superleague/tournament/1770/teams/45636/result/',
             'https://www.championat.com/hockey/_superleague/tournament/2134/teams/59028/result/',
             'https://www.championat.com/hockey/_superleague/tournament/2202/teams/63278/result/',
             'https://www.championat.com/hockey/_superleague/tournament/2559/teams/96459/result/',
             'https://www.championat.com/hockey/_superleague/tournament/2593/teams/99223/result/',
             'https://www.championat.com/hockey/_superleague/tournament/2875/teams/159819/result/',
             'https://www.championat.com/hockey/_superleague/tournament/2971/teams/165069/result/',
             'https://www.championat.com/hockey/_superleague/tournament/3298/teams/202110/result/',
             'https://www.championat.com/hockey/_superleague/tournament/3929/teams/207195/result/',
             'https://www.championat.com/hockey/_superleague/tournament/4305/teams/217269/result/',
             'https://www.championat.com/hockey/_superleague/tournament/4449/teams/220419/result/',
             'https://www.championat.com/hockey/_superleague/tournament/4893/teams/229877/result/',
             'https://www.championat.com/hockey/_superleague/tournament/5077/teams/233217/result/',
             'https://www.championat.com/hockey/_superleague/tournament/5255/teams/238961/result/',
             'https://www.championat.com/hockey/_superleague/tournament/5383/teams/241619/result/',
             'https://www.championat.com/hockey/_superleague/tournament/5856/teams/253368/result/',
             'https://www.championat.com/hockey/_superleague/tournament/5974/teams/255654/result/',
             'https://www.championat.com/hockey/_superleague/tournament/6446/teams/265700/result/']

SELECTORS = {
    'match_container': 'tr.stat-results__row',
    'date': 'td.stat-results__date-time',
    'team': 'span.table-item__name',
    'score': 'span.stat-results__count-main',
    'match_status': 'span.stat-results__count-ext'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

all_matches_data = []

for i in range(len(page_urls)):
    try:
        print(f"Обрабатываем сезон {i+1}/{len(page_urls)}: {page_urls[i]}")
        response = requests.get(page_urls[i], headers=headers)
        response.raise_for_status()
        time.sleep(3)

        soup = BeautifulSoup(response.text, 'lxml')
        
        match_containers = soup.select(SELECTORS['match_container'])
        print(f"Найдено матчей: {len(match_containers)}")

        matches_data = []

        for container in match_containers:
            try:
                date_element = container.select_one(SELECTORS['date'])
                date = date_element.get_text(strip=True) if date_element else 'Дата не найдена'

                team_elements = container.select(SELECTORS['team'])
                teams = [team.get_text(strip=True) for team in team_elements]

                opponent = ''
                if len(teams) == 2:
                    if teams[0] == 'ЦСКА':
                        opponent = teams[1]
                    else:
                        opponent = teams[0]
                
                score_element = container.select_one(SELECTORS['score'])
                score_text = score_element.get_text(strip=True) if score_element else '0:0'
                
                status_element = container.select_one(SELECTORS['match_status'])
                match_status = status_element.get_text(strip=True) if status_element else ''

                try:
                    goals = score_text.split(':')
                    goals_count = int(goals[0])
                    opponent_goals_count = int(goals[1])
                except (ValueError, IndexError):
                    goals_count = 0
                    opponent_goals_count = 0

                if len(teams) == 2:
                    if teams[0] == 'ЦСКА':
                        cska_goals = goals_count
                        opponent_goals = opponent_goals_count
                    elif teams[1] == 'ЦСКА':
                        cska_goals = opponent_goals_count
                        opponent_goals = goals_count
                    else:
                        cska_goals = goals_count
                        opponent_goals = opponent_goals_count

                    if cska_goals > opponent_goals:
                        result = 0 
                    else:
                        result = 1 

                    matches_data.append({
                        'Date': date,
                        'Team_1': teams[0],
                        'Team_2': teams[1],
                        'CSKA_goals': cska_goals,
                        'Opponent_goals': opponent_goals,
                        'Match_status': match_status,
                        'Opponent': opponent,
                        'Target': result
                    })

            except Exception as e:
                print(f"Ошибка при парсинге контейнера: {e}")
                continue
        
        all_matches_data.extend(matches_data)
        print(f"Добавлено матчей из сезона {i+1}: {len(matches_data)}")
        print(f"Всего матчей собрано: {len(all_matches_data)}")
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к странице: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if all_matches_data:
    df = pd.DataFrame(all_matches_data)
    file_path = r'C:\VS code progects\python files\cska_all_matches_results.xlsx'
    df.to_excel(file_path, index=False)
    
    full_path = os.path.abspath(file_path)
    print(f"\nВсе данные успешно сохранены в: {full_path}")
    print(f"Всего обработано матчей: {len(all_matches_data)}")
    
    print("\nПервые 5 матчей:")
    print(df.head())
    
    
else:
    print("Не удалось найти данные о матчах.")
