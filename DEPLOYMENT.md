# Save Tears Deployment Notes

Last verified: 2026-04-27 21:23 Asia/Shanghai

This document records where the production deployment lives and how to update it.
Do not store passwords, private keys, tokens, or `.env.production` contents in this file.

## Production Entry Points

- Primary site: `https://savetear.cloud/`
- `www` site: `https://www.savetear.cloud/`
- Backend health check: `https://savetear.cloud/api/health`
- Temporary direct IP entry, if domain troubleshooting is needed: `http://111.229.142.196/`
- Web frontend: H5 build of `save_tears_miniprogram`, currently showing the greywater saving experience.

Current verified status:

- `https://savetear.cloud/` returns `HTTP/2 200`.
- `https://www.savetear.cloud/` returns `HTTP/2 200`.
- `https://savetear.cloud/api/health` returns `{"status":"ok","database":"ok","service":"save-tears-backend","version":"1.0.0"}`.

## Cloud Server

- Provider: Tencent Cloud Lighthouse
- Instance name shown in console: `Ubuntu-Sq1J`
- Instance ID seen during setup: `lhins-gogn2w7c`
- Region: Shanghai
- Public IPv4: `111.229.142.196`
- SSH user: `ubuntu`
- Production app directory: `/home/ubuntu/save-tears`

Important detail:

- `/home/ubuntu/save-tears` is currently **not** a git clone.
- Updates are deployed by creating a local archive, copying it to the server, extracting it over `/home/ubuntu/save-tears`, and rebuilding Docker Compose.
- Do not assume `git pull` on the server will work unless the deployment method is changed later.

## Domain And DNS

Domain: `savetear.cloud`

DNS records:

```text
@     A     111.229.142.196
www   A     111.229.142.196
```

Firewall rules required in Tencent Cloud Lighthouse:

```text
HTTP    TCP 80    source 0.0.0.0/0    allow
HTTPS   TCP 443   source 0.0.0.0/0    allow
```

The backend container port `8000` must remain private; public traffic goes through Caddy.

## TLS Certificate

Caddy now uses automatic HTTPS for `DOMAIN`. The `ACME_EMAIL` value in `.env.production` is used for certificate registration and renewal.

Security rule:

- Do not commit `.env.production`.
- Do not commit any private key if the deployment is changed back to manual certificates later.

Restart Caddy after changing domain or TLS settings:

```bash
ssh ubuntu@111.229.142.196
cd ~/save-tears
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --force-recreate caddy
```

## Runtime Stack

Production is run by Docker Compose:

```text
docker-compose.prod.yml
```

Services:

- `backend`: FastAPI app, private port `8000`, SQLite database stored in Docker volume.
- `frontend`: H5 build of `save_tears_miniprogram`, private Nginx port `80`. This is the runnable web frontend; there is no separate `save_tears_frontend` deployment.
- `caddy`: public reverse proxy, exposes `80` and `443`.

Persistent volumes:

- `save-tears-backend-data`: backend SQLite data.
- `caddy-data`: Caddy state.
- `caddy-config`: Caddy config state.

Important production files on the server:

```text
/home/ubuntu/save-tears/.env.production
/home/ubuntu/save-tears/Caddyfile
/home/ubuntu/save-tears/docker-compose.prod.yml
```

`.env.production` contains secrets and must not be copied into git.

Required production environment highlights:

```bash
DOMAIN=savetear.cloud
ACME_EMAIL=your-email@example.com
SAVE_TEARS_SECRET=replace-with-a-long-random-secret
SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET=replace-with-a-different-long-random-secret
```

## Update Procedure

Use this when updating production from the local repository.

1. Verify locally before deploying.

```bash
python3 -m unittest discover -s save_tears_backend -p 'test*.py'
cd save_tears_miniprogram
npm run type-check
npm run build:h5
cd ..
```

2. Commit the code you want to deploy.

```bash
git status --short
git add <changed-files>
git commit -m "Describe deployment change"
git push origin taox/save-tears-project-upload
```

3. Create and upload a clean archive from the committed `HEAD`.

```bash
git archive --format=tar.gz -o /tmp/save-tears-deploy.tar.gz HEAD
scp /tmp/save-tears-deploy.tar.gz ubuntu@111.229.142.196:/home/ubuntu/save-tears-deploy.tar.gz
```

4. Extract and rebuild on the server.

```bash
ssh ubuntu@111.229.142.196
cd ~/save-tears
tar -xzf ~/save-tears-deploy.tar.gz
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
docker compose --env-file .env.production -f docker-compose.prod.yml ps
```

5. Verify production after deployment.

```bash
curl -I https://savetear.cloud/
curl https://savetear.cloud/api/health
```

Expected health response:

```json
{"status":"ok","database":"ok","service":"save-tears-backend","version":"1.0.0"}
```

Web frontend verification:

- Open `https://savetear.cloud/`.
- Register or log in.
- Confirm the home page title is `节水概览`.
- Confirm the data center shows the tabs `自来水`, `灰水`, `趋势`, and `计划`.
- For an admin account, open `我的 -> 管理` and confirm the page title is `节水管理`.
- Generate a saving plan from the `计划` tab. If no LLM API is configured, the backend should still return a rule-based fallback plan.

Optional ThingCloud webhook smoke test, using the secret from `.env.production`:

```bash
curl -X POST https://savetear.cloud/api/integrations/thingcloud/events \
  -H 'Content-Type: application/json' \
  -H "X-ThingCloud-Secret: $SAVE_TEARS_THINGCLOUD_WEBHOOK_SECRET" \
  -d '{
    "event_id": "deploy-smoke-001",
    "device_id": "GW-A101-001",
    "room_number": "A101",
    "event_type": "toilet_flush",
    "event_count": 1,
    "timestamp": "2026-04-27T10:30:00",
    "source": "device"
  }'
```

## Useful Operations

View running containers:

```bash
ssh ubuntu@111.229.142.196
cd ~/save-tears
docker compose --env-file .env.production -f docker-compose.prod.yml ps
```

View logs:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=120
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=120 backend
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=120 caddy
```

Restart all services:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --force-recreate
```

Restart only Caddy:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --force-recreate caddy
```

Check whether public ports are reachable:

```bash
nc -vz -w 8 savetear.cloud 80
nc -vz -w 8 savetear.cloud 443
```

Check certificate details:

```bash
echo | openssl s_client -connect savetear.cloud:443 -servername savetear.cloud 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

## WeChat Mini Program Notes

For WeChat Mini Program release, configure the request legal domain as:

```text
https://savetear.cloud
```

Do not use:

```text
http://111.229.142.196
http://savetear.cloud
```

WeChat production requests require HTTPS and an approved legal domain.

## Compliance Notes

- ICP filing is complete enough for the domain to serve from the mainland server.
- The public site should display the official ICP filing number in the footer.
- Public security filing may still require follow-up within the required window after service launch.
- The public security filing data code shown during filing is not the same as the ICP filing number.
