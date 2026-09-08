# AMY Electric — Electrical Services Skill

## Overview

This skill enables AI agents to interact with AMY Electric, a licensed C-10 electrical contractor serving the Greater Los Angeles area.

## Business Information

- **Name:** AMY Electric
- **License:** C-10 #981578
- **EVITP:** #4051604
- **Phone:** (818) 302-5614
- **Email:** info@amyelectric.com
- **Website:** https://amyelectric.com
- **Service Area:** Greater Los Angeles (16 cities, 62+ ZIP codes)

## Available Services

### Residential
- EV Charger Installation
- Panel Upgrades (100A to 200A, 200A to 400A)
- Whole Home Rewiring
- Generator Transfer Switch
- Smoke & CO Detector Installation
- Ceiling Fan Installation
- Outlet & Switch Installation
- Surge Protection
- Lighting Installation
- Dedicated Circuits
- Electrical Safety Inspections
- Smart Home Electrical
- Home Automation Electrical

### Commercial
- Commercial Electrical Services
- Commercial EV Charger Installation
- Commercial EV Fleet Charging
- Commercial Panel Upgrade
- Tenant Improvement Electrical
- Sub-Panel Installation

### Emergency
- Emergency Electrician
- Power Outage Repair
- Breaker Tripping
- Burning Smell Panel
- Same-Day Electrical Repair

## Service Areas

Los Angeles · Sherman Oaks · Burbank · Glendale · Pasadena · Santa Monica · West Hollywood · Beverly Hills · Culver City · Encino · Studio City · North Hollywood · Van Nuys · Tarzana · Woodland Hills · Calabasas

## How to Use This Skill

1. **Get Business Info:** Use the `get_business_info` tool to retrieve hours, license, and contact details
2. **List Services:** Use the `get_services` tool with optional category filter
3. **Request Estimate:** Use the `request_estimate` tool to pre-fill the contact form
4. **Navigate:** Use the `navigate_to_page` tool to move between sections

## API Endpoints

- **MCP Server Card:** `/.well-known/mcp/server-card.json`
- **OIDC Discovery:** `/.well-known/openid-configuration`
- **JWKS:** `/.well-known/http-message-signatures-directory`
- **Content Negotiation:** `Accept: text/markdown` for clean text

## Example Agent Interactions

### Get Business Hours
```
Agent: What are AMY Electric's business hours?
Tool: get_business_info()
Response: { "hours": { "monday-friday": "7:00 AM - 6:00 PM", "saturday": "8:00 AM - 4:00 PM", "sunday": "Closed" } }
```

### Find Services
```
Agent: What EV charger services do you offer?
Tool: get_services({ category: "ev" })
Response: ["EV Charger Installation", "Level 2 Charger Setup", "Commercial EV Charging Stations"]
```

### Request Estimate
```
Agent: I need a panel upgrade estimate
Tool: request_estimate({ name: "John", phone: "555-1234", service: "Panel Upgrade" })
Response: Estimate request prepared. Please complete the form and submit.
```

## Compliance

- Licensed C-10 #981578 (verify at CSLB)
- EVITP Certified #4051604
- 4.9★ Rated (87+ Reviews)
- Free Estimates
- Same-Day Response
