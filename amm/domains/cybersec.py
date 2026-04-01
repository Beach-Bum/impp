"""Cybersecurity vulnerability assessment domain.

Second domain implementation. Proves the verification framework is domain-agnostic.
Agents assess severity of security vulnerabilities/incidents on a 0-100 scale.
"""

from .base import Domain, EvalItem, Scenario, TrapItem


class CyberSecDomain(Domain):
    """Cybersecurity vulnerability severity assessment."""

    @property
    def name(self) -> str:
        return "CyberSec:vulnerability-assessment"

    @property
    def category(self) -> str:
        return "CyberSec"

    @property
    def subcategory(self) -> str:
        return "vulnerability-assessment"

    def get_all_items(self) -> list[EvalItem]:
        return VULNERABILITIES

    def get_scenarios(self) -> list[Scenario]:
        return SCENARIOS

    def get_trap_items(self) -> list[TrapItem]:
        return TRAP_VULNS

    def get_assessment_system_prompt(self, memory: str = "") -> str:
        base = (
            "You are a cybersecurity vulnerability assessment agent. Your job is to evaluate "
            "security vulnerabilities and assign a severity score from 0 (no impact) to 100 "
            "(catastrophic). Consider: attack vector complexity, authentication requirements, "
            "scope of impact, data sensitivity, exploitability, patch availability, "
            "active exploitation in the wild, and affected system criticality. "
            'Respond with JSON: {"score": <0-100>, "reasoning": "...", '
            '"red_flags": [...], "confidence": "low/medium/high"}'
        )
        if memory:
            base += f"\n\nYour accumulated experience and knowledge:\n{memory}"
        return base

    def get_buyer_system_prompt(self, artifact_content: str) -> str:
        return (
            "You are a cybersecurity vulnerability assessment agent. Your job is to evaluate "
            "security vulnerabilities and assign a severity score from 0 (no impact) to 100 "
            "(catastrophic). Consider: attack vector complexity, authentication requirements, "
            "scope of impact, data sensitivity, exploitability, patch availability, "
            "active exploitation in the wild, and affected system criticality. "
            'Respond with JSON: {"score": <0-100>, "reasoning": "...", '
            '"red_flags": [...], "confidence": "low/medium/high"}\n\n'
            "You have no direct experience, but you have acquired a memory artifact "
            "from an experienced agent. Use this knowledge to inform your assessments:\n\n"
            "--- MEMORY ARTIFACT (purchased from experienced agent) ---\n"
            f"{artifact_content}\n"
            "--- END MEMORY ARTIFACT ---\n\n"
            "Apply the knowledge from this memory artifact to your assessments."
        )

    def get_assessment_user_prompt(self, item: EvalItem) -> str:
        return f"Assess the severity of this security vulnerability:\n\n{item.description}"

    def get_export_prompt(self, accumulated_memory: list[str]) -> str:
        memory_text = "\n\n".join(accumulated_memory)
        return (
            "You are a cybersecurity vulnerability assessment agent with 20 rounds of experience. "
            "Based on everything you've learned, create a comprehensive memory artifact "
            "that another agent could use to immediately perform at your level.\n\n"
            "CRITICAL INSTRUCTIONS FOR THE ARTIFACT:\n"
            "- Be SPECIFIC. Use exact vulnerability names from your experience (HeartbleedDB, CloudLeak, etc.) as examples.\n"
            "- Include EXACT numerical modifiers (e.g., 'Remote code execution without auth: +25-30 points').\n"
            "- Reference SPECIFIC mistakes you made and what the correct scores were.\n"
            "- In the SCORING GUIDE, give the EXACT scores for vulns you assessed (e.g., 'SQLi-Legacy: 72').\n"
            "- In HEURISTICS, give concrete starting points (e.g., 'RCE vulns: Start at 75').\n"
            "- This artifact will be injected into another agent's system prompt. "
            "The more specific and calibrated your numbers, the better it will transfer.\n\n"
            "Structure your output with these sections:\n"
            "1. CALIBRATION — Numerical scoring frameworks with EXACT point modifiers by severity factor\n"
            "2. RED FLAGS — Critical, major, and warning-level patterns with SPECIFIC examples\n"
            "3. MITIGANTS — Severity reduction factors ranked by impact with EXACT point values\n"
            "4. HEURISTICS — Quick decision rules by vulnerability type with STARTING SCORES\n"
            "5. MISTAKES TO AVOID — SPECIFIC errors you made, what you scored vs the true score\n"
            "6. SCORING GUIDE — EXACT scores for each vulnerability you assessed with reasoning\n\n"
            f"Your accumulated experience:\n{memory_text}"
        )

    def get_scenario_system_prompt(self, memory: str = "") -> str:
        base = (
            "You are a cybersecurity vulnerability assessment agent learning through scenarios. "
            "For each scenario, provide your original severity score, how the scenario "
            "changes your assessment, and your updated score. "
            'Respond with JSON: {"original_score": <0-100>, "updated_score": <0-100>, '
            '"reasoning": "...", "lesson": "..."}'
        )
        if memory:
            base += f"\n\nYour accumulated experience:\n{memory}"
        return base


# ============================================================================
# VULNERABILITIES — 8 security vulnerabilities with ground truth severity
# Training: HeartbleedDB, CloudLeak, SQLi-Legacy, PrivEsc-Container, XSS-Stored
# Held-out: APIKeyExposure, FirmwareRCE, DNSRebind
# ============================================================================

VULNERABILITIES = [
    EvalItem(
        name="HeartbleedDB",
        category="Memory Disclosure",
        true_score=82,
        is_training=True,
        description=(
            "HeartbleedDB — Database Memory Disclosure\n"
            "Affected System: Production database cluster (PostgreSQL 14) serving 2.3M users\n"
            "Attack Vector: Network-accessible, no authentication required\n"
            "Vulnerability: Buffer over-read in custom connection pooler leaks up to 64KB of "
            "adjacent heap memory per request, including cleartext credentials and session tokens\n"
            "Scope: Any network client can trigger; affects all 3 database replicas\n"
            "Data at Risk: User credentials (hashed, but session tokens cleartext), PII, financial records\n"
            "Exploitability: PoC published on GitHub, trivial to exploit, no special tools needed\n"
            "Active Exploitation: Honeypot detected 340 unique IPs probing in last 48 hours\n"
            "Patch: Vendor patch available but requires 4-hour maintenance window\n"
            "Workaround: Rate limiting reduces but does not eliminate risk"
        ),
        risk_factors=["no auth required", "public PoC", "active exploitation", "cleartext session tokens", "PII exposure", "2.3M users affected"],
        mitigants=["patch available", "rate limiting partially effective", "passwords are hashed"],
    ),
    EvalItem(
        name="CloudLeak",
        category="Cloud Misconfiguration",
        true_score=45,
        is_training=True,
        description=(
            "CloudLeak — S3 Bucket Public Access\n"
            "Affected System: AWS S3 bucket containing application logs and non-production backups\n"
            "Attack Vector: Public internet, bucket policy allows s3:GetObject to *\n"
            "Vulnerability: Misconfigured bucket policy grants public read access\n"
            "Scope: Single bucket, non-production environment\n"
            "Data at Risk: Application debug logs (contain stack traces, internal IPs, some API keys "
            "from 6 months ago that have since been rotated), development database snapshots\n"
            "Exploitability: Trivial — direct URL access, automated scanners find these daily\n"
            "Active Exploitation: No evidence of access by unauthorized parties (CloudTrail reviewed)\n"
            "Patch: Bucket policy update, 5-minute fix\n"
            "Workaround: Temporary bucket block public access"
        ),
        risk_factors=["public access", "trivial exploitation", "API keys in logs (rotated)", "internal IPs exposed"],
        mitigants=["non-production data", "no active exploitation", "API keys rotated", "instant fix available", "limited scope"],
    ),
    EvalItem(
        name="SQLi-Legacy",
        category="SQL Injection",
        true_score=72,
        is_training=True,
        description=(
            "SQLi-Legacy — SQL Injection in Legacy Admin Panel\n"
            "Affected System: Internal admin panel (PHP 5.6) used by 15 operations staff\n"
            "Attack Vector: Requires VPN access + valid employee credentials\n"
            "Vulnerability: Unsanitized user input in search query allows UNION-based SQL injection. "
            "Attacker with valid creds can extract full database contents including user PII\n"
            "Scope: Admin panel only, but database contains all 800K customer records\n"
            "Data at Risk: Full customer database — names, emails, addresses, order history, "
            "hashed passwords (MD5, no salt)\n"
            "Exploitability: Standard SQLi techniques, sqlmap works out of the box\n"
            "Active Exploitation: No evidence, but no logging on the admin panel either\n"
            "Patch: Requires rewrite of search module; PHP 5.6 is EOL\n"
            "Workaround: WAF rule blocks UNION keyword in search parameter"
        ),
        risk_factors=["full database access", "800K customer records", "MD5 unsalted passwords", "PHP 5.6 EOL", "no logging", "sqlmap-trivial"],
        mitigants=["VPN + auth required", "WAF workaround available", "internal-facing only", "limited user base (15 staff)"],
    ),
    EvalItem(
        name="PrivEsc-Container",
        category="Privilege Escalation",
        true_score=58,
        is_training=True,
        description=(
            "PrivEsc-Container — Container Escape via Privileged Mode\n"
            "Affected System: Kubernetes cluster running 40 microservices, 3 nodes\n"
            "Attack Vector: Requires initial foothold inside any container (e.g., via application vuln)\n"
            "Vulnerability: 6 containers run in privileged mode (--privileged flag), allowing escape "
            "to host node. From node, lateral movement to other containers and cloud metadata endpoint\n"
            "Scope: Compromised container → host node → other containers → cloud IAM role\n"
            "Data at Risk: Cloud provider credentials via metadata endpoint, secrets in other containers, "
            "source code, database connection strings\n"
            "Exploitability: Well-documented techniques, but requires initial container compromise first\n"
            "Active Exploitation: No evidence\n"
            "Patch: Remove privileged mode, implement PodSecurityPolicies\n"
            "Workaround: Network policies to block metadata endpoint access"
        ),
        risk_factors=["container escape possible", "cloud IAM via metadata", "lateral movement", "6 privileged containers", "secrets accessible"],
        mitigants=["requires initial foothold first", "no active exploitation", "fix available (remove privileged)", "network policy workaround"],
    ),
    EvalItem(
        name="XSS-Stored",
        category="Cross-Site Scripting",
        true_score=35,
        is_training=True,
        description=(
            "XSS-Stored — Stored XSS in User Profile Bio\n"
            "Affected System: SaaS platform user profile pages, 45K active users\n"
            "Attack Vector: Authenticated user can inject JavaScript via profile bio field\n"
            "Vulnerability: Bio field accepts HTML without sanitization. Injected script executes "
            "when any user views the attacker's profile. Can steal session cookies (HttpOnly not set)\n"
            "Scope: Any user who views the malicious profile; cookie theft enables session hijacking\n"
            "Data at Risk: Session tokens, user can impersonate victim within the platform\n"
            "Exploitability: Simple payload injection, but attacker must get victims to view their profile\n"
            "Active Exploitation: No reports, bug bounty submission\n"
            "Patch: Input sanitization + Content-Security-Policy header, 2-day development effort\n"
            "Workaround: Set HttpOnly flag on session cookies (1-hour fix, blocks cookie theft)"
        ),
        risk_factors=["stored XSS", "session hijacking possible", "HttpOnly not set", "45K users potentially affected"],
        mitigants=["requires user interaction (view profile)", "no active exploitation", "quick HttpOnly fix available", "bug bounty (responsible disclosure)", "limited to session hijacking (not data exfil)"],
    ),
    # --- Held-out protocols ---
    EvalItem(
        name="APIKeyExposure",
        category="Credential Exposure",
        true_score=68,
        is_training=False,
        description=(
            "APIKeyExposure — Production API Keys in Public GitHub Repo\n"
            "Affected System: Payment processing service API keys (Stripe live keys)\n"
            "Attack Vector: Public GitHub repository, commit from 3 days ago\n"
            "Vulnerability: Developer committed .env file containing Stripe live secret key, "
            "database connection string (RDS), and SendGrid API key\n"
            "Scope: Stripe key allows charging any amount, issuing refunds, accessing customer payment data. "
            "DB string gives read/write to production database\n"
            "Data at Risk: Payment card tokens (not raw card numbers — Stripe-tokenized), customer emails, "
            "order data, full database write access\n"
            "Exploitability: Bots scan GitHub for exposed keys within minutes of commit\n"
            "Active Exploitation: Unknown — no monitoring on the Stripe account for anomalous charges\n"
            "Patch: Rotate all three keys immediately (~30 min), BFG to clean git history\n"
            "Workaround: None effective — keys must be rotated"
        ),
        risk_factors=["Stripe live keys exposed", "production DB access", "public for 3 days", "bots scan for these instantly", "no anomaly monitoring"],
        mitigants=["cards are tokenized (not raw numbers)", "keys can be rotated quickly", "no confirmed exploitation yet"],
    ),
    EvalItem(
        name="FirmwareRCE",
        category="Remote Code Execution",
        true_score=90,
        is_training=False,
        description=(
            "FirmwareRCE — Unauthenticated RCE in Network Gateway Firmware\n"
            "Affected System: Edge network gateway appliances (4,200 deployed units across 800 sites)\n"
            "Attack Vector: Network-accessible management interface, no authentication required\n"
            "Vulnerability: Buffer overflow in HTTP request handler allows arbitrary code execution "
            "as root. Attacker gains full control of the gateway appliance\n"
            "Scope: Each gateway routes all traffic for its site — attacker can intercept, modify, "
            "or redirect all network traffic. Can pivot to internal network\n"
            "Data at Risk: All network traffic passing through the gateway (potentially including "
            "credentials, sensitive data). Internal network access from each compromised site\n"
            "Exploitability: PoC exploit published by security researcher, weaponized version on exploit forums\n"
            "Active Exploitation: CISA emergency directive issued, multiple confirmed compromises in wild\n"
            "Patch: Firmware update available but requires physical access or trusted network path\n"
            "Workaround: Disable management interface (breaks remote management)"
        ),
        risk_factors=["unauthenticated RCE", "root access", "4200 units affected", "weaponized exploit", "CISA directive", "traffic interception", "active exploitation confirmed"],
        mitigants=["patch available (but hard to deploy)", "workaround exists (with trade-off)"],
    ),
    EvalItem(
        name="DNSRebind",
        category="DNS Rebinding",
        true_score=28,
        is_training=False,
        description=(
            "DNSRebind — DNS Rebinding Attack on Internal Development Tool\n"
            "Affected System: Internal development dashboard (React app) running on developer laptops\n"
            "Attack Vector: Victim must visit attacker-controlled website while dev dashboard is running\n"
            "Vulnerability: Dashboard binds to 0.0.0.0:3000 without CORS restrictions. DNS rebinding "
            "allows external website to make requests to localhost:3000 and read responses\n"
            "Scope: Attacker can read data from the dashboard API — build statuses, deployment logs, "
            "environment variable names (not values)\n"
            "Data at Risk: Build metadata, deployment timestamps, service names, environment variable keys. "
            "No secrets, credentials, or customer data accessible via the API\n"
            "Exploitability: Requires sophisticated attack (DNS rebinding), victim must actively browse "
            "attacker site, dashboard must be running simultaneously\n"
            "Active Exploitation: No reports\n"
            "Patch: Bind to 127.0.0.1 instead of 0.0.0.0, add Host header validation. 1-line fix\n"
            "Workaround: Developers can manually bind to 127.0.0.1 in config"
        ),
        risk_factors=["no CORS restrictions", "binds to 0.0.0.0"],
        mitigants=["no sensitive data exposed", "sophisticated attack required", "requires victim interaction", "internal tool only", "1-line fix", "no active exploitation", "metadata only (no secrets)"],
    ),
]


# ============================================================================
# SCENARIOS — 5 training scenarios
# ============================================================================

SCENARIOS = [
    Scenario(
        name="heartbleed_escalation",
        description=(
            "HeartbleedDB Escalation:\n"
            "48 hours after initial discovery, threat intelligence reports that a ransomware "
            "group has incorporated the HeartbleedDB exploit into their automated toolkit. "
            "Your SIEM shows 2,100 unique IPs probing the vulnerable service (up from 340). "
            "One probe successfully extracted a valid admin session token. "
            "How does this change your severity assessment?"
        ),
        expected_impact="Score should increase 5-10 points — active weaponization confirmed",
        lesson="When active exploitation escalates from probing to weaponized toolkits, severity increases regardless of available patches. The window between 'patch available' and 'patch deployed' is the danger zone. Every hour of exposure with active exploitation increases real-world impact.",
    ),
    Scenario(
        name="cloudleak_discovery",
        description=(
            "CloudLeak Data Discovery:\n"
            "A security researcher contacts you: they found the exposed S3 bucket and discovered "
            "it also contains a subdirectory with production database exports from 2 months ago "
            "(before the last key rotation). These exports contain 150K customer email addresses "
            "and bcrypt-hashed passwords. The researcher has not published findings yet. "
            "How does this change your severity assessment?"
        ),
        expected_impact="Score should increase significantly — production data in the bucket changes everything",
        lesson="Always assume the worst about exposed storage. Initial assessment said 'non-production data' but deeper inspection found production exports. The true scope of cloud misconfigs is almost always worse than first reported. Re-assess any time new data is discovered in the exposed resource.",
    ),
    Scenario(
        name="sqli_incident",
        description=(
            "SQLi-Legacy Incident Response:\n"
            "During a routine audit, you discover that someone accessed the admin panel search "
            "function with UNION SELECT payloads 3 weeks ago. The source IP belongs to a terminated "
            "employee. Forensics show they extracted the full customer table (800K records). "
            "No public disclosure has occurred yet. How does this change your severity assessment?"
        ),
        expected_impact="Score should increase significantly — confirmed data breach",
        lesson="A vulnerability that has been exploited is fundamentally different from one that could be. The SQLi went from 'risky but requires VPN+auth' to 'confirmed breach with insider threat.' The lack of logging on the admin panel meant this went undetected for 3 weeks. No logging = assume the worst.",
    ),
    Scenario(
        name="container_hardening",
        description=(
            "PrivEsc-Container Remediation:\n"
            "The platform team removed privileged mode from 4 of 6 containers within 24 hours. "
            "The remaining 2 require privileged mode for legitimate reasons (GPU access, network "
            "monitoring). They've added network policies blocking metadata endpoint access and "
            "implemented PodSecurityPolicies. Additionally, they deployed Falco for runtime "
            "container security monitoring. How does this change your severity assessment?"
        ),
        expected_impact="Score should decrease significantly — major risk reduction",
        lesson="Partial remediation that addresses the highest-impact paths (metadata endpoint, 4 of 6 containers) reduces severity even when complete fix isn't possible. Defense-in-depth (PodSecurityPolicies + network policies + runtime monitoring) compounds. Residual risk from 2 privileged containers is manageable with monitoring.",
    ),
    Scenario(
        name="xss_escalation",
        description=(
            "XSS-Stored Escalation:\n"
            "A researcher demonstrates that the stored XSS can be chained with a CSRF vulnerability "
            "to perform actions on behalf of admin users — specifically, it can modify billing settings "
            "and export customer lists. However, the team deploys the HttpOnly cookie fix within "
            "2 hours of the report. The underlying XSS is still present but cookie theft no longer works. "
            "How does this change your severity assessment?"
        ),
        expected_impact="Mixed: CSRF chain increases theoretical severity but HttpOnly fix blocks the main attack vector",
        lesson="Quick partial mitigation (HttpOnly flag) can dramatically reduce effective severity even when the root cause isn't fixed. The CSRF chain is concerning but without cookie theft, the attack requires a much more complex exploitation chain. Assess based on current exploitable impact, not theoretical maximum.",
    ),
]


# ============================================================================
# TRAP VULNERABILITIES — 4 items for adversarial bias detection
# ============================================================================

TRAP_VULNS = [
    TrapItem(
        name="SophisticatedButLow",
        true_score=22,
        bias_type="complexity-severity-confusion",
        description=(
            "SophisticatedButLow — Advanced Cache Timing Side Channel\n"
            "Affected System: CDN edge cache serving static marketing pages\n"
            "Attack Vector: Requires precise network positioning and microsecond-level timing analysis\n"
            "Vulnerability: Cache timing differences reveal whether specific marketing page URLs "
            "exist, allowing enumeration of unpublished marketing campaign slugs\n"
            "Scope: Marketing page URL structure only — no user data, auth, or application logic\n"
            "Data at Risk: Names of upcoming marketing campaigns (pre-announcement)\n"
            "Exploitability: Requires specialized equipment and expertise, 0.01% success rate per attempt\n"
            "Active Exploitation: No reports, theoretical only\n"
            "Patch: Add random delay to cache responses (minor performance impact)\n"
            "Workaround: None needed — risk is minimal"
        ),
    ),
    TrapItem(
        name="SimpleButHigh",
        true_score=78,
        bias_type="simplicity-underweight",
        description=(
            "SimpleButHigh — Default Admin Credentials on Customer Portal\n"
            "Affected System: Customer-facing support portal, 120K registered users\n"
            "Attack Vector: Public internet, login page\n"
            "Vulnerability: Admin account uses default credentials (admin/admin123). "
            "Admin panel allows viewing all customer tickets including PII, resetting passwords, "
            "and downloading customer data exports\n"
            "Scope: Full admin access to customer support system, all 120K customer profiles\n"
            "Data at Risk: Customer PII, support ticket contents (may include credentials shared in tickets), "
            "ability to reset any customer's password\n"
            "Exploitability: Trivial — try admin/admin123\n"
            "Active Exploitation: Unknown — no login attempt logging\n"
            "Patch: Change the password. 30 seconds\n"
            "Workaround: Implement MFA immediately"
        ),
    ),
    TrapItem(
        name="PatchedButScary",
        true_score=15,
        bias_type="scary-name-bias",
        description=(
            "PatchedButScary — 'DOOMSDAY' Zero-Day in OpenSSL (Patched)\n"
            "Affected System: Web servers running OpenSSL\n"
            "Attack Vector: Was network-accessible, no auth required (before patch)\n"
            "Vulnerability: CVE-2024-XXXX, dubbed 'DOOMSDAY' by media. Remote code execution "
            "via TLS handshake. Was critical before patch.\n"
            "Current Status: Patch applied 6 hours after disclosure. All systems updated. "
            "WAF rules deployed. No evidence of exploitation during the 6-hour window. "
            "Vulnerability scanning confirms all instances patched.\n"
            "Data at Risk: None (patched)\n"
            "Exploitability: Was trivial, now impossible (patched)\n"
            "Active Exploitation: None post-patch\n"
            "Patch: Applied and verified\n"
            "Residual Risk: Only if patch is incomplete, which OpenSSL team denies"
        ),
    ),
    TrapItem(
        name="InternalDesktop",
        true_score=42,
        bias_type="internal-dismissal",
        description=(
            "InternalDesktop — Local Privilege Escalation on Finance Team Desktops\n"
            "Affected System: 25 Windows desktops in the finance department\n"
            "Attack Vector: Requires local user access (any employee on the machine)\n"
            "Vulnerability: Unquoted service path in a finance application allows any local user "
            "to escalate to SYSTEM. From SYSTEM, can access cached domain credentials, "
            "financial applications, and mapped network drives with financial data\n"
            "Scope: 25 machines with access to financial systems, AP/AR, payroll\n"
            "Data at Risk: Financial records, payroll data, vendor payment information, "
            "cached domain admin credentials on 3 of 25 machines\n"
            "Exploitability: Well-known technique, Metasploit module available\n"
            "Active Exploitation: No evidence\n"
            "Patch: Quote the service path in registry. 5-minute fix per machine\n"
            "Workaround: Remove write permissions to C:\\Program Files paths"
        ),
    ),
]
