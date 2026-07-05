## Daily Security Briefing: Penetration Testing Focus

### Critical & High CVEs

| CVE ID | Keyword | CVSS Score | Severity | Pentest Relevance/Impact |
| :------- | :-------- | :--------- | :------- | :----------------------- |
| [CVE-2026-50160](https://nvd.nist.gov/vuln/detail/CVE-2026-50160) | JWT | 10.0 | CRITICAL | **Mass Assignment / Authentication Bypass / RCE:** Unauthenticated attackers can overwrite `JWT_SECRET` via mass assignment, leading to JWT forgery for any user (including administrators) and full server compromise. |
| [CVE-2026-14099](https://nvd.nist.gov/vuln/detail/CVE-2026-14099) | iOS | 8.8 | HIGH | **Use-after-free / RCE:** Heap corruption in Chrome for iOS allows remote attackers to potentially exploit heap corruption and achieve arbitrary code execution via crafted HTML and specific UI gestures. |
| [CVE-2026-14067](https://nvd.nist.gov/vuln/detail/CVE-2026-14067) | iOS | 8.8 | HIGH | **Use-after-free / RCE:** Use-after-free in Chrome for iOS allows remote attackers to execute arbitrary code via a crafted HTML page. |
| [CVE-2026-14428](https://nvd.nist.gov/vuln/detail/CVE-2026-14428) | Android | 8.3 | HIGH | **Sandbox Escape / RCE:** Insufficient input validation in Google Chrome (Dawn component) on Android allows a compromised renderer to potentially perform a sandbox escape. |
| [CVE-2026-14401](https://nvd.nist.gov/vuln/detail/CVE-2026-14401) | Android | 8.3 | HIGH | **Sandbox Escape / RCE:** Insufficient input validation in Google Chrome (ANGLE component) on Android allows a compromised renderer to potentially perform a sandbox escape. |
| [CVE-2026-14336](https://nvd.nist.gov/vuln/detail/CVE-2026-14336) | JWT | 8.2 | HIGH | **OIDC Issuer Bypass / JWT Forgery / SSRF:** PIA's OIDC issuer allowlist uses a weak prefix check, enabling attackers to craft malicious issuers (e.g., `https://ci.eclipse.org@evil.host`) to perform SSRF and accept attacker-signed JWTs. |
| [CVE-2026-11800](https://nvd.nist.gov/vuln/detail/CVE-2026-11800) | JWT | 8.1 | HIGH | **JWT Algorithm Confusion / Authentication Bypass / Privilege Escalation:** Keycloak JWT Authorization Grant flow allows attackers with valid client credentials to bypass signature verification and forge access tokens, impersonating federated users. |
| [CVE-2026-28699](https://nvd.nist.gov/vuln/detail/CVE-2026-28699) | OAuth | 8.1 | HIGH | **OAuth2 Scope Bypass:** Gitea allows OAuth2 access token scope enforcement to be bypassed via HTTP Basic authentication, leading to unauthorized access. |
| [CVE-2026-58299](https://nvd.nist.gov/vuln/detail/CVE-2026-58299) | Android | 7.5 | HIGH | **Race Condition / RCE:** Time-of-check time-of-use (TOCTOU) race condition in Microsoft Edge for Android allows unauthorized attackers to execute code over a network. |
| [CVE-2026-59096](https://nvd.nist.gov/vuln/detail/CVE-2026-59096) | JWT | 7.5 | HIGH | **OIDC Discovery Poisoning / JWT Forgery / SSRF:** Dapr Sentry's OIDC discovery endpoint honors `X-Forwarded-Host` without validation, allowing unauthenticated attackers to poison the discovery document and cause relying parties to accept attacker-signed JWTs. |
| [CVE-2026-11310](https://nvd.nist.gov/vuln/detail/CVE-2026-11310) | JWT | 7.5 | HIGH | **X.509 Trust-Chain Bypass:** wolfSSL's OpenSSL compatibility certificate verifier allows untrusted intermediate certificates to be accepted as trust anchors, leading to acceptance of attacker-controlled certificates. |
| [CVE-2026-55759](https://nvd.nist.gov/vuln/detail/CVE-2026-55759) | JWT | 7.4 | HIGH | **JWT Claims Validation Bypass / Authentication Bypass:** Rocket.Chat's Apple Sign-In handler verifies JWT signatures but skips claims validation, allowing replay of Apple identity tokens for authentication as a target user. |
| [CVE-2026-58297](https://nvd.nist.gov/vuln/detail/CVE-2026-58297) | Android | 7.1 | HIGH | **Information Disclosure:** Exposure of private personal information to an unauthorized actor in Microsoft Edge for Android allows unauthorized attackers to disclose information over a network. |
| [CVE-2026-58296](https://nvd.nist.gov/vuln/detail/CVE-2026-58296) | Android | 7.1 | HIGH | **Information Disclosure:** Exposure of private personal information to an unauthorized actor in Microsoft Edge for Android allows unauthorized attackers to disclose information over a network. |

### Mobile Security (Android/iOS)

Recent news highlights critical zero-day vulnerabilities actively exploited in both Android and iOS ecosystems. Android devices have seen multiple 0-day exploits, with Google and CISA confirming ongoing attacks targeting Android users and releasing emergency patches for affected versions (Android 14, 15, 16, and 16 QPR2) to address these high-severity issues and sandbox escapes. [[Android 0-Day Vulnerability Exploited in Attacks to Gain ...](https://cybersecuritynews.com/android-0-day-vulnerability-exploited-device/)][[Critical Android Update—Google And CISA Confirm 0-Day ...](https://www.forbes.com/sites/daveywinder/2026/03/04/critical-android-update-google-confirms-0day-security-bypass-attacks/)] Apple has similarly rushed out emergency security updates for iOS and iPadOS to counter actively exploited critical zero-day vulnerabilities, with warnings from CISA about these in-the-wild exploitations. Researchers have also identified new and powerful exploit kits targeting iPhones. [[Apple Zero-Day Vulnerability Actively Exploited in ...](https://cyberpress.org/apple-zero-day-vulnerability-actively-exploited-in-sophisticated-targeted-attacks/)][[CISA Warns of Apple iOS Vulnerability Exploited in Wild](https://cybersecuritynews.com/cisa-apple-ios-vulnerability-exploited/)][[New ‘Powerful’ iOS Attack Warning Issued To Millions Of ...](https://www.forbes.com/sites/kateoflahertyuk/2026/03/07/new-powerful-ios-attack-warning-issued-to-millions-of-iphone-users/)]

### Web & API Security

No directly relevant web application security news articles were found today. However, several critical CVEs related to JWT and OAuth highlight ongoing threats to web and API authentication mechanisms. These include vulnerabilities ranging from mass assignment leading to full server compromise by overwriting JWT secrets, to various JWT forgery and algorithm confusion attacks, OIDC discovery poisoning via `X-Forwarded-Host` headers, and OAuth2 scope bypasses. These underscore the importance of rigorous testing of token handling, authentication flows, and third-party authentication integrations.

### AI/LLM Security

No recent news specifically on AI/LLM security was found today.

### Today's Action Items

1.  **Prioritize Patching for Mobile Devices:** Immediately check for and apply the latest security updates for Android and iOS devices, especially for Chrome browsers, given the critical sandbox escape and RCE vulnerabilities reported.
2.  **Audit JWT/OAuth Implementations:** Conduct a thorough review of JWT and OAuth implementations for vulnerabilities such as:
    *   Weak secret management (e.g., mass assignment of `JWT_SECRET`).
    *   Insufficient validation of OIDC discovery endpoints, particularly handling of `X-Forwarded-Host` headers.
    *   JWT algorithm confusion attacks.
    *   Improper claims validation (e.g., `aud`, `exp`, `nbf`, `nonce`) during token processing, even after signature verification.
    *   Bypasses of OAuth2 scope enforcement.
3.  **Test for Race Conditions and Information Disclosure:** Include tests for TOCTOU race conditions and sensitive information disclosure in mobile application penetration tests, as seen in recent Android vulnerabilities.
4.  **Verify Trust Chain Validation:** If using libraries like wolfSSL with OpenSSL compatibility, ensure that X.509 certificate trust-chain validation is robust and cannot be bypassed by untrusted intermediate certificates.