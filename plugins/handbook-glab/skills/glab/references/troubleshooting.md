# glab Troubleshooting Guide

Comprehensive troubleshooting guide for common glab CLI issues and errors.

## Installation Issues

### Command Not Found

**Error:**
```
command not found: glab
```
or
```
glab: command not found
```

**Causes:**
- glab is not installed
- glab is not in PATH

**Solutions:**
1. Verify installation:
   ```bash
   which glab
   ```

2. Install glab if missing (see main README for installation instructions)

3. If installed but not in PATH, add to PATH:
   ```bash
   # Find where glab is installed
   find / -name glab 2>/dev/null

   # Add to PATH in ~/.bashrc or ~/.zshrc
   export PATH="$PATH:/path/to/glab"
   ```

4. For Go installation, ensure `$GOPATH/bin` is in PATH:
   ```bash
   export PATH="$PATH:$(go env GOPATH)/bin"
   ```

### Version Conflicts

**Error:**
```
glab: incompatible version
```

**Solution:**
Update to the latest version:
```bash
# macOS
brew upgrade glab

# Linux (depends on package manager)
sudo apt update && sudo apt upgrade glab
```

## Authentication Issues

### 401 Unauthorized

**Error:**
```
failed to get current user: GET https://gitlab.com/api/v4/user: 401 {message: 401 Unauthorized}
```

**Causes:**
- Not authenticated
- Token expired
- Invalid token
- Wrong GitLab instance

**Solutions:**
1. Authenticate:
   ```bash
   glab auth login
   ```

2. Check authentication status:
   ```bash
   glab auth status
   ```

3. Re-authenticate with new token:
   ```bash
   glab auth login --hostname gitlab.com --token YOUR_TOKEN
   ```

4. Verify token has correct scopes (api, read_user, write_repository)

5. For self-hosted GitLab, ensure correct hostname:
   ```bash
   glab auth login --hostname gitlab.example.org
   ```

### Token Permissions

**Error:**
```
403 Forbidden
```
or
```
insufficient permissions
```

**Causes:**
- Token lacks required scopes
- User doesn't have project permissions

**Solutions:**
1. Create new token with required scopes:
   - api
   - read_api
   - read_user
   - write_repository
   - read_repository

2. Verify project access in GitLab web UI

3. Check if project is private and token has access

### Multiple Accounts

**Issue:** Working with multiple GitLab instances

**Solution:**
glab supports multiple authenticated accounts:

```bash
# Authenticate with gitlab.com
glab auth login --hostname gitlab.com

# Authenticate with self-hosted instance
glab auth login --hostname gitlab.example.org

# Check all authenticated accounts
glab auth status

# Use specific host for command
glab mr list -R gitlab.example.org/namespace/project
```

## Repository Context Issues

### Not a Git Repository

**Error:**
```
fatal: not a git repository (or any of the parent directories): .git
```

**Causes:**
- Running glab outside a Git repository
- Git repository not initialized

**Solutions:**
1. Navigate to a Git repository:
   ```bash
   cd /path/to/your/repo
   ```

2. Or specify repository explicitly:
   ```bash
   glab mr list -R owner/repo
   ```

3. Initialize Git repository if needed:
   ```bash
   git init
   git remote add origin git@gitlab.com:owner/repo.git
   ```

### Wrong Repository Detected

**Issue:** glab operating on wrong repository

**Solution:**
1. Check current repository remote:
   ```bash
   git remote -v
   ```

2. Specify correct repository:
   ```bash
   glab mr list -R owner/correct-repo
   ```

3. Update Git remote if wrong:
   ```bash
   git remote set-url origin git@gitlab.com:owner/correct-repo.git
   ```

### 404 Project Not Found

**Error:**
```
404 Project Not Found
```

**Causes:**
- Repository doesn't exist
- Wrong namespace/project name
- No access permissions
- Wrong GitLab instance

**Solutions:**
1. Verify repository name:
   ```bash
   # Check in GitLab web UI
   # Correct format: namespace/project
   ```

2. Check you have access to the project

3. Verify GitLab instance:
   ```bash
   glab auth status
   ```

4. For self-hosted, set correct host:
   ```bash
   GITLAB_HOST=gitlab.example.org glab repo view
   ```

## Merge Request Issues

### Source Branch Already Has MR

**Error:**
```
failed to create merge request: source branch already has a merge request
```

**Cause:**
- A merge request already exists for this branch

**Solutions:**
1. List existing MRs to find it:
   ```bash
   glab mr list
   glab mr list --source-branch=$(git branch --show-current)
   ```

2. View the existing MR:
   ```bash
   glab mr view <mr-number>
   ```

3. Update existing MR instead of creating new one:
   ```bash
   glab mr update <mr-number> --title "New title"
   ```

### Cannot Merge: Conflicts Exist

**Error:**
```
Cannot merge: merge conflicts exist
```

**Solutions:**
1. Checkout MR locally:
   ```bash
   glab mr checkout <mr-number>
   ```

2. Fetch latest target branch:
   ```bash
   git fetch origin main
   ```

3. Merge or rebase:
   ```bash
   git merge origin/main
   # or
   git rebase origin/main
   ```

4. Resolve conflicts and push:
   ```bash
   git add .
   git commit
   git push
   ```

### Pipeline Must Succeed

**Error:**
```
cannot merge: pipeline must succeed
```

**Cause:**
- Project requires successful pipeline before merge
- Pipeline is failing or pending

**Solutions:**
1. Check pipeline status:
   ```bash
   glab ci status
   ```

2. View pipeline details:
   ```bash
   glab pipeline ci view
   ```

3. Fix pipeline failures and retry:
   ```bash
   glab ci retry
   ```

4. If project settings allow, force merge (not recommended):
   ```bash
   # Only if you have maintainer permissions
   glab mr merge <mr-number> --when-pipeline-succeeds
   ```

### Cannot Push to Source Branch

**Error:**
```
You cannot push commits to this source branch
```

**Cause:**
- MR is from a fork
- No write access to source repository

**Solution:**
Ask MR author to make changes, or:
1. Checkout MR:
   ```bash
   glab mr checkout <mr-number>
   ```

2. Make changes on their fork (requires special permissions)

## Pipeline/CI Issues

### Pipeline Not Found

**Error:**
```
pipeline not found
```

**Causes:**
- No pipeline exists for current branch
- Pipeline hasn't started yet

**Solutions:**
1. Trigger a pipeline:
   ```bash
   glab ci run
   ```

2. Check if .gitlab-ci.yml exists:
   ```bash
   ls -la .gitlab-ci.yml
   ```

3. Verify CI/CD is enabled in project settings

### CI Lint Errors

**Error:**
```
.gitlab-ci.yml is invalid
```

**Solutions:**
1. Lint locally:
   ```bash
   glab ci lint
   ```

2. Common issues:
   - YAML syntax errors (tabs vs spaces)
   - Invalid job names
   - Missing required fields
   - Incorrect indentation

3. Use GitLab CI/CD config validation in web UI

4. Check GitLab CI/CD documentation for syntax

### Cannot Download Artifacts

**Error:**
```
failed to download artifacts
```

**Causes:**
- Artifacts expired
- Job didn't produce artifacts
- Permission issues

**Solutions:**
1. Check if job has artifacts:
   ```bash
   glab ci view <pipeline-id>
   ```

2. Verify artifacts haven't expired (check project settings)

3. Run job again if needed:
   ```bash
   glab ci retry
   ```

## Network and Connection Issues

### Connection Timeout

**Error:**
```
dial tcp: i/o timeout
```

**Causes:**
- Network connectivity issues
- Firewall blocking connection
- GitLab instance down

**Solutions:**
1. Check network connection:
   ```bash
   ping gitlab.com
   ```

2. Verify GitLab status:
   ```bash
   curl -I https://gitlab.com
   ```

3. Check firewall/proxy settings

4. For self-hosted, verify hostname:
   ```bash
   ping gitlab.example.org
   ```

### SSL Certificate Issues

**Error:**
```
x509: certificate signed by unknown authority
```

**Causes:**
- Self-signed certificate
- Corporate proxy
- Invalid SSL certificate

**Solutions:**
1. For development/testing only (NOT production):
   ```bash
   export GIT_SSL_NO_VERIFY=true
   ```

2. Add certificate to system trust store (preferred)

3. Configure Git to use specific CA bundle:
   ```bash
   git config --global http.sslCAInfo /path/to/cert.pem
   ```

## Environment Variable Issues

### GITLAB_HOST Not Recognized

**Issue:** Commands still using gitlab.com instead of self-hosted instance

**Solutions:**
1. Export variable in current shell:
   ```bash
   export GITLAB_HOST=gitlab.example.org
   ```

2. Add to shell profile (~/.bashrc, ~/.zshrc):
   ```bash
   echo 'export GITLAB_HOST=gitlab.example.org' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Or use flag for each command:
   ```bash
   glab mr list -R gitlab.example.org/owner/repo
   ```

### GITLAB_TOKEN Not Working

**Issue:** Token set but authentication still failing

**Solutions:**
1. Verify token is exported:
   ```bash
   echo $GITLAB_TOKEN
   ```

2. Ensure no spaces in token:
   ```bash
   export GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
   ```

3. Token should not be quoted in export:
   ```bash
   # Correct
   export GITLAB_TOKEN=glpat-xxx

   # Incorrect
   export GITLAB_TOKEN="glpat-xxx"
   ```

4. Verify token is valid in GitLab web UI

## Output and Display Issues

### Garbled or Missing Output

**Issue:** Terminal output is corrupted or incomplete

**Solutions:**
1. Disable glamour styling:
   ```bash
   export GLAMOUR_STYLE=notty
   ```

2. Use plain text output:
   ```bash
   glab mr list --output=text
   ```

3. Update terminal emulator

4. Try different pager:
   ```bash
   export PAGER=less
   ```

### JSON Parsing Errors

**Issue:** Cannot parse JSON output

**Solutions:**
1. Ensure command supports JSON:
   ```bash
   glab mr list --output=json
   ```

2. Pipe through jq for validation:
   ```bash
   glab mr list --output=json | jq '.'
   ```

3. Check for error messages mixed with JSON

## Performance Issues

### Commands Running Slowly

**Causes:**
- Large repository
- Many results being fetched
- Network latency

**Solutions:**
1. Limit results:
   ```bash
   glab mr list --per-page=10 --page=1
   ```

2. Use specific filters:
   ```bash
   glab mr list --assignee=@me --state=opened
   ```

3. Disable web browser opening:
   ```bash
   glab mr view 123 --web=false
   ```

## Configuration Issues

### Config File Corruption

**Error:**
```
failed to load config
```

**Solutions:**
1. Check config file:
   ```bash
   cat ~/.config/glab-cli/config.yml
   ```

2. Backup and recreate:
   ```bash
   mv ~/.config/glab-cli/config.yml ~/.config/glab-cli/config.yml.bak
   glab auth login
   ```

3. Manually edit config:
   ```bash
   vim ~/.config/glab-cli/config.yml
   ```

## General Troubleshooting Steps

When encountering any error:

1. **Check version:**
   ```bash
   glab version
   ```

2. **Update glab:**
   ```bash
   glab check-update
   ```

3. **Enable verbose output:**
   ```bash
   glab <command> --verbose
   ```

4. **Check authentication:**
   ```bash
   glab auth status
   ```

5. **Verify repository context:**
   ```bash
   git remote -v
   ```

6. **Use --help:**
   ```bash
   glab <command> --help
   ```

7. **Check GitLab API status:**
   Visit https://status.gitlab.com

8. **Review logs:**
   ```bash
   # Check recent commands
   history | grep glab
   ```

## Getting Additional Help

If issues persist:

1. Check glab documentation: https://docs.gitlab.com/editor_extensions/gitlab_cli/
2. Search glab issues: https://gitlab.com/gitlab-org/cli/-/issues
3. Create a new issue with:
   - glab version
   - Operating system
   - Full error message
   - Steps to reproduce
   - Output with --verbose flag
