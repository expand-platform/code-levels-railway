## Code Levels Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/GB6Eki?referralCode=U5zXSw)

### Local start with Docker + Redis

1. Copy `.env.docker.example` to `.env.docker`.
2. Update Postgres credentials in `.env.docker`.
3. Run:

```bash
docker compose up --build
```

App URL: http://localhost:8000

Detailed guide: `docs/mvp/docker-redis-guide.md`
