# Golden Tagging Policy

## Naming
Use:
`<design>_<tech>_stagegolden_v<version>_<YYYYMMDD>`

Example:
`s8_gt3_stagegolden_v1_20260304`

## Source policy
1. Prefer one consistent run chain for place/cts/route.
2. If mixed run dirs are required, document reason in manifest note or task brief.
3. Always keep stage tuple matched: `DEF + V + SDC` from same stage source.

## Promotion
1. Keep previous tags immutable.
2. Promote new tag by changing `*_current` symlink only after verification.
