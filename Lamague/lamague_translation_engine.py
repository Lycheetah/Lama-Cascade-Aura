"""
LAMAGUE Translation Engine v1.0
================================
A testable, falsifiable implementation of the LAMAGUE bidirectional
conceptual translation protocol.

Author: Mackenzie Conor James Clark / Lycheetah Foundation
Status: TESTABLE — every claim has a corresponding test that can fail.

Core Claims (each with falsification criteria):
  1. Primitive Decomposition: Concepts can be decomposed into universal primitives
     → FALSIFIED IF: Native speakers reject decompositions as meaningless
  2. Invariant Preservation: Valid translations preserve semantic invariants
     → FALSIFIED IF: Breaking invariants does NOT correlate with translation errors
  3. Round-Trip Fidelity: LAMAGUE round-trips preserve more meaning than direct translation
     → FALSIFIED IF: Fidelity scores ≤ conventional translation scores
  4. Bidirectional Enrichment: Round-trips enrich rather than degrade concepts
     → FALSIFIED IF: E(C') < E(C) consistently
  5. Chiral Complementarity: Some cross-cultural concepts are structural mirrors
     → FALSIFIED IF: Proposed chiral pairs share no invariant structure
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json
import hashlib


# ============================================================
# PART 1: PRIMITIVE SPACE — The atoms of meaning
# ============================================================

class PrimitiveClass(Enum):
    """LAMAGUE symbol classes from the formal specification."""
    INVARIANT = "I"    # Stable reference points
    DYNAMIC = "D"      # Transformations and changes
    FIELD = "F"        # State descriptions
    META = "M"         # Compression operators


@dataclass
class Primitive:
    """A single LAMAGUE primitive with semantic vector representation.
    
    The vector is NOT arbitrary — each dimension corresponds to a 
    measurable experiential axis. This is the testable claim:
    if these axes don't map to real human experience, the system fails.
    """
    symbol: str
    name: str
    spoken: str          # Spoken LAMAGUE (SpL) phoneme
    pclass: PrimitiveClass
    description: str
    
    # 8-dimensional semantic vector
    # Dimensions: [valence, arousal, agency, temporality, 
    #              social, recursive, stability, boundary]
    # Each ∈ [-1.0, 1.0]
    # These dimensions are TESTABLE — they should correlate with
    # psychological measures of the same constructs.
    vector: np.ndarray = field(default_factory=lambda: np.zeros(8))
    
    def distance(self, other: 'Primitive') -> float:
        """Euclidean distance between primitive vectors."""
        return float(np.linalg.norm(self.vector - other.vector))
    
    def cosine_similarity(self, other: 'Primitive') -> float:
        """Cosine similarity — measures alignment of experiential direction."""
        dot = np.dot(self.vector, other.vector)
        norms = np.linalg.norm(self.vector) * np.linalg.norm(other.vector)
        if norms < 1e-10:
            return 0.0
        return float(dot / norms)


# === PRIMITIVE REGISTRY ===
# Dimensions: [valence, arousal, agency, temporality, social, recursive, stability, boundary]

PRIMITIVES = {
    # I-Class: Invariants
    "∅": Primitive("∅", "Void", "vu", PrimitiveClass.INVARIANT,
        "Zero-point, emptiness, ground state of potential",
        np.array([0.0, -0.8, -0.5, 0.0, -0.3, 0.0, 0.9, -0.9])),
    
    "A₀": Primitive("A₀", "Anchor", "an", PrimitiveClass.INVARIANT,
        "Stable foundation, point of reference",
        np.array([0.3, -0.3, 0.4, 0.0, 0.2, 0.0, 0.95, 0.5])),
    
    "Ω": Primitive("Ω", "Wholeness", "om", PrimitiveClass.INVARIANT,
        "Integration of fragments, healed state",
        np.array([0.9, 0.2, 0.6, 0.3, 0.7, 0.4, 0.85, -0.2])),
    
    "Ψ_inv": Primitive("Ψ_inv", "Invariant Curve", "sai-an", PrimitiveClass.INVARIANT,
        "Stable attractor state, convergence target",
        np.array([0.5, 0.0, 0.3, 0.8, 0.1, 0.7, 0.95, 0.0])),
    
    # D-Class: Dynamics
    "Φ↑": Primitive("Φ↑", "Ascent", "fi", PrimitiveClass.DYNAMIC,
        "Rising, purpose alignment, actualization",
        np.array([0.7, 0.6, 0.8, 0.5, 0.3, 0.2, 0.4, 0.3])),
    
    "↯": Primitive("↯", "Collision", "kol", PrimitiveClass.DYNAMIC,
        "Encounter with other/self, boundary event",
        np.array([-0.3, 0.9, 0.2, 0.0, 0.5, 0.0, -0.6, 0.8])),
    
    "∇_cas": Primitive("∇_cas", "Cascade", "kas", PrimitiveClass.DYNAMIC,
        "Sudden reorganization when truth pressure exceeds threshold",
        np.array([0.0, 0.95, 0.3, 0.0, 0.4, 0.6, -0.8, 0.5])),
    
    "⇈": Primitive("⇈", "Kinetic Rebound", "ki", PrimitiveClass.DYNAMIC,
        "Collapse as fuel, anti-fragile response",
        np.array([0.4, 0.7, 0.7, 0.3, 0.1, 0.3, -0.3, 0.4])),
    
    # F-Class: Fields
    "Ψ": Primitive("Ψ", "Fold", "sai", PrimitiveClass.FIELD,
        "Recursive self-awareness, consciousness folding",
        np.array([0.1, 0.3, 0.5, 0.2, -0.2, 0.9, 0.3, 0.1])),
    
    "∞": Primitive("∞", "Infinity", "in", PrimitiveClass.FIELD,
        "Eternal recursion, unbounded connection",
        np.array([0.4, 0.1, 0.1, 0.9, 0.6, 0.95, 0.5, -0.7])),
    
    "⥀": Primitive("⥀", "Recursive Loop", "lu", PrimitiveClass.FIELD,
        "Circular causality, effect creating cause",
        np.array([0.0, 0.3, 0.2, 0.7, 0.0, 0.95, 0.2, 0.0])),
    
    # Special operators
    "◇_ø": Primitive("◇_ø", "Dark Matter Block", "dah", PrimitiveClass.META,
        "Unprovable axiom with infinite explanatory power",
        np.array([0.0, 0.0, 0.0, 0.5, 0.0, 0.3, 0.9, 0.9])),
    
    "📡": Primitive("📡", "Ghost Signal", "gos", PrimitiveClass.DYNAMIC,
        "Pre-cognitive detection of future coherence",
        np.array([0.3, 0.4, 0.1, 0.8, 0.3, 0.5, 0.2, -0.3])),
    
    "✺": Primitive("✺", "Consensus-Flare", "fla", PrimitiveClass.DYNAMIC,
        "Minds synchronizing on truth without collusion",
        np.array([0.6, 0.5, 0.3, 0.0, 0.95, 0.4, 0.6, -0.5])),
}


# ============================================================
# PART 2: CONCEPT DECOMPOSITION — Breaking meaning into atoms
# ============================================================

@dataclass
class Decomposition:
    """A concept decomposed into LAMAGUE primitives with weights."""
    source_term: str
    source_language: str
    primitives: List[Tuple[str, float]]  # (primitive_symbol, weight)
    confidence: float                     # 0-1, how confident we are
    notes: str = ""
    
    @property
    def vector(self) -> np.ndarray:
        """Weighted sum of primitive vectors = concept vector."""
        result = np.zeros(8)
        total_weight = 0.0
        for sym, weight in self.primitives:
            if sym in PRIMITIVES:
                result += weight * PRIMITIVES[sym].vector
                total_weight += weight
        if total_weight > 0:
            result /= total_weight
        return result
    
    @property
    def sequence_string(self) -> str:
        """Human-readable primitive sequence."""
        parts = []
        for sym, w in self.primitives:
            name = PRIMITIVES[sym].name if sym in PRIMITIVES else sym
            parts.append(f"{sym}({name}:{w:.1f})")
        return " + ".join(parts)
    
    @property 
    def spoken(self) -> str:
        """Spoken LAMAGUE rendering."""
        return "-".join(PRIMITIVES[sym].spoken for sym, _ in self.primitives if sym in PRIMITIVES)
    
    def structural_hash(self) -> str:
        """Deterministic hash of the decomposition structure.
        Two decompositions with the same hash are structurally identical.
        """
        sig = "|".join(f"{s}:{w:.2f}" for s, w in sorted(self.primitives))
        return hashlib.md5(sig.encode()).hexdigest()[:12]


# === CONCEPT DATABASE ===
# Each entry is a TESTABLE claim: "this concept decomposes this way"
# FALSIFICATION: Native speakers rate the decomposition as inaccurate

CONCEPT_DB: Dict[str, Decomposition] = {
    # English concepts
    "shadow_jungian": Decomposition(
        "Shadow (Jungian)", "English",
        [("Ψ", 0.8), ("∅", 0.9), ("↯", 0.7), ("Ω", 0.6)],
        0.85,
        "The disowned self: ego-fold + repressed void + encounter + integration"
    ),
    "resilience": Decomposition(
        "Resilience", "English",
        [("↯", 0.6), ("⇈", 0.9), ("Ω", 0.7), ("A₀", 0.5)],
        0.80,
        "Strength through adversity: collision + rebound + wholeness + re-anchoring"
    ),
    "hope": Decomposition(
        "Hope", "English",
        [("Φ↑", 0.8), ("📡", 0.7), ("∞", 0.4)],
        0.75,
        "Ascent + ghost signal of future + infinite possibility"
    ),
    
    # Mandarin concepts  
    "yuan_fate": Decomposition(
        "缘 (yuán)", "Mandarin",
        [("∞", 0.9), ("∇_cas", 0.7), ("⥀", 0.8), ("Φ↑", 0.6)],
        0.80,
        "Relational destiny: eternal connection + cascade meeting + karmic loop + alignment"
    ),
    "wuwei": Decomposition(
        "无为 (wú wéi)", "Mandarin",
        [("∅", 0.8), ("Φ↑", 0.6), ("Ψ_inv", 0.9)],
        0.75,
        "Non-action: void of forced effort + natural ascent + convergence to invariant"
    ),
    
    # Sanskrit concepts
    "ahamkara": Decomposition(
        "अहंकार (ahamkāra)", "Sanskrit",
        [("Ψ", 0.9), ("A₀", 0.5), ("⥀", 0.8)],
        0.80,
        "Ego-maker: self-fold + false anchor + self-clinging loop"
    ),
    "wuwo": Decomposition(
        "无我 (wú wǒ)", "Mandarin",
        [("∅", 0.9), ("Ψ", 0.7)],
        0.85,
        "No-self: void of ego + true self-fold"
    ),
    "sat": Decomposition(
        "सत् (sat)", "Sanskrit",
        [("A₀", 0.9), ("Ψ", 0.7), ("∞", 0.8)],
        0.70,
        "Being/truth: ultimate anchor + self-awareness + infinite being"
    ),
    
    # Japanese concepts
    "wabi_sabi": Decomposition(
        "侘び寂び (wabi-sabi)", "Japanese",
        [("∅", 0.7), ("Ω", 0.6), ("∞", 0.5)],
        0.70,
        "Imperfect beauty: void of perfection + wholeness in imperfection + infinite beauty"
    ),
    
    # Arabic concepts
    "al_qadr": Decomposition(
        "القدر (al-qadr)", "Arabic",
        [("∇_cas", 0.8), ("⥀", 0.7), ("Φ↑", 0.5)],
        0.70,
        "Divine decree: cascade + predestination loop + surrender-ascent"
    ),
    
    # Portuguese
    "saudade": Decomposition(
        "Saudade", "Portuguese",
        [("∅", 0.8), ("∞", 0.9), ("↯", 0.6)],
        0.75,
        "Longing: void of presence + eternal connection + collision with absence"
    ),
}


# ============================================================
# PART 3: SEMANTIC INVARIANTS — The rules that cannot be broken
# ============================================================

class InvariantType(Enum):
    CONSENT = "consent"
    RESPONSIBILITY = "responsibility"  
    SCOPE = "scope"
    REVERSIBILITY = "reversibility"
    HARM_THRESHOLD = "harm_threshold"
    TEMPORAL_ORDER = "temporal_order"
    ENERGY_CONSERVATION = "energy_conservation"


@dataclass
class InvariantCheck:
    """Result of checking a single invariant."""
    invariant: InvariantType
    preserved: bool
    magnitude: float   # How much was preserved (0-1)
    detail: str


def check_invariants(original: Decomposition, translated: Decomposition) -> List[InvariantCheck]:
    """Check all semantic invariants between original and translated decomposition.
    
    TESTABLE CLAIM: Breaking these invariants correlates with bad translations.
    FALSIFIED IF: Translations that break invariants are rated equally good by native speakers.
    """
    results = []
    
    # 1. TEMPORAL ORDER — primitive sequence should maintain causal flow
    #    Measured by: correlation of temporal dimension across primitives
    orig_temporal = [PRIMITIVES[s].vector[3] for s, _ in original.primitives if s in PRIMITIVES]
    trans_temporal = [PRIMITIVES[s].vector[3] for s, _ in translated.primitives if s in PRIMITIVES]
    if len(orig_temporal) >= 2 and len(trans_temporal) >= 2:
        # Check if temporal ordering is preserved (monotonicity of temporal values)
        orig_flow = np.mean(np.diff(orig_temporal)) if len(orig_temporal) > 1 else 0
        trans_flow = np.mean(np.diff(trans_temporal)) if len(trans_temporal) > 1 else 0
        same_direction = (orig_flow >= 0) == (trans_flow >= 0)
        results.append(InvariantCheck(
            InvariantType.TEMPORAL_ORDER, same_direction,
            1.0 if same_direction else 0.0,
            f"Original flow: {orig_flow:.3f}, Translated flow: {trans_flow:.3f}"
        ))
    
    # 2. ENERGY CONSERVATION — entropy should not increase through translation
    #    Measured by: stability dimension should not decrease
    orig_stability = np.mean([PRIMITIVES[s].vector[6] for s, _ in original.primitives if s in PRIMITIVES])
    trans_stability = np.mean([PRIMITIVES[s].vector[6] for s, _ in translated.primitives if s in PRIMITIVES])
    energy_ok = trans_stability >= orig_stability - 0.15  # Allow small tolerance
    results.append(InvariantCheck(
        InvariantType.ENERGY_CONSERVATION, energy_ok,
        min(1.0, max(0.0, 1.0 - abs(trans_stability - orig_stability))),
        f"Original stability: {orig_stability:.3f}, Translated: {trans_stability:.3f}"
    ))
    
    # 3. SCOPE — boundary dimension should be preserved
    orig_boundary = np.mean([PRIMITIVES[s].vector[7] for s, _ in original.primitives if s in PRIMITIVES])
    trans_boundary = np.mean([PRIMITIVES[s].vector[7] for s, _ in translated.primitives if s in PRIMITIVES])
    scope_ok = abs(orig_boundary - trans_boundary) < 0.3
    results.append(InvariantCheck(
        InvariantType.SCOPE, scope_ok,
        max(0.0, 1.0 - abs(orig_boundary - trans_boundary)),
        f"Original boundary: {orig_boundary:.3f}, Translated: {trans_boundary:.3f}"
    ))
    
    # 4. AGENCY — should be preserved (self-directed vs other-directed)
    orig_agency = np.mean([PRIMITIVES[s].vector[2] for s, _ in original.primitives if s in PRIMITIVES])
    trans_agency = np.mean([PRIMITIVES[s].vector[2] for s, _ in translated.primitives if s in PRIMITIVES])
    agency_ok = abs(orig_agency - trans_agency) < 0.3
    results.append(InvariantCheck(
        InvariantType.RESPONSIBILITY, agency_ok,
        max(0.0, 1.0 - abs(orig_agency - trans_agency)),
        f"Original agency: {orig_agency:.3f}, Translated: {trans_agency:.3f}"
    ))
    
    return results


# ============================================================
# PART 4: TRANSLATION ENGINE — The core mechanism
# ============================================================

class LAMAGUETranslator:
    """The translation engine. Every method produces measurable output."""
    
    def __init__(self):
        self.primitives = PRIMITIVES
        self.concepts = CONCEPT_DB
        self.translation_log: List[Dict] = []
    
    def decompose(self, term: str, language: str, 
                  primitives: List[Tuple[str, float]], 
                  confidence: float = 0.5,
                  notes: str = "") -> Decomposition:
        """Create a new decomposition. Returns a measurable object."""
        d = Decomposition(term, language, primitives, confidence, notes)
        return d
    
    def fidelity(self, d1: Decomposition, d2: Decomposition) -> float:
        """Measure semantic fidelity between two decompositions.
        
        Uses cosine similarity of concept vectors.
        Range: [-1.0, 1.0] where 1.0 = identical meaning.
        
        TESTABLE: This score should correlate with native speaker
        ratings of translation quality. If it doesn't, the vector
        space is misconfigured.
        """
        v1 = d1.vector
        v2 = d2.vector
        dot = np.dot(v1, v2)
        norms = np.linalg.norm(v1) * np.linalg.norm(v2)
        if norms < 1e-10:
            return 0.0
        return float(dot / norms)
    
    def enrichment(self, original: Decomposition, 
                   round_tripped: Decomposition) -> float:
        """Measure whether round-trip translation enriched the concept.
        
        E = (dimensionality of round-tripped) / (dimensionality of original)
        Where dimensionality = number of non-trivial vector components.
        
        CLAIM: E >= 1.0 (concepts gain depth through translation)
        FALSIFIED IF: E < 1.0 consistently
        """
        def effective_dims(v):
            """Count dimensions with significant activation."""
            return float(np.sum(np.abs(v) > 0.15))
        
        orig_dims = effective_dims(original.vector)
        rt_dims = effective_dims(round_tripped.vector)
        
        if orig_dims < 1:
            return 1.0
        return rt_dims / orig_dims
    
    def chiral_score(self, d1: Decomposition, d2: Decomposition) -> float:
        """Measure chiral complementarity between two decompositions.
        
        Chiral complements are ANTI-correlated (mirror images).
        Score = -cosine_similarity (higher = more chiral)
        
        Range: [-1.0, 1.0] where 1.0 = perfect chiral mirror
        
        TESTABLE: Proposed chiral pairs should score > 0.3
        FALSIFIED IF: Score ≤ 0 (they're actually similar, not mirrored)
        """
        return -self.fidelity(d1, d2)
    
    def round_trip(self, concept_key: str, 
                   target_decomposition: Decomposition) -> Dict:
        """Perform a full round-trip translation and measure everything.
        
        Returns a dictionary of ALL measurable outputs.
        """
        if concept_key not in self.concepts:
            return {"error": f"Unknown concept: {concept_key}"}
        
        original = self.concepts[concept_key]
        
        # Fidelity: how well does the target capture the original?
        fid = self.fidelity(original, target_decomposition)
        
        # Enrichment: did the round-trip add depth?
        enr = self.enrichment(original, target_decomposition)
        
        # Invariant checks
        invariants = check_invariants(original, target_decomposition)
        invariants_passed = sum(1 for i in invariants if i.preserved)
        invariants_total = len(invariants)
        
        # Vector distance
        dist = float(np.linalg.norm(original.vector - target_decomposition.vector))
        
        result = {
            "original": {
                "term": original.source_term,
                "language": original.source_language,
                "vector": original.vector.tolist(),
                "spoken": original.spoken,
                "decomposition": original.sequence_string,
                "structural_hash": original.structural_hash(),
            },
            "translated": {
                "term": target_decomposition.source_term,
                "language": target_decomposition.source_language,
                "vector": target_decomposition.vector.tolist(),
                "spoken": target_decomposition.spoken,
                "decomposition": target_decomposition.sequence_string,
                "structural_hash": target_decomposition.structural_hash(),
            },
            "metrics": {
                "fidelity": round(fid, 4),
                "enrichment": round(enr, 4),
                "vector_distance": round(dist, 4),
                "invariants_passed": invariants_passed,
                "invariants_total": invariants_total,
                "invariant_ratio": round(invariants_passed / max(1, invariants_total), 4),
                "structural_match": original.structural_hash() == target_decomposition.structural_hash(),
            },
            "invariant_details": [
                {"type": i.invariant.value, "preserved": i.preserved, 
                 "magnitude": round(i.magnitude, 4), "detail": i.detail}
                for i in invariants
            ]
        }
        
        self.translation_log.append(result)
        return result
    
    def validate_translation(self, result: Dict) -> Dict:
        """Apply the truth test: is this translation valid?
        
        THE CORE FALSIFIABLE CLAIM:
        If invariant_ratio < 0.75, the translation is WRONG.
        If invariant_ratio >= 0.75 AND fidelity > 0.6, translation is VALID.
        
        This can be tested against human judgments.
        """
        m = result["metrics"]
        
        if m["invariant_ratio"] < 0.5:
            verdict = "DEFINITELY_WRONG"
            reason = "Multiple semantic invariants broken"
        elif m["invariant_ratio"] < 0.75:
            verdict = "PROBABLY_WRONG"
            reason = "Some invariants broken — flag for review"
        elif m["fidelity"] < 0.4:
            verdict = "LOW_FIDELITY"
            reason = "Invariants preserved but concept vectors diverge significantly"
        elif m["fidelity"] < 0.6:
            verdict = "ACCEPTABLE"
            reason = "Invariants preserved, moderate fidelity"
        else:
            verdict = "VALID"
            reason = "Invariants preserved, high fidelity"
        
        return {
            "verdict": verdict,
            "reason": reason,
            "fidelity": m["fidelity"],
            "invariant_ratio": m["invariant_ratio"],
            "enrichment": m["enrichment"],
        }


# ============================================================
# PART 5: FALSIFICATION TESTS — Where this can break
# ============================================================

def run_falsification_tests():
    """Run all falsification tests. If LAMAGUE works, these should pass.
    If LAMAGUE is broken, specific tests will fail and tell us WHERE.
    """
    engine = LAMAGUETranslator()
    results = []
    
    print("=" * 70)
    print("LAMAGUE FALSIFICATION TEST SUITE")
    print("=" * 70)
    print()
    
    # --- TEST 1: Chiral Complementarity ---
    print("TEST 1: Chiral Complementarity (ahamkāra vs wú wǒ)")
    print("-" * 50)
    aham = CONCEPT_DB["ahamkara"]
    wuwo = CONCEPT_DB["wuwo"]
    chiral = engine.chiral_score(aham, wuwo)
    
    print(f"  अहंकार decomposition: {aham.sequence_string}")
    print(f"  无我 decomposition:    {wuwo.sequence_string}")
    print(f"  Chiral score:          {chiral:.4f}")
    print(f"  CLAIM: Score > 0.0 (they are structural mirrors)")
    
    test1_pass = chiral > 0.0
    print(f"  RESULT: {'✓ PASS' if test1_pass else '✗ FAIL — NOT CHIRAL'}")
    results.append(("Chiral Complementarity", test1_pass, chiral))
    print()
    
    # --- TEST 2: Similar concepts should have high fidelity ---
    print("TEST 2: Semantic Proximity (similar concepts cluster)")
    print("-" * 50)
    yuan = CONCEPT_DB["yuan_fate"]
    qadr = CONCEPT_DB["al_qadr"]
    fid = engine.fidelity(yuan, qadr)
    
    print(f"  缘 (yuán) vector:      {yuan.vector.round(2).tolist()}")
    print(f"  القدر (al-qadr) vector: {qadr.vector.round(2).tolist()}")
    print(f"  Fidelity score:        {fid:.4f}")
    print(f"  CLAIM: Score > 0.5 (both are 'fate/destiny' concepts)")
    
    test2_pass = fid > 0.5
    print(f"  RESULT: {'✓ PASS' if test2_pass else '✗ FAIL — CONCEPTS DO NOT CLUSTER'}")
    results.append(("Semantic Proximity", test2_pass, fid))
    print()
    
    # --- TEST 3: Dissimilar concepts should have low fidelity ---
    print("TEST 3: Semantic Discrimination (dissimilar concepts diverge)")
    print("-" * 50)
    hope = CONCEPT_DB["hope"]
    saudade = CONCEPT_DB["saudade"]
    fid_dis = engine.fidelity(hope, saudade)
    
    print(f"  Hope vector:           {hope.vector.round(2).tolist()}")
    print(f"  Saudade vector:        {saudade.vector.round(2).tolist()}")
    print(f"  Fidelity score:        {fid_dis:.4f}")
    print(f"  CLAIM: Score < 0.7 (these are experientially different)")
    
    test3_pass = fid_dis < 0.7
    print(f"  RESULT: {'✓ PASS' if test3_pass else '✗ FAIL — SYSTEM CANNOT DISCRIMINATE'}")
    results.append(("Semantic Discrimination", test3_pass, fid_dis))
    print()
    
    # --- TEST 4: Invariant breaking detection ---
    print("TEST 4: Invariant Breaking Detection")
    print("-" * 50)
    shadow = CONCEPT_DB["shadow_jungian"]
    
    # Create a deliberately BAD translation (reversed agency + broken temporality)
    bad_translation = Decomposition(
        "影 (bad translation)", "Mandarin",
        [("∅", 0.3), ("Φ↑", 0.9), ("✺", 0.8)],  # Wrong primitives
        0.5, "Deliberately bad: no collision, no fold, no integration"
    )
    
    result = engine.round_trip("shadow_jungian", bad_translation)
    validation = engine.validate_translation(result)
    
    print(f"  Original:    {shadow.sequence_string}")
    print(f"  Bad trans:   {bad_translation.sequence_string}")
    print(f"  Fidelity:    {result['metrics']['fidelity']:.4f}")
    print(f"  Invariants:  {result['metrics']['invariants_passed']}/{result['metrics']['invariants_total']}")
    print(f"  Verdict:     {validation['verdict']}")
    print(f"  CLAIM: System detects this as wrong (verdict != VALID)")
    
    test4_pass = validation["verdict"] != "VALID"
    print(f"  RESULT: {'✓ PASS' if test4_pass else '✗ FAIL — DID NOT DETECT BAD TRANSLATION'}")
    results.append(("Invariant Breaking", test4_pass, result['metrics']['fidelity']))
    print()
    
    # --- TEST 5: Good translation should pass ---
    print("TEST 5: Valid Translation Acceptance")
    print("-" * 50)
    
    # Create a GOOD translation of shadow into Mandarin
    good_translation = Decomposition(
        "阴藏我 (yīn cáng wǒ)", "Mandarin",
        [("Ψ", 0.7), ("∅", 0.85), ("↯", 0.65), ("Ω", 0.55)],
        0.80, "Hidden dark self: fold + void + collision + wholeness"
    )
    
    result_good = engine.round_trip("shadow_jungian", good_translation)
    validation_good = engine.validate_translation(result_good)
    
    print(f"  Original:    {shadow.sequence_string}")
    print(f"  Good trans:  {good_translation.sequence_string}")
    print(f"  Fidelity:    {result_good['metrics']['fidelity']:.4f}")
    print(f"  Invariants:  {result_good['metrics']['invariants_passed']}/{result_good['metrics']['invariants_total']}")
    print(f"  Verdict:     {validation_good['verdict']}")
    print(f"  CLAIM: System accepts this as valid")
    
    test5_pass = validation_good["verdict"] in ("VALID", "ACCEPTABLE")
    print(f"  RESULT: {'✓ PASS' if test5_pass else '✗ FAIL — REJECTED GOOD TRANSLATION'}")
    results.append(("Valid Translation", test5_pass, result_good['metrics']['fidelity']))
    print()
    
    # --- TEST 6: Round-trip enrichment ---
    print("TEST 6: Bidirectional Enrichment (E(C') >= E(C))")
    print("-" * 50)
    
    # Take yuan, translate to English-enriched version
    yuan_enriched = Decomposition(
        "Recursive convergent destiny", "English (round-tripped)",
        [("∞", 0.9), ("∇_cas", 0.7), ("⥀", 0.8), ("Φ↑", 0.6), ("Ψ", 0.3)],
        0.75, "Added Ψ fold from English self-awareness framing"
    )
    
    e_score = engine.enrichment(yuan, yuan_enriched)
    print(f"  Original dims:     {sum(abs(yuan.vector) > 0.15)}")
    print(f"  Round-trip dims:   {sum(abs(yuan_enriched.vector) > 0.15)}")
    print(f"  Enrichment score:  {e_score:.4f}")
    print(f"  CLAIM: E >= 1.0 (round-trip does not degrade)")
    
    test6_pass = e_score >= 1.0
    print(f"  RESULT: {'✓ PASS' if test6_pass else '✗ FAIL — ROUND TRIP DEGRADED MEANING'}")
    results.append(("Enrichment", test6_pass, e_score))
    print()
    
    # --- TEST 7: Sat vs Dao structural comparison ---
    print("TEST 7: Cross-Cultural Structure (सत् vs 道)")
    print("-" * 50)
    sat = CONCEPT_DB["sat"]
    
    dao = Decomposition(
        "道 (dào)", "Mandarin",
        [("∅", 0.7), ("Φ↑", 0.6), ("∞", 0.8)],
        0.70, "The Way: void of form + ascending flow + infinite pattern"
    )
    
    fid_cross = engine.fidelity(sat, dao)
    print(f"  सत् (sat):  {sat.sequence_string}")
    print(f"  道 (dào):   {dao.sequence_string}")
    print(f"  Fidelity:   {fid_cross:.4f}")
    print(f"  CLAIM: Score > 0.5 (deep structural similarity)")
    
    test7_pass = fid_cross > 0.5
    print(f"  RESULT: {'✓ PASS' if test7_pass else '✗ FAIL — NO STRUCTURAL SIMILARITY'}")
    results.append(("Cross-Cultural Structure", test7_pass, fid_cross))
    print()
    
    # === SUMMARY ===
    print("=" * 70)
    print("FALSIFICATION SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    
    for name, passed_test, score in results:
        status = "✓" if passed_test else "✗"
        print(f"  {status} {name:35s} score={score:.4f}")
    
    print(f"\n  TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  ALL TESTS PASS — LAMAGUE claims hold under these conditions.")
        print("  NEXT STEP: Test against human native speaker ratings.")
    else:
        failed = [name for name, p, _ in results if not p]
        print(f"\n  FAILURES: {', '.join(failed)}")
        print("  These failures identify specific claims that need revision.")
    
    print(f"\n  CRITICAL REMINDER: These are internal consistency tests.")
    print(f"  External validation requires human subjects research.")
    print(f"  The system is honest about what it has and hasn't proven.")
    
    return results


# ============================================================
# PART 6: EXPERIMENTAL PROTOCOL — What to test with humans
# ============================================================

def print_experimental_protocol():
    """Print the protocol for human-subjects validation."""
    print()
    print("=" * 70)
    print("EXPERIMENTAL PROTOCOL FOR HUMAN VALIDATION")
    print("=" * 70)
    print("""
EXPERIMENT 1: Primitive Universality Test
-----------------------------------------
Hypothesis: LAMAGUE primitives map to universal human experiences.
Method:
  1. Select 50 participants across 5+ language families
  2. Present each primitive (symbol + name) without LAMAGUE context
  3. Ask: "Describe a personal experience that matches this concept"
  4. Rate match quality on 1-7 Likert scale
  5. Code responses for experiential overlap across languages
Falsification: If match quality < 4.0 for any primitive across 
  multiple language groups, that primitive is not universal.
Sample size: 50 (10 per language family minimum)
Expected duration: 2 hours per participant

EXPERIMENT 2: Translation Fidelity Comparison
----------------------------------------------
Hypothesis: LAMAGUE-mediated translations preserve more experiential 
  meaning than conventional (Google/DeepL) translations.
Method:
  1. Select 20 "untranslatable" concepts across 5 languages
  2. For each: produce (a) conventional translation, (b) LAMAGUE translation
  3. Native speakers rate both for "experiential fidelity" (1-7)
  4. Compare mean scores: LAMAGUE vs conventional
Falsification: If conventional scores >= LAMAGUE scores, the 
  LAMAGUE approach adds no value over existing methods.
Statistical test: Paired t-test, alpha = 0.05
Sample size: 100 (20 per language)

EXPERIMENT 3: Invariant Breaking Detection
-------------------------------------------
Hypothesis: Broken invariants correlate with bad translations.
Method:
  1. Create 30 translation pairs: 15 good, 15 with deliberately 
     broken invariants
  2. LAMAGUE system rates each (VALID / WRONG)
  3. Human raters rate each for accuracy (1-7)
  4. Measure correlation between LAMAGUE verdicts and human ratings
Falsification: If correlation < 0.5, invariant checking does not 
  predict translation quality.
Statistical test: Pearson r, alpha = 0.05
Sample size: 60 raters (30 per language pair)

EXPERIMENT 4: Chiral Complement Validation
-------------------------------------------
Hypothesis: Proposed chiral pairs are recognized as "opposite but 
  complementary" by speakers of both languages.
Method:
  1. Present 10 proposed chiral pairs to bilingual speakers
  2. Ask: "Are these concepts (a) similar, (b) opposite, (c) unrelated?"
  3. Record response + confidence
Falsification: If <60% select "opposite/complementary," the chiral 
  claim is unsupported.
Sample size: 40 bilingual speakers

EXPERIMENT 5: Round-Trip Enrichment
-------------------------------------
Hypothesis: Concepts translated through LAMAGUE and back gain depth.
Method:
  1. Take 10 concepts, translate via LAMAGUE to a target language
  2. Translate back to source language via LAMAGUE
  3. Present original + round-tripped version to native speakers
  4. Ask: "Which version captures MORE of the concept's meaning?"
Falsification: If <=50% select the round-tripped version (chance level),
  enrichment does not occur.
Statistical test: Binomial test against 50% baseline
Sample size: 50 per concept
""")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("LAMAGUE Translation Engine v1.0")
    print("Mackenzie Conor James Clark / Lycheetah Foundation")
    print()
    
    # Run all falsification tests
    results = run_falsification_tests()
    
    # Print experimental protocol
    print_experimental_protocol()
    
    # Export results as JSON for further analysis
    engine = LAMAGUETranslator()
    
    # Run a complete translation example
    print("=" * 70)
    print("FULL TRANSLATION EXAMPLE: Shadow (EN) → 阴藏我 (ZH)")
    print("=" * 70)
    
    shadow_zh = Decomposition(
        "阴藏我 (yīn cáng wǒ)", "Mandarin",
        [("Ψ", 0.7), ("∅", 0.85), ("↯", 0.65), ("Ω", 0.55)],
        0.80, "Hidden dark self"
    )
    
    result = engine.round_trip("shadow_jungian", shadow_zh)
    validation = engine.validate_translation(result)
    
    print(f"\n  Source:        {result['original']['term']} ({result['original']['language']})")
    print(f"  Decomposition: {result['original']['decomposition']}")
    print(f"  SpL:           {result['original']['spoken']}")
    print(f"\n  Target:        {result['translated']['term']} ({result['translated']['language']})")
    print(f"  Decomposition: {result['translated']['decomposition']}")
    print(f"  SpL:           {result['translated']['spoken']}")
    print(f"\n  Fidelity:      {result['metrics']['fidelity']:.4f}")
    print(f"  Enrichment:    {result['metrics']['enrichment']:.4f}")
    print(f"  Invariants:    {result['metrics']['invariants_passed']}/{result['metrics']['invariants_total']}")
    print(f"  Verdict:       {validation['verdict']}")
    print(f"  Reason:        {validation['reason']}")
    
    # Save full results
    output = {
        "engine_version": "1.0",
        "primitives_count": len(PRIMITIVES),
        "concepts_count": len(CONCEPT_DB),
        "translation_log": engine.translation_log,
        "concept_vectors": {k: v.vector.tolist() for k, v in CONCEPT_DB.items()},
    }
    
    # Convert numpy types for JSON
    def convert(obj):
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            c = convert(obj)
            if c is not obj:
                return c
            return super().default(obj)
    
    with open("/home/claude/lamague_results.json", "w") as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    
    print(f"\n  Results exported to lamague_results.json")
    print(f"\n  WHAT THIS PROVES: Internal consistency of the framework.")
    print(f"  WHAT THIS DOES NOT PROVE: External validity with humans.")
    print(f"  NEXT STEP: Run Experiments 1-5 with human participants.")
