
### ctl, base polish

| Newton step | max abs F before | after | dz before | dz after | lam | Delta moved by | seconds |
|---|---|---|---|---|---|---|---|
| 0 | 6.61e-48 | 2.45e-78 | 8.42e-39 | 2.62e-65 | 1 | -6.96e-46 | 101 |
| 1 (the check) | 2.45e-78 | converged | | | | | |

ending: {'steps': 2, 'F': 2.5e-78, 'converged': True}

### A, base polish

| Newton step | max abs F before | after | dz before | dz after | lam | Delta moved by | seconds |
|---|---|---|---|---|---|---|---|
| 0 | 6.61e-48 | 2.45e-78 | 8.42e-39 | 2.62e-65 | 1 | -6.96e-46 | 102 |
| 1 (the check) | 2.45e-78 | converged | | | | | |

ending: {'steps': 2, 'F': 2.5e-78, 'converged': True}

### A, attempt a = 0.125 to D 112.875

| Newton step | max abs F before | after | dz before | dz after | lam | Delta moved by | seconds |
|---|---|---|---|---|---|---|---|
| 0 | 1.21e-35 | 1.96e-22 | 7.48e-11 | 6.67e-22 | 1 | +1.96e-17 | 97 |
| 1 | 1.96e-22 | 1.11e-40 | 6.67e-22 | 2.90e-23 | 1 | -1.85e-28 | 111 |
| 2 | 1.11e-40 | 2.98e-47 | 2.90e-23 | 4.77e-44 | 1 | -6.45e-30 | 104 |
| 3 | 2.98e-47 | 7.83e-89 | 4.77e-44 | 5.25e-70 | 1 | -1.43e-51 | 123 |
| 4 (the check) | 7.83e-89 | converged | | | | | |

ending: {'steps': 5, 'F': 7.8e-89, 'converged': True}

### B, base polish

| Newton step | max abs F before | after | dz before | dz after | lam | Delta moved by | seconds |
|---|---|---|---|---|---|---|---|
| 0 | 6.61e-48 | 2.45e-78 | 8.42e-39 | 2.62e-65 | 1 | -6.96e-46 | 176 |
| 1 (the check) | 2.45e-78 | converged | | | | | |

ending: {'steps': 2, 'F': 2.5e-78, 'converged': True}

### B, attempt a = 0.250 to D 113.0

| Newton step | max abs F before | after | dz before | dz after | lam | Delta moved by | seconds |
|---|---|---|---|---|---|---|---|
| 0 | 1.86e-35 | 7.59e-22 | 1.48e-10 | 2.49e-21 | 1 | +3.46e-17 | 121 |
| 1 | 7.59e-22 | 3.53e-39 | 2.49e-21 | 3.51e-22 | 1 | -5.47e-28 | 110 |
| 2 | 3.53e-39 | 4.30e-45 | 3.51e-22 | 4.55e-42 | 1 | -1.17e-28 | 104 |
| 3 | 4.30e-45 | 7.25e-85 | 4.55e-42 | 9.00e-66 | 1 | +1.99e-49 | 103 |
| 4 (the check) | 7.25e-85 | converged | | | | | |

ending: {'steps': 5, 'F': 7.3e-85, 'converged': True}

### #726's quad-double attempts from D 112.75 (I726-win/table_726_out.md)

| a | from -> to | the re-seeded prediction's qd max abs F | after the first full step | corrector steps | final qd max abs F | outcome |
|---|---|---|---|---|---|---|
| 0.25 | 112.7500 -> 113.0000 | 1.20e-35 | 1.05e-21 | 8 | 2.90e-44 | REFUSED |
| 0.125 | 112.7500 -> 112.8750 | 1.09e-35 | 2.72e-22 | 5 | 1.10e-44 | REFUSED |
| 0.0625 | 112.7500 -> 112.8125 | 1.43e-35 | 6.81e-23 | 9 | 7.80e-44 | REFUSED |
| 0.03125 | 112.7500 -> 112.7812 | 1.86e-35 | 1.70e-23 | 7 | 6.60e-44 | REFUSED |
