# Github repo searcher 🔎

- 🤷 github 의 repo를 검색하되 아래와 같은 조건에 해당하는 repository를 찾는 파이썬 스크립트 입니다.
  - topic 이 '지정한 토픽' 이고 (and)
  - created_at 이 '지정한 범위' 내에 있고 (and)
  - 찾은 repository > user 의 location 이 '지정한 지역' 일때


- 🙋‍♂️ github 에서 '토픽' 과 '지역' 을 and 조건으로 검색이 안되어 만들게 되었습니다.
- 🤔 github api 호출 제한이 있기 때문에 적당히 호출해야 합니다.

- 💻 사용법
  - 파라미터를 받아 처리 됩니다.
  ```shell
  $ python main.py github_id=taetaetae github_token=ASDFASDFASDF
  search base time : 2020-10-11,  now time : 2020-10-11 17:47:46,  page : 1,  user_count : 30,  total_count : 76
  search base time : 2020-10-11,  now time : 2020-10-11 17:48:15,  page : 2,  user_count : 30,  total_count : 76
  search base time : 2020-10-11,  now time : 2020-10-11 17:48:45,  page : 3,  user_count : 16,  total_count : 76
  ...

  ```
  
  | 항목 | 필수여부 | 내용 | 기본값 | 
  | --- | --- | --- | --- | 
  | github_id | O | github id | 없음 |
  | github_token | O | Personal access tokens  | 없음 |
  | search_topic | X | 찾으려는 topic | hacktoberfest |
  | search_month_range | X | 찾으려는 기간(월) | 6 |
  | search_location | X | 찾으려는 지역 | Korea |