from pathlib import Path  # Python 3.6+ only
import dotenv as env

env_path = Path('.') / '.env'

setting = env.dotenv_values(dotenv_path=env_path)


def check():
    if setting['github_id'] is None or setting['github_token'] is None or setting['search_month_range'] == 6314:
        print('Required settings are missing or search_month_range is 6314 over')
        exit(-1)
    print(str(setting['search_topic'] or 'hacktoberfest'), int(
        setting['search_month_range'] or 6), str(setting['search_location'] or 'Korea'))
    return str(setting['search_topic'] or 'hacktoberfest'), int(setting['search_month_range'] or 6), str(setting['search_location'] or 'Korea')
