from rich import print
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser, Page

def get_job_ids(job_type: str,job_count: int) -> list[str]:
    with sync_playwright() as p:
        browser: Browser = p.chromium.connect_over_cdp(
            endpoint_url="http://localhost:9222/", timeout=5000
        )
        url: str=f"https://www.linkedin.com/jobs/{job_type}"
        page: Page =browser.contexts[0].pages[1]
        job_ids=[]
        for i in range(0,job_count,25):
            page.goto(url+f"?start={i}" if i!=0 else url,timeout=15000)        
            page.wait_for_selector(selector='li[data-occludable-job-id]', timeout=15000)
            job_id_element = page.query_selector_all(selector='li[data-occludable-job-id]')
            
            for element in job_id_element:
                job_ids.append( element.get_attribute(name='data-occludable-job-id'))
        return job_ids

# Example usage
print(get_job_ids(job_type="sales",job_count=50))