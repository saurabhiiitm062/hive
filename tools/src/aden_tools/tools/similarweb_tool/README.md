# SimilarWeb Tool

This tool provides integration with the SimilarWeb API, allowing agents to fetch deep website analytics, competitor intelligence, market research data, traffic sources, and audience demographics directly from SimilarWeb's database.

## Prerequisites

To use this tool, you need an API key from the [SimilarWeb Developer Portal](https://developer.similarweb.com/).

Set the `SIMILARWEB_API_KEY` environment variable or store it in your credentials manager.

## Available Tools

- `similarweb_get_website_overview`: Get total traffic, bounce rate, global/country ranking for a specific website domain.
- `similarweb_get_similar_competitors`: Find a list of similar websites or competitors for a given domain.
- `similarweb_get_traffic_sources`: Break down direct, social, organic, and paid traffic sources.
- `similarweb_get_top_keywords`: Identify top search keywords driving traffic.
- `similarweb_get_audience_geography`: Get traffic distribution by country.

## Usage

```python
from fastmcp import FastMCP
from aden_tools.tools.similarweb_tool import register_tools

mcp = FastMCP("my-server")
register_tools(mcp)
```
