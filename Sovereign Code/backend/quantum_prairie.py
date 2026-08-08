"""
Knowledge base and metadata for the Midwest Quantum Prairie ecosystem.
"""

QUANTUM_PRAIRIE_INFO = {
    "title": "The Quantum Prairie (Midwest Quantum Hub)",
    "region": "Illinois, Indiana, Wisconsin & the Great Lakes Region",
    "overview": (
        "The Quantum Prairie is the nation's premier quantum research and commercialization "
        "ecosystem, centered around Chicago, Illinois, and extending into Northwest Indiana. "
        "Anchored by federal national labs, world-class universities, state-backed infrastructure, "
        "and quantum optical fiber networks, it is positioned to be the Silicon Valley of Quantum Technology."
    ),
    "key_anchors": [
        {
            "name": "Illinois Quantum & Microelectronics Park (IQMP)",
            "location": "South Side of Chicago, IL",
            "type": "Quantum Park & Fabrication Facility",
            "highlights": "Multi-billion dollar park anchored by PsiQuantum, featuring cryogenic facilities and high-end cleanrooms."
        },
        {
            "name": "Chicago Quantum Exchange (CQE)",
            "location": "Chicago, IL",
            "type": "Research Consortium",
            "highlights": "Hub connecting UChicago, Argonne National Lab, Fermilab, UIUC, Northwestern, and UW-Madison with industry leaders like IBM."
        },
        {
            "name": "Quantum Corridor",
            "location": "Chicago, IL to Hammond, IN",
            "type": "Quantum-Safe Fiber Network",
            "highlights": "Commercial 400 Gbps quantum-safe optical network linking data centers across state lines, deployed with Quantum Computing Inc. (QUBT)."
        },
        {
            "name": "Argonne National Laboratory (Q-NEXT)",
            "location": "Lemont, IL",
            "type": "DOE National Quantum Center",
            "highlights": "National Quantum Information Science Research Center developing quantum interconnects and solid-state memories."
        },
        {
            "name": "Fermilab (SQMS Center)",
            "location": "Batavia, IL",
            "type": "Superconducting Quantum Center",
            "highlights": "Superconducting Quantum Materials and Systems Center pioneering ultra-high coherence 3D superconducting cavities."
        }
    ],
    "key_companies": [
        {
            "name": "PsiQuantum",
            "status": "Private Anchor",
            "focus": "Utility-scale photonic quantum computer building at IQMP."
        },
        {
            "name": "Infleqtion (ColdQuanta)",
            "status": "Publicly Listed (2026)",
            "focus": "Neutral-atom quantum sensors and quantum clocks with active Chicago research."
        },
        {
            "name": "Quantum Computing Inc. (QUBT)",
            "status": "Public (NASDAQ: QUBT)",
            "focus": "Dirac-3 photonic quantum optimization system integrated with Indiana Quantum Corridor."
        },
        {
            "name": "EeroQ",
            "status": "Private Startup",
            "focus": "Quantum hardware using electrons on liquid helium operating out of Chicago."
        },
        {
            "name": "IBM (IBM)",
            "status": "Public Anchor (NYSE: IBM)",
            "focus": "Founding corporate member of CQE providing quantum hardware access across Midwest research hubs."
        }
    ]
}

def get_quantum_prairie_summary():
    return QUANTUM_PRAIRIE_INFO
