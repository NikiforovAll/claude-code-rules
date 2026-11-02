import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Pr, Snapshot } from '../types'

const POLL_MS = 300_000
const FRESH_MS = 60_000
const CACHE = '60s'
const GIT_CHANGE = /\bgit\s+(checkout|switch|push|pull|merge|rebase|reset|commit|worktree)\b|\bgh\s+pr\b/
const REMOTE_CHANGE = /\bgit\s+(remote|init|clone)\b/
const ENV = { NO_COLOR: '1', GH_PROMPT_DISABLED: '1', GH_NO_UPDATE_NOTIFIER: '1' }
const STATE: Record<string, string> = { open: 'success', merged: 'merged', closed: 'error' }

const last = atom({ plugin: 'github-pr', key: 'last' } as const, null, { shape: 'snapshot-1' })

type Repo = { owner: string; url: string }

const repos = new Map<string, Promise<Repo>>()
const origins = new Map<string, Promise<boolean>>()
let ghHosts: Promise<Set<string>> | undefined
let checking: Promise<Snapshot> | undefined
let again = false
let fresh = false
let tick: { cancel: () => void } | undefined
let checkedCwd: string | undefined
let checkedAt = 0

async function run($: EngineInterface, argv: string[]) {
  const r = await $.process.run(argv, { env: ENV, timeoutMs: 20_000 })
  if (r.exitCode) throw new Error(r.stderr.trim().split(/\r?\n/).pop()?.trim() || `${argv[0]} exited ${r.exitCode}`)
  return r.stdout.trim()
}

// `gh api --cache` answers repeats from disk, so polling from several sessions spends one request per window.
async function api($: EngineInterface, args: string[], cache?: string) {
  return JSON.parse(await run($, ['gh', 'api', ...args, ...(cache ? ['--cache', cache] : [])]))
}

async function repo($: EngineInterface, cwd: string) {
  let r = repos.get(cwd)
  if (!r) {
    r = api($, ['repos/{owner}/{repo}'], '1h').then(x => ({ owner: x.owner.login, url: x.html_url }))
    repos.set(cwd, r)
    r.catch(() => repos.delete(cwd))
  }
  return r
}

function hostOf(url: string) {
  const m = /^[a-z][a-z0-9+.-]*:\/\/(?:[^@/]*@)?([^/:]+)/i.exec(url) ?? /^(?:[^@/]*@)?([^:/\\]+):/.exec(url)
  return m?.[1]?.toLowerCase().replace(/^ssh\./, '')
}

// The hosts gh is signed in to, read from its hosts file so a check spends no process on them.
async function readGhHosts($: EngineInterface) {
  const [dir, xdg, appData, home, profile, envHost] = await Promise.all([
    $.env.get('GH_CONFIG_DIR'),
    $.env.get('XDG_CONFIG_HOME'),
    $.env.get('APPDATA'),
    $.env.get('HOME'),
    $.env.get('USERPROFILE'),
    $.env.get('GH_HOST'),
  ])
  const files = [
    dir && `${dir}/hosts.yml`,
    xdg && `${xdg}/gh/hosts.yml`,
    appData && `${appData}/GitHub CLI/hosts.yml`,
    home && `${home}/.config/gh/hosts.yml`,
    profile && `${profile}/.config/gh/hosts.yml`,
  ]
  const hosts = new Set(['github.com'])
  if (envHost) hosts.add(hostOf(envHost) ?? envHost.toLowerCase())
  for (const file of new Set(files.filter(f => !!f) as string[])) {
    const text = await $.fs.read(file).catch(() => '')
    for (const m of text.matchAll(/^([^\s#:][^\s:]*):\s*$/gm)) if (m[1]) hosts.add(m[1].toLowerCase())
  }
  return hosts
}

// Only origin counts, so a repository with remotes on both GitLab and GitHub shows one band.
function isGitHub($: EngineInterface, cwd: string) {
  let r = origins.get(cwd)
  if (!r) {
    r = (async () => {
      const host = hostOf(await run($, ['git', 'remote', 'get-url', 'origin']).catch(() => ''))
      return !!host && ((await (ghHosts ??= readGhHosts($))).has(host) || host.includes('github'))
    })()
    origins.set(cwd, r)
  }
  return r
}

const stateOf =(x: { state: string; merged_at: string | null }) => (x.merged_at ? 'merged' : x.state)
const stateLabel = (pr: Pr) => (pr.draft && pr.state === 'open' ? 'draft' : pr.state)

async function snapshot($: EngineInterface, bypassCache: boolean): Promise<Snapshot> {
  checkedCwd = await $.session.cwd()
  checkedAt = await $.clock.now()
  if (!(await isGitHub($, checkedCwd))) return { error: 'Not a GitHub repository: origin is not on a host gh knows.' }
  const branch = await run($, ['git', 'branch', '--show-current'])
  if (!branch) return { error: 'Detached HEAD: no branch.' }
  const { owner, url } = await repo($, checkedCwd)
  const list = await api(
    $,
    ['-X', 'GET', 'repos/{owner}/{repo}/pulls', '-f', `head=${owner}:${branch}`, '-f', 'state=all', '-f', 'per_page=5'],
    bypassCache ? undefined : CACHE,
  )
  const p = list.find((x: { state: string }) => x.state === 'open') ?? list[0]
  if (!p) return { branch, create: `${url}/compare/${encodeURIComponent(branch)}?expand=1`, pr: null }
  return {
    branch,
    pr: { number: p.number, title: p.title, state: stateOf(p), draft: p.draft, url: p.html_url, target: p.base.ref },
  }
}

// One check at a time; a refresh asked for during a check runs once after it, so a branch switch mid-check is not lost.
function check($: EngineInterface, bypassCache = false): Promise<Snapshot> {
  fresh ||= bypassCache
  if (checking) {
    again = true
    return checking
  }
  const bypass = fresh
  fresh = false
  checking = snapshot($, bypass)
    .catch((err: Error): Snapshot => ({ error: err.message }))
    .then(async s => {
      const prev = await read($, last)
      if (JSON.stringify(prev) !== JSON.stringify(s)) await update($, last, () => s)
      return s
    })
    .finally(() => {
      checking = undefined
      if (again) {
        again = false
        void check($)
      }
    })
  return checking
}

async function details($: EngineInterface) {
  const s = await check($, true)
  if ('error' in s) return s.error
  if (!s.pr) return `No pull request for ${s.branch}. [Create one](${s.create})`
  const { pr } = s
  const rows = [`[#${pr.number}](${pr.url}) ${pr.title}`]
  let status = `${stateLabel(pr)} · ${s.branch} → ${pr.target}`
  if (pr.state === 'open') {
    const full = await api($, [`repos/{owner}/{repo}/pulls/${pr.number}`])
    if (full.mergeable_state && full.mergeable_state !== 'clean') status += ` · ${full.mergeable_state}`
    rows.push(status)
    const runs: { conclusion: string | null }[] = (await api($, [`repos/{owner}/{repo}/commits/${full.head.sha}/check-runs`]))
      .check_runs
    if (runs.length) {
      const counts = new Map<string, number>()
      for (const r of runs) counts.set(r.conclusion ?? 'running', (counts.get(r.conclusion ?? 'running') ?? 0) + 1)
      rows.push(`checks: ${[...counts].map(([k, n]) => `${n} ${k}`).join(', ')}`)
    }
  } else rows.push(status)
  return rows.join('  \n')
}

async function openWeb($: EngineInterface) {
  const s = (await read($, last)) ?? (await check($))
  if ('error' in s || !s.pr) return 'No pull request to open. Run /gh-pr for details.'
  await run($, ['gh', 'browse', String(s.pr.number)])
  return `Opened #${s.pr.number} in the browser.`
}

async function recheckIfStale($: EngineInterface) {
  if ((await $.session.cwd()) !== checkedCwd || (await $.clock.now()) - checkedAt > FRESH_MS) await check($)
}

// A repo gh does not know stays an error until a cwd change, a git command or /gh-pr checks again.
function poll($: EngineInterface) {
  tick?.cancel()
  tick = $.clock.every(POLL_MS, async () => {
    const s = await read($, last)
    if (!s || !('error' in s)) void check($)
  })
  void check($)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'gh-pr', description: 'GitHub PR of this branch; `/gh-pr web` opens it' })
    if (e.isInteractive) poll($)
    return next(e)
  })

  on('command.run', { command: 'gh-pr' }, async ($, e) => ({ text: e.args.trim() === 'web' ? await openWeb($) : await details($) }))

  on('classic.CwdChanged', async ($, e, next) => {
    void check($)
    return next(e)
  })

  // CwdChanged does not cover every directory change, so a prompt rechecks too.
  on('prompt.submit', async ($, e, next) => {
    void recheckIfStale($).catch(() => {})
    return next(e)
  })

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const ran = await next(e)
    const remote = REMOTE_CHANGE.test(e.command)
    if (remote) origins.clear()
    if (remote || GIT_CHANGE.test(e.command)) void check($, true)
    return ran
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const s = await read($, last)
    if (e.props.hasSurvey || !s || 'error' in s) return next(e)
    const { Box, Text, Link } = $.ui.resolve(e)
    const { pr } = s
    return (
      <Box width="100%" justifyContent="flex-end">
        {pr ? (
          <Text>
            <Text dimColor>PR </Text>
            <Text weight="bold">
              <Link href={pr.url}>#{pr.number}</Link>
            </Text>
            <Text color={stateLabel(pr) === 'draft' ? 'warning' : STATE[pr.state] ?? 'inactive'}> {stateLabel(pr)}</Text>
            <Text dimColor> → {pr.target}</Text>
          </Text>
        ) : (
          <Text dimColor>
            PR none for {s.branch} · <Link href={s.create}>create</Link>
          </Text>
        )}
      </Box>
    )
  })
}
