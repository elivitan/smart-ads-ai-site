const fs = require("node:fs");
const path = require("node:path");
const catalog = require("../pricing-catalog.json");

const pagePlans = {
  "index.html": ["free", "starter", "pro"],
  "pricing.html": ["free", "starter", "pro", "premium", "enterprise"],
};

const number = (value) => new Intl.NumberFormat("en-US").format(value);
const productLabel = (key, plan) => plan.maxProducts === null
  ? "Unlimited products"
  : (key === "free" ? "Scan up to " : "Up to ") + number(plan.maxProducts) + " products";
const campaignLabel = (plan) => plan.maxActiveCampaigns === null
  ? "Unlimited active campaigns"
  : plan.maxActiveCampaigns === 0
    ? "No active campaigns"
    : "Up to " + number(plan.maxActiveCampaigns) + " active campaigns";

function expectedFields(page) {
  const rows = new Map();
  const add = (plan, field, value) => rows.set(plan + "." + field, value);
  for (const key of pagePlans[page] ?? []) {
    const plan = catalog.plans[key];
    add(key, "price", "$" + number(plan.monthlyUsd));
    if (key === "enterprise") {
      const unlimited = plan.maxProducts === null && plan.maxActiveCampaigns === null;
      add(key, "limits", unlimited
        ? "Unlimited products &amp; campaigns"
        : productLabel(key, plan) + " &amp; " + campaignLabel(plan));
    } else {
      add(key, "products", productLabel(key, plan));
      add(key, "campaigns", campaignLabel(plan));
    }
    add(key, "credits", plan.monthlyAiCredits === 0
      ? "No monthly AI credits" : number(plan.monthlyAiCredits) + " AI credits / month");
  }
  add("starter", "trialDays", String(catalog.firstPaidTrialDays));
  if (page === "pricing.html") {
    add("starter", "faqTrialDays", String(catalog.firstPaidTrialDays));
    for (const key of ["starter", "pro", "premium", "enterprise"]) {
      add(key, "creditsNumber", number(catalog.plans[key].monthlyAiCredits));
    }
  }
  return rows;
}

function renderPricing(page, html) {
  const required = expectedFields(page);
  const result = html.replace(/<!--catalog:([a-z]+\.[a-zA-Z]+)-->[^\r\n]*?<!--\/catalog-->/g, (_match, key) => {
    if (!required.has(key)) throw new Error(page + ": unknown or repeated pricing marker " + key);
    const text = required.get(key);
    required.delete(key);
    return "<!--catalog:" + key + "-->" + text + "<!--/catalog-->";
  });
  if (required.size) throw new Error(page + ": missing pricing markers " + [...required.keys()].join(", "));
  return result;
}

function main() {
  const mode = process.argv[2] ?? "--check";
  if (!["--check", "--write"].includes(mode) || process.argv.length > 3) {
    throw new Error("Usage: node scripts/sync-pricing.cjs [--check|--write]");
  }
  const updates = Object.keys(pagePlans).map(page => {
    const file = path.join(__dirname, "..", page);
    const original = fs.readFileSync(file, "utf8");
    return { page, file, original, rendered: renderPricing(page, original) };
  }).filter(({ original, rendered }) => original !== rendered);

  if (mode === "--write") {
    for (const { file, rendered } of updates) fs.writeFileSync(file, rendered);
  } else if (updates.length > 0) {
    throw new Error("Displayed plan data differs from pricing-catalog.json in " + updates.map(row => row.page).join(", "));
  }
  console.log("Public pricing checked on home and pricing pages.");
}

module.exports = { renderPricing };
if (require.main === module) main();
