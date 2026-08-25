"""
Dempster-Shafer Theory (DST) Evidence Combination & Conflict Resolution.

Frame of Discernment:
Theta = {Real, Fake}
Subsets:
- {Real} (Belief in Authenticity)
- {Fake} (Belief in Synthetic/Manipulation)
- {Real, Fake} (Epistemic Uncertainty / Ignorance)

When forensic signals actively conflict (e.g. C2PA claims authentic, but Visual claims manipulated),
traditional Bayesian/Weighted averages silently hide the contradiction in a misleadingly confident middle score.
DST explicitly computes the conflict mass (K) and surfaces it as a named uncertainty in the report.
"""

from typing import Any, Dict, List, Tuple
import numpy as np


class BeliefMass:
    """Represents probability mass assignment over {Real, Fake, {Real, Fake}}."""
    def __init__(self, m_real: float, m_fake: float, m_uncertain: float):
        total = m_real + m_fake + m_uncertain
        self.m_real = max(0.0, m_real / total)
        self.m_fake = max(0.0, m_fake / total)
        self.m_uncertain = max(0.0, m_uncertain / total)

    def to_dict(self) -> Dict[str, float]:
        return {
            "m_real": round(self.m_real, 3),
            "m_fake": round(self.m_fake, 3),
            "m_uncertain": round(self.m_uncertain, 3),
        }


def combine_two_masses(m1: BeliefMass, m2: BeliefMass) -> Tuple[BeliefMass, float]:
    """
    Applies Dempster's Rule of Combination:
    m(A) = [sum_{B cap C = A} m1(B)*m2(C)] / (1 - K)
    where K is the conflict metric.
    """
    # Conflict mass: m1(Real)*m2(Fake) + m1(Fake)*m2(Real)
    K = (m1.m_real * m2.m_fake) + (m1.m_fake * m2.m_real)

    if K >= 0.999:  # Complete total conflict
        return BeliefMass(0.0, 0.0, 1.0), K

    normalization = 1.0 - K

    # Combine intersections
    m_real_comb = (
        (m1.m_real * m2.m_real) +
        (m1.m_real * m2.m_uncertain) +
        (m1.m_uncertain * m2.m_real)
    ) / normalization

    m_fake_comb = (
        (m1.m_fake * m2.m_fake) +
        (m1.m_fake * m2.m_uncertain) +
        (m1.m_uncertain * m2.m_fake)
    ) / normalization

    m_uncertain_comb = (m1.m_uncertain * m2.m_uncertain) / normalization

    return BeliefMass(m_real_comb, m_fake_comb, m_uncertain_comb), K


def fuse_evidence_masses(
    evidence_masses: List[BeliefMass],
) -> Tuple[BeliefMass, float, List[Dict[str, Any]]]:
    """
    Fuses multiple independent evidence sources sequentially via DST.
    Returns:
        (fused_mass, max_conflict_detected, conflict_log)
    """
    if not evidence_masses:
        return BeliefMass(0.0, 0.0, 1.0), 0.0, []

    current_mass = evidence_masses[0]
    total_conflict = 0.0
    conflict_log = []

    for i in range(1, len(evidence_masses)):
        next_mass = evidence_masses[i]
        fused, conflict_k = combine_two_masses(current_mass, next_mass)

        if conflict_k > 0.25:
            conflict_log.append({
                "step": i,
                "conflict_metric_K": round(conflict_k, 3),
                "severity": "HIGH" if conflict_k > 0.50 else "MODERATE",
            })

        total_conflict = max(total_conflict, conflict_k)
        current_mass = fused

    return current_mass, total_conflict, conflict_log
