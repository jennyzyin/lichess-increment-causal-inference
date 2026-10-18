# Research Report: Chess Clock Increments and Timeout Losses

**Dataset:** Lichess standard rated games, January 2013  
**Study type:** Retrospective observational analysis  
**Primary outcome:** Indicator that a player lost a game by time forfeit  
**Status:** Completed descriptive, adjusted, and sensitivity analyses; causal effect **not identified**

## Executive summary

This project examines whether selecting a 2-second-per-move increment queue, relative to an otherwise matching zero-increment queue, is associated with the probability of losing on time. Comparisons are made separately at initial clocks of 120, 180, and 300 seconds. Across **29,762 games and 59,524 player-game observations**, regression-adjusted differences were **−8.35**, **−8.75**, and **−4.19 percentage points**, respectively. A game-count-weighted average across the three starting clocks was **−6.64 percentage points** (descriptive pooled summary; no pooled confidence interval).

Alternative propensity-based estimators and game-level network-aware sensitivity analyses gave similar negative associations. Within-player estimates were more negative. However, time controls are voluntarily selected, so unobserved selection and matchmaking differences remain credible rival explanations. The findings **do not establish** that an increment alone caused the observed reduction.

## 1. Research question and intervention

**Question:** How does choosing a **+2-second increment** rather than **+0** within the same starting-clock queue relate to a player's chance of losing on time, and does the association differ for 2-, 3-, and 5-minute games?

The treatment is **queue choice before matchmaking**. A different queue may expose the player to a different opponent pool; therefore the estimated queue-choice contrast should not be called a pure clock-only causal effect. The latter would require a different intervention conceptually holding opponents and playing circumstances constant.

| Stratum | Control policy | Treatment policy |
|---|---|---|
| 120 seconds | `120+0` | `120+2` |
| 180 seconds | `180+0` | `180+2` |
| 300 seconds | `300+0` | `300+2` |

Secondary comparison: `300+0` vs `300+5`, studied separately from the prespecified primary +2 contrast.

## 2. Data preparation and population

The January 2013 PGN was parsed into one game-level record and two player-level records per eligible game. The cleaned dataset contained **112,440 games** and **224,880 player-game records** before the primary exact-policy restrictions. PGNs with invalid or unsupported time controls, missing essential fields, or other exclusions specified in the preparation script were omitted; records were deduplicated by game identifier. Analysis uses pre-game ratings, UTC start timestamps, game outcomes, and PGN termination labels.

For each player-game record, `lost_on_time = 1` if `Termination == "Time forfeit"` **and** that player lost the game; otherwise it is 0. This coding avoids treating time-forfeit draws as player losses. The **primary** exact-policy cohort comprised **29,762 games**, **59,524 player-game records**, and **2,819 unique players**.

The two players from the same game receive the same increment policy. Individual players also recur in many games, so naive independent-row standard errors are inappropriate.

## 3. Descriptive comparisons

| Starting clock | No-increment games | +2-second games | Timeout-loss rate (+0) | Timeout-loss rate (+2) | Raw difference (pp) |
|---|---:|---:|---:|---:|---:|
| 120 seconds | 5,950 | 1,212 | 20.64% | 11.80% | −8.84 |
| 180 seconds | 8,243 | 1,194 | 20.79% | 12.48% | −8.31 |
| 300 seconds | 10,172 | 2,991 | 14.97% | 11.12% | −3.86 |

Rates are calculated per **player-game**, not as the probability that a game has any timeout. In the exact-policy groups, pre-adjustment player-Elo standardized mean differences were approximately **+0.072**, **−0.093**, and **−0.094** for the respective starting clocks. This indicates small *measured rating* imbalances, but does not establish exchangeability.

## 4. Identification assumptions and model strategy

To interpret a queue-choice comparison causally, one would need: (i) a consistent, well-defined intervention; (ii) conditional exchangeability given pre-selection covariates; (iii) positivity of both choices for relevant players; and (iv) outcome measurement and dependence-adjusted inference appropriate to the data. These conditions have **not** been established.

The main linear probability models regress `lost_on_time` on a +2-treatment indicator, focal-player pre-game Elo, and sine/cosine terms for UTC hour, estimated separately for each starting clock. This yields percentage-point-scale adjusted associations. The main analysis omits opponent Elo because queue choice may influence matchmaking; adjusting for opponent Elo would change the estimand toward an opponent-standardized contrast. Post-game outcomes such as number of moves, termination type, or rating change are not used as confounder adjustments.

Sensitivity methods include switching-player fixed effects, Elo-only adjustment, row-contribution limits for highly active players, inverse propensity weighting (IPW), cross-fitted augmented IPW (AIPW), a game-level dyadic sandwich variance approximation, and an illustrative binary-unmeasured-confounder bias budget.

## 5. Regression results

### 5.1 Player-level adjusted association

| Starting clock | Regression-adjusted difference (pp) | Notebook 4 two-way-cluster *diagnostic* 95% CI (pp) |
|---|---:|---:|
| 120 seconds | **−8.35** | [−11.57, −5.14] |
| 180 seconds | **−8.75** | [−11.88, −5.62] |
| 300 seconds | **−4.19** | [−6.58, −1.81] |

The intervals above are computed using the notebook's game-ID/focal-player-ID two-way clustering approximation. This approach does **not** fully capture dependence when a person appears as either participant across games. Treat these intervals as preliminary uncertainty diagnostics, not fully network-robust intervals.

The **−6.64 percentage-point** pooled adjusted association used weights **0.241, 0.317, and 0.442**, corresponding to the observed game counts in the three clock strata. The notebook did not calculate a pooled confidence interval or a standardized estimate for a separately defined target population.

### 5.2 Within-player comparisons

| Starting clock | Switching players | Fixed-effects association (pp) |
|---|---:|---:|
| 120 seconds | 312 | −14.64 |
| 180 seconds | 389 | −16.90 |
| 300 seconds | 756 | −8.50 |

The fixed-effects estimates are more negative than full-sample models. They control for stable player-level factors but do not address time-varying reasons for choosing a clock policy. They also condition on being observed under both treatments, changing the analysis population. The larger magnitude is **not** proof of a larger causal effect.

## 6. Propensity-score and doubly robust checks

| Starting clock | IPW association (pp) | Cross-fitted AIPW association (pp) | Maximum weight | Share propensity-clipped |
|---|---:|---:|---:|---:|
| 120 seconds | −8.46 | −8.28 | 8.51 | 0.00% |
| 180 seconds | −8.47 | −8.32 | 20.00 | 0.33% |
| 300 seconds | −4.07 | −4.04 | 6.11 | 0.00% |

The nuisance models included player Elo and cyclical UTC hour. Weighted standardized mean differences for these modeled covariates were all less than 0.05 in absolute magnitude. This supports **measured-covariate balance**, not the absence of unmeasured confounding. Because cross-fitting on player-game rows does not necessarily isolate repeated player histories across folds, these AIPW estimates should be read as model-based sensitivity results, not as independently validated causal estimates.

## 7. Network-aware uncertainty sensitivity

Notebook 5 modeled each game as one observation, with outcome equal to the fraction of the two players who lost on time (0 or 0.5 for a decisive timeout), and used game-level mean Elo in its adjusted model. The dyadic sandwich-variance approximation accounts for some dependence from games sharing either participant.

| Starting clock | Game-level adjusted association (pp) | Dyadic 95% CI (pp) |
|---|---:|---:|
| 120 seconds | −8.66 | [−11.43, −5.90] |
| 180 seconds | −8.51 | [−11.74, −5.29] |
| 300 seconds | −3.97 | [−6.51, −1.42] |

These are **matched estimates and intervals** from the *same game-level model*. They are not confidence intervals for the main player-level estimates in Section 5. The variance approximation does not establish that all forms of temporal or network dependence have been addressed.

## 8. Sensitivity to unmeasured confounding

Notebook 5 examined a simple additive bias-budget scenario. If a binary unmeasured factor differed in prevalence by **20 percentage points** between +2 and +0 games, the risk shift attributed to that factor would have to be about **43.3**, **42.6**, or **19.8 percentage points**, respectively, to offset the observed game-level adjusted differences at 120, 180, or 300 seconds in this stylized calculation.

The required combinations are **hypothetical**, not measured evidence that such a factor does or does not exist. The framework assumes simplified additive relations and should not be presented as a formal adjustment for hidden confounding. The smaller association at 300 seconds is more readily offset under these scenarios.

## 9. Secondary policy and effect heterogeneity

The separate `300+5` versus `300+0` regression-adjusted association was **−6.96 percentage points** (Notebook 4 two-way-cluster diagnostic 95% CI approximately **[−9.18, −4.73] pp**). This is more negative than the `300+2` contrast but does **not** establish a causal increment-dose relationship; people selecting different increments may differ systematically.

Differences in +2 associations between 120-, 180-, and 300-second starting clocks are **descriptive heterogeneity**; the project did not conduct a formal between-stratum contrast test with joint uncertainty estimation.

## 10. Limitations

- **Self-selection and unmeasured confounding.** Time-management skill, time-control preferences, fatigue, motivation, and recent form were incompletely observed.
- **Treatment definition.** Queue choice can influence opponent matching; an opponent-held-fixed clock-only treatment is not identified here.
- **Complex dependence.** Two player-game records per game and repeated players/opponents complicate inference; dyadic methods cover only some dependency patterns.
- **Observational positivity.** No extreme propensities appeared in simple measured-covariate models, but this does not establish within-player practical overlap in all relevant conditions.
- **Outcome scope.** Losing on time is distinct from game score, win rate, or overall chess performance.
- **External validity.** One month of online rated games from January 2013 may not reflect present-day platforms, matchmaking, or player populations.

## 11. Conclusion

In January 2013 Lichess games, a +2-second per-move increment queue was **consistently associated with a lower observed probability of losing on time** at starting clocks of 120, 180, and 300 seconds. Measured-covariate adjustments, IPW, AIPW, within-player comparisons, and game-level network-aware sensitivity analysis preserved the negative direction. Nevertheless, voluntary time-control selection and potential matchmaking changes prevent strong causal identification. **The magnitude of the causal effect of a 2-second increment remains unknown.**

## 12. Reproducibility and source

Source: [Lichess open database](https://database.lichess.org/), standard rated games for January 2013. The project uses a local PGN, `src/prepare_increment_data.py`, and notebooks `01_data_validation.ipynb` through `05_sensitivity_and_robust_inference.ipynb`. See the repository [README](../README.md) for commands and folder structure. Commit analysis code, figures, and lightweight tables; keep the large raw PGN and generated row-level game data locally. Verify Lichess's current dataset terms before any redistribution.
