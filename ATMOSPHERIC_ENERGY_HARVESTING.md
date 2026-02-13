# Distributed Atmospheric Electrical Energy Harvesting:
# A Multi-Modal Framework for Earth, Mars, and Lunar Environments

## Research Proposal & Technical Analysis

---

**Author:** Mackenzie C. J. Clark  
**Organization:** Lycheetah Foundation  
**Date:** February 2026  
**Status:** Exploratory Research Proposal  
**License:** MIT — Open for collaboration  

---

## Abstract

We propose a distributed multi-modal system for harvesting electrical energy from atmospheric charge dynamics. Unlike prior work focused on single-strike lightning capture (which faces fundamental impedance-matching and timing challenges), our approach operates across three complementary harvesting modes that adapt to atmospheric conditions: (1) continuous corona-point field harvesting from the fair-weather atmospheric electric field, (2) electromagnetic induction from storm-cell motion across buried loop arrays, and (3) capacitive ground-plane coupling to pre-strike electric fields. We additionally propose a fourth novel mode: electrostatic dust-charge harvesting, which has unique applicability to Martian and Lunar environments where triboelectric dust charging is extreme.

The system is designed to self-organize between modes based on measured atmospheric state, scaling energy capture across six orders of magnitude from fair-weather trickle (microwatts) to storm-mode harvest (watts to kilowatts). We present the underlying physics for each mode, first-order power estimates, engineering challenges, and specific adaptations for Earth, Mars, and the Moon.

This is not a claim of solved engineering. It is a structured identification of the opportunity space, with honest physics and falsifiable predictions, intended to invite collaboration.

---

## 1. Motivation

### 1.1 The Wasted Charge Problem

Earth's atmosphere is a continuously operating electrical machine. The global atmospheric electric circuit maintains a potential difference of approximately 250 kV between the ionosphere and the surface, driving a total current of ~1,000-2,000 A through the atmosphere at all times. The total power of this circuit is approximately 250-500 MW [Rycroft et al., 2000].

This energy currently dissipates entirely into ground heating. No significant infrastructure exists to harvest it.

Simultaneously, lightning protection systems on buildings, transmission towers, and industrial facilities are specifically designed to *waste* the energy of lightning strikes — conducting it harmlessly to ground where it becomes heat. The global lightning flash rate is approximately 44 ± 5 flashes per second [Christian et al., 2003], each carrying 1-5 GJ of total energy. Even the ~250 kWh that reaches the ground per strike is deliberately discarded.

### 1.2 Why Prior Approaches Failed

**Direct lightning capture** has been attempted and abandoned [AEHI, 2007]. The fundamental problems are:

- **Temporal mismatch:** A strike delivers its energy in 1-100 microseconds. No affordable storage technology can absorb gigawatt-scale power for microsecond durations without destruction.
- **Spatial unpredictability:** Lightning strike locations are stochastic within a storm cell footprint. Fixed infrastructure cannot guarantee intercept.
- **Impedance catastrophe:** The source impedance of a lightning channel (~1 Ω) is mismatched by 6+ orders of magnitude against any practical load or storage system.

These are not engineering problems that scale away with investment. They are physics constraints.

### 1.3 The Reframe: Harvest the Field, Not the Bolt

Our central insight: **lightning is the least harvestable form of atmospheric electrical energy**. The same storm system that produces one bolt also maintains an electric field of 1,000-10,000 V/m across kilometres of ground for minutes to hours. The fair-weather atmosphere maintains 100-150 V/m continuously.

These fields represent harvestable energy at manageable power densities and timescales. The question is not "how do we catch lightning?" but "how do we efficiently couple to atmospheric electric fields across a range of conditions?"

---

## 2. The Earth's Atmospheric Electric Circuit

### 2.1 Fair-Weather Field

In the absence of storms, the atmospheric electric field near the surface is approximately:

```
E_fair ≈ 100-150 V/m  (pointing downward, surface negative relative to ionosphere)
```

This field drives a continuous "fair-weather current" of ~1-3 pA/m² (picoamps per square metre) through the weakly conducting atmosphere. The source of this field is the global thunderstorm activity, which acts as a charge pump maintaining the ionosphere-surface potential difference.

**Diurnal variation:** The fair-weather field follows the "Carnegie curve," peaking around 19:00 UTC when global thunderstorm activity (dominated by African and South American convection) is maximum.

**Urban modification:** Urban environments have enhanced fair-weather fields (~1.15-1.4× rural values) due to:
- Pollution increasing atmospheric conductivity
- Building geometries concentrating field lines
- Waste heat creating convective ion transport
- Electromagnetic pollution from power infrastructure

### 2.2 Storm Approach Phase

As a thunderstorm approaches, the surface electric field undergoes dramatic changes:

```
Phase 1 (fair weather):     E ≈ +130 V/m  (normal downward field)
Phase 2 (storm approach):   E → 0 V/m     (field reversal begins)
Phase 3 (overhead storm):   E ≈ -1,000 to -10,000 V/m  (inverted, strong)
Phase 4 (pre-strike):       E ≈ -5,000 to -30,000 V/m  (peak before discharge)
Phase 5 (post-strike):      E collapses, then rebuilds
Phase 6 (storm departure):  E returns to fair-weather values
```

**Critical observation:** Phase 3-4 lasts minutes to tens of minutes. The energy stored in the field during this phase is distributed across the entire storm footprint (5-50 km²). This is the primary harvest window.

### 2.3 Energy Density of the Atmospheric Field

The electrostatic energy density of an electric field is:

```
u = ½ε₀E²

Fair weather:  u = ½ × 8.854e-12 × (130)²     ≈ 7.5 × 10⁻⁸ J/m³
Storm phase:   u = ½ × 8.854e-12 × (5,000)²    ≈ 1.1 × 10⁻⁴ J/m³
Pre-strike:    u = ½ × 8.854e-12 × (30,000)²   ≈ 4.0 × 10⁻³ J/m³
```

This appears tiny per cubic metre. But integrated over a 100m column above a 1 km² area:

```
Fair weather:  E_total = 7.5e-8 × 100 × 1e6 = 7.5 J      (across 1 km², 100m column)
Storm phase:   E_total = 1.1e-4 × 100 × 1e6 = 11,000 J    (3 Wh)
Pre-strike:    E_total = 4.0e-3 × 100 × 1e6 = 400,000 J   (111 Wh)
```

A storm phase lasting 30 minutes over 1 km² represents approximately 3-100 Wh of harvestable field energy. Not grid-scale, but absolutely meaningful for distributed IoT, sensors, and emergency systems.

---

## 3. Mode 1: Corona-Point Field Harvesting

### 3.1 Principle

A sharp metallic point in an electric field concentrates the field at its tip. When the local field exceeds the breakdown threshold of air (~30 kV/cm at sea level), corona discharge occurs — ions are generated at the tip and drift toward the opposite polarity.

In the atmospheric electric field, a grounded pointed conductor generates a continuous corona current that flows from the atmosphere through the point to ground. By inserting a load impedance in this path, electrical power can be extracted.

### 3.2 Physics

**Corona onset condition:**

```
E_tip = E_atm × β

Where:
E_atm = ambient atmospheric field (V/m)
β = geometric enhancement factor (typically 100-10,000 for sharp points)
E_tip > 3 × 10⁶ V/m for corona onset in air at STP
```

For a needle with β = 1,000, corona onset occurs when:

```
E_atm > 3 × 10⁶ / 1,000 = 3,000 V/m
```

This means corona onset requires storm-level fields for a single point. However, arrays of many moderately sharp points (β ≈ 100-500) with elevated geometry (10-50m towers) can achieve corona onset at much lower field strengths:

```
E_atm > 3 × 10⁶ / (500 × height_factor)
```

Where height_factor accounts for the fact that the atmospheric field increases with altitude (roughly linearly in the first 100m).

**Current output:**

```
I_corona = k × (V - V_onset)

Where:
k = geometric constant (depends on point geometry and spacing)
V = applied voltage (= E × height for atmospheric field)
V_onset = corona onset voltage

Typical values: 0.1-10 μA per point in fair weather
                1-1000 μA per point in storm approach
```

### 3.3 Power Estimate

For a single elevated point collector (10m height):

```
Fair weather:   V = 130 × 10 = 1,300 V;  I ≈ 0.1 μA  →  P ≈ 0.13 μW
Storm approach: V = 5,000 × 10 = 50,000 V; I ≈ 100 μA →  P ≈ 5,000 μW = 5 mW
Pre-strike:     V = 20,000 × 10 = 200,000 V; I ≈ 1 mA  →  P ≈ 200 W (brief)
```

**Array scaling:** 100 points on a building rooftop:

```
Fair weather:   100 × 0.13 μW = 13 μW    (powers one IoT sensor)
Storm approach: 100 × 5 mW = 500 mW      (charges a phone in 10 hours)
Pre-strike:     100 × 200 W = 20 kW      (brief pulse, seconds only)
```

### 3.4 Engineering Challenges

1. **Impedance matching:** Corona sources are extremely high impedance (megaohms to gigaohms). Efficient power extraction requires specialized conversion circuits.
2. **Corrosion:** Corona discharge produces ozone and NOx, which corrode the collector points. Material science challenge.
3. **Safety:** Elevated conductors in storm fields attract lightning. The collector system must integrate with lightning protection, not replace it.
4. **Variability:** Output varies by 6+ orders of magnitude between fair weather and storm. Power management must handle this dynamic range.

### 3.5 Current State of the Art

Corona discharge energy harvesting from high-voltage transmission lines has been demonstrated in laboratory settings [Gu et al., 2025]. The physics is validated. The atmospheric application is uncharted but uses identical principles — the atmosphere provides the high-voltage field instead of a man-made conductor.

---

## 4. Mode 2: Inductive Storm-Motion Harvesting

### 4.1 Principle

This is the most novel and least explored approach.

When a charged thunderstorm cell moves across the landscape, it carries its charge distribution with it. This charge induces image charges on the ground surface below. As the storm moves, the image charges move — and moving charge is current.

A buried conductive loop experiences this moving charge as a time-varying magnetic flux. By Faraday's law, this induces an electromotive force (EMF) in the loop.

### 4.2 Physics

**Faraday's law:**

```
EMF = -dΦ_B/dt

Where:
Φ_B = ∫∫ B · dA  (magnetic flux through loop)
```

The storm-induced ground current density can be estimated from the displacement current:

```
J_displacement = ε₀ × dE/dt

For a storm moving at v = 40 km/h ≈ 11 m/s:
dE/dt ≈ ΔE × v / L_storm

Where ΔE = field change across storm edge (~5,000 V/m)
      L_storm = storm cell diameter (~5 km)

dE/dt ≈ 5,000 × 11 / 5,000 = 11 V/(m·s)

J_displacement = 8.854e-12 × 11 ≈ 10⁻¹⁰ A/m²
```

This displacement current is tiny. However, the storm also drives *conduction currents* through the ground, which are much larger (ground conductivity >> atmospheric conductivity):

```
J_ground = σ_ground × E_horizontal

Where σ_ground ≈ 0.01 S/m (typical soil)
      E_horizontal ≈ 10-100 V/m (horizontal component of storm field)

J_ground ≈ 0.01 × 50 = 0.5 A/m²
```

**This is orders of magnitude larger than the atmospheric displacement current.** Buried loops couple to the ground conduction current, not the atmospheric displacement current.

### 4.3 Power Estimate

For a buried loop array (100m × 100m, 10 turns):

```
Flux change: ΔΦ ≈ μ₀ × J_ground × A × N
Where A = 10,000 m², N = 10 turns

This is complex to compute precisely (requires numerical field modelling).
Order-of-magnitude estimate:

EMF ≈ 0.1 - 10 V (over storm transit time of ~5-15 minutes)
I ≈ EMF / R_loop

For R_loop ≈ 1 Ω (heavy copper):
P ≈ V²/R ≈ 0.01 - 100 W during storm transit
```

### 4.4 Advantages

- **No atmospheric exposure:** Entirely underground. No lightning risk. No corrosion.
- **No moving parts:** Purely electromagnetic induction.
- **Storm-scale integration:** Captures energy from the *motion* of the storm, not individual strikes.
- **Complementary timing:** Produces power during storm transit when solar is unavailable.

### 4.5 Engineering Challenges

1. **Signal extraction:** The EMF is small and slow-varying. Requires sensitive, low-noise electronics.
2. **Ground noise:** Buried loops will pick up interference from power lines, railways, and geological telluric currents. Signal processing required.
3. **Installation cost:** Burying large loop arrays is expensive. Best integrated with new construction (foundations, parking structures, agricultural drainage).
4. **Modelling requirement:** Optimal loop geometry depends on local soil conductivity and storm climatology. Site-specific design needed.

### 4.6 Research Gap

Helman (2011, 2020) proposed buried inductors for lightning energy harvesting but did not publish detailed power estimates or experimental validation. The concept of harvesting *storm motion* (rather than strike energy) via ground conduction currents appears to be novel.

---

## 5. Mode 3: Capacitive Ground-Plane Coupling

### 5.1 Principle

A large conductive surface, insulated from the ground, with a second conductor beneath it, forms a parallel-plate capacitor with the atmosphere above providing the electric field that charges it.

Unlike direct lightning capture, this approach is designed to couple to the *distributed field* of a storm, not to a concentrated strike channel. The geometry is optimised for field coupling and against strike attraction (rounded edges, no sharp points, controlled height).

### 5.2 Physics

**Capacitance of ground plane:**

```
C = ε₀ × A / d

Where:
A = plate area (m²)
d = plate separation (m) — distance from plate to ground return
```

**Charge stored from atmospheric field:**

```
Q = C × V_atm

Where V_atm = E × h (atmospheric voltage at plate height h)
```

**Energy stored:**

```
W = ½CV²
```

**Example:** 100 m² plate at 10m height, 1m plate separation:

```
C = 8.854e-12 × 100 / 1 = 885 pF

Fair weather:   V = 130 × 10 = 1,300 V    → W = ½ × 885e-12 × 1,300² = 0.75 μJ
Storm field:    V = 5,000 × 10 = 50,000 V  → W = ½ × 885e-12 × 50,000² = 1.1 J
Pre-strike:     V = 20,000 × 10 = 200,000 V → W = ½ × 885e-12 × 200,000² = 17.7 J
```

### 5.3 Continuous Power via Switched Discharge

The key to extracting continuous power is to repeatedly charge and discharge the capacitor through a load. If the atmospheric field recharges the capacitor in time τ_charge, the average power is:

```
P_avg = W / τ_charge

For storm conditions with active field maintenance:
τ_charge ≈ 1-10 seconds (field replenishes charge lost to discharge)

P_avg ≈ 1.1 J / 5 s = 0.22 W per 100 m² plate
```

An array of 10 such plates (total 1,000 m²):

```
P_array ≈ 2.2 W during storm conditions
```

### 5.4 Dual-Purpose: Energy Harvesting + Lightning Protection

Every large building already has a lightning protection system: a network of conductors that shunt strike energy to ground. Currently this energy is 100% wasted.

**Proposal:** Integrate supercapacitor banks into the ground path of existing lightning protection systems. The surge arrestor limits voltage to protect the capacitors. Even capturing 0.1% of a strike's ground-path energy through a properly designed surge-capacitor circuit yields:

```
E_captured = 0.001 × 250 kWh × 3.6e6 J/kWh = 900 J per strike

If a building takes ~10 strikes per year:
E_annual = 9,000 J ≈ 2.5 Wh
```

This is modest per building but interesting at city scale, and the infrastructure *already exists*. The marginal cost is the supercapacitor bank and control electronics.

### 5.5 Engineering Challenges

1. **Dielectric breakdown:** The atmosphere between the plate and ground must not arc. Plate geometry must be carefully designed with adequate clearances.
2. **Weather exposure:** Large exposed conductive surfaces in storms require robust construction.
3. **Voltage regulation:** Output voltage varies enormously. Power electronics must handle kV-range input and produce stable low-voltage output.
4. **Economics:** Large plate areas required for meaningful power. Best integrated with existing large structures (rooftops, car parks, solar panel frames).

---

## 6. Mode 4 (Novel): Electrostatic Dust-Charge Harvesting

### 6.1 The Dust Opportunity

This is the novel contribution of this proposal, with direct applicability to Mars and the Moon.

**On Earth:** Windblown dust is triboelectrically charged. Sandstorms, volcanic ash plumes, and even normal agricultural dust carry significant charge. This is a nuisance in conventional engineering (static discharge causes fires, explosions, equipment damage). We propose to harvest it.

**On Mars:** This is where the physics gets extraordinary.

### 6.2 Mars: The Triboelectric Planet

Mars has an atmosphere that is perfect for triboelectric charging and terrible for dissipating it:

- **Atmospheric pressure:** ~600 Pa (0.6% of Earth). Low pressure means low breakdown voltage — charge accumulates more easily and discharges less frequently.
- **Atmospheric composition:** 95% CO₂, very dry. No humidity to dissipate static.
- **Dust storms:** Mars experiences global dust storms lasting months. The dust is iron-rich (magnetic) and silicate-based — materials at opposite ends of the triboelectric series.
- **Measured atmospheric electric fields:** Mars atmospheric electricity is predicted to reach 5-25 kV/m during dust storms, comparable to Earth thunderstorm fields [Farrell et al., 2004].
- **Dust devil electrocharging:** Martian dust devils have been modelled to generate fields of 2-20 kV/m [Melnik & Parrot, 1998].

**The critical difference from Earth:** On Mars, there is no liquid water cycle to drive convective thunderstorm charging. The primary charge separation mechanism is *triboelectric dust interaction*. The entire atmospheric electrical machine on Mars is dust-driven.

### 6.3 Martian Dust-Charge Harvester Design

**Concept:** A passive structure with alternating triboelectric materials (iron oxide / silicate) arranged as vanes or fins. Wind-driven dust contacts these surfaces, deposits charge of opposite polarity on alternate vanes, and the resulting potential difference is harvested.

**Advantages for Mars:**
- No moving parts (critical for Mars reliability)
- Self-cleaning (wind removes accumulated dust from smooth surfaces)
- Scales with storm intensity (more dust = more power)
- Works during dust storms when *solar panels fail* (this is the key selling point)

Mars's biggest energy vulnerability is dust storms obscuring solar panels for weeks to months. A triboelectric harvester that *increases* output during dust storms directly addresses the primary failure mode of Martian solar power.

**Power estimate (speculative but physics-based):**

```
Charge deposition rate: ~1-10 μC/m² per minute during dust event
Collection area: 10 m²
Voltage: ~1,000-10,000 V (from charge separation on insulated surfaces)
Power: ~0.01-1 W during active dust event
```

This is supplementary, not primary power — but during a dust storm it may be the *only* available power source.

### 6.4 Lunar Application: Regolith Charge Harvesting

The Moon has no atmosphere, but it has a severe triboelectric charging problem:

- **Solar wind charging:** The dayside lunar surface accumulates positive charge from solar wind proton flux. Potential: +5 to +10 V.
- **Photoelectric emission:** UV photons eject electrons from the surface. This creates a positively charged surface and an electron sheath above it.
- **Terminator zone:** At the day-night boundary, extreme potential gradients exist (~100 V over metres).
- **Dust levitation:** Electrostatically charged dust levitates above the lunar surface near the terminator, reaching heights of kilometres.

**Harvest concept:** Vertical conductor arrays placed in the terminator zone to intercept the potential gradient between photoelectrically charged dayside and electron-accumulated nightside. The Moon's terminator sweeps around the surface every 29.5 days, but a fixed installation at a pole could experience nearly continuous terminator-zone conditions.

This is highly speculative but the physics of lunar electrostatic charging is well-documented [Stubbs et al., 2006].

---

## 7. Integrated System Architecture

### 7.1 Mode Switching via Atmospheric State Detection

The four harvesting modes operate optimally under different conditions:

| Condition | Mode 1 (Corona) | Mode 2 (Induction) | Mode 3 (Capacitive) | Mode 4 (Dust) |
|-----------|-----------------|--------------------|--------------------|---------------|
| Fair weather | Trickle | Off | Trickle | Low |
| Storm approach | Rising | Onset | Charging | Rising |
| Active storm | High | Peak | Peak | Peak |
| Pre-strike | Maximum (brief) | Steady | Maximum (brief) | High |
| Post-strike | Collapse/rebuild | Declining | Discharge/rebuild | Steady |
| Dust event (no storm) | Low | Off | Low | Peak |

**Self-organising network:** Each node in the distributed network measures:
- Electric field strength (E-field mill sensor)
- Electric field rate of change (dE/dt)
- Atmospheric conductivity
- Wind speed and direction
- Dust/particulate density

Based on these measurements, each node selects its optimal harvesting mode and reports its state to neighbours. The network collectively maps the atmospheric electrical environment in real time.

### 7.2 Storage Architecture

**Multi-stage storage:**

```
Stage 1: Ceramic capacitors (fast response, handles strike transients)
         τ ≈ microseconds, C ≈ nF, V ≈ kV

Stage 2: Supercapacitors (medium-term, absorbs storm harvest)
         τ ≈ seconds-minutes, C ≈ F, V ≈ 5V

Stage 3: LiFePO₄ battery (long-term, provides steady output)
         τ ≈ hours-days, Q ≈ Ah, V ≈ 3.2V
```

The three-stage cascade handles the enormous dynamic range: Stage 1 absorbs microsecond transients and trickle-feeds Stage 2. Stage 2 absorbs storm-duration energy and trickle-feeds Stage 3. Stage 3 provides steady power output.

### 7.3 Communication and Coordination

Each harvesting node doubles as an atmospheric electrical sensor. The network produces:
- Real-time atmospheric electric field maps
- Storm tracking and movement prediction
- Lightning strike probability forecasting
- Dust storm monitoring (Mars application)

This data has independent value for weather services, aviation safety, and scientific research — potentially exceeding the value of the harvested energy itself.

---

## 8. Comparative Analysis: Earth, Mars, Moon

| Parameter | Earth | Mars | Moon |
|-----------|-------|------|------|
| Atmospheric pressure | 101 kPa | 0.6 kPa | ~0 (vacuum) |
| Fair-weather E-field | 100-150 V/m | Unknown (~5-15 V/m predicted) | N/A |
| Storm E-field | 1-30 kV/m | 5-25 kV/m (dust storms) | N/A |
| Primary charge mechanism | Convective (water cycle) | Triboelectric (dust) | Photoelectric + solar wind |
| Dielectric breakdown | ~30 kV/cm | ~2 kV/cm (low pressure) | Infinite (vacuum) |
| Storm frequency | ~1,800 active at any time | Seasonal global storms | N/A (terminator is "storm") |
| Dust charging | Moderate | Extreme | Extreme (UV-driven) |
| Best harvesting mode | Corona + Capacitive | Dust-charge | Terminator potential gradient |
| Available infrastructure | Lightning rods, buildings | Habitat structures | Lander/base structures |
| Primary value | Supplementary IoT power | Storm-survival power | Dust-hazard mitigation + power |

### 8.1 Earth Deployment Priorities

1. **Urban rooftop corona arrays** — retrofit existing buildings, dual-purpose with lightning protection
2. **Smart road surfaces** — triboelectric harvesting from vehicle/pedestrian traffic (TENG-based, well-proven)
3. **Coastal wind-flutter harvesters** — high-wind, high-salt-spray environments maximise triboelectric output
4. **Agricultural induction loops** — buried during routine drainage installation, harvest storm-transit energy

### 8.2 Mars Deployment Priorities

1. **Dust-charge harvesters on habitat exteriors** — the only power source that works *better* during dust storms
2. **Atmospheric electric field sensors** — early warning for electrical discharge events (critical safety)
3. **Triboelectric dust filters** — combine air filtration with energy harvesting (dual-purpose)

### 8.3 Lunar Deployment Priorities

1. **Terminator-zone potential gradient harvesters** — fixed at polar sites, near-continuous terminator proximity
2. **Regolith-motion detectors** — sense electrostatic dust levitation for habitat hazard warnings
3. **Solar-wind charge collectors** — harvest proton flux on dayside surfaces

---

## 9. Falsifiable Predictions

### Prediction 1: Corona Array Power Scaling
**Claim:** An array of 100 corona-point collectors at 10m elevation will produce ≥10 μW continuous fair-weather power and ≥100 mW during storm approach (E > 2,000 V/m).

**Test:** Deploy prototype array with calibrated E-field mill and current measurement. Correlate output with atmospheric field over 12-month observation period.

**Falsification:** If fair-weather output < 1 μW or storm output < 10 mW at measured field strengths, the corona coupling model is wrong.

### Prediction 2: Inductive Storm Detection
**Claim:** A 100m × 100m buried loop will detect storm-cell transit as a measurable EMF signal distinguishable from background noise.

**Test:** Deploy buried loop with concurrent E-field and magnetometer measurements during storm season.

**Falsification:** If the storm-motion signal cannot be distinguished from telluric and power-line interference with standard filtering, the approach is impractical.

### Prediction 3: Capacitive Charging Rate
**Claim:** A 100 m² insulated ground plane at 10m height will accumulate ≥1 J per storm-approach event (E > 5,000 V/m sustained for >5 minutes).

**Test:** Deploy instrumented ground plane with voltage monitoring and controlled discharge measurement.

**Falsification:** If stored energy < 0.1 J per event, the atmospheric recharge rate is too slow for practical harvesting.

### Prediction 4: Triboelectric Dust Power on Mars (Simulation)
**Claim:** In Martian atmospheric conditions (600 Pa, CO₂, iron oxide/silicate dust), triboelectric charge generation per unit area exceeds Earth equivalents by ≥10×.

**Test:** Vacuum chamber experiments at 600 Pa CO₂ with Mars simulant dust and triboelectric measurement.

**Falsification:** If charge generation is comparable to or less than Earth atmospheric conditions, the low-pressure enhancement is not as predicted.

---

## 10. Economics and Practical Value

### 10.1 Energy Harvesting Value

For Earth applications, the direct energy value is modest:

```
Urban rooftop system (100 corona points + 200m² ground plane):
Fair weather: ~0.5 mW continuous = 4.4 Wh/year = ~$0.001/year at NZ rates
Storm augmented: ~5 W for 100 hours/year = 500 Wh/year = ~$0.15/year
```

This will not pay for itself through energy value alone.

### 10.2 The Real Value Proposition

The value is NOT the energy. It's the three things the energy enables:

**1. Self-Powered Atmospheric Sensing Network**
Each harvesting node is simultaneously a high-resolution atmospheric electrical sensor. A city-wide network produces real-time electric field maps with resolution impossible from ground-based weather stations. This data is commercially valuable for:
- Aviation (storm tracking, lightning risk assessment)
- Insurance (precise lightning incidence mapping)
- Telecommunications (atmospheric propagation conditions)
- Agriculture (storm prediction, frost warning)

**2. Lightning Protection Enhancement**
Integrating energy harvesting into lightning protection infrastructure creates smarter protection systems that self-monitor, self-test, and predict maintenance needs. The harvested energy powers the monitoring electronics.

**3. Mars/Moon Survival Power**
In extreme environments, supplementary power during primary-source failure (dust storms obscuring solar panels) is life-critical. The economic value is infinite when the alternative is mission loss.

### 10.3 Development Cost Estimate

```
Phase 1 (Earth prototype, 12 months):
  - Corona array (100 points, 10m tower)         $5,000
  - Capacitive ground plane (100m², insulated)    $8,000
  - Buried induction loop (100m × 100m)           $12,000
  - Instrumentation and data logging              $5,000
  - Power conversion electronics                  $3,000
  Total:                                          ~$33,000 NZD

Phase 2 (Mars-analogue testing, 12 months):
  - Vacuum chamber (600 Pa CO₂ capability)        $15,000
  - Mars dust simulant                            $2,000
  - Triboelectric measurement equipment           $8,000
  Total:                                          ~$25,000 NZD
```

This is within reach of university research grants, small foundation funding, or crowdfunding.

---

## 11. Open Questions and Collaboration Invitations

### 11.1 Physics Questions
- What is the actual recharge time constant for a capacitive ground plane in storm conditions? (Requires field measurement.)
- What are the ground conduction current densities beneath real storm cells? (Requires buried electrode arrays during storms.)
- Does Martian dust storm triboelectric charging scale as predicted from low-pressure CO₂ breakdown models?

### 11.2 Engineering Questions
- What is the optimal corona-point geometry for atmospheric field harvesting (tip radius, spacing, height)?
- Can existing lightning protection systems be retrofitted with energy harvesting without compromising safety?
- What power conversion topology best handles the 10⁶ dynamic range from fair-weather to pre-strike conditions?

### 11.3 Collaboration Sought
- **Atmospheric physics:** Field measurement campaigns during storms
- **Mars analogue research:** Vacuum chamber triboelectric experiments
- **Power electronics:** Ultra-high-dynamic-range DC-DC converters
- **Urban planning:** Integration with building electrical infrastructure
- **Space agencies:** Mars/Lunar mission power system trade studies

---

## 12. Conclusion

The atmospheric electrical environment represents a perpetually available, globally distributed, zero-fuel energy source that civilization currently ignores entirely. Direct lightning capture is a dead end, but the *fields* that produce lightning — and the *dust* that produces Martian storms — are harvestable with existing technology at modest cost.

No single mode solves the problem. The power densities are too low for any one approach to be economically compelling on its own. But a multi-modal system that adapts to conditions, doubles as an atmospheric sensing network, and addresses the specific vulnerability of Mars missions to dust-storm power loss — that system addresses real needs that no existing technology serves.

The physics is sound. The predictions are falsifiable. The prototype cost is modest. The question is not whether this works — portions of it demonstrably do (TENGs, corona discharge harvesting, atmospheric field measurement). The question is whether the integrated system produces enough value to justify deployment.

We believe it does. We invite others to help us prove it.

---

## References

Christian, H. J., et al. (2003). Global frequency and distribution of lightning as observed from space. *Journal of Geophysical Research*, 108(D1).

Farrell, W. M., et al. (2004). Electric and magnetic signatures of dust devils from the 2000-2001 MATADOR desert tests. *Journal of Geophysical Research*, 109(E3).

Gu, L., et al. (2025). Energy harvesting from corona discharge on HVdc overhead transmission line. *Electrical Engineering*.

Helman, D. (2011). Catching lightning for alternative energy. *Renewable Energy*, 36(5), 1311-1314.

Helman, D. (2020). Lightning for energy and material uses: A structured review. *Global Challenges*, 4(10), 2000029.

Melnik, O. & Parrot, M. (1998). Electrostatic discharge in Martian dust storms. *Journal of Geophysical Research*, 103(A12).

Rycroft, M. J., et al. (2000). New model simulations of the global atmospheric electric circuit. *Journal of Atmospheric and Solar-Terrestrial Physics*, 62(17-18).

Stubbs, T. J., et al. (2006). A dynamic fountain model for lunar dust. *Advances in Space Research*, 37(1), 59-66.

Wang, Z. L. (2012). Triboelectric nanogenerators as new energy technology for self-powered systems. *ACS Nano*, 7(11), 9533-9557.

Chung, S. H., et al. (2025). Particulate static effect induced electricity generation inspired by Tesla turbine. *Advanced Energy Materials*.

---

**Lycheetah Foundation**  
**Dunedin, New Zealand**  
**February 2026**  

*"Don't try to catch the waterfall. Drink from the river."*
