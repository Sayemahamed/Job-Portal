from rich import print
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser, Page
from html_to_markdown import convert_to_markdown
import re



def get_job_description(job_id: str) -> str:
    with sync_playwright() as p:
        browser: Browser = p.chromium.connect_over_cdp(
            endpoint_url="http://localhost:9222/", timeout=5000
        )
        url: str = f"https://www.linkedin.com/jobs/view/{job_id}"
        page: Page = browser.contexts[0].pages[2]
        page.goto(url=url, timeout=20000)
        page.wait_for_selector(selector="#job-details", timeout=15000)
        job_id_element = page.query_selector(selector="#job-details")
        details: str | None = convert_to_markdown(
            "<div>" + job_id_element.inner_html() + "</div>"  # type: ignore
        )
        details = re.sub(r" +", " ", details)
        details = re.sub(r"\n+", "\n", details)
        return details if details else "No description found"


def get_job_ids(job_type: str, job_count: int) -> list[str]:
    with sync_playwright() as p:
        browser: Browser = p.chromium.connect_over_cdp(
            endpoint_url="http://localhost:9222/", timeout=5000
        )
        url: str = f"https://www.linkedin.com/jobs/{job_type}"
        page: Page = browser.contexts[0].pages[1]
        job_ids = []
        for i in range(0, job_count, 25):
            page.goto(url + f"?start={i}" if i != 0 else url, timeout=15000)
            page.wait_for_selector(selector="li[data-occludable-job-id]", timeout=15000)
            job_id_element = page.query_selector_all(
                selector="li[data-occludable-job-id]"
            )

            for element in job_id_element:
                job_ids.append(element.get_attribute(name="data-occludable-job-id"))
        return job_ids


# Example usage
if __name__ == "__main__":
    print(get_job_ids(job_type="sales", job_count=50))
if __name__ == "__main__":
    job_ids = ["4129403317", "4125562922", "4144858273", "4129297008"]
    for job_id in job_ids:
        print(get_job_description(job_id))
