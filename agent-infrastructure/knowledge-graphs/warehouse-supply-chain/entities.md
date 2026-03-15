# Entity Types -- Warehouse & Supply Chain

## company
Fields: name, type(vendor|3PL|enterprise|startup|PE|VC|industrial|retailer), products, funding, revenue, AUA/AUM, founded, HQ, employees, facilities
Example: {name: "Blue Yonder", type: vendor, products: [WMS, Robotics Hub, LMS, WFM], revenue: "~$1.4B", HQ: "Scottsdale, AZ"}

## product
Fields: name, vendor, category(WMS|LMS|WES|WCS|WFM|AMR|AGV|cobot|fleet-mgmt|orchestration|software|hardware|platform), pricing, deployment(cloud|on-prem|hybrid|SaaS|RaaS), launched, features, customers
Example: {name: "Robotics Hub", vendor: "Blue Yonder", category: WES, pricing: "$500K+", deployment: cloud, features: "vendor-agnostic robot orchestration, +22% labor productivity"}

## market-segment
Fields: name, TAM, CAGR, forecast, description, sources
Example: {name: "Warehouse LMS", TAM: "$719M(2025)", CAGR: "23.3%", forecast: "$3.72B(2033)", description: "Labor management systems for warehouses"}

## technology
Fields: name, category(protocol|standard|framework|algorithm|methodology|hardware|sensor|platform), maturity(proven|emerging|speculative|commoditizing), age, description, region
Example: {name: "VDA 5050", category: protocol, maturity: proven, description: "EU-dominant AMR/AGV interop standard, JSON-over-MQTT"}

## metric
Fields: name, value, source, date, context, confidence(HIGH|MEDIUM|LOW)
Example: {name: "warehouse-labor-pct-opex", value: "45-57%", source: "MHL News", date: "2025", context: "US warehouses", confidence: HIGH}

## person
Fields: name, role, company, relevance
Example: {name: "Terry Duffy", role: "CEO", company: "CME Group", relevance: "confirmed GCUL pilot Feb 2026"}

## event
Fields: name, date, type(acquisition|funding|launch|partnership|regulation), parties, value, significance
Example: {name: "Symbotic acquires Walmart ASR", date: "Jan 2025", type: acquisition, parties: "Symbotic, Walmart", value: "$200M+$350M contingent+$520M dev"}
