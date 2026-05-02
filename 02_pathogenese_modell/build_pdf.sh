#!/bin/bash
clear

echo Merging Agentic Version
./02_pathogenese_modell/build.sh


echo Generate PDF version
 
 cd 02_pathogenese_modell
cat "../02_pathogenese_modell.md" |
sed 's/ℏ/$\\hbar$/g' |
sed 's/→/$\\to$/g' |
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
sed 's/✓/$\\checkmark$/g' |
sed 's/✗/$\\times$/g' |
sed 's$<images/$<02_pathogenese_modell/images/$g' |
sed 's/^\*\*\*$/\\pagebreak/' > "../output/02_pathogenese_modell.full.md"
#pandoc --output="../output/Pathogenese Modell.full.pdf" -s -d ../scripts/pandoc.yml

cd ..

echo --Create TEX
pandoc "output/02_pathogenese_modell.full.md" --output="output/02_pathogenese_modell.full.tex" -s -d scripts/pandoc.yml

echo --Create PDF
xelatex -interaction=batchmode -output-directory=output "output/02_pathogenese_modell.full.tex"
echo Done!
