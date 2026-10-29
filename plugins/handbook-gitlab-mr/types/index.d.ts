export type Mr = {
  iid: number
  title: string
  state: string
  draft: boolean
  url: string
  target: string
  /** Why an open MR cannot merge yet, in words; absent when it can. */
  merge?: string
}
export type Snapshot = { branch: string; mr: Mr } | { branch: string; create: string; mr: null } | { error: string }

declare module 'claude-code' {
  interface PluginState {
    'gitlab-mr': { last: Shaped<Snapshot | null> }
  }
}
