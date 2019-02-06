#!/bin/bash
find -L . -type f -name '*.tex' -or -name '*.pdf' -and ! -name 'gesamt.pdf'  | entr pdflatex \\nonstopmode\\input gesamt.tex

