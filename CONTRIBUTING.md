# Contributing

## Development principles

- Keep the platform local-first and provider-neutral.
- Put deployable processes in `apps/` and reusable business logic in `packages/`.
- Do not place provider-specific behavior in core retrieval or generation modules.
- Add database changes through migrations.
- Add or update tests with every behavioral change.
- Never commit credentials, uploaded documents, model weights, or database files.

## Branch and commit guidance

- Use short, descriptive branch names.
- Keep commits focused on one coherent change.
- Use imperative commit subjects, for example `Add filesystem storage adapter`.
- Document material architectural choices in `docs/adr/`.

## Quality checks

Before submitting a change, run the relevant formatting, linting, type checking, unit tests, and integration tests. Exact commands will be added when the application toolchains are initialized.
