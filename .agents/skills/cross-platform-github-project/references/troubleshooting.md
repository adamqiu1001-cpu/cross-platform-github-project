# Direct GitHub uploads: setup and troubleshooting

Use official Git and GitHub CLI for uploads; routine pushes do not need Chrome. A one-time web login may still be needed. Diagnose by the actual error before changing network or credentials. Commands handed to the user start with `cd <repository>` where applicable. Run the matching commands for the user's shell.

## Install or locate GitHub CLI

Check `git --version`, then `gh --version`. If `gh` is absent from PATH, check known installation or task tool locations first and use an existing executable's full path. Keep machine-specific paths in local setup notes, outside the shared skill.

- **macOS with Homebrew:** `brew install gh`.
- **macOS without Homebrew:** download the matching Apple silicon (`arm64`) or Intel (`amd64`) ZIP from [official GitHub CLI releases](https://github.com/cli/cli/releases/latest). Verify its SHA-256 against the release checksum before executing. Extract into a stable user-writable tools directory, preserve its license, and invoke `bin/gh` by full path or add that directory to PATH. A `.pkg`, Homebrew, Python, and an administrator install are not prerequisites for this route.
- **Windows:** `winget install --id GitHub.cli --exact`, or use the matching official release installer/archive. Reopen the terminal after installation if PATH has changed. Install Git separately if missing.

Do not disable TLS verification to make installation or login work. If Python reports certificate errors while macOS `curl` works, use the working official download route instead of weakening certificate checks.

## Authenticate and verify completion

```sh
gh auth login --hostname github.com --git-protocol https --web
gh auth status
gh auth setup-git --hostname github.com
```

Run the status/setup commands after login has completed. Check the intended account and storage location. GitHub CLI normally uses the system keychain or credential manager; if it reports plaintext fallback, resolve secure storage before treating setup as complete. Do not request `--insecure-storage` by default. Never print tokens, run `gh auth token` for diagnostics, put secrets into a remote URL, or ask the user to paste credentials into chat.

Let the user confirm the official device code and requested permissions. If the web page still shows **Confirm access**, **Verify via email**, two-factor authentication, or a pending authorization screen, have the user finish it. A user report that authorization is done should trigger a CLI check: wait for the CLI success result and verify `gh auth status`. If the code expires, start a fresh login and give the new code. Do not repeatedly restart an active login while the user is verifying their identity.

`gh auth setup-git` changes Git's credential-helper configuration for the host. Inspect existing helpers first when multiple accounts or custom helpers are involved; use repository-local helper settings if only that repository should change. Keep valid credentials for other accounts intact. Each computer authenticates separately; credentials are not included in skill packages or source archives.

After setup or permission repair, verify repository write access with `git push --dry-run` on the intended branch/ref. Then perform the authorized real push and compare the remote commit, for example with `git ls-remote origin refs/heads/<branch>`; for a Pull Request also check `gh pr view --json headRefOid,url`. Upload is complete only when these match the intended local commit.

## `403`, `Permission denied`, or connector integration errors

Network access has reached GitHub; distinguish the credential source and its permissions:

- A connector can read a repository while its write calls fail with **Resource not accessible by integration**. Connector access and local Git/CLI access are independent. Try the official CLI route; changing local credentials does not grant the connector new permissions.
- For Git HTTPS 403, inspect `gh auth status`, repository ownership/collaborator access, and helper precedence with `git config --show-origin --get-all credential.helper` and `git config --show-origin --get-all credential.https://github.com.helper`. Commit author settings do not grant write access.
- For an intended CLI account with write access, configure its helper using `gh auth setup-git --hostname github.com`, then retry the dry run. An old keychain credential may belong to the right username and still lack permission. Preserve it until the replacement route has been verified; host-wide credential deletion is not a first step.
- If the user chooses a fine-grained token, select the intended repository and **Contents: Read and write**; add **Workflows: Read and write** only when modifying workflow files. Follow GitHub's official approval flow and enter the token privately using a credential manager, never in chat or tracked files. Organization approval and account access may also be required. Do not assume changing token permissions is supported in place or that credential replacement is unnecessary; verify with a dry run.

GitHub account passwords do not work as Git HTTPS passwords. If the connector and CLI both lack write permission after these checks, report the exact remaining access requirement rather than retrying the same upload through Chrome.

## `Operation timed out`, `Failed to connect`, or `Recv failure`

Check direct HTTPS reachability and any configured proxy separately. Use bounded connection timeouts. A working public API does not by itself prove that Git transport or device login endpoints work.

- macOS: `scutil --proxy` shows system settings.
- Windows: inspect Settings → Network & Internet → Proxy and `netsh winhttp show proxy` as appropriate.
- Git: `git config --show-origin --get-regexp proxy`. Also check whether the terminal has `HTTP_PROXY`, `HTTPS_PROXY` or `ALL_PROXY`, without exposing credentials embedded in their values.

Git and terminal clients do not necessarily inherit system proxy settings. Confirm that the configured listener is running before routing GitHub through it with `git config --global http.https://github.com.proxy http://HOST:PORT`. Change only the relevant setting after diagnosis; avoid hardcoding a port from another computer. A login waiting on email verification is not a network timeout.

## `non-fast-forward`, `fetch first`, or divergent web-upload history

Fetch and inspect before deciding how to preserve both sides:

```sh
git fetch origin
git log --oneline --graph --all -20
git diff HEAD origin/<branch>
```

Use `git pull --ff-only` when the update is a fast-forward. If histories diverge, choose a history-preserving merge or the branch reconstruction below. Rebase rewrites commits and requires explicit authorization under the skill's Safety boundaries. The user's upload authorization may cover routine history-preserving reconciliation, but does not authorize discarding commits or force-pushing.

If web-upload commits and local commits contain equivalent source, keep the original local branch as a recoverable branch, start a new working branch from `origin/<branch>`, and apply only missing changes. Compare complete trees, including file modes; identical text does not imply identical history. Preserve unrelated uncommitted work before switching. Push the new commit as a fast-forward to the intended remote branch, and align the local branch name/upstream so subsequent plain `git push` works. Ask only when the comparison leaves a material choice about content or history unresolved.

If the complete trees already match, keep the original local branch, align the working branch with the intended remote branch and verify the existing remote state; no synthetic commit or redundant upload is needed.

## Other local setup errors

- **`not a git repository`:** enter the existing checkout; do not initialize a new repository in an unrelated directory.
- **Missing or unintended commit author:** inspect `git config user.name` and `git config user.email`, ask for missing identity, and set the chosen values. Changing commit identity does not fix authentication. Alter earlier commits only within the user's authorization and while preserving published history.
