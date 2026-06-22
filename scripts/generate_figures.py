#!/usr/bin/env python3
"""
Generate all figures from saved results.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
from src.scaling_model import ScalingModel
from src.governance_model import GovernanceModel
from src.visualization import FigureGenerator

def main():
    """
    Load saved results and generate figures.
    """
    print("Loading saved results...")
    
    with open('data/simulation_results.pkl', 'rb') as f:
        results = pickle.load(f)
    
    # Recreate models
    scaling_model = ScalingModel()
    governance_model = GovernanceModel()
    
    print("Generating figures...")
    fig_gen = FigureGenerator()
    fig_gen.figure_all(scaling_model, governance_model)
    
    print("All figures generated successfully!")

if __name__ == "__main__":
    main()
