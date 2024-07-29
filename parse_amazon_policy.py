import asyncio
import json

import aiohttp
from bs4 import BeautifulSoup


cookies = {
    "session-id": "258-5595314-9854402",
    "session-id-time": "2082787201l",
    "i18n-prefs": "GBP",
    "ubid-acbuk": "259-7012535-0067466",
    "sp-cdn": '"L5Z9:UA"',
    "csm-hit": "tb:8AT8SFK30VHHSQR3QEBW+s-MEG38VYZENH9BJBJ8J5F|1722185828003&t:1722185828003&adb:adblk_no",
    "session-token": '"ea8KCwx87uEr0OOZOlctX+A/sb9Mdoey2dytDoPKZZ3JDjOVawZ1svpIbtSzuAxLR6YnII4boJumm1EnMG3iYbiLGEYAarPshiUR5H9uhQDqDiAt2aSfW1k9DS4GFa+F6Szofheb58bSe2TtTRukKN7DGXWADiCK0nMIupI4UR1FnDDauIr2xGb0KvV7FmQkYFyra4R5QlTZko//Czs51z/W4CUWn7cMsqnCTpjcUTeBMoFt5jPa6XhrWk5oQj04kAtjmem14BJRaLqRHEYvDHRraOjgVDnB0+C+QCuSPn+YjnaXtbmebj6e3xQl0erX7kBmdSyzh50wUW4WuNkBoAyue3HqHSEv9wJzdG5bvMw="',
}
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    # 'cookie': 'session-id=258-5595314-9854402; session-id-time=2082787201l; i18n-prefs=GBP; ubid-acbuk=259-7012535-0067466; sp-cdn="L5Z9:UA"; csm-hit=tb:8AT8SFK30VHHSQR3QEBW+s-MEG38VYZENH9BJBJ8J5F|1722185828003&t:1722185828003&adb:adblk_no; session-token="ea8KCwx87uEr0OOZOlctX+A/sb9Mdoey2dytDoPKZZ3JDjOVawZ1svpIbtSzuAxLR6YnII4boJumm1EnMG3iYbiLGEYAarPshiUR5H9uhQDqDiAt2aSfW1k9DS4GFa+F6Szofheb58bSe2TtTRukKN7DGXWADiCK0nMIupI4UR1FnDDauIr2xGb0KvV7FmQkYFyra4R5QlTZko//Czs51z/W4CUWn7cMsqnCTpjcUTeBMoFt5jPa6XhrWk5oQj04kAtjmem14BJRaLqRHEYvDHRraOjgVDnB0+C+QCuSPn+YjnaXtbmebj6e3xQl0erX7kBmdSyzh50wUW4WuNkBoAyue3HqHSEv9wJzdG5bvMw="',
    "device-memory": "8",
    "downlink": "10",
    "dpr": "1",
    "ect": "4g",
    "priority": "u=0, i",
    "rtt": "50",
    "sec-ch-device-memory": "8",
    "sec-ch-dpr": "1",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-ch-ua-platform-version": '"6.5.0"',
    "sec-ch-viewport-width": "932",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "viewport-width": "932",
}


async def parse_amazon_policy_links():

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.amazon.co.uk/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7",
            headers=headers,
            cookies=cookies,
        ) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            links = soup.find("ul", class_="nav-topics").find_all("a")
            return [{"title": link.get_text(), "link": link["href"]} for link in links]


async def parse_amazon_policy(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link, cookies=cookies, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            return soup.find("div", class_="help-service-content").get_text()


async def main():
    links = await parse_amazon_policy_links()
    text = ""
    for link in links:
        policy = await parse_amazon_policy(link["link"])
        text += policy.strip() + "\n\n"
    with open("amazon_policy.txt", "w") as f:
        f.write(text)


if __name__ == "__main__":
    asyncio.run(main())
