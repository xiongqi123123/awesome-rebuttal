# Built-in One-Page Rebuttal Template

This asset is bundled with `awesome-rebuttal` as a **fallback ECCV/CVPR-style two-column one-page rebuttal template**.

Use an official venue/year template whenever the user provides one or an official source is found and confirmed. If this fallback is used for another venue, adapt conference name/year, paper ID, title policy, and rule text to the user-confirmed instructions. Never present this bundled fallback as an official template unless the user has confirmed that it matches the target venue's official instructions.

## Provenance

The source template is based on the ECCV/CVPR rebuttal author-kit style.

**History** (in reverse chronological order):
- Updated and fixed for ECCV 2024 by [Stefan Roth](https://github.com/sroth-visinf)
- Adopted rebuttal template from [CVPR 2024 templates](https://github.com/cvpr-org/author-kit)


## Instructions
- Modify the example document `rebuttal.tex` following the instructions therein
- Please make sure to look at all `TODO REBUTTAL` comments, which provide important instructions and todos
- Either compile with `pdflatex` as

        pdflatex rebuttal
        bibtex rebuttal
        pdflatex rebuttal
        pdflatex rebuttal

    or compile with plain `latex` as

        latex rebuttal
        bibtex rebuttal
        latex rebuttal
        latex rebuttal
        dvips rebuttal
        pstopdf rebuttal.ps
