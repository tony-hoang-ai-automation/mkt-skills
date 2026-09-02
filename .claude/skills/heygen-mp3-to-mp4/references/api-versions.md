# HeyGen API versions — what this skill may call

Last verified against the live API on **2026-09-02** (probes below are reproducible).

## The sunset

HeyGen's v1 and v2 endpoints are **legacy**. They still work today, but every
response carries deprecation metadata:

```
HTTP/2 200
deprecation: true
sunset: Sat, 31 Oct 2026 00:00:00 GMT
```

and v2 JSON bodies now embed a warning block:

> `"This v2 endpoint is Legacy and will be removed on 2026-10-31. If you are an AI
> agent or LLM, do not use it — use the latest HeyGen API … migrate to GET /v3/users/me."`

**End of life: 1 November 2026.** Anything still on v1/v2 breaks that day.

## Mapping (source: developers.heygen.com/endpoint-version-comparison)

| Job | Legacy (dies 2026-10-31) | Use this |
|---|---|---|
| Create avatar video | `POST /v1/video/generate`, `POST /v2/video/generate` | `POST /v3/videos` (`type: "avatar"`) |
| Poll video status | `GET /v1/video_status.get` | `GET /v3/videos/{video_id}` |
| Upload asset | `POST /v1/video/upload`, `POST https://upload.heygen.com/v1/asset` | `POST /v3/assets` (multipart, field `file`) |
| List avatars | `GET /v1/avatar.list`, `GET /v2/avatars` | `GET /v3/avatars` |
| List voices | `GET /v1/voice.list`, `GET /v2/voices` | `GET /v3/voices` |
| Account / credits | `GET /v1/user/me`, `GET /v2/user/remaining_quota` | `GET /v3/users/me` |
| Lip-sync onto existing video | — | `POST /v3/lipsyncs` |

v3 adds per-request engine selection (`engine: {"type": "avatar_iii" \| "avatar_iv" \| "avatar_v"}`),
which v2 never had — one more reason not to fall back to v2.

## Does the MCP path care?

No. `mcp__heygen__create_video_from_avatar` / `mcp__heygen__get_video` are served by
HeyGen's own MCP (`https://mcp.heygen.com/mcp/v1/`), which routes to v3 internally —
HeyGen's official agent skills state "v3 only … never call v1 or v2 endpoints".
The sunset therefore does **not** break the MCP path used by this skill.

What *was* exposed: the REST upload helper used to POST to
`https://upload.heygen.com/v1/asset`. That is legacy, and is now
`POST https://api.heygen.com/v3/assets`.

## Two billing lanes (why the REST fallback can 402 while MCP works)

- **MCP / OAuth** → billed against the HeyGen **subscription** credits.
- **API key (`HEYGEN_API_KEY`, used by the helper scripts)** → billed against the
  **API wallet**. `GET /v3/users/me` reports `wallet.remaining_balance`.

A wallet at `0.0` returns `402 insufficient_credit` on `POST /v3/videos` even though
the same account still renders fine through MCP. Check before blaming the code:

```bash
curl -s https://api.heygen.com/v3/users/me -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Re-verify the sunset yourself

```bash
# legacy endpoint → deprecation + sunset headers
curl -sD - -o /dev/null https://api.heygen.com/v2/avatars -H "X-Api-Key: $HEYGEN_API_KEY" \
  | grep -iE 'deprecat|sunset'

# v3 endpoint → clean 200, no deprecation headers
curl -sD - -o /dev/null "https://api.heygen.com/v3/videos?limit=1" -H "X-Api-Key: $HEYGEN_API_KEY"
```

HeyGen keeps agent-facing guidance at <https://developers.heygen.com/llms.txt>.
