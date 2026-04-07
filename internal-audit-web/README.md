# Internal Audit Prep (web)

Next.js app: product catalog, Secure Flow STI audits, and CSV-backed control questionnaires. Form answers persist in `localStorage` in the browser.

## Requirements

- Node.js 20+
- npm 10+

## Development

```bash
npm ci
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Production build

```bash
npm run ci
```

Runs ESLint and a production `next build`.

```bash
npm run start
```

Serves the app on port 3000 (set `PORT` to change).

### Configuration

Copy `.env.example` to `.env.local` when deploying. See comments there for optional `NEXT_PUBLIC_SITE_URL` and `ENABLE_HSTS`.

### Health check

`GET /api/health` returns JSON `{"status":"ok",...}` with `Cache-Control: no-store` for load balancers.

### Docker

```bash
docker build -t internal-audit-web .
docker run -p 3000:3000 internal-audit-web
```

Uses Next [standalone output](https://nextjs.org/docs/app/api-reference/config/next-config-js/output) and a non-root user inside the container.

### Data import (maintainers)

Sheet JSON is committed under `src/data/`. Refresh from CSV or Google Sheets using scripts in `scripts/` (`npm run import-audit-sheet`, `npm run import-audit-sheet-google`). Import tooling is dev-only; it is not part of the production server bundle for end users.

## GitLab (Red Hat internal)

Pipelines for **[gitlab.cee.redhat.com](https://gitlab.cee.redhat.com)** live in the **repository root**: `.gitlab-ci.yml` (next to `internal-audit-web/`).

**Push this repo to GitLab** (after creating an empty project under your group; replace URL and branch if needed):

```bash
git remote add gitlab https://gitlab.cee.redhat.com/<your-group>/pr-flow-ps.git
git push -u gitlab main
```

If `gitlab` remote already exists:

```bash
git push gitlab main
```

1. Create a project (or push this repo) on internal GitLab and ensure **shared or group runners** are available for `docker` / `node` jobs.
2. **Merge requests and branch pushes** run `verify` (`npm ci` + `npm run ci`) inside `internal-audit-web/`.
3. **Container image** job `build-image` is **manual** on the default branch and pushes to the project’s **GitLab Container Registry** (`$CI_REGISTRY_IMAGE`). Enable the registry under project **Settings → General**. The job needs a **Docker privileged** runner (Docker-in-Docker). If your org uses Kaniko, Tekton, or an external registry, replace that job with your standard pattern.

**CI/CD variables** (optional): `NEXT_PUBLIC_SITE_URL`, `ENABLE_HSTS` — same meaning as `.env.example`; passed as Docker build-args for the image job.

If the GitLab project contains **only** this app at the repo root (no `internal-audit-web/` folder), either move the app files to the root or edit `.gitlab-ci.yml`: set `APP_DIR` to `.`, drop the `cd`, and set the cache key/paths to `package-lock.json` and `node_modules/`.

## Security notes

- Default response headers include `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, and `X-Frame-Options`. Enable HSTS only when appropriate (see `.env.example`).
- Do not commit service account keys; `.gitignore` excludes `.secrets/` and common key filenames.
