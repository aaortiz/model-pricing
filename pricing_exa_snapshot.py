import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from exa_py import Exa

parser = argparse.ArgumentParser(
    description="Save monthly snapshots of the Claude pricing page using Exa."
)
parser.add_argument(
    "--force",
    action="store_true",
    help="re-fetch and overwrite snapshots that already exist",
)
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("EXA_API_KEY")
if not api_key:
    sys.exit(
        "EXA_API_KEY is not set. Copy .env.example to .env and add your key, "
        "or run: export EXA_API_KEY=your-key"
    )

exa = Exa(api_key)
out_dir = Path(__file__).parent / "pricing-snapshots"
out_dir.mkdir(exist_ok=True)

# Snapshot of the pricing page on the 1st of each month, June-October 2026
for month in range(6, 11):
    out_file = out_dir / f"claude-model-pricing-2026-{month:02d}-01.json"
    if out_file.exists() and not args.force:
        print(f"Skipped {out_file.name} (already exists, use --force to overwrite)")
        continue
    result = exa.get_contents(
        urls=["https://platform.claude.com/docs/en/about-claude/pricing"],
        highlights={"query": "Pull model pricing from the model provider only"},
        snapshot_as_of=f"2026-{month:02d}-01T22:12:00.000Z",
        summary=True,
    )
    out_file.write_text(json.dumps(result, default=vars, indent=2))
    print(f"Saved {out_file.name}")
