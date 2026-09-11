# Spatial production background fix

## Root causes observed

1. `SPATIAL_ENGINE` and `SPATIAL_ENVIRONMENT` defaulted to `false` when deployment environment variables were absent, so the live background motion did not activate by default in production builds.
2. The Spatial world image was present, but the readability scrim was intentionally very strong and visually washed the scene toward the former pale Academy background.

## Production decision

- `SPATIAL_ENGINE`: default **ON**
- `SPATIAL_ENVIRONMENT`: default **ON**
- Route transitions, audio, haptics, debug, and lifecycle runtime remain opt-in.
- Vercel/environment values can still explicitly disable the live engine using `false`/`0` or an invalid value.
- Reduced-motion behavior remains authoritative and unchanged.

## Verification

`SpatialBackground.production.test.js` verifies that an environment with no Spatial overrides renders `data-spatial-engine="on"` while preserving the explicit kill-switch behavior.
