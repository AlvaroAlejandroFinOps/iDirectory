# /idir - Claude Code Command for iDirectory Governance & Context Engineering

Execute iDirectory governance commands via `python FWengine.py`:
- `init`: Initialize structure, beacons, and satellite map.
- `route "<file>" [--move]`: Audit or relocate file to its canonical directory.
- `beacon --sync`: Generate or synchronize all `.context.yaml` beacons.
- `context --budget`: Inspect directory token density and budget.
- `audit`: Verify that no uppercase directories or missing beacons exist.
