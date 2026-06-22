#!/usr/bin/env python3
"""
Run scaling and governance simulations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pickle
from src.scaling_model import ScalingModel
from src.governance_model import GovernanceModel
from src.guild_optimization import GuildOptimizer
from src.visualization import FigureGenerator

def run_simulations():
    """
    Run all simulations.
    """
    print("=" * 60)
    print("Running Scaling and Governance Simulations...")
    print("=" * 60)
    
    # Initialize models
    scaling_model = ScalingModel()
    governance_model = GovernanceModel()
    
    # Generate city system
    city_sim = ScalingModel()
    cities = city_sim.generate_cities(n_cities=100)
    
    print(f"\nCity System Generated:")
    print(f"  Number of cities: {len(cities)}")
    print(f"  Total population: {np.sum(cities):.0f}")
    print(f"  Largest city: {cities[0]:.0f}")
    print(f"  Smallest city: {cities[-1]:.0f}")
    
    # Compute metrics for different governance models
    print("\n" + "=" * 60)
    print("Governance Model Comparison:")
    print("=" * 60)
    
    N_big = 1e7
    models = ['Guild', 'Jacobin', 'Metropolis']
    beta_Gs = [scaling_model.beta_G_guild, 
               scaling_model.beta_G_jacobin, 
               scaling_model.beta_G_metro]
    
    for name, beta_G in zip(models, beta_Gs):
        metrics = scaling_model.compute_metrics(N_big, beta_G)
        print(f"\n  {name}:")
        print(f"    beta_G = {beta_G:.2f}")
        print(f"    Efficiency = {metrics['efficiency']:.2e}")
        print(f"    Lambda = {metrics['lambda']:.2e}")
        print(f"    Stable = {beta_G < 1}")
    
    # Run guild optimization
    print("\n" + "=" * 60)
    print("Guild Optimization:")
    print("=" * 60)
    
    N_test = 100000
    N_g_opt = governance_model.optimal_guild_size(N_test)
    cost_opt = governance_model.total_governance_cost(N_test, N_g_opt)
    
    print(f"\n  For population N = {N_test}:")
    print(f"    Optimal guild size: {N_g_opt:.0f}")
    print(f"    Number of guilds: {N_test / N_g_opt:.0f}")
    print(f"    Minimum cost: {cost_opt:.0f}")
    
    # Save results
    os.makedirs('data', exist_ok=True)
    
    results = {
        'cities': cities,
        'scaling_model': scaling_model,
        'governance_model': governance_model,
        'N_big': N_big,
        'models': models,
        'beta_Gs': beta_Gs,
        'N_test': N_test,
        'N_g_opt': N_g_opt,
        'cost_opt': cost_opt
    }
    
    with open('data/simulation_results.pkl', 'wb') as f:
        pickle.dump(results, f)
    
    print("\n" + "=" * 60)
    print("Simulations complete. Results saved.")
    print("=" * 60)
    
    return scaling_model, governance_model

def main():
    """
    Main execution function.
    """
    scaling_model, governance_model = run_simulations()
    
    # Generate figures
    print("\nGenerating figures...")
    fig_gen = FigureGenerator()
    fig_gen.figure_all(scaling_model, governance_model)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
