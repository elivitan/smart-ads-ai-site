const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { test } = require("node:test");
const { renderPricing } = require("./sync-pricing.cjs");

const read = (file) => fs.readFileSync(path.join(__dirname, "..", file), "utf8");

test("home and pricing render the same current catalog into static HTML", () => {
  for (const page of ["index.html", "pricing.html"]) {
    const html = read(page);
    assert.equal(renderPricing(page, html), html);
    const restored = renderPricing(page, html.replace(
      "<!--catalog:starter.credits-->5 AI credits / month<!--/catalog-->",
      "<!--catalog:starter.credits-->30 images / month<!--/catalog-->",
    ));
    assert.equal(restored, html);
    assert.throws(
      () => renderPricing(page, html.replace("<!--catalog:starter.credits-->", "")),
      /missing pricing markers starter\.credits/,
    );
  }
});

test("home structured FAQ matches visible authorization and spending qualifications", () => {
  const html = read("index.html");
  const data = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)]
    .map((match) => JSON.parse(match[1]));
  const faqs = data.flatMap(row => row["@type"] === "FAQPage" ? [row] : row["@graph"] ?? [])
    .filter(row => row["@type"] === "FAQPage");
  const faq = faqs.flatMap(row => row.mainEntity);
  for (const [question, part] of [
    ["How does Bamzal connect to my ad accounts?", "X Ads requires separate authorization"],
    ["Will Bamzal spend my money without my permission?", "does not itself stop campaigns"],
  ]) {
    const answer = faq.find(row => row.name === question)?.acceptedAnswer.text;
    assert.ok(answer?.includes(part), question);
    assert.ok(html.includes('<div class="faq-a">' + answer + '</div>'), question);
  }
});

test("targeted marketing pages make no blanket undo, stop or OAuth protocol claims", () => {
  for (const page of ["index.html", "pricing.html", "demo.html", "product.html"]) {
    const html = read(page);
    assert.doesNotMatch(html, /every action is one click from undone|Pause everything instantly|SQLite in development|PostgreSQL\/MySQL|industry-standard OAuth 2\.0 protocol for each network|Official OAuth 2\.0 on every network|Takeover campaigns|Pinterest · X · X/i);
  }
});

test("governance, evaluation and product-cost claims describe actual conditions", () => {
  for (const page of ["index.html", "product.html"]) {
    const html = read(page);
    assert.doesNotMatch(html, /every (?:platform )?write (?:to |passes)|CI enforces|seven binding production SLOs|two consecutive breaches trigger auto-rollback/i);
    assert.doesNotMatch(html, /auto-promotes?|automatically demoted|only earn more autonomy when predicted ROAS|≥0\.7 correlation|&ge;0\.7 correlation/i);
    assert.doesNotMatch(html, /always with the competitor data|extra profit shown up front|guarded, reversible write|<em>true<\/em> margin per product/i);
    assert.match(html, /support(?:ed|s) (?:paid |operation)/i);
    assert.match(html, /authority (?:and limits )?you set/i);
    assert.match(html, /status in (?:the|your) ad (?:platform|account)/i);
  }
  const home = read("index.html");
  assert.match(home, /estimate of the effect on margin/);
  assert.match(home, /available recovery options depend on what was changed/);
});

test("public pricing preserves application catalog provenance", () => {
  const { source } = JSON.parse(read("pricing-catalog.json"));
  assert.match(source.commit, /^[0-9a-f]{40}$/);
  assert.equal(source.plans, "app/utils/billing/plans.ts");
  assert.equal(source.monthlyCredits, "app/utils/billing/plan-credits.ts");
});
