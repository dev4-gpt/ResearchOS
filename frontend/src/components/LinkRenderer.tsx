import React from 'react';
import { parseRichMarkdownLinks } from '../utils/linkParser';

interface LinkRendererProps {
  content: string;
  onNavigateWikilink?: (filename: string) => void;
  style?: React.CSSProperties;
  className?: string;
}

export const LinkRenderer: React.FC<LinkRendererProps> = ({
  content,
  onNavigateWikilink,
  style,
  className,
}) => {
  const parsedHtml = parseRichMarkdownLinks(content);

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const target = e.target as HTMLElement;

    // Check if a wikilink button was clicked
    const wikilinkBtn = target.closest('[data-wikilink]') as HTMLElement;
    if (wikilinkBtn) {
      const filename = wikilinkBtn.getAttribute('data-wikilink');
      if (filename && onNavigateWikilink) {
        e.preventDefault();
        onNavigateWikilink(filename);
      }
      return;
    }

    // Check if an anchor tag with href was clicked
    const anchor = target.closest('a') as HTMLAnchorElement;
    if (anchor && anchor.href) {
      // Ensure external links open in a new tab safely
      anchor.setAttribute('target', '_blank');
      anchor.setAttribute('rel', 'noopener noreferrer');
    }
  };

  return (
    <div
      className={className}
      style={{ fontSize: '13px', lineHeight: '1.6', color: 'var(--text-primary)', ...style }}
      onClick={handleClick}
      dangerouslySetInnerHTML={{ __html: parsedHtml }}
    />
  );
};

export default LinkRenderer;
