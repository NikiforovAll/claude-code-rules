import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Mr, Snapshot } from '../types'

const POLL_MS = 60_000
const GIT_CHANGE = /\bgit\s+(checkout|switch|push|pull|merge|rebase|reset|commit|worktree)\b|\bglab\s+mr\b/
const ENV = { NO_COLOR: '1', GLAB_NO_PROMPT: '1', NO_PROMPT: '1' }
const STATE: Record<string, string> = { opened: 'success', merged: 'merged', closed: 'error', locked: 'warning' }

const last = atom({ plugin: 'gitlab-mr', key: 'last' } as const, null, { shape: 'snapshot-2' })

const projects = new Map<string, Promise<string>>()
let checking: Promise<Snapshot> | undefined
let again = false
let tick: { cancel: () => void } | undefined

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

const words = (s: string) => s.replace(/_/g, ' ')
const stateLabel = (mr: Mr) => (mr.draft ? 'draft' : mr.state)

async function snapshot($: EngineInterface): Promise<Snapshot> {
  const branch = await run($, ['git', 'branch', '--show-current'])
  if (!branch) return { error: 'Detached HEAD: no branch.' }
  const list = await glab($, ['mr', 'list', '--all', '--source-branch', branch, '-P', '5']).catch(() => {
    throw new Error('Not a GitLab repository that glab knows.')
  })
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
  if (!s.mr) return `No merge request for ${s.branch}.\nCreate one: ${s.create}`
  const { mr } = s
  const rows = [`!${mr.iid} ${mr.title}`, `${stateLabel(mr)} · ${s.branch} → ${mr.target}${mr.merge ? ` · ${mr.merge}` : ''}`, mr.url]
  if (mr.state === 'opened') {
    const p = (await glab($, ['mr', 'view', String(mr.iid)])).head_pipeline
    if (p) rows.push(`pipeline ${p.status}: ${p.web_url}`)
  }
  return rows.join('\n')
}

async function openWeb($: EngineInterface) {
  const s = (await read($, last)) ?? (await check($))
  if ('error' in s || !s.mr) return 'No merge request to open. Run /mr for details.'
  await run($, ['glab', 'mr', 'view', String(s.mr.iid), '--web'])
  return `Opened !${s.mr.iid} in the browser.`
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

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const ran = await next(e)
    if (GIT_CHANGE.test(e.command)) void check($)
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
