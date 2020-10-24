#!/usr/bin/pyhton

import requests
import time
import datetime
from settings import check, setting
from dateutil.relativedelta import relativedelta


def main():
    check()

  # init
    github_api_url = 'https://api.github.com'
    github_id = str(setting['github_id'])
    github_token = setting['github_token']

    search_topic = setting['search_topic']
    search_month_range = int(setting['search_month_range'])
    search_location = setting['search_location']
    my_auth = (github_id, github_token)

    now_datetime = datetime.datetime.now()
    limit_datetime = relativedelta(months=-search_month_range) + now_datetime

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
                user_id = topic['owner']['login']
                user = requests.get(url=github_api_url +
                                    f'/users/{user_id}', auth=my_auth).json()
                time.sleep(0.5)
                # https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#rate-limiting
                # For API requests using Basic Authentication or OAuth, you can make up to 5,000 requests per hour.

                if 'location' in user and user['location'] is not None and search_location in user['location']:
                    print(
                        f'Found it! = createdat : {topic["created_at"]}, repository : {topic["html_url"]}')

            page = page + 1

        now_datetime = now_datetime + datetime.timedelta(days=-1)


if __name__ == "__main__":
    main()
