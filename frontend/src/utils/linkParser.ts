/**
 * System Design Link & Markdown Parser Utility
 * Implements high-reliability link routing for:
 * 1. External URLs (https://..., http://...) -> target="_blank" rel="noopener noreferrer"
 * 2. Markdown Links ([label](url)) -> target="_blank" rel="noopener noreferrer"
 * 3. Obsidian Wikilinks ([[filename]] / [[filename|Alias]]) -> clickable internal vault targets
 * 4. System Design Primer GitHub Integration -> https://github.com/donnemartin/system-design-primer
 */

export function parseRichMarkdownLinks(mdText: string): string {
  if (!mdText) return '';

  let html = mdText;

  // 1. Escape HTML special chars to prevent XSS
  html = html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // 2. Headings
  html = html.replace(
    /^# (.*?)$/gm,
    '<h1 style="font-family: var(--font-heading); font-size: 20px; font-weight: 800; margin: 16px 0 10px 0; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; color: var(--text-primary);">$1</h1>'
  );
  html = html.replace(
    /^## (.*?)$/gm,
    '<h2 style="font-family: var(--font-heading); font-size: 16px; font-weight: 700; margin: 14px 0 8px 0; color: var(--text-primary);">$1</h2>'
  );
  html = html.replace(
    /^### (.*?)$/gm,
    '<h3 style="font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 12px 0 6px 0; color: var(--text-primary);">$1</h3>'
  );

  // 3. Bold & Italics
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--text-primary); font-weight: 700;">$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // 4. Standard Markdown Links: [Label](URL) -> External Link with target="_blank" rel="noopener noreferrer"
  html = html.replace(
    /\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener noreferrer" class="external-link-btn" style="color: #60a5fa; text-decoration: underline; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 3px;">$1 ↗</a>'
  );

  // 5. Raw URLs (https://... or http://...) not already wrapped in href="..."
  html = html.replace(
    /(?<!href="|">)(https?:\/\/[^\s<>\)"]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer" class="external-link-btn" style="color: #60a5fa; text-decoration: underline; font-weight: 500; cursor: pointer; word-break: break-all;">$1 ↗</a>'
  );

  // 6. Obsidian Wikilinks: [[filename|Alias]] or [[filename]]
  html = html.replace(
    /\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]/g,
    (_match, p1, p2) => {
      const target = p1.trim();
      const label = (p2 || p1).trim();
      const filename = target.endsWith('.md') ? target : `${target}.md`;
      return `<button type="button" class="wikilink-btn" data-wikilink="${filename}" style="background: rgba(129,140,248,0.12); border: 1px solid rgba(129,140,248,0.3); color: #a5b4fc; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; margin: 0 2px;">📄 ${label}</button>`;
    }
  );

  // 7. System Design Primer references (e.g. system-design-primer)
  html = html.replace(
    /\b(system-design-primer|donnemartin\/system-design-primer)\b/gi,
    '<a href="https://github.com/donnemartin/system-design-primer" target="_blank" rel="noopener noreferrer" style="background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); color: #34d399; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">📚 System Design Primer ↗</a>'
  );

  // 8. Bullet Lists
  html = html.replace(/^- (.*?)$/gm, '<li style="margin-left: 20px; list-style-type: square; margin-bottom: 4px;">$1</li>');

  // 9. Line breaks
  html = html.replace(/\n/g, '<br />');

  return html;
}
