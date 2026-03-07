# Stale Delete And Archive Policy

Delete an artifact only when:
1. it is generated noise or a clearly disposable duplicate,
2. it has no unique traceability value,
3. the report records why deletion is safe.

Archive instead of delete when:
1. the artifact is stale but historically meaningful,
2. a newer canonical artifact replaces it,
3. future audit or rollback may still need it.

Keep in place when:
1. the artifact is still the canonical reference,
2. its age alone does not make it stale,
3. deletion or archiving would break links before those links are updated.
