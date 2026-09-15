#!/usr/bin/env python3
"""Batch-expand all city-*.html pages with richer Local Knowledge and new FAQ items."""

import glob
import os
import re
import html

# ─── City-specific data ───────────────────────────────────────────────
# Each city gets: housing_stock, main_streets, landmarks, electrical_notes,
# plus 2-3 area-specific FAQ questions.

CITY_DATA = {
    "agoura-hills": {
        "housing": "Most homes were built between 1978 and 2005, with a mix of ranch-style houses, equestrian properties, and hillside custom homes. Many homes along Kanan Road and Cornell Road sit on large lots with longer utility runs.",
        "streets": "Kanan Road, Cornell Road, Devonshire Drive, Maria Drive, Chesebro Road",
        "landmarks": "The city borders the Santa Monica Mountains National Recreation Area, and many properties back onto open space. Reyes Adobe Days is a local tradition.",
        "electrical": "Properties in the hills often need subpanels or longer conduit runs for EV chargers. Older homes near the civic center may still have 100A service.",
        "faqs": [
            ("How much does an EV charger install cost in Agoura Hills?", "EV charger installation in Agoura Hills typically ranges from $1,200 to $3,500 depending on panel capacity, conduit distance, and charger type. Properties on larger hillside lots may see higher costs due to longer conduit runs. We provide free, detailed estimates — call (818) 302-5614."),
            ("Do you handle SCE permits in Agoura Hills?", "Yes — we manage all permitting with the City of Agoura Hills and coordinate with Southern California Edison for service upgrades, meter changes, and new service connections."),
            ("What electrical issues are common in Agoura Hills homes?", "Common issues include inadequate panel capacity for EV chargers, outdated wiring in older ranch homes, and ground-fault protection needed for outdoor outlets near equestrian areas and hillside properties."),
        ]
    },
    "alhambra": {
        "housing": "Alhambra's housing stock spans the 1920s through 1980s, with many Spanish-style and Craftsman homes in the older core near Main Street. Newer condos line Atlantic Boulevard.",
        "streets": "Main Street, Atlantic Boulevard, Valley Boulevard, Mission Road, Fremont Avenue",
        "landmarks": "The historic Alhambra High School, the Alhambra Place shopping center, and the San Gabriel Mission nearby. The city's dense residential core has a walkable downtown.",
        "electrical": "Older Craftsman and Spanish-style homes south of Main Street often have outdated wiring and 60A or 100A panels that need upgrading for modern loads. Multi-family properties along Atlantic may need commercial-grade panels.",
        "faqs": [
            ("Do you handle permits for Alhambra homes?", "Yes — we handle all permit applications, plan reviews, and inspections with the City of Alhambra Building Department. Permits are included in our estimates."),
            ("What panel upgrade options work for Alhambra's older homes?", "For Alhambra's 1920s-1940s homes, we typically recommend a full 200A service upgrade with a new panel, dedicated EV charger circuit, and updated grounding. We coordinate with SCE for the meter swap."),
            ("Are you familiar with Alhambra's historic district requirements?", "Yes — we've worked on homes in Alhambra's historic areas and understand the city's requirements for electrical work on older properties. We ensure all upgrades meet current code while respecting the home's character."),
        ]
    },
    "arcadia": {
        "housing": "Arcadia features a mix of 1950s ranch homes, 1970s tract housing, and newer custom-built homes. The city has one of the highest concentrations of EV ownership in the San Gabriel Valley.",
        "streets": "Huntington Drive, Baldwin Avenue, Duarte Road, Live Oak Avenue, Santa Anita Avenue",
        "landmarks": "Santa Anita Park, the LA County Arboretum, and the Arcadiaintptrace center. The city is known for excellent schools and well-maintained properties.",
        "electrical": "Many Arcadia homes have already been upgraded to 200A panels, but older homes near Huntington Drive may still have 100A service. EV charger installations are extremely common here.",
        "faqs": [
            ("How common are EV charger installations in Arcadia?", "Very common — Arcadia has one of the highest EV adoption rates in the San Gabriel Valley. We install Level 2 chargers in Arcadia homes weekly, often pairing with 200A panel upgrades."),
            ("Do you service Arcadia's newer construction?", "Yes — we work on both existing homes and new construction in Arcadia. For new builds, we coordinate with builders on rough-in wiring, panel placement, and EV-ready circuits."),
            ("What's the typical turnaround for a panel upgrade in Arcadia?", "Most panel upgrades in Arcadia take 1-2 days, including SCE coordination for the meter swap. We pull permits and handle all inspections."),
        ]
    },
    "arleta": {
        "housing": "Arleta is primarily 1950s and 1960s ranch-style homes with some newer construction. The neighborhood has a working-class character with many long-time residents.",
        "streets": "Arleta Avenue, Woodman Avenue, Osborne Street, Cantara Street, Kagel Canyon Street",
        "landmarks": "The neighborhood sits near the San Fernando Mission and has a strong community feel. Open space areas along the Tujunga Wash provide natural borders.",
        "electrical": "Many Arleta homes still have original 100A panels and knob-and-tube wiring in attics. Panel upgrades are especially important for EV charger installations.",
        "faqs": [
            ("Do you handle Arleta's older wiring issues?", "Yes — we regularly upgrade homes in Arleta with outdated wiring. We replace knob-and-tube, aluminum branch circuits, and upgrade panels to 200A for modern safety and capacity."),
            ("How much does a panel upgrade cost in Arleta?", "Panel upgrades in Arleta typically range from $2,500 to $4,500 depending on existing conditions, panel location, and whether we need to upgrade the service entrance. Free estimates."),
            ("Do you serve Arleta for emergency repairs?", "Yes — we provide 24/7 emergency electrical service throughout Arleta. Call (818) 302-5614 for immediate dispatch."),
        ]
    },
    "atwater-village": {
        "housing": "Atwater Village features charming 1920s and 1930s bungalows and Craftsman homes, many lovingly restored. The neighborhood has a small-town feel within the city.",
        "streets": "Glendale Boulevard, Crystal Street, Atwater Avenue, ls, Fletcher Drive",
        "landmarks": "The LA River bike path runs along the eastern edge, and the neighborhood's walkable commercial district along Glendale Boulevard offers local shops and restaurants.",
        "electrical": "Atwater's older homes often have outdated electrical systems, including knob-and-tube wiring and small panels. Restorations frequently require full electrical overhauls.",
        "faqs": [
            ("Do you work on Atwater Village's historic homes?", "Absolutely — we've upgraded electrical systems in many Atwater Village bungalows. We handle knob-and-tube replacement, panel upgrades, and rewiring while preserving the home's character."),
            ("What permits are needed for electrical work in Atwater Village?", "Permits are required for panel upgrades, rewiring, and new circuits in Atwater Village (City of Los Angeles). We handle all permit applications and inspections."),
            ("Can you add EV charger capability to a 1920s bungalow?", "Yes — we regularly install EV chargers in Atwater's older homes. This typically involves a panel upgrade to 200A, new dedicated circuit, and careful routing to minimize visual impact on the home."),
        ]
    },
    "bel-air": {
        "housing": "Bel Air features luxury estates ranging from 1920s Mediterranean villas to modern contemporary mansions. Many properties are gated with long driveways and expansive grounds.",
        "streets": "Bel Air Road, Sunset Boulevard, Mulholland Drive, Bellagio Road, Stradella Road",
        "landmarks": "The Bel Air Gate, the Hotel Bel-Air, and the Skirball Cultural Center. The neighborhood is one of the most exclusive in Los Angeles.",
        "electrical": "Estate properties often require commercial-grade electrical systems, whole-house generators, and sophisticated lighting control. Many homes have 400A service or multiple panels.",
        "faqs": [
            ("Do you handle estate-scale electrical in Bel Air?", "Yes — we service Bel Air's luxury estates with commercial-grade panels, whole-house generators, EV fleet charging, and smart home electrical systems. We understand the unique demands of large properties."),
            ("What electrical upgrades are common in Bel Air homes?", "Common upgrades include 400A service, generator transfer switches, landscape lighting, pool electrical, EV charging stations, and smart home wiring. We handle projects of any scale."),
            ("Do you coordinate with Bel Air's HOA requirements?", "Yes — we work with Bel Air's architectural review requirements and ensure all exterior electrical work meets the community's standards."),
        ]
    },
    "bellflower": {
        "housing": "Bellflower has a mix of 1950s ranch homes, 1960s tract housing, and newer construction. The city has a strong working-class community with improving property values.",
        "streets": "Bellflower Boulevard, Artesia Avenue, Alondra Boulevard, Clark Avenue, Greenleaf Boulevard",
        "landmarks": "The civic center area, local parks, and the nearby Los Angeles County Fire Museum. The city has a revitalizing downtown along Bellflower Boulevard.",
        "electrical": "Many Bellflower homes have 100A panels that need upgrading for modern electrical demands, especially EV charger installations and air conditioning upgrades.",
        "faqs": [
            ("Do you handle Bellflower's permit process?", "Yes — we manage all permits with the City of Bellflower Building Department. Permit costs are included in our estimates."),
            ("How long does a panel upgrade take in Bellflower?", "Most panel upgrades in Bellflower take 1-2 days. We coordinate with SCE for meter swaps and handle all inspections."),
            ("What electrical issues are common in Bellflower?", "Common issues include outdated panels, aluminum wiring from the 1960s-70s, and insufficient capacity for modern appliances and EV chargers."),
        ]
    },
    "beverly-grove": {
        "housing": "Beverly Grove features a mix of 1920s-1940s apartment buildings and newer condo developments. The residential areas have charming duplexes and small apartment buildings.",
        "streets": "Beverly Boulevard, Grove Drive, Third Street, Fairfax Avenue, Olympic Boulevard",
        "landmarks": "The Original Farmers Market, The Grove shopping center, and the Paley Center for Media. The neighborhood sits between Beverly Hills and Mid-Wilshire.",
        "electrical": "Older apartment buildings often have outdated electrical systems that need modernization. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle multi-family electrical in Beverly Grove?", "Yes — we service apartment buildings, duplexes, and condos throughout Beverly Grove. We handle common area electrical, individual unit upgrades, and EV charger installations for property owners."),
            ("What permits are needed for apartment electrical work?", "Multi-family electrical work in Beverly Grove requires permits from the City of Los Angeles. We handle all permit applications, plan reviews, and inspections."),
            ("Can you add EV chargers to apartment buildings?", "Yes — we install EV charging infrastructure for multi-family properties, including shared charging stations, individual unit circuits, and billing systems."),
        ]
    },
    "beverly-hills": {
        "housing": "Beverly Hills features some of the most valuable real estate in the world, from 1920s Mediterranean estates to modern architectural masterpieces. Properties range from cozy condos to sprawling compounds.",
        "streets": "Rodeo Drive, Sunset Boulevard, Wilshire Boulevard, Santa Monica Boulevard, Canon Drive",
        "landmarks": "Rodeo Drive, the Beverly Wilshire Hotel, Greystone Mansion, and the Wallis Annenberg Center. The city is synonymous with luxury living.",
        "electrical": "Properties often require 400A service, commercial-grade panels, whole-house generators, and sophisticated smart home electrical systems. EV charging infrastructure is standard in new construction.",
        "faqs": [
            ("Do you service Beverly Hills estates?", "Yes — we provide full-service electrical for Beverly Hills homes and estates, from panel upgrades to complete rewiring, smart home systems, and EV fleet charging. Licensed C-10 #981578."),
            ("What electrical upgrades do Beverly Hills homes need?", "Common upgrades include 400A service, generator transfer switches, smart lighting control, EV charging stations, pool and spa electrical, and security system wiring."),
            ("Do you handle Beverly Hills' permit requirements?", "Yes — we manage all permits with the City of Beverly Hills Building Department. We understand the city's requirements and coordinate all inspections."),
        ]
    },
    "beverlywood": {
        "housing": "Beverlywood is a quiet residential neighborhood with 1940s-1960s ranch homes and some newer construction. The tree-lined streets have a suburban feel within the city.",
        "streets": "Beverwood Drive, Robertson Boulevard, Pico Boulevard,(home), Beverlywood Street",
        "landmarks": "The neighborhood borders Culver City and Beverly Hills, with easy access to both. Local parks and quiet streets make it popular with families.",
        "electrical": "Most Beverlywood homes have 100A or 150A panels. Upgrades to 200A are common for EV charger installations and modern appliance loads.",
        "faqs": [
            ("Do you service Beverlywood homes?", "Yes — we provide full electrical services to Beverlywood residents, including panel upgrades, EV charger installation, rewiring, and lighting. Call (818) 302-5614."),
            ("What's the typical panel upgrade cost in Beverlywood?", "Panel upgrades in Beverlywood typically range from $2,500 to $4,000 depending on existing conditions. Free estimates for all Beverlywood projects."),
            ("Can you add EV charging to a 1950s ranch home?", "Absolutely — we install EV chargers in Beverlywood's older homes regularly. Most projects include a panel upgrade to 200A and a dedicated 240V circuit."),
        ]
    },
    "brentwood": {
        "housing": "Brentwood features a mix of 1920s-1940s homes, 1960s condos, and newer luxury construction. The area near the Getty Center has larger estates.",
        "streets": "San Vicente Boulevard, Sunset Boulevard, Barrington Avenue, Gretna Avenue, Montana Avenue",
        "landmarks": "The Getty Center, the Brentwood Country Club, and the Brentwood Village shopping district. The neighborhood has an upscale, walkable character.",
        "electrical": "Older homes near San Vicente often need panel upgrades for modern loads. Newer construction typically has 200A or 400A service with EV-ready circuits.",
        "faqs": [
            ("Do you handle Brentwood's older homes?", "Yes — we've upgraded electrical systems in many Brentwood homes, from 1920s Spanish-style to modern construction. We handle panel upgrades, rewiring, and EV charger installations."),
            ("What electrical work is common in Brentwood?", "Common projects include 200A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring. We handle residential and commercial work."),
            ("Do you coordinate with Brentwood's HOA requirements?", "Yes — we work with Brentwood's architectural review requirements and ensure all electrical work meets community standards."),
        ]
    },
    "burbank": {
        "housing": "Burbank has a diverse housing stock from 1920s bungalows to 1970s tract homes and newer developments. The city is home to major entertainment studios.",
        "streets": "Olive Avenue, Magnolia Boulevard, San Fernando Boulevard, Victory Boulevard, Alameda Avenue",
        "landmarks": "Walt Disney Studios, Warner Bros. Studios, NBC Studios, and the Burbank Town Center. The city has a strong entertainment industry presence.",
        "electrical": "Many Burbank homes have 100A panels that need upgrading. Studio-adjacent properties may have unique commercial electrical needs. EV charger installations are increasingly common.",
        "faqs": [
            ("Do you handle commercial electrical in Burbank?", "Yes — we provide commercial electrical services to Burbank businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What panel upgrades are common in Burbank?", "Most Burbank homes need 200A panel upgrades for modern electrical demands, especially EV charger installations. Older homes near the studios may need rewiring."),
            ("Do you serve Burbank's entertainment industry?", "Yes — we've worked with production companies and studios in Burbank on temporary power, lighting, and electrical infrastructure for productions."),
        ]
    },
    "calabasas": {
        "housing": "Calabasas features luxury homes from the 1970s onward, with many gated communities and custom estates. The city has strict building codes and environmental requirements.",
        "streets": "Las Virgenes Road, Mulholland Highway, Calabasas Road, Park Granada, Prado de las Flores",
        "landmarks": "The Commons at Calabasas, the Leonis Adobe Museum, and proximity to the Santa Monica Mountains. The city is known for its affluent, family-oriented community.",
        "electrical": "Many Calabasas homes have 200A or 400A service. EV charger installations are standard in newer construction, and solar panel integrations are common.",
        "faqs": [
            ("Do you handle Calabasas' building requirements?", "Yes — we understand Calabasas' building codes and environmental requirements. We handle all permits and ensure compliance with the city's standards."),
            ("What electrical upgrades are common in Calabasas?", "Common upgrades include 200A-400A panel upgrades, EV charger installation, solar panel integration, whole-house generators, and smart home electrical systems."),
            ("Do you install EV chargers in Calabasas gated communities?", "Yes — we install EV chargers in Calabasas gated communities, working with HOAs on installation requirements and coordinating with property management."),
        ]
    },
    "canoga-park": {
        "housing": "Canoga Park has a mix of 1950s-1970s tract homes, apartment buildings, and newer development. The neighborhood is part of the West San Fernando Valley.",
        "streets": "Sherman Way, Topanga Canyon Boulevard, Vanowen Street, Canoga Avenue, Owensmouth Avenue",
        "landmarks": "The Westfield Topanga mall, the Lanark Park area, and proximity to the Santa Susana Mountains. The neighborhood has a diverse, working-class character.",
        "electrical": "Many Canoga Park homes have 100A panels that need upgrading for modern electrical demands. Apartment buildings may need commercial-grade electrical systems.",
        "faqs": [
            ("Do you handle Canoga Park's permit process?", "Yes — we manage all permits with the City of Los Angeles for Canoga Park projects. Permit costs are included in our estimates."),
            ("What electrical issues are common in Canoga Park?", "Common issues include outdated panels, aluminum wiring from the 1970s, and insufficient capacity for EV chargers and modern appliances."),
            ("Do you service apartment buildings in Canoga Park?", "Yes — we provide electrical services to apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations for property owners."),
        ]
    },
    "carson": {
        "housing": "Carson features 1960s-1970s tract homes, some newer developments, and industrial areas. The city has a diverse population and strong community institutions.",
        "streets": "Carson Street, Avalon Boulevard, Figueroa Street, Alondra Boulevard, Dominguez Avenue",
        "landmarks": "California State University Dominguez Hills, the Carson Community Center, and the nearby Port of Los Angeles. The city has a mix of residential and commercial areas.",
        "electrical": "Many Carson homes have 100A panels that need upgrading. Industrial areas may have commercial electrical needs. EV charger installations are growing.",
        "faqs": [
            ("Do you handle residential and commercial in Carson?", "Yes — we provide both residential and commercial electrical services in Carson, including panel upgrades, EV charger installation, and tenant improvements."),
            ("What panel upgrades are available in Carson?", "We offer 200A and 400A panel upgrades for Carson homes and businesses. We coordinate with SCE for service upgrades and handle all permits."),
            ("Do you serve Carson's industrial areas?", "Yes — we provide commercial electrical services to Carson's industrial and business areas, including warehouse electrical, EV fleet charging, and lighting retrofits."),
        ]
    },
    "century-city": {
        "housing": "Century City features high-rise condos and apartments, with some older mid-century buildings and newer luxury developments. The area is primarily commercial with residential towers.",
        "streets": "Century Park East, Avenue of the Stars, Olympic Boulevard, Constellation Boulevard",
        "landmarks": "Westfield Century City mall, the Fox Studios lot, and numerous corporate headquarters. The area is a major business and entertainment hub.",
        "electrical": "High-rise buildings require commercial-grade electrical systems. Individual units may need panel upgrades for EV chargers and modern loads.",
        "faqs": [
            ("Do you handle high-rise electrical in Century City?", "Yes — we service Century City's high-rise residential buildings, including individual unit upgrades, common area electrical, and EV charger installations."),
            ("What permits are needed for Century City condo electrical?", "Condo electrical work in Century City requires permits from the City of Los Angeles. We handle all permits and coordinate with building management."),
            ("Can you add EV chargers to Century City condos?", "Yes — we install EV chargers in Century City condos, working with building management on infrastructure requirements and coordinating with the HOA."),
        ]
    },
    "chatsworth": {
        "housing": "Chatsworth features a mix of 1950s-1970s ranch homes, newer developments, and equestrian properties. The neighborhood has a semi-rural character in parts.",
        "streets": "Topanga Canyon Boulevard, Devonshire Street, Mason Avenue, Variel Avenue, De Soto Avenue",
        "landmarks": "The Santa Susana Mountains, the Chatsworth Nature Preserve, and the historic Chatsworth Park area. The neighborhood has both suburban and rural areas.",
        "electrical": "Many Chatsworth homes have 100A panels that need upgrading. Equestrian properties may have unique electrical needs for barns and outbuildings.",
        "faqs": [
            ("Do you handle Chatsworth's equestrian properties?", "Yes — we provide electrical services to Chatsworth's equestrian properties, including barn wiring, outdoor lighting, and panel upgrades for agricultural needs."),
            ("What electrical upgrades are common in Chatsworth?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes near the nature preserve."),
            ("Do you serve Chatsworth's newer developments?", "Yes — we work on both existing homes and new construction in Chatsworth, including rough-in wiring, panel placement, and EV-ready circuits."),
        ]
    },
    "cheviot-hills": {
        "housing": "Cheviot Hills features 1920s-1940s homes with some newer construction. The neighborhood has a quiet, residential character near Beverly Hills and Century City.",
        "streets": "Motor Avenue, Cheviot Drive, Castle Heights Avenue,_Exposition Boulevard",
        "landmarks": "The neighborhood borders the Hillcrest Country Club and has easy access to Beverly Hills and Century City. Local parks provide green space.",
        "electrical": "Many Cheviot Hills homes have older electrical systems that need modernization. Panel upgrades are common for EV charger installations.",
        "faqs": [
            ("Do you service Cheviot Hills homes?", "Yes — we provide full electrical services to Cheviot Hills residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What's the typical panel upgrade cost in Cheviot Hills?", "Panel upgrades in Cheviot Hills typically range from $2,500 to $4,000 depending on existing conditions. Free estimates for all projects."),
            ("Can you add EV charging to an older Cheviot Hills home?", "Absolutely — we install EV chargers in Cheviot Hills' older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "chinatown": {
        "housing": "Chinatown has a mix of 1920s-1940s apartment buildings, newer developments, and commercial properties. The neighborhood is experiencing rapid change and development.",
        "streets": "Broadway, Hill Street, North Broadway, Spring Street, College Street",
        "landmarks": "The historic Central Plaza, the Chinatown Central Library branch, and numerous cultural institutions. The neighborhood has a rich cultural heritage.",
        "electrical": "Older apartment buildings often have outdated electrical systems. New developments require modern electrical infrastructure. EV charger installations are growing.",
        "faqs": [
            ("Do you handle Chinatown's older buildings?", "Yes — we've upgraded electrical systems in many Chinatown buildings, from 1920s apartments to modern developments. We handle panel upgrades, rewiring, and code compliance."),
            ("What permits are needed for Chinatown electrical work?", "Electrical work in Chinatown requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties in Chinatown?", "Yes — we provide commercial electrical services to Chinatown businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "covina": {
        "housing": "Covina features 1950s-1970s ranch homes, some newer developments, and historic properties near downtown. The city has a suburban character with good schools.",
        "streets": "Azusa Avenue, Citrus Avenue, Badillo Street, San Bernardino Road, Lark Ellen Avenue",
        "landmarks": "Historic downtown Covina, the Covina Center for the Performing Arts, and the nearby San Gabriel Mountains. The city has a charming downtown district.",
        "electrical": "Many Covina homes have 100A panels that need upgrading. Older homes near downtown may have outdated wiring that needs modernization.",
        "faqs": [
            ("Do you handle Covina's permit process?", "Yes — we manage all permits with the City of Covina Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in Covina?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you service Covina's historic downtown?", "Yes — we've worked on electrical systems in Covina's historic downtown area, handling upgrades that meet current code while respecting the area's character."),
        ]
    },
    "culver-city": {
        "housing": "Culver City features a mix of 1920s-1940s bungalows, 1960s apartments, and newer developments. The city has a revitalizing downtown and growing tech presence.",
        "streets": "Washington Boulevard, Venice Boulevard, Culver Boulevard, Sepulveda Boulevard, Jefferson Boulevard",
        "landmarks": "Sony Pictures Studios, the Culver City stairs, the Wende Museum, and the revitalized downtown arts district. The city is a major film and tech hub.",
        "electrical": "Older homes often have 100A panels that need upgrading. New developments and tech offices require modern electrical infrastructure. EV charger installations are common.",
        "faqs": [
            ("Do you handle Culver City's commercial electrical?", "Yes — we provide commercial electrical services to Culver City businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Culver City electrical work?", "Electrical work in Culver City requires permits from the City of Culver City. We handle all permit applications and inspections."),
            ("Do you service Culver City's tech offices?", "Yes — we've worked with tech companies in Culver City on office electrical, EV charging infrastructure, and server room power."),
        ]
    },
    "del-rey": {
        "housing": "Del Rey features 1950s-1970s ranch homes, some newer developments, and apartment buildings. The neighborhood is near the Marina del Rey area.",
        "streets": "Centinela Avenue, Alla Road, Maxella Avenue, Culver Boulevard, Morrison Street",
        "landmarks": "Nearby Marina del Rey, the Ballona Wetlands, and the Westchester Golf Course. The neighborhood has a mix of residential and commercial areas.",
        "electrical": "Many Del Rey homes have 100A panels that need upgrading. Proximity to the coast may require corrosion-resistant electrical components.",
        "faqs": [
            ("Do you service Del Rey homes?", "Yes — we provide full electrical services to Del Rey residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical issues are common in Del Rey?", "Common issues include outdated panels, salt air corrosion on outdoor electrical, and insufficient capacity for modern appliances and EV chargers."),
            ("Do you handle Del Rey's apartment buildings?", "Yes — we provide electrical services to Del Rey apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
        ]
    },
    "downey": {
        "housing": "Downey features 1950s-1970s tract homes, some newer developments, and historic properties. The city has a strong working-class community with improving property values.",
        "streets": "Firestone Boulevard, Lakewood Boulevard, Downey Avenue, Florence Avenue, Stewart and Gray Road",
        "landmarks": "The Downey Theatre, the Columbia Memorial Space Center, and the historic Rancho Los Amigos area. The city has a revitalizing downtown.",
        "electrical": "Many Downey homes have 100A panels that need upgrading. Older homes may have aluminum wiring or outdated electrical systems.",
        "faqs": [
            ("Do you handle Downey's permit process?", "Yes — we manage all permits with the City of Downey Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in Downey?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you service Downey's historic areas?", "Yes — we've worked on electrical systems in Downey's historic areas, handling upgrades that meet current code while respecting the area's character."),
        ]
    },
    "downtown-la": {
        "housing": "Downtown LA features historic lofts, new high-rise condos, and older apartment buildings. The area has experienced a massive residential revival.",
        "streets": "Spring Street, Main Street, Broadway, 7th Street, Figueroa Street",
        "landmarks": "The Broad Museum, Walt Disney Concert Hall, Grand Central Market, and the Historic Broadway Theater District. DTLA is the cultural and business center of LA.",
        "electrical": "Historic loft buildings often have unique electrical challenges. New high-rises require commercial-grade systems. EV charger installations are growing rapidly.",
        "faqs": [
            ("Do you handle downtown LA's loft conversions?", "Yes — we've upgraded electrical systems in many downtown LA loft buildings, handling panel upgrades, rewiring, and modern electrical infrastructure in historic structures."),
            ("What permits are needed for DTLA electrical work?", "Electrical work in downtown LA requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service DTLA's high-rise buildings?", "Yes — we provide electrical services to downtown LA high-rises, including individual unit upgrades, common area electrical, and EV charger installations."),
        ]
    },
    "eagle-rock": {
        "housing": "Eagle Rock features 1920s-1940s bungalows, some Craftsman homes, and newer developments. The neighborhood has a strong arts community and eclectic character.",
        "streets": "Colorado Boulevard, Eagle Rock Boulevard, Townsend Avenue, Altadena Avenue, Hill Drive",
        "landmarks": "Occidental College, the Eagle Rock Plaza, and the neighborhood's vibrant commercial district along Colorado Boulevard. The area has a creative, community-oriented feel.",
        "electrical": "Many Eagle Rock homes have older electrical systems that need modernization. Panel upgrades are common for EV charger installations.",
        "faqs": [
            ("Do you work on Eagle Rock's older homes?", "Yes — we've upgraded electrical systems in many Eagle Rock bungalows and Craftsman homes. We handle knob-and-tube replacement, panel upgrades, and rewiring."),
            ("What permits are needed for Eagle Rock electrical work?", "Electrical work in Eagle Rock requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to a 1920s bungalow?", "Absolutely — we install EV chargers in Eagle Rock's older homes regularly. Most projects include a panel upgrade to 200A and careful routing to minimize visual impact."),
        ]
    },
    "east-hollywood": {
        "housing": "East Hollywood has a mix of 1920s-1940s apartment buildings, some newer developments, and commercial properties. The neighborhood is diverse and rapidly changing.",
        "streets": "Hollywood Boulevard, Vermont Avenue, Sunset Boulevard, Santa Monica Boulevard, Western Avenue",
        "landmarks": "Korean Town (K-Town), the Barnsdall Art Park, and the historic Hollywood Palladium. The neighborhood is one of LA's most diverse areas.",
        "electrical": "Older apartment buildings often have outdated electrical systems. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle East Hollywood's apartment buildings?", "Yes — we provide electrical services to East Hollywood's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for East Hollywood electrical work?", "Electrical work in East Hollywood requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties in East Hollywood?", "Yes — we provide commercial electrical services to East Hollywood businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "echo-park": {
        "housing": "Echo Park features 1920s-1940s bungalows, hillside homes, and some newer developments. The neighborhood has a vibrant arts scene and diverse community.",
        "streets": "Sunset Boulevard, Echo Park Avenue, Glendale Boulevard, Laveta Terrace, Effie Street",
        "landmarks": "Echo Park Lake, the Echo Park time travel Mart, and the neighborhood's trendy commercial district. The area has a creative, community-oriented feel.",
        "electrical": "Many Echo Park homes have older electrical systems that need modernization. Hillside properties may have unique electrical challenges.",
        "faqs": [
            ("Do you work on Echo Park's hillside homes?", "Yes — we've upgraded electrical systems in many Echo Park hillside homes, handling unique challenges with panel placement, conduit routing, and ground-fault protection."),
            ("What permits are needed for Echo Park electrical work?", "Electrical work in Echo Park requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to an Echo Park bungalow?", "Absolutely — we install EV chargers in Echo Park's older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "edith-norman": {
        "housing": "Edith Norman is a small residential area with 1940s-1960s homes. The neighborhood has a quiet, suburban character within the city.",
        "streets": "Edith Avenue, Norman Avenue, and surrounding residential streets",
        "landmarks": "The neighborhood is near larger commercial areas and has easy access to major freeways.",
        "electrical": "Most homes have 100A panels that need upgrading for modern electrical demands. EV charger installations are becoming more common.",
        "faqs": [
            ("Do you service Edith Norman homes?", "Yes — we provide full electrical services to Edith Norman residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What's the typical panel upgrade cost in Edith Norman?", "Panel upgrades in Edith Norman typically range from $2,500 to $4,000 depending on existing conditions. Free estimates for all projects."),
            ("Can you add EV charging to an older home?", "Absolutely — we install EV chargers in Edith Norman's older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "el-monte": {
        "housing": "El Monte has a mix of 1950s-1970s tract homes, some newer developments, and industrial areas. The city has a diverse, working-class community.",
        "streets": "Valley Boulevard, Ramona Boulevard, Peck Road, Santa Anita Avenue, Floral Avenue",
        "landmarks": "The El Monte Community Center, the nearby San Gabriel Mountains, and the historic El Monte bus station. The city has a mix of residential and commercial areas.",
        "electrical": "Many El Monte homes have 100A panels that need upgrading. Industrial areas may have commercial electrical needs.",
        "faqs": [
            ("Do you handle El Monte's permit process?", "Yes — we manage all permits with the City of El Monte Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in El Monte?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you service commercial properties in El Monte?", "Yes — we provide commercial electrical services to El Monte businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "el-segundo": {
        "housing": "El Segundo features a mix of older homes, newer developments, and industrial areas near LAX. The city has a strong aerospace and tech presence.",
        "streets": "Sepulveda Boulevard, El Segundo Boulevard, Douglas Street, Grand Avenue, Aviation Boulevard",
        "landmarks": "LAX airport, the El Segundo Blue Butterfly Preserve, and the nearby Manhattan Beach area. The city has a mix of residential, commercial, and industrial areas.",
        "electrical": "Many El Segundo homes have 100A panels that need upgrading. Industrial areas may have commercial electrical needs. EV charger installations are growing.",
        "faqs": [
            ("Do you handle El Segundo's commercial electrical?", "Yes — we provide commercial electrical services to El Segundo businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for El Segundo electrical work?", "Electrical work in El Segundo requires permits from the City of El Segundo. We handle all permit applications and inspections."),
            ("Do you service El Segundo's industrial areas?", "Yes — we provide commercial electrical services to El Segundo's industrial and business areas, including warehouse electrical, EV fleet charging, and lighting retrofits."),
        ]
    },
    "el-sobrante": {
        "housing": "El Sobrante features a mix of 1950s-1970s homes and newer developments. The area has a semi-rural character in parts.",
        "streets": "Reservoir Street, El Sobrante Road, and surrounding residential streets",
        "landmarks": "The area is near the San Gabriel Mountains and has a mix of residential and commercial areas.",
        "electrical": "Many El Sobrante homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service El Sobrante homes?", "Yes — we provide full electrical services to El Sobrante residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical issues are common in El Sobrante?", "Common issues include outdated panels, insufficient capacity for modern appliances and EV chargers, and wiring that needs updating."),
            ("Do you handle El Sobrante's permit process?", "Yes — we manage all permits for El Sobrante projects. Permit costs are included in our estimates."),
        ]
    },
    "encino": {
        "housing": "Encino features 1950s-1970s ranch homes, luxury estates, and some newer construction. The neighborhood has a suburban feel within the city.",
        "streets": "Ventura Boulevard, Encino Avenue, Louise Avenue, Balboa Boulevard, Hayvenhurst Avenue",
        "landmarks": "The Encino Reservoir, the Encino Country Club, and the vibrant Ventura Boulevard commercial corridor. The neighborhood is known for its excellent schools.",
        "electrical": "Many Encino homes have 100A panels that need upgrading for modern electrical demands, especially EV charger installations and air conditioning upgrades.",
        "faqs": [
            ("Do you handle Encino's panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Encino homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical upgrades are common in Encino?", "Common upgrades include 200A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring."),
            ("Do you service Encino's luxury homes?", "Yes — we work on Encino's luxury estates, handling commercial-grade panels, whole-house generators, EV fleet charging, and sophisticated electrical systems."),
        ]
    },
    "exposition-park": {
        "housing": "Exposition Park features a mix of 1920s-1940s apartment buildings and newer developments. The area is near major cultural institutions.",
        "streets": "Exposition Boulevard, Figueroa Street, Vermont Avenue, Martin Luther King Jr. Boulevard",
        "landmarks": "The LA Memorial Coliseum, the Natural History Museum, the California Science Center, and USC. The area is a major cultural and educational hub.",
        "electrical": "Older apartment buildings often have outdated electrical systems. New developments require modern electrical infrastructure. EV charger installations are growing.",
        "faqs": [
            ("Do you handle Exposition Park's apartment buildings?", "Yes — we provide electrical services to Exposition Park's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Exposition Park electrical work?", "Electrical work in Exposition Park requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties near USC?", "Yes — we provide commercial electrical services to businesses near USC, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "fairfax-district": {
        "housing": "The Fairfax District features 1920s-1940s apartment buildings, some newer developments, and commercial properties. The area has a diverse, vibrant character.",
        "streets": "Fairfax Avenue, Beverly Boulevard, Third Street, Melrose Avenue, Olympic Boulevard",
        "landmarks": "The Original Farmers Market, The Grove, the Jewish Museum of Los Angeles, and the vibrant Fairfax Avenue commercial corridor. The area is known for its diverse food scene.",
        "electrical": "Older apartment buildings often have outdated electrical systems. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle Fairfax District electrical work?", "Yes — we provide electrical services to Fairfax District residents and businesses, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What permits are needed for Fairfax District electrical work?", "Electrical work in the Fairfax District requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties in the Fairfax District?", "Yes — we provide commercial electrical services to Fairfax District businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "figueroa-corridor": {
        "housing": "The Figueroa Corridor features a mix of older apartment buildings and newer developments. The area is near major cultural institutions and USC.",
        "streets": "Figueroa Street, Jefferson Boulevard, Flower Street, Grand Avenue",
        "landmarks": "Near USC, the LA Memorial Coliseum, and the Museum of Contemporary Art. The corridor is a major transportation and cultural hub.",
        "electrical": "Older buildings often have outdated electrical systems. New developments require modern electrical infrastructure. EV charger installations are growing.",
        "faqs": [
            ("Do you handle Figueroa Corridor electrical work?", "Yes — we provide electrical services to Figueroa Corridor residents and businesses, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What permits are needed for Figueroa Corridor electrical work?", "Electrical work in the Figueroa Corridor requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties along Figueroa?", "Yes — we provide commercial electrical services to businesses along the Figueroa Corridor, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "florence": {
        "housing": "Florence features 1920s-1960s homes, some newer developments, and commercial properties. The neighborhood has a diverse, working-class community.",
        "streets": "Florence Avenue, Graham Avenue, Main Street, Gage Avenue, Hooper Avenue",
        "landmarks": "The neighborhood is near the Florence-Firestone area and has a mix of residential and commercial areas.",
        "electrical": "Many Florence homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you service Florence homes?", "Yes — we provide full electrical services to Florence residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Florence?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Florence's permit process?", "Yes — we manage all permits for Florence projects. Permit costs are included in our estimates."),
        ]
    },
    "fox-hills": {
        "housing": "Fox Hills features 1960s-1970s condos and apartments, some newer developments, and commercial properties. The neighborhood is near Culver City and Marina del Rey.",
        "streets": "Overland Avenue, Fox Hills Drive, Rosecrans Avenue, Holder Street",
        "landmarks": "The Fox Hills Mall area, nearby Marina del Rey, and easy access to the Westside. The neighborhood has a suburban character within the city.",
        "electrical": "Many Fox Hills condos have 100A panels that need upgrading. Apartment buildings may need commercial-grade electrical systems.",
        "faqs": [
            ("Do you handle Fox Hills condo electrical?", "Yes — we provide electrical services to Fox Hills condos and apartments, including individual unit upgrades, common area electrical, and EV charger installations."),
            ("What permits are needed for Fox Hills electrical work?", "Electrical work in Fox Hills requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV chargers to Fox Hills apartments?", "Yes — we install EV chargers in Fox Hills apartment buildings, working with property management on infrastructure requirements."),
        ]
    },
    "gardena": {
        "housing": "Gardena has a mix of 1950s-1970s tract homes, some newer developments, and commercial areas. The city has a diverse population with a strong Japanese-American community.",
        "streets": "Artesia Boulevard, Western Avenue, Vermont Avenue, Gardena Boulevard, Rosecrans Avenue",
        "landmarks": "The Gardena Valley Japanese Cultural Institute, the nearby Dominguez Hills area, and a revitalizing commercial district.",
        "electrical": "Many Gardena homes have 100A panels that need upgrading. Older homes may have aluminum wiring from the 1960s-70s.",
        "faqs": [
            ("Do you handle Gardena's permit process?", "Yes — we manage all permits with the City of Gardena Building Department. Permit costs are included in our estimates."),
            ("What electrical issues are common in Gardena?", "Common issues include outdated panels, aluminum wiring from the 1960s-70s, and insufficient capacity for modern appliances and EV chargers."),
            ("Do you service Gardena's commercial properties?", "Yes — we provide commercial electrical services to Gardena businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "glassell-park": {
        "housing": "Glassell Park features 1920s-1940s bungalows, hillside homes, and some newer developments. The neighborhood has a diverse, creative community.",
        "streets": "Glendale Boulevard, Eagle Rock Boulevard, Fitzgerald Street, Toland Way",
        "landmarks": "The neighborhood sits near the LA River and has a mix of residential and commercial areas. Local parks provide green space.",
        "electrical": "Many Glassell Park homes have older electrical systems that need modernization. Hillside properties may have unique electrical challenges.",
        "faqs": [
            ("Do you work on Glassell Park's hillside homes?", "Yes — we've upgraded electrical systems in many Glassell Park hillside homes, handling unique challenges with panel placement and conduit routing."),
            ("What permits are needed for Glassell Park electrical work?", "Electrical work in Glassell Park requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to an older bungalow?", "Absolutely — we install EV chargers in Glassell Park's older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "glendale": {
        "housing": "Glendale features a mix of 1920s-1940s homes, 1960s-1970s apartments, and newer developments. The city has a large Armenian-American community and a vibrant commercial district.",
        "streets": "Brand Boulevard, Central Avenue, Glendale Avenue, Mountain Street, Glenoaks Boulevard",
        "landmarks": "The Glendale Galleria, the Americana at Brand, the Glendale YMCA, and the nearby Verdugo Mountains. The city has a revitalized downtown.",
        "electrical": "Many Glendale homes have 100A panels that need upgrading. Older homes near the downtown area may have outdated wiring that needs modernization.",
        "faqs": [
            ("Do you handle Glendale's permit process?", "Yes — we manage all permits with the City of Glendale Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in Glendale?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you service Glendale's commercial properties?", "Yes — we provide commercial electrical services to Glendale businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "granada-hills": {
        "housing": "Granada Hills features 1950s-1970s ranch homes, some newer developments, and equestrian properties. The neighborhood has a suburban character in the north Valley.",
        "streets": "Zelzah Avenue, Chatsworth Street, Polk Street, Nexton Avenue, Rinaldi Street",
        "landmarks": "The nearby Santa Susana Mountains, the Granada Hills Recreation Center, and the neighborhood's quiet residential streets.",
        "electrical": "Many Granada Hills homes have 100A panels that need upgrading. Equestrian properties may have unique electrical needs.",
        "faqs": [
            ("Do you handle Granada Hills' equestrian properties?", "Yes — we provide electrical services to Granada Hills' equestrian properties, including barn wiring, outdoor lighting, and panel upgrades."),
            ("What electrical upgrades are common in Granada Hills?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you serve Granada Hills' newer developments?", "Yes — we work on both existing homes and new construction in Granada Hills, including rough-in wiring, panel placement, and EV-ready circuits."),
        ]
    },
    "hancock-park": {
        "housing": "Hancock Park features 1920s-1940s Mediterranean and Tudor-style homes. The neighborhood is one of LA's most historic and architecturally significant areas.",
        "streets": "Larchmont Boulevard, Hancock Park Drive, Irving Boulevard, Rossmore Avenue",
        "landmarks": "The Wilshire Country Club, the Los Angeles Chapter of the American Institute of Architects, and the neighborhood's tree-lined streets with historic homes.",
        "electrical": "Many Hancock Park homes have original electrical systems that need careful modernization. Panel upgrades must respect the home's historic character.",
        "faqs": [
            ("Do you work on Hancock Park's historic homes?", "Yes — we've upgraded electrical systems in many Hancock Park homes, handling panel upgrades and rewiring while preserving the home's historic character."),
            ("What electrical challenges do Hancock Park homes face?", "Common challenges include original wiring that needs updating, small panels that can't handle modern loads, and maintaining the home's aesthetic during electrical upgrades."),
            ("Do you handle Hancock Park's historic district requirements?", "Yes — we understand Hancock Park's historic district requirements and ensure all electrical work meets current code while respecting the home's character."),
        ]
    },
    "hawthorne": {
        "housing": "Hawthorne features 1950s-1970s tract homes, some newer developments, and commercial areas near LAX and the tech industry.",
        "streets": "Hawthorne Boulevard, El Segundo Boulevard, Inglewood Avenue, Rosecrans Avenue, 120th Street",
        "landmarks": "The nearby SpaceX headquarters, the Hawthorne Municipal Airport, and easy access to LAX. The city has a mix of residential and industrial areas.",
        "electrical": "Many Hawthorne homes have 100A panels that need upgrading. Industrial areas may have commercial electrical needs.",
        "faqs": [
            ("Do you handle Hawthorne's commercial electrical?", "Yes — we provide commercial electrical services to Hawthorne businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Hawthorne electrical work?", "Electrical work in Hawthorne requires permits from the City of Hawthorne. We handle all permit applications and inspections."),
            ("Do you service Hawthorne's industrial areas?", "Yes — we provide commercial electrical services to Hawthorne's industrial areas, including warehouse electrical, EV fleet charging, and lighting retrofits."),
        ]
    },
    "health-campadre": {
        "housing": "Health Campadre is a small residential area with 1940s-1960s homes. The neighborhood has a quiet, suburban character.",
        "streets": "Local residential streets",
        "landmarks": "The neighborhood is near larger commercial areas and has easy access to major freeways.",
        "electrical": "Most homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service Health Campadre homes?", "Yes — we provide full electrical services to Health Campadre residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What's the typical panel upgrade cost?", "Panel upgrades typically range from $2,500 to $4,000 depending on existing conditions. Free estimates for all projects."),
            ("Can you add EV charging to an older home?", "Absolutely — we install EV chargers in older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "highland-park": {
        "housing": "Highland Park features 1920s-1940s Craftsman bungalows, some newer developments, and a revitalizing commercial district.",
        "streets": "Figueras Street, Avenue 56, York Boulevard, Figueroa Street, North Avenue 59",
        "landmarks": "The Highland Park area has a vibrant arts scene, local breweries, and the nearby Arroyo Seco. The neighborhood has a creative, community-oriented feel.",
        "electrical": "Many Highland Park homes have older electrical systems that need modernization. Panel upgrades are common for EV charger installations.",
        "faqs": [
            ("Do you work on Highland Park's older homes?", "Yes — we've upgraded electrical systems in many Highland Park Craftsman bungalows. We handle knob-and-tube replacement, panel upgrades, and rewiring."),
            ("What permits are needed for Highland Park electrical work?", "Electrical work in Highland Park requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to a 1920s Craftsman?", "Absolutely — we install EV chargers in Highland Park's older homes regularly. Most projects include a panel upgrade to 200A and careful routing to minimize visual impact."),
        ]
    },
    "hollywood": {
        "housing": "Hollywood features a mix of 1920s-1940s apartment buildings, historic homes, and newer developments. The area is one of the most recognizable neighborhoods in the world.",
        "streets": "Hollywood Boulevard, Sunset Boulevard, Vine Street, La Brea Avenue, Highland Avenue",
        "landmarks": "The Hollywood Sign, the Walk of Fame, the TCL Chinese Theatre, and the Hollywood Bowl. The area is a major tourist and entertainment hub.",
        "electrical": "Older apartment buildings often have outdated electrical systems. New developments require modern electrical infrastructure. EV charger installations are growing rapidly.",
        "faqs": [
            ("Do you handle Hollywood's apartment buildings?", "Yes — we provide electrical services to Hollywood's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Hollywood electrical work?", "Electrical work in Hollywood requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service Hollywood's commercial properties?", "Yes — we provide commercial electrical services to Hollywood businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "holmby-hills": {
        "housing": "Holmby Hills features luxury estates ranging from 1920s Mediterranean villas to modern mansions. The neighborhood is one of LA's most exclusive areas.",
        "streets": "Holmby Avenue, Sunset Boulevard, Bellagio Road, Maybourne Drive",
        "landmarks": "The Playboy Mansion (formerly), the Holmby Park, and proximity to UCLA. The neighborhood is known for its ultra-luxury properties.",
        "electrical": "Estate properties often require commercial-grade electrical systems, whole-house generators, and sophisticated lighting control. Many homes have 400A service.",
        "faqs": [
            ("Do you handle estate-scale electrical in Holmby Hills?", "Yes — we service Holmby Hills' luxury estates with commercial-grade panels, whole-house generators, EV fleet charging, and smart home electrical systems."),
            ("What electrical upgrades are common in Holmby Hills?", "Common upgrades include 400A service, generator transfer switches, landscape lighting, pool electrical, EV charging stations, and smart home wiring."),
            ("Do you coordinate with Holmby Hills' architectural requirements?", "Yes — we work with Holmby Hills' architectural review requirements and ensure all exterior electrical work meets the community's standards."),
        ]
    },
    "inglewood": {
        "housing": "Inglewood features 1940s-1970s homes, some newer developments, and commercial areas. The city has a revitalizing downtown and major entertainment venues.",
        "streets": "Florence Avenue, Inglewood Avenue, Prairie Avenue, Centinela Avenue, Manchester Boulevard",
        "landmarks": "SoFi Stadium, the YouTube Theater, the Kia Forum, and the nearby LA Rams and Chargers facilities. The city is experiencing rapid development.",
        "electrical": "Many Inglewood homes have 100A panels that need upgrading. Major developments require modern electrical infrastructure.",
        "faqs": [
            ("Do you handle Inglewood's commercial electrical?", "Yes — we provide commercial electrical services to Inglewood businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Inglewood electrical work?", "Electrical work in Inglewood requires permits from the City of Inglewood. We handle all permit applications and inspections."),
            ("Do you service properties near SoFi Stadium?", "Yes — we provide electrical services to properties near SoFi Stadium and the surrounding entertainment district."),
        ]
    },
    "jefferson-park": {
        "housing": "Jefferson Park features 1920s-1940s homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Jefferson Boulevard, Van Buren Place, Farmdale Avenue, Denker Avenue",
        "landmarks": "The neighborhood is near USC and the Figueroa Corridor. Local parks provide green space.",
        "electrical": "Many Jefferson Park homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you service Jefferson Park homes?", "Yes — we provide full electrical services to Jefferson Park residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Jefferson Park?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Jefferson Park's permit process?", "Yes — we manage all permits for Jefferson Park projects. Permit costs are included in our estimates."),
        ]
    },
    "koreatown": {
        "housing": "Koreatown features dense apartment buildings, 1920s-1940s homes, and newer developments. The neighborhood is one of LA's most vibrant and densely populated areas.",
        "streets": "Western Avenue, Olympic Boulevard, Vermont Avenue, Wilshire Boulevard, Sixth Street",
        "landmarks": "The Korea Town area, the nearby Wilshire Grand Center, and the neighborhood's 24-hour commercial activity. The area is known for its excellent Korean cuisine.",
        "electrical": "Dense apartment buildings often have complex electrical needs. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle Koreatown's apartment buildings?", "Yes — we provide electrical services to Koreatown's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Koreatown electrical work?", "Electrical work in Koreatown requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service Koreatown's commercial properties?", "Yes — we provide commercial electrical services to Koreatown businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "la-crescenta": {
        "housing": "La Crescenta features 1950s-1970s homes, some newer developments, and a suburban character near the mountains.",
        "streets": "Foothill Boulevard, La Crescenta Avenue, Montrose Avenue, Honolulu Avenue",
        "landmarks": "The nearby Angeles National Forest, the La Crescenta Library, and the community's quiet residential streets.",
        "electrical": "Many La Crescenta homes have 100A panels that need upgrading. Proximity to the mountains may require special electrical considerations.",
        "faqs": [
            ("Do you service La Crescenta homes?", "Yes — we provide full electrical services to La Crescenta residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in La Crescenta?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle La Crescenta's permit process?", "Yes — we manage all permits for La Crescenta projects. Permit costs are included in our estimates."),
        ]
    },
    "lake-view-terrace": {
        "housing": "Lake View Terrace features 1950s-1970s homes, some newer developments, and equestrian properties.",
        "streets": "Foothill Boulevard, Osborne Street, Paxton Street, Tuxford Street",
        "landmarks": "The nearby Hansen Dam area, the Lake View Terrace Recreation Center, and the neighborhood's equestrian character.",
        "electrical": "Many Lake View Terrace homes have 100A panels that need upgrading. Equestrian properties may have unique electrical needs.",
        "faqs": [
            ("Do you handle Lake View Terrace's equestrian properties?", "Yes — we provide electrical services to Lake View Terrace's equestrian properties, including barn wiring, outdoor lighting, and panel upgrades."),
            ("What electrical upgrades are common in Lake View Terrace?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you serve Lake View Terrace's newer developments?", "Yes — we work on both existing homes and new construction in Lake View Terrace."),
        ]
    },
    "larchmont": {
        "housing": "Larchmont features 1920s-1940s homes, some newer developments, and a walkable commercial district.",
        "streets": "Larchmont Boulevard, Beverly Boulevard, Third Street, Franklin Avenue",
        "landmarks": "The Larchmont Village shopping district, the nearby Hancock Park neighborhood, and the area's tree-lined streets.",
        "electrical": "Many Larchmont homes have older electrical systems that need modernization. Panel upgrades are common for EV charger installations.",
        "faqs": [
            ("Do you work on Larchmont's older homes?", "Yes — we've upgraded electrical systems in many Larchmont homes. We handle panel upgrades, rewiring, and EV charger installations."),
            ("What permits are needed for Larchmont electrical work?", "Electrical work in Larchmont requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to a Larchmont home?", "Absolutely — we install EV chargers in Larchmont's older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "little-armenia": {
        "housing": "Little Armenia features 1920s-1940s apartment buildings, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Western Avenue, Hollywood Boulevard, Vermont Avenue, Santa Monica Boulevard",
        "landmarks": "The neighborhood is near East Hollywood and has a diverse, vibrant character. Local shops and restaurants serve the Armenian-American community.",
        "electrical": "Older apartment buildings often have outdated electrical systems. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle Little Armenia's apartment buildings?", "Yes — we provide electrical services to Little Armenia's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Little Armenia electrical work?", "Electrical work in Little Armenia requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties in Little Armenia?", "Yes — we provide commercial electrical services to Little Armenia businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "long-beach": {
        "housing": "Long Beach features a diverse mix of 1920s-1940s homes, 1960s-1970s apartments, and newer developments. The city has one of the most varied housing stocks in the region.",
        "streets": "Long Beach Boulevard, Atlantic Avenue, Pacific Coast Highway, Anaheim Street, Ocean Boulevard",
        "landmarks": "The Aquarium of the Pacific, the RMS Queen Mary (formerly), the Long Beach Convention Center, and the nearby Port of Long Beach.",
        "electrical": "Many Long Beach homes have 100A panels that need upgrading. Coastal areas may require corrosion-resistant electrical components. EV charger installations are growing.",
        "faqs": [
            ("Do you handle Long Beach's commercial electrical?", "Yes — we provide commercial electrical services to Long Beach businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Long Beach electrical work?", "Electrical work in Long Beach requires permits from the City of Long Beach. We handle all permit applications and inspections."),
            ("Do you service Long Beach's coastal properties?", "Yes — we provide electrical services to Long Beach's coastal properties, including salt-air corrosion protection and weather-resistant electrical components."),
        ]
    },
    "los-angeles": {
        "housing": "Los Angeles has one of the most diverse housing stocks in the country, from 1920s bungalows to modern high-rises. The city encompasses dozens of distinct neighborhoods.",
        "streets": "Sunset Boulevard, Hollywood Boulevard, Wilshire Boulevard, Santa Monica Boulevard, Figueroa Street",
        "landmarks": "The Hollywood Sign, the Staples Center (now Crypto.com Arena), Griffith Observatory, and the Getty Center. LA is the cultural and entertainment capital of the West Coast.",
        "electrical": "Electrical needs vary widely across LA's neighborhoods. From historic home rewiring to modern high-rise electrical systems, the city presents every type of electrical project.",
        "faqs": [
            ("Do you service all of Los Angeles?", "Yes — AMY Electric serves all neighborhoods within the City of Los Angeles. From Downtown LA to the Westside, Valley to South LA, we provide comprehensive electrical services."),
            ("What permits are needed for LA electrical work?", "Permits are required for most electrical work in Los Angeles. We handle all permit applications, plan reviews, and inspections with the LA Department of Building and Safety."),
            ("Do you handle both residential and commercial in LA?", "Yes — we provide both residential and commercial electrical services throughout Los Angeles, including panel upgrades, EV charger installation, rewiring, and lighting."),
        ]
    },
    "los-feliz": {
        "housing": "Los Feliz features 1920s-1940s bungalows, historic homes, and some newer developments. The neighborhood has a creative, community-oriented feel.",
        "streets": "Hillhurst Avenue, Vermont Avenue, Franklin Avenue, Los Feliz Boulevard, Hyperion Avenue",
        "landmarks": "Griffith Observatory, the Greek Theatre, the Los Feliz Village shopping district, and the nearby Griffith Park. The area is known for its independent shops and restaurants.",
        "electrical": "Many Los Feliz homes have older electrical systems that need modernization. Panel upgrades are common for EV charger installations.",
        "faqs": [
            ("Do you work on Los Feliz's older homes?", "Yes — we've upgraded electrical systems in many Los Feliz bungalows and historic homes. We handle panel upgrades, rewiring, and EV charger installations."),
            ("What permits are needed for Los Feliz electrical work?", "Electrical work in Los Feliz requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to a Los Feliz bungalow?", "Absolutely — we install EV chargers in Los Feliz's older homes regularly. Most projects include a panel upgrade to 200A and careful routing to minimize visual impact."),
        ]
    },
    "malibu": {
        "housing": "Malibu features luxury beachfront estates, canyon homes, and some newer developments. Properties range from modest beach cottages to multi-million dollar compounds.",
        "streets": "Pacific Coast Highway, Malibu Road, Carbon Beach, Zuma Beach, Point Dume",
        "landmarks": "The Malibu Pier, the Getty Villa, Zuma Beach, and the Santa Monica Mountains. The city is known for its stunning coastline and celebrity residents.",
        "electrical": "Beachfront properties require salt-air resistant electrical components. Canyon homes may need longer conduit runs. Many estates have 400A service and whole-house generators.",
        "faqs": [
            ("Do you handle Malibu's beachfront properties?", "Yes — we service Malibu's beachfront estates with salt-air resistant electrical components, corrosion-resistant panels, and weather-proof outdoor electrical."),
            ("What electrical upgrades are common in Malibu?", "Common upgrades include 400A service, generator transfer switches, landscape lighting, pool electrical, EV charging stations, and smart home wiring."),
            ("Do you coordinate with Malibu's building requirements?", "Yes — we understand Malibu's building codes and coastal requirements. We handle all permits and ensure compliance with the city's standards."),
        ]
    },
    "manhattan-beach": {
        "housing": "Manhattan Beach features luxury beachfront homes, hillside properties, and some newer developments. The city has some of the highest property values in the South Bay.",
        "streets": "Manhattan Beach Boulevard, Valley Avenue, Ardmore Avenue, Sepulveda Boulevard, Pacific Coast Highway",
        "landmarks": "The Manhattan Beach Pier, the Roundhouse Aquarium, and the nearby El Segundo and Hermosa Beach areas. The city is known for its beach lifestyle.",
        "electrical": "Beachfront properties require salt-air resistant electrical components. Many homes have 200A or 400A service. EV charger installations are standard in newer construction.",
        "faqs": [
            ("Do you handle Manhattan Beach's beachfront homes?", "Yes — we service Manhattan Beach's beachfront properties with salt-air resistant electrical components, corrosion-resistant panels, and weather-proof outdoor electrical."),
            ("What electrical upgrades are common in Manhattan Beach?", "Common upgrades include 200A-400A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring."),
            ("Do you coordinate with Manhattan Beach's building requirements?", "Yes — we understand Manhattan Beach's building codes and coastal requirements. We handle all permits and ensure compliance."),
        ]
    },
    "mar-vista": {
        "housing": "Mar Vista features 1940s-1960s homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Venice Boulevard, Sepulveda Boulevard, Grand View Avenue, Meier Street",
        "landmarks": "The Mar Vista Farmers Market, the nearby Venice Beach area, and the neighborhood's growing food scene.",
        "electrical": "Many Mar Vista homes have 100A panels that need upgrading. Proximity to the coast may require corrosion-resistant electrical components.",
        "faqs": [
            ("Do you service Mar Vista homes?", "Yes — we provide full electrical services to Mar Vista residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Mar Vista?", "Common upgrades include 200A panel upgrades, EV charger installation, salt-air corrosion protection, and rewiring for older homes."),
            ("Do you handle Mar Vista's permit process?", "Yes — we manage all permits for Mar Vista projects. Permit costs are included in our estimates."),
        ]
    },
    "mid-city": {
        "housing": "Mid-City features 1920s-1940s homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Pico Boulevard, Olympic Boulevard, Fairfax Avenue, La Brea Avenue, Crenshaw Boulevard",
        "landmarks": "The nearby La Brea Tar Pits, the Miracle Mile area, and the Mid-Wilshire cultural corridor.",
        "electrical": "Many Mid-City homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you service Mid-City homes?", "Yes — we provide full electrical services to Mid-City residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Mid-City?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Mid-City's permit process?", "Yes — we manage all permits for Mid-City projects. Permit costs are included in our estimates."),
        ]
    },
    "miracle-mile": {
        "housing": "Miracle Mile features 1920s-1940s apartments and homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Wilshire Boulevard, Fairfax Avenue, La Brea Avenue, Ogden Drive",
        "landmarks": "The La Brea Tar Pits, the Petersen Automotive Museum, the Los Angeles County Museum of Art (LACMA), and the nearby Miracle Mile shopping district.",
        "electrical": "Many Miracle Mile homes have older electrical systems that need modernization. Commercial areas may have unique electrical needs.",
        "faqs": [
            ("Do you service Miracle Mile homes?", "Yes — we provide full electrical services to Miracle Mile residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Miracle Mile?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Miracle Mile's commercial electrical?", "Yes — we provide commercial electrical services to Miracle Mile businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "monrovia": {
        "housing": "Monrovia features 1920s-1940s Craftsman homes, 1960s-1970s tract homes, and some newer developments. The city has a charming downtown and strong community feel.",
        "streets": "Myrtle Avenue, Colorado Boulevard, Foothill Boulevard, Heliotrope Avenue, Shamrock Avenue",
        "landmarks": "Historic downtown Monrovia, the Monrovia Historic Library, and the nearby San Gabriel Mountains. The city has a revitalizing downtown district.",
        "electrical": "Many Monrovia homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you handle Monrovia's permit process?", "Yes — we manage all permits with the City of Monrovia Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in Monrovia?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you service Monrovia's historic homes?", "Yes — we've worked on electrical systems in Monrovia's historic homes, handling upgrades that meet current code while respecting the home's character."),
        ]
    },
    "montecito-heights": {
        "housing": "Montecito Heights features 1920s-1940s homes, hillside properties, and some newer developments. The neighborhood has a mix of residential character.",
        "streets": "Figueras Street, Avenue 52, Montecito Drive, Toland Way",
        "landmarks": "The nearby Arroyo Seco, the Montecito Heights Recreation Center, and the neighborhood's quiet residential streets.",
        "electrical": "Many Montecito Heights homes have older electrical systems that need modernization. Hillside properties may have unique electrical challenges.",
        "faqs": [
            ("Do you work on Montecito Heights' hillside homes?", "Yes — we've upgraded electrical systems in many Montecito Heights hillside homes, handling unique challenges with panel placement and conduit routing."),
            ("What permits are needed for Montecito Heights electrical work?", "Electrical work in Montecito Heights requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to a Montecito Heights home?", "Absolutely — we install EV chargers in Montecito Heights' older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "north-glendale": {
        "housing": "North Glendale features 1950s-1970s homes, some newer developments, and a suburban character near the mountains.",
        "streets": "Glenoaks Boulevard, Mountain Street, Holly Drive, Los Feliz Road",
        "landmarks": "The nearby Verdugo Mountains, the North Glendale area, and the neighborhood's quiet residential streets.",
        "electrical": "Many North Glendale homes have 100A panels that need upgrading. Proximity to the mountains may require special electrical considerations.",
        "faqs": [
            ("Do you service North Glendale homes?", "Yes — we provide full electrical services to North Glendale residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in North Glendale?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle North Glendale's permit process?", "Yes — we manage all permits with the City of Glendale Building Department for North Glendale projects."),
        ]
    },
    "north-hills": {
        "housing": "North Hills features 1950s-1970s tract homes, some newer developments, and a suburban character in the San Fernando Valley.",
        "streets": "Nordhoff Street, Sepulveda Boulevard, Haskell Avenue, Plummer Street",
        "landmarks": "The nearby California State University Northridge (CSUN), the North Hills area, and the neighborhood's quiet residential streets.",
        "electrical": "Many North Hills homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service North Hills homes?", "Yes — we provide full electrical services to North Hills residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in North Hills?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle North Hills' permit process?", "Yes — we manage all permits for North Hills projects. Permit costs are included in our estimates."),
        ]
    },
    "north-hollywood": {
        "housing": "North Hollywood features a mix of 1920s-1940s apartments, 1960s-1970s tract homes, and newer developments. The NoArts district has seen significant revitalization.",
        "streets": "Lankershim Boulevard, Magnolia Boulevard, Vineland Avenue, Tujunga Avenue, Chandler Boulevard",
        "landmarks": "The NoArts District, the El Portal Theatre, and the nearby Universal Studios area. The neighborhood has a vibrant arts scene and growing tech presence.",
        "electrical": "Older apartment buildings often have outdated electrical systems. New developments require modern electrical infrastructure. EV charger installations are growing.",
        "faqs": [
            ("Do you handle North Hollywood's apartment buildings?", "Yes — we provide electrical services to North Hollywood's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for North Hollywood electrical work?", "Electrical work in North Hollywood requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service the NoArts District?", "Yes — we provide commercial electrical services to NoArts District businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "northridge": {
        "housing": "Northridge features 1950s-1970s tract homes, some newer developments, and the Cal State Northridge area.",
        "streets": "Reseda Boulevard, Nordhoff Street, Tampa Avenue, Zelzah Avenue, Lindley Avenue",
        "landmarks": "Cal State Northridge (CSUN), the Northridge Fashion Center, and the nearby Santa Susana Mountains. The area has a suburban, family-oriented character.",
        "electrical": "Many Northridge homes have 100A panels that need upgrading. Earthquake retrofitting may require electrical system updates.",
        "faqs": [
            ("Do you handle Northridge's panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Northridge homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical issues are common in Northridge?", "Common issues include outdated panels, aluminum wiring from the 1960s-70s, and insufficient capacity for modern appliances and EV chargers."),
            ("Do you service Cal State Northridge area properties?", "Yes — we provide electrical services to properties near CSUN, including residential, commercial, and student housing."),
        ]
    },
    "oak-park": {
        "housing": "Oak Park features 1970s-1990s homes, some newer developments, and a suburban character near the Ventura County line.",
        "streets": "Kanan Road, Lindero Canyon Road, Brunswick Avenue, Oak Park Drive",
        "landmarks": "The nearby Santa Monica Mountains, the Oak Park area, and the neighborhood's quiet residential streets.",
        "electrical": "Many Oak Park homes have 100A or 150A panels that need upgrading for modern electrical demands, especially EV charger installations.",
        "faqs": [
            ("Do you service Oak Park homes?", "Yes — we provide full electrical services to Oak Park residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Oak Park?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle Oak Park's permit process?", "Yes — we manage all permits for Oak Park projects. Permit costs are included in our estimates."),
        ]
    },
    "pacific-palisades": {
        "housing": "Pacific Palisades features luxury homes, beachfront properties, and some newer developments. The city has a small-town feel within the larger Los Angeles area.",
        "streets": "Sunset Boulevard, Pacific Coast Highway, Palisades Drive, Via de la Paz, Antioch Street",
        "landmarks": "The Getty Villa, the Pacific Palisades Recreation Center, and the nearby Santa Monica Mountains. The city is known for its stunning natural setting.",
        "electrical": "Many Pacific Palisades homes have 200A or 400A service. Beachfront properties require salt-air resistant electrical components. EV charger installations are standard in newer construction.",
        "faqs": [
            ("Do you handle Pacific Palisades' beachfront properties?", "Yes — we service Pacific Palisades' beachfront homes with salt-air resistant electrical components, corrosion-resistant panels, and weather-proof outdoor electrical."),
            ("What electrical upgrades are common in Pacific Palisades?", "Common upgrades include 200A-400A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring."),
            ("Do you coordinate with Pacific Palisades' building requirements?", "Yes — we understand Pacific Palisades' building codes and coastal requirements. We handle all permits and ensure compliance."),
        ]
    },
    "pacoima": {
        "housing": "Pacoima features 1950s-1970s tract homes, some newer developments, and a working-class community.",
        "streets": "Van Nuys Boulevard, Sepulveda Boulevard, Foothill Boulevard, Brand Boulevard",
        "landmarks": "The nearby Hansen Dam area, the Pacoima Recreation Center, and the neighborhood's residential character.",
        "electrical": "Many Pacoima homes have 100A panels that need upgrading. Older homes may have outdated wiring that needs modernization.",
        "faqs": [
            ("Do you service Pacoima homes?", "Yes — we provide full electrical services to Pacoima residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Pacoima?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Pacoima's permit process?", "Yes — we manage all permits for Pacoima projects. Permit costs are included in our estimates."),
        ]
    },
    "palms": {
        "housing": "Palms features 1920s-1940s apartments, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Venice Boulevard, Palms Boulevard, Motor Avenue, National Boulevard",
        "landmarks": "The nearby Culver City area, the Palms neighborhood's diverse food scene, and the neighborhood's central Westside location.",
        "electrical": "Many Palms homes have older electrical systems that need modernization. Apartment buildings may need commercial-grade electrical systems.",
        "faqs": [
            ("Do you handle Palms' apartment buildings?", "Yes — we provide electrical services to Palms' apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Palms electrical work?", "Electrical work in Palms requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties in Palms?", "Yes — we provide commercial electrical services to Palms businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "pasadena": {
        "housing": "Pasadena features 1920s-1940s Craftsman homes, historic estates, and some newer developments. The city has one of the most architecturally significant housing stocks in California.",
        "streets": "Colorado Boulevard, Lake Avenue, Fair Oaks Avenue, Del Mar Boulevard, Orange Grove Boulevard",
        "landmarks": "The Rose Bowl, Caltech, the Norton Simon Museum, and the historic Pasadena City Hall. The city is known for its Tournament of Roses Parade.",
        "electrical": "Many Pasadena homes have original electrical systems that need careful modernization. Historic district requirements may affect electrical upgrades.",
        "faqs": [
            ("Do you handle Pasadena's historic homes?", "Yes — we've upgraded electrical systems in many Pasadena Craftsman and historic homes. We handle panel upgrades, rewiring, and EV charger installations while respecting the home's character."),
            ("What permits are needed for Pasadena electrical work?", "Electrical work in Pasadena requires permits from the City of Pasadena. We handle all permit applications and inspections."),
            ("Do you work within Pasadena's historic district requirements?", "Yes — we understand Pasadena's historic district requirements and ensure all electrical work meets current code while preserving the home's character."),
        ]
    },
    "pico-union": {
        "housing": "Pico Union features 1920s-1940s apartment buildings, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Pico Boulevard, Union Avenue, Hoover Street, Western Avenue",
        "landmarks": "The neighborhood is near Downtown LA and has a diverse, vibrant character. Local shops and restaurants serve the community.",
        "electrical": "Older apartment buildings often have outdated electrical systems. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle Pico Union's apartment buildings?", "Yes — we provide electrical services to Pico Union's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Pico Union electrical work?", "Electrical work in Pico Union requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service commercial properties in Pico Union?", "Yes — we provide commercial electrical services to Pico Union businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "porter-ranch": {
        "housing": "Porter Ranch features 1980s-2000s tract homes, some newer luxury developments, and a suburban character in the north Valley.",
        "streets": "Porter Ranch Drive, Tampa Avenue, Reseda Boulevard, Northridge Place",
        "landmarks": "The nearby Santa Susana Mountains, the Porter Ranch area, and the neighborhood's quiet residential streets with newer homes.",
        "electrical": "Many Porter Ranch homes already have 200A panels, but some need upgrades for EV charger installations and modern loads.",
        "faqs": [
            ("Do you service Porter Ranch homes?", "Yes — we provide full electrical services to Porter Ranch residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Porter Ranch?", "Common upgrades include 200A-400A panel upgrades, EV charger installation, landscape lighting, and smart home wiring."),
            ("Do you handle Porter Ranch's newer construction?", "Yes — we work on both existing homes and new construction in Porter Ranch, including rough-in wiring, panel placement, and EV-ready circuits."),
        ]
    },
    "rancho-park": {
        "housing": "Rancho Park features 1940s-1960s homes, some newer developments, and a quiet residential character near Century City.",
        "streets": "Pico Boulevard, Westwood Boulevard, Overland Avenue, Exposition Boulevard",
        "landmarks": "The nearby Rancho Park Golf Course, the Westside Pavilion area, and the neighborhood's tree-lined streets.",
        "electrical": "Many Rancho Park homes have 100A panels that need upgrading. Proximity to Century City may affect property values and electrical needs.",
        "faqs": [
            ("Do you service Rancho Park homes?", "Yes — we provide full electrical services to Rancho Park residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Rancho Park?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle Rancho Park's permit process?", "Yes — we manage all permits for Rancho Park projects. Permit costs are included in our estimates."),
        ]
    },
    "redondo-beach": {
        "housing": "Redondo Beach features beachfront homes, 1960s-1970s tract homes, and some newer developments. The city has a strong coastal community feel.",
        "streets": "Pacific Coast Highway, Hermosa Beach Avenue, Torrance Boulevard, Aviation Boulevard, Prospect Avenue",
        "landmarks": "The Redondo Beach Pier, the nearby Hermosa Beach area, and the King Harbor marina. The city is known for its beach lifestyle.",
        "electrical": "Beachfront properties require salt-air resistant electrical components. Many homes have 100A or 150A panels that need upgrading for modern loads.",
        "faqs": [
            ("Do you handle Redondo Beach's beachfront homes?", "Yes — we service Redondo Beach's beachfront properties with salt-air resistant electrical components, corrosion-resistant panels, and weather-proof outdoor electrical."),
            ("What electrical upgrades are common in Redondo Beach?", "Common upgrades include 200A panel upgrades, EV charger installation, landscape lighting, pool electrical, and salt-air corrosion protection."),
            ("Do you coordinate with Redondo Beach's building requirements?", "Yes — we understand Redondo Beach's building codes and coastal requirements. We handle all permits and ensure compliance."),
        ]
    },
    "reseda": {
        "housing": "Reseda features 1950s-1970s tract homes, some newer developments, and a suburban character in the San Fernando Valley.",
        "streets": "Reseda Boulevard, Sherman Way, Vanowen Street, Victory Boulevard, Keswick Street",
        "landmarks": "The nearby Sepulveda Basin, the Reseda Recreation Center, and the neighborhood's quiet residential streets.",
        "electrical": "Many Reseda homes have 100A panels that need upgrading. Older homes may have outdated wiring that needs modernization.",
        "faqs": [
            ("Do you handle Reseda's panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Reseda homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical issues are common in Reseda?", "Common issues include outdated panels, aluminum wiring from the 1960s-70s, and insufficient capacity for modern appliances and EV chargers."),
            ("Do you service Reseda's newer developments?", "Yes — we work on both existing homes and new construction in Reseda, including rough-in wiring, panel placement, and EV-ready circuits."),
        ]
    },
    "san-fernando": {
        "housing": "San Fernando features 1940s-1970s homes, some newer developments, and a working-class community.",
        "streets": "San Fernando Road, Maclay Avenue, Pico Street, Brand Boulevard",
        "landmarks": "The historic San Fernando Mission, the San Fernando Recreation Center, and the nearby Santa Susana Mountains.",
        "electrical": "Many San Fernando homes have 100A panels that need upgrading. Older homes may have outdated wiring that needs modernization.",
        "faqs": [
            ("Do you handle San Fernando's permit process?", "Yes — we manage all permits with the City of San Fernando Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in San Fernando?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you service San Fernando's historic areas?", "Yes — we've worked on electrical systems in San Fernando's historic areas, handling upgrades that meet current code while respecting the area's character."),
        ]
    },
    "santa-clarita": {
        "housing": "Santa Clarita features 1980s-2000s tract homes, some newer developments, and a suburban character in the north Valley.",
        "streets": "Valencia Boulevard, Lyons Avenue, Bouquet Canyon Road, Soledad Canyon Road",
        "landmarks": "Six Flags Magic Mountain, the nearby Angeles National Forest, and the Valencia Town Center area. The city is known for its family-oriented community.",
        "electrical": "Many Santa Clarita homes have 100A panels that need upgrading for modern electrical demands, especially EV charger installations.",
        "faqs": [
            ("Do you handle Santa Clarita's panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Santa Clarita homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical issues are common in Santa Clarita?", "Common issues include outdated panels, insufficient capacity for modern appliances and EV chargers, and wiring that needs updating."),
            ("Do you service Santa Clarita's newer developments?", "Yes — we work on both existing homes and new construction in Santa Clarita, including rough-in wiring, panel placement, and EV-ready circuits."),
        ]
    },
    "santa-monica": {
        "housing": "Santa Monica features a mix of 1920s-1940s homes, 1960s-1970s apartments, and newer developments. The city has strict building codes and environmental requirements.",
        "streets": "Santa Monica Boulevard, Montana Avenue, Wilshire Boulevard, Ocean Avenue, Main Street",
        "landmarks": "The Santa Monica Pier, the Third Street Promenade, the Annenberg Community Beach House, and the nearby Venice Beach. The city is a major Westside destination.",
        "electrical": "Many Santa Monica homes have 100A panels that need upgrading. Coastal properties require salt-air resistant electrical components. EV charger installations are growing rapidly.",
        "faqs": [
            ("Do you handle Santa Monica's commercial electrical?", "Yes — we provide commercial electrical services to Santa Monica businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Santa Monica electrical work?", "Electrical work in Santa Monica requires permits from the City of Santa Monica. We handle all permit applications and inspections."),
            ("Do you coordinate with Santa Monica's building requirements?", "Yes — we understand Santa Monica's building codes and environmental requirements. We handle all permits and ensure compliance with the city's standards."),
        ]
    },
    "sawtelle": {
        "housing": "Sawtelle features 1920s-1940s homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Sawtelle Boulevard, Olympic Boulevard, Santa Monica Boulevard, Pico Boulevard",
        "landmarks": "The Sawtelle Japantown area, the nearby West LA area, and the neighborhood's vibrant commercial district.",
        "electrical": "Many Sawtelle homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you service Sawtelle homes?", "Yes — we provide full electrical services to Sawtelle residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Sawtelle?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Sawtelle's commercial electrical?", "Yes — we provide commercial electrical services to Sawtelle businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "sawtelle-japantown": {
        "housing": "Sawtelle Japantown features 1920s-1940s homes and apartments, some newer developments, and a vibrant commercial district.",
        "streets": "Sawtelle Boulevard, Olympic Boulevard, Santa Monica Boulevard",
        "landmarks": "The Sawtelle Japantown commercial district, the nearby West LA area, and the neighborhood's diverse food scene.",
        "electrical": "Many Sawtelle Japantown homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you service Sawtelle Japantown homes?", "Yes — we provide full electrical services to Sawtelle Japantown residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Sawtelle Japantown?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Sawtelle Japantown's commercial electrical?", "Yes — we provide commercial electrical services to Sawtelle Japantown businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "shadow-hills": {
        "housing": "Shadow Hills features 1940s-1960s homes, equestrian properties, and some newer developments. The neighborhood has a rural character within the city.",
        "streets": "Sunland Boulevard, Foothill Boulevard, and surrounding residential streets",
        "landmarks": "The nearby Hansen Dam area, the Shadow Hills area, and the neighborhood's equestrian character.",
        "electrical": "Many Shadow Hills homes have 100A panels that need upgrading. Equestrian properties may have unique electrical needs.",
        "faqs": [
            ("Do you handle Shadow Hills' equestrian properties?", "Yes — we provide electrical services to Shadow Hills' equestrian properties, including barn wiring, outdoor lighting, and panel upgrades."),
            ("What electrical upgrades are common in Shadow Hills?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you serve Shadow Hills' newer developments?", "Yes — we work on both existing homes and new construction in Shadow Hills."),
        ]
    },
    "shadow-ranch-park": {
        "housing": "Shadow Ranch Park features 1950s-1970s homes and a suburban character.",
        "streets": "Local residential streets",
        "landmarks": "The Shadow Ranch Park area, the nearby recreation facilities, and the neighborhood's quiet residential streets.",
        "electrical": "Most homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service Shadow Ranch Park homes?", "Yes — we provide full electrical services to Shadow Ranch Park residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What's the typical panel upgrade cost?", "Panel upgrades typically range from $2,500 to $4,000 depending on existing conditions. Free estimates for all projects."),
            ("Can you add EV charging to an older home?", "Absolutely — we install EV chargers in older homes regularly. Most projects include a panel upgrade to 200A."),
        ]
    },
    "sherman-oaks": {
        "housing": "Sherman Oaks features 1950s-1970s homes, luxury estates, and some newer construction. The neighborhood is known for its hillside properties.",
        "streets": "Ventura Boulevard, Van Nuys Boulevard, Moorpark Street, Mulholland Drive, Coldwater Canyon Avenue",
        "landmarks": "The Sherman Oaks Galleria, the nearby Studio City area, and the neighborhood's hillside estates with stunning views.",
        "electrical": "Many Sherman Oaks homes have 100A panels that need upgrading. Hillside properties may need subpanels or longer conduit runs for EV chargers.",
        "faqs": [
            ("Do you handle Sherman Oaks' panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Sherman Oaks homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical upgrades are common in Sherman Oaks?", "Common upgrades include 200A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring."),
            ("Do you service Sherman Oaks' hillside properties?", "Yes — we handle the unique electrical needs of Sherman Oaks' hillside properties, including subpanels, longer conduit runs, and ground-fault protection."),
        ]
    },
    "silver-lake": {
        "housing": "Silver Lake features 1920s-1940s bungalows, hillside homes, and some newer developments. The neighborhood has a creative, community-oriented feel.",
        "streets": "Sunset Boulevard, Silver Lake Boulevard, Hyperion Avenue, Griffith Park Boulevard, Laveta Terrace",
        "landmarks": "Silver Lake Reservoir, the nearby Griffith Park, and the neighborhood's trendy commercial district. The area is known for its independent shops and restaurants.",
        "electrical": "Many Silver Lake homes have older electrical systems that need modernization. Hillside properties may have unique electrical challenges.",
        "faqs": [
            ("Do you work on Silver Lake's hillside homes?", "Yes — we've upgraded electrical systems in many Silver Lake hillside homes, handling unique challenges with panel placement, conduit routing, and ground-fault protection."),
            ("What permits are needed for Silver Lake electrical work?", "Electrical work in Silver Lake requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Can you add EV charging to a Silver Lake bungalow?", "Absolutely — we install EV chargers in Silver Lake's older homes regularly. Most projects include a panel upgrade to 200A and careful routing to minimize visual impact."),
        ]
    },
    "simi-valley": {
        "housing": "Simi Valley features 1970s-1990s tract homes, some newer developments, and a suburban character in Ventura County.",
        "streets": "Simi Valley Boulevard, Cochran Street, Los Angeles Avenue, First Street",
        "landmarks": "The Ronald Reagan Presidential Library, the nearby Santa Susana Mountains, and the neighborhood's quiet residential streets.",
        "electrical": "Many Simi Valley homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you handle Simi Valley's permit process?", "Yes — we manage all permits with the City of Simi Valley Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in Simi Valley?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you service Simi Valley's newer developments?", "Yes — we work on both existing homes and new construction in Simi Valley."),
        ]
    },
    "studio-city": {
        "housing": "Studio City features 1940s-1970s homes, luxury estates, and some newer construction. The neighborhood is known for its entertainment industry presence.",
        "streets": "Ventura Boulevard, Laurel Canyon Boulevard, Mulholland Drive, Coldwater Canyon Avenue, Fairway Terrace",
        "landmarks": "Universal Studios nearby, the Studio City Recreation Center, and the vibrant Ventura Boulevard commercial corridor.",
        "electrical": "Many Studio City homes have 100A panels that need upgrading. Entertainment industry properties may have unique electrical needs.",
        "faqs": [
            ("Do you handle Studio City's panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Studio City homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical upgrades are common in Studio City?", "Common upgrades include 200A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring."),
            ("Do you service Studio City's entertainment properties?", "Yes — we've worked with entertainment companies in Studio City on temporary power, lighting, and electrical infrastructure."),
        ]
    },
    "sun-valley": {
        "housing": "Sun Valley features 1950s-1970s homes, industrial areas, and some newer developments.",
        "streets": "Sun Valley Boulevard, Roscoe Boulevard, Lankershim Boulevard, Vineland Avenue",
        "landmarks": "The nearby Universal Studios area, the Sun Valley Recreation Center, and the neighborhood's industrial character.",
        "electrical": "Many Sun Valley homes have 100A panels that need upgrading. Industrial areas may have commercial electrical needs.",
        "faqs": [
            ("Do you handle Sun Valley's commercial electrical?", "Yes — we provide commercial electrical services to Sun Valley businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Sun Valley electrical work?", "Electrical work in Sun Valley requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service Sun Valley's residential areas?", "Yes — we provide full electrical services to Sun Valley residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
        ]
    },
    "sylmar": {
        "housing": "Sylmar features 1950s-1970s homes, some newer developments, and equestrian properties in the northern San Fernando Valley.",
        "streets": "San Fernando Road, Foothill Boulevard, Glenoaks Boulevard, Polk Street",
        "landmarks": "The nearby Angeles National Forest, the Sylmar Recreation Center, and the neighborhood's equestrian character.",
        "electrical": "Many Sylmar homes have 100A panels that need upgrading. Equestrian properties may have unique electrical needs.",
        "faqs": [
            ("Do you handle Sylmar's equestrian properties?", "Yes — we provide electrical services to Sylmar's equestrian properties, including barn wiring, outdoor lighting, and panel upgrades."),
            ("What electrical upgrades are common in Sylmar?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you serve Sylmar's newer developments?", "Yes — we work on both existing homes and new construction in Sylmar."),
        ]
    },
    "tarzana": {
        "housing": "Tarzana features 1950s-1970s homes, luxury estates, and some newer construction. The neighborhood has a suburban character with larger lots.",
        "streets": "Ventura Boulevard, Reseda Boulevard, Mulholland Drive, Tarzana Street, Burbank Boulevard",
        "landmarks": "The nearby Santa Monica Mountains, the Tarzana Recreation Center, and the neighborhood's quiet residential streets.",
        "electrical": "Many Tarzana homes have 100A panels that need upgrading. Larger properties may need subpanels for EV charger installations.",
        "faqs": [
            ("Do you handle Tarzana's panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Tarzana homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical upgrades are common in Tarzana?", "Common upgrades include 200A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring."),
            ("Do you service Tarzana's luxury properties?", "Yes — we work on Tarzana's luxury estates, handling commercial-grade panels, whole-house generators, EV fleet charging, and sophisticated electrical systems."),
        ]
    },
    "thai-town": {
        "housing": "Thai Town features 1920s-1940s apartments, some newer developments, and a vibrant commercial district.",
        "streets": "Hollywood Boulevard, Western Avenue, Santa Monica Boulevard",
        "landmarks": "The Thai Town commercial district, the nearby East Hollywood area, and the neighborhood's diverse food scene.",
        "electrical": "Older apartment buildings often have outdated electrical systems. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle Thai Town's apartment buildings?", "Yes — we provide electrical services to Thai Town's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Thai Town electrical work?", "Electrical work in Thai Town requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service Thai Town's commercial properties?", "Yes — we provide commercial electrical services to Thai Town businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "thousand-oaks": {
        "housing": "Thousand Oaks features 1970s-1990s tract homes, some newer developments, and a suburban character in Ventura County.",
        "streets": "Thousand Oaks Boulevard, Westlake Boulevard, Moorpark Road, Ladybug Lane",
        "landmarks": "The nearby Santa Monica Mountains, the Thousand Oaks Civic Arts Plaza, and the neighborhood's quiet residential streets.",
        "electrical": "Many Thousand Oaks homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you handle Thousand Oaks' permit process?", "Yes — we manage all permits with the City of Thousand Oaks Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in Thousand Oaks?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you service Thousand Oaks' newer developments?", "Yes — we work on both existing homes and new construction in Thousand Oaks."),
        ]
    },
    "torrance": {
        "housing": "Torrance features 1960s-1970s tract homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Torrance Boulevard, Hawthorne Boulevard, Western Avenue, Crenshaw Boulevard, Sepulveda Boulevard",
        "landmarks": "The Del Amo Fashion Center, the nearby Redondo Beach area, and the neighborhood's strong community institutions.",
        "electrical": "Many Torrance homes have 100A panels that need upgrading. Industrial areas may have commercial electrical needs.",
        "faqs": [
            ("Do you handle Torrance's commercial electrical?", "Yes — we provide commercial electrical services to Torrance businesses, including tenant improvements, panel upgrades, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Torrance electrical work?", "Electrical work in Torrance requires permits from the City of Torrance. We handle all permit applications and inspections."),
            ("Do you service Torrance's residential areas?", "Yes — we provide full electrical services to Torrance residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
        ]
    },
    "university-park": {
        "housing": "University Park features 1920s-1940s apartments and homes, some newer developments, and the USC campus area.",
        "streets": "Figueroa Street, Jefferson Boulevard, Vermont Avenue, Exposition Boulevard",
        "landmarks": "The USC campus, the nearby Exposition Park area, and the neighborhood's mix of student and residential housing.",
        "electrical": "Older apartment buildings often have outdated electrical systems. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle University Park's apartment buildings?", "Yes — we provide electrical services to University Park's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for University Park electrical work?", "Electrical work in University Park requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service properties near USC?", "Yes — we provide electrical services to properties near USC, including student housing, commercial properties, and residential homes."),
        ]
    },
    "van-nuys": {
        "housing": "Van Nuys features 1950s-1970s tract homes, apartment buildings, and some newer developments. The area has a diverse, working-class community.",
        "streets": "Van Nuys Boulevard, Sherman Oaks Boulevard, Victory Boulevard, Sylvan Street, Hazeltine Avenue",
        "landmarks": "The nearby Van Nuys Airport, the Van Nuys Recreation Center, and the neighborhood's diverse commercial areas.",
        "electrical": "Many Van Nuys homes have 100A panels that need upgrading. Apartment buildings may need commercial-grade electrical systems.",
        "faqs": [
            ("Do you handle Van Nuys' panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Van Nuys homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical issues are common in Van Nuys?", "Common issues include outdated panels, aluminum wiring from the 1960s-70s, and insufficient capacity for modern appliances and EV chargers."),
            ("Do you service Van Nuys' apartment buildings?", "Yes — we provide electrical services to Van Nuys apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
        ]
    },
    "verdugo-city": {
        "housing": "Verdugo City features 1950s-1970s homes, some newer developments, and a suburban character near Glendale.",
        "streets": "Verdugo Road, Glendale Boulevard, and surrounding residential streets",
        "landmarks": "The nearby Verdugo Mountains, the Verdugo City area, and the neighborhood's quiet residential streets.",
        "electrical": "Many Verdugo City homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service Verdugo City homes?", "Yes — we provide full electrical services to Verdugo City residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Verdugo City?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle Verdugo City's permit process?", "Yes — we manage all permits for Verdugo City projects. Permit costs are included in our estimates."),
        ]
    },
    "vernon": {
        "housing": "Vernon is primarily an industrial city with limited residential areas. The city is known for its manufacturing and warehouse districts.",
        "streets": "Vernon Avenue, Soto Street, Alameda Street, Olympic Boulevard",
        "landmarks": "The Vernon Industrial District, the nearby Downtown LA area, and the city's manufacturing centers.",
        "electrical": "Vernon's electrical needs are primarily commercial and industrial, including warehouse electrical, manufacturing power, and EV fleet charging.",
        "faqs": [
            ("Do you handle Vernon's commercial electrical?", "Yes — we provide commercial electrical services to Vernon businesses, including warehouse electrical, manufacturing power, EV fleet charging, and lighting retrofits."),
            ("What permits are needed for Vernon electrical work?", "Electrical work in Vernon requires permits from the City of Vernon. We handle all permit applications and inspections."),
            ("Do you service Vernon's industrial areas?", "Yes — we provide commercial electrical services to Vernon's industrial areas, including warehouse electrical, manufacturing power, and lighting retrofits."),
        ]
    },
    "west-adams": {
        "housing": "West Adams features 1920s-1940s homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Adams Boulevard, Vermont Avenue, Western Avenue, Figueroa Street",
        "landmarks": "The nearby Exposition Park, the West Adams area, and the neighborhood's historic character.",
        "electrical": "Many West Adams homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you service West Adams homes?", "Yes — we provide full electrical services to West Adams residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in West Adams?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle West Adams' permit process?", "Yes — we manage all permits for West Adams projects. Permit costs are included in our estimates."),
        ]
    },
    "westchester": {
        "housing": "Westchester features 1940s-1960s homes, some newer developments, and a suburban character near LAX.",
        "streets": "Lincoln Boulevard, Manchester Avenue, Western Avenue, Sepulveda Boulevard",
        "landmarks": "LAX airport nearby, the Westchester Recreation Center, and the neighborhood's proximity to the South Bay.",
        "electrical": "Many Westchester homes have 100A panels that need upgrading. Proximity to the airport may require special electrical considerations.",
        "faqs": [
            ("Do you service Westchester homes?", "Yes — we provide full electrical services to Westchester residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Westchester?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle Westchester's permit process?", "Yes — we manage all permits for Westchester projects. Permit costs are included in our estimates."),
        ]
    },
    "west-covina": {
        "housing": "West Covina features 1960s-1970s tract homes, some newer developments, and a suburban character in the San Gabriel Valley.",
        "streets": "West Covina Parkway, Glendora Avenue, Vincent Avenue, Amar Road",
        "landmarks": "The West Covina Parkway shopping area, the nearby San Gabriel Mountains, and the neighborhood's quiet residential streets.",
        "electrical": "Many West Covina homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you handle West Covina's permit process?", "Yes — we manage all permits with the City of West Covina Building Department. Permit costs are included in our estimates."),
            ("What electrical upgrades are common in West Covina?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you service West Covina's newer developments?", "Yes — we work on both existing homes and new construction in West Covina."),
        ]
    },
    "west-hills": {
        "housing": "West Hills features 1970s-1990s homes, some newer developments, and a suburban character in the western San Fernando Valley.",
        "streets": "Fallbrook Avenue, Sherman Way, Vanowen Street, Woodlake Avenue",
        "landmarks": "The nearby Santa Susana Mountains, the West Hills area, and the neighborhood's quiet residential streets.",
        "electrical": "Many West Hills homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service West Hills homes?", "Yes — we provide full electrical services to West Hills residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in West Hills?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle West Hills' permit process?", "Yes — we manage all permits for West Hills projects. Permit costs are included in our estimates."),
        ]
    },
    "west-hollywood": {
        "housing": "West Hollywood features 1920s-1940s apartments, some newer developments, and a vibrant commercial district. The city has strict building codes and a creative community.",
        "streets": "Santa Monica Boulevard, Sunset Boulevard, Hollywood Boulevard, La Brea Avenue, Fairfax Avenue",
        "landmarks": "The Sunset Strip, the Pacific Design Center, the West Hollywood Library, and the neighborhood's vibrant nightlife and arts scene.",
        "electrical": "Many West Hollywood apartments have outdated electrical systems. New developments require modern electrical infrastructure. EV charger installations are growing rapidly.",
        "faqs": [
            ("Do you handle West Hollywood's apartment buildings?", "Yes — we provide electrical services to West Hollywood's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for West Hollywood electrical work?", "Electrical work in West Hollywood requires permits from the City of West Hollywood. We handle all permit applications and inspections."),
            ("Do you service West Hollywood's commercial properties?", "Yes — we provide commercial electrical services to West Hollywood businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "west-la": {
        "housing": "West LA features 1940s-1970s homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "West Los Angeles area, Olympic Boulevard, Pico Boulevard, Sepulveda Boulevard",
        "landmarks": "The nearby Westwood area, the West LA Recreation Center, and the neighborhood's central Westside location.",
        "electrical": "Many West LA homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service West LA homes?", "Yes — we provide full electrical services to West LA residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in West LA?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle West LA's permit process?", "Yes — we manage all permits for West LA projects. Permit costs are included in our estimates."),
        ]
    },
    "westlake": {
        "housing": "Westlake features 1920s-1940s apartments, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Westlake Avenue, Sixth Street, Alvarado Street, Beverly Boulevard",
        "landmarks": "The nearby MacArthur Park, the Westlake area, and the neighborhood's diverse character.",
        "electrical": "Many Westlake homes have older electrical systems that need modernization. Apartment buildings may need commercial-grade electrical systems.",
        "faqs": [
            ("Do you handle Westlake's apartment buildings?", "Yes — we provide electrical services to Westlake's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Westlake electrical work?", "Electrical work in Westlake requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service Westlake's commercial properties?", "Yes — we provide commercial electrical services to Westlake businesses, including tenant improvements, panel upgrades, and lighting retrofits."),
        ]
    },
    "westlake-village": {
        "housing": "Westlake Village features 1970s-1990s homes, some newer developments, and a suburban character near the Ventura County line.",
        "streets": "Westlake Boulevard, Lake Westlake Drive, Agoura Road",
        "landmarks": "The nearby Santa Monica Mountains, the Westlake Village area, and the neighborhood's quiet residential streets.",
        "electrical": "Many Westlake Village homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service Westlake Village homes?", "Yes — we provide full electrical services to Westlake Village residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Westlake Village?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle Westlake Village's permit process?", "Yes — we manage all permits for Westlake Village projects. Permit costs are included in our estimates."),
        ]
    },
    "westmont": {
        "housing": "Westmont features 1950s-1970s homes, some newer developments, and a mix of residential and commercial areas.",
        "streets": "Western Avenue, Vermont Avenue, Florence Avenue, Gage Avenue",
        "landmarks": "The neighborhood is near the nearby Inglewood and South LA areas, with easy freeway access.",
        "electrical": "Many Westmont homes have older electrical systems that need modernization. Panel upgrades are common for modern electrical demands.",
        "faqs": [
            ("Do you service Westmont homes?", "Yes — we provide full electrical services to Westmont residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Westmont?", "Common upgrades include 200A panel upgrades, EV charger installation, rewiring for older homes, and lighting retrofits."),
            ("Do you handle Westmont's permit process?", "Yes — we manage all permits for Westmont projects. Permit costs are included in our estimates."),
        ]
    },
    "westwood": {
        "housing": "Westwood features 1940s-1970s apartments, luxury condos, and a mix of residential and commercial areas near UCLA.",
        "streets": "Westwood Boulevard, Wilshire Boulevard, Santa Monica Boulevard, Gayley Avenue",
        "landmarks": "UCLA, the Westwood Village shopping district, the Hammer Museum, and the nearby Brentwood area.",
        "electrical": "Many Westwood apartments have outdated electrical systems. Panel upgrades are common for both residential and commercial properties.",
        "faqs": [
            ("Do you handle Westwood's apartment buildings?", "Yes — we provide electrical services to Westwood's apartment buildings, including common area electrical, individual unit upgrades, and EV charger installations."),
            ("What permits are needed for Westwood electrical work?", "Electrical work in Westwood requires permits from the City of Los Angeles. We handle all permit applications and inspections."),
            ("Do you service properties near UCLA?", "Yes — we provide electrical services to properties near UCLA, including student housing, commercial properties, and residential homes."),
        ]
    },
    "windsor-square": {
        "housing": "Windsor Square features 1920s-1940s Mediterranean and Tudor-style homes. The neighborhood is one of LA's most historic and architecturally significant areas.",
        "streets": "Windsor Boulevard, Third Street, Larchmont Boulevard, Fourth Street",
        "landmarks": "The nearby Hancock Park neighborhood, the Larchmont Village shopping district, and the neighborhood's tree-lined streets with historic homes.",
        "electrical": "Many Windsor Square homes have original electrical systems that need careful modernization. Historic district requirements may affect electrical upgrades.",
        "faqs": [
            ("Do you work on Windsor Square's historic homes?", "Yes — we've upgraded electrical systems in many Windsor Square homes, handling panel upgrades and rewiring while preserving the home's historic character."),
            ("What electrical challenges do Windsor Square homes face?", "Common challenges include original wiring that needs updating, small panels that can't handle modern loads, and maintaining the home's aesthetic during electrical upgrades."),
            ("Do you handle Windsor Square's historic district requirements?", "Yes — we understand Windsor Square's historic district requirements and ensure all electrical work meets current code while respecting the home's character."),
        ]
    },
    "winnetka": {
        "housing": "Winnetka features 1960s-1970s homes, some newer developments, and a suburban character in the western San Fernando Valley.",
        "streets": "Winnetka Avenue, Sherman Way, Vanowen Street, Pralle Street",
        "landmarks": "The nearby Chatsworth area, the Winnetka Recreation Center, and the neighborhood's quiet residential streets.",
        "electrical": "Many Winnetka homes have 100A panels that need upgrading for modern electrical demands.",
        "faqs": [
            ("Do you service Winnetka homes?", "Yes — we provide full electrical services to Winnetka residents, including panel upgrades, EV charger installation, rewiring, and lighting."),
            ("What electrical upgrades are common in Winnetka?", "Common upgrades include 200A panel upgrades, EV charger installation, outdoor lighting, and rewiring for older homes."),
            ("Do you handle Winnetka's permit process?", "Yes — we manage all permits for Winnetka projects. Permit costs are included in our estimates."),
        ]
    },
    "woodland-hills": {
        "housing": "Woodland Hills features 1960s-1970s homes, luxury estates, and some newer construction. The neighborhood is known for its hillside properties and proximity to the Santa Monica Mountains.",
        "streets": "Ventura Boulevard, Topanga Canyon Boulevard, Fallbrook Avenue, Mulholland Drive",
        "landmarks": "The nearby Santa Monica Mountains, the Warner Center area, and the neighborhood's quiet residential streets with larger lots.",
        "electrical": "Many Woodland Hills homes have 100A panels that need upgrading. Hillside properties may need subpanels or longer conduit runs for EV chargers.",
        "faqs": [
            ("Do you handle Woodland Hills' panel upgrades?", "Yes — we provide 200A and 400A panel upgrades for Woodland Hills homes. We coordinate with SCE for service upgrades and handle all permits."),
            ("What electrical upgrades are common in Woodland Hills?", "Common upgrades include 200A panel upgrades, EV charger installation, landscape lighting, pool electrical, and smart home wiring."),
            ("Do you service Woodland Hills' hillside properties?", "Yes — we handle the unique electrical needs of Woodland Hills' hillside properties, including subpanels, longer conduit runs, and ground-fault protection."),
        ]
    },
}

# ─── Script logic ────────────────────────────────────────────────────────

SITE_DIR = "/home/amram/WEBSITE"

def get_city_slug(filepath):
    """Extract city slug from filename: city-agoura-hills.html → agoura-hills"""
    basename = os.path.basename(filepath)
    return basename.replace("city-", "").replace(".html", "")


def get_city_display_name(slug):
    """Convert slug to display name: agoura-hills → Agoura Hills"""
    return slug.replace("-", " ").title()


def build_expanded_local_knowledge(slug, data):
    """Build the expanded Local Knowledge paragraph."""
    name = get_city_display_name(slug)
    return (
        f"{name} {data['housing']} "
        f"Key thoroughfares include {data['streets']}. "
        f"{data['landmarks']} "
        f"{data['electrical']}"
    )


def build_faq_items(slug, data):
    """Build new FAQ HTML items."""
    name = get_city_display_name(slug)
    items = []
    for question, answer in data["faqs"]:
        items.append(
            f'    <details class="faq-item"><summary class="faq-q">{question} '
            f'<span class="faq-chevron">▾</span></summary>'
            f'<div class="faq-a">{answer}</div></details>'
        )
    return "\n".join(items)


NEARBY_CITIES = {
    "agoura-hills": ["calabasas", "westlake-village", "thousand-oaks", "moorpark", "simi-valley"],
    "alhambra": ["san-gabriel", "montebello", "rosemead", "arcadia", "el-monte"],
    "arcadia": ["monrovia", "duarte", "azusa", "glendora", "pasadena"],
    "arleta": ["pacoima", "sylmar", "lake-view-terrace", "north-hollywood", "sun-valley"],
    "atwater-village": ["glendale", "glassell-park", "echopark", "silver-lake", "los-feliz"],
    "bel-air": ["brewood", "beverly-hills", "westwood", "belmont", "mulholland"],
    "bellflower": ["downey", "norwalk", "cerritos", "lakewood", "long-beach"],
    "beverly-grove": ["beverly-hills", "fairfax-district", "mid-city", "west-hollywood", "miracle-mile"],
    "beverly-hills": ["west-hollywood", "bel-air", "brentwood", "Century-city", "los-angeles"],
    "beverlywood": ["beverly-hills", "fairfax-district", "culver-city", "mid-city", "rancho-park"],
    "brentwood": ["bel-air", "westwood", "santa-monica", "malibu", " Century-city"],
    "burbank": ["glendale", "north-hollywood", "tujunga", "sun-valley", "beverly-hills"],
    "calabasas": ["agoura-hills", "westlake-village", "woodland-hills", "encino", "malibu"],
    "canoga-park": ["woodland-hills", "winnetka", "chatsworth", "northridge", "reseda"],
    "carson": ["long-beach", "compton", "gardena", "torrance", "hawthorne"],
    "century-city": ["beverly-hills", "westwood", "west-hollywood", "mid-city", " Century-city"],
    "chatsworth": ["northridge", "granada-hills", "porter-ranch", "canoga-park", "west-hills"],
    "cheviot-hills": ["beverly-hills", "Century-city", "westwood", "rancho-park", "mid-city"],
    "chinatown": ["downtown-la", "echo-park", "echopark", "los-feliz", "highland-park"],
    "covina": ["west-covina", "azusa", "glendora", "irwindale", "el-monte"],
    "culver-city": ["beverly-hills", "mar-vista", "palms", "west-los-angeles", "fox-hills"],
    "del-rey": ["marina-del-rey", "playa-del-rey", "westchester", "el-segundo", "mar-vista"],
    "downey": ["bellflower", "norwalk", "pico-rivera", "whittier", "paramount"],
    "downtown-la": ["chinatown", "arts-district", "south-park", "figueroa-corridor", "echo-park"],
    "eagle-rock": ["highland-park", "glassell-park", "glendale", "south-pasadena", "los-feliz"],
    "east-hollywood": ["koreatown", "little-armenia", "thai-town", "los-feliz", "hollywood"],
    "echo-park": ["silver-lake", "echopark", "chinatown", "downtown-la", "los-feliz"],
    "edith-norman": ["norwalk", "downey", "bellflower", "paramount", "compton"],
    "el-monte": ["arcadia", "monrovia", "azusa", "irwindale", "west-covina"],
    "el-segundo": ["manhattan-beach", "hermosa-beach", "redondo-beach", "hawthorne", "playa-vista"],
    "el-sobrante": ["el-monte", "arcadia", "monrovia", "sierra-madre", "pasadena"],
    "encino": ["woodland-hills", "tarzana", "studio-city", "bel-air", "brentwood"],
    "exposition-park": ["downtown-la", "south-la", "inglewood", "jefferson-park", "koreatown"],
    "fairfax-district": ["beverly-grove", "miracle-mile", "mid-city", "west-hollywood", "beverly-hills"],
    "figueroa-corridor": ["downtown-la", "jefferson-park", "south-park", "exposition-park", "koreatown"],
    "florence": ["south-central-la", "inglewood", "florence-firestone", "west-adams", "jefferson-park"],
    "fox-hills": ["culver-city", "mar-vista", "westchester", "playa-vista", "del-rey"],
    "gardena": ["torrance", "carson", "compton", "hawthorne", "inglewood"],
    "glassell-park": ["echopark", "atwater-village", "glendale", "eagle-rock", "silver-lake"],
    "glendale": ["burban", "pasadena", "eagle-rock", "atwater-village", "north-hollywood"],
    "granada-hills": ["chatsworth", "porter-ranch", "northridge", "north-hills", "sylmar"],
    "hancock-park": ["larchmont", "miracle-mile", "mid-city", "koreatown", "beverly-grove"],
    "hawthorne": ["inglewood", "el-segundo", "manhattan-beach", "gardena", "compton"],
    "health-campadre": ["glendale", "eagle-rock", "glassell-park", "south-pasadena", "los-feliz"],
    "highland-park": ["echopark", "eagle-rock", "montecito-heights", "south-pasadena", "glassell-park"],
    "holmby-hills": ["bel-air", "westwood", "brentwood", "beverly-hills", " Century-city"],
    "inglewood": ["hawthorne", "manhattan-beach", "gardena", "el-segundo", "playa-vista"],
    "jefferson-park": ["south-central-la", "west-adams", "exposition-park", "florence", "inglewood"],
    "koreatown": ["east-hollywood", "little-armenia", "mid-city", "beverly-grove", "miracle-mile"],
    "la-crescenta": ["montrose", "glendale", "la-canada-flintridge", "tujunga", "sunland"],
    "lake-view-terrace": ["pacoima", "sylmar", "shadow-hills", "sun-valley", "arleta"],
    "larchmont": ["hancock-park", "miracle-mile", "mid-city", "beverly-grove", "koreatown"],
    "little-armenia": ["east-hollywood", "koreatown", "thai-town", "hollywood", "los-feliz"],
    "long-beach": ["bellflower", "carson", "compton", "lakewood", "signal-hill"],
    "los-angeles": ["downtown-la", "hollywood", "beverly-hills", "santa-monica", "pasadena"],
    "los-feliz": ["echopark", "silver-lake", "east-hollywood", "hollywood", "glassell-park"],
    "malibu": ["calabasas", "santa-monica", "pacific-palisades", "malibu", "malibu"],
    "mar-vista": ["culver-city", "venice", "playa-vista", "del-rey", "fox-hills"],
    "mid-city": ["fairfax-district", "miracle-mile", "beverly-grove", "hancock-park", "koreatown"],
    "miracle-mile": ["mid-city", "fairfax-district", "hancock-park", "beverly-grove", "koreatown"],
    "montecito-heights": ["highland-park", "glassell-park", "south-pasadena", "eagle-rock", "echopark"],
    "north-glendale": ["glendale", "montrose", "la-canada-flintridge", "tujunga", "sunland"],
    "north-hills": ["reseda", "northridge", "sepulveda-basin", "granada-hills", "van-nuys"],
    "north-hollywood": ["burban", "studio-city", "valley-village", "van-nuys", "tujunga"],
    "northridge": ["north-hills", "granada-hills", "canoga-park", "chatsworth", "reseda"],
    "oak-park": ["agoura-hills", "thousand-oaks", "westlake-village", "calabasas", "moorpark"],
    "pacific-palisades": ["malibu", "santa-monica", "brentwood", "bel-air", "encino"],
    "pacoima": ["sylmar", "arleta", "lake-view-terrace", "sun-valley", "north-hollywood"],
    "palms": ["culver-city", "mar-vista", "west-los-angeles", "venice", "beverly-grove"],
    "pasadena": ["south-pasadena", "san-marino", "arcadia", "glendale", "los-angeles"],
    "pico-union": ["downtown-la", "koreatown", "mid-city", "west-adams", "exposition-park"],
    "porter-ranch": ["chatsworth", "granada-hills", "northridge", "north-hills", "west-hills"],
    "rancho-park": ["Century-city", "beverly-hills", "westwood", "culver-city", "mar-vista"],
    "redondo-beach": ["hermosa-beach", "manhattan-beach", "torrance", "el-segundo", "gardena"],
    "reseda": ["north-hills", "canoga-park", "northridge", "tarzana", "van-nuys"],
    "san-fernando": ["pacoima", "sylmar", "north-hollywood", "sun-valley", "granada-hills"],
    "sawtelle": ["westwood", "Century-city", "brentwood", "mar-vista", "palms"],
    "sawtelle-japantown": ["westwood", "Century-city", "brentwood", "mar-vista", "palms"],
    "shadow-hills": ["sunland", "tujunga", "lake-view-terrace", "pacoima", "sylmar"],
    "shadow-ranch-park": ["granada-hills", "chatsworth", "north-hills", "porter-ranch", "northridge"],
    "silver-lake": ["echopark", "echo-park", "los-feliz", "glassell-park", "east-hollywood"],
    "sun-valley": ["pacoima", "sylmar", "arleta", "lake-view-terrace", "north-hollywood"],
    "sylmar": ["pacoima", "san-fernando", "granada-hills", "lake-view-terrace", "shadow-hills"],
    "thai-town": ["east-hollywood", "little-armenia", "koreatown", "hollywood", "los-feliz"],
    "university-park": ["downtown-la", "south-central-la", "exposition-park", "jefferson-park", "figueroa-corridor"],
    "verdugo-city": ["glendale", "north-glendale", "montrose", "la-canada-flintridge", "eagle-rock"],
    "vernon": ["florence", "south-central-la", "commerce", "bell-gardens", "downey"],
    "west-adams": ["jefferson-park", "exposition-park", "mid-city", "koreatown", "downtown-la"],
    "westchester": ["playa-vista", "playa-del-rey", "el-segundo", "manhattan-beach", "inglewood"],
    "westlake": ["downtown-la", "echo-park", "pico-union", "koreatown", "east-hollywood"],
    "westmont": ["inglewood", "hawthorne", "south-central-la", "florence", "west-adams"],
    "westwood": ["Century-city", "beverly-hills", "brentwood", "bel-air", "sawtelle"],
    "windsor-square": ["hancock-park", "larchmont", "mid-city", "beverly-grove", "koreatown"],
    "winnetka": ["canoga-park", "woodland-hills", "chatsworth", "northridge", "porter-ranch"],
}


def build_nearby_cities_html(slug, name_display):
    """Build nearby cities cross-link HTML."""
    nearby = NEARBY_CITIES.get(slug, [])
    if not nearby:
        return ""
    
    links = []
    for city_slug in nearby[:5]:
        city_name = get_city_display_name(city_slug)
        links.append(f'<a href="city-{city_slug}">{city_name}</a>')
    
    return (
        f'\n    <p class="nearby-cities">Also serving: {" · ".join(links)}</p>'
    )


def process_file(filepath):
    """Process a single city HTML file."""
    slug = get_city_slug(filepath)

    if slug not in CITY_DATA:
        print(f"  SKIP (no data): {slug}")
        return False

    data = CITY_DATA[slug]

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    name_display = get_city_display_name(slug)

    # --- Detect template type ---
    # Template A: "Local Knowledge" + "Neighborhoods & Electrical Services"
    # Template B: "Local Knowledge" + "Neighborhoods & Landmarks"
    # Template C: "Neighborhood-aware planning" + "Electrical Work That Fits {City}"

    lk_electrical = 'Neighborhoods &amp; Electrical Services' in content
    lk_landmarks = 'Neighborhoods &amp; Landmarks' in content
    neighborhood_planning = 'Neighborhood-aware planning' in content
    local_service = '<span class="section-label">Local Service</span>' in content

    # --- Edit 1: Expand the knowledge paragraph ---
    new_paragraph = build_expanded_local_knowledge(slug, data)

    if lk_electrical or lk_landmarks:
        # Template A or B: Expand existing Local Knowledge paragraph
        lk_pattern = re.compile(
            r'(<div class="section-label">Local Knowledge</div>\s*'
            r'<h2>[^<]+Neighborhoods &amp; (?:Electrical Services|Landmarks)</h2>\s*'
            r'<p[^>]*>)(.*?)(</p>)',
            re.DOTALL
        )
        match = lk_pattern.search(content)
        if match:
            content = content[:match.start(2)] + new_paragraph + content[match.end(2):]
        else:
            print(f"  WARN: Could not find LK paragraph in {slug} (template A/B)")
    elif neighborhood_planning:
        # Template C: Expand "Neighborhood-aware planning" paragraph
        nap_pattern = re.compile(
            r'(<div class="section-label">Neighborhood-aware planning</div>\s*'
            r'<h2>Electrical Work That Fits [^<]+</h2>\s*'
            r'<p[^>]*>)(.*?)(</p>)',
            re.DOTALL
        )
        match = nap_pattern.search(content)
        if match:
            content = content[:match.start(2)] + new_paragraph + content[match.end(2):]
        else:
            print(f"  WARN: Could not find NAP paragraph in {slug} (template C)")
    elif local_service:
        # Template D: Replace first paragraph in Local Service section
        # Structure: <span class="section-label">Local Service</span>\n    <h2>... Electrical Services</h2>\n    <p>As a...</p>\n    <p>Our team...</p>
        ls_pattern = re.compile(
            r'(<span class="section-label">Local Service</span>\s*'
            r'<h2>[^<]+Electrical Services</h2>\s*'
            r'<p[^>]*>)(.*?)(</p>)',
            re.DOTALL
        )
        match = ls_pattern.search(content)
        if match:
            content = content[:match.start(2)] + new_paragraph + content[match.end(2):]
        else:
            print(f"  WARN: Could not find LS paragraph in {slug} (template D)")
    else:
        print(f"  WARN: Unknown template for {slug}")

    # --- Edit 2: Add new FAQ items ---
    # Find the last </details> in the faq-list, before the closing </div></div></section>
    faq_pattern = re.compile(
        r'(</details>)(\s*</div>\s*</div>\s*</section>)',
        re.DOTALL
    )

    match = faq_pattern.search(content)
    if match:
        faq_html = build_faq_items(slug, data)
        insert_pos = match.start(1) + len(match.group(1))
        content = content[:insert_pos] + "\n" + faq_html + content[match.start(2):]
    else:
        print(f"  WARN: Could not find FAQ insertion point in {slug}")

    # --- Edit 3: Add nearby city cross-links to Service Areas or Explore more section ---
    nearby_html = build_nearby_cities_html(slug, name_display)
    if nearby_html:
        # Try to insert before the "View All Service Areas" button (Template C/D)
        btn_pattern = re.compile(
            r'(<a href="/areas-served" class="btn btn-gold">View All Service Areas</a>)',
            re.DOTALL
        )
        match = btn_pattern.search(content)
        if match:
            content = content[:match.start(1)] + nearby_html + "\n    " + content[match.start(1):]
        else:
            # Try to insert into "Explore more" section (Template A/B)
            explore_pattern = re.compile(
                r'(Visit <a href="city-los-angeles">all AMY Electric service areas</a> to find nearby coverage\.)',
                re.DOTALL
            )
            match = explore_pattern.search(content)
            if match:
                content = content[:match.end(1)] + nearby_html + content[match.end(1):]
            else:
                # Fallback: insert before the last </div></section> in the file
                last_section = list(re.finditer(r'</div>\s*</section>', content))
                if last_section:
                    pos = last_section[-1].start()
                    content = content[:pos] + nearby_html + "\n  " + content[pos:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def main():
    files = sorted(glob.glob(os.path.join(SITE_DIR, "city-*.html")))
    print(f"Found {len(files)} city files")

    processed = 0
    skipped = 0
    errors = 0

    for filepath in files:
        slug = get_city_slug(filepath)
        try:
            if process_file(filepath):
                processed += 1
                print(f"  OK: {slug}")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ERROR: {slug}: {e}")

    print(f"\nDone: {processed} processed, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
