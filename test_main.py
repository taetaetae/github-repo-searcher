import main, os, pytest

@pytest.fixture
def args():
    args = []
    args.append('github_id='+os.environ['MY_GITHUB_ID'])
    args.append('github_token='+os.environ['MY_GITHUB_TOKEN'])
    args.append('search_topic=hacktoberfest-dummy-test')
    args.append('search_month_range=0')
    args.append('search_day_range=1')
    args.append('search_start_date=2020-11-01')
    args.append('search_location=Korea')
    return args
    
def test_main_found_1_result(args):
    found_count = main.main(args)
    assert found_count == 1

def test_main_found_no_result(args):
    args.append('search_start_date=2020-11-02')
    
    found_count = main.main(args)
    assert found_count == 0
