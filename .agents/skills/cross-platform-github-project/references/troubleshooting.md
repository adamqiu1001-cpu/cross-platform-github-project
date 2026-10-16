# Troubleshooting clone, push, and authentication

Diagnose by the error text. Every fix here changes only the local machine. Commands handed to the user start with `cd <repository>`, because they often run them from their home directory.

## `Operation timed out`, `Failed to connect`, or `Recv failure`

A network problem; credentials are not involved yet. Test with `curl -sI -m 10 https://github.com | head -1`.

Git ignores the operating system's proxy settings. When the user runs a proxy, read its address:

- macOS: `scutil --proxy | grep -E "HTTPS?(Enable|Proxy|Port)"`
- Windows: Settings → Network & Internet → Proxy, or `netsh winhttp show proxy`

Then route only GitHub through it: `git config --global http.https://github.com.proxy http://HOST:PORT`. When the proxy port changes later, rerun the command with the new port.

## Prompted for `Username` and `Password`

GitHub rejects account passwords for Git. Use one of these, in order of preference:

1. **GitHub CLI.** Run `gh auth login` and choose GitHub.com → HTTPS → authenticate Git: Yes → login with a web browser. Install it with `brew install gh` on macOS (or the `.pkg` from https://github.com/cli/cli/releases when Homebrew is absent), or `winget install GitHub.cli` on Windows.
2. **Fine-grained personal access token.** Create it at https://github.com/settings/personal-access-tokens/new: Repository access → Only select repositories → the target repository; Permissions → Contents: Read and write. Add Workflows: Read and write only when pushes change `.github/workflows/`. At the prompt, enter the GitHub username and paste the token as the password; the input stays invisible. macOS Keychain or Windows Credential Manager stores it after the first successful push.

## `403` or `Permission to ... denied to <user>`

Authentication succeeded, but the credential lacks write access to this repository. For a fine-grained token, open it at https://github.com/settings/personal-access-tokens, choose Edit, confirm the repository is selected and Contents is Read and write, then Update. The token value stays the same and takes effect immediately.

Then clear the cached credential and push again:

- macOS or Git Bash: `printf "protocol=https\nhost=github.com\n\n" | git credential reject`
- PowerShell: `"protocol=https`nhost=github.com`n" | git credential reject`

## Commit author shows `user@hostname.local`, or Git says the name and email "were configured automatically"

The Git identity was unset. Set `git config --global user.name` to the GitHub username and `git config --global user.email` to the email registered on GitHub, or to the `ID+username@users.noreply.github.com` address to keep it private. Fix the last unpushed commit with `git commit --amend --reset-author --no-edit`.

## `not a git repository`

The shell is outside the project. `cd` into the clone and rerun.

## Push rejected with `non-fast-forward` or `fetch first`

The remote has commits this machine lacks. Run `git pull --ff-only`. When that stops because the branches have diverged, show the user both sides with `git log --oneline --graph --all -20` and choose merge or rebase together. Keep the push fast-forward.
