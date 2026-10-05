import json
import os
from pathlib import Path

from exa_py import Exa

exa = Exa(os.environ["EXA_API_KEY"])
out_dir = Path(__file__).parent / "pricing-snapshots"
out_dir.mkdir(exist_ok=True)

# Snapshot of the pricing page on the 1st of each month, June-October 2026
for month in range(6, 11):
    result = exa.get_contents(
        urls=["https://platform.claude.com/docs/en/about-claude/pricing"],
        highlights={"query": "Pull model pricing from the model provider only"},
        snapshot_as_of=f"2026-{month:02d}-01T22:12:00.000Z",
        summary=True,
    )
    out_file = out_dir / f"claude-model-pricing-{month}-1-26.json"
    out_file.write_text(json.dumps(result, default=vars, indent=2))
    print(f"Saved {out_file.name}")
