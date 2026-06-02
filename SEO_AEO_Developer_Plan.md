# AMY Electric SEO/AEO Implementation Plan — Developer Guide

**Project:** amyelectric.com SEO & AEO Optimization  
**Stack:** Next.js (React), Vercel  
**Owner:** Amy  
**Target Completion:** 8 weeks  

---

## Overview

This plan outlines the technical work needed to improve amyelectric.com from 7.2/10 SEO/AEO score to 8.5+/10. Focus is on structured data (schema markup), content metadata, author credibility signals, and internal linking.

**Success Metrics:**
- Schema markup implemented & validated (Google Rich Results Test: Pass)
- All service pages have 500+ words + internal links
- FAQ section expanded with schema markup
- Author bios added to all content
- Google Business Profile claimed & linked
- Blog posts have publish/update dates & metadata

---

## Phase 1: Foundation (Weeks 1–2) — CRITICAL

### 1.1 — Implement Schema Markup (JSON-LD)

**Goal:** Add structured data to help Google and AI models understand business info, services, and reviews.

**Files to Create/Modify:**

#### **A. Create `/lib/schema.ts` (or `.js`)**

This helper generates all schema markup consistently:

```typescript
// lib/schema.ts
export const generateLocalBusinessSchema = (baseUrl: string) => {
  return {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": baseUrl,
    "name": "AMY Electric",
    "image": `${baseUrl}/img/og-home.jpg`,
    "description": "Licensed C-10 electrical contractor in Los Angeles specializing in EV charger installation, panel upgrades, electrical repairs, and commercial electrical work.",
    "url": baseUrl,
    "telephone": "+1-818-302-5614",
    "email": "info@amyelectric.com",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "[INSERT FULL STREET ADDRESS]",
      "addressLocality": "Los Angeles",
      "addressRegion": "CA",
      "postalCode": "[INSERT ZIP]",
      "addressCountry": "US"
    },
    "foundingDate": "2012",
    "founder": {
      "@type": "Person",
      "name": "Amy",
      "description": "Licensed C-10 electrical contractor with 15+ years of experience"
    },
    "areaServed": [
      { "@type": "City", "name": "Los Angeles" },
      { "@type": "City", "name": "Sherman Oaks" },
      { "@type": "City", "name": "Studio City" },
      { "@type": "City", "name": "Burbank" },
      { "@type": "City", "name": "Glendale" },
      { "@type": "City", "name": "Pasadena" },
      { "@type": "City", "name": "Encino" },
      { "@type": "City", "name": "Van Nuys" },
      { "@type": "City", "name": "North Hollywood" },
      { "@type": "City", "name": "Santa Monica" },
      { "@type": "City", "name": "Beverly Hills" },
      { "@type": "City", "name": "West Los Angeles" },
      { "@type": "City", "name": "Hollywood" },
      { "@type": "City", "name": "Woodland Hills" },
      { "@type": "City", "name": "Calabasas" },
      { "@type": "City", "name": "Culver City" }
    ],
    "priceRange": "$",
    "sameAs": [
      "https://www.yelp.com/biz/amy-electric-los-angeles",
      "https://calevip.org/evsp/amy-electric"
    ],
    "knowsAbout": [
      "EV Charger Installation",
      "Panel Upgrades",
      "Electrical Repair",
      "Commercial Electrical",
      "Whole-Home Rewiring",
      "Lighting Installation",
      "Surge Protection"
    ],
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "5",
      "reviewCount": "3"
    },
    "review": [
      {
        "@type": "Review",
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5"
        },
        "reviewBody": "AMY Electric installed our Tesla Wall Connector in one afternoon. Super clean work, they handled the permit, and the price was exactly what they quoted. Highly recommend.",
        "author": {
          "@type": "Person",
          "name": "David R."
        },
        "datePublished": "2026-05-15"
      },
      {
        "@type": "Review",
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5"
        },
        "reviewBody": "Our old 100A panel was a disaster. They did a full 200A upgrade, coordinated with LADWP, and passed inspection on the first try. Professional from start to finish.",
        "author": {
          "@type": "Person",
          "name": "Maria T."
        },
        "datePublished": "2026-05-20"
      },
      {
        "@type": "Review",
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5"
        },
        "reviewBody": "We had flickering lights and a tripping breaker nobody could figure out. AMY Electric diagnosed it in 20 minutes — loose connection in the panel. Fast, honest, and affordable.",
        "author": {
          "@type": "Person",
          "name": "James K."
        },
        "datePublished": "2026-05-25"
      }
    ]
  };
};

export const generateServiceSchema = (
  serviceName: string,
  description: string,
  priceRange: string,
  baseUrl: string
) => {
  return {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": serviceName,
    "description": description,
    "provider": {
      "@type": "LocalBusiness",
      "name": "AMY Electric",
      "url": baseUrl
    },
    "areaServed": {
      "@type": "City",
      "name": "Los Angeles"
    },
    "priceRange": priceRange,
    "offers": {
      "@type": "Offer",
      "priceSpecification": {
        "@type": "PriceSpecification",
        "priceCurrency": "USD",
        "price": priceRange
      }
    }
  };
};

export const generateFAQSchema = (faqs: { question: string; answer: string }[]) => {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map((faq) => ({
      "@type": "Question",
      "name": faq.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": faq.answer
      }
    }))
  };
};

export const generateBreadcrumbSchema = (breadcrumbs: { name: string; url: string }[]) => {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": breadcrumbs.map((crumb, idx) => ({
      "@type": "ListItem",
      "position": idx + 1,
      "name": crumb.name,
      "item": crumb.url
    }))
  };
};
```

#### **B. Create Schema Component `/components/SchemaScript.tsx`**

```typescript
// components/SchemaScript.tsx
import { FC } from 'react';

interface SchemaScriptProps {
  schema: Record<string, any>;
}

export const SchemaScript: FC<SchemaScriptProps> = ({ schema }) => {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(schema)
      }}
    />
  );
};
```

#### **C. Update Homepage `/pages/index.html` or `/app/page.tsx`**

Add schema to the `<head>`:

```typescript
// pages/index.tsx (if using pages router) or app/page.tsx (if using app router)
import Head from 'next/head';
import { SchemaScript } from '@/components/SchemaScript';
import { generateLocalBusinessSchema, generateFAQSchema } from '@/lib/schema';

export default function Home() {
  const baseUrl = 'https://amyelectric.com';
  
  const faqs = [
    {
      question: "Are you licensed and insured?",
      answer: "Yes. AMY Electric holds a California C-10 Electrical Contractor license (#981578), is fully insured and bonded, and is EVITP-certified (#4051604) for EV charger installation. Our licenses are verified with the Contractors State License Board (CSLB) and updated annually."
    },
    {
      question: "Do you pull permits?",
      answer: "Yes — we handle all permitting and inspections with LADBS (Los Angeles Department of Building and Safety), LADWP (Los Angeles Department of Water and Power), and other local jurisdictions. You don't have to do anything. We coordinate inspection scheduling, manage plan review comments, and ensure all work passes final inspection."
    },
    // Add all 6+ FAQs here with expanded answers (100–150 words each)
  ];

  return (
    <>
      <Head>
        <title>Electrician Los Angeles | Panel Upgrades, EV Chargers, Repairs | AMY Electric</title>
        <meta name="description" content="AMY Electric — trusted licensed electricians in Los Angeles. Panel upgrades, EV charger installation, repairs & commercial electrical. C-10 #981578 · EVITP #4051604. Free estimates. Call (818) 302-5614." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="canonical" href={baseUrl} />
        
        {/* Open Graph */}
        <meta property="og:title" content="AMY Electric | Electrician Los Angeles" />
        <meta property="og:description" content="Licensed LA electricians. Panel upgrades, EV chargers, repairs. C-10 #981578 · EVITP #4051604." />
        <meta property="og:image" content={`${baseUrl}/img/og-home.jpg`} />
        <meta property="og:url" content={baseUrl} />
        <meta property="og:type" content="website" />
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="AMY Electric | Electrician Los Angeles" />
        <meta name="twitter:description" content="Licensed LA electricians. Panel upgrades, EV chargers, repairs." />
        <meta name="twitter:image" content={`${baseUrl}/img/og-home.jpg`} />
        
        {/* Schema Markup */}
        <SchemaScript schema={generateLocalBusinessSchema(baseUrl)} />
        <SchemaScript schema={generateFAQSchema(faqs)} />
      </Head>
      
      {/* Rest of homepage JSX */}
    </>
  );
}
```

#### **D. Update Service Pages (e.g., `/pages/ev-charger-installation.tsx`)**

```typescript
// pages/ev-charger-installation.tsx
import Head from 'next/head';
import { SchemaScript } from '@/components/SchemaScript';
import { generateServiceSchema, generateBreadcrumbSchema } from '@/lib/schema';

export default function EVChargerPage() {
  const baseUrl = 'https://amyelectric.com';
  const serviceName = 'EV Charger Installation';
  
  const serviceSchema = generateServiceSchema(
    serviceName,
    'Professional Level 2 EV charger installation for Tesla, Rivian, ChargePoint, and all EVs. EVITP-certified installation with permits and inspection handled.',
    '$350-$900',
    baseUrl
  );

  const breadcrumbs = [
    { name: 'Home', url: baseUrl },
    { name: 'Services', url: `${baseUrl}/services` },
    { name: serviceName, url: `${baseUrl}/ev-charger-installation.html` }
  ];

  return (
    <>
      <Head>
        <title>EV Charger Installation Los Angeles | AMY Electric</title>
        <meta name="description" content="Professional Level 2 EV charger installation in LA. Tesla Wall Connector, NEMA 14-50, and all electric vehicles. EVITP-certified. Permits & inspection included. Free estimates." />
        <link rel="canonical" href={`${baseUrl}/ev-charger-installation.html`} />
        
        <SchemaScript schema={serviceSchema} />
        <SchemaScript schema={generateBreadcrumbSchema(breadcrumbs)} />
      </Head>

      <main>
        {/* Breadcrumb navigation */}
        <nav aria-label="breadcrumb">
          {breadcrumbs.map((crumb, idx) => (
            <span key={crumb.name}>
              <a href={crumb.url}>{crumb.name}</a>
              {idx < breadcrumbs.length - 1 && ' > '}
            </span>
          ))}
        </nav>

        <h1>EV Charger Installation in Los Angeles</h1>
        
        {/* 500+ word content section */}
        <section>
          <h2>What We Install</h2>
          <p>
            AMY Electric installs Level 2 EV chargers for all electric vehicles, including Tesla, Rivian, 
            Hyundai Ioniq, Chevrolet Bolt, and more. Most homeowners in the Los Angeles area opt for a 
            Level 2 (240V) charger, which delivers 25–30 miles of range per hour of charging...
          </p>
          {/* Continue with 500+ words total */}
        </section>

        {/* FAQ Section */}
        <section>
          <h2>Common Questions</h2>
          <details>
            <summary>How much does EV charger installation cost in LA?</summary>
            <p>Most Level 2 installations in LA range from $350–$900 for straightforward garage installs with existing 240V service. If you need a panel upgrade to support the charger, add $2,500–$4,500...</p>
          </details>
          {/* More FAQs */}
        </section>
      </main>
    </>
  );
}
```

---

### 1.2 — Update Metadata Fields Across Pages

**Add these fields to every page's frontmatter or JSX head:**

| Field | Example | Why |
|-------|---------|-----|
| `title` | "EV Charger Installation Los Angeles" | SEO + browser tab |
| `description` | "Professional Level 2 EV charger installation..." | SEO snippet |
| `canonical` | "https://amyelectric.com/ev-charger-installation.html" | Prevent duplicates |
| `og:title` | "EV Charger Installation | AMY Electric" | Social sharing |
| `og:description` | "Professional Level 2 EV chargers in LA..." | Social snippet |
| `og:image` | "https://amyelectric.com/img/ev-charger-og.jpg" | Social thumbnail |
| `twitter:card` | "summary_large_image" | Twitter appearance |

**Implementation (add to each page's `Head` component):**

```typescript
<meta name="description" content="..." />
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="..." />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="..." />
<link rel="canonical" href="..." />
```

---

### 1.3 — Testing & Validation

**Test schema markup with these tools:**

1. **Google Rich Results Test:** https://search.google.com/test/rich-results
   - Paste each page URL
   - Verify "LocalBusiness," "Service," "FAQPage" schemas appear
   - Fix any errors (red X marks)

2. **Schema.org Validator:** https://validator.schema.org
   - Paste HTML or JSON-LD
   - Check for warnings/errors

3. **Lighthouse (Chrome DevTools)**
   - Run audit → check "SEO" section
   - Target: 90+ score

**Expected validation output:**
```
✓ Valid LocalBusiness schema detected
✓ Valid Service schema detected  
✓ Valid FAQPage schema detected
✓ Valid Review schema detected
✓ 3 reviews found
```

---

## Phase 2: Content & Metadata (Weeks 2–3)

### 2.1 — Add Publish/Update Dates to Blog Posts

**Goal:** Signal freshness to Google and AI models.

#### **A. Update Blog Post Metadata**

For each blog post, add `datePublished` and `dateModified`:

```typescript
// lib/posts.ts or blog data structure
export const blogPosts = [
  {
    slug: "ev-charging-benefits",
    title: "5 Ways EV Charging Can Reduce Your LA Energy Costs in 2025",
    datePublished: "2026-04-15",
    dateModified: "2026-06-01", // When last updated
    author: "Amy",
    excerpt: "...",
    content: "..."
  },
  // ... more posts
];
```

#### **B. Update Blog Post Layout**

Add metadata display + schema:

```typescript
// pages/blog/[slug].tsx
import Head from 'next/head';
import { SchemaScript } from '@/components/SchemaScript';
import { blogPosts } from '@/lib/posts';

interface BlogPostProps {
  post: (typeof blogPosts)[0];
}

export default function BlogPost({ post }: BlogPostProps) {
  const baseUrl = 'https://amyelectric.com';
  const postUrl = `${baseUrl}/blog/${post.slug}`;

  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": post.title,
    "image": `${baseUrl}/img/blog/${post.slug}-og.jpg`,
    "datePublished": post.datePublished,
    "dateModified": post.dateModified,
    "author": {
      "@type": "Person",
      "name": "Amy",
      "description": "California C-10 licensed electrical contractor with 15+ years of experience",
      "image": `${baseUrl}/img/amy-headshot.jpg`,
      "url": baseUrl
    },
    "publisher": {
      "@type": "Organization",
      "name": "AMY Electric",
      "logo": {
        "@type": "ImageObject",
        "url": `${baseUrl}/img/logo.png`
      }
    },
    "description": post.excerpt,
    "articleBody": post.content
  };

  return (
    <>
      <Head>
        <title>{post.title} | AMY Electric Blog</title>
        <meta name="description" content={post.excerpt} />
        <link rel="canonical" href={postUrl} />
        <SchemaScript schema={articleSchema} />
      </Head>

      <article>
        <header>
          <h1>{post.title}</h1>
          <div className="post-meta">
            <span>By <strong>Amy</strong></span>
            {' | '}
            <time dateTime={post.datePublished}>
              Published: {new Date(post.datePublished).toLocaleDateString()}
            </time>
            {post.dateModified !== post.datePublished && (
              <>
                {' | '}
                <time dateTime={post.dateModified}>
                  Updated: {new Date(post.dateModified).toLocaleDateString()}
                </time>
              </>
            )}
          </div>
        </header>

        <div className="post-content">{post.content}</div>

        {/* Author bio */}
        <aside className="author-bio">
          <img src={`${baseUrl}/img/amy-headshot.jpg`} alt="Amy" width="100" />
          <div>
            <h3>About Amy</h3>
            <p>
              Amy is a California-licensed C-10 electrical contractor (License #981578) and 
              EVITP-certified for EV infrastructure (Cert #4051604). She has 15+ years of experience 
              in residential and commercial electrical work, specializing in panel upgrades, EV charger 
              installation, and whole-home rewiring. Amy founded Amy Electric in 2012 to bring 
              transparent, code-perfect electrical work to the Los Angeles area.
            </p>
          </div>
        </aside>
      </article>
    </>
  );
}
```

---

### 2.2 — Expand FAQ Answers

**Current state:** 1–3 sentence answers  
**Target:** 100–150 words per answer (3–5 paragraphs)

#### **Example Expansion**

**Before:**
> Q: Do you pull permits?  
> A: Yes — we handle all permitting and inspections with LADBS, LADWP, and other local jurisdictions. You don't have to do a thing.

**After:**
> Q: Do you pull permits?
> 
> A: Yes — we handle all permitting and inspections as part of every installation. This is a significant advantage because permits ensure code compliance, proper inspection, and full insurance coverage for your project.
>
> Specifically, we manage:
> - **LADBS (Los Angeles Department of Building and Safety):** For structural and code compliance permits
> - **LADWP (Los Angeles Department of Water and Power):** For electrical service upgrades and EV charger installations connected to the grid
> - **City/County Inspections:** Scheduling and coordination with local inspectors
> 
> The permit process typically takes 3–10 business days, depending on the scope. We handle all paperwork, plan submissions, and coordination with inspectors. Once work is complete, we arrange final inspection and obtain the Certificate of Completion (Final Sign-Off), which is required for insurance claims and future home sales.
>
> Many customers are surprised to learn that unpermitted work can void homeowner's insurance coverage and create liability issues. By permitting everything we do, we protect you legally and structurally.

---

### 2.3 — Add Author Bio to Homepage & All Content

**Homepage footer or "About" section:**

```html
<section class="founder-bio">
  <h2>Meet Amy</h2>
  <div class="bio-content">
    <img src="/img/amy-headshot.jpg" alt="Amy, founder of AMY Electric" width="200" />
    <div>
      <p>
        <strong>Amy</strong> is a California-licensed C-10 electrical contractor (License #981578) 
        with 15+ years of hands-on electrical expertise. She holds an EVITP certification (#4051604) 
        for electric vehicle charging infrastructure and has completed 2,000+ residential and commercial 
        electrical projects across Greater Los Angeles.
      </p>
      <p>
        Amy founded <strong>AMY Electric in 2012</strong> to bridge the gap between expert craftsmanship 
        and transparent pricing. She personally evaluates complex electrical problems and directs every 
        significant project, ensuring code-perfect work and customer satisfaction.
      </p>
      <p>
        When not on a job site, Amy builds custom tools to streamline electrical estimation and 
        project management—combining her passion for coding with her contracting expertise.
      </p>
    </div>
  </div>
</section>
```

---

## Phase 3: Content Depth (Weeks 3–4)

### 3.1 — Expand Service Pages (500+ words each)

**Current:** Service pages are brief (2–3 sentences)  
**Target:** 500+ words with sections, FAQ, internal links

**Template for each service page:**

```markdown
# [Service Name] in Los Angeles

## What We Do
[2–3 paragraphs explaining the service, why it's needed, what it accomplishes]

## Why Choose Us for [Service]
[3–5 key differentiators: experience, certification, LADWP coordination, warranty, etc.]

## Our Process
[Step-by-step walkthrough: 1. Inspection 2. Quote 3. Scheduling 4. Installation 5. Inspection]

## Common Questions
[3–5 FAQs specific to this service, 100+ words each]

## Service Pricing
[Transparent pricing ranges, what's included, variables that affect cost]

## Related Services
[Internal links to adjacent services: e.g., "Need a panel upgrade for your EV charger? Learn more →"]

## Ready to Get Started?
[CTA: "Call (818) 302-5614 or request a free estimate"]
```

**Example: EV Charger Installation Page Outline**

```typescript
// pages/ev-charger-installation.tsx

const content = `
# EV Charger Installation in Los Angeles

## What We Install

AMY Electric installs Level 2 (240V) EV chargers for all electric vehicles, including Tesla, 
Rivian, Hyundai Ioniq, Chevrolet Bolt, Kia EV6, and others. Most homeowners in the Los Angeles 
area opt for a Level 2 charger because:

- **Faster charging:** 25–30 miles of range per hour (vs. 3 miles/hour with a standard 120V outlet)
- **Overnight charging:** Fully charge overnight with a typical daily commute
- **Cost-effective:** Lower installation cost than DC Fast Charger, works with existing home electrical service in many cases
- **Grid-friendly:** Can be set to charge during off-peak hours for lower electricity rates

We install Tesla Wall Connectors, Clipper Creek, ChargePoint, and most other brands. All installations 
are EVITP-certified, permitted, and inspected.

## Why Choose Amy Electric for EV Charger Installation

**EVITP-Certified:** Certification #4051604. This training covers EV charging system design, safety, 
code compliance, and best practices. It's the gold standard for professional installers.

**Transparent Pricing:** You'll know the cost upfront. Typical Level 2 installation: $350–$900 
(straightforward garage install with existing 240V service). If a panel upgrade is needed: add $2,500–$4,500.

**Permits & Inspection Handled:** We pull all permits with LADBS and LADWP, coordinate inspections, 
and obtain final sign-off. You don't touch a form.

**Code-Perfect Work:** All work meets NEC Article 625 (EV charging circuits), California Title 24 
(energy efficiency), and LADWP requirements. First-pass inspection rate: 99%.

**Direct Electrician Communication:** You talk to Amy or our lead electrician, not a call center. 
You get honest answers and real expertise.

## Our EV Charger Installation Process

### 1. Evaluation & Inspection (30 min — included in free estimate)
We assess your home's electrical panel capacity, existing 240V availability, wall condition, 
and distance from the electrical panel. This determines whether we can use existing service 
or need a panel upgrade.

### 2. Quote & Timeline
You receive a written estimate breaking down:
- Charger unit cost (if customer hasn't purchased)
- Installation labor
- Permitting & inspection fees
- Electrical upgrades (if any)
- Timeline (typically 2–4 weeks for permitting + 1–2 days for installation)

### 3. Permit Submission
We handle all paperwork, electrical plans, and coordination with LADBS and LADWP. 
Typical turnaround: 5–10 business days.

### 4. Installation (1–2 days)
- Run 240V circuit from breaker panel to installation location (if needed)
- Mount charger and connect to circuit
- Install weatherproof cover and ensure proper grounding
- Perform all tests and safety checks (continuity, resistance, voltage drop)

### 5. Final Inspection & Sign-Off
LADBS/LADWP inspector verifies the installation. We coordinate scheduling and attend inspection. 
Once approved, you receive Certificate of Completion (final sign-off).

### 6. Handoff & Support
We show you how to use the charger, explain any smart features, and provide warranty documentation.

## Pricing & What's Included

**Level 2 Installation (straightforward):** $350–$900
- Includes: charger mounting, circuit run, permits, inspection, warranty

**With 240V Circuit Run:** +$200–$500
- If you don't have existing 240V service

**With Panel Upgrade (100A → 200A):** +$2,500–$4,500
- Necessary if panel is at capacity or older than 30 years

**All-inclusive estimates:** We provide transparent line-item quotes. No surprises.

## Common Questions About EV Charger Installation

**Q: How much does EV charger installation cost in LA?**
A: Most Level 2 installations run $350–$900 for a straightforward garage install with existing 240V service. 
If a panel upgrade is also needed, expect $2,500–$4,500 additional. We provide free estimates after a 
brief on-site inspection (30 minutes). Factors that affect cost: distance from panel, existing electrical 
capacity, and whether upgrades are needed.

**Q: Do you install Tesla Wall Connectors specifically?**
A: Yes. Tesla Wall Connector (NEMA 14-50) installation is one of our specialties. We're EVITP-certified 
for Tesla infrastructure. Installation typically takes 1–2 days and costs $500–$800 if existing 240V is 
available. If you need a circuit run or panel upgrade, add $200–$500 or $2,500–$4,500 respectively.

**Q: How long does installation take?**
A: Permitting: 5–10 business days. Installation: 1–2 days. Total: 2–4 weeks from contract to final 
inspection sign-off. We can expedite for time-sensitive situations.

**Q: Will my Tesla/EV charge faster after installation?**
A: A Level 2 charger adds 25–30 miles of range per hour vs. 3 miles/hour with a standard 120V outlet. 
Most EV owners can fully charge overnight. DC Fast Chargers (Level 3) are installed by utility/commercial 
networks, not residential homes.

**Q: Do I need a panel upgrade?**
A: Maybe. If your home has a 200A service and is not at capacity, you likely don't need one. Older homes 
(100A service) almost always do. We inspect at no cost and let you know before giving a final quote.

## Related Services

- **Panel Upgrades:** Need 240V capacity for your charger? Learn about 100A → 200A upgrades.
- **Electrical Repairs:** Flickering lights or tripping breakers? Diagnose and fix.
- **Whole-Home Rewiring:** Older home? Full rewire ensures safety and EV-readiness.

## Ready? Get Your Free Estimate

Call (818) 302-5614 or fill out the form below. Licensed electrician will follow up within 2 hours.

[Estimate Form]
`;
```

**Effort:** ~2–4 hours per service page (6–8 service pages total = 12–32 hours)

---

### 3.2 — Build Internal Linking Map

**Goal:** Create topical clusters so Google and AI understand content relationships.

#### **A. Create linking strategy document:**

```
HOME
├── EV Charger Installation
│   ├── Links to → Blog: "EV Charging Benefits"
│   ├── Links to → Service: "Panel Upgrades" (for upgrades)
│   └── Links to → Service Area pages: "EV Charger Installation in Sherman Oaks"
│
├── Panel Upgrades
│   ├── Links to → Blog: "Panel Upgrade Signs"
│   ├── Links to → Blog: "Whole-Home Rewiring Guide" (related)
│   └── Links to → Service: "EV Charger Installation" (complement)
│
├── Electrical Repair
│   ├── Links to → Blog: "GFCI vs AFCI Protection"
│   └── Links to → Blog: "How to Choose an LA Electrician"
│
├── Blog (Archive)
│   ├── "EV Charging Benefits" → Links to Service: "EV Charger Installation"
│   ├── "Panel Upgrade Signs" → Links to Service: "Panel Upgrades"
│   ├── "How to Choose an LA Electrician" → Links to Service: "Electrical Repair"
│   └── "Whole-Home Rewiring Guide" → Links to Service: "Rewiring"
│
└── Service Areas (Sherman Oaks, Burbank, etc.)
    ├── Links to all Services
    └── Links to relevant testimonials/reviews
```

#### **B. Implementation (add hyperlinks):**

**In service pages, add "Related" section:**

```typescript
<section className="related-services">
  <h3>Related Services</h3>
  <ul>
    <li>
      <a href="/ev-charger-installation.html">
        EV Charger Installation (all types)
      </a>
    </li>
    <li>
      <a href="/panel-upgrade.html">
        200A Panel Upgrades for EV-Ready Homes
      </a>
    </li>
    <li>
      <a href="/blog/ev-charging-benefits.html">
        Blog: 5 Ways EV Charging Can Save You Money
      </a>
    </li>
  </ul>
</section>

<section className="related-blog">
  <h3>Learn More</h3>
  <ul>
    <li>
      <a href="/blog/panel-upgrade-signs.html">
        Panel Upgrade Signs (when you need one)
      </a>
    </li>
    <li>
      <a href="/blog/choosing-electrician-la.html">
        How to Choose an LA Electrician
      </a>
    </li>
  </ul>
</section>
```

**In blog posts, add CTA:**

```markdown
## Ready for an EV Charger?

Learn more about our [EV charger installation service](link) or 
[request a free estimate](estimate-link) today.
```

---

## Phase 4: Local SEO & Citations (Week 4)

### 4.1 — Google Business Profile Setup

**Goal:** Claim & optimize GBP so Amy Electric shows in Local Pack.

**Checklist:**
- [ ] Go to https://business.google.com
- [ ] Sign in with Amy's Google account
- [ ] Search for "AMY Electric, Los Angeles"
- [ ] Verify ownership (postcard sent to address, or phone verification)
- [ ] Fill out all fields:
  - Full business name: "AMY Electric"
  - Full street address (add to website if not already there)
  - Phone: (818) 302-5614
  - Website: https://amyelectric.com
  - Hours: Mon–Fri 7 AM–5 PM, Closed weekends
  - Service areas: Add all 16 cities
  - Services: EV Charger Installation, Panel Upgrades, Electrical Repair, etc.
  - Photos: Upload 10+ high-quality photos (job site, team, office, before/after)
  - Business category: Electrical Contractor
  - Description: Full business description

**Link GBP to website:**
Add schema markup to your home page linking to GBP:

```typescript
"sameAs": [
  "https://business.google.com/[GBP-ID]",
  "https://www.yelp.com/biz/amy-electric-los-angeles",
  "https://calevip.org/evsp/amy-electric"
]
```

---

### 4.2 — Directory Listings (Citations)

**Create accounts in these directories (NAP consistency: Name, Address, Phone must match exactly):**

| Directory | Link | Priority |
|-----------|------|----------|
| Better Business Bureau (BBB) | https://www.bbb.org | High |
| Angie's List | https://www.angieslist.com | High |
| HomeAdvisor | https://www.homeadvisor.com | High |
| Yelp (verify existing) | https://www.yelp.com | High |
| CALeVIP (verify) | https://calevip.org | High |
| The Spruce | https://www.thespruce.com | Medium |
| Nextdoor | https://nextdoor.com | Medium |

**Effort:** 4–6 hours total (30 min per directory)

---

## Phase 5: Testing & QA (Week 5)

### 5.1 — Schema Validation

Run each page through validators:

**Tools:**
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org
- JSON-LD Linter: https://linter.jsonld.io

**Expected results:**
```
✓ LocalBusiness schema: VALID
✓ Service schema (each service): VALID
✓ FAQPage schema: VALID
✓ BlogPosting schema (each post): VALID
✓ Review schema: VALID (3 reviews)
✓ BreadcrumbList schema: VALID
```

### 5.2 — On-Page SEO Audit

**Per-page checklist:**

- [ ] Title tag (50–60 characters, includes primary keyword)
- [ ] Meta description (150–160 characters, clear CTA)
- [ ] H1 (one per page, includes target keyword)
- [ ] H2/H3 hierarchy (logical nesting)
- [ ] Image alt text (descriptive, includes keyword if relevant)
- [ ] Internal links (3–5 per page minimum)
- [ ] Content length (500+ words for service pages, 1,200+ for guides)
- [ ] Canonical URL set
- [ ] Open Graph tags (og:title, og:description, og:image)
- [ ] Mobile responsiveness (test in Chrome DevTools)
- [ ] Page speed (Lighthouse Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1)

### 5.3 — Google Search Console Setup

**Setup:**
1. Go to https://search.google.com/search-console
2. Add property for amyelectric.com
3. Verify ownership (HTML file or DNS)
4. Submit sitemap: https://amyelectric.com/sitemap.xml
5. Monitor for indexing issues

**Check monthly:**
- Impressions & clicks by keyword
- Average position
- Coverage (indexed pages)
- Mobile usability issues
- Structured data errors

---

## Phase 6: Monitoring & Maintenance (Ongoing)

### 6.1 — Monthly Tasks

- [ ] Update blog with new post (target: 2–3 posts/month)
- [ ] Check Google Search Console for errors/opportunities
- [ ] Monitor Google Business Profile reviews & respond
- [ ] Update "Last Modified" date on pages that haven't changed but are still relevant
- [ ] Check search console for new keyword opportunities

### 6.2 — Quarterly Tasks

- [ ] Review top-performing pages (high impression, low CTR = needs title/meta improvement)
- [ ] Audit internal links (fix broken links)
- [ ] Refresh oldest blog posts with new data
- [ ] Check competitor keyword strategy

---

## Deployment Checklist

**Before deploying to production:**

- [ ] All schema markup validated (Google Rich Results Test: PASS)
- [ ] Mobile responsiveness tested (Chrome DevTools)
- [ ] Links tested (no 404s)
- [ ] Images optimized (<200KB each)
- [ ] Lighthouse SEO score: 90+
- [ ] Google Search Console setup complete
- [ ] Sitemap generated and submitted
- [ ] robots.txt configured
- [ ] All pages have canonical URLs
- [ ] OG tags tested (Facebook Sharing Debugger)
- [ ] Twitter Card tested

---

## Estimated Timeline & Effort

| Phase | Duration | Effort (hours) |
|-------|----------|-----------------|
| **1. Schema Markup** | 1 week | 8–12 |
| **2. Content Metadata** | 1 week | 6–8 |
| **3. Content Depth** | 2 weeks | 20–32 |
| **4. Local SEO** | 1 week | 6–8 |
| **5. Testing & QA** | 1 week | 4–6 |
| **Total** | **6–8 weeks** | **44–66 hours** |

---

## Code Resources & Libraries

### Next.js SEO Utilities

**Recommended libraries:**

```bash
npm install next-seo schema-dts
```

**next-seo example:**

```typescript
import { NextSeo } from 'next-seo';

export default function Page() {
  return (
    <>
      <NextSeo
        title="EV Charger Installation Los Angeles"
        description="Professional Level 2 EV charger installation..."
        canonical="https://amyelectric.com/ev-charger-installation.html"
        openGraph={{
          type: 'website',
          url: 'https://amyelectric.com/ev-charger-installation.html',
          title: 'EV Charger Installation | AMY Electric',
          description: 'Professional installation...',
          images: [
            {
              url: 'https://amyelectric.com/img/ev-charger-og.jpg',
              width: 1200,
              height: 630,
              alt: 'EV charger installation'
            }
          ]
        }}
        twitter={{
          handle: '@amyelectric',
          cardType: 'summary_large_image'
        }}
      />
      {/* Page content */}
    </>
  );
}
```

### Image Optimization

```bash
npm install next-image-export-optimizer
```

Use `next/image` for all images:

```typescript
import Image from 'next/image';

<Image
  src="/img/ev-charger.jpg"
  alt="Level 2 EV charger installation"
  width={800}
  height={600}
  priority
/>
```

---

## Questions & Escalation

**If stuck on:**
- **Schema validation:** Google Rich Results Test error message + page URL
- **Performance:** Lighthouse report (DevTools → Lighthouse tab)
- **Indexing:** Google Search Console coverage report
- **Content:** Review audit document for topic/keyword guidance

**Reference documentation:**
- Schema.org: https://schema.org
- Google Search Central: https://developers.google.com/search
- Next.js SEO: https://nextjs.org/learn/seo/introduction-to-seo
- NEC 2020 (for electrical code citations): NFPA 70

---

**Deliverables checklist on completion:**
- ✅ Schema markup on all pages (validated)
- ✅ Author bios on homepage + blog
- ✅ Publish/update dates on blog posts
- ✅ 500+ word service pages with FAQs
- ✅ Internal linking map implemented
- ✅ Google Business Profile claimed & linked
- ✅ Directory citations created (BBB, Angie's List, etc.)
- ✅ Sitemap & robots.txt deployed
- ✅ Google Search Console setup
- ✅ Lighthouse SEO score: 90+

---

**Owner:** Amy  
**Dev Lead:** [Your name]  
**Status:** [Track in project board]
