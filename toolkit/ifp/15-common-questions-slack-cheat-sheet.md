# Common Questions — Slack Cheat Sheet
> Use when: Quick reference for facilitators answering in Slack. Paste any of these as a starting point for your reply.

COMMON QUESTIONS — SLACK CHEAT SHEET

"Generation is taking forever"
→ 20–40 min is normal. Watch the /applications page, not the App Framework page (status indicator lags inside the Application Framework).

"I see errors after generation"
→ That's expected. Page 09 (Error Log Review) walks the diagnostic. Most are LINE_ITEM_FORMULA — fixable by copying from the base TRAIN model.

"Which models do I use for extensions?"
→ The pre-populated TRAIN models (with TRAIN prefix), not the ones you generated. The TRAIN models have data; extensions need data to demonstrate behavior.

"Can I delete a hierarchy level?"
→ Yes, but only middle levels — the leaf must stay at the bottom. When adding levels, drag new ones above the original leaf.

"What if I make a mistake in configuration?"
→ Restore Default per hierarchy (one at a time — no global reset). Or regenerate — you have the rest of the week.

"How do I know if my formula error is a real bug or my fault?"
→ Compare against the base TRAIN model. If the formula works there with similar config, it's something you renamed or changed during configuration.

"My generation hit an error and now I can't restart"
→ Confirm your four roles (Page Builder, Application Owner, Integration Admin, Workspace Admin) and Dataspace assignment with the tenant admin. Most "stuck" generations are actually permissions problems.

"Where's the recording of the live kickoff?"
→ Posted in the Slack channel as a pinned message. Also available at [RECORDING URL].
