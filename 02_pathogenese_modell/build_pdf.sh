#!/bin/bash
clear

echo Merging Agentic Version
./02_pathogenese_modell/build.sh


echo Generate PDF version
 
cat "02_pathogenese_modell.md" |
sed 's/ℏ/$\\hbar$/g' |
sed 's/↔/$\\leftrightarrow$/g' |
sed 's/⇒/$\\Rightarrow$/g' |
sed 's/⇔/$\\Leftrightarrow$/g' |
sed 's/∝/$\\propto$/g' |
sed 's/∩/$\\cap$/g' |
sed 's/∼/$\\sim$/g' |
sed 's/≙/$\\widehat{=}$/g' |
sed 's/≪/$\\ll$/g' |
sed 's/⊥/$\\perp$/g' |
sed 's/☉/$\\odot$/g' |
sed 's/𝜅/$\\kappa$/g' |
sed 's/ϰ/$\\kappa$/g' |
sed 's/𝜌/$\\rho$/g' |
sed 's/ϱ/$\\rho$/g' |
sed 's/→/$\\textrightarrow$/g' |
sed 's/↑/$\\textuparrow$/g' |
sed 's/↓/$\\textdownarrow$/g' |
sed 's/✓/$\\checkmark$/g' |
sed 's/✗/$\\texttimes$/g' |
sed 's/^\*\*\*$/\\pagebreak/' |
pandoc --output="output/Pathogenese Modell.full.pdf" -s -d scripts/pandoc.yml 