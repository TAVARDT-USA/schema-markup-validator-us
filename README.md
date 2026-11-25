# Schema Markup and Structured Data Validator

[![Schema Validator](https://img.shields.io/badge/TAVARDT-Schema.org%20Validator-5b3cf5.svg)](https://tools.tavardt.com/schema-markup-validator/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Rigorous structured data validation engine for Schema.org JSON-LD and Microdata markup, verifying entity relationships, mandatory attribute completeness, and rich search feature eligibility.

The utility extracts semantic entity structures from live web properties to identify unparseable syntax, broken schemas, and omitted properties required by search crawlers and AI answer engines. Built with zero third-party dependencies, the validator executes natively in Python CLI environments and automated CI/CD pipelines.

***

## Semantic Validation Capabilities and Supported Entity Models

Search engines and neural retrieval pipelines rely on explicit structured data to disambiguate organizations, understand content authorship, and award rich results. Syntactic errors or missing required properties lead directly to schema disqualification and degraded visibility.

* **Automated Structured Data Extraction**: Parses all embedded JSON-LD (`application/ld+json`) blocks and detects legacy Microdata attributes (`itemscope`, `itemtype`) across the document.
* **Knowledge Graph Support**: Seamlessly traverses complex `@graph` nested arrays, resolving distributed entity relationships across modern web applications.
* **Core Schema.org Classification**: Validates required semantic properties across essential entity models: Organization, LocalBusiness, WebSite, Article, NewsArticle, BlogPosting, Product, BreadcrumbList, and FAQPage.
* **Syntax and Schema Integrity Checking**: Flags unparseable JSON blocks (-20 points), zero JSON-LD presence (-40 points), missing recognized entities (-30 points), and missing recommended properties (-5 points each).
* **Quantitative Semantic Quality Score**: Deductive 0 to 100 rating classifying target domains into OPTIMAL, WARNING, or CRITICAL status with prioritized remediation directives.

***

## Semantic Entity Inspection Matrix

<table>
  <thead>
    <tr>
      <th align="left">Entity Class</th>
      <th align="left">Mandatory Properties</th>
      <th align="left">Deduction Rule</th>
      <th align="left">Rich Result and Retrieval Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Organization</strong></td>
      <td><code>name</code>, <code>url</code></td>
      <td>-5 Pts per missing property</td>
      <td>Validates primary brand entity and canonical corporate presence in knowledge graphs.</td>
    </tr>
    <tr>
      <td><strong>LocalBusiness</strong></td>
      <td><code>name</code>, <code>address</code></td>
      <td>-5 Pts per missing property</td>
      <td>Essential for local pack rankings, geographic relevance, and map integration.</td>
    </tr>
    <tr>
      <td><strong>WebSite</strong></td>
      <td><code>name</code>, <code>url</code></td>
      <td>-5 Pts per missing property</td>
      <td>Enables sitelinks search box eligibility and establishes domain brand context.</td>
    </tr>
    <tr>
      <td><strong>Article / NewsArticle</strong></td>
      <td><code>headline</code>, <code>author</code></td>
      <td>-5 Pts per missing property</td>
      <td>Enables Google News, Top Stories carousel inclusion, and AI citation grounding.</td>
    </tr>
    <tr>
      <td><strong>BlogPosting</strong></td>
      <td><code>headline</code>, <code>author</code></td>
      <td>-5 Pts per missing property</td>
      <td>Attributes content authorship and publication dates for editorial content.</td>
    </tr>
    <tr>
      <td><strong>Product</strong></td>
      <td><code>name</code>, <code>offers</code></td>
      <td>-5 Pts per missing property</td>
      <td>Powers merchant rich snippets, price displays, and stock availability badges.</td>
    </tr>
    <tr>
      <td><strong>BreadcrumbList</strong></td>
      <td><code>itemListElement</code></td>
      <td>-5 Pts per missing property</td>
      <td>Builds navigational URL paths in SERPs, replacing raw URLs with breadcrumb trails.</td>
    </tr>
    <tr>
      <td><strong>FAQPage</strong></td>
      <td><code>mainEntity</code></td>
      <td>-5 Pts per missing property</td>
      <td>Generates collapsible question-and-answer rich snippets in organic search results.</td>
    </tr>
  </tbody>
</table>

***

## Installation and Quick Start

Requires Python 3.8 or higher utilizing strictly standard library modules (`sys`, `re`, `json`, `ssl`, `argparse`, `urllib.request`, `urllib.error`). Zero external packages or pip installations are required.

Clone the repository and validate a target web property:

```bash
git clone https://github.com/TAVARDT-USA/schema-markup-validator-us.git
cd schema-markup-validator-us
python schema_validator.py example.com
```

To export results in clean JSON format for automated pipelines:

```bash
python schema_validator.py example.com -j
```

Inspect target domains with a custom request timeout:

```bash
python schema_validator.py https://example.com -j -t 12
```

Sample JSON response payload:

```json
{
  "target": "https://example.com",
  "score": 95,
  "status": "OPTIMAL",
  "json_ld_blocks": 1,
  "entities": [
    "Organization",
    "WebSite"
  ],
  "microdata_detected": false,
  "issues": [
    "Entity 'Organization' is missing recommended property: url"
  ],
  "recommendations": [
    "Add missing property 'url' to 'Organization' entity."
  ]
}
```

Status classification scale:

* **Score 85 to 100 (OPTIMAL)**: High-quality structured data implementation with complete entity coverage and zero syntax errors.
* **Score 65 to 84 (WARNING)**: Minor property omissions or partial schema coverage that may restrict rich result eligibility.
* **Score 0 to 64 (CRITICAL)**: Broken JSON syntax, zero structured data blocks, or unparseable markup requiring immediate remediation.

***

## Frequently Asked Questions

### Why is JSON-LD preferred over Microdata for search engine rich results and LLM entity ingestion?
JSON-LD decouples structured data from presentation HTML, allowing developers to maintain clean, centralized scripts without altering visible markup. Furthermore, Google and leading AI crawlers recommend JSON-LD because it can be injected dynamically and parsed without DOM rendering overhead.

### How does the validator handle `@graph` arrays in complex JSON-LD markup?
When the validator encounters an `@graph` key, it automatically iterates through the array of sub-objects, extracting each nested entity type and subjecting it to property validation rules. This ensures interconnected schema nodes are thoroughly evaluated.

### What algorithmic scoring deductions occur when mandatory Schema.org properties are missing?
The tool deducts 40 points if zero JSON-LD blocks are found, 20 points per block containing invalid JSON syntax, and 30 points if no recognizable entities exist. Additionally, each missing recommended property on recognized entities deducts 5 points from the baseline score of 100.

### How does the script validate structured data without loading a full headless browser?
The engine performs direct HTTP GET requests with custom User-Agent headers, retrieving the raw HTML payload. It extracts script contents using optimized regular expressions and parses them with Python standard `json.loads`, completing full audits in sub-second execution windows.

### How can engineering teams incorporate the JSON validation output into automated CI/CD deployment gates?
By running `schema_validator.py` with the `-j` parameter, build runners can ingest the JSON payload into jq or CI test suites. Teams can configure pipeline gates that fail deployment builds if the `score` drops below 85 or if any syntax errors appear in the `issues` array.

***

## Semantic Architecture and Knowledge Graph Advisory

For advanced structured data engineering, knowledge graph integration, and compliance with W3C Semantic Web Standards in United States, contact **TAVARDT United States**.

***

## Useful Links

* **Corporate Portal:** https://ag.tavardt.com/
* **Diagnostic Suite:** https://tools.tavardt.com/
* **Technical Contact:** https://ag.tavardt.com/contact/

***

### License
Released under the MIT License.

***

© 2026 TAVARDT. All rights reserved.
