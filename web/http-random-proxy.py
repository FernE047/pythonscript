import time
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

if __name__ == "__main__":
    start = time.time()
    req_proxy = RequestProxy()
    print(f"Initialization took: {(time.time() - start)} sec")
    print(f"Size: {len(req_proxy.get_proxy_list())}")
    print(f"ALL = {list(map(lambda x: x.get_address(), req_proxy.get_proxy_list()))}")

    test_url = "http://ipv4.icanhazip.com"

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print(
            f"Proxied Request Took: {(time.time() - start)} sec => Status: {request.__str__()}"
        )
        if request is not None:
            print(f"\t Response: ip={''.join(request.text).encode('utf-8')}")
        print(f"Proxy List Size: {len(req_proxy.get_proxy_list())}")

        print("-> Going to sleep..")
        time.sleep(10)


##############################################################SOLU��O#################################################################


from http.requests.proxy.requestProxy import RequestProxy
from requests import get

# list of proxies proxies...
req_proxy = RequestProxy()
proxy_list = req_proxy.get_proxy_list()
#

game_date = "03/16/2017"
results_dict = {}
headers = {
    "Referer": "http://stats.nba.com/standings/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
}

response = ""
len_resultsets = 0
trying = True

while trying:
    try:
        proxies = {"http": random.choice(proxy_list)}
        response = get(
            "http://stats.nba.com/stats/scoreboard",
            params={"DayOffset": 0, "LeagueID": "00", "gameDate": game_date},
            headers=headers,
            timeout=30,
            proxies=proxies,
        )

        response.raise_for_status()  # raise exception if invalid response
        len_resultsets = len(response.json()["resultSets"])

        trying = False

    except:
        time.sleep(5)
