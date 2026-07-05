# Secure Coding Standards

Please adhere to the following secure coding standards when developing and maintaining this agent:

- **API Keys**: Always load API keys and other sensitive credentials from environment variables. Never hardcode them in the codebase.
- **Input Validation**: Always validate and sanitize all inputs before passing them to external APIs or processing them.
- **Sensitive Data Logging**: Never log sensitive data such as API keys, credentials, or CVE details to plain text files.
