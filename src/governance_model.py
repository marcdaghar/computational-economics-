"""
Governance models and optimization.
"""

import numpy as np
from src.scaling_model import ScalingModel

class GovernanceModel(ScalingModel):
    """
    Models for governance structure and optimization.
    
    Key relationships:
        L* = floor(log_s*(N/N₀))  # Optimal hierarchical levels
        n_g = N/N_g               # Number of guilds
        C_total = n_g·C_guild + C_coordination  # Total governance cost
        N_g* = √(α/γ · N)         # Optimal guild size
    """
    
    def __init__(self, N0=1000, s_star=7, alpha=0.01, gamma_cost=0.1,
                 C_guild_base=100, **kwargs):
        """
        Args:
            N0: Minimum viable community size
            s_star: Optimal span of control
            alpha: Coordination cost coefficient
            gamma_cost: Guild cost coefficient
            C_guild_base: Base cost per guild
        """
        super().__init__(**kwargs)
        self.N0 = N0
        self.s_star = s_star
        self.alpha = alpha
        self.gamma_cost = gamma_cost
        self.C_guild_base = C_guild_base
    
    def optimal_levels(self, N):
        """
        Optimal number of governance levels: L* = floor(log_s*(N/N₀))
        """
        if N <= self.N0:
            return 0
        return int(np.floor(np.log(N / self.N0) / np.log(self.s_star)))
    
    def number_of_guilds(self, N, N_g):
        """
        Number of guilds: n_g = N/N_g
        """
        return N / N_g
    
    def total_governance_cost(self, N, N_g):
        """
        Total governance cost: C_total = n_g·C_guild + C_coordination
        
        C_guild = C_guild_base · N_g^γ_cost
        C_coordination = α · N · N_g
        """
        C_guild = self.C_guild_base * (N_g ** self.gamma_cost)
        n_g = self.number_of_guilds(N, N_g)
        C_coordination = self.alpha * N * N_g
        
        return n_g * C_guild + C_coordination
    
    def optimal_guild_size(self, N):
        """
        Optimal guild size: N_g* = √(α/γ · N)
        """
        return np.sqrt((self.alpha / self.gamma_cost) * N)
    
    def compute_guild_metrics(self, N, N_g_range=None):
        """
        Compute guild metrics over a range of guild sizes.
        """
        if N_g_range is None:
            N_g_range = np.linspace(10, 5000, 100)
        
        costs = []
        for N_g in N_g_range:
            costs.append(self.total_governance_cost(N, N_g))
        
        N_g_opt = self.optimal_guild_size(N)
        cost_opt = self.total_governance_cost(N, N_g_opt)
        
        return {
            'N_g_range': N_g_range,
            'costs': np.array(costs),
            'N_g_opt': N_g_opt,
            'cost_opt': cost_opt
        }
    
    def compare_governance_models(self, N, models=None):
        """
        Compare different governance models.
        """
        if models is None:
            models = {
                'Guild': self.beta_G_guild,
                'Jacobin': self.beta_G_jacobin,
                'Metropolis': self.beta_G_metro
            }
        
        results = {}
        for name, beta_G in models.items():
            metrics = self.compute_metrics(N, beta_G)
            results[name] = {
                'beta_G': beta_G,
                'diversity': metrics['diversity'],
                'gov_size': metrics['gov_size'],
                'efficiency': metrics['efficiency'],
                'lambda': metrics['lambda']
            }
        
        return results
    
    def simulate_population_distribution(self, total_pop=1e7, n_cities=100):
        """
        Simulate population distribution across governance levels.
        """
        city_sizes = self.generate_city_sizes(n_cities, 1000, 5e6)
        city_sizes = city_sizes / np.sum(city_sizes) * total_pop
        
        results = []
        for N in city_sizes:
            L = self.optimal_levels(N)
            N_g_opt = self.optimal_guild_size(N)
            results.append({
                'population': N,
                'levels': L,
                'guild_size': N_g_opt,
                'n_guilds': N / N_g_opt
            })
        
        return results
