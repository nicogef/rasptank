# File: bandit_json_to_sarif.py
#!/usr/bin/env python3
import json, sys, hashlib, datetime, pathlib
from datetime import datetime, UTC

SEV_TO_LEVEL = {
    "HIGH": "error",
    "MEDIUM": "warning",
    "LOW": "note"
}

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main(inp, outp):
    data = load(inp)
    results_raw = data.get("results", [])
    rules = {}
    sarif_results = []

    for r in results_raw:
        test_id = r.get("test_id", "UNKNOWN")
        if test_id not in rules:
            rules[test_id] = {
                "id": test_id,
                "name": r.get("test_name") or test_id,
                "shortDescription": {"text": r.get("issue_text", "")[:120]},
                "fullDescription": {"text": r.get("issue_text", "")},
                "help": {
                    "text": r.get("more_info", ""),
                    "markdown": r.get("more_info", "")
                },
                "properties": {
                    "problem.severity": r.get("issue_severity"),
                    "confidence": r.get("issue_confidence")
                }
            }

        level = SEV_TO_LEVEL.get(r.get("issue_severity", "").upper(), "warning")
        fingerprint = hashlib.sha256(
            f"{r.get('filename')}|{r.get('line_number')}|{test_id}".encode()
        ).hexdigest()

        sarif_results.append({
            "ruleId": test_id,
            "level": level,
            "message": {"text": r.get("issue_text", "")},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": r.get("filename")},
                    "region": {
                        "startLine": r.get("line_number", 1),
                        "endLine": r.get("line_number", 1)
                    }
                }
            }],
            "fingerprints": {"issueInstance": fingerprint}
        })

    sarif = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "bandit",
                    "informationUri": "https://bandit.readthedocs.io/",
                    "rules": list(rules.values())
                }
            },
            "invocations": [{
                "executionSuccessful": True,
                "endTimeUtc": datetime.now(UTC).isoformat().replace("+00:00", "Z")
            }],
            "results": sarif_results
        }]
    }
    pathlib.Path(outp).write_text(json.dumps(sarif, indent=2), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: bandit_json_to_sarif.py bandit.json bandit.sarif", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
