# Testing Strategy

Initial software-level scenarios:

| Scenario | Expected result |
|---|---|
| Normal driving | No event |
| Sudden braking | No immediate accident confirmation |
| Single abnormal sample | Reject |
| Consecutive abnormal samples | Confirm |
| GPS valid | Generate location link |
| GPS invalid | Report unavailable |
| Confirmed event | Generate alert message |

Run:

```bash
pytest -q
```

These tests do not establish real-world crash-detection accuracy.
