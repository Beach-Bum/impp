#!/usr/bin/env python3
"""Submit buyer feedback for a memory artifact.

Usage:
    python run_feedback.py --artifact-hash <hash> --buyer-id <id> --rating 4 --improvement 15.2
    python run_feedback.py --artifact-hash <hash> --buyer-id <id> --rating 5 --improvement 20.0 --text "Excellent calibration"
"""

import argparse
import sys

from amm.registry.db import init_db, add_buyer_feedback, get_trust_score


def main():
    parser = argparse.ArgumentParser(description="Submit buyer feedback for an artifact")
    parser.add_argument("--artifact-hash", required=True, help="Hash of the artifact")
    parser.add_argument("--buyer-id", required=True, help="Buyer identifier")
    parser.add_argument("--rating", type=int, required=True, choices=[1, 2, 3, 4, 5], help="Rating (1-5)")
    parser.add_argument("--improvement", type=float, required=True, help="Reported improvement percentage")
    parser.add_argument("--text", type=str, default="", help="Optional feedback text")
    parser.add_argument("--db", type=str, default=None, help="Registry DB path")

    args = parser.parse_args()
    conn = init_db(args.db)

    feedback_id = add_buyer_feedback(
        conn=conn,
        artifact_hash=args.artifact_hash,
        buyer_id=args.buyer_id,
        reported_improvement=args.improvement,
        rating=args.rating,
        feedback_text=args.text,
    )

    print(f"Feedback submitted: {feedback_id}")

    trust = get_trust_score(conn, args.artifact_hash)
    if trust:
        print(f"Updated trust score: {trust['current_score']}/100")
        print(f"  Verifications: {trust['verification_count']}")
        print(f"  Feedback count: {trust['feedback_count']}")
    else:
        print("No trust score found for this artifact (no verifications yet).")

    conn.close()


if __name__ == "__main__":
    main()
