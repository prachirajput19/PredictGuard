# PredictGuard — Prototype (Team: Pirates Code, SIH26184)

## How to run it (Windows / PowerShell)

```powershell
cd path\to\project
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

It'll open at `http://localhost:8501`. **Log in** with the demo credentials
shown on screen: `investigator1` / `sih2026`.

## Enabling real notifications (optional, for a more impressive demo)

Open `config.py` and fill in real credentials to make notifications
actually fire instead of showing "skipped":

- **Email**: set `EMAIL_ENABLED = True`, add a Gmail address + an
  [App Password](https://myaccount.google.com/apppasswords) (not your
  normal Gmail password).
- **SMS**: set `SMS_ENABLED = True`, sign up for a free
  [Twilio trial account](https://www.twilio.com/try-twilio), verify your
  own phone number as the recipient, fill in the SID/token/numbers, then
  `pip install twilio`.
- **API webhook**: already enabled by default, pointed at
  `https://httpbin.org/post` (a free public echo endpoint) — this fires a
  real HTTP POST with no setup needed. Check the Audit Log tab to see the
  live response code.

None of these are required for the demo to work — without them, the audit
log will just show `"status": "skipped"` for that channel, which is an
honest and defensible state to show judges if asked ("production would use
live credentials; here's the exact code path that fires them").

## What's already working in this version

- Synthetic dataset of 300 complaints, each tagged with a **crime type**
  (UPI Fraud, Investment Scam, OTP Fraud, Loan App Fraud, Job Fraud)
- Mule-ring detection via graph community detection (Louvain)
- **Predicted risk heatmap** — a real Kernel Density Estimate (KDE)
  surface, weighted by ring risk score, toggleable against raw complaint
  points (Heatmap tab)
- **Full drill-down filtering** — by crime category, by location/city, and
  by time range, directly matching PS deliverable (b)'s wording
- **Mule-network graph view** — the actual node-edge structure of linked
  accounts and rings (Network tab)
- **Secure LEA login gate** — nothing else in the app renders until you log
  in, matching PS deliverable (c)'s "secure interface for investigators"
- **Per-alert Intelligence Report** — auto-generated summary (ring size,
  total amount, crime-type breakdown, recommended action) for each alert
- **Per-alert Evidence Documentation** — the underlying complaint records
  tied to that ring, viewable and downloadable as CSV
- **Real notification channels (Deliverable d)** — every alert fires actual
  email (SMTP), SMS (Twilio), and API webhook (HTTP POST) attempts, with
  honest sent/skipped/failed status logged into the audit ledger
- **Live ledger integrity verification + tamper demo** — "Verify Chain
  Integrity" checks the hash-chain; "Simulate Tampering" deliberately
  corrupts a past block so you can show the verification catching it live

## For the demo video

Best sequence for a strong 60-75 second walkthrough:

1. **Login screen** — show the secure login gate, log in as `investigator1`.
2. Start with the risk slider high (~0.9) — few/no alerts. Show the
   **crime category** and **location** filters narrowing the map live.
3. Lower the slider — watch the KDE-predicted hotspot surface intensify and
   alerts populate.
4. Switch to **Network** tab — show the actual mule-account graph.
5. Switch to **Alerts** — expand one alert's "Intelligence Report" and
   "Evidence Documentation," show the CSV download.
6. Switch to **Audit Log** — point out a notification entry showing real
   email/SMS/API attempt status, then click "Verify Chain Integrity"
   (green), then "Simulate Tampering (Demo)" and verify again to show it
   getting caught in red. This is your strongest closing moment for a
   Blockchain & Cybersecurity themed problem statement.

## Honest scope note (say this in the pitch, don't hide it)

Email/SMS fire for real if you add your own credentials to `config.py`;
without them they report "skipped," which is a real, honest system state —
not a mock. The API webhook fires for real against a public test endpoint
by default. If judges ask what's mocked vs. real: the prediction engine,
graph detection, KDE surface, audit ledger, and notification code paths
are all real; only the specific bank-side CFCFRMS integration and LEA
identity-provider SSO are out of scope for a hackathon build.

---

## Latest upgrade batch (added 4 Sept)

- **PDF Intelligence Report export** — alongside the CSV evidence download,
  each alert now has a "Download Intelligence Report (PDF)" button
  generating a polished, letterhead-style report (`pdf_report.py`) with
  ring summary, evidence table, and recommended action — deployment-grade,
  not just a raw data dump.
- **Command Center trend charts** — crime-category breakdown bar chart and
  complaint-volume-over-time line chart, both computed live from the actual
  dataset (not static images).
- **Mock Bank/CFCFRMS Response panel** (`bank_response.py`) — after an
  auto-freeze fires for a high-risk ring (risk >= 0.8), a simulated bank
  response (bank name, reference ID, amount held) now shows directly on
  the alert card in Priority Alerts, and appears as its own event type in
  the Audit Log.
- **Live-injected complaint highlighting** — after using Live Simulation,
  the newly injected account is gold-highlighted in the Network
  Intelligence graph, and its complaint point is gold-highlighted on the
  Predictive Hotspots map (Raw Complaint Points layer) — closes the loop
  visually so the "live pipeline" claim is visible everywhere, not just in
  a success message.

New dependency: `reportlab` (for PDF generation) — already added to
`requirements.txt`, run `pip install -r requirements.txt` after unzipping.

## UI polish pass (visual identity + motion)

No new dependencies, no structural changes — purely `ui_theme.py` plus small
additive tweaks in `dashboard.py`, `lea_interface.py`, and `live_injection.py`:

- **Space Grotesk + Inter** fonts (Google Fonts) replace the default
  Streamlit typeface everywhere.
- **Glassmorphic cards** (blurred, translucent) replace flat dark boxes for
  KPI cards, alert cards, and the ledger integrity panel.
- **Subtle radial gradient background** instead of flat black.
- **Custom thin dark scrollbar**.
- **Pulsing "LIVE" chip** next to the PredictGuard title and a pulsing
  status dot in the sidebar.
- **Animated count-up KPI cards** in the Command Center (0 → value on load).
- **Staggered fade/slide-in** on KPI cards and alert cards.
- **Hover elevation/glow** on all cards.
- **Pulsing glow on CRITICAL badges**.
- **Toast notifications** on login, alert status changes, chain verify/tamper,
  and live complaint injection.
- **Plotly transition animation** on the two Command Center trend charts.
- **"Injecting complaint..." spinner** in Live Simulation instead of an
  instant result.

Nothing here touches ring detection, KDE, the ledger, notifications, or any
other teammate's logic — only presentation.

### Updated demo sequence suggestion

Add these two beats to your existing walkthrough:
1. After showing Live Simulation inject a complaint, jump to **Network
   Intelligence** and point out the gold-highlighted new node, then to
   **Predictive Hotspots** and point out the gold marker on the map.
2. In **Priority Alerts**, for any CRITICAL alert, show the green
   "Bank/CFCFRMS Response Received" panel, then open the evidence expander
   and click "Download Intelligence Report (PDF)" on camera to show the
   actual generated PDF opening.
