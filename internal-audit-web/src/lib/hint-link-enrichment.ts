/**
 * Master template hints often say “see link to CMDB” etc. without exporting
 * real URLs from Sheets/PDF. Append concrete links when phrases match and
 * the URL is not already present.
 */
const KNOWN: ReadonlyArray<{
  /** Match hint text (case-insensitive). */
  pattern: RegExp;
  /** Skip if this substring already appears (avoid duplicates). */
  skipIfIncludes: string;
  line: string;
}> = [
  {
    pattern: /see link to cmdb|cmdb where you can search|search for cmdb ids/i,
    skipIfIncludes: "service-now.com",
    line: "- CMDB (ServiceNow — business applications): https://redhat.service-now.com/cmdb_ci_business_app_list.do",
  },
  {
    pattern:
      /pia assessments reviewed|privacy impact assessments?\s*\(pia\)|pia\s*\(\s*['\u2018\u2019]?lite['\u2018\u2019]?\s*\)/i,
    skipIfIncludes: "source.redhat.com",
    line: "- Privacy & PIA (Source): https://source.redhat.com/departments/it/it-information-security/data_privacy/data_privacy",
  },
  {
    pattern: /ess guidelines on controls|about the enterprise security standard\s*\(ess\)|\bESS v8\b/i,
    skipIfIncludes: "enterprise_security_standard_80_essv8",
    line: "- Enterprise Security Standard (ESS v8 wiki): https://source.redhat.com/departments/operations/it-information-security/wiki/enterprise_security_standard_80_essv8",
  },
  {
    pattern: /\bSSML\b|secure software management lifecycle|RH-SDLC|red hat secure development lifecycle/i,
    skipIfIncludes: "secure_software_management_lifecycle",
    line: "- SSML (Source): https://source.redhat.com/departments/products_and_global_engineering/offerings/secure_software_management_lifecycle_ssml",
  },
  {
    pattern: /service impact analysis|\bSIA\b.*guidance/i,
    skipIfIncludes: "technology-resilience",
    line: "- Technology resilience / SIA (Source hub): https://source.redhat.com/departments/it/technology-resilience/",
  },
];

const QUICK = "\n\nQuick links (added for clickable URLs in this app):\n";

/** Run on hints, supported-doc text, or any template guidance without raw URLs. */
export function enrichHintWithKnownLinks(hint: string): string {
  const h = hint.trim();
  if (!h) return hint;

  const lines: string[] = [];
  for (const { pattern, skipIfIncludes, line } of KNOWN) {
    if (!pattern.test(h)) continue;
    if (h.includes(skipIfIncludes)) continue;
    if (lines.includes(line)) continue;
    lines.push(line);
  }
  if (!lines.length) return hint;

  if (h.includes("Quick links (added for clickable URLs in this app)")) {
    return hint;
  }

  return `${h}${QUICK}${lines.join("\n")}`;
}
