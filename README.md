# Computational Economics and Optimal Decentralization

This repository contains the code for the paper "Computational Economics and Optimal Decentralization: Scaling Laws, Guilds, and the Size of Government" by Marc Daghar.

## Overview

The framework implements:
1. Urban scaling laws: Diversity(N) ∝ N^β
2. Government scaling: G(N) ∝ N^(β_G)
3. Optimal guild size: N_g* = √(α/γ · N)
4. Lambda scaling: Λ ∝ N^(β_G - 1)
5. Stability condition: β_G < 1 ⇔ Λ → 0

## Requirements

```bash
pip install -r requirements.txt
