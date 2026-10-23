# Ask-the-docs Worker

Answers questions on the site from the sections the browser retrieves. Free: it uses the
Workers AI binding, so there is no API key, and the free daily allowance caps total use.

Deploy (one time):

    cd worker/ask
    npx wrangler login
    npx wrangler deploy

Wrangler prints the Worker URL (`https://wardogs-ask.<account>.workers.dev`). Put it in
`_config.yml` as `ask_endpoint:` and push. Until it is set, the site's Ask box still works
and lists the best-matching sections, without a written answer.

If a local site needs to call it, add its origin to `ALLOWED_ORIGINS` (comma separated).
If `wrangler deploy` rejects the `[[unsafe.bindings]]` rate-limit block, check the current
rate-limiting binding syntax in the Cloudflare docs; the Worker skips the limit when the
`LIMITER` binding is absent.
