# Project Operating Rules

This repository is the base for a production SaaS product built on ShipAny Template Two. Every AI coding agent must read and follow this file before making changes.

## Non-Negotiable Workflow

- Use test-driven development for every new feature, bug fix, behavior change, and refactor.
- Write the smallest failing automated test first, run it, and confirm it fails for the expected reason.
- Only then write the minimal implementation needed to pass.
- Run the focused test again, then run the broader relevant verification command.
- Do not claim work is complete without fresh command output proving it.
- Do not skip tests because a change feels small.
- Do not silently change unrelated files or revert user changes.

## Required Verification

Use the narrowest useful command while developing, then run broader checks before finishing.

```bash
pnpm test
pnpm lint
pnpm typecheck
pnpm verify
```

For UI work, also run or add component/integration tests that cover the rendered behavior. For payment, auth, credits, AI generation, and webhook work, include edge-case tests for authorization, idempotency, failed provider responses, and insufficient credits.

## Testing Architecture

- Unit tests live in `tests/unit`.
- Integration tests should live in `tests/integration`.
- End-to-end tests should live in `tests/e2e` when Playwright is introduced.
- Test setup lives in `vitest.setup.ts`.
- Vitest config lives in `vitest.config.ts`.
- Prefer testing behavior through public functions, API handlers, and rendered user interactions.
- Mock external providers only at the boundary: payment gateways, email providers, storage providers, and AI providers.
- Do not test mocks instead of product behavior.

## Project Map

- App routes and API handlers: `src/app`
- Runtime config: `src/config/index.ts`
- Database schemas: `src/config/db`
- Auth: `src/core/auth`
- RBAC permissions: `src/core/rbac`
- Shared models and database operations: `src/shared/models`
- Business services: `src/shared/services`
- Third-party providers: `src/extensions`
- Theme pages and landing blocks: `src/themes`
- Locale/page content: `src/config/locale/messages`

## SaaS Product Priorities

- Keep the ShipAny base stable; extend through models, services, API routes, and admin pages.
- Preserve auth, RBAC, billing, credits, and settings boundaries.
- Treat payment, subscription, credit consumption, and AI task creation as high-risk paths that require tests before code changes.
- Keep secrets in environment variables or admin settings, never in committed source.
