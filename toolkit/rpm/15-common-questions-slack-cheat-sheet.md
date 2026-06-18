# Common Questions — Slack Cheat Sheet
> Use when: Quick reference for facilitators answering in Slack. Paste any of these as a starting point for your reply.

COMMON QUESTIONS — SLACK CHEAT SHEET

"How is RPM different from Sales Cloud?"
→ Sales Cloud is the CRM — accounts, opportunities, activity. RPM Apps are the planning layer that sit on top: how you carve territory, set quota, segment accounts, plan capacity, and forecast revenue. Most RPM customers also run a CRM; RPM doesn't replace it, it plans around it.

"Why does Segmentation feed both T&Q and Capacity?"
→ Because account tiering is the input to both. T&Q uses segmentation to weight territory carve and quota allocation. Capacity uses it to size coverage by tier. If segmentation changes, both downstream apps should re-run. That's by design — it's the same source of truth across the suite.

"What's the difference between Anaplan Prediction and the Forecaster?"
→ Anaplan Prediction is the broader ML platform — many algorithms, many use cases. The Forecaster in Sales Forecasting is one specific application of it, tuned for revenue forecasting with the algorithm panel you see in the Prediction Lab. Prediction is the engine; Forecaster is the app that wraps it for the sales-forecasting use case.

"Why doesn't Sales Forecasting have a configurator?"
→ Sales Forecasting ships as a template — the model structure is consistent across customers, so there's no per-implementation configurator step. You configure the inputs (hierarchies, data feeds) but not the model skeleton. T&Q is the opposite end: every customer needs a different carve, hence the 8-step configurator.

"Check My Work says my answer's wrong but I'm sure it's right"
→ Re-read the question first — Check My Work is strict about exact values. If you're still convinced, post in Slack with a screenshot of your work and the question. Sometimes the lab expects a specific format (number vs. percentage, comma vs. period). If it's a real lab bug, we want to know.

"CoModeler isn't giving me a useful answer"
→ Two things to check: (1) you're on a model-review page that has CoModeler enabled, not a regular lab page; (2) your prompt is concrete — "show me the module that calculates quota by territory" works better than "explain the model." If the answer is still off, paste your prompt in Slack — we're collecting examples.

"Do I need to do the app tracks in order?"
→ T&Q first is the natural path because Segmentation feeds into it, and Capacity uses both. Sales Forecasting is mostly independent and can go any time. If you want to start with Sales Forecasting because it's shorter, fine — you'll come back to the others.

"How long should each track take?"
→ Rough guide: T&Q is the longest (4–6 hours across the 8-step configurator), Segmentation and Capacity are 2–3 hours each, Sales Forecasting plus the Prediction Lab is 2–3 hours. Total ~12–15 hours of content spread across the week.

"My knowledge check score is below 70%"
→ Unlimited retakes. Review the questions you missed, go back to the relevant lab sections, retake. Open book — this is a learning checkpoint, not a gate.

"Where's the recording of the live kickoff?"
→ Posted in the Slack channel as a pinned message. Also available at [RECORDING URL].
