import schedule, requests
from .h2s.scraper import scraper as h2s_scraper

# 29 Eind
H2S_SEARCH_URL = "https://holland2stay.com/residences.html?available_to_book=179&city=" + 29


def run_scrapers():
    h2s_scraper()

def report_crash():
    requests.post(
        "https://discordapp.com/api/webhooks/997554015783100476/nltop35cmxVMDKKMtLC8kYz_AOKZdAa4VvGgQkM-Msjbm14X2DewK971BJF54y8arLZ6",
        data={"content": "Scrapers are down!"},
    )


run_scrapers()
schedule.every(1).minutes.do(run_scrapers)
while True:
    try:
        schedule.run_pending()
    except Exception:
        report_crash()
