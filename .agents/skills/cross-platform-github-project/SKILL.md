---
name: cross-platform-github-project
description: Initialize a new project with a GitHub remote, shared cross-platform source workflow, locked dependencies, and separate Windows/macOS build paths. Use when starting a project that must be developed on multiple computers or operating systems.
---

# Cross-Platform GitHub Project

Set up a new project so GitHub is the shared source of truth and each operating system builds its own artifacts locally or in CI. Ask only for choices that materially affect repository visibility, owner, or build tooling; infer routine defaults from the project files.

## Workflow

1. Inspect the target directory and identify the project type, existing version-control state, package manager, runtime version files, build scripts, and any existing `AGENTS.md` instructions.
2. Before creating or changing a remote repository, collect the required GitHub account/owner, repository name, visibility, and whether the target directory already contains code. A remote repository creation is an external mutation and requires explicit user authorization immediately before it.
3. Initialize local Git when needed. Preserve existing history and uncommitted user changes. Add or update only the minimum project files required for the workflow: `.gitignore`, `.gitattributes`, package-manager lockfiles, runtime version files, `.env.example`, and platform build scripts.
4. Create the GitHub repository only after the user has approved the concrete owner/name/visibility. Prefer the connected GitHub integration or `gh repo create` when available. Never put credentials, tokens, or machine-specific paths in tracked files.
5. Add the remote, create the initial commit, and push the default branch only after confirming the repository target and showing the files that will be committed. Do not force-push or overwrite an existing remote.
6. Configure platform builds. Keep shared application code and build configuration in Git; generate `.exe`, `.msi`, `.dmg`, `.pkg`, and other artifacts outside the source tree or under ignored directories. Use GitHub Actions with separate `windows-latest` and `macos-latest` jobs when CI validation or release artifacts are requested.
7. Verify the result: clean working tree after the initial push, remote URL, default branch, lockfile presence, ignored build/secrets paths, and discoverable development/build commands. Report anything that could not be run because the project lacks its toolchain.

## Cross-machine operating rules

- Each computer clones the same remote repository and runs `git pull --rebase` before starting work.
- Feature work goes on branches; shared work lands through pull requests. Keep `main` buildable.
- Do not synchronize `node_modules`, virtual environments, IDE metadata, build output, or secrets through Git.
- Resolve dependency and runtime differences through committed lockfiles and version-manager files rather than copying local directories.
- Use Git LFS only when large binary assets are required and the user accepts the hosting cost.

## Safety boundaries

Treat repository creation, pushing, changing visibility, and deleting or replacing a remote as external mutations. Ask for authorization at the point of that action if it was not already explicitly authorized. Read-only inspection, local initialization, ignore-file edits, and local validation can proceed without another approval.

When the project already has a remote or Git history, inspect it first and adapt the workflow. Never replace an existing remote, rewrite history, or discard local changes as a convenience.
