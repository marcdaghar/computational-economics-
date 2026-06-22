"""
Urban scaling models for economic diversity and governance.
"""

import numpy as np
from scipy.optimize import curve_fit

class ScalingModel:
    """
    Urban scaling laws for diversity and governance.
    
    Key relationships:
        Diversity(N) ∝ N^β
        N_f = η · N
        f(x) = A · x^(-γ) · e^(-x/x₀)
        N_c ∝ N^(β_c)
        G(N) ∝ N^(β_G)
    """
    
    def __init__(self, beta=0.92, eta=21.6, gamma=0.49, x0=211.0,
                 beta_agri=0.85, beta_retail=1.01, beta_finance=1.15,
                 beta_G_guild=0.85, beta_G_jacobin=1.00, beta_G_metro=1.15):
        """
        Args:
            beta: Overall scaling exponent for diversity
            eta: Universal constant for establishments per capita
            gamma: Zipf exponent
            x0: Cutoff scale
            beta_agri: Agriculture scaling exponent
            beta_retail: Retail scaling exponent
            beta_finance: Finance scaling exponent
            beta_G_guild: Guild governance exponent
            beta_G_jacobin: Jacobin governance exponent
            beta_G_metro: Metropolis governance exponent
        """
        self.beta = beta
        self.eta = eta
        self.gamma = gamma
        self.x0 = x0
        
        self.beta_agri = beta_agri
        self.beta_retail = beta_retail
        self.beta_finance = beta_finance
        
        self.beta_G_guild = beta_G_guild
        self.beta_G_jacobin = beta_G_jacobin
        self.beta_G_metro = beta_G_metro
        
        # Sector names
        self.sectors = ['Agriculture', 'Extraction', 'Manufacturing', 
                       'Retail', 'Finance', 'Technology']
        self.beta_sectors = [0.85, 0.82, 0.95, 1.01, 1.15, 1.20]
    
    def diversity(self, N):
        """
        Economic diversity: Diversity(N) = N^β
        """
        return N ** self.beta
    
    def establishments(self, N):
        """
        Number of economic establishments: N_f = η · N
        """
        return self.eta * N
    
    def rank_abundance(self, x):
        """
        Rank-abundance distribution: f(x) = A · x^(-γ) · e^(-x/x₀)
        """
        A = 1.0 / (self.x0 ** (1 - self.gamma) * np.math.gamma(1 - self.gamma))
        return A * x ** (-self.gamma) * np.exp(-x / self.x0)
    
    def sector_diversity(self, N, sector_index):
        """
        Diversity by sector: N_c ∝ N^(β_c)
        """
        beta_c = self.beta_sectors[sector_index]
        return N ** beta_c
    
    def government_size(self, N, beta_G):
        """
        Government size: G(N) = N^(β_G)
        """
        return N ** beta_G
    
    def governance_efficiency(self, N, beta_G):
        """
        Governance efficiency: E_G(N) = N^(β - β_G)
        """
        return N ** (self.beta - beta_G)
    
    def lambda_scaling(self, N, beta_G):
        """
        Lambda as a function of governance scale: Λ ∝ N^(β_G - 1)
        """
        return N ** (beta_G - 1)
    
    def generate_city_sizes(self, n_cities=100, min_pop=1000, max_pop=1e7):
        """
        Generate realistic city size distribution (Zipf-like).
        """
        # Power law distribution
        sizes = np.random.pareto(1.5, n_cities) * min_pop
        sizes = np.clip(sizes, min_pop, max_pop)
        sizes = np.sort(sizes)[::-1]
        return sizes
    
    def compute_metrics(self, N, beta_G):
        """
        Compute all metrics for a given population and governance exponent.
        """
        diversity_val = self.diversity(N)
        gov_size = self.government_size(N, beta_G)
        efficiency = self.governance_efficiency(N, beta_G)
        lambda_val = self.lambda_scaling(N, beta_G)
        
        return {
            'diversity': diversity_val,
            'gov_size': gov_size,
            'efficiency': efficiency,
            'lambda': lambda_val
        }

class CitySimulator(ScalingModel):
    """
    Simulator for urban systems with multiple cities.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cities = None
        self.total_population = 0
    
    def generate_cities(self, n_cities=100, min_pop=1000, max_pop=1e7):
        """
        Generate a system of cities with realistic size distribution.
        """
        self.cities = self.generate_city_sizes(n_cities, min_pop, max_pop)
        self.total_population = np.sum(self.cities)
        return self.cities
    
    def compute_system_metrics(self, beta_G):
        """
        Compute aggregate metrics for the entire system.
        """
        if self.cities is None:
            self.generate_cities()
        
        total_diversity = 0
        total_gov_size = 0
        total_efficiency = 0
        total_lambda = 0
        
        for N in self.cities:
            metrics = self.compute_metrics(N, beta_G)
            total_diversity += metrics['diversity']
            total_gov_size += metrics['gov_size']
            total_efficiency += metrics['efficiency']
            total_lambda += metrics['lambda']
        
        return {
            'total_diversity': total_diversity,
            'total_gov_size': total_gov_size,
            'total_efficiency': total_efficiency / len(self.cities),
            'total_lambda': total_lambda / len(self.cities)
        }
