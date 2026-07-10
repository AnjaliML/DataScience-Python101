# Course data

`customer_renewals.csv` is a deterministic synthetic dataset created for this
course. It represents no real people, company, or commercial process.

Each row is one fictional customer at a subscription-renewal decision:

| Column | Meaning | Contract |
| --- | --- | --- |
| `customer_id` | row identifier | unique string |
| `plan` | current plan | `basic`, `plus`, or `pro` |
| `signup_channel` | acquisition channel | `organic`, `referral`, `paid`, or `partner` |
| `tenure_months` | completed months | integer from 1 to 48 |
| `monthly_usage_hours` | recent product use | decimal from 0 to 100 |
| `support_tickets` | recent ticket count | integer from 0 to 30 |
| `satisfaction_score` | optional survey score | decimal from 1 to 10 or missing |
| `renewed` | observed outcome | `0` or `1` |

The target is generated from a documented probability rule plus random noise.
Eighteen survey values are missing completely at random so learners must make
their missing-data policy explicit. The CSV is regenerated with:

```bash
uv run python scripts/generate_data.py
```

The seed and row count are constants in the generator. Both the generator and
generated data are covered by the repository's MIT License.
