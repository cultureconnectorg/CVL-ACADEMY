# CVLN Academy V1 — Integration provenance

Status: release-candidate evidence document for PR #5.

## Canonical curriculum checkpoint

Canonical/FMS checkpoint branch:

`claude/cvln-academy-canonical-fms`

Checkpoint SHA:

`38ebd6ab91bef74a005a75dd05ba5d488a131d14`

The release/integration branch is:

`claude/cvln-academy-production-r35l31`

Git ancestry was verified before this document was added: the canonical/FMS checkpoint is an ancestor of the release branch, with the release branch **0 commits behind** canonical. No FMS/canonical commit is being cherry-picked, duplicated, squashed, or rewritten for PR #5.

That means PR #5 includes the canonical curriculum runtime and corpus work by ancestry, then adds the later spatial production work and V1 closure hardening.

## Branch roles for V1 closure

- `main`: currently deployed/reference history; do not mutate until release evidence is complete.
- `claude/cvln-academy-canonical-fms`: preserved checkpoint for the canonical pedagogical work.
- `claude/cvln-academy-production-r35l31`: single V1 integration/release candidate.
- PR #5: only active merge candidate for the complete V1 state.

PR #4 was closed without merging because its head is already fully contained in the PR #5 head. Closing it avoids two competing merge candidates while preserving the branch and all history.

## Spatial closure scope

The initial H0.10 production-shell commit covered the application shell, environmental backdrop, desktop rail and Dashboard target tile. The V1 closure pass extends the same visual language to the remaining explicitly identified core learning surfaces:

- Roadmap stage cards and canonical-progress surface;
- Formations discovery/focus cards and next-action surface;
- Badges glanceable cluster;
- ModuleJourney phase shells.

These changes remain presentation-only and feature-flagged. Existing domain state, unlock rules, canonical routing, progression, certification and economic state are not redefined by the spatial layer.

## Merge gate

Do not merge PR #5 solely because this provenance document exists.

The exact final PR #5 HEAD must still pass the repository's real CI gates and final runtime/smoke validation. A V1 freeze is allowed only with no blocking P0 classified BROKEN, MISSING or PARTIAL.
