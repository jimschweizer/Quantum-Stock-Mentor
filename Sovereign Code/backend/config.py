"""
Configuration and Ticker Metadata for RJ-Stock AI Quantum Platform.
"""

# Quantum Stock Universe Definitions
QUANTUM_PURE_PLAY = [
    {
        "ticker": "IONQ",
        "name": "IonQ Inc.",
        "sector": "Quantum Hardware (Trapped Ion)",
        "price": 14.85,
        "description": "Leading developer of ion-trap quantum computers with high gate fidelity.",
        "quantum_focus": "Hardware Scaling & Enterprise Cloud Access"
    },
    {
        "ticker": "RGTI",
        "name": "Rigetti Computing",
        "sector": "Quantum Hardware (Superconducting)",
        "price": 2.15,
        "description": "Full-stack quantum computing enterprise building superconducting quantum processors.",
        "quantum_focus": "Superconducting Qubits & Hybrid Algorithms"
    },
    {
        "ticker": "QBTS",
        "name": "D-Wave Quantum",
        "sector": "Quantum Annealing & Optimization",
        "price": 1.95,
        "description": "Commercial provider of quantum annealing systems specialized for logistics and optimization.",
        "quantum_focus": "Quantum Annealing & Advantage Systems"
    },
    {
        "ticker": "QUBT",
        "name": "Quantum Computing Inc.",
        "sector": "Photonic Quantum & Quantum Networks",
        "price": 4.10,
        "description": "Nanophotonics and quantum optics company deploying Dirac-3 optimization systems.",
        "quantum_focus": "Quantum Corridor Partner & Photonic Qubits"
    }
]

QUANTUM_PRAIRIE_GIANTS = [
    {
        "ticker": "IBM",
        "name": "International Business Machines",
        "sector": "Enterprise Tech & Quantum Pioneer",
        "price": 204.50,
        "description": "Founding partner of the Chicago Quantum Exchange and builder of Heron quantum processors.",
        "quantum_focus": "Qiskit Ecosystem & Midwest Hub Anchor",
        "prairie_role": "Founding corporate partner of Chicago Quantum Exchange (CQE)"
    },
    {
        "ticker": "NVDA",
        "name": "NVIDIA Corporation",
        "sector": "Accelerated Compute & Quantum Simulation",
        "price": 128.40,
        "description": "Powering quantum circuit simulation via cuQuantum and partner at IQMP.",
        "quantum_focus": "cuQuantum SDK & Hybrid Quantum GPU Supercomputing",
        "prairie_role": "AI/Quantum compute provider for Midwest research labs"
    },
    {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "sector": "Cloud & Quantum Software",
        "price": 448.20,
        "description": "Azure Quantum cloud platform and topological qubit developer.",
        "quantum_focus": "Azure Quantum & Topological Qubit Research",
        "prairie_role": "Cloud infrastructure partner for Midwest quantum startups"
    },
    {
        "ticker": "GOOGL",
        "name": "Alphabet Inc. (Google)",
        "sector": "Quantum AI & Sycamore Processor",
        "price": 178.60,
        "description": "Pioneer in quantum supremacy demonstrations with the Sycamore processor.",
        "quantum_focus": "Quantum AI & Error Correction",
        "prairie_role": "Research partner with University of Chicago quantum labs"
    }
]

ALL_TICKERS = [stock["ticker"] for stock in (QUANTUM_PURE_PLAY + QUANTUM_PRAIRIE_GIANTS)]
