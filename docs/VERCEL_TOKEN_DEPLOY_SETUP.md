# CVLN Academy — Vercel token deployment setup

This setup provides a GitHub Actions fallback for production deployment when the ChatGPT/Vercel connector cannot enumerate the CVLN team.

## Security rule

Never paste a Vercel token into chat, source code, commits, issues, pull requests, or logs. Store it only as a GitHub Actions secret.

## 1. Create a Vercel access token

In Vercel, open account settings and create an access token for the account/team that can deploy the `cvl-academy` project.

Copy the token once and store it immediately as the GitHub Actions secret `VERCEL_TOKEN`.

## 2. Find the Vercel organization/team ID

Use one of these safe sources:

- Vercel project/team settings; or
- a locally linked project's `.vercel/project.json` file after running `vercel link`.

The value normally appears as `orgId` in `.vercel/project.json`.

Store it in GitHub Actions as `VERCEL_ORG_ID`.

## 3. Find the Vercel project ID

For the linked CVLN Academy project, `.vercel/project.json` normally contains `projectId`.

Store it in GitHub Actions as `VERCEL_PROJECT_ID`.

Do not commit `.vercel/project.json` merely to expose these IDs; GitHub Actions secrets are the intended destination.

## 4. Add the three GitHub Actions secrets

Repository:

`cultureconnectorg/CVL-ACADEMY`

GitHub path:

`Settings → Secrets and variables → Actions → New repository secret`

Create exactly these names:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## 5. Run the deployment workflow

After this setup PR is merged, open:

`Actions → Vercel Production Deploy → Run workflow`

The workflow intentionally uses `workflow_dispatch` only. It does not automatically deploy on every push to `main` until the token path has been verified once.

The workflow performs:

1. secret-presence validation without printing secret values;
2. frontend dependency installation;
3. frontend ESLint;
4. frontend unit tests;
5. `vercel pull --environment=production`;
6. `vercel build --prod`;
7. `vercel deploy --prebuilt --prod`;
8. production deployment URL in the GitHub Actions job summary.

## 6. Verification gate

A deployment is considered valid only when:

- the workflow is green;
- the returned production URL loads CVLN Academy;
- the production domain points to the expected deployment;
- the deployed frontend matches the intended commit;
- the required production environment variables are present in Vercel;
- a visual canary check passes before further Spatial reconstruction work.

## Why this exists

The current ChatGPT Vercel connector can authenticate but returns no visible teams. This workflow is an operational fallback; it does not modify authentication, backend behavior, or CVLN Academy business logic.
