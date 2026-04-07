/**
 * Products and Global Engineering (PGE) — canonical internal directory:
 * https://source.redhat.com/departments/products_and_global_engineering
 *
 * Product names below match the user-provided PGE list (duplicates in the
 * source list appear once; “Core Platforms” grouping omitted per request).
 */
export const PGE_PRODUCTS_SOURCE_URL =
  "https://source.redhat.com/departments/products_and_global_engineering";

export type PgeProduct = {
  slug: string;
  name: string;
  /** Catalog card links here (e.g. STI list) instead of opening the product questionnaire */
  catalogHref?: string;
};

export const pgeProducts: readonly PgeProduct[] = [
  { slug: "bifrost-program", name: "Bifrost Program" },
  { slug: "red-hat-certificate-system", name: "Red Hat Certificate System" },
  { slug: "red-hat-directory-server", name: "Red Hat Directory Server" },
  { slug: "red-hat-developer-toolset", name: "Red Hat Developer Toolset" },
  { slug: "fedora-linux", name: "Fedora Linux" },
  { slug: "red-hat-lightspeed", name: "Red Hat Lightspeed" },
  { slug: "red-hat-enterprise-linux", name: "Red Hat Enterprise Linux" },
  {
    slug: "red-hat-in-vehicle-operating-system",
    name: "Red Hat In-Vehicle Operating System",
  },
  {
    slug: "red-hat-openstack-services-on-openshift",
    name: "Red Hat OpenStack Services on OpenShift",
  },
  {
    slug: "red-hat-enterprise-linux-for-sap-solutions",
    name: "Red Hat Enterprise Linux for SAP Solutions",
  },
  { slug: "red-hat-satellite", name: "Red Hat Satellite" },
  { slug: "risc-v-support-program", name: "RISC-V Support Program" },
  {
    slug: "post-quantum-cryptography-program",
    name: "Post Quantum Cryptography Program",
  },
  {
    slug: "red-hat-enterprise-linux-lightspeed",
    name: "Red Hat Enterprise Linux Lightspeed",
  },
  { slug: "red-hat-automotive-suite", name: "Red Hat Automotive Suite" },
  { slug: "project-hummingbird", name: "Project Hummingbird" },
  { slug: "nvidia-jetpack-for-rhel", name: "NVIDIA Jetpack for RHEL" },
  { slug: "hybrid-platforms", name: "Hybrid Platforms" },
  {
    slug: "red-hat-openshift-virtualization",
    name: "Red Hat OpenShift Virtualization",
  },
  {
    slug: "red-hat-hybrid-cloud-console",
    name: "Red Hat Hybrid Cloud Console",
  },
  { slug: "fast-datapath", name: "Fast Datapath" },
  {
    slug: "hypershift-aka-hosted-control-planes",
    name: "HyperShift (aka Hosted Control Planes)",
  },
  {
    slug: "logical-volume-manager-storage",
    name: "logical volume manager storage",
  },
  { slug: "managed-openshift-program", name: "Managed OpenShift Program" },
  {
    slug: "microsoft-azure-red-hat-openshift",
    name: "Microsoft Azure Red Hat OpenShift",
  },
  {
    slug: "red-hat-openshift-cluster-manager-ocm",
    name: "Red Hat OpenShift Cluster Manager (OCM)",
  },
  {
    slug: "red-hat-openshift-dedicated",
    name: "Red Hat OpenShift Dedicated",
  },
  {
    slug: "red-hat-openshift-service-on-aws",
    name: "Red Hat OpenShift Service on AWS",
  },
  {
    slug: "regional-openshift-cluster-manager",
    name: "Regional OpenShift Cluster Manager",
  },
  {
    slug: "red-hat-build-of-microshift",
    name: "Red Hat build of MicroShift",
  },
  {
    slug: "migration-toolkit-for-applications",
    name: "Migration Toolkit for Applications",
  },
  {
    slug: "migration-toolkit-for-containers",
    name: "migration toolkit for containers",
  },
  {
    slug: "migration-toolkit-for-virtualization",
    name: "Migration Toolkit for Virtualization",
  },
  {
    slug: "multi-architecture-program",
    name: "Multi-Architecture Program",
  },
  {
    slug: "openshift-apis-for-data-protection",
    name: "OpenShift APIs for Data Protection",
  },
  { slug: "observability", name: "Observability" },
  {
    slug: "openshift-layered-services-program",
    name: "OpenShift Layered Services Program",
  },
  {
    slug: "mirror-registry-for-red-hat-openshift",
    name: "mirror registry for Red Hat OpenShift",
  },
  {
    slug: "red-hat-openshift-container-platform",
    name: "Red Hat OpenShift Container Platform",
  },
  {
    slug: "operator-framework-program",
    name: "Operator Framework Program",
  },
  {
    slug: "red-hat-openshift-service-mesh",
    name: "Red Hat OpenShift Service Mesh",
  },
  { slug: "red-hat-quay", name: "Red Hat Quay" },
  {
    slug: "red-hat-advanced-cluster-management-for-kubernetes",
    name: "Red Hat Advanced Cluster Management for Kubernetes",
  },
  {
    slug: "red-hat-advanced-cluster-security-for-kubernetes",
    name: "Red Hat Advanced Cluster Security for Kubernetes",
  },
  {
    slug: "red-hat-connectivity-link",
    name: "Red Hat Connectivity Link",
  },
  {
    slug: "red-hat-update-infrastructure",
    name: "Red Hat Update Infrastructure",
  },
  {
    slug: "red-hat-openshift-sandboxed-containers-program",
    name: "Red Hat OpenShift sandboxed containers Program",
  },
  {
    slug: "red-hat-openshift-sandboxed-containers",
    name: "Red Hat OpenShift sandboxed containers",
  },
  { slug: "openshift-on-openstack", name: "OpenShift on OpenStack" },
  {
    slug: "service-telemetry-framework",
    name: "Service Telemetry Framework",
  },
  {
    slug: "secure-flow",
    name: "Secure Flow",
    catalogHref: "/products/secure-flow",
  },
  {
    slug: "red-hat-subscription-management",
    name: "Red Hat Subscription Management",
  },
  {
    slug: "telecommunications-program",
    name: "Telecommunications Program",
  },
  { slug: "management-fabric", name: "Management Fabric" },
  {
    slug: "subscription-management-program",
    name: "Subscription Management Program",
  },
  {
    slug: "red-hat-openshift-lightspeed",
    name: "Red Hat OpenShift Lightspeed",
  },
  {
    slug: "pen-drive-powered-by-red-hat-lightspeed",
    name: "Pen Drive Powered by Red Hat Lightspeed",
  },
  {
    slug: "red-hat-openshift-networking",
    name: "Red Hat OpenShift Networking",
  },
  { slug: "red-hat-edge-manager", name: "Red Hat Edge Manager" },
  {
    slug: "zero-trust-workload-identity-manager",
    name: "zero trust workload identity manager",
  },
  {
    slug: "mcp-server-for-red-hat-openshift",
    name: "MCP server for Red Hat OpenShift",
  },
  { slug: "mcp-gateway", name: "MCP gateway" },
  {
    slug: "mcp-server-for-red-hat-advanced-cluster-management-for-kubernetes",
    name: "MCP server for Red Hat Advanced Cluster Management for Kubernetes",
  },
  { slug: "mcp-lifecycle-operator", name: "MCP lifecycle operator" },
  {
    slug: "unified-intelligence-engineering",
    name: "Unified Intelligence Engineering",
  },
  {
    slug: "lightspeed-core-product-alignment-program",
    name: "Lightspeed Core Product Alignment Program",
  },
  { slug: "ansible", name: "Ansible" },
  {
    slug: "red-hat-ansible-automation-platform",
    name: "Red Hat Ansible Automation Platform",
  },
  {
    slug: "red-hat-ansible-lightspeed",
    name: "Red Hat Ansible Lightspeed",
  },
  { slug: "portfolio-and-delivery", name: "Portfolio and Delivery" },
  {
    slug: "builds-for-red-hat-openshift",
    name: "builds for Red Hat OpenShift",
  },
  { slug: "developer-sandbox", name: "Developer Sandbox" },
  {
    slug: "red-hat-openshift-dev-spaces",
    name: "Red Hat OpenShift Dev Spaces",
  },
  {
    slug: "red-hat-openshift-gitops",
    name: "Red Hat OpenShift GitOps",
  },
  { slug: "ide-extensions", name: "IDE Extensions" },
  { slug: "konflux", name: "Konflux" },
  { slug: "konflux-program", name: "Konflux Program" },
  {
    slug: "openshift-developer-tools-and-services-program",
    name: "OpenShift Developer Tools and Services Program",
  },
  { slug: "red-hat-openshift-local", name: "Red Hat OpenShift Local" },
  {
    slug: "red-hat-openshift-pipelines",
    name: "Red Hat OpenShift Pipelines",
  },
  { slug: "podman-desktop", name: "Podman Desktop" },
  {
    slug: "red-hat-advanced-developer-suite",
    name: "Red Hat Advanced Developer Suite",
  },
  { slug: "red-hat-developer-hub", name: "Red Hat Developer Hub" },
  {
    slug: "red-hat-trusted-profile-analyzer",
    name: "Red Hat Trusted Profile Analyzer",
  },
  {
    slug: "red-hat-ads-ssc-installer-ref-arch",
    name: "Red Hat ADS SSC Installer (Ref Arch)",
  },
  {
    slug: "red-hat-trusted-artifact-signer",
    name: "Red Hat Trusted Artifact Signer",
  },
  { slug: "red-hat-desktop", name: "Red Hat Desktop" },
  {
    slug: "red-hat-trusted-libraries",
    name: "Red Hat Trusted Libraries",
  },
  {
    slug: "red-hat-ads-trusted-software-factory",
    name: "Red Hat ADS Trusted Software Factory",
  },
  {
    slug: "sustaining-engineering-program",
    name: "Sustaining Engineering Program",
  },
  { slug: "web-terminal-operator", name: "Web Terminal Operator" },
  { slug: "exploitintelligence", name: "ExploitIntelligence" },
  { slug: "ge-ai-engineering-org", name: "GE AI Engineering Org" },
  { slug: "ai", name: "AI" },
  { slug: "red-hat-openshift-ai", name: "Red Hat OpenShift AI" },
  {
    slug: "red-hat-ai-inference",
    name: "Red Hat AI Inference",
  },
  {
    slug: "red-hat-enterprise-linux-ai",
    name: "Red Hat Enterprise Linux AI",
  },
  { slug: "red-hat-ai", name: "Red Hat AI" },
] as const;

const bySlug = new Map(pgeProducts.map((p) => [p.slug, p] as const));

export function getPgeProductBySlug(slug: string): PgeProduct | undefined {
  return bySlug.get(slug);
}

export function isPgeProductSlug(slug: string): boolean {
  return bySlug.has(slug);
}
