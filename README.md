# model-pricing

Saves point-in-time snapshots of the [Claude pricing page](https://platform.claude.com/docs/en/about-claude/pricing) using the [Exa](https://exa.ai) API, so you can see how model prices change month to month.

## Requirements

- Python 3.9+
- An Exa API key ([dashboard.exa.ai](https://dashboard.exa.ai)). Each snapshot is a paid API call, about $0.002 at the time of writing.

## Setup

```bash
git clone <repo-url>
cd model-pricing
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then put your key in .env
```

You can also set the key in your shell instead of using `.env`:

```bash
export EXA_API_KEY=your-key
```

## Usage

```bash
python pricing_exa_snapshot.py
```

This fetches the pricing page as it was on the 1st of each month from June to October 2026 and writes one file per month to `pricing-snapshots/`.

Snapshots that already exist are skipped, so re-running does not spend API credits. To re-fetch and overwrite them:

```bash
python pricing_exa_snapshot.py --force
```

## Output

Files are named `claude-model-pricing-YYYY-MM-DD.json`. Each one is the raw Exa response:

| Field | Contents |
| --- | --- |
| `results[].highlights` | Excerpts from the page, including the model pricing table in Markdown |
| `results[].summary` | Exa-generated summary of the page |
| `statuses` | Whether the fetch succeeded and where the content came from |
| `costDollars` | What the API call cost |

The snapshots in this repo are provided for reference. Pricing content belongs to Anthropic; check the live pricing page for current prices.

## License

[MIT](LICENSE)
