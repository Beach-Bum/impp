#!/usr/bin/env python3
"""Generate a trust report for a memory artifact.

Usage:
    python run_trust_report.py --artifact-hash <hash>
"""

import argparse

from amm.registry.db import init_db, get_trust_score, get_verifications, get_artifact
from amm.registry.trust import format_trust_report


def main():
    parser = argparse.ArgumentParser(description="Generate trust report for an artifact")
    parser.add_argument("--artifact-hash", required=True, help="Hash of the artifact")
    parser.add_argument("--db", type=str, default=None, help="Registry DB path")

    args = parser.parse_args()
    conn = init_db(args.db)

    # Check artifact exists
    artifact = get_artifact(conn, args.artifact_hash)
    if not artifact:
        print(f"No artifact found with hash: {args.artifact_hash}")
        conn.close()
        return

    trust = get_trust_score(conn, args.artifact_hash)
    if not trust:
        print(f"No trust data for artifact: {args.artifact_hash}")
        print(f"  Domain: {artifact['domain']}")
        print(f"  Created: {artifact['created_at'][:10]}")
        print("  (No verifications have been run yet)")
        conn.close()
        return

    verifications = get_verifications(conn, args.artifact_hash)
    report = format_trust_report(trust, verifications)
    print(report)

    conn.close()


if __name__ == "__main__":
    main()
