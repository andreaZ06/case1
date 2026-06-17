# Claude Project Memory

This is a production SaaS product being built on ShipAny Template Two. Follow these rules every time you work in this repository.

## Always Use TDD

For every new requirement or code change:

1. Write a failing automated test first.
2. Run the test and confirm the failure is expected.
3. Implement the smallest change that makes the test pass.
4. Re-run the focused test.
5. Run broader verification before reporting completion.

No production code should be changed without a test that failed first, unless the user explicitly approves an exception for documentation-only or configuration-only work.

## Verification Commands

```bash
pnpm test
pnpm lint
pnpm typecheck
pnpm verify
```

Use focused tests during development, then run `pnpm verify` before finalizing substantial work.

## Test Layout

- `tests/unit`: pure functions, models, utilities, service helpers.
- `tests/integration`: API handlers, database-backed flows, provider boundaries.
- `tests/e2e`: browser flows when Playwright is added.
- `vitest.config.ts`: test runner config.
- `vitest.setup.ts`: shared test setup.

## High-Risk Areas

Add or update tests first for:

- Auth and RBAC
- Payment checkout, callbacks, webhooks, subscriptions
- Credit grants and consumption
- AI generation, async tasks, provider callbacks
- API key access
- Admin write flows

## Coding Boundaries

- App routes and API handlers: `src/app`
- Config: `src/config`
- Core infrastructure: `src/core`
- Models: `src/shared/models`
- Services: `src/shared/services`
- Provider integrations: `src/extensions`
- Theme and landing UI: `src/themes`

Do not mix UI, database, provider, and business logic in one place when an existing layer already fits.
