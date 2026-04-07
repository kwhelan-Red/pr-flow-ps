import {
  PGE_PRODUCTS_SOURCE_URL,
  pgeProducts,
} from "@/pge-products";

/** STIs under the Secure Flow product line only (internal audit by STI). */
export const secureFlowStis = [
  "BOTA-001",
  "CGER-001",
  "CHAR-001",
  "CICA-001",
  "COMP-016",
  "CONJ-001",
  "CPAA-001",
  "CVP-001",
  "DPLM-001",
  "DRDB-001",
  "ERRA-001",
  "ETER-001",
  "EXOD-001",
  "EXOD-002",
  "EXOD-003",
  "FMKR-001",
  "GWVE-001",
  "HONE-001",
  "IIB-001",
  "INDY-001",
  "ISVP-001",
  "MACS-001",
  "MBS-001",
  "MERC-001",
  "MET-001",
  "MXOR-001",
  "NXS-001",
  "ODCS-001",
  "PULP-003",
  "PXS-001",
  "RCMR-001",
  "RELE-001",
  "RNDA-001",
  "RSIG-001",
  "SIGS-001",
  "UBIP-002",
  "UTDH-001",
  "WADB-001",
  "WINS-001",
  "WINS-002",
] as const;

export type SecureFlowSti = (typeof secureFlowStis)[number];

export function isSecureFlowSti(id: string): id is SecureFlowSti {
  return (secureFlowStis as readonly string[]).includes(id);
}

export type ProductScope = "secure-flow" | "all";

export const productScopeConfig = {
  "secure-flow": {
    title: "Secure Flow",
    description:
      "Internal audit for Secure Flow uses Service Track Identifiers (STIs). Each card is an STI code.",
    stis: secureFlowStis,
  },
  all: {
    title: "All Red Hat products",
    description:
      "Product lines aligned with Products & Global Engineering (PGE). STIs are not used outside Secure Flow.",
    products: pgeProducts,
    sourceUrl: PGE_PRODUCTS_SOURCE_URL,
  },
} as const;

export function isProductScope(value: string): value is ProductScope {
  return value === "secure-flow" || value === "all";
}

export type AuditQuestion = {
  id: number;
  category: string;
  question: string;
  options: string[];
  /** Short guidance for auditors / business units answering the control. */
  hint: string;
};

export const auditQuestions: AuditQuestion[] = [
  {
    id: 1,
    category: "System Hardening",
    question:
      "Do you follow any system (Nodes, cluster, containers, pods, worker node etc) or server hardening guides to secure your environments?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Point to DISA STIGs, CIS benchmarks, RH security guides, or your team’s standard image/hardening checklist. Note scope: clusters, VMs, and container hosts.",
  },
  {
    id: 2,
    category: "Logging & Alerting",
    question:
      "Are your systems or apps logging activity (e.g., access logs, error logs, audit trails, privilege users activities)?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Cite where logs are collected, retention, and whether privileged actions and authentication events are included. Mention centralized log stack if any.",
  },
  {
    id: 3,
    category: "SSH Key Management",
    question:
      "If you use SSH keys to access systems, do those keys have passphrases/passwords?",
    options: ["Yes", "No", "Not Applicable"],
    hint: "If No, describe key protection (HSM, vault, or corporate standard). Use Not Applicable only when SSH keys are not used for human access.",
  },
  {
    id: 4,
    category: "Image Hardening",
    question:
      "Do you use hardened (secure and clean) base images when building containers or virtual machines?",
    options: ["Yes", "No", "Not Applicable"],
    hint: "Reference gold images, UBI/minimal bases, image scanning in CI, or SOE builds. Not Applicable if you do not build images (consume only vetted images).",
  },
  {
    id: 5,
    category: "Network Firewall",
    question:
      "How often do you review and clean up old or unused firewall/security group rules?",
    options: ["Monthly", "Quarterly", "Annually", "Not Sure"],
    hint: "Name the review process or ticket type. If cadence varies by zone, say so. Not Sure: no formal review yet—note planned approach.",
  },
  {
    id: 6,
    category: "SUDO Setup & Configuration",
    question:
      "Do you use SUDO access (temporary admin/root access) for any team members?",
    options: ["Yes", "No", "Not Applicable"],
    hint: "If Yes, describe break-glass, time limits, logging, and approval. Not Applicable if elevation is never used for your scope.",
  },
  {
    id: 7,
    category: "ESS Compliance",
    question:
      "Are the systems or applications your team owns following Red Hat's Enterprise Secure Standards (ESS)?",
    options: ["Compliant", "In Progress", "Not Started", "Not Sure"],
    hint: "Align with latest ESS self-assessment or exception path. Link ESS workspace/ticket if available.",
  },
  {
    id: 8,
    category: "SSML Compliance",
    question:
      "Are you following Red Hat's SSML (Security Software Measurement List) standards to ensure your products or internal tools are secure?",
    options: ["Yes", "No", "Not Applicable"],
    hint: "Reference SSML coverage or waiver. Not Applicable if SSML does not apply to this offering (explain).",
  },
  {
    id: 9,
    category: "Software & Code Security",
    question:
      "Do you regularly review your codebase and dependencies for vulnerabilities (e.g., using scanners like Snyk, Black Duck)?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Name tools, frequency (CI vs release), and how critical findings are tracked to closure.",
  },
  {
    id: 10,
    category: "Security Operations Approval",
    question:
      "Have your team’s services, tools, infrastructure, or applications gone through Security Operations Approval (SOA)?",
    options: ["Approved", "In Progress", "Not Started"],
    hint: "Include SOA ticket ID or status in ServiceNow/GRC. In Progress: note target date or blocker.",
  },
  {
    id: 11,
    category: "Access Management",
    question:
      "Is there an approval or request process in place before new user-IDs are activated?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Reference HR + IT workflow, entitlement catalog, or IdP joiner process.",
  },
  {
    id: 12,
    category: "Access Management",
    question:
      "Does your team use any shared user-IDs or API keys (e.g., for automation, integrations)?",
    options: ["Yes", "No", "Not Sure"],
    hint: "If Yes, document controls: vault storage, rotation, MFA on break-glass, and who can use the credential.",
  },
  {
    id: 14,
    category: "Least Privilege",
    question:
      "Do users only have access to what they need to do their jobs (no more, no less)?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Mention RBAC model, periodic access review, and removal on role change.",
  },
  {
    id: 18,
    category: "Authentication",
    question:
      "Is strong authentication (like 2FA/MFA) required for your systems?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Specify IdP (e.g. SSO) and MFA policy scope—interactive users, admins, VPN, privileged interfaces.",
  },
  {
    id: 20,
    category: "Patching",
    question:
      "When you set up a new system, infra, or app, do you ensure it has all the latest updates/patches before use?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Reference image pipeline, bootstrap config, or first-run patching standard.",
  },
  {
    id: 24,
    category: "Data Integrity",
    question:
      "Do you have checks in place to make sure that only authorized people can change data in your system/app?",
    options: ["Yes", "No", "Not Sure"],
    hint: "Describe app roles, DB grants, admin interfaces, and audit of changes (including CI/CD to production).",
  },
  {
    id: 29,
    category: "Data Privacy",
    question:
      "Does your system/app handle any personal or sensitive data? If yes, has a Privacy Impact Assessment (PIA) been completed?",
    options: ["Yes", "No", "Not Sure"],
    hint: "If personal data: cite PIA status/link. If no PII: state data classes handled and why PIA is not required.",
  },
];
