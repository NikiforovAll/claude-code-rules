import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Claude Code Handbook',
  tagline: 'Best practices and tips for using Claude Code effectively',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://nikiforovall.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/claude-code-rules/',

  // GitHub pages deployment config.
  organizationName: 'nikiforovall', // GitHub org/user name
  projectName: 'claude-code-rules', // Repo name

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Serve docs at the root
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/nikiforovall/claude-code-rules/edit/main/website/',
        },
        blog: false, // Disable blog functionality
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [
    '@docusaurus/theme-mermaid',
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        indexDocs: true,
        indexBlog: false,
        docsRouteBasePath: '/',
        language: ['en'],
        highlightSearchTermsOnTargetPage: true,
      },
    ],
  ],

  markdown: {
    mermaid: true,
  },

  themeConfig: {
    // Replace with your project's social card
    image: 'img/cch-social.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Claude Code Handbook 🚀',
      logo: {
        alt: 'Claude Code Logo',
        src: 'img/cc.png',
      },
      items: [
        {
          to: '/best-practices',
          label: 'Best Practices',
          position: 'left',
        },
        {
          to: '/tips-and-tricks/use-cc-alias',
          label: 'Tips & Tricks',
          position: 'left',
        },
        {
          to: '/plugins',
          label: '🔌 Plugins',
          position: 'right',
        },
        {
          href: 'https://github.com/nikiforovall/claude-code-rules',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Best Practices',
              to: '/best-practices',
            },
            {
              label: 'Tips & Tricks',
              to: '/tips-and-tricks/use-cc-alias',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/nikiforovall/claude-code-rules',
            },
            {
              label: 'Claude Code Docs',
              href: 'https://docs.claude.com/en/docs/claude-code/overview',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} nikiforovall.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'markdown'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
