# iDirectory v6 agent governance

Use the minimum sufficient context. Start atomic work with `python FWengine.py context --pack <directory> --tier 1a`. For scoped planning use the compact view and focused slices; for architectural work consult the relevant seed sections and ecosystem pack.

- Precedence: executable code and schemas; config/context_policy.json; verified tree, beacons and layer states; active session; architectural seed; approved or executing plans.
- Never scan blindly or enter a crawl:false subtree. Do not preload the seed for atomic work. Never expose secrets; keep generated documentation paths relative.
- Consultations, audit checks and dry runs must not write. Respect the user's task scope and preserve their existing work.
- After topology or beacon changes, run `python FWengine.py reconcile` once. Verification uses `reconcile --check`.
- Maintain task identity, objective, constraints, evidence, decisions and next action in a session checkpoint. Completed or draft plans do not authorize execution.
- Edit canonical runtime sources in src/core; tools/icontext_runtime is generated with tools/build_runtime.py. Skills use the version in .context/toolchain.json.
- Workflow and migration details: docs/specs/icontext-v6.md. The entire previous governance file is preserved in docs/specs/agent-governance-before-v6.md for historical reference; current runtime and schemas take precedence over its v5 command semantics.
