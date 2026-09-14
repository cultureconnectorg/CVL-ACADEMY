# BCI-03 — Banque N1 (formative, M1→M3)

```
Sourced against BCH-01-M03's own real module definition
(seed_modules.py:1521-1528, cited never re-derived) and standard
smart-contract security-audit methodology.
```

## M1 — `BCH-01-M03` literacy

1. What is `BCH-01-M03`'s real name and deliverable? ("Smart
   contracts pour royalties automatiques" — deliverable: "Smart
   contract déployé testnet")
2. Is this deployment on mainnet or testnet? (Testnet — never
   overstated as mainnet/production)

## M2 — standard vulnerability classes

3. Name at least 3 standard vulnerability classes an auditor checks
   for in a royalty-distribution smart contract. (E.g. reentrancy,
   integer overflow/underflow, access-control checks, oracle
   manipulation)

## M3 — testnet-vs-audited discipline

4. Does a successful testnet deployment, by itself, demonstrate that
   a contract has been security-audited? (No — it demonstrates the
   contract runs as coded, not that it is free of the vulnerability
   classes in M2)
5. What is the correct answer if asked "has `BCH-01-M03`'s contract
   been professionally audited?" (No — its real scope is a
   pedagogical testnet deployment, never presented as an audited
   production system)
6. Why does automated royalty distribution specifically raise the
   access-control vulnerability class as a top concern, more than a
   generic utility contract might? (Because it moves value between
   parties automatically — a broken access check could let an
   unauthorized party redirect or drain royalty payments, a direct
   financial-harm vector unique to payment-moving contracts)
7. If a candidate is asked to design a *real* audit engagement for a
   contract like `BCH-01-M03`'s, what would need to exist that does
   not exist today? (A contracted third-party security auditor, a
   defined audit scope and methodology sign-off, and a mainnet
   deployment target — none of which exist for this pedagogical
   exercise)
