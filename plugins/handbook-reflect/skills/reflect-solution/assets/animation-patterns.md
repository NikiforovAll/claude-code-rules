# Animation patterns — for the reflect aesthetic

Slim crib sheet for the agent. Match the "Editorial / Magazine" feeling: staggered text reveals, strong type hierarchy, restrained motion.

## Reveal patterns (already wired in template.html)

```css
/* Fade + slight slide up — the default */
.reveal {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.visible .reveal { opacity: 1; transform: translateY(0); }
.slide.visible .reveal:nth-child(N) { transition-delay: calc(0.05s + N * 0.1s); }
```

**When to add new variants:**

```css
/* Slide from left — for nav rails or side accents */
.reveal-left { opacity: 0; transform: translateX(-30px); transition: opacity 0.5s, transform 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.slide.visible .reveal-left { opacity: 1; transform: translateX(0); }

/* Scale in — for hero pitch on title slide */
.reveal-scale { opacity: 0; transform: scale(0.96); transition: opacity 0.6s, transform 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.slide.visible .reveal-scale { opacity: 1; transform: scale(1); }
```

## Don't

- No bouncy/spring easing (wrong feeling for technical recap).
- No 3D tilt on hover (gimmicky).
- No particle systems or canvas backgrounds.
- No glow/neon effects.
- No glitch/scramble text.

## Background atmosphere (optional, title slide only)

A single, very subtle radial gradient on the title slide to add depth. Skip on body slides — they should feel paper-clean.

```css
.title-slide {
  background:
    radial-gradient(ellipse at 30% 70%, color-mix(in oklab, var(--accent) 6%, transparent) 0%, transparent 55%),
    var(--bg);
}
```

## Troubleshooting

| Problem | Fix |
|---|---|
| Reveals not triggering | Check IntersectionObserver threshold (0.5); verify `.visible` is being added; confirm `.reveal` children are direct children of `.slide` |
| Scroll-snap fighting smooth scrolling | Already handled — `scroll-behavior: smooth` + `scroll-snap-type: y mandatory` work together |
| Text wrapping character-by-character | The parent has `display: flex; flex-direction: column` applied to inline elements. Inline `<code>` MUST be `display: inline` (not inline-block inside a flex column). The template's `code` rule already enforces this — don't override |
| Mobile choppy | Disable nav rail at <700px (already done in template) |
| Fonts not loading | Confirm `<link>` is in `<head>` and the `family=` querystring matches `font-family` strings exactly |
