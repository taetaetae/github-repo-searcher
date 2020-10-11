#!/usr/bin/pyhton

import requests, time, datetime, sys
from dateutil.relativedelta import relativedelta


def main(args) :
    args = dict([arg.split('=', maxsplit=1) for arg in args[1:]])

    # init
    github_api_url='https://api.github.com'
    github_id=args['github_id']
    github_token=args['github_token']

    search_topic=args.get('search_topic', 'hacktoberfest')
    search_month_range=args.get('search_month_range', 6)
    search_location=args.get('search_location', 'Korea')
    my_auth=(github_id, github_token)

    now_datetime=datetime.datetime.now()
    limit_datetime=relativedelta(months=-search_month_range) + now_datetime

    while now_datetime > limit_datetime :
        page=1
        while True :
            topics=requests.get(url=github_api_url + '/search/repositories?q=topic:' + search_topic + '+created:'
                                    + str(now_datetime.strftime('%Y-%m-%d'))
                                    + '&page=' + str(page),
                                auth=my_auth,
                                headers={'Accept': 'application/vnd.github.mercy-preview+json'}).json()
            time.sleep(5) # https://docs.github.com/en/free-pro-team@latest/rest/reference/search
            if int(len(topics['items'])) == 0:
                break

            print(
                'search base time : ' + now_datetime.strftime('%Y-%m-%d') + ', ',
                'now time : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ', ',
                'page : ' + str(page) + ', ',
                'user_count : ' + str(len(topics['items'])) + ', ',
                'total_count : ' + str(topics['total_count'])
            )

            for topic in topics['items'] :
                user=requests.get(url=github_api_url + '/users/' + topic['owner']['login'], auth=my_auth).json()
                # https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#rate-limiting
                # For API requests using Basic Authentication or OAuth, you can make up to 5,000 requests per hour.
                # Sun Oct 11 2020 17:23:32 GMT+0900
                if 'location' in user and search_location in user['location'] :
                    print(topic['html_url'], topic['created_at'])

            page=page+1

        now_datetime = now_datetime + datetime.timedelta(days=-1)


if __name__ == "__main__" :
    main(sys.argv)