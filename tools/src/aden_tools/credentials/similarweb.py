from __future__ import annotations

from aden_tools.credentials.base import CredentialSpec

SIMILARWEB_CREDENTIALS = {
    "similarweb": CredentialSpec(
        env_var="SIMILARWEB_API_KEY",
        tools=[
            "similarweb_get_website_overview",
            "similarweb_get_similar_competitors",
            "similarweb_get_traffic_sources",
            "similarweb_get_top_keywords",
            "similarweb_get_audience_geography",
            "similarweb_get_app_overview",
            "similarweb_get_audience_interests",
            "similarweb_get_top_outgoing_links",
            "similarweb_get_device_split",
            "similarweb_get_category_leaders",
            "similarweb_get_technologies",
            "similarweb_get_social_media_traffic",
            "similarweb_get_referring_websites",
            "similarweb_get_subdomain_traffic",
            "similarweb_get_top_pages",
            "similarweb_get_app_ranking",
            "similarweb_get_app_engagement",
            "similarweb_get_display_ads_publishers",
            "similarweb_get_paid_search_competitors",
            "similarweb_get_ad_creatives",
            "similarweb_get_cross_browsing_behavior",
            "similarweb_get_company_info",
        ],
        required=True,
        help_url="https://developer.similarweb.com/",
        description="API key for SimilarWeb traffic and competitor insights.",
        direct_api_key_supported=True,
        api_key_instructions="""To get a SimilarWeb API key:
1. Go to the SimilarWeb Developer Portal (https://developer.similarweb.com/)
2. Or log into your SimilarWeb Pro account at pro.similarweb.com
3. Navigate to Account Settings > API (or Data Extraction / API section)
4. Click on "Generate API Key"
5. Copy the generated API key and securely store it in your .env file""",
        credential_id="similarweb",
        credential_key="api_key",
        health_check_endpoint="https://api.similarweb.com/v1/website/google.com/total-traffic-and-engagement/visits",
    )
}
