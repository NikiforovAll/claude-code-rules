# Quickstart: Manual Testing Guide

## Overview
This document provides step-by-step instructions for manually testing the Docusaurus static website implementation. Follow these steps to verify that all acceptance criteria are met.

## Prerequisites
- Node.js 18+ installed
- Git repository cloned locally
- Web browser (Chrome, Firefox, or Edge)

## Test Scenario 1: Local Development Environment

### Setup
1. Navigate to website directory:
   ```bash
   cd website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```

### Expected Result
- Development server starts without errors
- Browser automatically opens to `http://localhost:3000`
- Homepage loads within 3 seconds

### Verification Checklist
- [ ] No build errors in terminal
- [ ] Homepage displays with title "Claude Code Handbook"
- [ ] Dark mode toggle works
- [ ] Mobile responsive menu works (resize browser)

## Test Scenario 2: Homepage Navigation

### Steps
1. From homepage, verify presence of:
   - Introduction text about Claude Code Handbook
   - Link/card to "Best Practices" section
   - Link/card to "Tips & Tricks" section
   - Footer with links to community resources

2. Click "Best Practices" navigation item

### Expected Result
- Navigates to Best Practices index page
- Sidebar shows hierarchical structure:
  - Planning & Problem Solving (category)
  - Context Engineering (category)
  - Tips for Success
  - Customization

### Verification Checklist
- [ ] Navigation occurs instantly (client-side routing)
- [ ] Sidebar remains visible and accessible
- [ ] Breadcrumb shows current location
- [ ] Search box is visible in navbar

## Test Scenario 3: Content Navigation & Structure

### Steps
1. In sidebar, expand "Planning & Problem Solving" category

2. Click "Test-Driven Development" page

3. Verify page content:
   - Title matches: "Test-Driven Development"
   - Content includes all original text from BEST-PRACTICES.md
   - Code examples render with syntax highlighting
   - Internal links work correctly

4. Click an internal link to another documentation page

### Expected Result
- TDD page loads with full content
- All formatting preserved (headings, lists, code blocks)
- Links navigate to correct pages
- Browser back button works

### Verification Checklist
- [ ] All text from source file present
- [ ] Code blocks have correct syntax highlighting
- [ ] Inline code formatted correctly
- [ ] Bold, italic, and other markdown formatting preserved
- [ ] Lists render correctly (ordered and unordered)
- [ ] No broken links

## Test Scenario 4: Search Functionality

### Steps
1. Click search box in navbar (or press Ctrl+K / Cmd+K)

2. Type "git worktree" in search box

3. Review search results

4. Click first result

### Expected Result
- Search modal appears
- Results show "Use git worktree for parallel development" page
- Clicking result navigates to that page
- Search highlights matched terms

### Verification Checklist
- [ ] Search modal opens with keyboard shortcut
- [ ] Search finds content across all pages
- [ ] Results are relevant to search query
- [ ] Clicking result closes modal and navigates
- [ ] Search works on mobile (responsive)

## Test Scenario 5: Mobile Responsiveness

### Steps
1. Resize browser to mobile width (< 768px) OR use browser dev tools device emulation

2. Verify:
   - Hamburger menu icon appears
   - Click hamburger to open sidebar
   - Navigate to a page
   - Try search functionality

### Expected Result
- Layout adapts to narrow screen
- Sidebar becomes collapsible menu
- All content readable without horizontal scroll
- Touch targets appropriately sized

### Verification Checklist
- [ ] Hamburger menu visible on mobile
- [ ] Sidebar slides in/out smoothly
- [ ] Content doesn't overflow
- [ ] Search works on mobile
- [ ] Dark mode toggle accessible

## Test Scenario 6: Dark Mode

### Steps
1. Click dark mode toggle in navbar

2. Verify theme changes:
   - Background becomes dark
   - Text becomes light
   - Code blocks adjust colors
   - Links remain visible

3. Toggle back to light mode

### Expected Result
- Smooth transition between themes
- All content remains readable
- Theme preference persists on page navigation
- Syntax highlighting adapts to theme

### Verification Checklist
- [ ] Theme toggle button visible
- [ ] Dark mode applies to entire site
- [ ] Code syntax highlighting readable in both themes
- [ ] Images/diagrams remain visible
- [ ] Theme persists across page loads

## Test Scenario 7: Content Accuracy Verification

### Steps
1. Open original `BEST-PRACTICES.md` file

2. Navigate to "Planning & Problem Solving" section in website

3. Compare content:
   - Check each subsection exists as separate page
   - Verify all text present
   - Check code examples match
   - Verify links converted correctly

4. Repeat for TIPS-AND-TRICKS.md

### Expected Result
- 100% of content migrated
- No information loss
- All sections accessible
- Original files unchanged

### Verification Checklist
- [ ] All major sections from BEST-PRACTICES.md present
- [ ] All tips from TIPS-AND-TRICKS.md present
- [ ] Code examples identical to source
- [ ] External links work
- [ ] Internal cross-references work
- [ ] Original .md files untouched in repository root

## Test Scenario 8: Production Build

### Steps
1. Stop development server (Ctrl+C)

2. Build for production:
   ```bash
   npm run build
   ```

3. Serve production build locally:
   ```bash
   npm run serve
   ```

4. Open browser to `http://localhost:3000`

5. Perform quick smoke test:
   - Homepage loads
   - Navigate to 2-3 pages
   - Try search
   - Test dark mode

### Expected Result
- Build completes without errors or warnings
- Production site loads faster than dev mode
- All functionality works identically
- No console errors in browser

### Verification Checklist
- [ ] Build succeeds (exit code 0)
- [ ] No warnings about broken links
- [ ] Bundle size reasonable (< 5MB total)
- [ ] Pages load quickly (< 3s)
- [ ] Search index generated
- [ ] Service worker registered (optional)

## Test Scenario 9: GitHub Pages Deployment (Post-Merge)

### Prerequisites
- Changes merged to main branch
- GitHub Actions workflow triggered

### Steps
1. Go to repository on GitHub

2. Click "Actions" tab

3. Find latest workflow run for "Deploy to GitHub Pages"

4. Verify workflow completed successfully

5. Navigate to GitHub Pages URL (https://[username].github.io/claude-code-rules)

6. Perform full acceptance test on live site

### Expected Result
- Workflow completes without errors
- Site accessible at GitHub Pages URL
- All functionality works on public site
- HTTPS enabled

### Verification Checklist
- [ ] GitHub Actions workflow succeeds
- [ ] Site accessible via GitHub Pages URL
- [ ] All pages load correctly
- [ ] Search works
- [ ] Dark mode works
- [ ] Mobile responsive
- [ ] No mixed content warnings (HTTPS)

## Known Limitations & Acceptable Deviations

**Performance**:
- First page load may take up to 3 seconds (acceptable per requirements)
- Subsequent navigation should be instant due to client-side routing

**Original Files**:
- BEST-PRACTICES.md and TIPS-AND-TRICKS.md remain in repository root
- Users can still view/edit these files if needed
- Website files live in `website/` directory

**Content Splitting**:
- Long pages split at H2 headings for better navigation
- All content preserved, just reorganized

## Troubleshooting

**Build Fails**:
- Check Node.js version (must be 18+)
- Delete `node_modules` and `package-lock.json`, reinstall
- Check for broken markdown or invalid front matter

**Links Broken**:
- Verify link format matches Docusaurus conventions
- Use relative paths for internal links
- Check sidebar configuration references correct files

**Search Not Working**:
- Ensure build completed successfully
- Check that search plugin enabled in config
- Verify search index generated in build output

## Completion Criteria

All scenarios must pass for feature to be considered complete:
- ✅ Local development works
- ✅ All content migrated accurately
- ✅ Navigation and sidebar functional
- ✅ Search works across all pages
- ✅ Mobile responsive
- ✅ Dark mode functional
- ✅ Production build succeeds
- ✅ GitHub Pages deployment successful
- ✅ Original files untouched
