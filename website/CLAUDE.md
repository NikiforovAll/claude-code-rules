# CLAUDE.md

- Source docs in `website/docs/`
- Configuration in `website/docusaurus.config.js`
- Build and deploy via standard Docusaurus commands


Docusaurus-based documentation site deployed at [nikiforovall.blog/claude-code-rules](https://nikiforovall.blog/claude-code-rules)

## Guidelines

* When updating the location of documentation files, ensure referential integrity by updating all relevant links within the repository to point to the new locations. This includes links in markdown files, configuration files, and any other references that may exist throughout the codebase as part of `website` folder.
* Use `npm run build` to verify that the Docusaurus site builds successfully after making changes.