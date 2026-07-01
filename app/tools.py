import time

import requests
from duckduckgo_search import DDGS

from app.config import NVD_API_KEY, NVD_API_URL


def search_security_news(topic: str, max_results: int = 5) -> str:
    """Searches the web for today's security news on a specific topic.

    Args:
        topic: The topic/platform to search for (e.g. 'Android', 'iOS', 'web app security', 'AI LLM security').
        max_results: The maximum number of search results to return.

    Returns:
        A markdown formatted string containing the search results (title, snippet, URL).
    """
    query = f"today security news vulnerability exploit {topic}"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f"No recent news found for {topic}."

            formatted_results = []
            for r in results:
                title = r.get("title", "No Title")
                body = r.get("body", "No description available.")
                href = r.get("href", "#")
                formatted_results.append(f"- **[{title}]({href})**\n  {body}\n")
            return "\n".join(formatted_results)
    except Exception as e:
        return f"Error searching for '{topic}': {e!s}. Falling back to local search news placeholder."


def fetch_recent_cves(keyword: str, limit: int = 5) -> str:
    """Fetches recent CVEs from the NVD API for a given keyword and filters them.

    Args:
        keyword: The search keyword (e.g., 'Android', 'iOS', 'JWT', 'OAuth').
        limit: Number of CVEs to fetch.

    Returns:
        A markdown formatted list of CVEs with their details.
    """
    params = {
        "keywordSearch": keyword,
        "resultsPerPage": limit,
    }

    headers = {}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY
    else:
        # NVD API rate limits heavily. Let's sleep to respect limits if API key is not present.
        time.sleep(2.0)

    try:
        # First request to get total results
        response = requests.get(NVD_API_URL, params=params, headers=headers, timeout=15)
        if response.status_code == 403:
            return f"Rate limit or access forbidden by NVD API for keyword '{keyword}' (HTTP 403)."
        if response.status_code != 200:
            return f"Error fetching CVEs for {keyword}: HTTP {response.status_code}"

        data = response.json()
        total_results = data.get("totalResults", 0)
        if total_results == 0:
            return f"No CVEs found for keyword '{keyword}'."

        # NVD API v2 sorts by publish date ASCENDING.
        # To get the latest CVEs, we fetch from the end of the results.
        vulns = data.get("vulnerabilities", [])
        if total_results > limit:
            params["startIndex"] = total_results - limit
            params["resultsPerPage"] = limit
            if not NVD_API_KEY:
                time.sleep(2.0)
            response = requests.get(
                NVD_API_URL, params=params, headers=headers, timeout=15
            )
            if response.status_code == 200:
                vulns = response.json().get("vulnerabilities", [])
            elif response.status_code == 403:
                # Fallback to the initial results instead of failing
                pass

        formatted_cves = []
        for item in vulns:
            cve = item.get("cve", {})
            cve_id = cve.get("id")
            published = cve.get("published", "")

            # Extract description
            desc = "No description available."
            for d in cve.get("descriptions", []):
                if d.get("lang") == "en":
                    desc = d.get("value")
                    break

            # Extract CVSS score and severity
            metrics = cve.get("metrics", {})
            score = "N/A"
            severity = "UNKNOWN"

            # Check v3.1 then v3.0 then v2
            for v_key in ["cvssMetricV31", "cvssMetricV30"]:
                if metrics.get(v_key):
                    cvss_data = metrics[v_key][0].get("cvssData", {})
                    score = cvss_data.get("baseScore", score)
                    severity = cvss_data.get("baseSeverity", severity)
                    break
            else:
                if metrics.get("cvssMetricV2"):
                    cvss_data = metrics["cvssMetricV2"][0].get("cvssData", {})
                    score = cvss_data.get("baseScore", score)
                    severity = metrics["cvssMetricV2"][0].get("baseSeverity", severity)

            formatted_cves.append(
                f"### [{cve_id}](https://nvd.nist.gov/vuln/detail/{cve_id}) (Keyword: {keyword})\n"
                f"- **Published**: {published}\n"
                f"- **CVSS Score**: {score} ({severity})\n"
                f"- **Description**: {desc}\n"
                f"- **Reference Link**: [NVD CVE Detail](https://nvd.nist.gov/vuln/detail/{cve_id})\n"
            )

        # Reverse the order so the most recent (which was at the very end) is shown first
        formatted_cves.reverse()
        return "\n".join(formatted_cves)

    except Exception as e:
        return f"Error retrieving CVEs for keyword '{keyword}': {e!s}"
