"""HTML landing page for the enterprise application fleet."""

from __future__ import annotations

from collections import defaultdict
from html import escape
from urllib.parse import urlsplit, urlunsplit

from fastapi import Request

from .catalog import AppScenario

REPOSITORY_URL = "https://github.com/KrishnaDistributedcomputing/SREAgentEnterpriseShowcase"

PORTFOLIOS = {
    "retail-checkout": "Commerce and retail",
    "inventory-service": "Commerce and retail",
    "order-fulfillment": "Commerce and retail",
    "payments-api": "Financial services",
    "banking-ledger": "Financial services",
    "claims-processing": "Financial services",
    "patient-scheduling": "Customer experience",
    "airline-reservation": "Customer experience",
    "media-streaming": "Customer experience",
    "logistics-tracking": "Industrial and data",
    "iot-ingestion": "Industrial and data",
    "data-pipeline": "Industrial and data",
    "identity-access": "Digital platforms",
    "collaboration-api": "Digital platforms",
    "ai-inference-gateway": "Digital platforms",
}

SRE_AGENT_VALUE = {
    "retail-checkout": "Correlates checkout failures with payment dependency traces and revenue impact.",
    "inventory-service": "Separates application health from database failure and tracks reservation impact.",
    "order-fulfillment": "Connects dispatch errors to revisions, queue context, and safe rollback evidence.",
    "payments-api": "Finds authorization latency across processor traces, revisions, and SLO signals.",
    "banking-ledger": "Uses readiness evidence to isolate unhealthy revisions without accessing ledger data.",
    "claims-processing": "Diagnoses document dependency loss while preserving regulated-data boundaries.",
    "patient-scheduling": "Links calendar latency to patient access impact without exposing patient records.",
    "airline-reservation": "Correlates reservation errors with seat inventory and deployment context.",
    "media-streaming": "Explains playback delay through request duration, revisions, and CDN dependencies.",
    "logistics-tracking": "Connects stale shipment updates to event-stream dependency failures.",
    "iot-ingestion": "Correlates ingestion errors with device stream and active revision evidence.",
    "data-pipeline": "Identifies warehouse dependency failure and downstream data-freshness impact.",
    "identity-access": "Uses readiness and revision state to explain broad access disruption safely.",
    "collaboration-api": "Traces broker latency without reading customer or employee message content.",
    "ai-inference-gateway": "Correlates model endpoint loss with provider, policy, and cost boundaries.",
}

PORTFOLIO_ORDER = [
    "Commerce and retail",
    "Financial services",
    "Customer experience",
    "Industrial and data",
    "Digital platforms",
]


def _application_url(request: Request, current_slug: str, target_slug: str) -> str:
    parsed = urlsplit(str(request.base_url))
    scheme = "https" if parsed.hostname and parsed.hostname.endswith(".azurecontainerapps.io") else parsed.scheme
    expected_prefix = f"ca-{current_slug}-"
    if parsed.hostname and parsed.hostname.startswith(expected_prefix):
        target_host = f"ca-{target_slug}-{parsed.hostname.removeprefix(expected_prefix)}"
        if parsed.port:
            target_host = f"{target_host}:{parsed.port}"
        return urlunsplit((scheme, target_host, "/", "", ""))
    return urlunsplit((scheme, parsed.netloc, "/", "", ""))


def _render_rows(
    request: Request,
    current_slug: str,
    scenarios: list[AppScenario],
) -> str:
    grouped: dict[str, list[AppScenario]] = defaultdict(list)
    for scenario in scenarios:
        grouped[PORTFOLIOS[scenario.slug]].append(scenario)

    sections: list[str] = []
    number = 1
    for portfolio in PORTFOLIO_ORDER:
        rows: list[str] = []
        for scenario in sorted(grouped[portfolio], key=lambda item: item.name):
            application_url = _application_url(request, current_slug, scenario.slug)
            runbook_url = f"{REPOSITORY_URL}/blob/main/{scenario.runbook}"
            rows.append(
                f"""
                <tr>
                  <td data-label="#">
                    <span class="row-number">{number:02d}</span>
                  </td>
                  <td data-label="Application">
                    <div class="app-name">{escape(scenario.name)}</div>
                    <div class="domain">{escape(scenario.domain)}</div>
                  </td>
                  <td data-label="SLO">
                    <div class="slo">{scenario.slo_availability:.2f}%</div>
                    <div class="slo-detail">&lt; {scenario.slo_latency_ms} ms</div>
                  </td>
                  <td data-label="Incident">
                    <span class="fault fault-{escape(scenario.default_fault)}">
                      {escape(scenario.default_fault.replace("-", " "))}
                    </span>
                    <div class="dependency">{escape(scenario.dependency)}</div>
                  </td>
                  <td data-label="How SRE Agent helps" class="value-cell">
                    {escape(SRE_AGENT_VALUE[scenario.slug])}
                  </td>
                  <td data-label="Links">
                    <div class="actions">
                      <a class="action primary" href="{escape(application_url)}">Open app</a>
                      <a class="action" href="{escape(application_url)}docs">API</a>
                      <a class="action" href="{escape(runbook_url)}">Runbook</a>
                    </div>
                  </td>
                </tr>
                """
            )
            number += 1
        sections.append(
            f"""
            <tbody>
              <tr class="portfolio-row">
                <th colspan="6">
                  <span>{escape(portfolio)}</span>
                  <small>{len(rows)} applications</small>
                </th>
              </tr>
              {"".join(rows)}
            </tbody>
            """
        )
    return "".join(sections)


def render_landing_page(
    request: Request,
    current_scenario: AppScenario,
    scenarios: list[AppScenario],
) -> str:
    """Render the fleet landing page."""
    table_rows = _render_rows(request, current_scenario.slug, scenarios)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Fifteen live enterprise workloads for Azure SRE Agent.">
  <title>Azure SRE Agent Enterprise Showcase</title>
  <style>
    :root {{
      --ink: #162b2a;
      --muted: #5d6f6d;
      --paper: #f7f5ee;
      --surface: rgba(255, 255, 255, 0.82);
      --line: rgba(22, 43, 42, 0.12);
      --brand: #0b6b61;
      --brand-dark: #064b45;
      --accent: #d78a32;
      --shadow: 0 1px 2px rgba(10, 75, 69, 0.05), 0 18px 50px rgba(10, 75, 69, 0.10);
      color-scheme: light;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 9% 8%, rgba(215, 138, 50, 0.16), transparent 27rem),
        radial-gradient(circle at 91% 4%, rgba(11, 107, 97, 0.15), transparent 32rem),
        linear-gradient(180deg, #fbfaf6 0%, var(--paper) 100%);
      font-family: "Segoe UI", Inter, Arial, sans-serif;
      line-height: 1.55;
      min-height: 100vh;
    }}
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      opacity: 0.025;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    }}
    .shell {{ width: min(1480px, calc(100% - 40px)); margin: 0 auto; padding: 32px 0 72px; }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 24px;
      margin-bottom: 76px;
    }}
    .brand {{ display: flex; align-items: center; gap: 12px; font-weight: 700; letter-spacing: -0.02em; }}
    .brand-mark {{
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      border-radius: 12px;
      color: white;
      background: var(--brand);
      box-shadow: 0 8px 24px rgba(11, 107, 97, 0.24);
    }}
    .status {{ display: flex; align-items: center; gap: 9px; color: var(--muted); font-size: 0.875rem; }}
    .status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #37a26c; box-shadow: 0 0 0 5px rgba(55, 162, 108, 0.12); }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1.45fr) minmax(280px, 0.55fr);
      gap: 64px;
      align-items: end;
      margin-bottom: 52px;
    }}
    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--brand);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    h1 {{
      max-width: 870px;
      margin: 16px 0 20px;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(3rem, 6vw, 6.7rem);
      line-height: 0.95;
      letter-spacing: -0.055em;
      font-weight: 500;
    }}
    .lede {{ max-width: 740px; margin: 0; color: var(--muted); font-size: clamp(1rem, 1.6vw, 1.25rem); line-height: 1.7; }}
    .metric-card {{
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--surface);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }}
    .metric-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }}
    .metric strong {{ display: block; font-family: Georgia, serif; font-size: 2.25rem; font-weight: 500; letter-spacing: -0.04em; }}
    .metric span {{ color: var(--muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; }}
    .flow {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin: 0 0 28px;
      color: var(--muted);
      font-size: 0.82rem;
    }}
    .flow span {{ padding: 8px 12px; border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,.55); }}
    .flow b {{ color: var(--accent); }}
    .table-frame {{
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--surface);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }}
    table {{ width: 100%; border-collapse: collapse; }}
    thead th {{
      padding: 16px 18px;
      color: var(--muted);
      background: rgba(11, 107, 97, 0.045);
      border-bottom: 1px solid var(--line);
      font-size: 0.72rem;
      letter-spacing: 0.1em;
      text-align: left;
      text-transform: uppercase;
    }}
    tbody td {{ padding: 18px; border-bottom: 1px solid var(--line); vertical-align: top; font-size: 0.9rem; }}
    tbody:last-child tr:last-child td {{ border-bottom: 0; }}
    .portfolio-row th {{ padding: 16px 18px; color: var(--brand-dark); background: rgba(11, 107, 97, 0.075); text-align: left; }}
    .portfolio-row th span {{ font-family: Georgia, serif; font-size: 1.1rem; font-weight: 600; }}
    .portfolio-row small {{ margin-left: 10px; color: var(--muted); font-weight: 500; }}
    .row-number {{ color: var(--accent); font-family: Georgia, serif; font-size: 1.15rem; }}
    .app-name {{ font-weight: 750; letter-spacing: -0.02em; white-space: nowrap; }}
    .domain, .slo-detail, .dependency {{ margin-top: 4px; color: var(--muted); font-size: 0.78rem; }}
    .slo {{ color: var(--brand-dark); font-weight: 800; }}
    .fault {{ display: inline-flex; padding: 4px 9px; border-radius: 999px; background: #f4e8d8; color: #7f4b17; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; }}
    .fault-not-ready {{ background: #e9e2f4; color: #60447b; }}
    .fault-error {{ background: #f4dddd; color: #873c3c; }}
    .value-cell {{ max-width: 380px; color: #405351; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 7px; min-width: 190px; }}
    .action {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 7px 10px;
      border: 1px solid var(--line);
      border-radius: 9px;
      color: var(--brand-dark);
      background: rgba(255,255,255,.7);
      font-size: 0.75rem;
      font-weight: 750;
      text-decoration: none;
      transition: transform 180ms cubic-bezier(.2,.8,.2,1), opacity 180ms ease;
    }}
    .action.primary {{ color: white; background: var(--brand); border-color: var(--brand); }}
    .action:hover {{ transform: translateY(-2px); }}
    .action:active {{ transform: translateY(0) scale(.97); }}
    .action:focus-visible {{ outline: 3px solid rgba(215, 138, 50, .45); outline-offset: 2px; }}
    footer {{ display: flex; justify-content: space-between; gap: 24px; margin-top: 30px; color: var(--muted); font-size: 0.8rem; }}
    footer a {{ color: var(--brand); font-weight: 700; text-underline-offset: 3px; }}
    @media (max-width: 900px) {{
      .shell {{ width: min(100% - 24px, 1480px); padding-top: 20px; }}
      header {{ align-items: flex-start; margin-bottom: 40px; }}
      .brand {{ max-width: 150px; font-size: .95rem; }}
      .brand-mark {{ flex: 0 0 38px; }}
      .status {{ max-width: 150px; align-items: flex-start; font-size: .76rem; }}
      .status-dot {{ flex: 0 0 8px; margin-top: 5px; }}
      .hero {{ grid-template-columns: 1fr; gap: 20px; margin-bottom: 32px; }}
      h1 {{ margin-top: 12px; font-size: clamp(2.7rem, 12vw, 4rem); }}
      .lede {{ font-size: .98rem; line-height: 1.6; }}
      .metric-card {{ padding: 20px; border-radius: 20px; }}
      .metric-grid {{ gap: 14px; }}
      .metric strong {{ font-size: 1.8rem; }}
      .metric span {{ font-size: .66rem; }}
      .flow {{ gap: 4px; margin-bottom: 18px; font-size: .72rem; }}
      .flow span {{ padding: 6px 8px; }}
      .table-frame {{ overflow: visible; border: 0; background: transparent; box-shadow: none; }}
      table, tbody, tr, td {{ display: block; width: 100%; }}
      thead {{ display: none; }}
      tbody {{ margin-bottom: 24px; border: 1px solid var(--line); border-radius: 20px; overflow: hidden; background: var(--surface); box-shadow: var(--shadow); }}
      tbody td {{ display: grid; grid-template-columns: 120px 1fr; gap: 16px; padding: 14px 18px; }}
      tbody td::before {{ content: attr(data-label); color: var(--muted); font-size: .7rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }}
      .portfolio-row th {{ display: flex; justify-content: space-between; }}
      .value-cell {{ max-width: none; }}
      .actions {{ min-width: 0; }}
      footer {{ flex-direction: column; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .action {{ transition: none; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div class="brand">
        <span class="brand-mark" aria-hidden="true">S</span>
        <span>SRE Agent Showcase</span>
      </div>
      <div class="status"><span class="status-dot"></span>15 services deployed in West US 2</div>
    </header>
    <section class="hero">
      <div>
        <div class="eyebrow">Enterprise reliability portfolio</div>
        <h1>From alert to evidence to action.</h1>
        <p class="lede">
          Fifteen observable workloads show how Azure SRE Agent correlates telemetry,
          source, Azure resources, and runbooks before proposing a governed recovery.
        </p>
      </div>
      <aside class="metric-card" aria-label="Showcase metrics">
        <div class="metric-grid">
          <div class="metric"><strong>15</strong><span>Applications</span></div>
          <div class="metric"><strong>5</strong><span>Portfolios</span></div>
          <div class="metric"><strong>4</strong><span>Fault modes</span></div>
          <div class="metric"><strong>100%</strong><span>Runbook coverage</span></div>
        </div>
      </aside>
    </section>
    <div class="flow" aria-label="SRE Agent workflow">
      <span>Detect</span><b>→</b><span>Correlate</span><b>→</b><span>Diagnose</span><b>→</b>
      <span>Approve</span><b>→</b><span>Recover</span><b>→</b><span>Verify</span>
    </div>
    <section class="table-frame" aria-label="Application catalog">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Application</th>
            <th>SLO</th>
            <th>Incident</th>
            <th>How SRE Agent helps</th>
            <th>Explore</th>
          </tr>
        </thead>
        {table_rows}
      </table>
    </section>
    <footer>
      <span>Fault injection is disabled on the public deployment. Applications scale to zero.</span>
      <a href="{REPOSITORY_URL}">View specifications and source on GitHub</a>
    </footer>
  </main>
</body>
</html>"""
