# SaaS Product Base

This project is a new SaaS product built on top of ShipAny Template Two.

## Development Rules

Every new requirement, bug fix, behavior change, and refactor must follow test-driven development:

1. Write the failing automated test first.
2. Run the test and confirm it fails for the expected reason.
3. Implement the smallest change that makes the test pass.
4. Re-run the focused test.
5. Run broader verification before reporting completion.

AI agents should read `AGENTS.md` and `CLAUDE.md` before making changes.

## Testing

```bash
pnpm test
pnpm test:unit
pnpm test:watch
pnpm test:coverage
pnpm lint
pnpm typecheck
pnpm verify
```

Test layout:

- `tests/unit`: pure functions, models, utilities, service helpers.
- `tests/integration`: API handlers, database-backed flows, provider boundaries.
- `tests/e2e`: browser flows when Playwright is added.

High-risk areas must have tests before implementation: auth, RBAC, payments, subscriptions, credits, AI generation, API keys, webhooks, and admin write flows.

## Project Structure

- `src/app`: app routes and API handlers.
- `src/config`: runtime config, database schema, locale messages, styles.
- `src/core`: auth, database adapters, i18n, RBAC, theme loading.
- `src/shared/models`: database-backed domain models.
- `src/shared/services`: business services.
- `src/extensions`: third-party providers.
- `src/themes`: theme pages and landing blocks.

## ShipAny Documentation

Read the ShipAny docs for scaffold-specific setup:

https://shipany.ai/zh/docs

## License

!!! Please do not publicly release ShipAny's Code. Illegal use will be prosecuted

[ShipAny LICENSE](./LICENSE)
