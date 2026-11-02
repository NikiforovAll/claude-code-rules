import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Mr, Snapshot } from '../types'

const POLL_MS = 300_000
const FRESH_MS = 60_000
const GIT_CHANGE = /\bgit\s+(checkout|switch|push|pull|merge|rebase|reset|commit|worktree)\b|\bglab\s+mr\b/
const REMOTE_CHANGE = /\bgit\s+(remote|init|clone)\b/
const ENV = { NO_COLOR: '1', GLAB_NO_PROMPT: '1', NO_PROMPT: '1' }
const STATE: Record<string, string> = { opened: 'success', merged: 'merged', closed: 'error', locked: 'warning' }

const last = atom({ plugin: 'gitlab-mr', key: 'last' } as const, null, { shape: 'snapshot-2' })

const projects = new Map<string, Promise<string>>()
const origins = new Map<string, Promise<boolean>>()
let glabHosts: Promise<Set<string>> | undefined
let checking: Promise<Snapshot> | undefined
let again = false
let tick: { cancel: () => void } | undefined
let checkedCwd: string | undefined
let checkedAt = 0

async function run($: EngineInterface, argv: string[]) {
  const r = await $.process.run(argv, { env: ENV, timeoutMs: 20_000 })
  if (r.exitCode) throw new Error(r.stderr.trim().split(/\r?\n/).pop()?.trim() || `${argv[0]} exited ${r.exitCode}`)
  return r.stdout.trim()
}

async function glab($: EngineInterface, args: string[]) {
  return JSON.parse(await run($, ['glab', ...args, '-F', 'json']))
}

async function projectUrl($: EngineInterface) {
  const cwd = await $.session.cwd()
  let url = projects.get(cwd)
  if (!url) {
    url = glab($, ['repo', 'view']).then(r => r.web_url)
    projects.set(cwd, url)
    url.catch(() => projects.delete(cwd))
  }
  return url
}

function hostOf(url: string) {
  const m = /^[a-z][a-z0-9+.-]*:\/\/(?:[^@/]*@)?([^/:]+)/i.exec(url) ?? /^(?:[^@/]*@)?([^:/\\]+):/.exec(url)
  return m?.[1]?.toLowerCase().replace(/^ssh\./, '')
}

// The hosts glab is signed in to, read from its config file so a check spends no process on them.
async function readGlabHosts($: EngineInterface) {
  const [dir, xdg, home, profile, appData, envHost] = await Promise.all([
    $.env.get('GLAB_CONFIG_DIR'),
    $.env.get('XDG_CONFIG_HOME'),
    $.env.get('HOME'),
    $.env.get('USERPROFILE'),
    $.env.get('APPDATA'),
    $.env.get('GITLAB_HOST'),
  ])
  const files = [
    dir && `${dir}/config.yml`,
    xdg && `${xdg}/glab-cli/config.yml`,
    home && `${home}/.config/glab-cli/config.yml`,
    profile && `${profile}/.config/glab-cli/config.yml`,
    appData && `${appData}/glab-cli/config.yml`,
  ]
  const hosts = new Set(['gitlab.com'])
  if (envHost) hosts.add(hostOf(envHost) ?? envHost.toLowerCase())
  for (const file of new Set(files.filter(f => !!f) as string[])) {
    const text = await $.fs.read(file).catch(() => '')
    const section = (text.split(/^hosts:\s*$/m)[1] ?? '').split(/^\S/m)[0] ?? ''
    for (const m of section.matchAll(/^ {2,4}([^\s#:][^\s:]*):\s*$/gm)) if (m[1]) hosts.add(m[1].toLowerCase())
  }
  return hosts
}

// Only origin counts, so a repository with remotes on both GitLab and GitHub shows one band.
function isGitLab($: EngineInterface, cwd: string) {
  let r = origins.get(cwd)
  if (!r) {
    r = (async () => {
      const host = hostOf(await run($, ['git', 'remote', 'get-url', 'origin']).catch(() => ''))
      return !!host && ((await (glabHosts ??= readGlabHosts($))).has(host) || host.includes('gitlab'))
    })()
    origins.set(cwd, r)
  }
  return r
}

const words = (s: string) => s.replace(/_/g, ' ')
const stateLabel = (mr: Mr) => (mr.draft ? 'draft' : mr.state)

async function snapshot($: EngineInterface): Promise<Snapshot> {
  checkedCwd = await $.session.cwd()
  checkedAt = await $.clock.now()
  if (!(await isGitLab($, checkedCwd))) return { error: 'Not a GitLab repository: origin is not on a host glab knows.' }
  const branch = await run($, ['git', 'branch', '--show-current'])
  if (!branch) return { error: 'Detached HEAD: no branch.' }
  const list = await glab($, ['mr', 'list', '--all', '--source-branch', branch, '-P', '5'])
  const m = list.find((x: { state: string }) => x.state === 'opened') ?? list[0]
  if (!m) {
    const create = new URL(`${await projectUrl($)}/-/merge_requests/new`)
    create.searchParams.set('merge_request[source_branch]', branch)
    return { branch, create: create.href, mr: null }
  }
  const merge = m.state === 'opened' && m.detailed_merge_status !== 'mergeable' ? words(m.detailed_merge_status) : undefined
  return { branch, mr: { iid: m.iid, title: m.title, state: m.state, draft: m.draft, url: m.web_url, target: m.target_branch, merge } }
}

// One check at a time; a refresh asked for during a check runs once after it, so a branch switch mid-check is not lost.
function check($: EngineInterface): Promise<Snapshot> {
  if (checking) {
    again = true
    return checking
  }
  checking = snapshot($)
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
  const s = await check($)
  if ('error' in s) return s.error
  if (!s.mr) return `No merge request for ${s.branch}. [Create one](${s.create})`
  const { mr } = s
  const rows = [`[!${mr.iid}](${mr.url}) ${mr.title}`, `${stateLabel(mr)} · ${s.branch} → ${mr.target}${mr.merge ? ` · ${mr.merge}` : ''}`]
  if (mr.state === 'opened') {
    const p = (await glab($, ['mr', 'view', String(mr.iid)])).head_pipeline
    if (p) rows.push(`[pipeline #${p.id}](${p.web_url}) ${p.status}`)
  }
  return rows.join('  \n')
}

async function openWeb($: EngineInterface) {
  const s = (await read($, last)) ?? (await check($))
  if ('error' in s || !s.mr) return 'No merge request to open. Run /mr for details.'
  await run($, ['glab', 'mr', 'view', String(s.mr.iid), '--web'])
  return `Opened !${s.mr.iid} in the browser.`
}

async function recheckIfStale($: EngineInterface) {
  if ((await $.session.cwd()) !== checkedCwd || (await $.clock.now()) - checkedAt > FRESH_MS) await check($)
}

// A repo glab does not know stays an error until a cwd change, a git command or /mr checks again.
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
    await $.command.register({ name: 'mr', description: 'GitLab MR of this branch; `/mr web` opens it' })
    if (e.isInteractive) poll($)
    return next(e)
  })

  on('command.run', { command: 'mr' }, async ($, e) => ({ text: e.args.trim() === 'web' ? await openWeb($) : await details($) }))

  on('classic.CwdChanged', async ($, e, next) => {
    void check($)
    return next(e)
  })

  // CwdChanged does not cover every directory change (`/cd` showed the old MR), so a prompt rechecks too.
  on('prompt.submit', async ($, e, next) => {
    void recheckIfStale($).catch(() => {})
    return next(e)
  })

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const ran = await next(e)
    const remote = REMOTE_CHANGE.test(e.command)
    if (remote) origins.clear()
    if (remote || GIT_CHANGE.test(e.command)) void check($)
    return ran
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const s = await read($, last)
    if (e.props.hasSurvey || !s || 'error' in s) return next(e)
    const { Box, Text, Link } = $.ui.resolve(e)
    const { mr } = s
    return (
      <Box width="100%" justifyContent="flex-end">
        {mr ? (
          <Text>
            <Text dimColor>MR </Text>
            <Text weight="bold">
              <Link href={mr.url}>!{mr.iid}</Link>
            </Text>
            <Text color={mr.draft ? 'warning' : STATE[mr.state] ?? 'inactive'}> {stateLabel(mr)}</Text>
            {mr.merge && <Text color="warning"> · {mr.merge}</Text>}
            <Text dimColor> → {mr.target}</Text>
          </Text>
        ) : (
          <Text dimColor>
            MR none for {s.branch} · <Link href={s.create}>create</Link>
          </Text>
        )}
      </Box>
    )
  })
}
