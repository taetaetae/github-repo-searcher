#!/usr/bin/pyhton

import requests, time, datetime, sys
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def main(args):
    dummy_dict = {}
    for arg in args:
        if '=' in arg:
            split = arg.split('=')
            dummy_dict[split[0]] = split[1]
    args = dummy_dict

    if 'github_id' not in args or 'github_id' not in args:
        print('Required parameters are missing.')
        exit(-1)

    f = open("found.txt", 'w')

    # init
    github_api_url = 'https://api.github.com'
    github_id = args['github_id']
    github_token = args['github_token']

    search_topic = args.get('search_topic', 'hacktoberfest')
    search_month_range = int(args.get('search_month_range', 6))
    search_location = args.get('search_location', 'Korea')
    my_auth = (github_id, github_token)

    now_datetime = datetime.datetime.now()
    limit_datetime = relativedelta(months=-search_month_range) + now_datetime

    # for simple test, set isDebug to True. The test should found 2 repos by phg98
    isDebug = False
    if isDebug:
        now_datetime = parse('2015-04-26')
        limit_datetime = relativedelta(days=-search_month_range) + now_datetime

    while now_datetime > limit_datetime:
        page = 1
        while True:
            search_base_time = str(now_datetime.strftime('%Y-%m-%d'))
            topics = requests.get(url=github_api_url + f'/search/users?q=location:{search_location}+created:{search_base_time}&page={page}',
                                  auth=my_auth).json()
            time.sleep(3)
            # https://docs.github.com/en/free-pro-team@latest/rest/reference/search
            # To satisfy that need, the GitHub Search API provides up to 1,000 results for each search.
            if int(len(topics['items'])) == 0:
                break

            print(
                f'search base time : {search_base_time}, ',
                f'now time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, ',
                f'page : {page}, ',
                f'user_count : {len(topics["items"])}, ',
                f'total_count : {topics["total_count"]}'
            )

            user_string = ''
            for user in topics['items']:
                user_string += f'user:{user["login"]}+'
            repos = requests.get(url=github_api_url + f'/search/repositories?q={user_string}topic:{search_topic}', auth=my_auth).json()
            time.sleep(3)
            if 'errors' in repos:
                print(f'error on user:{user_string} topic:{search_topic} with error message:{repos["errors"]}')
                f.write(f'error on user:{user_string} topic:{search_topic} with error message:{repos["errors"]} \n')
            if 'items' in repos and repos['items'] is not None and repos['total_count'] > 0:
                print(repos)
                for repo in repos['items']:
                    f.write(repo['html_url']+'\n')

            page = page + 1

        now_datetime = now_datetime + datetime.timedelta(days=-1)

    f.close()

if __name__ == "__main__":
    main(sys.argv)
