from rich import print
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser, Page
def get_job_description(job_id: str) -> str:
    with sync_playwright() as p:
        browser: Browser = p.chromium.connect_over_cdp(
            endpoint_url="http://localhost:9222/", timeout=5000
        )
        url: str=f"https://www.linkedin.com/jobs/view/{job_id}"
        page: Page =browser.contexts[0].pages[2]
        page.goto(url=url,timeout=15000)        
        page.wait_for_selector(selector='#job-details', timeout=15000)
        job_id_element = page.query_selector(selector='#job-details')
        details: str|None=job_id_element.text_content()
        return details if details else "No description found"
        


if __name__ == "__main__":
    job_ids =[                                               
    '4129403317',                                               
    '4125562922',                                                      
    '4144858273',
    '4129297008'
]
    for job_id in job_ids:
        print(get_job_description(job_id))
    