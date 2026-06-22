"""
Guild optimization and multi-level governance analysis.
"""

import numpy as np
from scipy.optimize import minimize

class GuildOptimizer:
    """
    Optimization of guild structures and governance hierarchy.
    """
    
    def __init__(self, governance_model):
        self.model = governance_model
    
    def objective_function(self, N_g, N):
        """
        Objective function for guild optimization.
        Minimizes total governance cost.
        """
        return self.model.total_governance_cost(N, N_g)
    
    def optimize_guild_size(self, N, bounds=(10, 10000)):
        """
        Numerically optimize guild size.
        """
        result = minimize(
            lambda x: self.objective_function(x[0], N),
            x0=[self.model.optimal_guild_size(N)],
            bounds=[bounds],
            method='L-BFGS-B'
        )
        return result.x[0], result.fun
    
    def optimize_hierarchy(self, total_pop, levels, bounds=None):
        """
        Optimize population distribution across hierarchical levels.
        """
        if bounds is None:
            bounds = [(100, 100000)] * levels
        
        def objective(pops):
            total_cost = 0
            for N in pops:
                N_g_opt = self.model.optimal_guild_size(N)
                total_cost += self.model.total_governance_cost(N, N_g_opt)
            return total_cost
        
        # Initial guess: equal distribution
        x0 = [total_pop / levels] * levels
        
        # Constraint: sum of populations = total_pop
        constraint = {'type': 'eq', 'fun': lambda x: np.sum(x) - total_pop}
        
        result = minimize(
            objective,
            x0,
            bounds=bounds,
            constraints=[constraint],
            method='SLSQP'
        )
        
        return result.x, result.fun
    
    def compute_efficiency_landscape(self, N_range, N_g_range):
        """
        Compute efficiency landscape over N and N_g.
        """
        N_grid, N_g_grid = np.meshgrid(N_range, N_g_range)
        efficiency_grid = np.zeros_like(N_grid)
        lambda_grid = np.zeros_like(N_grid)
        
        for i in range(len(N_range)):
            for j in range(len(N_g_range)):
                N = N_range[i]
                N_g = N_g_grid[j, i]
                cost = self.model.total_governance_cost(N, N_g)
                # Efficiency = 1 / cost (simplified)
                efficiency_grid[j, i] = 1.0 / (cost + 1e-10)
                lambda_grid[j, i] = self.model.lambda_scaling(N, 0.9)
        
        return N_grid, N_g_grid, efficiency_grid, lambda_grid
