"use client";

import { find } from "linkifyjs";
import type { CSSProperties, ReactNode } from "react";
import { Fragment } from "react";

/** Tailwind + class linkified in globals.css (color forced with !important there). */
const linkAnchorClass =
  "linkified-external relative z-[2] inline cursor-pointer break-words rounded px-0.5 align-baseline underline-offset-2 outline-offset-2 hover:bg-blue-100/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600";

const anchorStyle: CSSProperties = {
  color: "#1d4ed8",
  textDecoration: "underline",
  textDecorationThickness: "2px",
  textUnderlineOffset: "3px",
  fontWeight: 600,
};

/** Hosts we always open with https (linkifyjs uses http:// for scheme-less matches). */
const HTTPS_PREFERRED = new Set([
  "source.redhat.com",
  "spaces.redhat.com",
  "issues.redhat.com",
  "gitlab.cee.redhat.com",
  "redhat.service-now.com",
  "docs.google.com",
  "drive.google.com",
  "docs.engineering.redhat.com",
]);

function preferHttpsForKnownHosts(href: string): string {
  try {
    const u = new URL(href);
    if (u.protocol === "http:" && HTTPS_PREFERRED.has(u.hostname)) {
      u.protocol = "https:";
      return u.toString();
    }
  } catch {
    /* ignore */
  }
  return href;
}

function stripTrailingFromUrl(raw: string): string {
  let u = raw.trim();
  while (u.length > 0) {
    if (u.endsWith("…")) {
      u = u.slice(0, -1);
      continue;
    }
    if (u.endsWith("...")) {
      u = u.slice(0, -3);
      continue;
    }
    const ch = u[u.length - 1]!;
    if (".,;:!?)]".includes(ch)) {
      u = u.slice(0, -1);
      continue;
    }
    break;
  }
  return u;
}

/** Angle-bracket URLs anywhere: <https://...> */
function unwrapAngleBrackets(s: string): string {
  return s.replace(/<+(https?:\/\/[^>\s]+)>+/gi, "$1");
}

/** Strip ZWSP / BOM / NBSP so URL regex matches pasted Sheets/Docs text. */
function normalizeForLinkify(s: string): string {
  return unwrapAngleBrackets(s)
    .replace(/\uFEFF/g, "")
    .replace(/[\u200B-\u200D\u2060]/g, "")
    .replace(/\u00A0/g, " ");
}

function renderExternalLink(
  rawDisplay: string,
  key: string,
  hrefOverride?: string,
) {
  const cleanedDisplay = rawDisplay.trim();
  const hrefRaw = hrefOverride ?? cleanedDisplay;
  const href = preferHttpsForKnownHosts(stripTrailingFromUrl(hrefRaw));
  if (!href) return null;
  const normalized =
    href.startsWith("http://") || href.startsWith("https://")
      ? href
      : `https://${href}`;

  return (
    <a
      key={key}
      href={normalized}
      target="_blank"
      rel="noopener noreferrer"
      className={linkAnchorClass}
      style={anchorStyle}
      title={normalized}
    >
      {cleanedDisplay}
      <span
        className="ml-0.5 select-none align-text-top text-[0.7em] font-extrabold no-underline"
        style={{ color: "#2563eb" }}
        aria-hidden
      >
        ↗
      </span>
    </a>
  );
}

function linkifyPlainSegment(
  plain: string,
  keyPrefix: string,
): ReactNode[] {
  if (!plain) return [];
  const tokens = find(plain, "url");
  if (!tokens.length) {
    return [<Fragment key={`${keyPrefix}-txt0`}>{plain}</Fragment>];
  }
  const out: ReactNode[] = [];
  let pos = 0;
  tokens.forEach((tok) => {
    if (tok.start > pos) {
      out.push(
        <Fragment key={`${keyPrefix}-txt${pos}`}>
          {plain.slice(pos, tok.start)}
        </Fragment>,
      );
    }
    const href = preferHttpsForKnownHosts(stripTrailingFromUrl(tok.href));
    const el = renderExternalLink(
      tok.value,
      `${keyPrefix}-u${tok.start}`,
      href,
    );
    if (el) out.push(el);
    pos = tok.end;
  });
  if (pos < plain.length) {
    out.push(
      <Fragment key={`${keyPrefix}-txt${pos}`}>{plain.slice(pos)}</Fragment>,
    );
  }
  return out;
}

/** `[label](https://...)` allowing `(` / `)` inside the URL (balanced parens). */
function extractMarkdownLinks(line: string): Array<{
  start: number;
  end: number;
  label: string;
  url: string;
}> {
  const results: Array<{
    start: number;
    end: number;
    label: string;
    url: string;
  }> = [];
  let i = 0;
  outer: while (i < line.length) {
    const open = line.indexOf("[", i);
    if (open === -1) break;
    const closeBracket = line.indexOf("]", open + 1);
    if (closeBracket === -1) break;
    if (
      closeBracket + 1 >= line.length ||
      line[closeBracket + 1] !== "("
    ) {
      i = open + 1;
      continue;
    }
    const urlStart = closeBracket + 2;
    let depth = 1;
    for (let j = urlStart; j < line.length; j++) {
      const c = line[j];
      if (c === "(") depth++;
      else if (c === ")") {
        depth--;
        if (depth === 0) {
          const url = line.slice(urlStart, j);
          if (/^https?:\/\//i.test(url)) {
            results.push({
              start: open,
              end: j + 1,
              label: line.slice(open + 1, closeBracket),
              url,
            });
          }
          i = j + 1;
          continue outer;
        }
      }
    }
    i = open + 1;
  }
  return results;
}

function linkifyLine(line: string, keyPrefix: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  const mdLinks = extractMarkdownLinks(line);
  if (mdLinks.length === 0) {
    return linkifyPlainSegment(line, keyPrefix);
  }
  let last = 0;
  for (const m of mdLinks) {
    if (m.start > last) {
      nodes.push(
        ...linkifyPlainSegment(
          line.slice(last, m.start),
          `${keyPrefix}-b${last}`,
        ),
      );
    }
    const href = preferHttpsForKnownHosts(stripTrailingFromUrl(m.url));
    nodes.push(
      <a
        key={`${keyPrefix}-md${m.start}`}
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className={linkAnchorClass}
        style={anchorStyle}
        title={href}
      >
        {m.label}
        <span
          className="ml-0.5 select-none align-text-top text-[0.7em] font-extrabold no-underline"
          style={{ color: "#2563eb" }}
          aria-hidden
        >
          ↗
        </span>
      </a>,
    );
    last = m.end;
  }
  if (last < line.length) {
    nodes.push(...linkifyPlainSegment(line.slice(last), `${keyPrefix}-end`));
  }
  return nodes;
}

/**
 * Plain text → clickable http(s), markdown [label](url), &
 * bare hosts (via linkifyjs), including internal URLs pasted without a scheme.
 */
export function LinkifiedText({
  text,
  className,
}: {
  text: string;
  className?: string;
}) {
  const normalized = normalizeForLinkify(text);
  const lines = normalized.split(/\r?\n/);
  return (
    <span className={`linkified ${className ?? ""}`.trim()}>
      {lines.map((line, li) => (
        <Fragment key={li}>
          {li > 0 ? <br /> : null}
          {linkifyLine(line, `ln${li}`)}
        </Fragment>
      ))}
    </span>
  );
}
