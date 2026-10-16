# Instructor guide — local-to-HPC

Learning outcome: distinguish reproducibility, correctness and successful execution. Run the four-read synthetic parser locally, change one quality character, and compare outputs. Encourage students to consider sample tracking and checksums rather than treating job success as proof of biological validity.

Before a cluster demonstration, confirm allocation policies, Python availability, working directory, scheduler flags and whether running a small classroom job is allowed. Do not execute batch submissions to shared resources without local permission.

Discussion points: Phred+33 is a base-quality encoding; read quality is not ATAC-specific library quality. Mixing coordinate systems or reference genomes can invalidate downstream interpretation. The mock file is not representative of realistic sequencing data.
