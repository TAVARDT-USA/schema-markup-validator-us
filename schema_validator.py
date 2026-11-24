#!/usr/bin/env python3
import sys
import re
import json
import ssl
import argparse
import urllib.request
import urllib.error

CORE_SCHEMA_PROPERTIES = {
    "Organization": ["name", "url"],
    "LocalBusiness": ["name", "address"],
    "WebSite": ["name", "url"],
    "Article": ["headline", "author"],
    "NewsArticle": ["headline", "author"],
    "BlogPosting": ["headline", "author"],
    "Product": ["name", "offers"],
    "BreadcrumbList": ["itemListElement"],
    "FAQPage": ["mainEntity"]
}

def validate_schema(target_url, timeout=8):
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url
    target_url = target_url.rstrip("/")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    results = {
        "target": target_url,
        "score": 100,
        "status": "PASS",
        "json_ld_blocks": 0,
        "entities": [],
        "microdata_detected": False,
        "issues": [],
        "recommendations": []
    }

    req = urllib.request.Request(target_url, headers={"User-Agent": "Mozilla/5.0 (TAVARDT-Schema-Auditor/1.0)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="ignore")

        # 1. JSON-LD extraction
        matches = re.findall(r'<script[^>]+type=["']application/ld\+json["'][^>]*>(.*?)</script>', body, re.DOTALL | re.IGNORECASE)
        results["json_ld_blocks"] = len(matches)

        if not matches:
            results["score"] -= 40
            results["issues"].append("Zero JSON-LD structured data blocks discovered in document body.")
            results["recommendations"].append("Deploy JSON-LD scripts to provide explicit semantic context for search crawlers.")
        else:
            for idx, raw in enumerate(matches):
                raw = raw.strip()
                try:
                    data = json.loads(raw)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        if isinstance(item, dict):
                            if "@graph" in item and isinstance(item["@graph"], list):
                                for sub in item["@graph"]:
                                    if isinstance(sub, dict):
                                        t = sub.get("@type", "Unknown")
                                        results["entities"].append(t)
                                        _validate_properties(t, sub, results)
                            else:
                                t = item.get("@type", "Unknown")
                                results["entities"].append(t)
                                _validate_properties(t, item, results)
                except Exception as je:
                    results["score"] -= 20
                    results["issues"].append(f"JSON-LD block #{idx+1} contains malformed JSON syntax: {str(je)[:70]}")
                    results["recommendations"].append(f"Fix JSON syntax parsing errors in block #{idx+1}.")

        # 2. Microdata detection
        if re.search(r'\bitemscope\b', body, re.I) and re.search(r'\bitemtype\b', body, re.I):
            results["microdata_detected"] = True

        if not results["entities"] and not results["microdata_detected"]:
            results["score"] = max(0, results["score"] - 30)
            results["issues"].append("No recognizable Schema.org entities identified in markup.")
            results["recommendations"].append("Implement essential semantic entities such as Organization, WebSite, or Article.")

    except Exception as e:
        results["score"] = 0
        results["issues"].append(f"Failed to fetch document: {str(e)}")
        results["recommendations"].append("Ensure target server is reachable and responds with HTTP 200.")

    results["score"] = max(0, min(100, results["score"]))
    if results["score"] >= 85:
        results["status"] = "OPTIMAL"
    elif results["score"] >= 65:
        results["status"] = "WARNING"
    else:
        results["status"] = "CRITICAL"

    return results

def _validate_properties(entity_type, entity_dict, results):
    if entity_type in CORE_SCHEMA_PROPERTIES:
        required = CORE_SCHEMA_PROPERTIES[entity_type]
        missing = [p for p in required if p not in entity_dict]
        if missing:
            results["score"] -= len(missing) * 5
            results["issues"].append(f"Entity '{entity_type}' is missing recommended property: {', '.join(missing)}")
            results["recommendations"].append(f"Add missing property '{', '.join(missing)}' to '{entity_type}' entity.")

def main():
    parser = argparse.ArgumentParser(description="TAVARDT USA - Structured Data Validator")
    parser.add_argument("target", help="Target domain or URL to validate")
    parser.add_argument("-json", "--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("-timeout", "--timeout", type=int, default=8, help="Request timeout in seconds")

    args = parser.parse_args()
    report = validate_schema(args.target, timeout=args.timeout)

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print("=" * 60)
    print(" " + "TAVARDT USA - Structured Data Validator")
    print("=" * 60)
    print(f"Target: {report['target']}")
    print(f"Semantic Quality Score: {report['score']}/100")
    print(f"Validation Status: {report['status']}")
    print(f"JSON-LD Blocks: {report['json_ld_blocks']}")
    print(f"Microdata Detected: {report['microdata_detected']}")
    print("-" * 60)

    print(f"\n[Identified Semantic Entities]:")
    if not report["entities"]:
        print("  - No entities detected.")
    else:
        for ent in report["entities"]:
            print(f"  * Schema Type: {ent}")

    print(f"\n[Syntax Errors and Validation Warnings]:")
    if not report["issues"]:
        print(f"  - No structured data errors or missing required fields found.")
    else:
        for iss in report["issues"]:
            print(f"  * {iss}")

    if report["recommendations"]:
        print(f"\n[Semantic Optimization Recommendations]:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")

    print("-" * 60)
    print(f"Full audit and online validation: https://tools.tavardt.com/schema-markup-validator/")
    print("=" * 60)

if __name__ == "__main__":
    main()
