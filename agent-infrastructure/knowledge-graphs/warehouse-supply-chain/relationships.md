# Relationship Types -- Warehouse & Supply Chain

## competes-with
Direction: company -> company (or product -> product)
Properties: segment, intensity(direct|indirect|adjacent), notes
Example: R[Blue Yonder|competes-with|Manhattan Associates|segment:enterprise-WMS+LMS|intensity:direct]

## integrates-with
Direction: product -> product (or product -> technology)
Properties: method(API|native|adapter|webhook|SDK|REST|MQTT|OData|SFTP), depth(deep|shallow|native), status(production|planned|beta)
Example: R[Robotics Hub|integrates-with|VDA 5050|method:native|depth:deep]

## acquired
Direction: company -> company (or company -> product)
Properties: date, price, rationale, from(previous-owner)
Example: R[Ocado|acquired|6 River Systems|date:2023|from:Shopify]

## serves-segment
Direction: product -> market-segment
Properties: tier(primary|secondary|emerging), pricing-range
Example: R[Robotics Hub|serves-segment|Warehouse LMS|tier:primary|pricing:$500K+]

## uses-technology
Direction: product -> technology
Properties: how, since, depth(core|supplementary|experimental)
Example: R[Robotics Hub|uses-technology|VDA 5050|how:robot-interop-standard|depth:core]

## invests-in
Direction: company -> company
Properties: amount, date, round(seed|A|B|C|D|growth|PE), lead(bool)
Example: R[Insight Partners|invests-in|Locus Robotics|amount:undisclosed|round:multiple]

## partners-with
Direction: company -> company
Properties: type(technology|channel|OEM|integration|strategic), since, scope
Example: R[Manhattan Associates|partners-with|Agility Robotics|type:technology|since:Apr-2024|scope:humanoid-integration]

## employs-methodology
Direction: product -> technology
Properties: how, phase(core|optional|deferred)
Example: R[Active Labor Management|employs-methodology|MOST|how:engineered-labor-standards]

## parent-of
Direction: company -> company
Properties: relationship(subsidiary|division|brand|portfolio-company)
Example: R[Cinven|parent-of|Alter Domus|relationship:portfolio-company]

## supplies-to
Direction: company -> company
Properties: product, volume, significance
Example: R[Symbotic|supplies-to|Walmart|product:warehouse-automation|volume:42-DCs|significance:exclusive-12yr]

## disrupts
Direction: technology -> market-segment (or product -> product)
Properties: mechanism, timeline(immediate|near-term|medium-term|long-term), severity(incremental|significant|transformative)
Example: R[WES|disrupts|Warehouse LMS|mechanism:absorbing-LMS-functions-from-above|timeline:medium-term|severity:significant]

## bundles-with
Direction: product -> product
Properties: coupling(tight|loose|optional), pricing-impact
Example: R[Active WM|bundles-with|Active Labor Management|coupling:tight|pricing-impact:LMS-included-in-WMS-license]
