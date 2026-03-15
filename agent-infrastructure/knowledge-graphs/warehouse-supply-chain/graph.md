# Warehouse & Supply Chain Knowledge Graph
## Last updated: 2026-03-14
## Source: sigma-review warehouse-LMS analysis (r1+r2, 5 agents + DA)
## Status: seeded from initial review, will grow with subsequent analyses

---

### Companies -- Vendors (WMS/LMS/WES)

E[Blue Yonder|type:vendor|products:WMS,Robotics-Hub,LMS,WFM,WES|revenue:~$1.4B|HQ:Scottsdale-AZ|notes:closest-to-unified-labor+robot-platform,cloud-native-SaaS,vendor-agnostic-robot-orchestration|src:workspace-DA[#1],TIA-r2]
E[Manhattan Associates|type:vendor|products:Active-WM,Active-Labor-Management,Manhattan-Automation-Network,WES|revenue:~$950M|HQ:Atlanta-GA|notes:best-in-class-embedded-LMS,250+-microservices-architecture,"every-resource-labor-automation-robotics",only-WES-built-inside-WMS|src:PS-F1,TA-F1,TIA-r2]
E[Easy Metrics|type:vendor|products:ProTrack-LMS|facilities:600+|HQ:US|notes:standalone-LMS-market-leader,acquired-TZA-ProTrack-May-2025,AI/ML-features-rolling-out|src:PS-F1,PS-F7]
E[SAP|type:vendor|products:SAP-EWM,MFS|notes:enterprise-ERP-captive-WMS,PLC-level-automation,OData-integration|src:PS-F1,TA-F7]
E[Oracle|type:vendor|products:Oracle-WMS|notes:enterprise-WMS,mature-market|src:PS-F1,TIA-F3]
E[Infios|type:vendor|products:WMS-WES|notes:rebranded-from-Korber-Mar-2025|src:PS-F1]
E[Korber|type:vendor|products:WMS-WES|notes:rebranded-to-Infios-Mar-2025,leading-WES-vendor|src:PS-F1,TIA-F3]
E[Softeon|type:vendor|products:WMS-WES|notes:leading-WES-vendor|src:TIA-F3]
E[Dematic|type:vendor|products:WES,automation|notes:owned-by-KION|src:TIA-F3,TIA-F1]
E[Takt|type:vendor|products:cloud-LMS|deployment:SaaS|notes:4-week-onboard,B2C/D2C/3PL-focus,cloud-native|src:PS-F1,PS-F7]
E[Rebus|type:vendor|products:LMS|notes:system-agnostic,3PL-billing,Legion-partnership|src:PS-F1]
E[Honeywell|type:vendor|products:Momentum-WES,Vocollect-voice|notes:43%-productivity-gain-claimed,cloud-WES-launched-Mar-2025,voice-directed-picking-leader,30+-languages|src:PS-F1,UX-F2,UX-F5]
E[Lucas Systems|type:vendor|products:Jennifer-AI-voice|notes:voice-directed-picking,open-API/WMS-integration,30+-languages,99.99%-accuracy|src:UX-F2,UX-DA[#14a]]
E[Legion Technology|type:vendor|products:AI-scheduling-WFM|funding:$50M-SVB-Dec-2024|notes:13x-ROI-claimed,Rebus-partnership,WFM-adjacent|src:PS-F1]
E[Onomatic|type:vendor|products:vendor-agnostic-orchestration|notes:early-stage,no-labor-management|src:TIA-F8]
E[JASCI|type:vendor|products:robot+human-workflow-orchestration|notes:execution-focused,not-labor-economics|src:TIA-r2]
E[UKG|type:vendor|products:Kronos-WFM|notes:broad-WFM,not-warehouse-specific|src:PS-F1]
E[Deposco|type:vendor|products:WMS|notes:WMS-agnostic-integration-target,mid-market|src:PS-F5]
E[Extensiv|type:vendor|products:WMS|notes:WMS-agnostic-integration-target,3PL-focused|src:PS-F5]

### Companies -- Robotics Vendors

E[Locus Robotics|type:vendor|products:LocusONE,LocusINTELLIGENCE,Locus-Array-R2G,AMR|picks:6B+|picks-per-week:45M|growth:30-40%-YoY|notes:RaaS-model-leader,patent-pending-AI-human+robot-coordination,LocusINTELLIGENCE-Mar-2025-system-directed-labor-optimization,Locus-robots-only-not-vendor-agnostic,CLOSEST-to-unified-labor+robot|src:PS-F1,TIA-F1,TIA-F8]
E[Symbotic|type:vendor|products:warehouse-automation-systems|revenue:$1.68B-TTM|backlog:$5B+|notes:acquired-Walmart-ASR-Jan-2025+Fox-Robotics,42-Walmart-DCs,12yr-exclusive-Walmart|src:TIA-F1,TIA-F4]
E[AutoStore|type:vendor|products:cube-storage-automation|revenue:$496M(2023)|notes:cube-storage-dominant|src:TIA-F1]
E[Boston Dynamics|type:vendor|products:Stretch,Orbit|notes:DHL-1000+-unit-MOU,Lidl-EU-rollout-2026,Otto-Group-20+-facilities,700-1000-cases/hr,Orbit=fleet-mgmt-not-labor|src:TIA-F1,TIA-r2]
E[6 River Systems|type:vendor|products:Chuck-AMR|facilities:100+|customers:70+|notes:robot-leads-picker-model,acquired-from-Shopify-by-Ocado,now-Ocado-Intelligent-Automation|src:TIA-F1,TA-F5]
E[Ocado|type:vendor|products:Ocado-Intelligent-Automation|notes:acquired-6-River-Systems-from-Shopify-2023|src:TIA-F1]
E[Geek+|type:vendor|products:shelf/tote/pallet-to-person-AMR|notes:China-origin-global-expansion,goods-to-person|src:TIA-F1]
E[GreyOrange|type:vendor|products:GreyMatter-orchestration|funding:$436M-total|notes:orchestrates-robotic+manual,narrow-robot-type-support|src:TIA-F1,TIA-F8]
E[Vecna Robotics|type:vendor|products:AMR|funding:$193M-total($100M-Series-C)|customers:FedEx,GEODIS,Caterpillar|notes:triple-digit-revenue-growth|src:TIA-F1]
E[Fetch Robotics|type:vendor|products:AMR|notes:acquired-by-Zebra|src:TIA-F1]
E[Berkshire Grey|type:vendor|products:robotic-picking-systems|revenue:$23.6M-Q3|installs:57|notes:partnered-with-Locus-Robotics|src:TIA-F1]
E[Figure|type:startup|products:humanoid-robots|funding:$675M($1B-first-round)|notes:pre-commercial-2-3yr-from-production|src:TIA-F2,TIA-F6]
E[Apptronik|type:startup|products:humanoid-robots|funding:$350M-Series-A|notes:pre-commercial|src:TIA-F6]
E[Neura Robotics|type:startup|products:humanoid-robots|funding:€120M|notes:pre-commercial|src:TIA-F6]
E[Physical Intelligence|type:startup|products:AI-robotics|funding:$400M|valuation:$2B|src:TIA-F6]
E[Agility Robotics|type:vendor|products:Digit-humanoid|notes:Manhattan-partnership-Apr-2024|src:workspace-DA[#1]]
E[Rapyuta Robotics|type:vendor|products:AMR|notes:13-bots-@$1K/mo+$75K-setup,ROI-positive-month-9|src:TIA-F5]
E[Standard Bots|type:vendor|products:robot-arms|notes:lacks-LocusINTELLIGENCE-equivalent|src:PS-DA[#9]]

### Companies -- Industrials & Conglomerates

E[Zebra Technologies|type:industrial|products:handheld-scanners(TC52/TC72),acquired-Fetch+Photoneo|notes:rugged-Android-devices,IP67/68,warehouse-hardware-leader|src:UX-F2,TIA-F1]
E[Toyota Industries|type:industrial|products:material-handling|notes:acquired-Vanderlande|src:TIA-F1]
E[KION Group|type:industrial|products:material-handling|notes:owns-Dematic|src:TIA-F1]
E[ABB|type:industrial|products:industrial-automation|notes:acquired-ASTI|src:TIA-F1]
E[Rockwell Automation|type:industrial|products:industrial-automation,Emulate3D|notes:acquired-Clearpath,5x-productivity-in-sim,10x-error-reduction|src:TIA-F2]
E[Siemens|type:industrial|products:digital-twin,AI-robotics|notes:Feb-2026-AI-robotics-partnership-for-virtual-warehouse-trials|src:TIA-F2]

### Companies -- Retailers & 3PLs

E[Amazon|type:retailer|products:internal-warehouse-automation|notes:BUILDS-own(Gen13/14),75%-automation-target,$50B+-logistics-capex,anomaly-not-replicable,1.5M+-warehouse-workers,$22+/hr-wage-floor,$2.2B-wage-hike-Q1-2025|src:TIA-F4,EA-F3,DA[#8]]
E[Walmart|type:retailer|notes:PIVOTED-build-to-buy(sold-ASR-to-Symbotic-Jan-2025),50%+-automated-via-partners,29-e-commerce-FCs,2x-productivity-vs-legacy|src:TIA-F4]
E[DHL|type:3PL|notes:44%-deployed-robotics,34%-satisfied,BD-Stretch-1000+-unit-MOU,AR-glasses-15-25%-productivity-gain|src:PS-F1,UX-F9,TIA-F1]
E[GXO|type:3PL|revenue:$11.7B|margin:1.9%-net|notes:low-margin-illustrates-3PL-economics|src:EA-F6]
E[FedEx|type:enterprise|notes:Vecna-Robotics-customer|src:TIA-F1]
E[GEODIS|type:3PL|notes:Vecna-Robotics-customer|src:TIA-F1]
E[Caterpillar|type:enterprise|notes:Vecna-Robotics-customer|src:TIA-F1]
E[Otto Group|type:retailer|notes:BD-Stretch-20+-facilities|src:TIA-F1]
E[Lidl|type:retailer|notes:BD-Stretch-EU-rollout-2026|src:TIA-F1]
E[PepsiCo|type:enterprise|notes:digital-twin-deployment-20%-improvement|src:UX-F9]

### Companies -- PE/VC/Investors

E[Insight Partners|type:VC|notes:invests-in-Locus-Robotics+Hypercore|src:PS-r1,TIA-F6]
E[Woven Capital|type:VC|fund:$200M|notes:Toyota-affiliated,robotics-focused|src:TIA-F6]
E[Tiger Global|type:VC|notes:active-in-robotics|src:TIA-F6]
E[B Capital|type:VC|notes:active-in-robotics|src:TIA-F6]
E[Bezos Expeditions|type:VC|notes:active-in-robotics|src:TIA-F6]
E[SVB|type:VC|notes:funded-Legion-Technology-$50M-Dec-2024|src:PS-F1]
E[Cinven|type:PE|notes:Alter-Domus-investment-€4.9B-EV-Mar-2024|src:PS-loan-admin]
E[Oakley Capital|type:PE|notes:GLAS-investment-$1.35B-Jan-2026|src:PS-loan-admin]

### Companies -- Wearables & Sensors

E[ProGlove|type:vendor|products:smart-ring-scanners|notes:haptic-feedback,BLE,<50g,50%-scan-time-reduction,API-available|src:UX-F2,UX-F8]
E[Modjoul|type:vendor|products:SmartBelt-wearable|notes:haptic-feedback,ergonomic-monitoring,API-available|src:UX-F2,UX-F8]
E[RealWear|type:vendor|products:smart-glasses|notes:noise-cancel-to-100dB,heads-up-display|src:UX-F5]
E[Vuzix|type:vendor|products:smart-glasses|notes:AR-heads-up-display|src:UX-F2]
E[BaselineNC|type:vendor|products:predictive-fatigue-analytics|notes:98%-accuracy-claimed,wearable-based|src:UX-F9]
E[Bodytrak|type:vendor|products:fatigue-monitoring-wearable|src:UX-F9]

### Companies -- Software/Analytics

E[Nvidia|type:vendor|products:Omniverse|notes:digital-twin-platform-for-warehouse-simulation|src:UX-F9]
E[Grafana|type:vendor|products:dashboards-observability|notes:68%-IoT-use-TSDB+RDBMS-2025|src:TA-F2]
E[Confluent|type:vendor|products:Kafka-platform|notes:45%-cite-state-mgmt-as-top-Kafka-Streams-challenge|src:TA-F3]

### Companies -- Loan Admin (cross-domain, from prior review)

E[Alter Domus|type:vendor|products:Agency360,Solvas-Digitize,CorPro|AUA:$2.5T|employees:5500+|revenue-growth:18%-2024|notes:M&A-assembled-integration-debt,Cinven-€4.9B-EV,Solvas-Digitize-has-AI-in-production,Bain-Capital-$30B-win-Feb-2026|src:PS-loan-admin-r1-r3]
E[GLAS|type:vendor|products:loan-agency-trustee|AUA:$750B+|revenue:$30.9M-parent|notes:independent-conflict-free,proprietary-tech,40%-organic-growth,Oakley-Capital+La-Caisse-$1.35B-Jan-2026-43x-revenue-multiple,acquired-Serica+Watiga+LAS(Italy),10-jurisdictions|src:PS-loan-admin-r1-r3]
E[Kroll|type:vendor|products:cloud-native-loan-agency|notes:#3-Bloomberg-Q1-2025,8-day-vs-47-day-settlement,AI-practices-launched-2026,expanding-APAC-Madison-Pacific|src:PS-loan-admin-r1-r3]
E[Hypercore|type:startup|products:AI-loan-admin-SaaS|funding:$13.5M-Series-A(Insight-Partners-Feb-2026)|AUM:$20B+|loans:10K+|CARR-growth:3.5x|notes:first-AI-Admin-Agent-for-private-credit,SaaS-only,20-person-team,most-acquirable-competitor|src:PS-loan-admin-r1-r3]
E[Finastra|type:vendor|products:Loan-IQ|notes:75%-global-syndicated-loan-volume,IDC-MarketScape-2025-Leader|src:PS-loan-admin-r1]
E[Versana|type:vendor|products:digital-loan-data|notional:$5T|notes:real-time-digital-capture,JPM+BofA+Citi+DB+MS+WF+Barclays-backed,Morgan-Stanley+Mizuho-live-2025|src:PS-loan-admin-r1]
E[Oxane Partners|type:vendor|products:Panorama,Loan-Servicing-2.0|notional:$350B+|clients:100+|notes:13/25-top-banks|src:PS-loan-admin-r1]
E[Ontra|type:vendor|products:AI-contract-intelligence|docs:2M+|firms:1000+|notes:9/10-top-PE,Insight-for-Credit-Sep-2025,point-tool|src:PS-loan-admin-r1]

---

### Products

E[Robotics Hub|vendor:Blue-Yonder|category:WES/orchestration|pricing:$500K+|deployment:cloud-SaaS|features:vendor-agnostic-robot-orchestration,+22%-labor-productivity,-17%-cycle-times,+25%-throughput-mixed-fleet,plug-and-play-hours-not-months,resource-orchestration-engine-human+robotic-workloads,WMS-agnostic(DA-confirmed)|src:workspace-DA[#1],TIA-r2]
E[Active WM|vendor:Manhattan-Associates|category:WMS|deployment:cloud|features:250+-microservices,K8s,REST,real-time-per-task-tracking,unified-resource-orchestration-labor+automation+robotics|src:TA-F1,TIA-F8]
E[Active Labor Management|vendor:Manhattan-Associates|category:LMS|notes:best-in-class-embedded-LMS,deep-WMS-lock-in,ELS-engine-task-timestamp-vs-standard,robotics-integration-less-mature|src:PS-F1,TA-F4]
E[Manhattan Automation Network|vendor:Manhattan-Associates|category:robotics-integration|notes:vendor-specific-below-unified-metrics-above|src:TA-DA[#6]]
E[LocusONE|vendor:Locus-Robotics|category:fleet-mgmt|features:unified-fleet,patent-pending-AI-human+robot-coordination,Locus-robots-only,multi-robot-orchestration|src:PS-F1,TIA-F8]
E[LocusINTELLIGENCE|vendor:Locus-Robotics|category:labor-optimization|launched:Mar-2025|features:system-directed-labor-optimization,worker-productivity-dashboards,real-time-operational-intelligence,next-best-task-direction|src:workspace-DA[#1]]
E[Locus Array R2G|vendor:Locus-Robotics|category:AMR|notes:shipped,goods-to-person|src:PS-F1]
E[ProTrack LMS|vendor:Easy-Metrics|category:LMS|facilities:600+|notes:acquired-from-TZA-May-2025,standalone-LMS-market-leader|src:PS-F1]
E[Chuck|vendor:6-River-Systems/Ocado|category:AMR|features:robot-leads-picker,touchscreen-SKU-info,15-min-onboarding|notes:collaborative-picking-AMR|src:UX-F3,TA-F5]
E[Stretch|vendor:Boston-Dynamics|category:robot-arm|features:700-1000-cases/hr|notes:case-handling-robot,DHL-1000+-MOU|src:TIA-F1]
E[Orbit|vendor:Boston-Dynamics|category:fleet-mgmt|notes:fleet-management+WMS-integration,not-labor-management|src:TIA-r2]
E[GreyMatter|vendor:GreyOrange|category:orchestration|features:orchestrates-robotic+manual|notes:narrow-robot-type-support|src:TIA-F8]
E[SAP EWM|vendor:SAP|category:WMS|features:MFS-PLC-level-automation,OData-integration|notes:enterprise-ERP-captive|src:TA-F7]
E[Momentum WES|vendor:Honeywell|category:WES|launched:Mar-2025|notes:cloud-WES,43%-productivity-gain-claimed|src:PS-F1]
E[Vocollect|vendor:Honeywell|category:voice-directed|features:hands-free-eyes-free,30+-languages,99.99%-accuracy,works-noise/cold/dark|src:UX-F2,UX-F5]
E[Jennifer AI|vendor:Lucas-Systems|category:voice-directed|features:open-API/WMS-integration,30+-languages,99.99%-accuracy,accent-tolerance|notes:voice-directed-picking-leader,partner-not-compete|src:UX-DA[#14a]]
E[Emulate3D|vendor:Rockwell-Automation|category:digital-twin|features:5x-productivity-in-sim,10x-error-reduction,retrofit-focus|src:TIA-F2]
E[SmartBelt|vendor:Modjoul|category:wearable|features:haptic-feedback,ergonomic-monitoring|src:UX-F8]
E[TC52|vendor:Zebra|category:handheld-scanner|features:rugged-Android,5+-inch-screen,glove-compatible,IP67/68,all-shift-battery|src:UX-F2]
E[TC72|vendor:Zebra|category:handheld-scanner|features:rugged-Android,glove-compatible,IP67/68|src:UX-F2]

---

### Technologies

E[VDA 5050|category:protocol|maturity:proven|region:EU-dominant-NA-growing|version:v2.1.0-Jan-2025|description:JSON-over-MQTT-robot-interop-standard,order=graph(nodes+edges),QoS0-order/state,QoS1-connection|src:TA-F6,PS-research]
E[MassRobotics AMR Interop|category:protocol|maturity:proven|region:NA-dominant|version:v2.0|description:coexistence-monitoring-layer,broadcasts-location/speed/health,v2.0-adds-charging,monitoring-only-no-command|src:TA-F6,PS-research]
E[Open-RMF|category:protocol|maturity:proven|type:open-source|description:ROS2-based,free_fleet-adapter,traffic-negotiation-via-schedule-aware-routing,most-complex-of-3-standards|src:TA-F6,PS-research]
E[MOST|category:methodology|maturity:proven|age:50yr|description:Maynard-Operation-Sequence-Technique,3-sequences(General-Move,Controlled-Move,Tool-Use),calc=sum-indexes*10=TMU(1TMU=0.036s),dominant-PMTS-for-engineered-labor-standards|src:TA-F4,PS-research]
E[MTM|category:methodology|maturity:proven|description:Methods-Time-Measurement,alternative-to-MOST|src:PS-research]
E[MODAPTS|category:methodology|maturity:proven|description:Modular-Arrangement-of-Predetermined-Time-Standards,alternative-to-MOST|src:PS-research]
E[Hungarian Method|category:algorithm|maturity:proven|complexity:O(n3)|age:1955|description:optimal-bipartite-worker-to-task-assignment,optimal-for-waveless-allocation|src:TA-F5]
E[Waveless Picking|category:methodology|maturity:proven|description:continuous-order-release-not-wave-based,+40%-throughput(inVia),+20%-labor-utilization|src:TA-F5]
E[MQTT|category:protocol|maturity:proven|description:pub/sub-for-edge-IoT,low-latency-<10ms,scanner+RTLS+robot-telemetry|src:TA-F3,TA-F8]
E[Kafka|category:platform|maturity:proven|description:high-throughput-event-streaming,topic-per-domain,partitioned-by-site-id,headroom=millions/s|src:TA-F3]
E[Kafka Streams|category:framework|maturity:proven|description:embedded-stream-processing-no-cluster,tumbling/sliding/session-windows,80%-of-Flink-capability|src:TA-F3]
E[Apache Flink|category:framework|maturity:proven|description:distributed-stream-processing,multi-stream-joins,event-time,used-at-DHL/Amazon/Walmart-at-1M+/min,complex-ops-cluster+checkpointing|src:TA-F3]
E[TimescaleDB|category:database|maturity:proven|description:PG-extension-TSDB,continuous-aggregates,same-cluster-as-PG,better-JOINs-than-InfluxDB|src:TA-F2]
E[ClickHouse|category:database|maturity:proven|description:columnar-analytics-DB,deferred-until-analytics-latency>5s-at-~100-sites,CDC-via-Debezium|src:TA-F2]
E[PostgreSQL|category:database|maturity:proven|description:operational-store,JSONB+partitioning,entities=Worker-Task-Zone-Robot-Standard-Shift-CostCenter|src:TA-F2]
E[CloudEvents|category:standard|maturity:proven|description:vendor-neutral-event-format|src:TA-F1]
E[UWB RTLS|category:sensor-technology|maturity:proven|description:ultra-wideband-real-time-location,10-30cm-accuracy,tag-to-anchor-to-server-5-layer|src:PS-research]
E[RFID|category:sensor-technology|maturity:proven|description:barcode-alternative,warehouse-standard|src:TA-F3]
E[XGBoost|category:algorithm|maturity:proven|description:gradient-boosted-trees,ML-for-labor-standard-adjustment,cap-at-±15%,retrain-weekly-90d-window|src:TA-F4]
E[YOLO11|category:algorithm|maturity:emerging|description:computer-vision-pose-estimation,PPE-hazards,item-ID-quality-inspection|src:PS-research]
E[Reinforcement Learning|category:algorithm|maturity:emerging|description:Q-Mix-POMDP-for-task-allocation,92.5%-conflict-free-in-research,NOT-production-ready-day-1|src:TA-F5,PS-research]
E[Digital Twin|category:technology|maturity:emerging|market:$617M(2025)-to-$2.4B(2035)|CAGR:14.5%|description:warehouse-simulation,Siemens+Rockwell-leaders,74.6%-on-premises,worker-facing=novel|src:TIA-F2,UX-F9]
E[RaaS|category:business-model|maturity:proven|description:Robot-as-a-Service,subscription-OPEX-model,$2-4K/mo-per-AMR,52%-new-deployments-2024,64%-using-up-from-46%-2022|src:TIA-F5]
E[ISO 10218:2025|category:standard|maturity:proven|description:robot-safety-standard,force-limiting,AI-3D-vision,speed-reduction-on-proximity|src:UX-F3]
E[PFD Allowance|category:methodology|maturity:proven|description:Personal-Fatigue-Delay-allowance-15-20%-added-to-engineered-standards|src:TA-F4]
E[Pick-to-Light|category:technology|maturity:proven|description:LEDs-at-bins-for-fast-mover-areas,reduces-search-time|src:UX-F2]
E[Put-to-Light|category:technology|maturity:proven|description:scan-item-illuminates-destination,ideal-sorting/packing|src:UX-F2]
E[Voice-Directed Picking|category:technology|maturity:proven|description:hands-free-eyes-free,check-digit-confirm,99.99%-accuracy,30+-languages,works-noise/cold/dark|src:UX-F2]

---

### Market Segments

E[Warehouse LMS|TAM:$719.4M(2025)|CAGR:23.3%|forecast:$3.72B(2033)|notes:fastest-growing-WMS-segment,conservative-estimate-15-18%-CAGR=$500M-$1.5B(2033),standalone-TAM-inflated-by-WMS-bundling,true-standalone=$400-500M(EA-revised),29%-spike-demand-for-WMS-with-labor-features|src:EA-F1,PS-F2,GrandViewResearch]
E[Warehouse WMS|TAM:$3.38-4.85B(2025)|CAGR:17-18%|forecast:$10B+(2030)|notes:mature-market,Oracle/SAP/Manhattan-dominate|src:EA-F1,MordorIntel,MarketsandMarkets]
E[Warehouse WES|TAM:$1.86B(2025)|CAGR:18%|forecast:$9.57B(2035)|notes:fastest-growing-stack-layer,absorbing-WCS-from-below-AND-LMS-from-above,critical-integration-layer|src:TIA-F3,GrandViewResearch]
E[Warehouse Automation|TAM:~$31B(2025)|CAGR:16%|forecast:$120B(2034)|notes:M&A-acceleration-Symbotic+Zebra+Rockwell+Toyota+KION+ABB|src:TIA-F1,FortuneBizInsights]
E[Warehouse Robotics|TAM:$7-9.3B(2025)|CAGR:17.5%|forecast:$24.55B(2031)|notes:AGV-40%-share-commoditizing,AMR-22%-fastest-growing,AMR-shipments-547K(2023)-to-2.79M(2030)-25%-CAGR|src:TIA-F1,MordorIntel,MarketsandMarkets]
E[AMR/AGV Market|TAM:$7-9.3B(2025)|CAGR:22%|forecast:$24.5B(2031)|notes:AGV-mature-commoditizing,AMR-fastest-segment,revenue-$18B-to-$124B(2030)|src:TIA-F1,TIA-r2]
E[RaaS Market|TAM:$2.21B(2025)|CAGR:21.2%|forecast:$14.56B(2035)|notes:52%-new-deployments-use-RaaS(2024),64%-companies-using-up-from-46%(2022)|src:TIA-F5,FutureMarketInsights]
E[3PL Market|TAM:$1.2-1.6T(2025)|CAGR:9.7-10.1%|forecast:$2.9-4.3T(2034-35)|notes:tech-segment=24.67%-market-share,labor>40%-opex,margins-net-3-6%|src:EA-F6,GMInsights,GrandView]
E[WFM Software|TAM:$9.36-17.8B(2025)|notes:broader-than-warehouse-specific|src:EA-F1]
E[Digital Twin Market|TAM:$617M(2025)|CAGR:14.5%|forecast:$2.4B(2035)|notes:Siemens+Rockwell-leaders,74.6%-on-premises|src:TIA-F2]
E[Robotics VC Funding|TAM:$6B+-H1-2025|notes:pace-exceeds-2024-$6.1B,$2.26B-Q1-alone,70%+-to-warehouse/logistics,deal-count-DOWN-round-sizes-UP=consolidation|src:TIA-F6]
E[Unified Workforce Economics|TAM:$300-500M(estimated)|notes:NEW-category-between-LMS+WES,created-by-convergence,TIA-estimate-post-DA|src:TIA-DA[#4]]
E[Standalone LMS SAM|TAM:$450-600M(revised)|notes:EA-committed-post-DA,$700M-1B-minus-30-40%-WES-absorption,capital-efficiency-forces-lean-path-$25-35M|src:EA-DA[#4]]

### Market Segments -- Loan Admin (cross-domain)

E[Loan Agency Services|TAM:$10.8B(2024)|CAGR:8.7%|forecast:$22.1B(2033)|src:IntelMarketResearch]
E[Private Credit AUM|TAM:$3.5T(2025)|forecast:$5T(2029)|notes:deployment-+78%-YoY|src:AIMA,Morgan-Stanley]
E[BSL Market|notional:~$5T|notes:Finastra-Loan-IQ=75%-global-volume|src:Finastra]

---

### Key Metrics -- Labor Economics

E[warehouse-labor-pct-opex|value:45-57%|source:MHL-News|date:2025|context:US-warehouses,up-to-65%-fulfillment|confidence:HIGH|src:EA-F3]
E[warehouse-avg-wage-US|value:$18-20/hr(coastal-$22-25)|source:BLS,FRED|date:2025|context:fully-loaded=$25-30/hr|confidence:HIGH|src:EA-research]
E[warehouse-avg-wage-EU|value:€33.5/hr(range-BG-€10.6-to-LU-€55.2)|source:Eurostat|date:2025|confidence:HIGH|src:EA-research]
E[warehouse-avg-wage-APAC|value:$1.50/hr(SEAsia)-$35/hr(AU)|source:industry|date:2025|confidence:HIGH|src:EA-research]
E[warehouse-turnover-rate|value:36-49%/yr(some-100%+)|source:Instawork|date:2025|context:US-warehouses|confidence:HIGH|src:EA-research]
E[warehouse-unfilled-jobs|value:370K+|source:SupplyChainBrain|date:Feb-2025|context:+15%-YoY|confidence:HIGH|src:EA-research]
E[warehouse-cost-per-departure|value:$18.6K|source:Instawork|date:2025|confidence:HIGH|src:EA-F3]
E[warehouse-OT-benchmark|value:5-10%|source:industry|date:2025|context:20%-OT-on-$50M=$15M-extra|confidence:MEDIUM|src:EA-research]
E[warehouse-temp-agency-markup|value:40-45%-typical(avg-62.5%)|source:industry|date:2025|confidence:MEDIUM|src:EA-research]
E[warehouse-wage-inflation|value:7.4%-YoY-2023-2024|source:Amazon-Q1-2025,Instawork|date:2025|context:outpaces-CPI-3.2%|confidence:HIGH|src:EA-research]
E[amazon-wage-floor-effect|value:$22+/hr|source:Amazon-Q1-2025|date:2025|context:$2.2B-wage-hike-sets-regional-floor|confidence:HIGH|src:EA-research]

### Key Metrics -- LMS ROI

E[LMS-productivity-gain|value:10-20%(LMS-alone),20-30%(w/-ELS+perf-mgmt),25-50%(w/-pay-for-perf)|source:Jackpine,TZA,Rebus,BlueYonder|date:2025|confidence:HIGH|src:EA-F3]
E[LMS-ROI-timeline|value:conservative-5-9mo,typical-3-6mo,larger-12-18mo|source:Jackpine,TZA,Rebus|date:2025|confidence:HIGH|src:EA-F3]
E[LMS-annual-labor-reduction|value:8-12%|source:cross-vendor|date:2025|confidence:HIGH|src:EA-F3]
E[LMS-ROI-3PL|value:20-60x|payback:3-6mo|source:Jackpine,TZA,Rebus|date:2025|context:$100M-3PL-saves-$4-9M-on-$80-150K-cost|confidence:HIGH|src:EA-F6]
E[LMS-ROI-case-study-3PL|value:indirect-39%-to-27%=$400K/yr-savings|source:industry|date:2025|confidence:MEDIUM|src:EA-research]
E[vendor-ROI-discount|value:median-customer=60-70%-of-stated-ROI|source:EA-calibration|date:2025|context:use-50%-for-conservative-modeling|confidence:MEDIUM|src:EA-calibration]

### Key Metrics -- Automation Economics

E[robot-vs-human-cost|value:$3-8/hr-vs-$22-40+/hr|source:SCMR,Bain|date:2025|confidence:HIGH|src:EA-F4]
E[RaaS-pricing|value:$1.9-2.2K/mo-industrial|source:Locus,VecnaRobotics|date:2025|context:$499-5K/mo-range,~$4/hr-basic|confidence:HIGH|src:EA-F4,TIA-F5]
E[AMR-payback|value:<24mo-with-250%+-ROI|source:MordorIntel|date:2025|confidence:MEDIUM|src:EA-research]
E[humanoid-robot-speed|value:70-85%-human-speed|source:industry|date:2025|context:mfg-cost-declined-40%-YoY,some-$5.9K|confidence:MEDIUM|src:EA-research]
E[forklift-vs-AMR-cost|value:forklift=$50K/yr(24/7=$200K+),AMR=25-30%-labor-reduction|source:industry|date:2025|confidence:MEDIUM|src:EA-research]
E[mixed-workforce-OPEX-reduction|value:42%-5yr-OPEX-reduction,8mo-payback-augmenting|source:ScienceDirect,Formic|date:2025|confidence:MEDIUM|src:EA-research]
E[human-cobot-team-productivity|value:85%-more-productive-vs-either-alone|source:industry|date:2025|context:the-stat-that-sells-blended-optimization|confidence:MEDIUM|src:PS-F4]
E[Rapyuta-ROI-case|value:13-bots-@$1K/mo+$75K-setup,ROI-positive-month-9,cumulative-$104K-savings-month-18|source:Rapyuta|date:2025|confidence:MEDIUM|src:TIA-F5]

### Key Metrics -- Market Adoption

E[AI-logistics-adoption|value:38%|source:industry|date:2025|context:can-cut-OpEx-up-to-50%|confidence:HIGH|src:TIA-F2]
E[3PL-AI-adoption|value:33.7%(2026,2x-from-2023-16%)|source:industry|date:2025|confidence:MEDIUM|src:PS-F2]
E[robotics-planning-vs-deployment|value:planning-20%-to-30%(growing)-vs-usage-18%-to-10%(declining)|source:MMH-2025|date:2025|context:planning-to-deployment-gap-WIDENING|confidence:HIGH|src:DA[#14d]]
E[warehouse-robotics-plan-by-2026|value:79%|source:industry|date:2025|context:aspirational-not-deployed,DHL-44%-deployed-34%-satisfied|confidence:MEDIUM|src:PS-F2]
E[RaaS-adoption-rate|value:72%-logistics-firms-plan-contracts|source:industry|date:2025|context:1.3M+-deployments-by-2026|confidence:MEDIUM|src:EA-research]
E[AMR-units-deployed-2024|value:200K+|source:industry|date:2024|context:+25%-YoY,contradicts-survey-showing-usage-decline|confidence:MEDIUM|src:DA[#14d]]
E[gamification-adoption-forecast|value:40%-by-2028|source:Gartner|date:2025|confidence:MEDIUM|src:UX-F6]
E[worker-monitoring-rate|value:42%|source:2025-workforce-survey|date:2025|context:LMS-succeeds-commercially-despite-concerns|confidence:HIGH|src:DA[#8]]
E[union-surveillance-contracts|value:38%-address-automated-surveillance|source:industry|date:2025|context:growing-regulatory-surface|confidence:MEDIUM|src:DA[#8]]
E[transport-warehouse-3yr-survival|value:45.7%|source:BLS|date:2025|context:tech-startups-5yr-failure=63%|confidence:HIGH|src:TIA-F6]
E[warehouse-noise-level|value:80-100dB-typical|source:industry|date:2025|context:affects-interface-modality-selection|confidence:HIGH|src:UX-F5]
E[time-to-productivity-warehouse|value:avg-5-6mo-fully-productive,target-2-4wk-basic|source:industry|date:2025|context:good-onboarding-+82%-retention-+70%-productivity|confidence:HIGH|src:UX-F7]
E[Chuck-AMR-onboarding|value:15-min|source:Locus/6RS|date:2025|context:best-in-class-for-AMR|confidence:HIGH|src:UX-F7]
E[AR-glasses-productivity-gain|value:15-25%|source:DHL|date:2025|context:$1500-3000/unit,defer-until-<$500|confidence:MEDIUM|src:UX-F9]
E[ring-scanner-time-reduction|value:50%-scan-time|source:ProGlove|date:2025|confidence:MEDIUM|src:UX-F2]
E[waveless-throughput-gain|value:+40%|source:inVia|date:2025|confidence:MEDIUM|src:TA-F5]
E[waveless-utilization-gain|value:+20%|source:inVia|date:2025|confidence:MEDIUM|src:TA-F5]
E[Amazon-FC-Games|value:expanded-20+-states|source:Amazon|date:2025|context:gamification,injury-rate-scrutiny|confidence:HIGH|src:UX-F6]
E[Kenco-gamification-productivity|value:3-5%|source:Kenco|date:2025|confidence:MEDIUM|src:UX-F6]
E[worker-automation-sentiment|value:85%-positive,90%-trust|source:Locus(vendor-reported,biased-upward)|date:2025|confidence:LOW|src:UX-F3]

### Key Metrics -- LMS Pricing

E[LMS-SaaS-pricing|value:$100-500/user/mo(entry-$100,mid-$167-avg,enterprise-$400-500+)|source:ExploreWMS,ShipHero,LogiMax|date:2025|confidence:MEDIUM-HIGH|src:EA-F7]
E[LMS-enterprise-license|value:$250K-$1M/facility|source:industry|date:2025|confidence:MEDIUM|src:EA-F7]
E[LMS-contract-value-mid|value:$50-150K/yr|source:industry|date:2025|confidence:MEDIUM|src:EA-F2]
E[LMS-contract-value-enterprise|value:$500K-2M/yr|source:industry|date:2025|confidence:MEDIUM|src:EA-F2]
E[LMS-contract-value-3PL|value:$30-80K/facility|source:industry|date:2025|confidence:MEDIUM|src:EA-F2]
E[Manhattan-LMS-pricing|value:$500K-2M(bundled-with-WMS)|source:industry|date:2025|confidence:MEDIUM|src:EA-F7]
E[Easy-Metrics-pricing|value:$100-300K|source:industry|date:2025|confidence:MEDIUM|src:EA-F7]
E[Blue-Yonder-implementation|value:$500K+|source:industry|date:2025|context:enterprise-only,structural-pricing-gap-vs-mid-market|confidence:HIGH|src:PS-DA[#2]]

### Key Metrics -- Talent

E[triple-threat-salary|value:$200-350K|source:industry|date:2025|context:AI+robotics+logistics-intersection,6-12mo-to-assemble-8-12-core-team|confidence:HIGH|src:TIA-F7]
E[warehouse-engineering-team-cost|value:$2-4M/yr-fully-loaded-US|source:industry|date:2025|context:offshore-viable-for-platform-not-domain-integration|confidence:HIGH|src:TIA-F7]
E[warehouse-floor-openings|value:320K+|source:AutomationAlley,Hirecruiting|date:Dec-2024-to-Apr-2025|confidence:HIGH|src:TIA-F7]
E[reskilling-need|value:50%-need-reskilling-for-automation|source:industry|date:2025|confidence:MEDIUM|src:TIA-F7]

### Key Metrics -- Capital/Investment

E[LMS-startup-capital-to-breakeven|value:$25-35M(lean)-to-$40-65M(full)|source:EA-analysis|date:2025|context:lean-path-required-per-SAM-revision|confidence:MEDIUM|src:EA-F5,EA-DA[#4]]
E[LMS-startup-MVP-cost|value:$3-5M(human-only-10-12mo)|source:TA-analysis|date:2025|context:revised-from-$5-8M-after-DA|confidence:MEDIUM|src:TA-DA[#7]]
E[LMS-startup-seed-round|value:$4-6M(2025-Carta-median)|source:Carta|date:2025|context:gets-to-MVP-only,Series-A-required-before-revenue|confidence:HIGH|src:PS-DA[#5]]
E[LMS-founding-to-revenue|value:24-30mo|source:EA-analysis|date:2025|context:founding-to-$1M-ARR,revised-from-12-18mo|confidence:MEDIUM|src:EA-DA[#5]]
E[LMS-founding-to-breakeven|value:5-6yr|source:EA-analysis|date:2025|context:revised-from-4-5yr|confidence:MEDIUM|src:EA-DA[#5]]
E[LMS-startup-EV|value:2.2x-gross,1.0-1.3x-net-at-base-rate|source:EA-analysis|date:2025|context:MARGINAL,requires-above-average-survival|confidence:MEDIUM|src:EA-DA[#3]]
E[LMS-exit-range|value:strategic-$200-500M(6-10x),PE-$500M-1B,IPO-8-15x|source:EA-F8|date:2025|confidence:MEDIUM|src:EA-F8]
E[Easy-Metrics-valuation-estimate|value:$180-500M|source:PS-analysis|date:2025|context:3-5x-on-$60-100M-implied-ARR,not-startup-acquirable|confidence:MEDIUM|src:PS-DA[#10]]

---

### Relationships -- Competition

R[Blue Yonder|competes-with|Manhattan Associates|segment:enterprise-WMS+LMS+WES|intensity:direct]
R[Blue Yonder|competes-with|Locus Robotics|segment:robot-orchestration|intensity:indirect|notes:BY-vendor-agnostic-vs-Locus-own-robots-only]
R[Blue Yonder|competes-with|SAP|segment:enterprise-WMS|intensity:direct]
R[Blue Yonder|competes-with|Oracle|segment:enterprise-WMS|intensity:direct]
R[Manhattan Associates|competes-with|SAP|segment:enterprise-WMS|intensity:direct]
R[Manhattan Associates|competes-with|Oracle|segment:enterprise-WMS|intensity:direct]
R[Easy Metrics|competes-with|Takt|segment:standalone-LMS-mid-market|intensity:direct]
R[Easy Metrics|competes-with|Rebus|segment:standalone-LMS|intensity:direct]
R[Locus Robotics|competes-with|6 River Systems|segment:AMR-collaborative-picking|intensity:direct]
R[Locus Robotics|competes-with|Geek+|segment:AMR-goods-to-person|intensity:direct]
R[Locus Robotics|competes-with|GreyOrange|segment:robotic-orchestration|intensity:indirect]
R[Symbotic|competes-with|AutoStore|segment:warehouse-automation-systems|intensity:indirect|notes:different-automation-paradigms]
R[Boston Dynamics|competes-with|Locus Robotics|segment:warehouse-robotics|intensity:indirect|notes:different-robot-types]
R[Vecna Robotics|competes-with|Locus Robotics|segment:AMR|intensity:direct]
R[Honeywell|competes-with|Lucas Systems|segment:voice-directed-picking|intensity:direct]
R[Figure|competes-with|Apptronik|segment:humanoid-robots|intensity:direct|notes:both-pre-commercial]
R[Robotics Hub|competes-with|LocusONE|segment:robot-fleet-orchestration|intensity:direct|notes:BY-vendor-agnostic-vs-Locus-proprietary]
R[Robotics Hub|competes-with|GreyMatter|segment:robot-orchestration|intensity:indirect]
R[Robotics Hub|competes-with|Orbit|segment:fleet-management|intensity:indirect|notes:BD-fleet-only-not-labor]
R[Active Labor Management|competes-with|ProTrack LMS|segment:LMS|intensity:indirect|notes:embedded-vs-standalone]
R[LocusINTELLIGENCE|competes-with|Active Labor Management|segment:labor-optimization|intensity:indirect|notes:robotics-up-vs-WMS-down]
R[WES|disrupts|Warehouse LMS|mechanism:absorbing-LMS-functions-from-above|timeline:medium-term|severity:significant|notes:WES-@18%-CAGR-eating-standalone-LMS-TAM]
R[WES|disrupts|WCS|mechanism:absorbing-WCS-functions-from-below|timeline:near-term|severity:significant]

### Relationships -- Acquisitions

R[Easy Metrics|acquired|TZA/ProTrack|date:May-2025|notes:standalone-LMS-consolidation]
R[Symbotic|acquired|Walmart ASR|date:Jan-2025|price:$200M+$350M-contingent+$520M-dev|notes:42-Walmart-DCs,12yr-exclusive]
R[Symbotic|acquired|Fox Robotics|date:2025|notes:pallet-handling]
R[Ocado|acquired|6 River Systems|date:2023|from:Shopify|notes:now-Ocado-Intelligent-Automation]
R[Zebra Technologies|acquired|Fetch Robotics|date:pre-2025|notes:AMR-integration]
R[Zebra Technologies|acquired|Photoneo|date:2025|notes:3D-vision]
R[Rockwell Automation|acquired|Clearpath Robotics|date:pre-2025|notes:autonomous-vehicles]
R[Toyota Industries|acquired|Vanderlande|date:pre-2025|notes:material-handling]
R[KION Group|acquired|Dematic|date:pre-2025|notes:warehouse-automation]
R[ABB|acquired|ASTI Mobile Robotics|date:pre-2025|notes:AMR]
R[Oakley Capital|acquired|GLAS|date:Jan-2026|price:$1.35B(43x-revenue)|notes:La-Caisse-minority-stake]
R[Cinven|acquired|Alter Domus|date:Mar-2024|price:€4.9B-EV|notes:PE-playbook]

### Relationships -- Investments

R[Insight Partners|invests-in|Locus Robotics|amount:undisclosed|round:multiple]
R[Insight Partners|invests-in|Hypercore|amount:$13.5M|date:Feb-2026|round:Series-A|lead:true]
R[SVB|invests-in|Legion Technology|amount:$50M|date:Dec-2024]
R[Woven Capital|invests-in|robotics-startups|amount:$200M-fund|notes:Toyota-affiliated]

### Relationships -- Partnerships

R[Manhattan Associates|partners-with|Agility Robotics|type:technology|since:Apr-2024|scope:humanoid-integration]
R[Rebus|partners-with|Legion Technology|type:technology|scope:LMS+WFM-integration]
R[Berkshire Grey|partners-with|Locus Robotics|type:technology|scope:picking-systems+AMR]
R[Boston Dynamics|partners-with|DHL|type:strategic|scope:Stretch-1000+-unit-MOU]
R[Siemens|partners-with|AI-robotics-partner|type:technology|since:Feb-2026|scope:virtual-warehouse-trials]

### Relationships -- Technology Integration

R[Robotics Hub|integrates-with|VDA 5050|method:native|depth:deep|notes:primary-interop-standard]
R[Robotics Hub|integrates-with|MassRobotics AMR Interop|method:native|depth:deep]
R[Active WM|integrates-with|Manhattan Automation Network|method:native|depth:deep|notes:robotics-via-Automation-Network]
R[SAP EWM|integrates-with|SAP|method:native|depth:deep|notes:ERP-captive-OData]
R[LocusONE|uses-technology|patent-pending-AI|how:human+robot-coordination|depth:core]
R[Chuck|uses-technology|collaborative-picking|how:robot-leads-picker-model|depth:core]

### Relationships -- Product-Methodology

R[Active Labor Management|employs-methodology|MOST|how:ELS-engine-task-timestamp-vs-standard|phase:core]
R[Robotics Hub|employs-methodology|ML-forecasting|how:AI/ML-forecasting+dynamic-adjustment|phase:core]
R[ProTrack LMS|employs-methodology|MOST|how:engineered-labor-standards|phase:core]

### Relationships -- Segment Serving

R[Robotics Hub|serves-segment|Warehouse LMS|tier:primary|pricing:$500K+]
R[Robotics Hub|serves-segment|Warehouse WES|tier:primary|pricing:$500K+]
R[Active Labor Management|serves-segment|Warehouse LMS|tier:primary|pricing:$500K-2M-bundled]
R[ProTrack LMS|serves-segment|Warehouse LMS|tier:primary|pricing:$100-300K]
R[Takt|serves-segment|Warehouse LMS|tier:primary|pricing:SaaS-entry|notes:3PL/B2C/D2C]
R[LocusONE|serves-segment|AMR/AGV Market|tier:primary|pricing:RaaS]
R[LocusINTELLIGENCE|serves-segment|Warehouse LMS|tier:secondary|notes:robotics-up-into-LMS]
R[Momentum WES|serves-segment|Warehouse WES|tier:primary]
R[GreyMatter|serves-segment|Warehouse Robotics|tier:primary]

### Relationships -- Supply/Customer

R[Symbotic|supplies-to|Walmart|product:warehouse-automation|volume:42-DCs|significance:exclusive-12yr-$5B+-potential]
R[Boston Dynamics|supplies-to|DHL|product:Stretch|volume:1000+-units-MOU]
R[Boston Dynamics|supplies-to|Lidl|product:Stretch|volume:EU-rollout-2026]
R[Boston Dynamics|supplies-to|Otto Group|product:Stretch|volume:20+-facilities]
R[Locus Robotics|supplies-to|multiple-3PLs|product:AMR|volume:6B+-picks-total]
R[Vecna Robotics|supplies-to|FedEx|product:AMR]
R[Vecna Robotics|supplies-to|GEODIS|product:AMR]
R[Vecna Robotics|supplies-to|Caterpillar|product:AMR]

### Relationships -- Platform Bundling

R[Active WM|bundles-with|Active Labor Management|coupling:tight|pricing-impact:LMS-included-in-WMS-license|notes:enterprise-lock-in]
R[SAP EWM|bundles-with|SAP-ERP|coupling:tight|pricing-impact:ERP-captive]
R[Blue Yonder|bundles-with|Robotics Hub|coupling:tight|pricing-impact:WMS+WES+LMS+WFM-suite|notes:DA-confirmed-WMS-agnostic-for-Robotics-Hub]

### Relationships -- Cross-Domain (Loan Admin)

R[Alter Domus|competes-with|GLAS|segment:loan-agency|intensity:direct]
R[Alter Domus|competes-with|Kroll|segment:loan-agency|intensity:direct]
R[Hypercore|competes-with|Alter Domus|segment:private-credit-admin-SaaS|intensity:indirect|notes:most-direct-but-most-acquirable]
R[Finastra|supplies-to|BSL Market|product:Loan-IQ|volume:75%-global-syndicated]

---

### Analytical Findings (from sigma-review r2)

## Key Thesis: Warehouse LMS Venture Assessment

### r1 Thesis
"Build unified human+robot LMS into UNOCCUPIED market. $719M->$3.72B TAM. $5-8M MVP in 18mo."

### r2 Thesis (DA-revised)
"Build human-only workforce economics LMS (WMS-agnostic, mid-market priced) into CONTESTED market. Robot integration=phase-2 when market demands it. $3-5M MVP in 10-14mo. SAM=$400-550M (shrinking from WES squeeze). EV=marginal at base rate (2.2x gross). Requires above-average execution, founder-market fit, and lean capital ($25-35M total)."

### Key Strategic Patterns Discovered
E[PINCER-PROBLEM|type:analytical-pattern|description:large-deployers-HAVE-BY/Manhattan+mid-market-DOESNT-NEED-mixed-workforce-yet|implication:must-compete-enterprise-vs-BY-OR-human-only-floor+robot-ceiling|src:TIA-DA[#14d]+DA[#1]]
E[WES-SQUEEZE|type:analytical-pattern|description:WES-@18%-CAGR-absorbing-LMS-from-above+WCS-from-below|implication:standalone-LMS-TAM-shrinking-not-growing|src:TIA-F3]
E[ORCHESTRATION-vs-ECONOMICS|type:analytical-pattern|description:orchestration-gaps-close-fast(BY-already-shipping)+economics-gaps-take-longer(cost-per-unit-engine)|implication:differentiate-on-economics-not-orchestration|src:TIA-r2]
E[PLANNING-DEPLOYMENT-GAP|type:analytical-pattern|description:AMR/AGV-planning-grows(20-30%)-while-usage-declines(18-10%)|implication:mixed-workforce-demand-may-be-3-5yr-premature-for-mid-market|src:DA[#14d]]
