"""Builds MBC-wm-ai_Tool_Spec.pdf — spec + critique of the West Monroe AI-Native Enterprise Agent."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

OUT = "MBC-wm-ai_Tool_Spec.pdf"
NAVY = colors.HexColor("#14213D")
ACCENT = colors.HexColor("#E4572E")
GREY = colors.HexColor("#5C6370")
LIGHT = colors.HexColor("#F2F4F7")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=NAVY, fontSize=18, spaceBefore=6, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=NAVY, fontSize=13, spaceBefore=12, spaceAfter=6)
H3 = ParagraphStyle("H3", parent=ss["Heading3"], textColor=ACCENT, fontSize=11, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("Body", parent=ss["BodyText"], fontSize=9.8, leading=13.5, spaceAfter=5)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.5, leading=11, textColor=GREY)
CELL = ParagraphStyle("Cell", parent=BODY, fontSize=8.8, leading=11.5, spaceAfter=0, alignment=TA_LEFT)
CELLB = ParagraphStyle("CellB", parent=CELL, fontName="Helvetica-Bold")
TITLE = ParagraphStyle("Title", parent=H1, fontSize=24, leading=29, spaceAfter=4)


def p(t, s=BODY):
    return Paragraph(t, s)


def bullets(items, style=BODY):
    return ListFlowable([ListItem(p(i, style), leftIndent=12) for i in items],
                        bulletType="bullet", start="•", leftIndent=12, bulletFontSize=8)


def table(rows, widths, header=True):
    data = [[p(c, CELLB if (header and r == 0) else CELL) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9CED6")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
        data[0] = [Paragraph(c.text, ParagraphStyle("hdr", parent=CELLB, textColor=colors.white)) for c in data[0]]
        t = Table(data, colWidths=widths, repeatRows=1)
    for r in range(1 if header else 0, len(rows)):
        if r % 2 == 0:
            st.append(("BACKGROUND", (0, r), (-1, r), LIGHT))
    t.setStyle(TableStyle(st))
    return t


def footer(c, d):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(GREY)
    c.drawString(0.75 * inch, 0.5 * inch, "MBC x West Monroe — AI-Native Enterprise Agent revamp | Working draft, internal")
    c.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch, f"Page {d.page}")
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(0.75 * inch, LETTER[1] - 0.55 * inch, LETTER[0] - 0.75 * inch, LETTER[1] - 0.55 * inch)
    c.restoreState()


W = LETTER[0] - 1.5 * inch
s = []

# ---------- Cover / summary ----------
s += [Spacer(1, 6),
      p("AI-Native Enterprise Agent", TITLE),
      p("Current-state specification &amp; improvement opportunities", ParagraphStyle("sub", parent=H2, textColor=ACCENT, spaceBefore=0)),
      p("Project: MBC-wm-ai &nbsp;|&nbsp; Role: Tech Lead (Graham Pilkington) &nbsp;|&nbsp; Date: 23 Sep 2026 &nbsp;|&nbsp; Status: Draft v0.2 (hands-on tested)", SMALL),
      p("Subject: <font color='#E4572E'>https://agents.westmonroe.ai/ai-native-enterprise-agent/</font>", SMALL),
      Spacer(1, 10)]

s += [p("1. Executive summary", H2),
      p("The AI-Native Enterprise Agent is a public, West Monroe-branded web tool that turns the firm's annual "
        "<i>Building the AI-Native Enterprise</i> research into a company-specific executive brief. A visitor enters a "
        "company name or website, confirms which organization was matched, optionally overrides the industry, and "
        "receives a generated brief that ranks six enterprise-AI trends by their likely 24-month impact on that company, "
        "maps them across six business pressures, and lists opportunities, threats, actions and supporting evidence. "
        "The brief can be downloaded as a PDF in exchange for name and email, making the tool a thought-leadership "
        "asset <b>and</b> a lead-generation funnel."),
      p("Hands-on testing (Section 4) shows it works end-to-end in about 30 seconds and tailors the story to each company. "
        "But it is a <b>one-shot, thin-evidence report generator</b>. It reads only about three pages of the company's own "
        "website, and its company matching can pick the wrong entity. When that happens, the tool still writes a confident "
        "brief about the wrong thing. The revamp "
        "opportunity is to move it from a static readout toward an interactive, evidence-grounded, client-specific "
        "advisory agent — with the scoring, sourcing and lead-handoff made transparent and defensible."),
      p("<b>Method note:</b> this spec was produced by reviewing the live site's UI copy, public front-end bundle and "
        "API calls on 23 Sep 2026, then by running the tool end to end for two companies (Ameren, Chipotle) and "
        "inspecting the returned JSON. The PDF export was not completed because it requires entering personal contact "
        "details. Items marked <i>(inferred)</i> still need confirming with West Monroe once we have repo/backend access.", SMALL)]

# ---------- What it does ----------
s += [p("2. What the tool does", H2),
      p("2.1 Purpose &amp; audience", H3),
      bullets(["<b>Audience:</b> executives and strategy leads at prospective West Monroe clients; also consultants prepping for meetings.",
               "<b>Value to user:</b> a fast, personalized read on how enterprise-AI trends affect their company in the next 24 months.",
               "<b>Value to West Monroe:</b> distributes the annual research, demonstrates AI capability, and captures qualified leads (HubSpot)."]),
      p("2.2 Research framework (the 'knowledge base')", H3),
      p("The research content is hard-coded in the front-end as six trend objects: the report's three imperatives plus "
        "three shared pressures. Each carries a thesis, horizon, a baseline pressure score, opportunity tags, risk tags "
        "and source facts from the report. In testing, the model re-ranks the six trends for each company. The horizons "
        "never changed, and the brief shows High / Medium / Watch labels rather than numeric scores."),
      table([["ID", "Trend", "Category", "Horizon", "Base score"],
             ["ai-operating-layer", "AI becomes the operating layer", "Imperative 01 — AI as the new operating layer", "0-6 mo", "96"],
             ["ai-roi-divide", "The AI ROI divide widens", "Imperative 02 — Bridging the AI ROI divide", "0-6 mo", "94"],
             ["org-chart-rewrite", "Work is rebuilt around human-agent teams", "Imperative 03 — Rewriting the org chart", "6-12 mo", "90"],
             ["pace-of-change", "The pace of change compresses decisions", "Shared pressure", "0-6 mo", "86"],
             ["regulation-sovereignty-risk", "Regulation and sovereignty shape where AI can run", "Shared pressure", "6-12 mo", "84"],
             ["trust-capacity", "Trust and capacity become business constraints", "Shared pressure", "12-24 mo", "82"]],
            [1.35 * inch, 1.85 * inch, 1.95 * inch, 0.6 * inch, 0.55 * inch]),
      Spacer(1, 6),
      p("Every trend is then pressure-tested against six business lenses: <b>Growth, Operations, Risk, Workforce, "
        "Customer, Compliance</b>."),
      p("2.3 Output — the executive brief", H3),
      table([["#", "Section", "Content"],
             ["01", "Understand the company", "Public posture, source boundary (what public data was used), and what needs validation."],
             ["02", "Read the AI pressure", "Ranked 24-month enterprise-AI impact board: which imperatives/pressures force the most change."],
             ["03", "Pressure-test implications", "Full-pressure coverage across the six lenses; opportunity and threat stories; driver-specific actions."],
             ["04", "Use the evidence", "Evidence appendix (sources, confidence) and what leadership should validate before acting."]],
            [0.35 * inch, 1.6 * inch, 4.35 * inch])]

# ---------- How it works ----------
s += [p("3. How it works", H2),
      p("3.1 User flow", H3),
      table([["Step", "User action", "System behavior"],
             ["1. Find the company", "Types a company name or URL; clicks <i>Find organization</i>.", "POST <font face='Courier'>/api/resolve-company</font> returns a best match plus alternative candidates."],
             ["2. Review alternatives", "Confirms the match or picks an alternative; optional <i>Industry override</i> (e.g. 'regional bank').", "Up to 3 candidates, each with name, URL, industry and a 'Strong match' label. The best match is pre-selected. "
               "<b>Tested:</b> 'Ameren' gave two duplicates of the same company; 'Chipotle' gave a company called <i>'Contact US'</i> in the <i>Technology</i> industry."],
             ["3. Generate brief", "Clicks <i>Generate the executive brief</i>.", "POST <font face='Courier'>/api/trend-impact</font> starts an async run and returns a <font face='Courier'>runId</font>. Client polls <font face='Courier'>GET /api/trend-impact/{runId}</font> with back-off (1.5s growing x1.2 up to 5s) until <i>succeeded</i> or <i>failed</i>. The UI shows 3 named stages (review company, rank pressure, write read). <b>Tested: ~31 s per brief.</b>"],
             ["4. Read on screen", "Scrolls the rendered brief.", "React renders a ~31 KB result JSON as a ~20k-character brief. It is fully visible on screen <i>without</i> any email gate."],
             ["5. Download PDF", "Enters first name, last name, email.", "POST <font face='Courier'>/api/captures</font> stores the lead (session cookie); POST <font face='Courier'>/api/readout-pdf</font> sends report JSON + an HTML print snapshot of the page and returns a download URL."]],
            [1.15 * inch, 2.0 * inch, 3.15 * inch]),
      p("3.2 Architecture (observed)", H3),
      bullets(["<b>Front end:</b> React SPA using Vike (vite-plugin-ssr) client routing; IBM Plex type; served from "
               "<font face='Courier'>agents.westmonroe.ai/ai-native-enterprise-agent</font>. Runtime config via <font face='Courier'>app-config.js</font> "
               "(APP_HOST, APP_FRONTEND_PATH, APP_BACKEND_PATH).",
               "<b>Back end:</b> JSON REST API under <font face='Courier'>/api</font> — resolve-company, trend-impact (async job + status), "
               "captures, captures/current, readout-pdf. Errors return <font face='Courier'>{error, issues[]}</font> (schema-validation style, likely Zod). <i>(inferred)</i>",
               "<b>AI layer (confirmed):</b> the result reports <font face='Courier'>mode: \"openai\"</font>. The backend fetches about 3 pages "
               "(roughly 2,000-2,500 words) from the company's own website, adds the bundled West Monroe research facts, and asks the "
               "model to rank each of the six trends once. The model's own notes say it was told to avoid numeric scores.",
               "<b>PDF:</b> server-side render of a client-provided HTML snapshot (elements marked <font face='Courier'>data-pdf-hidden</font> removed).",
               "<b>Martech:</b> HubSpot (forms, analytics, banners), Google Tag Manager / GA4, OneTrust cookie consent."]),
      p("3.3 Core data model (simplified)", H3),
      p("<font face='Courier' size='8.5'>Candidate { companyName, companyUrl, industry, sourceTitle, sourceDescription, matchStrength, reason }<br/>"
        "TrendImpactRun { runId, status, submittedAt, startedAt, completedAt, error?, result? }<br/>"
        "Result { companyProfile, rankedImpacts[6], opportunities[], threats[], recommendedActions[], "
        "sourceHandling[], caveats[], sourceAppendix, mode, generatedAt }<br/>"
        "CompanyProfile { companyName, companyUrl, industry, industryBasis, industryPosture, summary, strengths[], watchouts[] }<br/>"
        "RankedImpact { trendId, name, category, priority: High|Medium|Watch, confidence, horizon, whyItMatters, "
        "priorityRationale, twentyFourMonthImplication, detailedImpact[5], nowActions[4], futureActions[3], "
        "opportunities[3], threats[3], sourceFacts[], sourceImplications[] }<br/>"
        "SourceAppendix { sourceStatus, officialUrl, fetchedAt, pageCount, wordCount, sourcePages[], sourceUrls[], modelNotes[], trendBase[] }<br/>"
        "Capture { firstName, lastName, email }  -&gt;  HubSpot</font>", SMALL)]

# ---------- Test results ----------
s += [KeepTogether([p("4. Hands-on test results (23 Sep 2026)", H2),
      table([["", "Test A: 'Ameren'", "Test B: 'Chipotle'"],
             ["Company match", "Correct (Ameren, Energy &amp; Utilities), but 2 'Strong match' candidates were the same company on different domains.",
              "<b>Wrong.</b> Default pick was 'Contact US' (chipotle.com/contact-us) labelled <b>Technology</b>. The only restaurant-classified option was the jobs site."],
             ["Run time", "31.1 s", "30.8 s"],
             ["Sources used", "3 pages of ameren.com, 2,525 words (home, sustainability policy, EV for business)", "3 pages of chipotle.com, 2,004 words (contact-us, sustainability, transparency)"],
             ["Ranking", "1 Operating layer, 2 ROI divide, 3 Regulation, 4 Org chart, 5 Pace, 6 Trust",
              "1 ROI divide, 2 Trust, 3 Operating layer, 4 Pace, 5 Regulation, 6 Org chart ('Watch')"],
             ["Output quality", "Specific and credible for a utility: outage response, crew routing, rate recovery.",
              "Titled 'Contact US' throughout, framed as a customer-support 'surface', not a restaurant chain. Still marked 'source-backed'."]],
            [1.1 * inch, 2.6 * inch, 2.6 * inch])]),
      Spacer(1, 6),
      p("<b>Takeaways:</b> the model tailors the story and re-orders the trends for each company, which is good. But the output "
        "can only be as good as the company match and a very small source set. There is no check that the matched page is "
        "really the company, so a bad match is invisible to the reader. Both runs also mis-report the industry source as "
        "<font face='Courier'>industryBasis: \"override\"</font> even though no override was entered. Each summary list "
        "(opportunities, threats) repeats one item word-for-word from the trend-level lists.")]

# ---------- Flaws ----------
s += [p("5. Flaws &amp; risks (brief)", H2),
      table([["Area", "Issue", "Why it matters"],
             ["<b>Company resolution</b>", "Treats web page titles as company names ('Contact US'), guesses the industry from the page, and shows duplicate or sub-site candidates, all labelled 'Strong match'.", "<b>Highest risk:</b> a polished brief about the wrong entity damages West Monroe's credibility on first use."],
             ["<b>Thin evidence</b>", "Only ~3 pages and ~2k words from the company's own site. No filings, news, earnings calls, job postings or analyst data.", "Shallow and self-promotional inputs. It cannot see AI maturity, strategy shifts or competitive position."],
             ["Opaque ranking", "The LLM ranks the trends freely and is told to avoid numbers. There is no rubric, and horizons are fixed per trend.", "'Why is this #1?' has no defensible answer, and rankings may not be repeatable between runs."],
             ["No quality gate", "Marked 'source-backed' even when the source is a contact page. Industry basis is mis-reported, and summary items are duplicated.", "Errors reach the reader unflagged, which creates brand and legal exposure about named companies."],
             ["Public data only", "No way to add internal context, docs or interview input.", "Shallow for private or mid-market firms; misses the real operating picture."],
             ["One-shot, static", "No follow-up questions, drill-down, what-if, or edit/regenerate of a section; no saved history.", "Low engagement after first read; no reason to return."],
             ["Wait time", "~31 s with 3 static stage cards. Uses polling with no timeout, no streamed partial results, and no caching of repeat companies.", "Acceptable today, but gets worse as sources grow. The same cost is paid for every run."],
             ["Lead gate placement", "The full brief is readable on screen with no email. Name and email are only asked for at PDF export, and the lead carries little context (role, interest, top trend).", "Low-quality leads and missed routing to the right West Monroe partner."],
             ["Research hard-coded", "Trend content lives in the client JS bundle.", "Annual refresh needs a redeploy; no versioning of which research edition produced a brief."],
             ["Abuse / cost", "Public, unauthenticated endpoints that trigger LLM runs; no visible rate limiting or CAPTCHA.", "Cost blow-ups and scraping; also lets anyone generate a brief on any named company."],
             ["PDF pipeline", "Server renders HTML supplied by the client.", "Fragile formatting and a potential injection surface if not sanitized server-side."],
             ["Accessibility / mobile", "Dense multi-stage layout; heavy third-party scripts.", "Slower load and weaker experience on mobile, where many execs first open links."]],
            [1.2 * inch, 2.65 * inch, 2.45 * inch])]

# ---------- Improvements ----------
s += [p("6. Recommended improvements", H2),
      p("5.1 Product", H3),
      bullets(["<b>Fix company resolution first:</b> resolve to a canonical entity using a company database or knowledge graph "
               "(legal name, ticker, domain, NAICS code). Collapse duplicate domains, reject page-title names, and show a clear "
               "'is this the right company?' check with a logo and HQ.",
               "<b>Richer evidence:</b> add filings (10-K), earnings transcripts, news, job postings and tech-stack signals, "
               "each with a date and cited inline.",
               "<b>Dynamic, explainable scoring:</b> compute per-company scores from explicit signals (industry, size, AI maturity, "
               "regulatory exposure, recent news) and show a 'why this rank' breakdown per trend and lens.",
               "<b>Conversational follow-up:</b> after the brief, let users ask questions, drill into a lens, or run what-ifs "
               "('we're moving to a new ERP', 'assume EU AI Act scope').",
               "<b>Bring-your-own-context:</b> optional upload (strategy deck, 10-K, org chart) or a short guided intake "
               "(5-7 questions on AI maturity and priorities) to go beyond public data.",
               "<b>Peer benchmarking:</b> position the company against the Enterprise AI Transformation Index cohort (leader vs laggard).",
               "<b>Actionable next steps:</b> convert actions into a 30/60/90-day roadmap with owners and KPIs; offer 'book a session' with the relevant practice."]),
      p("5.2 Trust &amp; quality", H3),
      bullets(["Inline citations on every company-specific claim, with source date and link; flag unsupported statements.",
               "Grounding/verification pass (second model or rules) before render; confidence per section, not just overall.",
               "Automatic checks: block a 'source-backed' label when sources are thin or off-topic, dedupe summary lists, and record the industry source correctly.",
               "Eval suite of reference companies with golden outputs; track score variance and factual accuracy per release."]),
      p("5.3 Platform &amp; engineering", H3),
      bullets(["Move trend/research content to a versioned CMS or config service; stamp every brief with research edition and model version.",
               "Stream progress (SSE) with named stages — 'resolving company', 'gathering sources', 'scoring', 'writing' — plus timeouts and retry.",
               "Cache briefs per company + edition to cut cost and latency; add rate limiting, bot protection and per-IP quotas.",
               "Generate the PDF from the structured report JSON with a server-side template (not a client HTML snapshot).",
               "Enrich the HubSpot lead with company, top-ranked trend, role and engagement data for partner routing; add consent-aware analytics."]),
      KeepTogether([p("5.4 Suggested phasing", H3),
      table([["Phase", "Scope", "Outcome"],
             ["0 — Discovery (2-3 wks)", "Access to repo, prompts, logs, lead data; stakeholder interviews; baseline evals.", "Confirmed current-state architecture and prioritized backlog."],
             ["1 — Foundations", "Canonical company resolution, versioned research store, streaming status, caching, rate limits, JSON-driven PDF.", "Faster, cheaper, safer; unblocks later work."],
             ["2 — Credible output", "Explainable dynamic scoring, inline citations, verification pass, eval harness.", "Briefs that differ meaningfully by company and can be defended."],
             ["3 — Interactive agent", "Follow-up chat, BYO context, benchmarking, roadmap generation, richer lead handoff.", "From one-off report to a reusable advisory tool."]],
            [1.45 * inch, 2.9 * inch, 1.95 * inch])]),
      Spacer(1, 8),
      p("7. Open questions for kickoff", H2),
      bullets(["Which OpenAI model(s), crawler logic and prompts does the current backend use, and what are per-brief cost and latency?",
               "What are current funnel metrics: visits → briefs generated → PDFs downloaded → meetings booked?",
               "Is the goal primarily lead generation, client-delivery tooling for consultants, or both?",
               "What legal/brand guardrails apply to generating analysis about named third-party companies?",
               "Hosting, stack and security constraints for the rebuild (cloud, SSO for internal use, data residency)?"])]

doc = SimpleDocTemplate(OUT, pagesize=LETTER, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                        topMargin=0.8 * inch, bottomMargin=0.75 * inch,
                        title="AI-Native Enterprise Agent — Spec & Improvements", author="Graham Pilkington")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
