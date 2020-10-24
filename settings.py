from pathlib import Path  # Python 3.6+ only
import dotenv as env

env_path = Path('.') / '.env'

setting = env.dotenv_values(dotenv_path=env_path)


def check():
    if setting['github_id'] is None or setting['github_token'] is None:
        print('Required parameters are missing.')
        exit(-1)
    elif setting['search_topic'] == None or setting['search_month_range'] == None or setting['search_location'] == None:
        setting['search_topic'], setting['search_month_range'], setting['search_location'] = 'hacktoberfest', 6, 'Korea'
        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
    else:
        return str(setting['search_topic']), int(setting['search_month_range'] or 6), str(setting['search_location'])
