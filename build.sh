pandoc paper.md -o paper.pdf \
    --filter pandoc-eqnos \
    --filter pandoc-fignos \
    --filter pandoc-tablenos \
    --filter pandoc-citeproc \
    --template default.latex \
    --bibliography "../references-master/papers-library.bib" \

open paper.pdf
