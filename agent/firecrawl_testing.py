from firecrawl import FirecrawlApp
from rich import print

app = FirecrawlApp()

# Crawl a website:
print(
    app.scrape_url(
        "devdocs.io/",
        params={
            "formats": ["markdown"],
        },
    )
)
