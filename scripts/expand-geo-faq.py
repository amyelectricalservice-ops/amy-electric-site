import os, re

root = "/home/amram/WEBSITE"

city_name_map = {
    "beverly-hills": "Beverly Hills", "burbank": "Burbank", "calabasas": "Calabasas",
    "culver-city": "Culver City", "encino": "Encino", "glendale": "Glendale",
    "hollywood": "Hollywood", "los-angeles": "Los Angeles",
    "north-hollywood": "North Hollywood", "pasadena": "Pasadena",
    "santa-monica": "Santa Monica", "sherman-oaks": "Sherman Oaks",
    "studio-city": "Studio City", "van-nuys": "Van Nuys",
    "west-la": "West LA", "woodland-hills": "Woodland Hills",
}

# --- Panel upgrade geo templates (7 Qs, each 134-167 words) ---
panel_templates = [
    # Q1: Cost
    (
        "How much does panel upgrade cost in {city}?",
        "A standard 100A to 200A panel upgrade in {city} typically ranges from $2,500 to $4,500, depending on the complexity of the installation and the condition of your existing service equipment. This price includes the new 200A panel and main breaker, all labor, permit fees through {city}'s building department, and the required final inspection. Additional charges may apply if your service mast or weatherhead needs replacement, if new grounding electrodes are required by the current code, or if trenching is needed for an underground service conversion. Older homes in {city} often require meter socket upgrades or conduit repairs that add $500 to $1,200 to the total. We provide free, detailed estimates with a full line-item breakdown after an on-site evaluation so you know the exact cost upfront, with no hidden fees or surprises. According to the California Building Performance Association, upgrading to 200A service has become the standard recommendation for California homes undergoing electrification retrofits."
    ),
    # Q2: License
    (
        "Are you licensed to work in {city}?",
        "Yes — AMY Electric holds an active California C-10 Electrical Contractor license (#981578), which is verified and in good standing with the Contractors State License Board (CSLB). You can confirm our license status yourself at cslb.ca.gov by entering our license number online or by calling (800) 321-CSLB, and our EVITP certification (#4051604) can be verified through the EVITP website. We carry comprehensive general liability insurance and workers compensation coverage for all employees, with certificates of insurance available upon request for any homeowner in {city}. We also maintain all required business licenses for {city} and Los Angeles County and renew them annually. Every project we perform is backed by the CSLB-mandated contractor bond and is fully permitted through the local building department, ensuring full legal and financial protection for every {city} homeowner we serve."
    ),
    # Q3: Duration
    (
        "How long does panel upgrade take in {city}?",
        "A standard 100A to 200A panel upgrade in {city} is typically completed in 4 to 8 hours for the physical installation, with the total project spanning 1 to 3 days when you account for permitting and LADWP coordination. The permit application through {city}'s building department is usually processed within 24 to 72 hours for standard electrical permits. On installation day, our electricians arrive in the morning, perform the upgrade with a brief power interruption of 2 to 4 hours, and fully restore all circuits by the afternoon. For projects requiring LADWP service coordination — such as underground service conversions or mast replacements — the timeline extends to 1 to 3 weeks due to utility scheduling. We provide a precise timeline during your free on-site estimate, and we always communicate any scheduling changes promptly so you know exactly when to expect power restoration."
    ),
    # Q4: Same-day
    (
        "Do you offer same-day service in {city}?",
        "Call (818) 302-5614 to discuss current emergency dispatch availability for urgent electrical situations in {city} and throughout Greater Los Angeles. Common emergencies include complete power outages affecting only your home, sparking or smoking electrical panels, exposed live wires, burning odors, and water near electrical equipment. Call 911 first for active fire, severe shock, or downed power lines."
    ),
    # Q5: Home value
    (
        "Will a panel upgrade increase my home's value in {city}?",
        "Yes — upgrading from 100A to 200A service is consistently ranked as one of the highest-ROI electrical improvements you can make to a {city} home. Many {city} home buyers specifically search for properties with 200A service because modern 200A panels accommodate Level 2 EV charging, central air conditioning with heat pumps, all-electric kitchen appliances, tankless water heaters, and future home additions or ADUs without requiring an immediate electrical service upgrade after moving in. Real estate agents across Los Angeles consistently report that 200A panels are a strong selling point that can increase a home's marketability and final sale price by a measurable amount compared to similar homes with outdated 100A service. With the growing adoption of electric vehicles and California's aggressive push toward building electrification through programs like the California Energy Commission's Title 24 requirements, a 200A panel is becoming a must-have feature for home buyers rather than just a nice-to-have upgrade."
    ),
    # Q6: LADWP
    (
        "Do you handle LADWP coordination for panel upgrades in {city}?",
        "Absolutely — we manage the complete LADWP coordination process for every panel upgrade we perform in {city} so you never have to deal with the utility company or fill out any of their paperwork yourself. This includes submitting the service upgrade application to LADWP, scheduling the meter pull before installation begins, coordinating the meter release inspection after work is complete, and scheduling the final reconnection of power once LADWP has approved the installation. Our team handles all required paperwork, including load letters and service agreements, and we communicate directly with LADWP's service planning department to ensure your upgrade meets all utility requirements. For {city} homes that are within LADWP's service territory, we also coordinate any necessary tree trimming, overhead service clearance, or temporary power arrangements during the upgrade process."
    ),
    # Q7: Need for upgrade
    (
        "How do I know if my {city} home needs a 200A panel?",
        "If your {city} home was built before 1990, it most likely has 100A service — which may no longer be adequate for today's electrical demands. Common signs that you need a 200A panel include: your main breaker trips frequently when running multiple appliances simultaneously, you are planning to install a Level 2 EV charger or a heat pump HVAC system, your lights dim noticeably when the air conditioner or washing machine starts, your panel has no remaining empty breaker slots for new circuits, or you are considering adding an ADU, home office, or major kitchen remodel in the near future. We offer free on-site evaluations in {city} where we measure your current electrical load using professional software and recommend the most cost-effective upgrade path for your specific situation and budget, with no obligation to proceed."
    ),
]

# --- EV charger geo templates (7 Qs, each 134-167 words) ---
ev_templates = [
    # Q1: Cost
    (
        "How much does ev charger installation cost in {city}?",
        "Most Level 2 EV charger installations in {city} range from $350 to $900 for a straightforward garage installation where the charger is located close to the electrical panel, with the total cost reaching $1,500 to $2,500 for more complex installations that require a panel upgrade, trenching, or long wiring runs through finished walls. The installation cost includes the dedicated 40- to 60-amp circuit breaker, conduit and wiring from the panel to the charging location, installation and hardwiring of the charging station, all permit fees through {city}'s building department, and the required electrical inspection. The price of the actual EV charger unit itself — typically $400 to $750 for most Level 2 chargers — is separate from the installation cost. We provide free, detailed estimates with full line-item breakdowns before any work begins."
    ),
    # Q2: License
    (
        "Are you licensed to work in {city}?",
        "Yes — AMY Electric holds an active California C-10 Electrical Contractor license (#981578), which is verified and in good standing with the Contractors State License Board (CSLB). You can confirm our license status yourself at cslb.ca.gov by entering our license number online or by calling (800) 321-CSLB, and our EVITP certification (#4051604) can be verified through the EVITP website. We carry comprehensive general liability insurance and workers compensation coverage for all employees, with certificates of insurance available upon request for any homeowner in {city}. We also maintain all required business licenses for {city} and Los Angeles County and renew them annually. Every project we perform is backed by the CSLB-mandated contractor bond and is fully permitted through the local building department, ensuring full legal protection for every {city} homeowner we serve."
    ),
    # Q3: Duration
    (
        "How long does ev charger installation take in {city}?",
        "Most residential Level 2 EV charger installations in {city} take 2 to 4 hours for a straightforward installation where the charger is located in a garage or carport within 25 to 50 feet of the electrical panel. Installations requiring longer wiring runs, conduit routing through finished walls or ceilings, or a panel load calculation review typically take 4 to 6 hours. If your home needs a panel upgrade to accommodate the EV charger — which is common for {city} homes with 100A service — the total project extends to 1 to 2 days, including both the panel upgrade and the charger installation on consecutive days. Permit processing through {city}'s building department adds 24 to 72 hours before installation day. We schedule all work after permit approval to ensure everything is fully permitted and inspected before you begin charging your EV."
    ),
    # Q4: Same-day
    (
        "Do you offer same-day service in {city}?",
        "Call (818) 302-5614 to discuss current emergency dispatch availability for urgent electrical situations in {city} and throughout Greater Los Angeles. Common emergencies include complete power outages affecting only your home, sparking or smoking electrical panels, exposed live wires, burning odors, and water near electrical equipment. Call 911 first for active fire, severe shock, or downed power lines."
    ),
    # Q5: Permit
    (
        "Do I need a permit to install an EV charger in {city}?",
        "Yes — all EV charger installations in {city} require an electrical permit through the local building department, and AMY Electric handles the entire permitting process for every installation we perform at no additional hassle to you. The permit typically costs $75 to $200 depending on {city}'s fee schedule and covers plan review, the rough-in wiring inspection, and the final inspection of the completed installation. Permitting ensures that your EV charger installation meets all current California Electrical Code requirements, including proper circuit sizing, GFCI protection where required, correct conduit fill, and load calculations that verify your panel has adequate capacity for the additional 40- to 60-amp load. An unpermitted EV charger installation can void your homeowners insurance coverage and must be disclosed if you sell your home, potentially reducing its resale value and causing title complications."
    ),
    # Q6: Rebates
    (
        "What rebates are available for EV charger installation in {city}?",
        "LADWP offers up to $500 in rebates for qualifying Level 2 EV charger installations for residential customers within their service territory, which covers most of {city}. Southern California Edison customers in certain parts of {city} may qualify for up to $1,000 through the Pre-Owned EV Rebate program, which includes charger installation support. The California Air Resources Board (CARB) also offers the Clean Vehicle Rebate Project for EV purchases, and many {city} homeowners can combine the federal 30% tax credit for EV charger installation — up to $1,000 — with local utility rebates for significant total savings of $1,000 or more. We help every {city} customer identify and apply for all available rebates and provide all required documentation including invoices, permit records, and inspection certificates needed for each rebate or tax credit application."
    ),
    # Q7: Tesla
    (
        "Do you offer Tesla Wall Connector installation in {city}?",
        "Yes — we are experienced, EVITP-certified Tesla Wall Connector installers serving {city} and all of Greater Los Angeles. We install the Tesla Wall Connector on both 60-amp circuits for the full 11.5 kW charging speed and 50-amp or 40-amp circuits where panel capacity is limited. Every Tesla installation includes proper conduit routing, torque-spec tightening of all connections per Tesla's installation manual, commissioning and Wi-Fi setup through the Tesla app, and a full demonstration of the charger's features including scheduled charging, power sharing, and load management. We also install the Tesla Universal Wall Connector, which is compatible with both Tesla's NACS connector and standard J1772 EVs. All Tesla charger installations are fully permitted, inspected, and backed by our workmanship warranty for your complete peace of mind and compliance with local code requirements."
    ),
]

def expand_file(path, city_name, templates):
    with open(path) as f:
        content = f.read()

    for question, answer in templates:
        q_city = question.replace("{city}", city_name)
        a_text = answer.replace("{city}", city_name)

        # Replace in JSON-LD (uses plain apostrophe)
        json_pat = r'"name"\s*:\s*"' + re.escape(q_city) + r'"[\s\S]*?"acceptedAnswer"\s*:\s*\{[^}]*?"text"\s*:\s*"'
        # Find the start of the answer text in the JSON-LD block
        m = re.search(json_pat, content)
        if m:
            start = m.end()
            # Find the closing quote
            end = content.index('"', start)
            content = content[:start] + a_text + content[end:]
        else:
            # Try with HTML entity apostrophe
            q_html = q_city.replace("'", "&#8217;")
            json_pat2 = r'"name"\s*:\s*"' + re.escape(q_html) + r'"[\s\S]*?"acceptedAnswer"\s*:\s*\{[^}]*?"text"\s*:\s*"'
            m = re.search(json_pat2, content)
            if m:
                start = m.end()
                end = content.index('"', start)
                content = content[:start] + a_text + content[end:]
            else:
                print(f"  WARNING: Could not find Q in JSON: {q_city[:50]}")

        # Replace in visible FAQ (uses HTML entity apostrophe &#8217;)
        q_visible = q_city.replace("'", "&#8217;")
        visible_pat = r'(<summary class="faq-q">)' + re.escape(q_visible) + r'(\s*<span class="faq-chevron">▾</span></summary><div class="faq-a">)[^<]+(</div>)'
        m = re.search(visible_pat, content)
        if m:
            content = re.sub(visible_pat, lambda m2, a=a_text: m2.group(1) + q_visible + m2.group(2) + a_text + m2.group(3), content, count=1)
        else:
            print(f"  WARNING: Could not find Q in visible: {q_visible[:50]}")

    with open(path, 'w') as f:
        f.write(content)

for fname in sorted(os.listdir(root)):
    if not fname.startswith("panel-upgrade-") or not fname.endswith(".html"):
        continue
    city_slug = fname.replace("panel-upgrade-", "").replace(".html", "")
    if city_slug in city_name_map:
        city = city_name_map[city_slug]
        print(f"Panel: {city}...")
        expand_file(os.path.join(root, fname), city, panel_templates)

for fname in sorted(os.listdir(root)):
    if not fname.startswith("ev-charger-installation-") or not fname.endswith(".html"):
        continue
    city_slug = fname.replace("ev-charger-installation-", "").replace(".html", "")
    if city_slug in city_name_map:
        city = city_name_map[city_slug]
        print(f"EV: {city}...")
        expand_file(os.path.join(root, fname), city, ev_templates)

print("Geo FAQ expansion complete.")
