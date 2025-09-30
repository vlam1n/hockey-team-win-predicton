import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

pages = [
    'https://www.championat.com/hockey/_superleague/tournament/2202/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/2559/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/2593/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/2875/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/2971/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/3298/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/3929/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/4305/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/4449/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/4893/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/5077/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/5255/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/5383/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/5856/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/5974/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/6446/calendar/',
    'https://www.championat.com/hockey/_superleague/tournament/6608/calendar/'
]

SELECTORS = {
    'match_container': 'tr.stat-results__row',
    'link_match': 'td.stat-results__link a[href]'
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

all_urls_data = []
for url in pages:
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        time.sleep(2)

        soup = BeautifulSoup(response.text, 'lxml')

        match_containers = soup.select(SELECTORS['match_container'])
        print(f"Найдено матчей: {len(match_containers)}")

        for container in match_containers:
            try:
                # Извлекаем ссылку
                link_el = container.select_one(SELECTORS['link_match'])
                if link_el:
                    href = link_el.get('href')
                    if href:
                        all_urls_data.append(f'https://www.championat.com{href}')
            except Exception as e:
                print(f"Ошибка при парсинге контейнера: {e}")
                continue


    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к странице: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
print(len(all_urls_data))
#обработка страницы
PAGE_SELECTORS = {
    'data': 'div.match-info__title',
    'team': 'div.match-info__team-name',
    'score': 'div.match-info__score-total',
    'match_status': 'div.match-info__score-extra',
    'win_prediction': 'span.user-votes__value span',
    'left_statisics': 'div.stat-graph__value._left strong',
    'right_statisics': 'div.stat-graph__value._right strong'
}
all_mathes_data = []
for i in range(5): #сделаем тестовый парсинг на небольшой выборке
    match_data = []
    try:
        response_1 = requests.get(all_urls_data[i], headers=header)
        response_1.raise_for_status()
        time.sleep(2)

        soup_1 = BeautifulSoup(response_1.text, 'lxml') 

        try:
            data_element = soup_1.select_one(PAGE_SELECTORS['data'])
            data = data_element.get_text(strip=True)
        except Exception as e:
            print(f'Ошибка даты{e}')

        try:
            team_elemet = soup_1.select(PAGE_SELECTORS['team'])
            teams = [team.get_text(strip=True) for team in team_elemet]
        except Exception as e:
            print(f"Ошибка команды:{e}")
            print(teams)
            continue

        try:
            score_element = soup_1.select_one(PAGE_SELECTORS['score'])
            score = score_element.get_text(strip=True) if score_element else 0
        except Exception as e:
            print(f"Ошибка счета:{e}")
            print(score)
            continue
        try:
            match_status_element = soup_1.select_one(PAGE_SELECTORS['match_status'])
            match_status = match_status_element.get_text(strip=True) if match_status_element else 0
        except Exception as e:
            print(f"Ошибка статуса:{e}")
            continue
        try:    
            win_element = soup_1.select(PAGE_SELECTORS['win_prediction'])
            win_prediction = [win.get_text(strip=True) for win in win_element]
            if len(win_prediction) > 0:
                predict_team1 = win_prediction[0]
                predict_team2 = win_prediction[2]
            else:
                predict_team1 = 0
                predict_team2 = 0
        except Exception as e:
            print(f"Ошибка предсказания:{e}")
            continue
        try:
            left_statistics_element = soup_1.select(PAGE_SELECTORS['left_statisics'])
            left_statistics = [left.get_text(strip=True) for left in left_statistics_element]
            if len(left_statistics) > 3:
                team_1_strikes = left_statistics[0]
                team_1_trows = left_statistics[1]
                team_1_block_strikes = left_statistics[2]
                team_1_strong = left_statistics[3]
                team_1_penalty = left_statistics[4]
            else:
                team_1_strikes = left_statistics[0]
                team_1_trows = left_statistics[1]
                team_1_block_strikes = 0
                team_1_strong = 0
                team_1_penalty = left_statistics[2]
        except Exception as e:
            print(f"Ошибка левой статистики:{e}")
            continue
        try:
            right_statistics_element = soup_1.select(PAGE_SELECTORS['right_statisics'])
            right_statistics = [right.get_text(strip=True) for right in right_statistics_element]
            if len(right_statistics) > 3:
                team_2_strikes = right_statistics[0]
                team_2_trows = right_statistics[1]
                team_2_block_strikes = right_statistics[2]
                team_2_strong = right_statistics[3]
                team_2_penalty = right_statistics[4]
            else:
                team_2_strikes = right_statistics[0]
                team_2_trows = right_statistics[1]
                team_2_block_strikes = 0
                team_2_strong = 0
                team_2_penalty = right_statistics[2]
        except Exception as e:
            print(f"Ошибка правой статистики:{e}")
            continue
        match_data.append({
            'data': data,
            'team1': teams[0],
            'team2': teams[1],
            'goals_team1':  score[0],
            'goals_team2': score[4],
            'match_status': match_status,
            'predict_team1': predict_team1,
            'predict_team2': predict_team2,
            'team_1_strikes': team_1_strikes,
            'team_1_trows': team_1_trows,
            'team_1_block_strikes': team_1_block_strikes,
            'team_1_strong': team_1_strong,
            'team_1_penalty': team_1_penalty,
            'team_2_strikes': team_2_strikes,
            'team_2_trows': team_2_trows,
            'team_2_block_strikes': team_2_block_strikes,
            'team_2_strong': team_2_strong,
            'team_2_penalty': team_2_penalty,
        })

        all_mathes_data.extend(match_data)
        print('матч добавлен')

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к странице: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}") 

if all_mathes_data:
    df = pd.DataFrame(all_mathes_data)
    file_path = '/Users/vladimirkuzmin/Documents/VS code projects/Python files/temp_parsing.xlsx'
    df.to_excel(file_path, index=False)
    
    full_path = os.path.abspath(file_path)
    print(f"\nВсе данные успешно сохранены в: {full_path}")
    print(f"Всего обработано матчей: {len(all_mathes_data)}")
    
    print("\nПервые 5 матчей:")
    print(df.head())

else:
    print("Не удалось найти данные о матчах.")
