export type Pr = {
  number: number
  title: string
  /** `open`, `closed` or `merged`. */
  state: string
  draft: boolean
  url: string
  target: string
}
export type Snapshot = { branch: string; pr: Pr } | { branch: string; create: string; pr: null } | { error: string }

declare module 'claude-code' {
  interface PluginState {
    'github-pr': { last: Shaped<Snapshot | null> }
  }
}
