pandoc paper.md -o paper.pdf \
    --filter pandoc-eqnos \
    --filter pandoc-fignos \
    --filter pandoc-tablenos \
    --filter pandoc-citeproc \
    --bibliography "../references-master/papers-library.bib" \
    --template "../pandoc-templates/default.latex" \

open paper.pdf
