# How to Run Ralph (Claude Code Edition) - Step-by-Step Guide

## What is Ralph?

Ralph is an autonomous AI agent that automatically implements features from a Product Requirements Document (PRD). It works by:
1. Reading your PRD (a JSON file with user stories)
2. Picking one story at a time
3. Implementing it with Claude Code AI assistance
4. Testing and committing the changes
5. Repeating until all stories are done

---

## Prerequisites Checklist

Before running Ralph, you need:

### 1. Claude Code CLI

Install the Claude Code CLI from Anthropic:

**Option A: Using npm (Recommended)**
```bash
npm install -g @anthropic-ai/claude-code
```

**Option B: macOS/Linux**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Option C: Windows (PowerShell)**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Option D: Homebrew (macOS)**
```bash
brew install --cask claude-code
```

Verify installation:
```bash
claude --version
```

### 2. Authenticate Claude Code

```bash
claude auth login
```

Or set the API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. jq (JSON processor)

**macOS:**
```bash
brew install jq
```

**Windows (Chocolatey):**
```powershell
choco install jq
```

**Windows (Scoop):**
```powershell
scoop install jq
```

**Linux:**
```bash
sudo apt-get install jq
```

### 4. Git

Make sure you have git installed and configured:
```bash
git --version
```

---

## Step-by-Step: Running Ralph

### Step 1: Set Up Your Project

Ralph needs to run **inside your project directory** (not in the Ralph repo itself).

1. Navigate to your project:
   ```bash
   cd /path/to/your/project
   ```

2. Make sure it's a git repository:
   ```bash
   git status
   ```
   If it's not a git repo, initialize it:
   ```bash
   git init
   ```

### Step 2: Copy Ralph Files to Your Project

Copy the Ralph files into your project:

```bash
# Create a scripts/ralph directory
mkdir -p scripts/ralph

# Copy the files (adjust the path to where Ralph is installed)
cp /path/to/ralph/ralph.sh scripts/ralph/
cp /path/to/ralph/prompt.md scripts/ralph/

# Make the script executable
chmod +x scripts/ralph/ralph.sh
```

### Step 3: Create a PRD (Product Requirements Document)

You need a PRD that describes what you want to build. There are two ways:

#### Option A: Use the PRD Skill (Recommended)

1. Make sure the PRD skill is installed:
   ```bash
   # Copy the skill to your Claude Code config
   cp -r /path/to/ralph/skills/prd ~/.claude/skills/
   ```

2. In your project, ask Claude Code:
   ```
   Load the prd skill and create a PRD for [describe your feature]
   ```

3. Answer the clarifying questions

4. The skill will create a file like `tasks/prd-[feature-name].md`

#### Option B: Create PRD Manually

Create a markdown file describing your feature with user stories. See `prd.json.example` for the structure.

### Step 4: Convert PRD to JSON Format

Ralph needs the PRD in JSON format:

1. Make sure the Ralph skill is installed:
   ```bash
   cp -r /path/to/ralph/skills/ralph ~/.claude/skills/
   ```

2. In your project, ask Claude Code:
   ```
   Load the ralph skill and convert tasks/prd-[feature-name].md to prd.json
   ```

3. This creates `prd.json` in your scripts/ralph directory

### Step 5: Run Ralph!

Once you have `prd.json`, you can run Ralph:

```bash
cd scripts/ralph
./ralph.sh
```

**Default:** Ralph runs for 10 iterations. To change:
```bash
./ralph.sh 20  # Run for 20 iterations max
```

---

## What Happens When Ralph Runs?

1. **Creates a feature branch** (from the `branchName` in prd.json)
2. **Picks the highest priority story** where `passes: false`
3. **Implements that story** using Claude Code
4. **Runs quality checks** (typecheck, tests, etc.)
5. **Commits if checks pass**
6. **Updates prd.json** to mark story as `passes: true`
7. **Repeats** until all stories are done or max iterations reached

---

## Windows Users

On Windows, you have several options to run the bash script:

### Option A: Git Bash (Recommended)
Git Bash comes with Git for Windows and can run bash scripts:
```bash
# Open Git Bash
cd /c/path/to/your/project/scripts/ralph
./ralph.sh
```

### Option B: WSL (Windows Subsystem for Linux)
If you have WSL installed:
```bash
# Open WSL terminal
cd /mnt/c/path/to/your/project/scripts/ralph
./ralph.sh
```

### Option C: PowerShell Version
If you need a native PowerShell version, let me know and I can help create one.

---

## Troubleshooting

### "claude: command not found"
- Install Claude Code CLI (see Prerequisites section)
- Make sure it's in your PATH
- Try restarting your terminal

### "jq: command not found"
- Install jq (see Prerequisites section)
- On Windows, restart your terminal after installation

### "prd.json not found"
- Make sure you've converted your PRD to JSON format
- Check that prd.json is in the same directory as ralph.sh

### "Permission denied"
- Make the script executable: `chmod +x ralph.sh`
- On Windows, use Git Bash or WSL

### Claude Code authentication failed
- Run `claude auth login` to re-authenticate
- Check your ANTHROPIC_API_KEY environment variable

---

## Quick Start Example

Let's say you want to add a "task priority" feature:

1. **Create PRD:**
   ```
   Load the prd skill and create a PRD for adding priority levels to tasks
   ```

2. **Convert to JSON:**
   ```
   Load the ralph skill and convert tasks/prd-task-priority.md to prd.json
   ```

3. **Run Ralph:**
   ```bash
   ./scripts/ralph/ralph.sh
   ```

4. **Watch it work!** Ralph will implement each story one by one.

---

## Need Help?

If you get stuck:
1. Check that all prerequisites are installed
2. Make sure you're in your project directory (not the Ralph repo)
3. Verify prd.json exists and is valid JSON
4. Check the `progress.txt` file for what Ralph has learned
5. Review git log to see what commits Ralph has made
