"""Tests for similarweb_tool - Website traffic and competitor analytics."""

from unittest.mock import MagicMock, patch

import httpx
import pytest
from fastmcp import FastMCP

from aden_tools.tools.similarweb_tool.similarweb_tool import register_tools


# Mock credentials adapter
class MockCredentials:
    def get(self, key):
        if key in ("similarweb", "similarweb_api_key"):
            return "test_api_key_123"
        return None


@pytest.fixture
def credentials():
    return MockCredentials()


@pytest.fixture
def tools_fns(mcp: FastMCP, credentials):
    """Register and return the SimilarWeb tools."""
    register_tools(mcp, credentials=credentials)
    return {
        "overview": mcp._tool_manager._tools["similarweb_get_website_overview"].fn,
        "competitors": mcp._tool_manager._tools["similarweb_get_similar_competitors"].fn,
        "sources": mcp._tool_manager._tools["similarweb_get_traffic_sources"].fn,
        "keywords": mcp._tool_manager._tools["similarweb_get_top_keywords"].fn,
        "geography": mcp._tool_manager._tools["similarweb_get_audience_geography"].fn,
    }


class TestSimilarWebTool:
    """Tests for similarweb_tool functions."""

    @patch("aden_tools.tools.similarweb_tool.similarweb_tool.httpx.get")
    def test_get_website_overview_success(self, mock_get, tools_fns):
        """Test getting website traffic overview."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "global_rank": 10,
            "bounce_rate": 0.45,
            "visits": 1000000,
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Execute
        result = tools_fns["overview"](
            domain="example.com", start_date="2024-01", end_date="2024-01"
        )

        # Verify
        mock_get.assert_called_once()
        assert "example.com" in mock_get.call_args[0][0]
        assert mock_get.call_args[1]["params"]["api"] == "test_api_key_123"
        assert result["global_rank"] == 10
        assert result["visits"] == 1000000

    @patch("aden_tools.tools.similarweb_tool.similarweb_tool.httpx.get")
    def test_get_similar_competitors_success(self, mock_get, tools_fns):
        """Test getting similar competitors."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "similar_sites": [{"site": "competitor1.com"}, {"site": "competitor2.com"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Execute
        result = tools_fns["competitors"](domain="example.com", limit=2)

        # Verify
        mock_get.assert_called_once()
        assert mock_get.call_args[1]["params"]["limit"] == 2
        assert "similar_sites" in result
        assert len(result["similar_sites"]) == 2

    @patch("aden_tools.tools.similarweb_tool.similarweb_tool.httpx.get")
    def test_api_http_error_handling(self, mock_get, tools_fns):
        """Test HTTP error handling."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"

        # We need to create a proper Exception instance the way httpx raises it
        mock_get.side_effect = httpx.HTTPStatusError(
            "403 Forbidden", request=MagicMock(), response=mock_response
        )

        # Execute
        result = tools_fns["overview"](domain="example.com")

        # Verify
        assert "error" in result
        assert "HTTP error 403" in result["error"]
