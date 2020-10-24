from pathlib import Path  # Python 3.6+ only
import dotenv as env

env_path = Path('.') / '.env'

setting = env.dotenv_values(dotenv_path=env_path)


def check():
    if setting['github_id'] is None or setting['github_token'] is None or setting['search_month_range'] == 6314:
        print('Required settings are missing or search_month_range is 6314 over')
        exit(-1)
    elif setting['search_topic'] == str('') is setting['search_month_range'] == str('') is setting['search_location'] == str(''):
        setting['search_topic'], setting['search_month_range'], setting['search_location'] = 'hacktoberfest', 6, 'Korea'

        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
    elif setting['search_month_range'] == str('') is setting['search_location'] == str(''):
        setting['search_month_range'], setting['search_location'] = 6, 'Korea'

        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
    elif setting['search_topic'] == str('') is setting['search_location'] == str(''):
        setting['search_topic'], setting['search_location'] = 'hacktoberfest', 'Korea'

        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
    elif setting['search_topic'] == str(''):
        setting['search_topic'] = 'hacktoberfest'

        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
    elif setting['search_month_range'] == str(''):
        setting['search_month_range'] = 6

        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
    elif setting['search_location'] == str(''):
        setting['search_location'] = 'Korea'

        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
    else:
        return str(setting['search_topic']), int(setting['search_month_range']), str(setting['search_location'])
