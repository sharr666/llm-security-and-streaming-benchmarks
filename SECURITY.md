# Security Policy

## Status

This project is an experimental detector prototype, not a certified or comprehensive prompt-injection defense.

## Supported versions

| Version | Status |
|---|---|
| Current default branch | Best-effort review; no service-level response guarantee |

## Reporting

Report suspected vulnerabilities privately through GitHub Security Advisories. Include a minimal reproduction, affected commit, expected behavior and observed behavior. Do not include real credentials, personal data or production secrets.

## Key handling

Production HMAC keys must be provisioned outside the repository, scoped per trusted producer/repository, rotated, and access-controlled. The engine accepts keys through dependency injection. The test keys in the benchmark and unit tests are public fixtures and must never be reused in production.
