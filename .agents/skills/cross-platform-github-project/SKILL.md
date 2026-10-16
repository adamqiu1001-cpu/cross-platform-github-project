---
name: cross-platform-github-project
description: Set up a project so several computers share one GitHub repository while Windows and macOS each build their own artifacts. Use when starting a new project that will be developed on multiple computers or operating systems, connecting an existing local project to GitHub, or adding separate Windows/macOS builds or CI to an existing repository.
---

# Cross-Platform GitHub Project

GitHub is the shared source of truth; each operating system builds its own artifacts locally or in CI. Ask only for choices that materially affect repository owner, visibility, or build tooling; infer routine defaults from the project files. Every action listed under Safety boundaries needs the user's authorization at the point of that action.

## Workflow

1. **Inspect.** Identify the project type, Git state (history, remotes, uncommitted changes), package manager, runtime version files, build scripts, and agent instruction files (`AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`). Follow every instruction file that exists; when two conflict, ask the user which one wins. When the project already has a remote or history, adapt the remaining steps to it.
2. **Check the machine.** Confirm `git config user.name` and `git config user.email` hold the user's GitHub identity; when either is empty, ask for it and set it before the first commit. Check whether `gh` is installed and authenticated. Done when the identity is set and you know which repository-creation path in step 5 is available.
3. **Collect the target.** GitHub owner, repository name, visibility, and whether the remote repository already exists.
4. **Prepare local files.** Initialize Git when needed, preserving existing history and uncommitted changes. Add or update only `.gitignore`, `.gitattributes`, package-manager lockfiles, runtime version files, `.env.example`, platform build scripts, the agent instruction files, and the collaboration rules, following the sections below. Set local Git config: `pull.ff only`, `core.quotepath false`, and on Windows `core.longpaths true`.
5. **Create the remote.** Use the connected GitHub integration or `gh repo create`. When neither is available, ask the user to create an empty repository on github.com (no README, license, or `.gitignore`, so the first push is a fast-forward) and send you its URL.
6. **First push.** Show the files that will be committed, add the remote, commit, and push the default branch. When clone, push, or authentication fails, read `references/troubleshooting.md` and diagnose by the error text before retrying.
7. **Configure platform builds.** Build artifacts (`.exe`, `.msi`, `.dmg`, `.pkg`, and similar) go to ignored directories outside the tracked source. When CI or release artifacts are requested, use GitHub Actions with separate `windows-latest` and `macos-latest` jobs. When the installers will be distributed to other people, ask whether to set up code signing: Developer ID signing plus notarization on macOS, Authenticode on Windows. Signing credentials live in GitHub Actions secrets.
8. **Verify.** Done when every item holds: clean working tree after the push; correct remote URL and default branch; lockfile and runtime version file present; build output and secret paths ignored; development and build commands written in the README; collaboration rules present in the project; local `pull.ff only` set. Report anything that could not be run because the toolchain is missing.

## Cross-platform file rules

- `.gitattributes` starts from `* text=auto eol=lf`, then adds `*.bat text eol=crlf` and `*.cmd text eol=crlf` (cmd.exe misparses labels and `goto` in LF batch files) and marks binary assets with `binary`.
- Shell scripts committed from Windows arrive without the executable bit; set it in Git with `git update-index --chmod=+x <file>`.
- macOS and Windows filesystems are case-insensitive while Linux CI is case-sensitive. Keep file names and import paths in identical case everywhere; for a case-only rename, `git mv` through an intermediate name.
- Git carries source, lockfiles, and version-manager files. Dependencies (`node_modules`, virtual environments), IDE metadata, build output, and secrets stay local and are listed in `.gitignore`. Tracked files hold no credentials or machine-specific paths.
- Use Git LFS only when large binary assets are required and the user accepts the hosting cost.

## Collaboration rules

Write this section into the project's README, or into `AGENTS.md` when the project keeps contributor rules there, adapted to its default branch:

- Each computer clones the same repository and runs `git config --local pull.ff only` once.
- Before starting work, commit local changes, then run `git pull --ff-only`. If the pull stops because the branches have diverged, inspect both sides and choose merge or rebase deliberately.
- Feature work goes on branches and lands through pull requests; the default branch stays buildable.
- Push finished work before switching to another computer.

## Agent instruction files

The project may be worked on with both Codex and Claude Code. Keep one source of truth for project instructions:

- Put shared instructions in `AGENTS.md`. Codex reads it directly.
- Make `CLAUDE.md` a thin file whose first line is `@AGENTS.md`, so Claude Code imports the same content. Add only Claude-specific notes below that line.
- If only one of the two files exists, create the other in this form rather than copying content, so the two cannot drift apart.
- Commit both files. Personal or machine-specific instructions belong in `CLAUDE.local.md` (listed in `.gitignore`) or in the user's home-level configuration.
- Commit agent skill folders (`.agents/skills/` for Codex, `.claude/skills/` for Claude Code) when the project ships its own skills; keep `.claude/settings.local.json` out of Git.

## Safety boundaries

External mutations: creating a repository, pushing, changing visibility, and deleting or replacing a remote. Ask for authorization at the point of each one unless the user already explicitly authorized that specific action. Read-only inspection, local initialization, ignore-file edits, and local validation proceed without asking.

Preserve what already exists: push fast-forward only, keep existing remotes and history intact, and carry uncommitted changes forward. Force-pushing, rewriting history, replacing a remote, or discarding local changes happens only on the user's explicit request.
