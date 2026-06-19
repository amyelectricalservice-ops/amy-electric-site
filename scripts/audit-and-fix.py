#!/usr/bin/env python3
"""
Audit and Fix Script for AMY Electric Site:
1. L1: Fix Breadcrumb Text Formatting on all blog files (31 files).
2. L2: Add WebSite + SearchAction Schema to all city pages (16 files).
3. M3: Add customized HowTo Schema to remaining 11 service pages.
"""

import os
import glob
import re
import json

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- 1. Breadcrumb List Fix mappings ---
# We split camelCase and fix common missing spaces and colon run-on patterns.
TYPO_REPLACEMENTS = {
    "Costin": "Cost in",
    "Tipsfor": "Tips for",
    "Chargerin": "Charger in",
    "InstallationMakes": "Installation Makes",
    "Upgradesfor": "Upgrades for",
    "Upgradein": "Upgrade in",
    "Codefor": "Code for",
    "Tipsfor": "Tips for",
}

def fix_blog_breadcrumbs():
    print("\n--- Fixing Blog Breadcrumb Text Formatting ---")
    blog_files = glob.glob(os.path.join(SITE_DIR, "blog", "*.html"))
    fixed_count = 0
    
    for filepath in blog_files:
        stem = os.path.basename(filepath)
        if stem == "index.html":
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            
        original_html = html
        
        # 1. Regex to find the BreadcrumbList JSON-LD block
        match = re.search(r'("@type"\s*:\s*"BreadcrumbList"[^<]+)', html)
        if match:
            breadcrumb_block = match.group(1)
            original_block = breadcrumb_block
            
            # Apply typo replacements
            for typo, repl in TYPO_REPLACEMENTS.items():
                if typo in breadcrumb_block:
                    breadcrumb_block = breadcrumb_block.replace(typo, repl)
            
            # Regex to find a colon followed immediately by a letter/number without a space, e.g. "Angeles:What" -> "Angeles: What"
            # Since JSON-LD uses double quotes, we make sure it's not part of URL like "https://..."
            # Let's search inside the "name" values only to be completely safe.
            # Example in JSON: "name": "200 Amp Panel Upgrade Cost in Los Angeles:Complete Pricing Guide"
            def colon_replacer(m):
                name_val = m.group(1)
                # Replace colons followed by word chars that have no space
                fixed_val = re.sub(r':([A-Za-z0-9])', r': \1', name_val)
                return f'"name": "{fixed_val}"'
                
            breadcrumb_block = re.sub(r'"name"\s*:\s*"([^"]+)"', colon_replacer, breadcrumb_block)
            
            if breadcrumb_block != original_block:
                html = html.replace(original_block, breadcrumb_block)
                fixed_count += 1
                print(f"  Fixed breadcrumb format in {stem}")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html)
                    
    print(f"Completed blog breadcrumb fixes: {fixed_count} files updated.")


# --- 2. Add WebSite Schema to City Pages ---
WEBSITE_SCHEMA_TEMPLATE = """<!-- WebSite + SearchAction Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "AMY Electric",
  "url": "https://amyelectric.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://amyelectric.com/?q={search_term_string}"
    }
  }
}
</script>
"""

CITY_PAGES = [
    "city-los-angeles.html",
    "city-sherman-oaks.html",
    "city-burbank.html",
    "city-glendale.html",
    "city-pasadena.html",
    "city-studio-city.html",
    "city-north-hollywood.html",
    "city-hollywood.html",
    "city-beverly-hills.html",
    "city-west-la.html",
    "city-encino.html",
    "city-santa-monica.html",
    "city-van-nuys.html",
    "city-woodland-hills.html",
    "city-calabasas.html",
    "city-culver-city.html"
]

def add_website_schema_to_cities():
    print("\n--- Adding WebSite Schema to City Pages ---")
    added_count = 0
    
    for filename in CITY_PAGES:
        filepath = os.path.join(SITE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP {filename} (not found)")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            
        if "WebSite" in html:
            print(f"  {filename} already has WebSite schema")
            continue
            
        # Insert before </head>
        if "</head>" in html:
            html = html.replace("</head>", f"{WEBSITE_SCHEMA_TEMPLATE}\n</head>", 1)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            added_count += 1
            print(f"  Added WebSite schema to {filename}")
        else:
            print(f"  ERROR: </head> not found in {filename}")
            
    print(f"Completed WebSite schema addition: {added_count} files updated.")


# --- 3. Add HowTo Schema to 11 Service Pages ---
HOWTO_SCHEMAS = {
    "ceiling-fan-installation.html": {
        "name": "How to Install a Ceiling Fan in Los Angeles",
        "description": "Professional ceiling fan installation process: safety prep, mounting bracket installation, motor assembly, wiring connection, and balancing.",
        "steps": [
            ("Turn Power Off", "We turn off the circuit breaker at the main panel, test the wires at the box to ensure they are dead, and verify a secure work environment."),
            ("Inspect / Install Support Box", "We verify that the junction box is ceiling fan-rated. If not, we install an approved fan-rated box and brace to handle the weight and vibration."),
            ("Mount Support Bracket", "We attach the fan's mounting bracket to the junction box using heavy-duty screws, ensuring it's perfectly level."),
            ("Assemble and Hang Fan", "We assemble the fan motor, downrod, and canopy, then lift the assembly onto the mounting bracket."),
            ("Connect Wiring", "We wire the fan (ground, neutral, hot motor, and light kit wires) using wire nuts, and tuck the wiring neatly into the box."),
            ("Attach Blades and Test", "We attach the fan blades and light kit, verify balancing to prevent wobble, restore power, and test all speeds and controls.")
        ],
        "totalTime": "PT2H"
    },
    "commercial-electrical.html": {
        "name": "How to Handle Commercial Electrical Upgrades in Los Angeles",
        "description": "Professional commercial electrical service process: load assessment, planning & permitting, power isolation, commercial-grade installation, and testing.",
        "steps": [
            ("Load and Code Assessment", "We assess your commercial property's power requirements, phases, and any specific code compliance needs."),
            ("Permitting and Utility Coordination", "We submit plans to LADBS or local building departments and coordinate with the utility provider for service changes."),
            ("Safety Isolation", "We perform Lockout/Tagout (LOTO) safety protocols to isolate the circuits or feed before starting any installation."),
            ("Commercial-Grade Installation", "We install heavy-duty, commercial-grade components, EMT conduit, commercial panels, or specialized three-phase equipment."),
            ("Testing and Load Balancing", "We test the completed installation under operational load, measure phase balance, and verify safety controls are fully active.")
        ],
        "totalTime": "PT16H"
    },
    "dedicated-circuits.html": {
        "name": "How to Install a Dedicated Circuit in Los Angeles",
        "description": "Professional dedicated circuit installation process: load calculation, conduit & wire run, panel connection, and outlet installation.",
        "steps": [
            ("Load Calculation", "We calculate the appliance's power draw and select the correct wire gauge and circuit breaker size (e.g., 20A, 30A, 50A) to prevent overload."),
            ("Path Planning and Conduit Run", "We plan the route from the panel to the appliance and install conduit or run Romex cable through walls, attics, or crawlspaces."),
            ("Install Outlet or Disconnect", "We mount the new receptacle box or safety disconnect switch at the appliance location, wiring the ground, neutral, and hot wires."),
            ("Panel Connection and Breaker Install", "We wire the new cable into the main electrical panel, install the new dedicated breaker, and connect the circuit."),
            ("Testing and Calibration", "We restore power, test voltage and polarity at the new outlet, verify ground safety, and test under load.")
        ],
        "totalTime": "PT3H"
    },
    "electrical-repair.html": {
        "name": "How to Perform Electrical Repairs Safely in Los Angeles",
        "description": "Professional electrical repair process: safety troubleshooting, diagnostic testing, component replacement, and system verification.",
        "steps": [
            ("Isolate and Test", "We shut off power to the affected circuit and use a non-contact voltage tester to verify the line is dead before starting work."),
            ("Troubleshoot and Diagnose", "We inspect the faulty component (e.g., outlet, breaker, switch, or wiring joint) and perform continuity and voltage tests to find the root cause."),
            ("Replace Defective Parts", "We remove the faulty component and install a code-compliant, commercial-grade replacement."),
            ("Verify Wire Connections", "We inspect surrounding connections, tighten terminals, and ensure proper grounding of the entire box."),
            ("Restore and Test", "We turn the power back on, test voltage, polarity, and GFCI/AFCI functions, and verify the circuit is working safely.")
        ],
        "totalTime": "PT2H"
    },
    "electrical-safety-inspections.html": {
        "name": "How to Conduct a Comprehensive Home Electrical Safety Inspection",
        "description": "Step-by-step home electrical safety inspection: panel review, outlet & switch testing, grounding check, and safety device verification.",
        "steps": [
            ("Main Electrical Panel Review", "We inspect the main service panel for corrosion, tight connections, proper breaker sizing, and thermal anomalies."),
            ("GFCI and AFCI Device Testing", "We test all ground fault and arc fault circuit interrupters throughout the house to ensure they trip and reset properly."),
            ("Outlet and Switch Diagnostic", "We test representative outlets for proper polarity, solid ground connections, and correct physical condition."),
            ("Grounding and Bonding System Check", "We inspect the water pipe bonds, ground rods, and connection clamps to ensure a reliable system ground."),
            ("Smoke and CO Detector Verification", "We check the age, battery power, and interlink operation of all smoke and carbon monoxide detectors.")
        ],
        "totalTime": "PT3H"
    },
    "lighting-installation.html": {
        "name": "How to Install Recessed and Decorative Lighting in Los Angeles",
        "description": "Professional lighting installation process: fixture layout, ceiling prep, conduit/wire routing, fixture mounting, and switch/dimmer integration.",
        "steps": [
            ("Layout Design and Planning", "We measure the space, calculate lighting coverage, and map out the exact fixture locations on the ceiling."),
            ("Ceiling Preparation", "We cut precise circular or rectangular holes for the lighting housings, taking care to avoid structural joists."),
            ("Run Wiring and Feed", "We route new lighting cables from the switch location through the ceiling to each light box."),
            ("Mount and Connect Fixtures", "We wire the fixtures (ground, neutral, hot), secure the housings into the ceiling, and insert the LED trim or bulb."),
            ("Install Switch or Dimmer", "We replace or wire the wall switch box with a high-quality dimmer or smart switch designed for LED lighting."),
            ("System Testing", "We turn on the power, adjust trim settings on the dimmers, and verify consistent, flicker-free operation.")
        ],
        "totalTime": "PT4H"
    },
    "outlet-switch-installation.html": {
        "name": "How to Install or Replace Outlets and Switches",
        "description": "Professional outlet and switch replacement process: circuit safety check, wire prep, device connection, and functional testing.",
        "steps": [
            ("Safety Shutoff and Verification", "We turn off the circuit breaker, remove the cover plate, and use a multimeter to verify no voltage is present."),
            ("Disconnect Old Device", "We unscrew the outlet or switch from the box, gently pull it out, and disconnect the wires from the terminals."),
            ("Inspect and Prep Wires", "We inspect the insulation of existing wires, clip and strip fresh copper ends if needed, and verify proper ground availability."),
            ("Wire the New Device", "We connect the wires to the correct terminals: green/bare to ground, white to silver (neutral), black to brass (hot), and screw tightly."),
            ("Secure and Mount", "We fold the wires neatly into the junction box, screw the device into place, align it straight, and attach the cover plate."),
            ("Restore Power and Test", "We turn the breaker back on, test with a receptacle tester for proper wiring, and verify GFCI trip function if applicable.")
        ],
        "totalTime": "PT1H"
    },
    "smart-home-electrical.html": {
        "name": "How to Integrate Smart Switches and Home Automation",
        "description": "Professional smart device installation process: neutral wire verification, smart switch wiring, hub integration, and testing.",
        "steps": [
            ("Verify Neutral Wire", "Most smart switches require a neutral wire. We open the switch box to verify the presence of neutral (white) wires."),
            ("Isolate and Disconnect", "We shut off power to the circuit, verify the line is dead, and remove the existing mechanical switch."),
            ("Wire the Smart Switch", "We connect the smart switch's wire leads: line (incoming hot), load (outgoing to light), neutral, and ground."),
            ("Mount and Secure", "Because smart switches are larger, we dress the wires carefully to fit the box, mount the switch, and add the plate."),
            ("Power Up and Pair", "We turn on the circuit breaker, verify the switch boots up, and configure/pair it with your home Wi-Fi or automation hub.")
        ],
        "totalTime": "PT2H"
    },
    "smoke-co-detector-installation.html": {
        "name": "How to Install Hardwired Smoke and CO Detectors",
        "description": "Professional smoke and carbon monoxide detector installation process: planning, routing 3-wire cable, box installation, wiring connections, and testing.",
        "steps": [
            ("Placement Planning", "We map out locations to meet California Building Code: inside every bedroom, outside sleeping areas, and on every level."),
            ("Box Installation and Cable Run", "We cut holes in drywall and mount ceiling junction boxes. We run 14/3 three-wire cable between all detector locations to enable interconnected alarms."),
            ("Connect Alarms", "At each box, we wire the adapter harness: black (hot), white (neutral), and red (interconnect) for simultaneous alarming."),
            ("Mount and Insert Batteries", "We secure the detector mounting plate to the ceiling box, plug in the adapter, install the backup battery, and twist the detector onto the base."),
            ("Interconnect Testing", "We restore power, press the test button, and verify that triggering one alarm activates every alarm in the house.")
        ],
        "totalTime": "PT4H"
    },
    "surge-protection.html": {
        "name": "How to Install a Whole-Home Surge Protective Device (SPD)",
        "description": "Professional whole-house surge protector installation process: main breaker prep, SPD mounting, wiring to breaker, and verification.",
        "steps": [
            ("Turn Off Main Power", "We shut off the main utility breaker, verify the entire panel interior is dead using a multimeter, and set up safe working conditions."),
            ("Select Location and Mount", "We identify a knockout on the side of the main electrical panel and mount the whole-house surge protector securely."),
            ("Install Dedicated Double-Pole Breaker", "We install a new, dedicated 2-pole 20A or 30A breaker at the top of the panel to ensure the shortest path for surge dissipation."),
            ("Route and Connect Wires", "We cut the surge protector's leads as short and straight as possible. Wire the white to neutral bus, green to ground bus, and two black leads to the new breaker."),
            ("Power Up and Verify", "We re-energize the panel and verify the LED status indicators on the surge protective device are green and active.")
        ],
        "totalTime": "PT2H"
    },
    "tesla-charger-installation.html": {
        "name": "How to Install a Tesla Wall Connector",
        "description": "Professional Tesla Wall Connector installation process: load calculation, conduit run, wall connector mounting, circuit connection, and commissioning.",
        "steps": [
            ("Load Calculation and Breaker Selection", "We perform a load calculation of your electrical panel. We select the correct breaker size (typically 60A for maximum 48A charging)."),
            ("Conduit and Wire Run", "We run heavy-duty 6 AWG copper wires inside conduit from the electrical panel to the charging location (garage or exterior)."),
            ("Mount Tesla Wall Connector", "We secure the Wall Connector's low-profile mounting bracket to a wall stud or solid exterior surface."),
            ("Connect Wires and Ground", "We route wires into the Wall Connector, strip and secure them to the terminal block, and torque to Tesla's specifications."),
            ("Commissioning and WiFi Setup", "We turn on the circuit breaker, connect to the Wall Connector's temporary Wi-Fi network, configure the maximum amperage, and test charging.")
        ],
        "totalTime": "PT3H"
    }
}

def add_howto_schemas():
    print("\n--- Adding HowTo Schema to 11 Service Pages ---")
    added_count = 0
    
    for filename, data in HOWTO_SCHEMAS.items():
        filepath = os.path.join(SITE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP {filename} (not found)")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            
        if '"@type": "HowTo"' in html:
            print(f"  {filename} already has HowTo schema")
            continue
            
        # Build JSON-LD
        steps_json = []
        for pos, (name, text) in enumerate(data["steps"], 1):
            steps_json.append({
                "@type": "HowToStep",
                "position": pos,
                "name": name,
                "text": text
            })
            
        howto_data = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": data["name"],
            "description": data["description"],
            "step": steps_json,
            "totalTime": data["totalTime"]
        }
        
        howto_block = f"""<script type="application/ld+json">
{json.dumps(howto_data, indent=2, ensure_ascii=False)}
</script>
"""
        
        # Insert before </head>
        if "</head>" in html:
            html = html.replace("</head>", f"{howto_block}\n</head>", 1)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            added_count += 1
            print(f"  Added HowTo schema to {filename}")
        else:
            print(f"  ERROR: </head> not found in {filename}")
            
    print(f"Completed HowTo schema addition: {added_count} files updated.")


def main():
    print("=" * 60)
    print("Audit and Fix Execution for AMY Electric")
    print("=" * 60)
    
    fix_blog_breadcrumbs()
    add_website_schema_to_cities()
    add_howto_schemas()
    
    print("\n" + "=" * 60)
    print("All audits and fixes complete.")
    print("=" * 60)

if __name__ == "__main__":
    main()
