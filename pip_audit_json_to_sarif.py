#!/usr/bin/env python3
import json, sys, hashlib, datetime, pathlib

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def make_rule(advisory):
    rule_id = advisory.get("id") or advisory.get("advisory_id") or "UNKNOWN"
    return {
        "id": rule_id,
        "name": rule_id,
        "shortDescription": {"text": advisory.get("id") or "Vulnerability"},
        "fullDescription": {"text": advisory.get("description") or "No description"},
        "help": {
            "text": advisory.get("description") or "",
            "markdown": advisory.get("description") or ""
        }
    }

def make_result(pkg, advisory):
    rule_id = advisory.get("id") or advisory.get("advisory_id") or "UNKNOWN"
    loc = {
        "physicalLocation": {
            "artifactLocation": {"uri": "requirements.txt"},
            "region": {"startLine": 1}
        }
    }
    message = f"{pkg['name']} {pkg['version']} vulnerable: {rule_id}. Fix versions: {', '.join(advisory.get('fix_versions', []) or ['(none)'])}"
    fingerprint = hashlib.sha256(
        f"{pkg['name']}|{pkg['version']}|{rule_id}".encode()
    ).hexdigest()
    return {
        "ruleId": rule_id,
        "level": "error",
        "message": {"text": message},
        "locations": [loc],
        "fingerprints": {"issueInstance": fingerprint}
    }

def main(inp, outp):
    data = load(inp)
    vulns = data.get("vulnerabilities", [])
    rules = {}
    results = []
    for v in vulns:
        pkg = v.get("dependency", {}).get("package", {}) or v.get("package", {})
        advisory = v.get("advisory", v)
        if not pkg:
            continue
        rule_id = advisory.get("id") or advisory.get("advisory_id") or "UNKNOWN"
        if rule_id not in rules:
            rules[rule_id] = make_rule(advisory)
        results.append(make_result({"name": pkg.get("name"), "version": v.get("dependency", {}).get("version") or v.get("version")}, advisory))

    sarif = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "pip-audit",
                    "informationUri": "https://github.com/pypa/pip-audit",
                    "rules": list(rules.values())
                }
            },
            "invocations": [{
                "executionSuccessful": True,
                "endTimeUtc": datetime.datetime.utcnow().isoformat() + "Z"
            }],
            "results": results
        }]
    }
    pathlib.Path(outp).write_text(json.dumps(sarif, indent=2), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pip_audit_json_to_sarif.py pip-audit.json pip-audit.sarif", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
