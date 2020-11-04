#!/usr/bin/pyhton

import requests, time, datetime, sys, os
from dateutil.relativedelta import relativedelta

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

    # init
    github_api_url = 'https://api.github.com'
    github_id = args['github_id']
    github_token = args['github_token']

    search_topic = args.get('search_topic', 'hacktoberfest')
    search_month_range = int(args.get('search_month_range', 6))
    search_day_range = int(args.get('search_day_range', 0))
    search_location = args.get('search_location', 'Korea')
    my_auth = (github_id, github_token)

    search_start_date = args.get('search_start_date', None)
    if search_start_date is None:
        now_datetime = datetime.datetime.now()
    else:
        now_datetime = datetime.datetime.strptime(search_start_date, '%Y-%m-%d')
    print(now_datetime)
    limit_datetime = relativedelta(months=-search_month_range) + now_datetime
    limit_datetime += relativedelta(days=-search_day_range) 
    found_count = 0

    while now_datetime > limit_datetime:
        page = 1
        while True:
            search_base_time = str(now_datetime.strftime('%Y-%m-%d'))
            topics = requests.get(url=github_api_url + f'/search/repositories?q=topic:{search_topic}+created:{search_base_time}&page={page}',
                                  auth=my_auth,
                                  headers={'Accept': 'application/vnd.github.mercy-preview+json'}).json()
            time.sleep(5)
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

            for topic in topics['items']:
                user_id=topic['owner']['login']
                user = requests.get(url=github_api_url + f'/users/{user_id}', auth=my_auth).json()
                time.sleep(0.5)
                # https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#rate-limiting
                # For API requests using Basic Authentication or OAuth, you can make up to 5,000 requests per hour.

                if 'location' in user and user['location'] is not None and search_location in user['location']:
                    print(f'Found it! = createdat : {topic["created_at"]}, repository : {topic["html_url"]}')
                    found_count += 1

            page = page + 1

        now_datetime = now_datetime + datetime.timedelta(days=-1)
    return found_count

def test_main():
    args = []
    args.append('github_id='+os.environ['MY_GITHUB_ID'])
    args.append('github_token='+os.environ['MY_GITHUB_TOKEN'])
    args.append('search_topic=hacktoberfest-dummy-test')
    args.append('search_month_range=0')
    args.append('search_day_range=1')
    args.append('search_start_date=2020-11-01')
    args.append('search_location=Korea')
    
    found_count = main(args)
    assert found_count == 1

if __name__ == "__main__":
    main(sys.argv)
