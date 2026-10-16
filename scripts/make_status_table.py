#!/usr/bin/env python3
"""Write STATUS.md from status.json. Edit status.json, then run this."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "status.json").read_text())
icon = {"done": "✅ done", "doing": "🛠️ doing", "todo": "⬜ to do", "blocked": "⛔ blocked"}
done = sum(1 for m in data["milestones"] if m["status"] == "done")
lines = [f"# 🔫 Soldat Android: status", "",
         f"Updated: {data['updated']} · {done} of {len(data['milestones'])} milestones done", "",
         f"> {data['note']}", "",
         "| # | Milestone | Status | Size (estimate) |", "|---|---|---|---|"]
for m in data["milestones"]:
    lines.append(f"| {m['id']} | {m['title']} | {icon[m['status']]} | {m['estimate']} |")
lines += ["", "This table is made from `status.json` by `scripts/make_status_table.py`.", ""]
(root / "STATUS.md").write_text("\n".join(lines))
