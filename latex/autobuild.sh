#!/bin/bash
find . name - '*.tex' | entr pdflatex \\nonstopmode\\input gesamt.tex

