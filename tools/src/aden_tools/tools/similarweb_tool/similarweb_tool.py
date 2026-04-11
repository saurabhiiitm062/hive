"""
SimilarWeb Tool - Traffic and competitor insights for FastMCP.

Provides website analytics, demographic data, and competitor intelligence.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx

if TYPE_CHECKING:
    from fastmcp import FastMCP

    from aden_tools.credentials import CredentialStoreAdapter


def _get_api_key(credentials: CredentialStoreAdapter | None = None) -> str | dict[str, str]:
    """Get the SimilarWeb API key from credentials or environment."""
    if credentials:
        key = credentials.get("similarweb")
        if key:
            return key

    import os

    env_key = os.environ.get("SIMILARWEB_API_KEY")
    if env_key:
        return env_key

    return {
        "error": "SimilarWeb credentials not configured",
        "help": (
            "Set SIMILARWEB_API_KEY environment variable or configure "
            "via credential store. Get a key at https://developer.similarweb.com/"
        ),
    }


def _make_request(
    endpoint: str,
    api_key: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Helper method to make requests to the SimilarWeb API."""
    if params is None:
        params = {}

    # SimilarWeb official API uses the api key as a query parameter
    params["api"] = api_key

    # Defaults according to official v1 API structure
    if "start_date" not in params:
        # Some default/dummy dates or required by specific endpoints
        pass

    url = f"https://api.similarweb.com/v1/{endpoint}"

    try:
        response = httpx.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict):
            # Enforce returning dict
            return {"data": result}
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def register_tools(mcp: FastMCP, credentials: CredentialStoreAdapter | None = None) -> None:
    """Register SimilarWeb tools with the MCP server."""

    @mcp.tool()
    def similarweb_get_website_overview(
        domain: str,
        start_date: str | None = None,
        end_date: str | None = None,
        country: str = "world",
    ) -> dict[str, Any]:
        """
        Get total traffic and engagement overview for a specific website domain.

        Args:
            domain: The website domain to analyze (e.g., 'amazon.com')
            start_date: Format YYYY-MM (e.g., '2024-01'). Optional.
            end_date: Format YYYY-MM (e.g., '2024-01'). Optional.
            country: 2-letter ISO country code or 'world' (default).

        Returns:
            Dict containing total visits, bounce rate, pages per visit, etc.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params: dict[str, Any] = {"country": country, "granularity": "monthly"}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/total-traffic-and-engagement/visits"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_similar_competitors(domain: str, limit: int = 10) -> dict[str, Any]:
        """
        Find a list of similar websites or competitors for a given domain.

        Args:
            domain: The base website domain (e.g., 'netflix.com')
            limit: Number of similar sites to return (default 10)

        Returns:
            Dict containing a list of similar domains with similarity scores.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params = {"limit": limit}
        endpoint = f"website/{domain}/similar-sites/similarsites"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_traffic_sources(
        domain: str,
        start_date: str | None = None,
        end_date: str | None = None,
        country: str = "world",
    ) -> dict[str, Any]:
        """
        Get the distribution of traffic sources (direct, search, social, referrals) for a domain.

        Args:
            domain: The website domain (e.g., 'nytimes.com')
            start_date: Format YYYY-MM. Optional.
            end_date: Format YYYY-MM. Optional.
            country: 2-letter ISO country code or 'world'.

        Returns:
            Dict containing percentage breakdown of incoming traffic channels.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params: dict[str, Any] = {"country": country, "granularity": "monthly"}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/traffic-sources/overview"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_top_keywords(
        domain: str,
        start_date: str | None = None,
        end_date: str | None = None,
        country: str = "world",
        limit: int = 25,
    ) -> dict[str, Any]:
        """
        Identify top search keywords driving organic or paid traffic to a domain.

        Args:
            domain: The website domain.
            start_date: Format YYYY-MM. Optional.
            end_date: Format YYYY-MM. Optional.
            country: 2-letter ISO country code or 'world'.
            limit: Maximum number of keywords (default 25).

        Returns:
            Dict containing top keywords and their respective traffic share.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params: dict[str, Any] = {"country": country, "limit": limit}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/keywords/organic-search"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_audience_geography(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Get website traffic distribution by country (where visitors are located).

        Args:
            domain: The website domain.
            start_date: Format YYYY-MM. Optional.
            end_date: Format YYYY-MM. Optional.

        Returns:
            Dict containing a list of top countries and their traffic share.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/geography/audience-geography"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_app_overview(
        app_id: str,
        store: str = "google",
        country: str = "us",
    ) -> dict[str, Any]:
        """
        Get an overview of mobile app performance (downloads, rank, usage).

        Args:
            app_id: The app identifier (e.g., 'com.whatsapp' or '310633997').
            store: 'google' for Play Store or 'apple' for App Store.
            country: 2-letter ISO country code (e.g., 'us').

        Returns:
            Dict containing app analytics like global rank, downloads, and usage patterns.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params: dict[str, Any] = {"country": country, "store": store}
        endpoint = f"app/{store}/app/{app_id}/performance/overview"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_audience_interests(
        domain: str,
    ) -> dict[str, Any]:
        """
        Identify the browsing interests and other visited categories of a website's audience.

        Args:
            domain: The website domain.

        Returns:
            Dict containing affinity scores for categories and other websites.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        endpoint = f"website/{domain}/audience-interests/also-visited"
        return _make_request(endpoint, api_key, {})

    @mcp.tool()
    def similarweb_get_top_outgoing_links(
        domain: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """
        Identify the top destination websites traffic flows to from this domain.

        Args:
            domain: The website domain.
            start_date: Format YYYY-MM. Optional.
            end_date: Format YYYY-MM. Optional.

        Returns:
            Dict containing top outgoing links and their traffic share.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/traffic-sources/outgoing-links"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_device_split(
        domain: str,
        start_date: str | None = None,
        end_date: str | None = None,
        country: str = "world",
    ) -> dict[str, Any]:
        """
        Get the split of traffic between Desktop and Mobile web for a domain.

        Args:
            domain: The website domain.
            start_date: Format YYYY-MM. Optional.
            end_date: Format YYYY-MM. Optional.
            country: 2-letter ISO country code or 'world'.

        Returns:
            Dict showing the desktop vs mobile traffic percentage breakdown.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params: dict[str, Any] = {"country": country}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/total-traffic-and-engagement/desktop-vs-mobile"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_category_leaders(
        category: str,
        country: str = "world",
        device: str = "Desktop_and_MobileWeb",
        limit: int = 100,
    ) -> dict[str, Any]:
        """
        Get the top websites in a specific industry/category based on traffic.

        Args:
            category: Industry category slug (e.g., 'E-commerce_and_Shopping').
            country: 2-letter ISO country code or 'world'.
            device: 'Desktop', 'MobileWeb', or 'Desktop_and_MobileWeb'.
            limit: Number of leaders to return (default 100).

        Returns:
            Dict listing the category leaders ranked by traffic volume.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        params = {"country": country, "device": device, "limit": limit}
        endpoint = f"industry/{category}/top-websites"
        return _make_request(endpoint, api_key, params)

    @mcp.tool()
    def similarweb_get_technologies(
        domain: str,
    ) -> dict[str, Any]:
        """
        Get the software technologies, frameworks, and tracking codes used by a domain.

        Args:
            domain: The website domain.

        Returns:
            Dict listing the technologies grouped by category (e.g., 'Analytics', 'CMS').
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res
        api_key = api_key_res

        endpoint = f"website/{domain}/technologies/technologies-used"
        return _make_request(endpoint, api_key, {})

    @mcp.tool()
    def similarweb_get_social_media_traffic(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Breaks down traffic from different social platforms.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/traffic-sources/social"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_referring_websites(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Identifies incoming traffic domains (referrals).
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/traffic-sources/referrals"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_subdomain_traffic(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Analyzes traffic distribution across subdomains.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/total-traffic-and-engagement/subdomains"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_top_pages(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Finds the most popular pages/sections of a domain.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/popular-pages/popular-pages"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_app_ranking(
        app_id: str, store: str = "google", country: str = "us"
    ) -> dict[str, Any]:
        """
        Gets App Store/Google Play rankings.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {"country": country, "store": store}
        endpoint = f"app/{store}/app/{app_id}/ranking/category-rank"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_app_engagement(
        app_id: str, store: str = "google", country: str = "us"
    ) -> dict[str, Any]:
        """
        Fetches DAU, MAU, and retention metrics.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {"country": country, "store": store}
        endpoint = f"app/{store}/app/{app_id}/engagement/usage-metrics"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_display_ads_publishers(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Identifies ad networks and publishers used.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/traffic-sources/display-publishers"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_paid_search_competitors(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Identifies PPC/Google Ads competitors.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/traffic-sources/paid-search-competitors"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_ad_creatives(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Retrieves active ad creatives for a domain.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/traffic-sources/ad-creatives"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_cross_browsing_behavior(
        domain: str, start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, Any]:
        """
        Analyzes audience overlap between two domains.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        params: dict[str, Any] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        endpoint = f"website/{domain}/audience-interests/cross-browsing"
        return _make_request(endpoint, api_key_res, params)

    @mcp.tool()
    def similarweb_get_company_info(domain: str) -> dict[str, Any]:
        """
        Gets estimated revenue, employee size, HQ location.
        """
        api_key_res = _get_api_key(credentials)
        if isinstance(api_key_res, dict):
            return api_key_res

        endpoint = f"website/{domain}/company-info/company-info"
        return _make_request(endpoint, api_key_res, {})
