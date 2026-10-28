# Cross-Platform GitHub Project Skill

Codex skill source for initializing projects with a shared GitHub repository, consistent cross-platform source, locked dependencies, and separate Windows/macOS build paths.

## Contents

- `.agents/skills/cross-platform-github-project/SKILL.md` — reusable workflow instructions.
- `.agents/skills/cross-platform-github-project/references/troubleshooting.md` — official CLI installation/login, direct uploads, and fixes for proxy, permissions and divergent upload history.
- `.agents/skills/cross-platform-github-project/agents/openai.yaml` — Codex interface metadata.

## Use on another computer

Clone this repository, then copy `.agents/skills/cross-platform-github-project` into that computer's Codex skills directory:

- Windows: `%USERPROFILE%\.codex\skills\cross-platform-github-project`
- macOS: `~/.codex/skills/cross-platform-github-project`

Alternatively, open this repository as a Codex workspace and invoke the skill from the project-local `.agents/skills` location.

### Claude

The same `SKILL.md` works in Claude without changes (`agents/openai.yaml` is Codex-only and is ignored).

- Claude Code (terminal or the desktop Code tab): copy the skill folder to `~/.claude/skills/cross-platform-github-project` on macOS, or `%USERPROFILE%\.claude\skills\cross-platform-github-project` on Windows. To scope it to one project, use that project's `.claude/skills/` instead.
- Claude desktop Cowork: skills are stored on the Claude account, not on disk. Upload `dist/cross-platform-github-project.zip` under Customize → Skills, or ask Claude in Cowork to install it from this repository.

Skills installed for Claude Code and for Cowork are configured separately; install in both if both are used.

## Cross-platform collaboration

Keep skill and project source in Git; do not commit credentials, machine-specific settings, dependencies, generated installers, or build output. Use LF line endings for portable text files. For ordinary project repositories, commit the ecosystem's dependency lockfile and runtime version file, and build Windows and macOS installers on their respective operating systems.

Commit and push completed work so every machine can fetch the same source. Use branches and pull requests when changes are developed concurrently. See the safe synchronization steps below before switching computers.

## 本项目在 Windows / macOS 上使用

仓库：`adamqiu1001-cpu/cross-platform-github-project`，可见性：公开。

每台电脑各自克隆仓库。下载公开源码无需登录；推送修改仍需使用具有写入权限的 GitHub 账号认证：

```sh
git clone https://github.com/adamqiu1001-cpu/cross-platform-github-project.git
cd cross-platform-github-project
git pull --ff-only
```

本项目只有 Skill 文本和使用 Python 标准库的检查、打包脚本，没有第三方运行依赖，所以不需要安装依赖或生成依赖锁文件。推荐 Python 3.12，版本记录于 `.python-version`。

两种系统使用相同的检查和打包命令（macOS 可使用 `python3`）：

```sh
python scripts/skill.py check
python scripts/skill.py package
```

生成的 `dist/cross-platform-github-project.zip` 只包含 Skill 源码，不提交到 Git。ZIP 可以在 Windows 和 macOS 通用；GitHub Actions 分别在这两种系统上检查、打包，并保留构建产物。

工作开始前检查 `git status`；有未提交修改时先提交到当前分支，再同步远端。普通同步使用 `git pull --ff-only`，如果分支已分叉，检查双方提交后再选择合并或变基。不要用强制推送、硬重置覆盖另一台电脑上的修改。

首次完成克隆后，可分别运行以下仓库级设置，使同步默认只接受快进，并保留中文路径的可读性：

```sh
git config --local pull.ff only
git config --local core.quotepath false
```

GitHub 插件连接和本机 Git 身份验证是两套独立配置；首次克隆或推送可能需要在 GitHub 的正常登录流程中完成认证。

## 直接上传，无需 Chrome 逐个上传文件

技能优先使用 Git 直接推送，配合 GitHub 官方 CLI（`gh`）登录和管理 Pull Request。首次登录可能需要在浏览器完成一次设备码、邮箱或双重验证；之后可直接对 Codex 说：“把本次修改上传到 GitHub，并更新现有 Pull Request。”每台电脑分别登录，凭据不随技能包分发。

- Mac 有 Homebrew：`brew install gh`；没有 Homebrew：从 [官方 Releases](https://github.com/cli/cli/releases/latest) 下载对应芯片的 ZIP，校验后解压，通过完整路径运行 `bin/gh`。不必为了上传安装 Python。
- Windows：`winget install --id GitHub.cli --exact`，并确认 Git 已安装。
- 登录：`gh auth login --hostname github.com --git-protocol https --web`。完成网页验证后，用 `gh auth status` 核对账号及安全存储，再用 `gh auth setup-git --hostname github.com` 配置 Git 的登录方式；多账号环境先检查已有凭据配置。

连接器可读但写入报 403 时，技能会检查本机 CLI 权限；不会直接转为 Chrome 上传，也不会先清空旧凭据。上传后会核对远端提交和 Pull Request；遇到本地与网页提交历史不同，会保留原分支并比较差异，避免覆盖之前的工作。
