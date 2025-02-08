from celery import shared_task
from rich import print
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser, Page
from html_to_markdown import convert_to_markdown
import re

@shared_task
def get_job_description(job_id: str) -> str:
    with sync_playwright() as p:
        browser: Browser = p.chromium.connect_over_cdp(
            endpoint_url="http://localhost:9222/", timeout=5000
        )
        url: str = f"https://www.linkedin.com/jobs/view/{job_id}"
        page: Page = browser.contexts[0].pages[3]
        page.goto(url=url, timeout=20000)
        page.wait_for_selector(selector="#job-details", timeout=15000)
        job_id_element = page.query_selector(selector="#job-details")
        details: str | None = convert_to_markdown(
            "<div>" + job_id_element.inner_html() + "</div>"  # type: ignore
        )
        details = re.sub(r" +", " ", details)
        details = re.sub(r"\n+", "\n", details)
        return details if details else "No description found"


@shared_task
def add():
    return "Task executed! without delay"
