# Decision Template

Use this exact structure in veto output.

## Verdict
- `GO` | `CONDITIONAL` | `NO-GO`

## Blocking reasons
1. ...
2. ...

## Assumption table
| assumption | supporting evidence | conflict evidence | status |
|---|---|---|---|
| ... | ... | ... | valid / risky / invalid |

## Safe next step
1. one minimal, testable action with fixed baseline and fixed route policy.

## Override policy
- If user explicitly requests override:
  - mark: `veto_overridden`
  - log the accepted risk in maintenance log and retrospective note.
