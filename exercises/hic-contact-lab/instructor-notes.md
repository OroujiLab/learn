# Instructor notes — Hi-C contact-map laboratory

**Use:** Instructor guide for a self-paced or instructor-led teaching exercise. **Data:** Entirely simulated 240-kb region; no experimental or patient data.

## Core explanations students should provide

- A contact map summarizes proximity-ligation pairs from a population. It is not a physical distance map or a snapshot of an individual nucleus.
- Higher count depth improves sampling stability, but does not change bin width, genomic mapping properties, or the biological assay itself.
- Coarse binning pools counts: visibly smoother patterns can come at the cost of position accuracy.
- Raw counts carry distance decay; simple O/E removes the average by separation from the **synthetic matrix** only. It is not ICE/KR, and the displayed value is not a loop-calling significance score.
- Inter-domain and intra-domain patterns reflect the simulator's chosen functions, not real TADs. Highlighted blue focal cells indicate *programmed enrichments*, not inferred loops.
- Focal contact enrichment does not establish enhancer target specificity or clinical actionability.

## Assessment rubric (10 points)

| Criterion | Points |
|---|---:|
| Identifies proximity-ligation measurement and avoids physical-distance claim | 2 |
| Explains distinction between depth and binning | 2 |
| Separates raw, O/E and matrix balancing | 2 |
| Provides cautious focal-interaction interpretation | 2 |
| Proposes replication and functional tests | 2 |

## Recommended discussion

Ask students to identify a plausible artifact (low coverage, map bias, alignment filtering, sample heterogeneity). Then ask which experimental evidence could independently establish target-gene regulation in a CRC organoid and what matched controls are necessary.

## Caution

The sampler uses synthetic counts generated from a chosen distance-decay function, three programmed blocks and one focal enrichment. It intentionally omits actual library-generation and correction for genomic biases. The simulation should **never** be used to choose real sequencing depth or make quantitative benchmarking claims.

## Primary literature

- Lieberman-Aiden et al. (2009), doi:10.1126/science.1181369.
- Rao et al. (2014), doi:10.1016/j.cell.2014.11.021.
- Forcato et al. (2017), doi:10.1038/nmeth.4325.
