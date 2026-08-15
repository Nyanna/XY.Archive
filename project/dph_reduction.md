Prüfe für den angefügten Mechanismus die Potenz und Selektivität von DPH. Ziel ist eine Dosisreduktion bei Erhalt des gewünschten Effektes der Limitierung der Salven.

# Mechanismus

**DPH-positiv → Membranstabilisierung, nicht Antihistaminik.** Diphenhydramin ist ein **use-dependent, inaktivierungs-selektiver Na⁺-Kanal-Blocker**: Kd ~10 µM am inaktivierten, >300 µM am Ruhekanal; „*profound use-dependent block when repeatedly stimulated with high-frequency depolarizing pulses*" (Kuo et al., Mol Pharmacol 2000; Kim et al., Brain Res 2000). Es teilt sich das Diphenyl-Pharmakophor mit **Phenytoin, Imipramin, Benztropin**. Das ist exakt die Biophysik, die Sie brauchen: bei normaler Frequenz nahezu stumm, bei der HR>130-Salve progressiv abklemmend. **DPH wirkt also vermutlich als „lokalanästhetischer" Membranstabilisator auf die NTS/LC-Salve, nicht über H1 und nicht über Muskarin.**
SystemInit:  id=67218be4-c64d-4874-9a1a-83ded32ffa70, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
Control Request:
```yaml
id: 5f72f753-c20b-468e-a211-a3222102cb62
toolName: openalex-search
arguments:
  query: diphenhydramine use-dependent sodium channel block inactivated state
  reason: Verify Kd values and mechanism of DPH Na+ channel block
  fields: abstract
```
/answer 5f72f753-c20b-468e-a211-a3222102cb62 allow
Control Request:
```yaml
id: 877f9d27-e1e2-458a-af0e-452060caa6dd
result:
  structuredContent:
    count: 113
    returned: 25
    page: 1
    per_page: 25
    results:
    - id: https://openalex.org/W2137618884
      doi: https://doi.org/10.1093/cvr/cvr044
      title: Simulation of multiple ion channel block provides improved early prediction of compounds’ clinical torsadogenic risk
      publication_year: 2011
      relevance_score: 259.22232
      abstract: "AIMS: The level of inhibition of the human Ether-à-go-go-related gene (hERG) channel is one of the earliest preclinical markers used to predict the risk of a compound causing Torsade-de-Pointes (TdP) arrhythmias. While avoiding the use of drugs with maximum therapeutic concentrations within 30-fold of their hERG inhibitory concentration 50% (IC(50)) values has been suggested, there are drugs that are exceptions to this rule: hERG inhibitors that do not cause TdP, and drugs that can cause TdP but are not strong hERG inhibitors. In this study, we investigate whether a simulated evaluation of multi-channel effects could be used to improve this early prediction of TdP risk. METHODS AND RESULTS: We collected multiple ion channel data (hERG, Na, L-type Ca) on 31 drugs associated with varied risks of TdP. To integrate the information on multi-channel block, we have performed simulations with a variety of mathematical models of cardiac cells (for rabbit, dog, and human ventricular myocyte models). Drug action is modelled using IC(50) values, and therapeutic drug concentrations to calculate the proportion of blocked channels and the channel conductances are modified accordingly. Various pacing protocols are simulated, and classification analysis is performed to evaluate the predictive power of the models for TdP risk. We find that simulation of action potential duration prolongation, at therapeutic concentrations, provides improved prediction of the TdP risk associated with a compound, above that provided by existing markers. CONCLUSION: The suggested calculations improve the reliability of early cardiac safety assessments, beyond those based solely on a hERG block effect."
    - id: https://openalex.org/W2113927644
      doi: https://doi.org/10.1016/s0008-6363(02)00846-5
      title: "Relationships between preclinical cardiac electrophysiology, clinical QT interval prolongation and torsade de pointes for a broad range of drugs: evidence for a provisional safety margin in drug development"
      publication_year: 2003
      relevance_score: 213.70251
      abstract: "OBJECTIVE: To attempt to determine the relative value of preclinical cardiac electrophysiology data (in vitro and in vivo) for predicting risk of torsade de pointes (TdP) in clinical use. METHODS: Published data on hERG (or I(Kr)) activity, cardiac action potential duration (at 90% repolarisation; APD(90)), and QT prolongation in dogs were compared against QT effects and reports of TdP in humans for 100 drugs. These data were set against the free plasma concentrations attained during clinical use (effective therapeutic plasma concentrations; ETPC(unbound)). The drugs were divided into five categories: (1) Class Ia and III antiarrhythmics; (2) Withdrawn from market due to TdP; (3) Measurable incidence/numerous reports of TdP in humans; (4) Isolated reports of TdP in humans; (5) No reports of TdP in humans. RESULTS: Data from hERG (or I(Kr)) assays in addition to ETPC(unbound) data were available for 52 drugs. For Category 1 drugs, data for hERG/I(Kr) IC(50), APD(90), QTc in animals and QTc in humans were generally close to or superimposed on the ETPC(unbound) values. This relationship was uncoupled in the other categories, with more complex relationships between the data. In Category 1 (except amiodarone), the ratios between hERG/I(Kr) IC(50) and ETPC(unbound) (max) ranged from 0.1- to 31-fold. Similar ranges were obtained for drugs in Category 2 (0.31- to 13-fold) and Category 3 (0.03- to 35-fold). A large spread was found for Category 4 drugs (0.13- to 35700-fold); this category embraced an assortment of mechanisms ranging from drugs which may well be affecting I(Kr) currents in clinical use (e.g. sparfloxacin) to others such as nifedipine (35700-fold) where channel block is not involved. Finally, for the majority of Category 5 drugs there was a >30-fold separation between hERG/I(Kr) activity and ETPC(unbound) values, with the notable exception of verapamil (1.7-fold), which is free from QT prolongation in man; this is probably explained by its multiple interactions with cardiac ion channels. CONCLUSIONS: The dataset confirms the widely-held belief that most drugs associated with TdP in humans are also associated with hERG K(+) channel block at concentrations close to or superimposed upon the free plasma concentrations found in clinical use. A 30-fold margin between C(max) and hERG IC(50) may suffice for drugs currently undergoing clinical evaluation, but for future drug discovery programmes, pharmaceutical companies should consider increasing this margin, particularly for drugs aimed at non-debilitating diseases. However, interactions with multiple cardiac ion channels can either mitigate or exacerbate the prolongation of APD and QT that would ensue from block of I(Kr) currents alone, and delay of repolarisation per se is not necessarily torsadogenic. Clearly, an integrated assessment of in vitro and in vivo data is required in order to predict the torsadogenic risk of a new candidate drug in humans."
    - id: https://openalex.org/W2055531039
      doi: https://doi.org/10.1016/0079-6107(85)90005-7
      title: Batrachotoxin as a tool to study voltage-sensitive sodium channels of excitable membranes
      publication_year: 1985
      relevance_score: 211.9555
    - id: https://openalex.org/W1977762789
      doi: https://doi.org/10.1038/sj.bjp.0706058
      title: "V102862 (Co 102862): a potent, broad‐spectrum state‐dependent blocker of mammalian voltage‐gated sodium channels"
      publication_year: 2005
      relevance_score: 190.80219
      abstract: "1. 4-(4-Fluorophenoxy)benzaldehyde semicarbazone (V102862) was initially described as an orally active anticonvulsant with robust activity in a variety of rodent models of epilepsy. The mechanism of action was not known. We used whole-cell patch-clamp techniques to study the effects of V102862 on native and recombinant mammalian voltage-gated Na+ channels. 2. V102862 blocked Na+ currents (I(Na)) in acutely dissociated cultured rat hippocampal neurons. Potency increased with membrane depolarization, suggesting a state-dependent mechanism of inhibition. There was no significant effect on the voltage dependence of activation of I(Na). 3. The dissociation constant for the inactivated state (K(I)) was approximately 0.6 microM, whereas the dissociation constant for the resting state (K(R)) was >15 microM. 4. The binding to inactivated channels was slow, requiring a few seconds to reach steady state at -80 mV. 5. The mechanism of inhibition was characterized in more detail using human embryonic kidney-293 cells stably expressing rat brain type IIA Na+ (rNa(v)1.2) channels, a major Na+ channel alpha subunit in rat hippocampal neurons. Similar to hippocampal neurons, V102862 was a potent state-dependent blocker of rNa(v)1.2 channels with a K(I) of approximately 0.4 microM and K(R) approximately 30 microM. V102862 binding to inactivated channels was relatively slow (k(+) approximately = 1.7 microM(-1) s(-1)). V102862 shifted the steady-state availability curve in the hyperpolarizing direction and significantly retarded recovery of Na+ channels from inactivation. 6. These results suggest that inhibition of voltage-gated Na+ channels is a major mechanism underlying the anticonvulsant properties of V102862. Moreover, understanding the biophysics of the interaction may prove to be useful in designing a new generation of potent Na+ channel blocker therapeutics."
    - id: https://openalex.org/W1134233855
      doi: https://doi.org/10.1007/s13181-015-0483-y
      title: A Literature Review of the Use of Sodium Bicarbonate for the Treatment of QRS Widening
      publication_year: 2015
      relevance_score: 182.35576
    - id: https://openalex.org/W2022126452
      doi: https://doi.org/10.1007/s00210-002-0669-0
      title: "Inhibition of skeletal muscle sodium currents by mexiletine analogues: specific hydrophobic interactions rather than lipophilia per se account for drug therapeutic profile"
      publication_year: 2003
      relevance_score: 87.15315
    - id: https://openalex.org/W2783919199
      doi: https://doi.org/10.1002/med.21476
      title: Comprehensive review of cardiovascular toxicity of drugs and related agents
      publication_year: 2018
      relevance_score: 82.7227
      abstract: "Cardiovascular diseases are a leading cause of morbidity and mortality in most developed countries of the world. Pharmaceuticals, illicit drugs, and toxins can significantly contribute to the overall cardiovascular burden and thus deserve attention. The present article is a systematic overview of drugs that may induce distinct cardiovascular toxicity. The compounds are classified into agents that have significant effects on the heart, blood vessels, or both. The mechanism(s) of toxic action are discussed and treatment modalities are briefly mentioned in relevant cases. Due to the large number of clinically relevant compounds discussed, this article could be of interest to a broad audience including pharmacologists and toxicologists, pharmacists, physicians, and medicinal chemists. Particular emphasis is given to clinically relevant topics including the cardiovascular toxicity of illicit sympathomimetic drugs (e.g., cocaine, amphetamines, cathinones), drugs that prolong the QT interval, antidysrhythmic drugs, digoxin and other cardioactive steroids, beta-blockers, calcium channel blockers, female hormones, nonsteroidal anti-inflammatory, and anticancer compounds encompassing anthracyclines and novel targeted therapy interfering with the HER2 or the vascular endothelial growth factor pathway."
    - id: https://openalex.org/W2108712957
      doi: https://doi.org/10.1016/j.tiv.2014.11.010
      title: In vitro detection of cardiotoxins or neurotoxins affecting ion channels or pumps using beating cardiomyocytes as alternative for animal testing
      publication_year: 2014
      relevance_score: 79.0533
    - id: https://openalex.org/W2560528760
      doi: https://doi.org/10.1016/j.vascn.2016.12.003
      title: A new paradigm for drug-induced torsadogenic risk assessment using human iPS cell-derived cardiomyocytes
      publication_year: 2016
      relevance_score: 74.688286
      abstract: "INTRODUCTION: Human induced pluripotent stem cell-derived cardiomyocytes (hiPSC-CMs) are anticipated to be a useful tool for conducting proarrhythmia risk assessments of drug candidates. However, a torsadogenic risk prediction paradigm using hiPSC-CMs has not yet been fully established. METHODS: Extracellular field potentials (FPs) were recorded from hiPSC-CMs using the multi-electrode array (MEA) system. The effects on FPs were evaluated with 60 drugs, including 57 with various clinical torsadogenic risks. Actual drug concentrations in medium were measured using the equilibrium dialysis method with a Rapid Equilibrium Dialysis device. Relative torsade de pointes (TdP) scores were determined for each drug according to the degree of FP duration prolongation and early afterdepolarization occurrence. The margins were calculated from the free concentration in medium and free effective therapeutic plasma concentration. Each drug's results were plotted on a two-dimensional map of relative TdP risk scores versus margins. RESULTS: Each drug was categorised as high, intermediate, or low risk based on its location within predefined areas of the two-dimensional map. We categorised 19 drugs as high risk; 18 as intermediate risk; and 17 as low risk. We examined the concordance between our categorisation of high and low risk drugs against the torsadogenic risk categorisation in CredibleMeds®. Our system demonstrated high concordance, as reflected in a sensitivity of 81%, specificity of 87%, and accuracy of 83%. DISCUSSION: These results indicate that our torsadogenic risk assessment is reliable and has a potential to replace the hERG assay for torsadogenic risk prediction, however, this system needs to be improved for the accurate of prediction of clinical TdP risk. Here, we propose a novel drug induced torsadogenic risk categorising system using hiPSC-CMs and the MEA system."
    - id: https://openalex.org/W1602075345
      doi: https://doi.org/10.1111/j.1476-5381.2009.00334.x
      title: "Pharmacological and electrophysiological characterization of nine, single nucleotide polymorphisms of the hERG‐encoded potassium channel"
      publication_year: 2009
      relevance_score: 69.87079
      abstract: "BACKGROUND AND PURPOSE: Potencies of compounds blocking K(V)11.1 [human ether-ago-go-related gene (hERG)] are commonly assessed using cell lines expressing the Caucasian wild-type (WT) variant. Here we tested whether such potencies would be different for hERG single nucleotide polymorphisms (SNPs). EXPERIMENTAL APPROACH: SNPs (R176W, R181Q, Del187-189, P347S, K897T, A915V, P917L, R1047L, A1116V) and a binding-site mutant (Y652A) were expressed in Tet-On CHO-K1 cells. Potencies [mean IC(50); lower/upper 95% confidence limit (CL)] of 48 hERG blockers was estimated by automated electrophysiology [IonWorks HT (IW)]. In phase one, rapid potency comparison of each WT-SNP combination was made for each compound. In phase two, any compound-SNP combinations from phase one where the WT upper/lower CL did not overlap with those of the SNPs were re-examined. Electrophysiological WT and SNP parameters were determined using conventional electrophysiology. KEY RESULTS: IW detected the expected sixfold potency decrease for propafenone in Y652A. In phase one, the WT lower/upper CL did not overlap with those of the SNPs for 77 compound-SNP combinations. In phase two, 62/77 cases no longer yielded IC(50) values with non-overlapping CLs. For seven of the remaining 15 cases, there were non-overlapping CLs but in the opposite direction. For the eight compound-SNP combinations with non-overlapping CLs in the same direction as for phase 1, potencies were never more than twofold apart. The only statistically significant electrophysiological difference was the voltage dependence of activation of R1047L. CONCLUSION AND IMPLICATIONS: Potencies of hERG channel blockers defined using the Caucasian WT sequence, in this in vitro assay, were representative of potencies for common SNPs."
    - id: https://openalex.org/W3131769770
      doi: https://doi.org/10.3389/fphar.2021.618411
      title: Advances in Oral Drug Delivery
      publication_year: 2021
      relevance_score: 55.03142
      abstract: "The oral route is the most common route for drug administration. It is the most preferred route, due to its advantages, such as non-invasiveness, patient compliance and convenience of drug administration. Various factors govern oral drug absorption including drug solubility, mucosal permeability, and stability in the gastrointestinal tract environment. Attempts to overcome these factors have focused on understanding the physicochemical, biochemical, metabolic and biological barriers which limit the overall drug bioavailability. Different pharmaceutical technologies and drug delivery systems including nanocarriers, micelles, cyclodextrins and lipid-based carriers have been explored to enhance oral drug absorption. To this end, this review will discuss the physiological, and pharmaceutical barriers influencing drug bioavailability for the oral route of administration, as well as the conventional and novel drug delivery strategies. The challenges and development aspects of pediatric formulations will also be addressed."
    - id: https://openalex.org/W1551796354
      doi: https://doi.org/10.1111/j.1476-5381.2011.01547.x
      title: "Induction of prolonged, continuous slow‐wave sleep by blocking cerebral H<sub>1</sub>histamine receptors in rats"
      publication_year: 2011
      relevance_score: 48.71487
      abstract: "BACKGROUND AND PURPOSE: Classic H(1) histamine receptor (H(1)R) antagonists are non-selective for H(1)R and known to produce drowsiness. Modern antihistamines are more selective for H(1)R, and are 'non-drowsy' presumably due to reduced permeability through the blood-brain barrier. To characterize both histaminergic sleep regulation and the central actions of antihistamines, in the present study we analysed the effect of classic and modern antihistamines on rats' sleep using continuous i.c.v. infusions. EXPERIMENTAL APPROACH: Effects of classic (d-chlorpheniramine; d-CPA) and second-generation (cetirizine) antihistamines on sleep were compared after i.p. injections or continuous i.c.v. infusions into rats. Fluorescent cetirizine/DBD-pz was synthesized to trace the approximate distribution of cerebral cetirizine. Furthermore, the effects of H(1) R antagonists on cultured preoptic neurons were examined using calcium imaging. KEY RESULTS: d-CPA 4 mg·kg(-1) i.p. increased non-rapid eye movement (REM) sleep whereas 10-40 mg·kg(-1) d-CPA decreased non-REM sleep at dark onset time. Nocturnal i.c.v. infusions of d-CPA (10 µmol·100 µL(-1)·10 h(-1)) increased drowsiness but not non-REM sleep, whereas the same i.c.v. infusions of cetirizine significantly increased non-REM sleep, abolished REM sleep, and decreased wakefulness for more than 10 h. The medial preoptic area contained the greatest fluorescent labelling after i.c.v. cetirizine/DBD-pz infusions. Histamine-induced Ca(2+) increases in medial preoptic neurons were blocked by d-CPA or cetirizine, whereas d-CPA, but not cetirizine, increased Ca(2+) irrespective of antihistaminergic activity at ≥ 100 µM. CONCLUSION AND IMPLICATIONS: The excitatory action of d-CPA may explain the seemingly inconsistent actions of d-CPA on sleep. Cerebral H(1)R inhibition by cetirizine induces synchronization of cerebral activity and prolonged, continuous slow-wave sleep."
    - id: https://openalex.org/W1968956582
      doi: https://doi.org/10.1016/j.pbiomolbio.2003.09.001
      title: "HERG binding specificity and binding site structure: evidence from a fragment-based evolutionary computing SAR study"
      publication_year: 2004
      relevance_score: 48.09378
      abstract: "We describe the application of genetic programming, an evolutionary computing method, to predicting whether small molecules will block the HERG cardiac potassium channel. Models based on a molecular fragment-based descriptor set achieve an accuracy of 85-90% in predicting whether the IC(50) of a 'blind' set of compounds is <1 microM. Analysis of the models provides a 'meta-SAR', which predicts a pharmacophore of two hydrophobic features, one preferably aromatic and one preferably nitrogen-containing, with a protonatable nitrogen asymmetrically situated between them. Our experience of the approach suggests that it is robust, and requires limited scientist input to generate valuable predictive results and structural understanding of the target."
    - id: https://openalex.org/W2014716920
      doi: https://doi.org/10.1186/2050-6511-15-47
      title: A systematic review of the pathophysiology of 5-fluorouracil-induced cardiotoxicity
      publication_year: 2014
      relevance_score: 44.01085
      abstract: "BACKGROUND: Cardiotoxicity is a serious side effect to treatment with 5-fluorouracil (5-FU), but the underlying mechanisms are not fully understood. The objective of this systematic review was to evaluate the pathophysiology of 5-FU- induced cardiotoxicity. METHODS: We systematically searched PubMed for articles in English using the search terms: 5-FU OR 5-fluorouracil OR capecitabine AND cardiotoxicity. Papers evaluating the pathophysiology of this cardiotoxicity were included. RESULTS: We identified 27 articles of 26 studies concerning the pathophysiology of 5-FU-induced cardiotoxicity. The studies demonstrated 5-FU-induced: hemorrhagic infarction, interstitial fibrosis and inflammatory reaction in the myocardium; damage of the arterial endothelium followed by platelet aggregation; increased myocardial energy metabolism and depletion of high energy phosphate compounds; increased superoxide anion levels and a reduced antioxidant capacity; vasoconstriction of arteries; changes in red blood cell (RBC) structure, function and metabolism; alterations in plasma levels of substances involved in coagulation and fibrinolysis and increased endothelin-1 levels and N-terminal-pro brain natriuretic peptide levels. Based on these findings the proposed mechanisms are: endothelial injury followed by thrombosis, increased metabolism leading to energy depletion and ischemia, oxidative stress causing cellular damage, coronary artery spasm leading to myocardial ischemia and diminished ability of RBCs to transfer oxygen resulting in myocardial ischemia. CONCLUSIONS: There is no evidence for a single mechanism responsible for 5-FU-induced cardiotoxicity, and the underlying mechanisms might be multifactorial. Further research is needed to elucidate the pathogenesis of this side effect."
    - id: https://openalex.org/W4366548482
      doi: https://doi.org/10.3389/fphar.2023.1175702
      title: Role of voltage-gated proton channel (Hv1) in cancer biology
      publication_year: 2023
      relevance_score: 43.932972
      abstract: "The acid-base characteristics of tumor cells and the other elements that compose the tumor microenvironment have been topics of scientific interest in oncological research. There is much evidence confirming that pH conditions are maintained by changes in the patterns of expression of certain proton transporters. In the past decade, the voltage-gated proton channel (Hv1) has been added to this list and is increasingly being recognized as a target with onco-therapeutic potential. The Hv1 channel is key to proton extrusion for maintaining a balanced cytosolic pH. This protein-channel is expressed in a myriad of tissues and cell lineages whose functions vary from producing bioluminescence in dinoflagellates to alkalizing spermatozoa cytoplasm for reproduction, and regulating the respiratory burst for immune system response. It is no wonder that in acidic environments such as the tumor microenvironment, an exacerbated expression and function of this channel has been reported. Indeed, multiple studies have revealed a strong relationship between pH balance, cancer development, and the overexpression of the Hv1 channel, being proposed as a marker for malignancy in cancer. In this review, we present data that supports the idea that the Hv1 channel plays a significant role in cancer by maintaining pH conditions that favor the development of malignancy features in solid tumor models. With the antecedents presented in this bibliographic report, we want to strengthen the idea that the Hv1 proton channel is an excellent therapeutic strategy to counter the development of solid tumors."
    - id: https://openalex.org/W4403054069
      doi: https://doi.org/10.7759/cureus.70719
      title: "Diphenhydramine Overdose: A Case Report and Topic Review of Prehospital Diagnosis and Treatment"
      publication_year: 2024
      relevance_score: 41.315445
      abstract: "Diphenhydramine (DPH), a readily available first-generation H1 receptor antihistamine, can have severe consequences when taken in excessive amounts and can lead to grave outcomes such as seizures, dysrhythmias, coma, and death. Recognizing the early signs and symptoms of DPH toxicity is crucial. Fortunately, fatal adult cases of DPH overdose are rare. This report describes a near-fatal overdose of a young adult female who experienced recurrent seizures, respiratory failure, and cardiac arrest with the return of spontaneous circulation (ROSC) in the prehospital setting and complete functional recovery. This case underscores the urgency of addressing DPH toxicity and the utility of reversal agents, such as sodium bicarbonate, in sodium channel blockade."
    - id: https://openalex.org/W2105007258
      doi: https://doi.org/10.1186/2008-2231-20-81
      title: Advances in toxicology and medical treatment of chemical warfare nerve agents
      publication_year: 2012
      relevance_score: 38.83393
      abstract: "Organophosphorous (OP) Nerve agents (NAs) are known as the deadliest chemical warfare agents. They are divided into two classes of G and V agents. Most of them are liquid at room temperature. NAs chemical structures and mechanisms of actions are similar to OP pesticides, but their toxicities are higher than these compounds. The main mechanism of action is irreversible inhibition of Acetyl Choline Esterase (AChE) resulting in accumulation of toxic levels of acetylcholine (ACh) at the synaptic junctions and thus induces muscarinic and nicotinic receptors stimulation. However, other mechanisms have recently been described. Central nervous system (CNS) depression particularly on respiratory and vasomotor centers may induce respiratory failure and cardiac arrest. Intermediate syndrome after NAs exposure is less common than OP pesticides poisoning. There are four approaches to detect exposure to NAs in biological samples: (I) AChE activity measurement, (II) Determination of hydrolysis products in plasma and urine, (III) Fluoride reactivation of phosphylated binding sites and (IV) Mass spectrometric determination of cholinesterase adducts. The clinical manifestations are similar to OP pesticides poisoning, but with more severity and fatalities. The management should be started as soon as possible. The victims should immediately be removed from the field and treatment is commenced with auto-injector antidotes (atropine and oximes) such as MARK I kit. A 0.5% hypochlorite solution as well as novel products like M291 Resin kit, G117H and Phosphotriesterase isolated from soil bacterias, are now available for decontamination of NAs. Atropine and oximes are the well known antidotes that should be infused as clinically indicated. However, some new adjuvant and additional treatment such as magnesium sulfate, sodium bicarbonate, gacyclidine, benactyzine, tezampanel, hemoperfusion, antioxidants and bioscavengers have recently been used for OP NAs poisoning."
    - id: https://openalex.org/W2559446188
      doi: https://doi.org/10.1039/c6md00578k
      title: "Discovery and hit-to-lead evaluation of piperazine amides as selective, state-dependent Na <sub>V</sub> 1.7 inhibitors"
      publication_year: 2016
      relevance_score: 34.71681
      abstract: Optimization of a screening hit led to the identification of Na <sub>V</sub> 1.7 inhibitors with a desirable balance of properties.
    - id: https://openalex.org/W3113029451
      doi: https://doi.org/10.3389/fphys.2020.554195
      title: The Mysteries of Capsaicin-Sensitive Afferents
      publication_year: 2020
      relevance_score: 33.620537
      abstract: "A fundamental subdivision of nociceptive sensory neurons is named after their unique sensitivity to capsaicin, the pungent ingredient in hot chili peppers: these are the capsaicin-sensitive afferents. The initial excitation by capsaicin of these neurons manifested as burning pain sensation is followed by a lasting refractory state, traditionally referred to as “capsaicin desensitization,” during which the previously excited neurons are unresponsive not only to capsaicin but a variety of unrelated stimuli including noxious heat. The long sought-after capsaicin receptor, now known as TRPV1 (transient receptor potential cation channel, subfamily V member 1), was cloned more than two decades ago. The substantial reduction of the inflammatory phenotype of Trpv1 knockout mice has spurred extensive efforts in the pharmaceutical industry to develop small molecule TRPV1 antagonists. However, adverse effects, most importantly hyperthermia and burn injuries, have so far prevented any compounds from progressing beyond Phase 2. There is increasing evidence that these limitations can be at least partially overcome by approaches outside of the mainstream pharmaceutical development, providing novel therapeutic options through TRPV1. Although ablation of the whole TRPV1-expressing nerve population by high dose capsaicin, or more selectively by intersectional genetics, has allowed researchers to investigate the functions of capsaicin-sensitive afferents in health and disease, several “mysteries” remain unsolved to date, including the molecular underpinnings of “capsaicin desensitization,” and the exact role these nerves play in thermoregulation and heat sensation. This review tries to shed some light on these capsaicin mechanisms."
    - id: https://openalex.org/W2001336902
      doi: https://doi.org/10.1016/s0005-2736(03)00080-4
      title: Sensitivity of bile acid transport by organic anion-transporting polypeptides to intracellular pH
      publication_year: 2003
      relevance_score: 27.888973
    - id: https://openalex.org/W1552265434
      doi: https://doi.org/10.1111/j.1476-5381.2012.02093.x
      title: "Histamine H<sub>3</sub>receptor antagonists in relation to epilepsy and neurodegeneration: a systemic consideration of recent progress and perspectives"
      publication_year: 2012
      relevance_score: 27.426365
      abstract: "The central histaminergic actions are mediated by H(1) , H(2) , H(3) and H(4) receptors. The histamine H(3) receptor regulates the release of histamine and a number of other neurotransmitters and thereby plays a role in cognitive and homeostatic processes. Elevated histamine levels suppress seizure activities and appear to confer neuroprotection. The H(3) receptors have a number of enigmatic features like constitutive activity, interspecies variation, distinct ligand binding affinities and differential distribution of prototypic splice variants in the CNS. Furthermore, this Gi/Go-protein-coupled receptor modulates several intracellular signalling pathways whose involvement in epilepsy and neurotoxicity are yet to be ascertained and hence represent an attractive target in the search for new anti-epileptogenic drugs. So far, H(3) receptor antagonists/inverse agonists have garnered a great deal of interest in view of their promising therapeutic properties in various CNS disorders including epilepsy and related neurotoxicity. However, a number of experiments have yielded opposing effects. This article reviews recent works that have provided evidence for diverse mechanisms of antiepileptic and neuroprotective effects that were observed in various experimental models both in vitro and in vivo. The likely reasons for the apparent disparities arising from the literature are also discussed with the aim of establishing a more reliable basis for the future use of H(3) receptor antagonists, thus improving their utility in epilepsy and associated neurotoxicity."
    - id: https://openalex.org/W2947337803
      doi: https://doi.org/10.3390/ijms20133210
      title: Recent Topics on The Mechanisms of Immunosuppressive Therapy-Related Neurotoxicities
      publication_year: 2019
      relevance_score: 26.204494
      abstract: "Although transplantation procedures have been developed for patients with end-stage hepatic insufficiency or other diseases, allograft rejection still threatens patient health and lifespan. Over the last few decades, the emergence of immunosuppressive agents such as calcineurin inhibitors (CNIs) and mammalian target of rapamycin (mTOR) inhibitors have strikingly increased graft survival. Unfortunately, immunosuppressive agent-related neurotoxicity commonly occurs in clinical practice, with the majority of neurotoxicity cases caused by CNIs. The possible mechanisms through which CNIs cause neurotoxicity include increasing the permeability or injury of the blood-brain barrier, alterations of mitochondrial function, and alterations in the electrophysiological state. Other immunosuppressants can also induce neuropsychiatric complications. For example, mTOR inhibitors induce seizures, mycophenolate mofetil induces depression and headaches, methotrexate affects the central nervous system, the mouse monoclonal immunoglobulin G2 antibody (used against the cluster of differentiation 3) also induces headaches, and patients using corticosteroids usually experience cognitive alteration. Therapeutic drug monitoring, individual therapy based on pharmacogenetics, and early recognition of symptoms help reduce neurotoxic events considerably. Once neurotoxicity occurs, a reduction in the drug dosage, switching to other immunosuppressants, combination therapy with drugs used to treat the neuropsychiatric manifestation, or blood purification therapy have proven to be effective against neurotoxicity. In this review, we summarize recent topics on the mechanisms of immunosuppressive drug-related neurotoxicity. In addition, information about the neuroprotective effects of several immunosuppressants is also discussed."
    - id: https://openalex.org/W89030335
      doi: https://doi.org/10.36076/ppj.2011/14/e343
      title: Pharmacology of Opioids in the Treatment ofChronic Pain Syndromes
      publication_year: 2011
      relevance_score: 26.086607
      abstract: "The perpetual pursuit of pain elimination has been constant throughout human history and pervades human cultures. In some ways it is as old as medicine itself. Cultures throughout history have practiced the art of pain management through remedies such as oral ingestion of herbs or techniques believed to have special properties. In fact, even Hippocrates wrote about the practice of trepanation, the cutting of holes in the body to release pain. Current therapies for management of pain include the pervasive utilization of opioids, which have an extensive history, spanning centuries. There is general agreement about the appropriateness of opioids for the treatment of acute and cancer pain, but the long-term use of these drugs for treatment of chronic non-malignant pain remains controversial. The pros and cons regarding these issues are beyond the scope of this review. Instead, the purpose of this review will be directed towards the pharmacology of commonly prescribed opioids in the treatment of various chronic pain syndromes. Opium, derived from the Greek word for \"juice,\" is extracted from the latex sap of the opium poppy (Papaverum somniferum). The juice of the poppy is the source of some 20 different alkaloids of opium. These alkaloids of opioids can be divided into 2 chemical classes: phenanthrenes (morphine, codeine, and thebaine) and benzylisoquinolines (agents that do not interact with opioid receptors)."
    - id: https://openalex.org/W3147714328
      doi: https://doi.org/10.3390/pharmaceutics13040450
      title: Topical Treatments and Their Molecular/Cellular Mechanisms in Patients with Peripheral Neuropathic Pain—Narrative Review
      publication_year: 2021
      relevance_score: 25.835566
      abstract: "Neuropathic pain in humans results from an injury or disease of the somatosensory nervous system at the peripheral or central level. Despite the considerable progress in pain management methods made to date, peripheral neuropathic pain significantly impacts patients' quality of life, as pharmacological and non-pharmacological methods often fail or induce side effects. Topical treatments are gaining popularity in the management of peripheral neuropathic pain, due to excellent safety profiles and preferences. Moreover, topical treatments applied locally may target the underlying mechanisms of peripheral sensitization and pain. Recent studies showed that peripheral sensitization results from interactions between neuronal and non-neuronal cells, with numerous signaling molecules and molecular/cellular targets involved. This narrative review discusses the molecular/cellular mechanisms of drugs available in topical formulations utilized in clinical practice and their effectiveness in clinical studies in patients with peripheral neuropathic pain. We searched PubMed for papers published from 1 January 1995 to 30 November 2020. The key search phrases for identifying potentially relevant articles were \"topical AND pain\", \"topical AND neuropathic\", \"topical AND treatment\", \"topical AND mechanism\", \"peripheral neuropathic\", and \"mechanism\". The result of our search was 23 randomized controlled trials (RCT), 9 open-label studies, 16 retrospective studies, 20 case (series) reports, 8 systematic reviews, 66 narrative reviews, and 140 experimental studies. The data from preclinical studies revealed that active compounds of topical treatments exert multiple mechanisms of action, directly or indirectly modulating ion channels, receptors, proteins, and enzymes expressed by neuronal and non-neuronal cells, and thus contributing to antinociception. However, which mechanisms and the extent to which the mechanisms contribute to pain relief observed in humans remain unclear. The evidence from RCTs and reviews supports 5% lidocaine patches, 8% capsaicin patches, and botulinum toxin A injections as effective treatments in patients with peripheral neuropathic pain. In turn, single RCTs support evidence of doxepin, funapide, diclofenac, baclofen, clonidine, loperamide, and cannabidiol in neuropathic pain states. Topical administration of phenytoin, ambroxol, and prazosin is supported by observational clinical studies. For topical amitriptyline, menthol, and gabapentin, evidence comes from case reports and case series. For topical ketamine and baclofen, data supporting their effectiveness are provided by both single RCTs and case series. The discussed data from clinical studies and observations support the usefulness of topical treatments in neuropathic pain management. This review may help clinicians in making decisions regarding whether and which topical treatment may be a beneficial option, particularly in frail patients not tolerating systemic pharmacotherapy."
    - id: https://openalex.org/W2783786322
      doi: https://doi.org/10.1016/j.toxicon.2018.01.003
      title: "BotAF, a new Buthus occitanus tunetanus scorpion toxin, produces potent analgesia in rodents"
      publication_year: 2018
      relevance_score: 25.048279
```
/answer 877f9d27-e1e2-458a-af0e-452060caa6dd allow
Control Request:
```yaml
id: 29f343fc-1dbf-470d-95b3-7578f5701a25
toolName: openalex-search
arguments:
  query: diphenhydramine H1 receptor affinity Ki nanomolar
  reason: Get H1 receptor potency for selectivity comparison
  fields: abstract
```
/answer 29f343fc-1dbf-470d-95b3-7578f5701a25 allow
Control Request:
```yaml
id: d21902c3-ceba-4394-8409-2892fc6d45ef
result:
  structuredContent:
    count: 11
    returned: 11
    page: 1
    per_page: 25
    results:
    - id: https://openalex.org/W3205136031
      doi: https://doi.org/10.2147/dddt.s329547
      title: The Expanding Role of Pyridine and Dihydropyridine Scaffolds in Drug Design
      publication_year: 2021
      relevance_score: 56.04832
      abstract: "Pyridine-based ring systems are one of the most extensively used heterocycles in the field of drug design, primarily due to their profound effect on pharmacological activity, which has led to the discovery of numerous broad-spectrum therapeutic agents. In the US FDA database, there are 95 approved pharmaceuticals that stem from pyridine or dihydropyridine, including isoniazid and ethionamide (tuberculosis), delavirdine (HIV/AIDS), abiraterone acetate (prostate cancer), tacrine (Alzheimer's), ciclopirox (ringworm and athlete's foot), crizotinib (cancer), nifedipine (Raynaud's syndrome and premature birth), piroxicam (NSAID for arthritis), nilvadipine (hypertension), roflumilast (COPD), pyridostigmine (myasthenia gravis), and many more. Their remarkable therapeutic applications have encouraged researchers to prepare a larger number of biologically active compounds decorated with pyridine or dihydropyridine, expandeing the scope of finding a cure for other ailments. It is thus anticipated that myriad new pharmaceuticals containing the two heterocycles will be available in the forthcoming decade. This review examines the prospects of highly potent bioactive molecules to emphasize the advantages of using pyridine and dihydropyridine in drug design. We cover the most recent developments from 2010 to date, highlighting the ever-expanding role of both scaffolds in the field of medicinal chemistry and drug development."
    - id: https://openalex.org/W3197358523
      doi: https://doi.org/10.3390/ijms22189739
      title: Label-Free Investigations on the G Protein Dependent Signaling Pathways of Histamine Receptors
      publication_year: 2021
      relevance_score: 55.65535
      abstract: "G protein activation represents an early key event in the complex GPCR signal transduction process and is usually studied by label-dependent methods targeting specific molecular events. However, the constrained environment of such “invasive” techniques could interfere with biological processes. Although histamine receptors (HRs) represent (evolving) drug targets, their signal transduction is not fully understood. To address this issue, we established a non-invasive dynamic mass redistribution (DMR) assay for the human H1–4Rs expressed in HEK cells, showing excellent signal-to-background ratios above 100 for histamine (HIS) and higher than 24 for inverse agonists with pEC50 values consistent with literature. Taking advantage of the integrative nature of the DMR assay, the involvement of endogenous Gαq/11, Gαs, Gα12/13 and Gβγ proteins was explored, pursuing a two-pronged approach, namely that of classical pharmacology (G protein modulators) and that of molecular biology (Gα knock-out HEK cells). We showed that signal transduction of hH1–4Rs occurred mainly, but not exclusively, via their canonical Gα proteins. For example, in addition to Gαi/o, the Gαq/11 protein was proven to contribute to the DMR response of hH3,4Rs. Moreover, the Gα12/13 was identified to be involved in the hH2R mediated signaling pathway. These results are considered as a basis for future investigations on the (patho)physiological role and the pharmacological potential of H1–4Rs."
    - id: https://openalex.org/W2008105473
      doi: https://doi.org/10.1155/s0962935193000444
      title: Phosphoinositide hydrolysis mediated by H1 receptors in autoimmune myocarditis mice
      publication_year: 1993
      relevance_score: 48.03052
      abstract: "Stimulation of phosphoinositide hydrolysis in myocardium from autoimmune myocarditis mice by ThEA and histamine was assayed. Myocardium from autoimmune heart, but not the normal forms, specifically increased phosphoinositide turnover in the presence of histaminergic agonists. This increment was blocked by a specific H1 antagonist mepyramine and to the same extent by the phospholipase C inhibitor NCDC. By using a binding assay H1 histaminergic receptors were detected in autoimmune heart membrane preparations, but this was not observed in normal heart. These data suggest that autoimmune myocardium expressed a functional H1 receptor that could involve a distinctive mechanism operating in the disease."
    - id: https://openalex.org/W4415240287
      doi: https://doi.org/10.2218/gtopdb/f33/2025.3
      title: Histamine receptors in GtoPdb v.2025.3
      publication_year: 2025
      relevance_score: 29.882227
      abstract: "Histamine receptors (nomenclature as agreed by the NC-IUPHAR Subcommittee on Histamine Receptors [82, 176]) are activated by the endogenous ligand histamine. Marked species differences exist between histamine receptor orthologues [82]. The human and rat H3 receptor genes are subject to significant splice variance [12]. The potency order of histamine at histamine receptor subtypes is H3 = H4 &gt; H2 &gt; H1 [176]. Some agonists at the human H3 receptor display significant ligand bias [185]. Antagonists of all 4 histamine receptors have clinical uses: H1 antagonists for allergies (e.g. cetirizine), H2 antagonists for acid-reflux diseases (e.g. ranitidine), H3 antagonists for narcolepsy (e.g. pitolisant/WAKIX; Registered) and H4 antagonists for atopic dermatitis (e.g. adriforant; Phase IIa) [176] and vestibular neuritis (AUV) (SENS-111 (Seliforant, previously UR-63325), entered and completed vestibular neuritis (AUV) Phase IIa efficacy and safety trials, respectively) [219, 8]. Histamine receptor photopharmacology has provided both agonist and antagonist tools to achieve optical control over H3 receptor function. The best-characterized agonist is VUF15000, an azobenzene-containing compound in which the trans-isomer binds the H3 receptor with nanomolar affinity (Ki = 4 nM) and behaves as a full agonist. Its cis-isomer is approximately 10-fold less active, thereby creating a reversible light-controlled switch for receptor activation that has been validated in binding, NanoBRET biosensor, and electrophysiology assays [78]. Also several photoswitchable antagonists have been established as tools for histamine H3 receptor photopharmacology. The first-generation azobenzene-based antagonists included VUF14738 and VUF14862, which are part of a bidirectional toolbox [77]. VUF14738 (trans: Ki = 631 nM) shows a light-induced 10-fold increase in affinity, while VUF14862 (trans: Ki = 1.6 nM) displays the opposite, with more than a tenfold change upon illumination. Both compounds are highly fatigue-resistant, underwent rapid trans-cis isomerization, and had long thermal half-lives, allowing reversible optical control in binding and electrophysiological assays. Building on these scaffolds, recently 2nd generation ligands were developed to overcome limitations of azobenzenes [18]. The arylazopyrazole-based antagonist VUF26063 displayed subnanomolar affinity at the H3 receptor in its trans isomer (Ki = 0.5 nM) and a 50-fold lower affinity in the cis state. This compound showed robust switching with high photostationary state efficiency and improved aqueous solubility compared to earlier analogues. Importantly, radiolabeling yielded [3H]VUF26063, the first radiolabeled photoswitchable GPCR ligand, enabling the direct study of ligand binding kinetics and photoisomerization inside the receptor pocket in real time. These antagonists, together with the agonist VUF15000, provide a well-characterized toolkit of photosensitive ligands that can be used to dissect H3 receptor pharmacology with spatiotemporal precision."
    - id: https://openalex.org/W2957984814
      doi: https://doi.org/10.2147/cpaa.s206615
      title: '&lt;p&gt;Novel approaches to treating advanced systemic mastocytosis&lt;/p&gt;'
      publication_year: 2019
      relevance_score: 26.754274
      abstract: "Abstract: Mastocytosis is a myeloproliferative neoplasm characterized by expansion of abnormal mast cells (MCs) in various tissues, including skin, bone marrow, gastrointestinal tract, liver, spleen, or lymph nodes. Subtypes include indolent systemic mastocytosis, smoldering systemic mastocytosis and advanced systemic mastocytosis (AdvSM), a term collectively used for the three most aggressive forms of the disease: aggressive systemic mastocytosis, mast cell leukemia, and systemic mastocytosis with an associated clonal hematological non-mast cell disease (SM-AHNMD). MC activation and proliferation is physiologically controlled in part through stem cell factor (SCF) binding to its cognate receptor, KIT. Gain-of-function KIT mutations that lead to ligand-independent kinase activation are found in most SM subtypes, and the overwhelming majority of AdvSM patients harbor the KIT D816V, mutation. Several approved tyrosine kinase inhibitors (TKIs), such as imatinib and nilotinib, have activity against wild-type KIT but lack activity against KIT D816V, . Midostaurin, a broad spectrum TKI with activity against KIT, D816V has a 60% clinical response rate, and is currently the only drug specifically approved for AdvSM. While this agent improves the prognosis of AdvSM patients and provides proof of principle for targeting KIT D816V, as a driver mutation, most responses are partial and/or not sustained, indicating that more potent and/or specific inhibitors are required. Avapritinib, a KIT and PDGFRα inhibitor, was specifically designed to inhibit KIT D816V, . Early results from a Phase 1 trial suggest that avapritinib has potent antineoplastic activity in AdvSM, extending to patients who failed midostaurin. Patients exhibited a rapid reduction in both symptoms as well as reductions of bone marrow MCs, serum tryptase, and KIT D816V, mutant allele burden. Adverse effects include expected toxicities such as myelosuppression and periorbital edema, but also cognitive impairment in some patients. Although considerable excitement about avapritinib exists, more data are needed to assess long-term responses and adverse effects of this novel TKI. Keywords: avapritinib, BLU285, systemic mastocytosis, KIT, tyrosine kinase inhibitor"
    - id: https://openalex.org/W2476139746
      doi: https://doi.org/10.5772/1864
      title: "Nutrition, Well-Being and Health"
      publication_year: 2012
      relevance_score: 26.627989
      abstract: "In our modern society, expectations are high, also with respect to our daily diet. In addition to being merely \"nutritious\", i.e. supplying a variety of essential nutrients, including macro-nutrients such as proteins or micro-nutrients such as minerals and vitamins, it is almost expected that a good diet offers further advantages - especially well-being and health and the prevention of chronic diseases, which are, as we generally tend to grow older and older, becoming a burden to enjoying private life and to the entire society. These additional qualities are often sought in diets rich also in non-nutritive components, such as phytochemicals. In contrast to drugs, which are taken especially to cure or ameliorate diseases, it is expected that a healthy diet acts in particular on the side of prevention, allowing us to become old without feeling old. In the present book, rather then trying to give an exhaustive overview on nutritional aspects and their link to well-being and health, selected topics have been chosen, intended to address presently discussed key issues of nutrition for health, presenting a reasonable selection of the manifold topics around diet, well-being, and health: from the antioxidants polyphenols and carotenoids, aroma-active terpenoids, to calcium for bone health, back to traditional Chinese Medicine."
    - id: https://openalex.org/W2296589160
      doi: https://doi.org/10.1093/database/bav087
      title: "Connecting proteins with drug-like compounds: Open source drug discovery workflows with BindingDB and KNIME"
      publication_year: 2015
      relevance_score: 21.637733
      abstract: "Today's large, public databases of protein-small molecule interaction data are creating important new opportunities for data mining and integration. At the same time, new graphical user interface-based workflow tools offer facile alternatives to custom scripting for informatics and data analysis. Here, we illustrate how the large protein-ligand database BindingDB may be incorporated into KNIME workflows as a step toward the integration of pharmacological data with broader biomolecular analyses. Thus, we describe a collection of KNIME workflows that access BindingDB data via RESTful webservices and, for more intensive queries, via a local distillation of the full BindingDB dataset. We focus in particular on the KNIME implementation of knowledge-based tools to generate informed hypotheses regarding protein targets of bioactive compounds, based on notions of chemical similarity. A number of variants of this basic approach are tested for seven existing drugs with relatively ill-defined therapeutic targets, leading to replication of some previously confirmed results and discovery of new, high-quality hits. Implications for future development are discussed. Database URL: www.bindingdb.org."
    - id: https://openalex.org/W2951361919
      doi: https://doi.org/10.3390/ph12020099
      title: Psychotropic Drugs for the Management of Chronic Pain and Itch
      publication_year: 2019
      relevance_score: 21.06027
      abstract: "Clinical observations have shown that patients with chronic neuropathic pain or itch exhibit symptoms of increased anxiety, depression and cognitive impairment. Such patients need corrective therapy with antidepressants, antipsychotics or anticonvulsants. It is known that some psychotropic drugs are also effective for the treatment of neuropathic pain and pruritus syndromes due to interaction with the secondary molecular targets. Our own clinical studies have identified antipruritic and/or analgesic efficacy of the following compounds: tianeptine (atypical tricyclic antidepressant), citalopram (selective serotonin reuptake inhibitor), mianserin (tetracyclic antidepressant), carbamazepine (anticonvulsant), trazodone (serotonin antagonist and reuptake inhibitor), and chlorprothixene (antipsychotic). Venlafaxine (serotonin-norepinephrine reuptake inhibitor) is known to have an analgesic effect too. The mechanism of such effect of these drugs is not fully understood. Herein we review and correlate the literature data on analgesic/antipruritic activity with pharmacological profile of these compounds."
    - id: https://openalex.org/W215292424
      doi: https://doi.org/10.5283/epub.22958
      title: "Hetarylalkyl(aryl)cyanoguanidines as histamine H4 receptor ligands: Synthesis, chiral separation, pharmacological characterization, structure-activity and -selectivity relationships"
      publication_year: 2011
      relevance_score: 20.153254
      abstract: "The recently discovered histamine H4 receptor (H4R) is reported to be involved in immunological processes and inflammatory diseases. However, the (patho)physiological role of the H4R is far from being fully understood. Controversial data on H4R agonists as well as reports on β-arrestin-mediated signaling and partial agonistic effects of the standard H4R antagonist JNJ-7777120 at certain H4R species orthologs complicate the interpretation of in vivo studies. Therefore, additional potent and receptor subtype selective H4R ligands, antagonists as well as agonists, are required as pharmacological tools. Discrimination between the closely related H3 and H4 receptors turned out to be a critical issue in the development of selective H4R agonists. Starting from UR-PI376, a lead from our laboratory, the major objective of this thesis was the design, synthesis and pharmacological characterization of bioisosteric and conformationally constrained cyanoguanidine-type H4R agonist to evaluate structure-activity and –selectivity relationships. The prepared compounds were investigated for agonism and antagonism at the human (h) H1R, H2R, H3R and H4R in functional [35S]GTPyS binding assays or steady-state GTPase assays, respectively, using Sf9 cell membranes expressing the HR subtype of interest. Selected compounds were evaluated in radioligand binding studies at the human HR subtypes (Sf9 cell membranes) and mouse H4R (mH4R expressed in HEK293 cells). In addition, representative compounds were investigated in a luciferase gene reporter assay at mH4R and hH4R using genetically engineered HEK293 cells. In a first approach, based on a previously suggested model of UR-PI376 binding to the hH4R, the tetramethylene chain in UR-PI376 was replaced by conformationally restricted spacers connecting imidazole ring with the cyanoguanidine moiety. Phenylene linkers proved to be inappropriate: None of the prepared compounds or amine precursor showed relevant activity at the H3R and H4R. To retain some flexibility, in a second series the phenylene was replaced by a cyclohexylene linker. Compounds with a cis-configured 1,4-cyclohexylene spacer, turned out to be moderately potent and selective hH4R agonists. The same holds for the building block, cis-4-(1H-imidazol-4-yl)cyclohexylamine. In case of the trans-configured analogues, there was a tendency toward preference for the hH3R. To optimize the spacer regarding ring size, balance between rigidification and flexibility, regioisomers and stereochemical properties a cyclopentane-1,3-diyl moiety and an additional exocyclic methylene group were introduced. The most potent H4R agonists identified among a set of 14 racemic compounds were separated by chiral HPLC to yield eight enantiomerically pure compounds. trans-(+)-(1S,3S)-UR-RG98 was the most potent and selective H4R agonist in this series with an EC50 of 11 nM, a more than 100-fold selectivity for the H4R over the H3R and negligible activities at the other HR subtypes. By contrast, the optical antipode, trans-(-)-(1R,3R)-UR-RG98, proved to be an H4R antagonist in the [35S]GTPyS assay. The absolute configuration of the stereoisomers was determined subsequent to an enzyme-assisted stereoselective synthesis. In search for bioisosteric replacements of the imidazole ring in cyanoguanidine-type H4R agonists, ten different heterocycles were combined with linkers of various chain lengths and substitution patterns. A total of 42 compounds, cyanoguanidines and amine precursor, were synthesized and evaluated at the HR subtypes. The exchange of the 4-imidazolyl ring considerably affected the activities at all HRs. Only the 2- and 5-methyl substituted imidazoles showed H4R agonistic potency. None of the investigated compounds was superior to UR-PI376. In an attempt to synthesize fluorescent H4R ligands several fluorophores (pyrylium, bodipy and cyanine dyes) were coupled to a benzimidazole building block, reported to have high H4R affinity. The Ki-values of the labeled compounds were only in the micromolar range (1.3 - 30 µM) at the hH4R and the other HR subtypes as well, suggesting that a different affinity-conferring moiety should be selected. The investigation of selected H4R agonists revealed neither cytotoxicity nor hemolytic activity but remarkable plasma protein binding (up to 94 %), which has to be taken into account in future in vivo investigations. In summary, the structural variations of the cyanoguanidine-type H4R ligands produced valuable information regarding structure-activity and structure-selectivity relationships and led to several promising pharmacological tools. The identified hH4R agonist trans-(+)-(1S, 3S)-UR-RG98 is one of the most potent and selective H4R ligands identified so far. The optimized stereochemical properties of the ligands provide valuable information with respect to future ligand design and refined ligand-receptor models."
    - id: https://openalex.org/W406910919
      doi: null
      title: Cannabinoids delivery systems based on supramolecular inclusion complexes and polymeric nanocapsules for treatment of neuropathic pain
      publication_year: 2012
      relevance_score: 4.569052
      abstract: "Cannabinoids (CBs) and particularly CB2 agonists have been shown to reduce pain andinflammation without eliciting any apparent psychotropic effect conversely to CB1agonist compounds. CBs candidates are usually lipophilic non drug-like compoundswith poor bioavailability. To serve the purpose of evaluating new synthetic CB2 agonistsdeveloped by our group, on in vivo neuropathic pain models, an enabling formulationstrategy has been set up and four Drug Delivery Systems (DDS) developed. Forparenteral administration, cyclodextrin (CD)-based inclusion complexes, liposomes andsurfactants/co-solvents micellar solution have been investigated whereas Self-Emulsifying DDS (SEDDS) was selected for oral administration. A pharmacologicalstudy conducted with lead compound MDA7, formulated in CD-based DDS resulted inthe higher antinociceptive activity. A comprehensive study of the inclusion mechanismof MDA7 in the CD supramolecular complexes prepared was carried out. MDA7pharmacokinetic profile was also generated formulated in micellar solution and SEDDS.Besides, cationic polymeric nanocapsules (NCs) have been designed to serve as aprotective DDS for oral administration of a dietary phytocannabinoid CB2 agonist.Studies were undertaken to characterize and evaluate the influence of differentparameters on NCs formation prepared by nanoprecipitation. The cationic NCsdeveloped have been explored for their property to yield proportion of counterioniccondensation in the presence of macrocycles bearing anionic groups such assulfobutylether-beta-cyclodextrin or to form electrostatic interactions/host-guestcomplexion with cucurbit[n]uril."
    - id: https://openalex.org/W7167082190
      doi: https://doi.org/10.1038/s41392-026-02865-4
      title: Next-generation chemogenetic inhibition using a brain-permeant non-prescription agent
      publication_year: 2026
      relevance_score: 4.425892
      abstract: "Chemogenetics allows the controllable manipulation of brain circuits upon delivery of a selective activating ligand, and has been invaluable in dissecting brain circuits underlying many behaviours. The Gαi/o-coupled designer muscarinic receptor hM4Di is an especially versatile tool for on-demand inhibition, and has proven effective not only in fundamental neuroscience but also as a therapeutic transgene in preclinical models of epilepsy and other CNS disorders. Indeed, by placing the circuit modulation under the control of an exogenous ligand, chemogenetics mitigates the potential risk of overdosage intrinsic to viral-vector mediated gene therapy. An obstacle to clinical translation, however, is the absence of an activating ligand with favourable biodistribution and side effect profile. Here we show that mutation of hM4Di at two sites (S85 and Y416) imparts full and potent agonism to the widely used over-the-counter antihistamine diphenhydramine. We complement medium-throughput screening in human embryonic kidney cells with in vitro electrophysiological characterization in neuronal circuits, and reveal the interaction of diphenhydramine with key residues using cryo-electron microscopy. Administration of diphenhydramine to mice expressing the modified receptor in the ventral hippocampus reversibly modulated anxiety-related behaviour and attenuated the severity of chemoconvulsant-induced seizures. We further demonstrate on-demand seizure suppression in a chronic epilepsy model. G protein-coupled Receptors Activated by Non-Prescription Agents (GRANPAs) lower the barrier to clinical translation of a powerful chemogenetic approach to brain circuit manipulation."
```
/answer d21902c3-ceba-4394-8409-2892fc6d45ef allow
Control Request:
```yaml
id: 490e126c-3697-4d14-b50c-5af1bf95d276
toolName: openalex-search
arguments:
  query: diphenhydramine muscarinic receptor affinity anticholinergic Ki
  reason: Get muscarinic receptor potency for selectivity comparison
  fields: abstract
```
/answer 490e126c-3697-4d14-b50c-5af1bf95d276 allow
Control Request:
```yaml
id: 5fb5d49a-1803-4311-a7a2-f04fc9fb89b6
result:
  structuredContent:
    count: 28
    returned: 25
    page: 1
    per_page: 25
    results:
    - id: https://openalex.org/W4315486951
      doi: https://doi.org/10.3390/pharmaceutics15010230
      title: A Universal Pharmacological-Based List of Drugs with Anticholinergic Activity
      publication_year: 2023
      relevance_score: 119.02422
      abstract: "Anticholinergic burden tools have relevant pharmacological gaps that may explain their limited predictive ability for clinical outcomes. The aim of this study was to provide a universal pharmacological-based list of drugs with their documented affinity for muscarinic receptors. A comprehensive literature review was performed to identify the anticholinergic burden tools. Drugs included in these instruments were searched in four pharmacological databases, and the investigation was supplemented with PubMed. The evidence regarding the potential antagonism of the five muscarinic receptors of each drug was assessed. The proportion of drugs included in the tools with an affinity for muscarinic receptors was evaluated. A universal list of drugs with anticholinergic activity was developed based on their documented affinity for the different subtypes of muscarinic receptors and their ability to cross the blood-brain barrier. A total of 23 tools were identified, including 304 different drugs. Only 48.68%, 47.70%, 48.03%, 43.75%, and 42.76% of the drugs had an affinity to the M1, M2, M3, M4, and M5 receptor, respectively, reported in any pharmacological database. The proportion of drugs with confirmed antagonism varied among the tools (36.8% to 100%). A universal pharmacological-based list of 133 drugs is presented. It should be further validated in different clinical settings."
    - id: https://openalex.org/W2889719465
      doi: https://doi.org/10.3389/fphar.2018.00913
      title: A History of Drug Discovery for Treatment of Nausea and Vomiting and the Implications for Future Research
      publication_year: 2018
      relevance_score: 86.2893
      abstract: "The origins of the major classes of current anti-emetics are examined. Serendipity is a recurrent theme in discovery of their anti-emetic properties and repurposing from one indication to another is a continuing trend. Notably, the discoveries occurred against a background of company mergers and changing anti-emetic requirements. Major drug classes include: (i) Muscarinic receptor antagonists - originated from historical accounts of plant extracts containing atropine and hyoscine with development stimulated by the need to prevent sea-sickness among soldiers during beach landings; (ii) Histamine receptor antagonists - searching for replacements for the anti-malaria drug quinine, in short supply because of wartime shipping blockade, facilitated the discovery of histamine (H1) antagonists (e.g. dimenhydrinate), followed by serendipitous discovery of anti-emetic activity against motion sickness in a patient undergoing treatment for urticaria; (iii) Phenothiazines and dopamine receptor antagonists - investigations of their pharmacology as “sedatives” (e.g. chlorpromazine) implicated dopamine receptors in emesis, leading to development of selective dopamine (D2) receptor antagonists (e.g. domperidone with poor ability to penetrate the blood-brain barrier) as anti-emetics in chemotherapy and surgery; (iv) Metoclopramide and selective 5-hydroxytryptamine3 (5-HT3) receptor antagonists - metoclopramide was initially assumed to act only via D2 receptor antagonism but subsequently its gastric motility stimulant effect (contributing to anti-emetic action) was shown to be due to 5-hydroxytryptamine4 receptor agonism. Pre-clinical studies showed that anti-emetic efficacy against the newly-introduced, highly emetic, chemotherapeutic agent cisplatin was due to antagonism at 5-HT3 receptors. The latter led to identification of selective 5-HT3 receptor antagonists (e.g. granisetron), a major breakthrough in treatment of chemotherapy-induced emesis; (v) Neurokinin1 receptor antagonists - antagonists of the actions of substance P were developed as analgesics but pre-clinical studies identified broad-spectrum anti-emetic effects; clinical studies showed particular efficacy in the delayed phase of chemotherapy-induced emesis. Finally, the repurposing of different drugs for treatment of nausea and vomiting is examined, particularly during palliative care, and also the challenges in identifying novel anti-emetic drugs, particularly for treatment of nausea as compared to vomiting. We consider the lessons from the past for the future and ask why there has not been a major breakthrough in the last 20 years."
    - id: https://openalex.org/W4413305183
      doi: https://doi.org/10.1097/jcp.0000000000002073
      title: Anticholinergic Equivalence in Psychotropic Medications
      publication_year: 2025
      relevance_score: 84.49193
      abstract: "BACKGROUND: Anticholinergic side effects from psychotropic medications are common and can lead to significant adverse events, including cognitive impairment and falls, particularly in vulnerable populations like the elderly. The cumulative anticholinergic burden from multiple medications is a critical concern associated with poorer clinical outcomes. Quantifying this burden is essential for safer prescribing. METHODS: This article developed an anticholinergic equivalence (AE) table for various psychotropic medications. Diphenhydramine (AE=1) was used as the reference standard. AE values for other drugs were derived from their M1 muscarinic receptor binding affinities (Ki) relative to diphenhydramine. This allows estimation of the diphenhydramine equivalent burden per milligram of a given medication. Antihistaminic properties were also reviewed. RESULTS: An AE table was generated, detailing the anticholinergic potency of numerous psychotropic agents. Values varied significantly, with older tricyclic antidepressants (eg, amitriptyline AE: 8.99) and some antipsychotics (eg, clozapine AE: 6.67, olanzapine AE: 3.08) showing high anticholinergic equivalence. Many sedating medications (eg, quetiapine, mirtazapine) are noted to have potent antihistaminic but low anticholinergic properties, clarifying that sedation is not always due to anticholinergic effects. CONCLUSIONS: The anticholinergic equivalence table provides a practical, pharmacologically based tool for psychiatrists to quantify and compare the anticholinergic potential of psychotropic medications. This can aid in minimizing cumulative anticholinergic burden, making more informed prescribing decisions, and ultimately enhancing patient safety and therapeutic outcomes, especially in high-risk groups."
    - id: https://openalex.org/W3205136031
      doi: https://doi.org/10.2147/dddt.s329547
      title: The Expanding Role of Pyridine and Dihydropyridine Scaffolds in Drug Design
      publication_year: 2021
      relevance_score: 61.71962
      abstract: "Pyridine-based ring systems are one of the most extensively used heterocycles in the field of drug design, primarily due to their profound effect on pharmacological activity, which has led to the discovery of numerous broad-spectrum therapeutic agents. In the US FDA database, there are 95 approved pharmaceuticals that stem from pyridine or dihydropyridine, including isoniazid and ethionamide (tuberculosis), delavirdine (HIV/AIDS), abiraterone acetate (prostate cancer), tacrine (Alzheimer's), ciclopirox (ringworm and athlete's foot), crizotinib (cancer), nifedipine (Raynaud's syndrome and premature birth), piroxicam (NSAID for arthritis), nilvadipine (hypertension), roflumilast (COPD), pyridostigmine (myasthenia gravis), and many more. Their remarkable therapeutic applications have encouraged researchers to prepare a larger number of biologically active compounds decorated with pyridine or dihydropyridine, expandeing the scope of finding a cure for other ailments. It is thus anticipated that myriad new pharmaceuticals containing the two heterocycles will be available in the forthcoming decade. This review examines the prospects of highly potent bioactive molecules to emphasize the advantages of using pyridine and dihydropyridine in drug design. We cover the most recent developments from 2010 to date, highlighting the ever-expanding role of both scaffolds in the field of medicinal chemistry and drug development."
    - id: https://openalex.org/W2209617566
      doi: https://doi.org/10.1002/mdc3.12266
      title: "Clozapine in Parkinsonian Rest Tremor: A Review of Outcomes, Adverse Reactions, and Possible Mechanisms of Action"
      publication_year: 2015
      relevance_score: 46.557343
      abstract: "BACKGROUND: The pathogenesis of rest tremor in Parkinson's disease (PD) is incompletely understood. This symptom can be resistant to typical anti-PD medications. Therefore, new treatments are needed given the concern that this symptom causes to patients and family. Limited experience suggests that clozapine can have an important antitremor effect in PD. The mechanism(s) underlying this effect is not well understood, but could provide insight and impetus to the development of more-effective and safer antitremor therapies. METHODS AND RESULTS: Exemplifying the antitremor effects of clozapine, we describe a patient with tremor-predominant PD who obtained prominent reduction of rest tremor with clozapine treatment. We review the responses to this treatment in another 7 of our PD patients with treatment-resistant rest tremor. We also review the published literature on clozapine for tremor in PD and discuss its potential mechanisms of action and possible adverse effects. In our case series, there was a 64% reduction of tremor score after clozapine was initiated. The mechanism of tremor reduction remains unclear with possible involvement of anticholinergic, serotonergic, antihistaminergic, antiadrenergic, and antidopaminergic effects. Clozapine does have potential serious adverse effects. CONCLUSIONS: Clozapine may be effective in controlling rest tremor in PD. Given the potential fatal side effects, if clozapine is to be initiated in PD patients, it has to be used cautiously with proper monitoring, preferably in specialized centers. We acknowledge that the number of patients in this case series is small. Further studies are needed to understand clozapine's mechanism of action in reducing tremor."
    - id: https://openalex.org/W4384130528
      doi: https://doi.org/10.3389/fpsyt.2023.1185750
      title: "Pathophysiology and management of risperidone-induced sialorrhea: case report"
      publication_year: 2023
      relevance_score: 42.185524
      abstract: "Background: Among antipsychotics, sialorrhea is most associated with clozapine, and when it occurs, it is uncomfortable, socially stigmatizing, and can contribute to medication non-adherence. Risperidone has a generally negligible muscarinic activity compared to clozapine, and yet, multiple reports of severe sialorrhea associated with risperidone have been reported. Case presentation: This case report describes risperidone-induced sialorrhea that was unintentionally masked by simultaneous clonidine administration that was intended to treat hypertension. Interestingly, sialorrhea was present but mild when clonidine was present; however, when risperidone was further titrated and clonidine removed, a significant worsening of sialorrhea developed. Sialorrhea did not respond to treatment with anticholinergic medication. Conclusion: The pathophysiology of antipsychotic-induced sialorrhea is complex and varies between antipsychotics. Risperidone-induced sialorrhea is suspected of having prominent adrenergic pathophysiology that is likely composed of highly viscoelastic saliva (high protein content), differing from the more commonly encountered clozapine-induced sialorrhea. Risperidone-induced sialorrhea is reported as more likely to respond to dose reduction and treatment with α2-adrenergic receptor agonists or β-adrenergic receptor antagonists and less likely to respond to anticholinergic (antimuscarinic) medications."
    - id: https://openalex.org/W3113257430
      doi: https://doi.org/10.1016/j.euf.2021.10.009
      title: "Receipt of Overactive Bladder Drugs and Incident Dementia: A Population-based Case-control Study"
      publication_year: 2021
      relevance_score: 28.7892
    - id: https://openalex.org/W4316363162
      doi: https://doi.org/10.3389/fcell.2023.1072629
      title: "Neuropathic pain: Mechanisms and therapeutic strategies"
      publication_year: 2023
      relevance_score: 28.702194
      abstract: "The physiopathology and neurotransmission of pain are of an owe inspiring complexity. Our ability to satisfactorily suppress neuropathic or other forms of chronic pain is limited. The number of pharmacodynamically distinct and clinically available medications is low and the successes achieved modest. Pain Medicine practitioners are confronted with the ethical dichotomy imposed by Hippocrates: On one hand the mandate of primum non nocere , on the other hand, the promise of heavenly joys if successful divinum est opus sedare dolorem . We briefly summarize the concepts associated with nociceptive pain from nociceptive input (afferents from periphery), modulatory output [descending noradrenergic (NE) and serotoninergic (5-HT) fibers] to local control. The local control is comprised of the “ inflammatory soup ” at the site of pain origin and synaptic relay stations, with an ATP-rich environment promoting inflammation and nociception while an adenosine-rich environment having the opposite effect. Subsequently, we address the transition from nociceptor pain to neuropathic pain (independent of nociceptor activation) and the process of sensitization and pain chronification (transient pain progressing into persistent pain). Having sketched a model of pain perception and processing we attempt to identify the sites and modes of action of clinically available drugs used in chronic pain treatment, focusing on adjuvant (co-analgesic) medication."
    - id: https://openalex.org/W4210431202
      doi: https://doi.org/10.1093/ijnp/pyac005
      title: "Incidence of Drug-Induced Delirium During Treatment With Antidepressants or Antipsychotics: A Drug Surveillance Report of German-Speaking Countries Between 1993 and 2016"
      publication_year: 2022
      relevance_score: 28.630888
      abstract: "OBJECTIVES: Successful treatment of delirium depends on the detection of the reversible contributors. Drugs with delirogenic properties are the most prevalent reversible cause of delirium. METHODS: This observational study is based on data from Arzneimittelsicherheit in der Psychiatrie, a multicenter drug surveillance program in German-speaking countries recording severe adverse drug reactions (ADRs) in psychiatric inpatients. The present study analyzes drug-induced delirium (DID) during treatment with antidepressants and antipsychotics. RESULTS: A total of 436 565 psychiatric inpatients were treated with antidepressants and/or antipsychotics during the observation period from 1993 to 2016 in the participating 110 hospitals. Overall, 254 cases (0.06% of all patients treated with antidepressants and/or antipsychotics) of DID were detected. Implicated either in combination or alone (multiple drugs were implicated in 70.1% of DID), clomipramine (0.24%), amitriptyline (0.21%), and clozapine (0.18%) showed the highest incidence rates of DID. When implicated alone (98 cases overall), clozapine (0.11%) followed by amitriptyline (0.05%) were most likely causally associated with the occurrence of DID. Drugs with strong antimuscarinic properties generally exhibited higher risk of DID. CONCLUSIONS: With an incidence rate of <0.1%, the use of antidepressants and antipsychotics was rarely associated with DID within the Arzneimittelsicherheit in der Psychiatrie program. Tricyclic antidepressants and clozapine were the most commonly implicated psychotropic drugs. These data support the specific role of antimuscarinic properties in DID."
    - id: https://openalex.org/W4406274798
      doi: https://doi.org/10.1007/s40262-024-01466-0
      title: "Influence of Ageing on the Pharmacodynamics and Pharmacokinetics of Chronically Administered Medicines in Geriatric Patients: A Review"
      publication_year: 2025
      relevance_score: 28.311085
      abstract: "As people age, the efficiency of various regulatory processes that ensure proper communication between cells and organs tends to decline. This deterioration can lead to difficulties in maintaining homeostasis during physiological stress. This includes but is not limited to cognitive impairments, functional difficulties, and issues related to caregivers which contribute significantly to medication errors and non-adherence. These factors can lead to higher morbidity, extended hospital stays, reduced quality of life, and even mortality. The decrease in homeostatic capacity varies among individuals, contributing to the greater variability observed in geriatric populations. Significant pharmacokinetic and pharmacodynamic alterations accompany ageing. Pharmacokinetic changes include decreased renal and hepatic clearance and an increased volume of distribution for lipid-soluble drugs, which prolong their elimination half-life. Pharmacodynamic changes typically involve increased sensitivity to various drug classes, such as anticoagulants, antidiabetic and psychotropic medications. This review examines the primary age-related physiological changes in geriatrics and their impact on the pharmacokinetics and pharmacodynamics of medications."
    - id: https://openalex.org/W2989772907
      doi: https://doi.org/10.1186/s40360-019-0363-1
      title: "Antihistamine effects and safety of fexofenadine: a systematic review and Meta-analysis of randomized controlled trials"
      publication_year: 2019
      relevance_score: 27.9004
      abstract: "BACKGROUND: As a new generation antihistamine, fexofenadine has been widely used in allergic diseases. However, there is still a lack of collective evidence regarding the antihistamine effects and safety profiles of fexofenadine relative to other antihistamine drugs and placebo. Therefore, we aimed to systematically evaluate the antihistamine effects and safety of fexofenadine. METHODS: An electronic literature search of randomized controlled trials (RCTs) was performed using Embase, Cochrane and PubMed from establishment to January 1st, 2018. RCTs comparing the antihistamine effects or safety (adverse events, sedative effects, and cognitive/psychomotor function) of fexofenadine with either other antihistamines or placebo for healthy subjects and patients with allergy were selected. RESULTS: Fifty-one studies of 14,551 participants met the inclusion criteria. When compared with the first-generation antihistamines, fexofenadine produced significantly lower adverse events frequency (OR = 0.446; 95% CI: 0.214 to 0.929, P = 0.031), significantly lower sedative effects frequency (OR = 0.265; 95% CI: 0.072 to 0.976, P = 0.046) and significantly less change of all cognitive/psychomotor function. When compared with the second-generation antihistamines, fexofenadine produced significantly marginal sedative effects (OR = 0.59; 95% CI, 0.38 to 0.93; P = 0.02) and significantly less change of most of the cognitive/psychomotor function. When compared with placebo, fexofenadine produced more significant antihistamine effects. CONCLUSIONS: Fexofenadine has a positive antihistamine effect, which is probably no worse than the second-generation antihistamines. Fexofenadine probably has a favorable safety profile, which is more likely better than that of the first-generation antihistamines. There is lack of data to support that fexofenadine has a better overall safety profile compared to the second-generation antihistamines, however, some presently available evidence on sedative effects and certain aspects of cognitive/psychomotor function favors fexofenadine. Therefore, fexofenadine may be worthy of recommendation for safety related workers."
    - id: https://openalex.org/W1984380615
      doi: https://doi.org/10.2147/jaa.s3108
      title: Ebastine in the light of CONGA recommendations for the development of third-generation antihistamines
      publication_year: 2009
      relevance_score: 26.018562
      abstract: "In 2003 a consensus group on new-generation antihistamines (CONGA) defined the characteristics required for a third-generation H(1) antihistamine as there had been much controversy about this issue since the early 1990s. One of the antihistamines that had been claimed to belong to such a group is the second-generation antihistamine, ebastine. The objective of this review is to analyze the pharmacology of ebastine, in light of the CONGA recommendations for the development of new-generation antihistamines: (1) anti-inflammatory properties, (2) potency, efficacy and effectiveness, (3) lack of cardiotoxicity, (4) lack of drug interactions, (5) lack of CNS effects, and (6) pharmacological approach. Ebastine seems to have anti-inflammatory properties that help to ameliorate nasal congestion, though this has not yet been conclusively demonstrated. Its pharmacological-therapeutic profile does not differ greatly from that of other second-generation antihistamines. Its cardiac safety has been widely assessed and no cardiac toxicity has been found at therapeutic doses despite initial concerns. The risk of potentially relevant drug interactions has been investigated and ruled out. Ebastine does not produce sedation at therapeutic doses and drug interaction studies with classical CNS depressants have not demonstrated a synergistic effect. Pharmacologically, ebastine is an H(1) inverse agonist. Perhaps the answer to the quest for new-generation antihistamines lies not only in H(1) but in a combined approach with other histamine receptors."
    - id: https://openalex.org/W4386096306
      doi: https://doi.org/10.3390/toxics11090723
      title: Antidotes in Clinical Toxicology—Critical Review
      publication_year: 2023
      relevance_score: 24.893803
      abstract: "Poisoning and overdose are very important aspects in medicine and toxicology. Chemical weapons pose a threat to civilians, and emergency medicine principles must be followed when dealing with patients who have been poisoned or overdosed. Antidotes have been used for centuries and modern research has led to the development of new antidotes that can accelerate the elimination of toxins from the body. Although some antidotes have become less relevant due to modern intensive care techniques, they can still save lives or reduce the severity of toxicity. The availability of antidotes is crucial, especially in developing countries where intensive care facilities may be limited. This article aims to provide information on specific antidotes, their recommended uses, and potential risks and new uses. In the case of poisoning, supportive therapies are most often used; however, in many cases, the administration of an appropriate antidote saves the patient’s life. In this review, we reviewed the literature on selected antidotes used in the treatment of poisonings. We also characterised the antidotes (bio)chemically. We described the cases in which they are used together with the dosage recommendations. We also analysed the mechanisms of action. In addition, we described alternative methods of using a given substance as a drug, an example of which is N-acetylcysteine, which can be used in the treatment of COVID-19. This article was written as part of the implementation of the project of the Polish Ministry of Education and Science, “Toxicovigilance, poisoning prevention, and first aid in poisoning with xenobiotics of current clinical importance in Poland”, grant number SKN/SP/570184/2023."
    - id: https://openalex.org/W2296589160
      doi: https://doi.org/10.1093/database/bav087
      title: "Connecting proteins with drug-like compounds: Open source drug discovery workflows with BindingDB and KNIME"
      publication_year: 2015
      relevance_score: 22.854467
      abstract: "Today's large, public databases of protein-small molecule interaction data are creating important new opportunities for data mining and integration. At the same time, new graphical user interface-based workflow tools offer facile alternatives to custom scripting for informatics and data analysis. Here, we illustrate how the large protein-ligand database BindingDB may be incorporated into KNIME workflows as a step toward the integration of pharmacological data with broader biomolecular analyses. Thus, we describe a collection of KNIME workflows that access BindingDB data via RESTful webservices and, for more intensive queries, via a local distillation of the full BindingDB dataset. We focus in particular on the KNIME implementation of knowledge-based tools to generate informed hypotheses regarding protein targets of bioactive compounds, based on notions of chemical similarity. A number of variants of this basic approach are tested for seven existing drugs with relatively ill-defined therapeutic targets, leading to replication of some previously confirmed results and discovery of new, high-quality hits. Implications for future development are discussed. Database URL: www.bindingdb.org."
    - id: https://openalex.org/W4392197090
      doi: https://doi.org/10.1017/s1478951524000117
      title: "Concomitant use of hydroxyzine and haloperidol did not worsen delirium in patients with cancer: A multicenter, retrospective, observational study"
      publication_year: 2024
      relevance_score: 11.768445
      abstract: "Abstract Objectives There is concern that hydroxyzine exacerbates delirium, but a recent preliminary study suggested that the combination of haloperidol and hydroxyzine was effective against delirium. This study examined whether the concomitant use of hydroxyzine and haloperidol worsened delirium in patients with cancer. Methods This retrospective, observational study was conducted at 2 general hospitals in Japan. The medical records of patients with cancer who received haloperidol for delirium from July to December 2020 were reviewed. The treatments for delirium included haloperidol alone or haloperidol combined with hydroxyzine. The primary outcome was the duration from the first day of haloperidol administration to the resolution of delirium, defined as its absence for 2 consecutive days. The time to delirium resolution was analyzed to compare the haloperidol group and hydroxyzine combination group using the log-rank test with the Kaplan–Meier method. Secondary outcomes were (1) the total dose of antipsychotic medications, including those other than haloperidol (measured in chlorpromazine-equivalent doses), and (2) the frequencies of detrimental incidents during delirium, specifically falls and self-removal of drip infusion lines. The unpaired t -test and Fisher’s exact test were used to analyze secondary outcomes. Results Of 497 patients who received haloperidol, 118 (23.7%) also received hydroxyzine. No significant difference in time to delirium resolution was found between the haloperidol group and the hydroxyzine combination group (log-rank test, P = 0.631). No significant difference between groups was found in either chlorpromazine-equivalent doses or the frequency of detrimental incidents. Significance of results This study showed that the concomitant use of hydroxyzine and haloperidol did not worsen delirium in patients with cancer."
    - id: https://openalex.org/W3048582011
      doi: https://doi.org/10.25772/cmq2-4a23
      title: ANTICHOLINERGIC BURDEN AND RISK OF COGNITIVE IMPAIRMENT IN OLDER ADULTS
      publication_year: 2020
      relevance_score: 10.716678
      abstract: "Studies reveal that 10-27% of older adults chronically use anticholinergic medications. Increased cumulative anticholinergic burden scores are associated with increased risks of dementia. The mechanisms by which anticholinergic drugs negatively impact cognition remain elusive. However, researchers speculate that the drug’s impairment of cholinergic neurons promotes neuroinflammation.\\nWe hypothesize that drugs with anticholinergic properties will induce inflammation in the brain. MCP1 and IL 6 are chemokines that contribute to neuroinflammation. We investigated the influence of diphenhydramine (Benadryl) on the production of MCP1 and IL-6 in Normal Human Astrocytes and Paroxetine on the production of MCP1 in Normal Human Astrocytes and Normal Human Brain Microvascular Endothelial Cells.\\nNormal Human Astrocytes were cultured (seeded at 5,000 cells/cm2) and treated with a clinically relevant concentration (equivalent to clinically observed Cmax for the respective drugs) of diphenhydramine (66ng/ml) and Paroxetine (1.67*10-4mM). RNA was isolated and converted into cDNA, and then gene expression was measured via RT-PCR. MCP1 and IL-6 protein production were measured from cell culture supernatants by ELISA. One-way ANOVA compared MCP-1 and IL-6 protein concentrations with Tukey correction for multiple corrections. The gene expression was reported with relative significance (p= 0.05) using Student’s t-test.\\nDrugs with anticholinergic properties are considered to be pro-inflammatory. However, our data from normal human astrocytes treated suggest that diphenhydramine possesses anti-inflammatory properties. This preliminary finding suggests the possibility of pathological mechanisms of anticholinergic medications with dementia that may not be associated with inflammation.\\nOur data from Paroxetine in normal human brain microvascular endothelial cells suggest that Paroxetine possesses pro-inflammatory properties. Our preliminary findings indicate the possibility of a pathological pro-inflammatory mechanism associated with Paroxetine. Further evaluation of anticholinergic drugs in the human brain is warranted."
    - id: https://openalex.org/W7134287882
      doi: https://doi.org/10.3389/fpsyt.2026.1807080
      title: "Commentary: Real-world effectiveness and safety of xanomeline and trospium for treatment-resistant schizophrenia in a state hospital system"
      publication_year: 2026
      relevance_score: 8.580256
      abstract: "We appreciated the article \"Real-world effectiveness and safety of xanomeline and trospium for treatment-resistant schizophrenia in a state hospital system\" by Vadiei N and Crismon ML (2026) (Front Psychiatry 16:1736922. doi: 10.3389/fpsyt.2025.1736922) (1). This retrospective study was especially fascinating because the prescribing practices frequently challenged the clinically significant warnings and precautions found in the FDA prescribing guidelines for xanomeline/trospium chloride (KarXT) (2), generating real-world evidence that further reinforces those guidelines for safety and efficacy. Not surprisingly, combining KarXT with medications that can raise xanomeline levels, along with laxatives, increased procholinergic gastrointestinal adverse effects (e.g. nausea, vomiting, diarrhea, sialorrhea) in this study.Likewise, combining KarXT with anticholinergic medications increased peripheral anticholinergic side effects (e.g. blurry vision, tachycardia, gastroesophageal reflux/dyspepsia, constipation, urinary retention) from the trospium component. Additionally, administering KarXT in conjunction with centrally-acting anticholinergic medications attenuated the procholinergic benefits of xanomeline for treatment of schizophrenia symptoms. Consequently, a thorough analysis of this study provides a valuable opportunity to apply FDA prescribing guidelines, extant data, along with our clinical experience treating over 100 patients with KarXT to date, building upon our previously published case series (3), in developing a more nuanced treatment approach to utilizing KarXT successfully. Tailored KarXT adjustments for potential drug-drug interactions (listed parenthetically in this study below), food administration, titration schedule, and prophylactic or rescue ondansetron are useful strategies that can help meet the individual needs of complex patients with schizophrenia, taking multiple medications at baseline. 2 Reviewing Potential KarXT Drug-Drug Interactions (4) Firstly, it is important to consider potential pharmacokinetic interactions affecting plasma exposure, Cmax (maximum concentration) and AUC (area under the curve) of xanomeline and trospium when prescribing KarXT in combination with other medications. According to the KarXT package insert, use in CYP2D6 intermittent/poor metabolizers or concomitant use with strong hepatic CYP2D6 inhibitors (2) (e.g. strong-bupropion, terbinafine; moderate-sertraline, haloperidol, hydroxyzine) may increase systemic plasma concentrations of xanomeline, which may increase frequency and/or severity of xanomeline-related adverse reactions. For example, based on a population pharmacokinetic analysis, median Cmax and median AUC of xanomeline increased approximately 28% and 15%, respectively, in intermediate metabolizers (2). Further, xanomeline transiently inhibits both CYP3A4 and P-glycoprotein locally in the intestine (first-pass), which may increase plasma concentrations of oral sensitive substrates (2) (e.g. CYP3A4 substrates-clonazepam, metoprolol, haloperidol, hydroxyzine, aripiprazole, risperidone, clozapine, benztropine, quetiapine, terbinafine, lurasidone, suvorexant, trazodone, amlodipine, melatonin, tamsulosin, loratadine, chlorpromazine, buspirone, mirtazapine; P-glycoprotein substrates-aripiprazole, risperidone, paliperidone, quetiapine, valsartan, amlodipine, famotidine, tamsulosin, loratidine, lorazepam, sitagliptin), increasing the frequency and/or severity of adverse reactions from those substrates. Drugs eliminated by active tubular secretion (2) (e.g. amantadine, metformin [decreases trospium], clozapine, atropine, famotidine, glycopyrrolate, nicotine, sitagliptin) may increase plasma concentrations of trospium, and/or the concomitantly used drug, which may increase the frequency and/or severity of adverse reactions.Secondly, it is also important to consider potential pharmacodynamic interactions of co-prescribed anticholinergic medications affecting additive anticholinergic burden with trospium and receptor-level competition affecting procholinergic benefits with xanomeline.Concomitant use of KarXT with other anticholinergics (2) (e.g. glycopyrrolate) may increase the frequency and/or severity of peripheral anticholinergic side effects. Moreover, the mechanism of action of KarXT is thought to be related to its central agonist activity at M1 and M4 muscarinic acetylcholine receptors, with comparable affinity at M1-M5 (Ki=10, 12,17, 7, and 22 nM, respectively) (2), such that combining KarXT with central M1 and M4 antagonists in the nM range (e.g. olanzapine, clozapine, quetiapine, atropine, chlorpromazine, benztropine, diphenhydramine) can attenuate efficacy. However, individual results can vary as the Ki values for xanomeline may be lower than several anticholinergic antipsychotics used successfully with KarXT in treatment-resistant schizophrenia (TRS) (5), and certainly for concomitant non-anticholinergic antipsychotics in TRS (6). Ki values need to be interpreted in context of in vivo receptor occupancy and activity, which also depends on free plasma concentration, blood-brain barrier penetration, and dynamic pharmacokinetic factors.KarXT should be administered twice daily at least one hour before meals and at least two hours after meals because trospium's AUC absorption can be reduced 85%-90% with a high fat meal, and xanomeline's AUC can be increased 30% compared to fasted state (2). This imbalance may transiently amplify procholinergic effects during early titration by relatively reducing peripheral antagonism, while modestly increasing central and peripheral agonist exposure from unopposed xanomeline. Nevertheless, the authors note that KarXT was administered without regard to this food warning, which explains the high rate of xanomeline-related procholinergic side effects, limiting tolerability and often curtailing an adequate trial to capture the full benefits of KarXT (1). This warning is especially important during the first 4 weeks of dose titration, when procholinergic side effects can predominate for a couple weeks until tolerability develops, especially when moving from the 50 mg xanomeline/20 mg trospium dose to the 100 mg xanomeline/20 mg trospium dose, where the xanomeline dose doubles, yet the trospium dose remains the same. This is further mitigated by titrating up to the highest dose of 125 mg xanomeline/30 mg trospium. Following the first 4 weeks, taking KarXT with food can help mitigate anticholinergic side effects of trospium by limiting its absorption (7,8). This is a useful strategy in patients who have anticholinergic side effects but require strongly anticholinergic antipsychotics for stability while titrating KarXT to full effect, prior to gradually tapering these meds. Conversely, stable patients have been able to successfully taper off previous antipsychotics over 2 weeks prior to initiating KarXT (8).Given that the procholinergic side effects of xanomeline tend to predominate during KarXT initiation and the initial titration, using prophylactic or as needed (PRN) ondansetron has been largely effective in real-world TRS practice. In a retrospective analysis of 90 patients initiating KarXT while taking antipsychotics, prophylactic (21%) or PRN (44%) ondansetron yielded improvement in nausea or vomiting (71%). This includes those transitioning from clozapine (11%), olanzapine (24%), or other antipsychotics in helping patients stay on treatment until these side effects abate, without adding further anticholinergic burden from other antiemetics. Adverse effects from the addition of ondansetron, such as QT-prolongation, were not observed (9). Unfortunately, ondansetron was utilized in only one patient in this study (1, Supplement).While we appreciate the courage to add KarXT to complicated medication regimens in patients suffering with TRS, concluding that KarXT would necessarily be intolerable and ineffective in this population may be more reflective of implementation factors (Table 1). The authors acknowledge that the retrospective design may limit causal inference and that illness severity, institutional prescribing constraints, and baseline comorbidity burden may have also influenced outcomes (1). Nonetheless, the majority of patients (80%) were treated off label for a diagnosis of schizoaffective disorder rather than schizophrenia, potentially necessitating treatments other than KarXT. Notwithstanding that ondansetron was rarely provided, all reports of nausea, vomiting, diarrhea could have been explained by taking KarXT with food, which is the highest priority and most effective means to mitigate these side effects. Careful attention needs to be paid to drug-drug interactions that can either raise xanomeline exposure and side effects (CYP2D6 inhibitors), raise levels of other medications and side effects (intestinal CYP3A4 and P-glucoprotein substrates), compete for active tubular secretion, or add to anticholinergic side effects and may attenuate xanomeline's first-in-class putative mechanism of action."
    - id: https://openalex.org/W2594753874
      doi: null
      title: Empathy and the subjective-behavioural effects of D1 and D2 receptor blockade in pathological gamblers
      publication_year: 2015
      relevance_score: 4.5241294
      abstract: "This study assessed the relationship between Empathy and reinforcing effects of gambling and a psychostimulant drug, in 30 otherwise healthy pathological gamblers (PGs). To explore the roles of dopamine D1 and D2 receptors in these relationships, subjects received either: D2 antagonist, haloperidol (3-mg) or D1-D2 antagonist, fluphenazine (3-mg), in a placebo-controlled, double-blind, counterbalanced design. On separate sessions, subjects played a 15-minute slot machine game and received d-amphetamine (AMPH; 20-mg, oral). Under placebo, Empathy correlated positively with Desire to Gamble (DTG) at all time-points in both groups. Haloperidol negated, whereas fluphenazine enhanced, the correlation between Empathy and pleasurable effects of the slot machine. Haloperidol enhanced, whereas fluphenazine attenuated, the correlation between Empathy and DTG under AMPH. Results suggest post- synaptic D2 receptors may mediate Empathy-related differences in Liking of gambling; D1 receptors may mediate Empathy-related differences in Wanting to gamble under AMPH in PGs. Low statistical power and restricted generalizability were limitations."
    - id: https://openalex.org/W2472086479
      doi: https://doi.org/10.5283/epub.30043
      title: Synthesis and pharmacological characterization of new histamine H1-/H4-receptor ligands derived from the atypical antipsychotic drug Clozapine
      publication_year: 2016
      relevance_score: 4.3687825
      abstract: "The combined application of mepyramine (H1R-antagonist) and JNJ7777120 (H4R-antagonist) evoked a synergistic inhibitory effect on the eosinophil accumulation in the bronchoalveolar lavage fluid in the acute murine asthma model, pointing out that the H1R as well as the H4R is involved in type-I-allergic diseases. Molecules bearing pharmacophores that address both receptors could therefore be useful in therapy for this kind of diseases, such as, e.g., histamine induced itch or inflammatory asthma. As the antipsychotic drug Clozapine exhibits (among others) affinity to the H1R and the H4R, the modified Clozapine derivative 7-chloro-11-(4-methylpiperazin-1-yl)dibenzo[b,f][1,4]oxazepine was developed by Smits et al. revealing an increased agonistic affinity to H4R as well as a constantly high antagonistic affinity to the H1R. Based on this compound we prepared a series of molecules with modified substitution pattern and piperazine moiety in order to obtain a closer insight into structure activity relationships at H1R and H4R. Furthermore, from the most promising compounds, new dimeric molecules with different spacer-lengths and types were prepared, linking the modified Clozapine derivatives in different positions of the molecule. All compounds were characterized at the guinea pig ileum in the presence of histamine and in a competition binding assay at hH1R and hH4R. Moreover, to explain structure activity relationships on a molecular level, molecular modelling studies at appropriate models of hH1R and hH4R were performed."
    - id: https://openalex.org/W4406118399
      doi: https://doi.org/10.4088/jcp.24m15569
      title: Effects of Intravenous Hydroxyzine Versus Haloperidol Monotherapy for Delirium
      publication_year: 2025
      relevance_score: 2.6489682
      abstract: "Objective: Although antipsychotics are used commonly for delirium, they increase the risk of mortality in elderly patients and those with dementia.As hydroxyzine has sedative and anxiolytic effects, it can be used in the treatment of delirium.We performed a retrospective study to compare the effects of intravenous hydroxyzine and haloperidol monotherapy on delirium.Methods: Patients who admitted to a university hospital from April 1, 2017, to September 30, 2022, and received either hydroxyzine or haloperidol intravenously as monotherapy for the treatment of delirium were included.The time to and rate of delirium improvement were compared.Improvement of delirium was defined as negative on the Confusion Assessment Method (CAM) or Confusion Assessment Method for the ICU (CAM-ICU) for 3 consecutive days.Results: Among 5,555 patients who developed delirium, 71 (1.3%) and 82 (1.5%) received intravenous hydroxyzine and haloperidol monotherapy, respectively.The time to delirium improvement was 7.0 days (95% CI, 5.7-8.3days) for hydroxyzine and 8.2 days (95% CI, 7.6-8.8days) for haloperidol, with no significant difference between the two groups (P = .059).On the other hand, the rate of delirium improvement was 23.9% for hydroxyzine and 8.5% for haloperidol, with a significant difference in favor of the hydroxyzine group (P = .009). Conclusions:We first showed that intravenous hydroxyzine monotherapy was not inferior for the time to delirium improvement and superior for the rate of delirium improvement to intravenous haloperidol monotherapy.Considering that hydroxyzine is relatively safe with few side effects, it can be a viable option for delirium as an alternative to antipsychotics."
    - id: https://openalex.org/W4405839960
      doi: https://doi.org/10.1002/9781394182862.ch19
      title: Phenotypic Polypharmacology Drug Discovery for <scp>CNS</scp> Applications
      publication_year: 2024
      relevance_score: 2.552001
      abstract: "The complexity of the central nervous system (CNS), characterized by an intricate interplay among multiple neurotransmitter systems, poses a substantial challenge for drug discovery, especially for neuropsychiatric disorders. Not surprisingly, most psychiatric drugs rely on polypharmacology, the simultaneous modulation of multiple targets by a single drug, often the result of phenotypic, and in many cases serendipitous, observations. In this light, approaching CNS drug discovery through a target-agnostic in vivo phenotypic profiling of compounds may provide the best strategy for the successful identification of novel CNS drugs. To prosecute effectively, such a strategy must rely on infrastructure that is high throughput, standardized, and unbiased, i.e., a system that holistically assesses the CNS effects of compounds without preconceptions on pharmacological targets. We believe that target agnostic strategies should drive the identification of new leads and the development of structure-activity relationships (SAR) in lead optimization campaigns. After briefly analyzing the history of psychopharmacology to learn what worked (and what did not) in the drug discovery process, we will present examples of target agnostic approaches to drug discovery based on SmartCube®, a proprietary platform that integrates behavior phenotype profiling in vivo with innovative machine learning (ML) and artificial intelligence (AI). We will present examples of the high-content behavioral phenotypic profiles obtained by exploring privileged scaffolds, such as tryptamine and 1,2 benzisoxazole, and highlight how structural modifications result in prominent changes in potency, therapeutic window, and overall CNS profile of the derivative compounds. As a different example, we highlight the power of target agnostic approaches in the discovery of ulotaront, a putative antipsychotic currently in Phase III clinical trials with a first-in-class mechanism of action (MOA) that does not target dopamine receptors and has a placebo-like tolerability profile. In conclusion, this chapter illustrates our view that in vivo phenotypic profiling, what we called behavioral phenotypic drug discovery (BPDD) is better suited for CNS drug discovery than traditional approaches due to its target agnostic nature and its potential to identify treatments with novel MOAs."
    - id: https://openalex.org/W7128433781
      doi: https://doi.org/10.5114/ain.2025.158884
      title: "Tianeptine use disorder: a\_narrative review"
      publication_year: 2025
      relevance_score: 2.485542
      abstract: "Introduction: Tianeptine is an atypical tricyclic antidepressant with a unique, multi-receptor effect increasingly reported as having addictive potential over the past two decades.This narrative review summarises the current knowledge on tianeptine use disorder, including neurobiological mechanisms, clinical presentation, principles of diagnosis and treatment of abuse consequences.Review of available knowledge: Tianeptine, introduced into therapy in the 1980s in France, is currently administered in dozens of countries as an antidepressant with additional anxiolytic effects.Its activity includes the modulation of the glutamatergic system through the activation of opioid receptors and influence on neuroplasticity.The discovery that tianeptine is an opioid receptor agonist proved crucial to understanding its addictive potential.Abuse of tianeptine was initially observed in the 1990s mainly in European countries and has been on the rise since 2010 in the USA.Those with StreszczenieWprowadzenie: Tianeptyna jest atypowym, trjpiercieniowym lekiem przeciwdepresyjnym o unikalnym, wieloreceptorowym mechanizmie dziaania.W ostatnich dwch dekadach coraz czciej pojawiaj si informacje o jej potencjale uzaleniajcym"
    - id: https://openalex.org/W7140108333
      doi: https://doi.org/10.1177/02698811261431056
      title: "Trip killers: Addressing a critical knowledge gap in psychedelic research"
      publication_year: 2026
      relevance_score: 2.4535315
      abstract: "Psychedelic drugs are increasingly under investigation as potential therapeutic agents for mental health conditions and are being increasingly used recreationally. Psychedelic use may result in an episode of intense psychological distress, commonly referred to as a \"bad trip.\" Bad trips represent a potentially volatile, erratic, and dangerous situation, which may, in extreme cases, require presentation to accident and emergency departments and psychiatric hospital admission. Managing such cases requires careful consideration, with priority given to non-pharmacological strategies. When these measures prove insufficient, an alternative approach may be necessary, one that can effectively attenuate or terminate the psychedelic state and restore psychological stability. Despite clinical relevance, there is no systematic evaluation of pharmacological interventions to terminate such experiences. This review identifies and critically appraises candidate medications with potential utility as abortive agents, including serotonin antagonists, drugs for psychosis, and select drugs for anxiety and depression. We review these agents, their mechanisms of action, pharmacokinetics, safety profiles, and applicability in acute care settings. Binding strength at the molecular level, potency to functionally block receptor-mediated effects, and lack of side effects are key considerations. We conclude by proposing a provisional framework for the pharmacologic management of adverse psychedelic experiences and highlight key priorities for future research."
    - id: https://openalex.org/W4403196897
      doi: https://doi.org/10.15406/jaccoa.2024.16.00603
      title: What anesthesiologists need to know about Antidepressants and other Psychotropic Drugs
      publication_year: 2024
      relevance_score: 2.0414793
      abstract: "Psychotropic medications are widely prescribed and are a mainstay treatment for various mental health disorders. A significant portion of patients undergoing surgery or various procedures take these medications. With the rising prevalence of mental health conditions, anesthesiologists increasingly find themselves encountering patients who depend on these medications, making the understanding of potential interactions with anesthetic agents crucial during the perioperative period. Appreciating the adverse-effect profiles and familiarity with the clinically relevant drug interactions that may occur in the perioperative setting are imperative to ensure the best possible outcome in delivering patient care. This review focuses on various classes of psychotropic agents, including antidepressants, antipsychotics, mood stabilizers, and anxiolytics. It covers the pharmacodynamics and pharmacokinetics of these medication classes and their interactions with agents commonly used in anesthesia."
    - id: https://openalex.org/W4391569316
      doi: https://doi.org/10.3389/978-2-8325-4421-1
      title: Case reports in psychopharmacology
      publication_year: 2024
      relevance_score: 1.984156
      abstract: "Frontiers in Psychiatry is proud to present our Case Reports series. Our case reports aim to highlight unique cases of patients that present with an unexpected/unusual diagnosis, treatment outcome, or clinical course. Case reports provide insight into the differential diagnosis, decision-making, and clinical management of unusual cases and are a valuable educational tool.<br/><br/>This Research Topic will only accept Case Reports or Community Case Studies, but also relevant Opinions and Perspectives may be considered, all manuscripts must be original with the aim to significantly advance the field to be considered. We welcome contributions that cover all aspects of Psychopharmacology."
```
/answer 5fb5d49a-1803-4311-a7a2-f04fc9fb89b6 allow
ReasoningToken: 534
Control Request:
```yaml
id: 250fdedb-9c28-49e5-9ade-1e2ae03f441f
toolName: web-search-exa
arguments:
  query: diphenhydramine Ki H1 receptor 1 nM muscarinic receptor Ki nM binding affinity
  reason: Get precise Ki values for DPH at H1 and muscarinic receptors for selectivity index calculation
```
/answer 250fdedb-9c28-49e5-9ade-1e2ae03f441f allow
ReasoningToken: 195
Control Request:
```yaml
id: ade0dfb8-3887-4df0-8762-b807b7cb03ae
result:
  structuredContent:
    content: |-
      Title: Diphenhydramine Documentation Hub | BenchChem
      URL: https://www.benchchem.com/product/B000027/docs
      Published: N/A
      Author: N/A
      Highlights:
      The following tables summarize the binding affinities (Ki, nM) of diphenhydramine for various CNS targets. A lower Ki value indicates a stronger binding affinity.
      ...
      | Receptor | Diphenhydramine Ki (nM) | Reference |
      | --- | --- | --- |
      | Histamine H1 | 14.08 - 16 | [20],[6] |
      | Muscarinic M1 | 210 | [20] |
      | Muscarinic M2 | 130 | [20] |
      | Muscarinic M3 | 240 | [20] |
      | Muscarinic M4 | 112 | [20] |
      | Muscarinic M5 | 260 | [20] |
      ...
      outlines a competitive binding assay to determine the affinity (Ki) of diphenhydramine for a target receptor (e.g., Histamine H1).
      ...
      | Target Receptor/Channel | Species | Value (nM) | Value Type | Reference |
      | --- | --- | --- | --- | --- |
      | Muscarinic M1 Receptor | Human | 80–100 | Ki | [1] |
      | Muscarinic M2 Receptor | Human | 120–490 | Ki | [1] |
      | Muscarinic M3 Receptor | Human | 84–229 | Ki | [1] |
      | Muscarinic M4 Receptor | Human | 53–112 | Ki | [1] |
      | Muscarinic M5 Receptor | Human | 30–260 | Ki | [1] |
      | Voltage-gated Sodium Channel | Rat | 48000–86000 | Ki | [1] |
      | hERG Potassium Channel | Human | 27100 | IC50 | [1] |
      | h
      ...
      K+ channel | Not Specified | 5200 | IC50 | [1
      ...
      ] |
      | Proton Channel (H V 1) | Murine | 42000 | IC50 | [
      ...
      ] |
      | Histamine H4 Receptor | Human | >10000 | Ki | [11] |
      ...
      | HIV/EBOV pseudotyped virus | Not Applicable | 2600 | IC50 | [12] |
      ...
      /MARV pseudotyped virus |
      ...
      7600 | IC50 | [12] |
      ...
      Table 1
      ...
      Ki, nM
      ...
      | Receptor | Diphenhydramine | Cetirizine | Fexofenadine |
      | --- | --- | --- | --- |
      | Histamine H1 | 14.08[7] | ~6[7] | ~10[7] |
      | Muscarinic M1 | 210[7] | >10,000[7] | >10,000[7] |
      | Muscarinic M2 | 130[7] | >10,000[7] | >10,000[7] |
      | Muscarinic M3 | 240[7] | >10,000[7] | >10,000[7] |
      | Muscarinic M4 | 112[7] | >10,000[7] | >10,000[7] |
      | Muscarinic M5 | 260[7] | >10,000[7] | >10,000[7] |
      | Alpha-1 Adrenergic | 430[7] | >10,000[7] | >10,000[7] |
      | Alpha-2 Adrenergic | 7,600[7] | >10,000[7] | >10,000[7] |
      ...
      A lower Ki value indicates a higher binding affinity.[
      ...
      Diphenhydramine's sedative and other side effects are not solely attributable to its action on the histamine H1 receptor. It exhibits a broad receptor binding profile, interacting with various other neurotransmitter receptors, which contributes to its overall pharmacological effects. The following table summarizes the binding affinities (Ki) of Diphenhydramine for several key receptors. A lower Ki value indicates a higher binding affinity.
      ...
      | Receptor Subtype | Ki (nM) |
      | --- | --- |
      | Histamine Receptors |
      | Histamine H1 | 14.08 - 20 |
      | Muscarinic Acetylcholine (B1216132) Receptors |
      | Muscarinic M1 | 83 - 210 |
      | Muscarinic M2 | 130 - 230 |
      | Muscarinic M3 | 130 - 240 |
      | Muscarinic M4 | 112 - 160 |
      | Muscarinic M5 | 120 - 260 |
      | Adrenergic Receptors |
      | Alpha-1 | 430 |
      | Alpha-2 | 7,600 |
      | Serotonin Receptors |
      | 5-HT2A | 1295 |
      ...
      a test compound
      ...
      henhydramine
      ...
      histamine H1 receptor

      ---

      Title: Diphenhydramine (hydrochloride) - Biochemicals - CAT N°: 11158
      URL: https://www.bertin-bioreagent.com/diphenhydramine-hydrochloride/
      Published: 2024-07-16T00:00:00.000Z
      Author: N/A
      Highlights:
      Diphenhydramine (DPH) is a first generation antihistamine that is a potent antagonist of the histamine H1 receptor (Ki = 11.7 nM using human recombinant receptors).{15199,22787} DPH readily crosses the blood-brain barrier and produces diverse cognitive and psychomotor effects.{15199,22788} DPH also antagonizes muscarinic cholinergic receptors (Kis = 100 to 260 nM for M1-M5), increasing the range of central nervous system effects and applications.{22786} This product is also available as an analytical reference standard (Item No. 22489).

      ---

      Title: Diphenhydramine
      URL: https://en.wikipedia.org/wiki/Diphenhydramine
      Published: 2026-06-08T00:00:00.000Z
      Author: N/A
      Highlights:
      | Diphenhydramine | Site | Ki (nM) | Species | Ref |
      | --- | --- | --- | --- | --- |
      | 3800+ | Human |
      | 960–2400 | Human |
      | 1100–2200 | Human |
      | 5-HT2C | 780 | Human |
      | α1B | 1300 | Human |
      | α2A | 2900 | Human |
      | α2B | 1600 | Human |
      | α2C | 2100 | Human |
      | D2 | 20000 | Rat |
      | H1 | 9.6–16 | Human |
      | H2 | 100000+ | Canine |
      | H3 | 10000+ | Human |
      | H4 | 10000+ | Human |
      | M1 | 80–100 | Human |
      | M2 | 120–490 | Human |
      | M3 | 84–229 | Human |
      | M4 | 53–112 | Human |
      | M5 | 30–260 | Human |
      | 48000–86000 | Rat |
      | ) | Human |
      | Values are Ki (nM), unless otherwise noted. The smaller the value, the more strongly the drug binds to the site. |
      ...
      Diphenhydramine, while traditionally known as an antagonist, acts primarily as an inverse agonist of the histamine H1 receptor. It is a member of the ethanolamine class of antihistaminergic agents. By reversing the effects of histamine on the capillaries, it can reduce the intensity of allergic symptoms. It also crosses the blood–brain barrier and inversely agonizes the H1 receptors centrally. Its effects on central H1 receptors cause drowsiness.
      ...
      Diphenhydramine is a potent antimuscarinic(a competitive antagonist of muscarinic acetylcholine receptors) and, as such, at high doses can cause anticholinergic syndrome. The utility of diphenhydramine as an antiparkinson agent is the result of its blocking properties on the muscarinic acetylcholine receptors in the brain.
      ...
      | Overview of diphenhydramine targets and effects | Biological target | Mode of action | Effect |
      | --- | --- | --- | --- |
      | H1 receptor | Inverse agonist | Allergy reduction; Sedation |
      | mACh receptors | Antagonist | Anticholinergic; Antiparkinson |
      | Sodium channels | Blocker | Local anesthetic |

      ---

      Title: Diphenhydramine - StatPearls - NCBI Bookshelf
      URL: https://www.ncbi.nlm.nih.gov/books/NBK526010/
      Published: 2025-03-27T00:00:00.000Z
      Author: Maher AR, Theodore G.
      Highlights:
      Diphenhydramine primarily works by antagonizing the H1 (histamine-1) receptor, although it also has other mechanisms of action.[15] The H1 receptor is located on respiratory smooth muscles, vascular endothelial cells, cardiac tissue, the gastrointestinal tract (GIT), the uterus, immune cells, and the central nervous system (CNS) neurons. When the H1 receptor is stimulated in these tissues, it produces a wide variety of actions, including increased vascular permeability, promotion of vasodilation causing flushing, decreased atrioventricular (AV) node conduction time, stimulation of sensory nerves of airways producing coughing, smooth muscle contraction of bronchi and GIT, and eosinophilic chemotaxis promoting the allergic immune response. Diphenhydramine acts as an inverse agonist at the H1 receptor, reversing histamine's effects on capillaries and reducing allergic reaction symptoms. Since diphenhydramine is a first-generation antihistamine, it readily crosses the blood-brain barrier and inversely agonizes the H1 CNS receptors, resulting in drowsiness and suppressing the medullary cough center.[16] The H1 receptor is similar to muscarinic receptors. Therefore, diphenhydramine also acts as an antimuscarinic, a competitive antagonist of the muscarinic acetylcholine receptor, resulting in its use as an antiparkinson medication. Lastly, diphenhydramine acts as an intracellular sodium channel blocker, producing local anesthetic properties.

      ---

      Title: diphenhydramine | Ligand Activity Charts | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandActivityRangeVisForward?ligandId=1224
      Published: N/A
      Author: N/A
      Highlights:
      - H1 receptor/Histamine H1 receptor in Human [ChEMBL: CHEMBL231] [GtoPdb: 262] [UniProtKB: P35367]
      ...
      - Histamine H1 receptor in Guinea pig [ChEMBL
      ...
      CHEMBL3943] [UniProtKB: P31389]

      ---

      Title: diphenhydramine | Ligand page | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=1224
      Published: N/A
      Author: N/A
      Highlights:
      Comment: Diphenhydramine has anti-histamine action.
      ...
      | Canonical SMILES | CN(CCOC(c1ccccc1)c1ccccc1)C |
      | --- | --- |
      | Isomeric SMILES | CN(CCOC(c1ccccc1)c1ccccc1)C |
      | InChI | InChI=1S/C17H21NO/c1-18(2)13-14-19-17(15-9-5-3-6-10-15)16-11-7-4-8-12-16/h3-12,17H,13-14H2,1-2H3 |
      | InChI Key | ZZVUWRFHKOJYTH-UHFFFAOYSA-N |
      ...
      | Database Links |
      | --- |
      | Specialist databases |
      | GPCRdb Ligand | diphenhydramine |
      | Other databases |
      | BindingDB Ligand | 50017674 |
      | BitterDB Ligand | 61 |
      | CAS Registry No. | 58-73-1 |
      | ChEBI | CHEBI:4636 |
      | ChEMBL Ligand | CHEMBL657 |
      | DrugBank Ligand | DB01075 |
      | DrugCentral Ligand | 916 |
      | GtoPdb PubChem SID | 135650192 |
      | PubChem CID | 3100 |
      | RCSB PDB Ligand | 2PM |
      ...
      | Search Google
      ...
      -N |

      ---

      Title: Comparative anticholinergic activities of 10 histamine H1 receptor antagonists in two functional models - ScienceDirect
      URL: https://www.sciencedirect.com/science/article/abs/pii/S0014299904012622
      Published: N/A
      Author: N/A
      Highlights:
      Since their discovery and early development in the 1940s, histamine H1 receptor antagonists (antihistamines) have become one of the most widely used classes of medications for allergic disorders (Slater et al., 1999). Older “first-generation” antihistamines exhibit high binding affinity for H1 receptors, but many of these drugs exhibit binding affinity for other classes of cellular receptors such as the muscarinic cholinergic subtypes (M1−M5) (Kubo et al., 1987). Anticholinergic properties of antihistamines have long been recognized (Sherrod et al., 1947, Reuse, 1948), and some clinical effects of antihistamines, such as dry mouth, constipation, urinary retention and tachycardia, are attributed to the antimuscarinic actions of these drugs (Simons, 1999). Another characteristic feature of the older antihistamines is that they gain access to the brain and bind to cellular receptors in the central nervous system (CNS), causing sedation and impaired psychomotor performance (Hindmarch and Shamsi, 1999, Shamsi and Hindmarch, 2000).
      ...
      Newer “second-generation” antihistamines were developed as relatively more selective histamine H1 receptor antagonists than the first-generation agents, with an aim of minimizing centrally mediated effects, such as sedation. However, it would appear that some of the newer antihistamines are capable of binding to muscarinic receptors, as well as to histamine H1 receptors in the brain (Ter Laak et al., 1993).
      ...
      Numerous functional models have been used to characterize the anticholinergic properties of antihistamines. For example, Niemegeers et al. (1982b) evaluated the central anticholinergic activity of several pharmacological classes of drugs by antagonism of physostigmine-induced lethality in rats. Among the antihistamines tested in this model, diphenhydramine and cyproheptadine were active. The central anticholinergic activity of diphenhydramine was also noted by its ability to suppress cholinomimetic-induced jaw tremors in a rat model (Carlson et al., 2000). Cardelús et al. (1999) measured ocular mydriatic responses in guinea pigs, and contractions of rabbit isolated iris muscle, reflecting anticholinergic activity; desloratadine was active and fexofenadine was inactive at the concentrations tested.
      ...
      Eight of the antihistamines expressed anticholinergic activity of varying potencies, as evidenced by parallel rightward shifts of the concentration–response curves for carbachol. The rank order of potencies was: cyproheptadine>promethazine>desloratadine>diphenhydramine>loratadine>chlorpheniramine>hydroxyzine>pyrilamine (Table 2). The pA2 values ranged from 8.2±0.4 for cyproheptadine to 4.8±0.4 for pyrilamine. The relative anticholinergic potencies of the four reference antimuscarinic compounds

      ---

      Title: Diphenhydramine: Uses, Interactions, Mechanism of Action | DrugBank Online
      URL: https://web.archive.org/web/20240922051631/https:/go.drugbank.com/drugs/DB01075
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine - perhaps known most commonly as its brand name formulation Benadryl - is a first-generation H1 receptor antihistamine that is used extensively for the treatment of seasonal allergies, insect bites and stings, and rashes 9,10,11,17. However, it also has antiemetic, antitussive, hypnotic, and antiparkinson properties 11,16. As histamine receptors exist both peripherally and in the central nervous system, diphenhydramine has been shown to cause sedation due to its competitive antagonism of histamine H1 receptors within the
      ...
      nervous system 9,10,11,17,5. While its use in
      ...
      therapy can sometimes fall out of favor due to its sedative effect, diphenhydramine has been repurposed for use
      ...
      many non-prescription over-the-counter sleep aids and cough-and-
      ...
      medications that have been marketed for
      ...
      time" use 9,12,13.
      ...
      Diphenhydramine has anti-histaminic (H1-receptor), anti-emetic, anti-vertigo and sedative and hypnotic properties 12. The anti-histamine action occurs by blocking the spasmogenic and congestive effects of histamine by competing with histamine for H1 receptor sites on effector cells, preventing but not reversing responses mediated by histamine alone 12. Such receptor sites may be found in the gut, uterus, large blood vessels, bronchial muscles, and elsewhere 12. Anti-emetic action is by inhibition at the medullary chemoreceptor trigger zone 12. Anti-vertigo action is by a central antimuscarinic effect on the vestibular apparatus and the integrative vomiting center and medullary chemoreceptor trigger zone of the midbrain 12.
      ...
      Diphenhydramine predominantly works via the antagonism of H1 (Histamine 1) receptors 9,10,11,17,5. Such H1 receptors are located on respiratory smooth muscles, vascular endothelial cells, the gastrointestinal tract (GIT), cardiac tissue, immune cells, the uterus, and the central nervous system (CNS) neurons 9,10,11,17,5. When the H1 receptor is stimulated in these tissues it produces a variety of actions including increased vascular permeability, promotion of vasodilation causing flushing, decreased atrioventricular (AV) node conduction time, stimulation of sensory nerves of airways producing coughing, smooth muscle contraction of bronchi and the GIT, and eosinophilic chemotaxis that promotes the allergic immune response 9,10,11,17,5.
      ...
      Furthermore, H1 receptors are similar to muscarinic receptors 9,10,11,17,5. Consequently, diphenhydramine also acts as an antimuscarinic 9,10,11,17,5. It does so by behaving as a competitive antagonist of muscarinic acetylcholine receptors, resulting in its use as an antiparkinson medication 9,10,11,17,5.
      ...
      | Organism |
      ...
      | --- | --- |
      ...
      | AHistamine
      ...
      Histamine H1 receptor |
      ...
      2 | Humans |

      ---

      Title: Diphenhydramine · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/diphenhydramine/
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine (CHEMBL657) is an approved small-molecule H1-
      ...
      antagonist (ATC D04AA32) targeting HRH1; indicated
      ...
      63
      ...
      including allergic disease
      ...
      plasma cell myeloma.
      ...
      | Gene | Target | Action | pAffinity | Cancer dependency | UniProt |
      | --- | --- | --- | --- | --- | --- |
      | HRH1 | H1 receptor | Antagonist | 7.9 | P35367 |
      ...
      | Gene | p
      ...
      | Value | Activity
      ...
      | --- | --- | --- | --- | --- |
      ...
      | P3
      ...
      | IC5
      ...
      | 1 nM | CHEMBL_ACT_429899
      ...
      amine H1 receptor
      ...
      .93 |
      ...
      11.75 nM | CHEM
      ...
      7846167 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.83 | Ki | 14.79 nM | CHEMBL_ACT_7846197 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.7 | Ki | 20 nM | CHEMBL_ACT_7681414 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.5 | AC50 | 32 nM | CHEMBL_ACT_25212872 |
      ...
      | Muscarinic acetylcholine receptor M4 | P08173 | CHRM4 | 7.28 | Ki | 52 nM | CHEMBL_ACT_7681448 |
      ...
      | Muscarinic acetylcholine receptor M1 | P11229 | CHRM1 | 7.08 | Ki | 83 nM | CHEMBL_ACT_7681442 |
      ...
      12 |
      ...
      5 | 6.94 |
      ...
      | 116 nM | CHEM
      ...
      6.86 |
      ...
      137 nM | CHEM
      ...
      | Histamine H1 receptor | P35367 | HRH1 | 6.77 | IC50 | 171 nM | CHEMBL_ACT_7681413 |
      ...
      | Muscar
      ...
      M2 | P08172 | CHRM2 | 6.43 | Ki | 373 nM | CHEMBL_ACT_7681444 |

      ---

      Title: Antimuscarinic Effects of Antihistamines: Quantitative Evaluation by Receptor-Binding Assay
      URL: https://www.jstage.jst.go.jp/article/jphs1951/43/3/43_3_277/_article
      Published: 2006-09-15T00:00:00.000Z
      Author: N/A
      Highlights:
      Quantitative evaluation of antimuscarinic effects of antihistamines (H1and H2-receptor antagonists) was carried out using a receptor-binding assay. The inhibition constants (K1 values) of twenty seven H1-receptor antagonists, one related antidepressant and three H2-receptor antagonists at H1-receptors and muscarinic receptors in the bovine cerebral cortex were determined. All the H2receptor antagonists examined showed very low affinity for the muscarinic receptors. On the other hand, some H1-receptor antagonists (mequitazine, cyproheptazine, clemastine, diphenylpyraline, promethazine, homochlorcyclizine and alimemazine) had high affinity for the muscarinic receptors (K1=5.0-38 nM). Another group of H1 -receptor antagonists (mepyramine, terfenadine, metapyrilen, azelastine, hydroxyzine and meclizine) had low affinity for the muscarinic receptors (K1=3, 600-30, 000 nM). Thus, a broad range of antimuscarinic potencies among the antihistamines was demonstrated. These results should provide helpful information with regard to the clinical and experimental use of antihistamines.
```
/answer ade0dfb8-3887-4df0-8762-b807b7cb03ae allow
Control Request:
```yaml
id: c975140e-05ad-44e0-9e74-da83fe909bbc
toolName: web-search-exa
arguments:
  query: diphenhydramine plasma concentration therapeutic 50-100 ng/mL sedation dose oral 25mg 50mg peak plasma nM
  reason: Get therapeutic plasma concentration of DPH in molar units to compare against Na channel Kd
```
/answer c975140e-05ad-44e0-9e74-da83fe909bbc allow
Control Request:
```yaml
id: a05c8d4e-7735-40b0-b483-846423b52539
result:
  structuredContent:
    content: |-
      Title: Correlation between plasma diphenhydramine level and ...
      URL: https://pubmed.ncbi.nlm.nih.gov/24512/
      Published: N/A
      Author: N/A
      Highlights:
      Checking your browser - reCAPTCHA

      Checking your browser before accessing pubmed.ncbi.nlm.nih.gov ...

      Click here if you are not automatically redirected after 5 seconds.

      Checking your browser - reCAPTCHA
      Checking your browser before accessing pubmed.ncbi.nlm.nih.gov ...
      Click [here](#) if you are not automatically redirected after 5 seconds.

      ---

      Title: Pharmacokinetics and Pharmacodynamics of Diphenhydramine 25 mg in Young and Elderly Volunteers
      URL: https://accp1.onlinelibrary.wiley.com/doi/10.1002/j.1552-4604.1998.tb04466.x
      Published: N/A
      Author: Tempero KF
      Highlights:
      Thirty-seven young and elderly male and female volunteers 21 to 76 years of age received a single 25-mg oral dose of diphenhydramine or matching placebo in a double-blind, randomized, two-way crossover study. Plasma diphenhydramine concentrations, self-ratings of sedation, mood, and autonomic effects, performance on the digit-symbol substitution test (DSST), and heart rate were determined for 24 hours after administration. Information acquisition and recall were tested at 2.5 and 24 hours after administration. Age and gender did not significantly influence diphenhydramine peak plasma concentration, time of peak concentration, elimination half-life, area under the plasma concentration curve, or apparent oral clearance. Effects on psychomotor performance, sedation, mood, and memory did not differ between diphenhydramine and placebo in either group. Thus, the pharmacokinetics of single 25-mg oral doses of diphenhydramine are not influenced by age or gender. This dose of diphenhydramine produces essentially undetectable pharmacodynamic effects in both the young and elderly.
      ...
      * 9Carruthers SG,Shoeman DW,Hignite CE,Azarnoff DL:Correlation between plasma diphenhydramine level and sedative and antihistamine effects.*Clin Pharmacol Ther*1978;23:375–382.

      ---

      Title: Pharmacokinetics and pharmacodynamics of diphenhydramine 25 mg in young and elderly volunteers
      URL: https://pubmed.ncbi.nlm.nih.gov/9702844/
      Published: N/A
      Author: N/A
      Highlights:
      Thirty-seven young and elderly male and female volunteers 21 to 76 years of age received a single 25-mg oral dose of diphenhydramine or matching placebo in a double-blind, randomized, two-way crossover study. Plasma diphenhydramine concentrations, self-ratings of sedation, mood, and autonomic effects, performance on the digit-symbol substitution test (DSST), and heart rate were determined for 24 hours after administration. Information acquisition and recall were tested at 2.5 and 24 hours after administration. Age and gender did not significantly influence diphenhydramine peak plasma concentration, time of peak concentration, elimination half-life, area under the plasma concentration curve, or apparent oral clearance. Effects on psychomotor performance, sedation, mood, and memory did not differ between diphenhydramine and placebo in either group. Thus, the pharmacokinetics of single 25-mg oral doses of diphenhydramine are not influenced by age or gender. This dose of diphenhydramine produces essentially undetectable pharmacodynamic effects in both the young and elderly.
      ...
      - Adult
      - Age Factors
      - Aged
      - Cross-Over Studies
      - Diphenhydramine / pharmacokinetics*
      - Diphenhydramine / pharmacology
      - Double-Blind Method
      - Female
      - Heart Rate / drug effects
      - Histamine H1 Antagonists / pharmacokinetics*
      - Histamine H1 Antagonists / pharmacology
      - Humans
      - Hypnotics and Sedatives / pharmacokinetics*
      - Hypnotics and Sedatives / pharmacology
      - Male
      - Middle Aged
      - Sex Factors
      ...
      - Histamine H1 Antagonists
      - Hypnotics and Sedatives
      - Diphenhydramine

      ---

      Title: Diphenhydramine - StatPearls - NCBI Bookshelf - NIH
      URL: https://www.ncbi.nlm.nih.gov/books/NBK526010/
      Published: 2025-03-27T15:39:29.000Z
      Author: Maher AR, Theodore G.
      Highlights:
      Absorption: Diphenhydramine has an oral bioavailability of 72% (±8%), with peak plasma concentration (Cmax) occurring around 1.5 hours after administration.
      ...
      The injectable solution is provided at a concentration of 50 mg/mL. Oral dosage forms include tablets with strengths of 25 mg and 50 mg, as well as capsules available in 25 mg and 50 mg strengths. Chewable tablets are formulated with 12.5 mg of diphenhydramine, while dispersible tablets contain 25 mg. Liquid formulations consist of oral solutions containing 12.5 mg/5 mL and 50 mg/30 mL, with elixirs available at 12.5 mg/5 mL and syrups at 12.5 mg/5 mL. These different formulations offer flexible dosing options for both pediatric and adult populations. The topical formulation contains diphenhydramine hydrochloride at 2% and zinc acetate at 0.1%. The following are recommended dosages for allergy symptoms.
      ...
      25 to 50 mg every 4 to 6 hours as needed (PO/IM/IV)
      ...
      Max: 300 mg daily (PO); 100 mg/dose, up to 400 mg daily (IM/IV)
      ...
      25 to 50 mg every 2 to 4 hours as needed (PO/IM/IV)
      ...
      50 mg
      ...
      25 to 50 mg, every 4 to 6 hours as needed (PO/IM/IV)
      ...
      25 to 50 mg, every 4 to 6 hours as needed (PO/IM/IV); max 300 mg daily (PO);
      ...
      100 mg
      ...
      400 mg daily (IM/IV)
      ...
      25 to 50 mg, every 4 to 6 hours as needed (PO/IM/IV); max 300 mg daily (PO); 100 mg/dose up to 400 mg daily (IM/IV)

      ---

      Title: Diphenhydramine Pharmacology - Active Ingredient - RxReasoner
      URL: https://www.rxreasoner.com/substances/diphenhydramine/pharmacology
      Published: N/A
      Author: N/A
      Highlights:
      The sedative mechanism for diphenhydramine is thought to result from antagonism of central histamine and cholinergic receptors. The time course for sedation following a 50 mg oral dose was associated with higher plasma concentrations, and was significantly different from placebo during the first three hours following administration. The pharmacodynamics of sedation was correlated from placebo during the first three hours following administration. The pharmacodynamics of sedation was correlated with peak concentration of drug occurring during absorption and the alpha distribution phase.
      ...
      Diphenhydramine is well absorbed from the gastrointestinal tract, reaching peak plasma concentrations from 47-153 ng/ml between 1.5 hours and 4 hours after a single 50 mg dose in adults. After multiple oral doses of 50 mg diphenhydramine hydrochloride four times during each day to four subjects, minimum diphenhydramine plasma concentrations at steady state on the third day ranged from 57-150 ng/ml.
      ...
      Mean oral clearances for adults
      ...
      a 25 and 50 mg dose are 1041 and 1029 ml/min, respectively having coefficients of variation of 40% and 35%. Oral clearance is about 50% lower in elderly adults. Oral clearance is 691 ml/min (32%) for children ages 2 to 11 years, and is 1251 ml/min (43%) for adolescents' ages 12 to 17 years.

      ---

      Title: Pharmacokinetics of Diphenhydramine and a Demethylated Metabolite Following Intravenous And Oral Administration
      URL: https://accp1.onlinelibrary.wiley.com/doi/10.1002/j.1552-4604.1986.tb02946.x
      Published: N/A
      Author: Cirillo VJ
      Highlights:
      *Ten healthy volunteers received a single 50-mg dose of diphenhydramine (DP) hydrochloride intravenously and orally on two separate occasions. Kinetics of DP and a major demethylated metabolite (DMDP) were determined from multiple plasma samples drawn during a 24- to 48-hour period after dosage. Modification of a gas chromatographic (GC) technique allowed simultaneous quantitation of DP and DMDP. Mean kinetic variables for DP after intravenous (IV) dosage were: volume of distribution, 4.5 L/kg; elimination half-life, 8.4 hours; clearance, 6.2 mL/min/kg. After oral DP administration, a peak plasma level of 66 ng/mL was reached 2.3 hours after dosage. Systemic availability was 72%, nearly identical to the predicted estimate (71%) based on clearance of IV DP relative to hepatic blood flow. Appearance of the metabolite, DMDP, mirrored disappearance of DP; the area under the plasma concentration-time curve (AUC) for DMDP was highly correlated (*r =*.79*, P <*.05) with clearance of IV DP. However, metabolite AUC was significantly higher after oral as opposed to IV DP (218 vs 145 hr-ng/mL*, P <*.05). Because DP and DMDP elute nearly identically on standard GC systems, methodologic modifications are needed to resolve them. Coelution of the two compounds could bias kinetic data based on plasma concentration presumed to be specific for intact DP*.

      ---

      Title: Diphenhydramine: From Antihistamine to Anticholinergic — A Comprehensive Pharmacology Review | RxHero Blog
      URL: https://rxhero.pharmacologymentor.com/blog/diphenhydramine-pharmacology-review
      Published: N/A
      Author: N/A
      Highlights:
      | Parameter | Value |
      | --- | --- |
      | Absorption | Rapid oral absorption; peak plasma concentration in 0.5–1 h. |
      | Bioavailability | ~50 % due to first‑pass metabolism. |
      | Distribution | Extensive; volume of distribution ~2.5 L/kg; highly protein bound (~85 %). |
      | Metabolism | Hepatic N‑demethylation via CYP2D6 and CYP3A4 to active metabolite N‑desmethyl‑diphenhydramine. |
      | Elimination | Renal excretion of metabolites; half‑life 4–6 h (shorter in young adults, prolonged in the elderly). |
      | Clearance | ~0.2 L/min in healthy adults. |
      ...
      Pharmacodynamic (PD) data show a dose–response relationship with a therapeutic window of 25–50 mg for antihistaminic effects and 50–100 mg for sedation. The drug’s onset of action is dose‑dependent, with higher doses producing more pronounced CNS depression.
      ...
      - Allergic Rhinitis and Urticaria: 25–50 mg PO q6–8 h as needed. Effective in both acute and chronic allergic symptoms.
      - Insomnia: 25–50 mg PO at bedtime; not recommended for chronic use due to tolerance and daytime sedation.
      - Pre‑operative Sedation: 25–50 mg PO 1–2 h before surgery; often combined with local anesthetics.
      - Motion Sickness and Post‑operative Nausea: 25–50 mg PO q6–8 h; can be given orally or rectally.
      ...
      - Anticholinergic for Parkinsonian Tremor (off-label): 25–50 mg PO q6–8 h; limited evidence but used in refractory cases.
      - Viral Rhinovirus Symptom Relief (off-label): 25–50 mg PO q6–8 h; reduces nasal congestion and cough.
      ...
      - Pre‑operative Use: A single 25–50 mg dose 1–2 h before surgery reduces postoperative nausea and sedation without significant hemodynamic changes.
      ...
      - Half‑life is prolonged in the elderly; use 25 mg at bedtime only.
      - Contraindicated in narrow angle glaucoma.
      - In overdose, monitor for QT prolongation and treat with activated charcoal and benzodiazepines.
      - Drug interaction with CYP2D6 inhibitors can increase plasma concentration by up to 50 %.
      - Use in pregnancy is Category C; consider second‑generation antihistamines if needed.
      ...
      8. For pre‑operative sedation, a single 25–50 mg dose 1–2 h before surgery is effective.

      ---

      Title: Diphenhydramine: Pharmacokinetics and Pharmacodynamics in Elderly Adults, Young Adults, and Children
      URL: https://accp1.onlinelibrary.wiley.com/doi/10.1002/j.1552-4604.1990.tb01871.x
      Published: N/A
      Author: Douglas WW
      Highlights:
      The pharmacokinetics and pharmacodynamics of the H1-receptor antagonist diphenhydramine were studied in 21 fasting subjects divided into three age groups: elderly, (mean age 69.4 ±4.3 years), young adults, (mean age 31.5 ±10.4 years), and children, (mean age 8.9 ±1.7 years). All subjects ingested a single dose of diphenhydramine syrup 1.25 mg/kg, in mean doses of 86.0 ±7.3 mg, 87.9 ±12.4 mg, and 39.5 ±8.4 mg, respectively. Blood samples were collected hourly for 6 hours, every 2 hours until 12 hours, at 24 hours, and, in the adults, up to 72 hours after diphenhydramine administration. At these times, histamine skin tests were performed and wheal and flare areas were computed. The mean serum elimination half-life values for diphenhydramine differed significantly in elderly adults, young adults, and children, with values of 13.5 ±4.2 hours, 9.2 ±2.5 hours, and 5.4 ±1.8 hours being found respectively in each age group. Clearance rates for diphenhydramine also differed significantly with age, being 11.7 ±3.1 mL/min/kg in elderly adults, 23.3 ±9.4 mL/min/kg in young adults and 49.2 ±22.8 mL/min/kg in children. Diphenhydramine produced a maximum wheal suppression of 39.6 ±22.5% and a maximum flare suppression of 46.5 ±32.1% at 5 and 6 hours respectively in the elderly, a maximum wheal suppression of 45.5 ±25.0% and a maximum flare suppression of 53.4 ±16.9% at 6 and 4 hours respectively in young adults; and a maximum wheal suppression of 68.4 ±10.2% and a maximum flare suppression of 87.2 ±4.2% at 2 hours in children.
      ...
      * 7Carruthers SG,Shoeman DW,Hignite CE,Azarnoff DL:Correlation between plasma diphenhydramine level and sedative and antihistamine effects.*Clin Pharmacol Ther*1978;23:375–382.

      ---

      Title: BELARMIN Syrup Pharmacology - MPI, EU: SmPC - RxReasoner
      URL: https://www.rxreasoner.com/monographs/belarmin/pharmacology
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine is a potent antihistamine and antitussive with concurrent anticholinergic and sedative properties. Experiments have shown that the antitussive action is discrete from H1-receptor blockade and is located in the brain stem. The duration of activity of diphenhydramine is between 4 and 8 hours. The sedative mechanism for diphenhydramine is thought to result from antagonism of central histamine and cholinergic receptors. The time course for sedation following a 50 mg oral dose was associated with higher plasma concentrations, and was significantly different from placebo during the first three hours following administration. The pharmacodynamics of sedation was correlated from placebo during the first three hours following administration. The pharmacodynamics of sedation was correlated with peak concentration of drug occurring during absorption and the alpha distribution phase.
      ...
      Diphenhydramine is well absorbed from the gastrointestinal tract, reaching peak plasma concentrations from 47-153 ng/ml between 1.5 hours and 4 hours after a single 50 mg dose in adults. After multiple oral doses of 50 mg diphenhydramine hydrochloride four times during each day to four subjects, minimum diphenhydramine plasma concentrations at steady state on the third day ranged from 57-150 ng/ml.
      ...
      ml/min,
      ...
      40%
      ...
      % lower in elderly adults.
      ...
      %) for children ages 2 to
      ...
      17 years

      ---

      Title: Diphenhydramine Facts
      URL: https://data.ntsb.gov/Docket/Document/docBLOB?FileExtension=.PDF&FileName=Diphenhydramine+Facts-Master.PDF&ID=40388037
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine Diphenhydramine is a white, crystalline powder. Available primarily in tablet, capsule and liquid form. Synonyms: 2-(diphenylmethoxy)-N,N-dimethylethylamine hydrochloride; diphenhydramine hydrochloride; Benadryl®, Unisom® Sleepgels, Dytuss®, Dramamine®. Source: Available in capsules, tablets, chewable tablets, syrups, elixirs, topical, and injectable forms in a variety of prescription and over-the counter medications. Products contain diphenhydramine alone or in combination with other drugs such as pseudoephedrine and acetaminophen. Diphenhydramine is also an ingredient in several Tylenol® (i.e., acetaminophen) preparations. Dimenhydrinate (Dramamine®) is a combination of diphenhydramine and 8chlorotheophylline in equal molecular proportions. Drug Class: Antihistamine, antiemetic, sleep aid, sedative, CNS depressant. Medical and Recreational Uses: Used as an antihistamine for the temporary relief of seasonal and perennial allergy symptoms. Diphenhydramine is also used as a sleep aid and a cough suppressant, and has been used as a centrally acting antitussive although the mechanism for this action is unclear. Dramamine is used as a prophylaxis against and for the treatment of motion sickness. Potency, Purity and Dose: As an antihistamine, recommended doses for adults is 25-50 mg diphenhydramine every 6-8 hours, not to exceed 50-100 mg every 4-6 hours. For children, 12.5-25 mg three or four times daily is recommended. As a sleep aid the dose is 50 mg at bedtime. Adults can be given 10-50 mg intravenously or intramuscularly, up to a maximum daily dose of 400 mg. Route of Administration: Oral, injected, and topical applications. Pharmacodynamics: Diphenhydramine is a first generation antihistamine and is a H 1 receptor antagonist. Antagonism is achieved through blocking the effect of histamine more than blocking its production or release. Diphenhydramine inhibits most responses of smooth muscle to histamine and the vasoconstrictor effects of histamine. The antagonism may also produce anticholinergic effects, antiemetic effects, and significant sedative side effects. Pharmacokinetics: Following oral administration diphenhydramine is well absorbed from the gastrointestinal tract, is widely distributed throughout
      ...
      Drugs and Human Performance FACT SHEETS - Diphenhydramine Page 1 of 4 http://www.nhtsa.gov/people/injury/research/job185drugs/diphenhydramine.htm 2/27/2013 the body, and is able to pass though the blood-brain barrier. The oral availability is 61%, and 78% is bound in plasma. Peak plasma concentrations are reached in 2-3 hours. Diphenhydramine is metabolized to nordiphenhydramine (active metabolite), dinordiphenhydramine, and diphenylmethoxyacetic acid. The plasma half-life is 8.5±3.2 hours; shorter and longer half-lives have been reported for children and elderly subjects, respectively. Urinary excretion of unchanged diphenhydramine is 1.9%. Molecular Interactions / Receptor Chemistry: Diphenhydramine is metabolized via cytochrome P450 2D6 isoenzyme. Potential inhibitors of P450 2D6 could decrease the rate of drug elimination if administered concurrently, while potential inducers could increase the rate of drug elimination. Blood to Plasma Concentration Ratio: 0.77 and 0.82 reported. Interpretation of Blood Concentrations: Following a single oral dose of 50 mg, average peak plasma concentrations of 83 ng/mL diphenhydramine were detected at 3 hours, declining to 9 ng/mL by 24 hours. A single oral 100 mg dose resulted in average peak plasma concentrations of 112 ng/mL at 2 hours post dose. Effective antihistamine concentrations are greater than 25 ng/mL, drowsiness can be observed at 30-40 ng/mL, and mental impairment may be observed with concentrations above 60 ng/mL. Interpretation of Urine Test Results: Less than 2% of an oral dose is excreted in the 24 hour urine as unchanged parent drug, while approximately 11% is eliminated as its glucuronide conjugate. Effects: First generation H 1 antagonists can both stimulate and depress the CNS. Stimulation results in restlessness, nervousness and inability to sleep, while depressive effects include diminished alertness, slowed reaction time and somnolence. Diphenhydramine is particularly prone to cause marked sedation. Drowsiness, reduced wakefulness, altered mood, impaired cognitive and psychomotor performance may also be observed. Side Effect Profile: Includes agitation, anticholinergic side effects such as dry mouth, confusion, dizziness, drowsiness, fatigue, disturbed coordination, irritability, paresthesia, blurred vision, and depression. In overdose, symptoms may include excitement, ataxia, tremor, sinus tachycardia, fever, hallucination, athetosis, convulsions or seizures, hypotension, deep coma, cardiorespiratory collapse, and death. Fixed and dilated pupils are also observed. Gastrointestinal symptoms are less with diphenhydramine than with other H 1 antagonists. Duration of Effects: Dose-dependent, however, following oral administration of therapeutic doses, peak plasma concentrations are reached in 2-3 hours and effects usually last 4-6 hours. Tolerance, Dependence and Withdrawal Effects: Some tolerance may develop to the sedative effects of diphenhydramine with repeated oral dosing. No reported dependence or withdrawal effects with doses recommended. Drug Interactions: Effects of diphenhydramine are increased by the presence of alcohol, MAOI’s, diazepam, hypnotics, sedatives, tranquilizers, and other CNS depressants. Alcohol enhances such effects as drowsiness, sedation and decreased motor skills. These decrements in effect are more pronounced in the elderly. MAOI’s prolong and intensify the anticholinergic effects of diphenhydramine.
      ...
      diazepam and
      ...
      performance decrements
      ...
      severely impair tracking
      ...
      doses of dip
      ...
      33(4
      ...
      comparisons, Saint Louis, MO; 1
      ...
      96.
```
/answer a05c8d4e-7735-40b0-b483-846423b52539 allow
ReasoningToken: 2926
# Potenz- und Selektivitätsprüfung: DPH als „Salven-Limiter“

## 1. Belastbare Zahlen aus der Literatur (Ki/Kd, human wo verfügbar)

| Target | Ki/Kd (DPH) | Quelle/Bereich |
|---|---|---|
| **H1-Rezeptor** | **9,6–20 nM** (Median ~14 nM) | mehrfach bestätigt (radioligand binding, human) |
| **Muskarin M1–M5** | **80–260 nM** (Ø ~150 nM) | konsistent über mehrere Quellen |
| **α1-adrenerg** | ~430 nM | – |
| **Naᵥ, Ruhezustand** | **~48.000–86.000 nM** (48–86 µM, Ratte) | Standard-Bindungsassay |
| **Naᵥ, inaktivierter Zustand** | **~10.000 nM** (10 µM) | Kuo 2000, Kim 2000 – Ihre Quelle |

→ **Selektivitäts-Rangfolge nach Affinität: H1 ≫ Muskarin ≫≫ Naᵥ(inaktiviert) > Naᵥ(Ruhe)**

Faktor H1 : Naᵥ(inaktiviert) ≈ **1 : 700**
Faktor Muskarin : Naᵥ(inaktiviert) ≈ **1 : 65**

DPH ist also **kein** Membranstabilisator „mit H1-Nebenwirkung“, sondern pharmakologisch das Gegenteil: ein **hochpotenter H1-Blocker und mäßig potenter Anticholinergikum mit einer sehr schwachen, erst bei hoher Exposition relevanten Na⁺-Kanal-Komponente**.

## 2. Realitätscheck: Erreichbare freie Plasmakonzentrationen vs. benötigte Kd

Klinische Dosis 50 mg p.o. → Peak-Gesamtplasma ~47–153 ng/mL (Ø ~83 ng/mL), Proteinbindung ~78% → **freie Konzentration ~70 nM**.

**Rezeptorbesetzung bei Standarddosis (frei ~70 nM):**

| Target | Besetzung bei 70 nM frei |
|---|---|
| H1 | **~83%** (praktisch gesättigt) |
| Muskarin (Ø Ki 150 nM) | **~32%** (klinisch relevant – anticholinerge Effekte!) |
| Naᵥ inaktiviert (Ki 10 µM) | **~0,7%** |
| Naᵥ Ruhe (Ki ~65 µM) | **~0,1%** |

**Um nur 50% Besetzung des inaktivierten Na⁺-Kanals zu erreichen**, wäre eine freie Konzentration von ~10 µM nötig → bei 22% freier Fraktion entspricht das ~45 µM Gesamtplasma ≈ **~11.500 ng/mL** – das ist **~140-fach höher** als die Standard-50-mg-Dosis erzeugt, und liegt bereits im Bereich, der in Fallberichten mit **Krampfanfällen, QRS-Verbreiterung, Na⁺-Kanal-vermittelter Kardiotoxizität und Herzstillstand** assoziiert ist (vgl. das gefundene Cureus-Fallbeispiel zur DPH-Intoxikation, das explizit Natriumbicarbonat als Antidot gegen die Na⁺-Kanal-Blockade nennt).

## 3. Konsequenz für „Use-Dependence“

Der use-dependente Mechanismus (Kuo/Kim) ändert an dieser Rechnung nichts Grundsätzliches: Use-Dependence beschreibt die **kinetische Freilegung** des hochaffinen inaktivierten Zustands bei repetitiver Depolarisation – sie senkt aber nicht die **Gleichgewichts-Kd** selbst. Bei einer freien Konzentration von 70 nM bleibt die maximal erreichbare Kanalbesetzung im inaktivierten Zustand (selbst bei optimaler Salven-Frequenz) im Bereich von ~1%, weil das Massenwirkungsgesetz (Kd = 10 µM) die Obergrenze vorgibt. Use-Dependence „verstärkt" also nur einen ohnehin vernachlässigbaren Effekt.

## 4. Fazit zur Zieldefinition „Dosisreduktion bei Erhalt der Salven-Limitierung"

**Das Ziel ist mit DPH pharmakologisch nicht erreichbar – die Selektivität läuft in die falsche Richtung:**

- Eine Dosisreduktion würde zuerst die (unerwünschten) H1- und muskarinergen Effekte reduzieren – **das ist trivial und immer der Fall**, weil diese bei jeder klinisch gebräuchlichen Dosis bereits nahe der Sättigung liegen.
- Der gewünschte Na⁺-Kanal-Effekt (Salven-Limitierung) tritt aber **erst bei Konzentrationen ~2–3 Größenordnungen oberhalb der Standarddosis** auf – also in einem Bereich, der mit Sedierung, Anticholinergika-Syndrom, Delir, QT/QRS-Veränderungen und Krampfrisiko einhergeht.
- Es gibt **keinen Dosisbereich**, in dem die Na⁺-Kanal-Komponente wirksam, die H1/muskarinerge Komponente aber schon „ausgedünnt" ist. Die Wirkfenster liegen nicht getrennt, sondern die unerwünschten Effekte sättigen **weit unterhalb** des gewünschten Effekts.

## 5. Empfehlung

1. **DPH ist als „selektiver Membranstabilisator" ungeeignet** – das Konstrukt „DPH-positiv = Na-Kanal-Effekt ohne Antihistaminika-Last" ist pharmakokinetisch/-dynamisch nicht haltbar.
2. Wenn die Biophysik (use-dependenter, inaktivierungsselektiver Block der NTS/LC-Salve) das eigentliche Wirkprinzip sein soll, sollte auf eine Substanz **aus derselben Diphenyl-Pharmakophor-Familie mit saubererer Trennung** ausgewichen werden:
   - **Phenytoin**: Naᵥ-Ki im ähnlichen µM-Bereich, aber **keine relevante H1/M-Affinität** (Ki jeweils >>10 µM) → deutlich höherer Selektivitätsindex für den gewünschten Effekt.
   - Alternativ Mexiletin/Lidocain-Analoga (reine Klasse-Ib-Wirkung ohne Rezeptor-Kollateralschaden).
3. Falls DPH aus anderen Gründen (z. B. Verfügbarkeit, Kombinationseffekt mit H1/M-Blockade erwünscht) beibehalten werden soll: **keine Dosisreduktion**, sondern Akzeptanz, dass die Salvenlimitierung bei DPH ohnehin nur ein **Nebeneffekt der antihistaminerg/anticholinerg wirksamen Dosis** ist, nicht ein separat titrierbarer Mechanismus – ein Therapieversuch „hoch genug für Naᵥ, aber schonend" widerspricht der pharmakologischen Datenlage.

**Kurz:** Potenz-Ranking = H1 (nM) > Muskarin (100 nM) ≫ Naᵥ (µM–zweistellig-µM). Der gewünschte Salven-Effekt sitzt im am wenigsten potenten, am wenigsten selektiven Teil des Wirkprofils – eine Dosisreduktion killt exakt den Zieleffekt zuerst, nicht die Nebenwirkungen.
Das kann nicht stimmen. In Experimenten konnten wir einen signifikanten Effekt bereits bei 12,5 mg nachweisen. Der Muskarin-Antogonismus und H1(Doxepin) konnten abgegrenzt werden. Es verbeleiben nur a1 Kalzium und NDMA.
SystemInit:  id=67218be4-c64d-4874-9a1a-83ded32ffa70, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
Control Request:
```yaml
id: 623722d8-14b3-42d2-9b21-a7231e6e1178
toolName: web-search-exa
arguments:
  query: diphenhydramine NMDA receptor affinity Ki antagonist
  reason: Get Ki for DPH at NMDA receptor to compare with plasma levels at 12.5mg
```
/answer 623722d8-14b3-42d2-9b21-a7231e6e1178 deny Korrektur ich meine a2 nicht a1.
Control Request:
```yaml
id: 8ff4a5f8-6781-405b-8c0e-67fa15291761
toolName: web-search-exa
arguments:
  query: diphenhydramine L-type calcium channel block Ki potency alpha1 adrenergic affinity
  reason: Get Ki for DPH at calcium channels and alpha1 receptor
```
/answer 8ff4a5f8-6781-405b-8c0e-67fa15291761 allow
Control Request:
```yaml
id: a250b4b7-5ff5-4524-92d2-7c512e685458
result:
  structuredContent:
    content: |-
      Title: molecular determinants of selective binding to the inactivated channels
      URL: https://pubmed.ncbi.nlm.nih.gov/10617688/
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine is an H1 histamine receptor antagonist, yet it also has a clinically useful local anesthetic effect. We found that diphenhydramine inhibits the neuronal Na(+) current, and the inhibition is stronger with more positive holding potentials. The dissociation constant between diphenhydramine and the inactivated Na(+) channel is approximately 10 microM, whereas the dissociation constant between diphenhydramine and the resting channel is more than 300 microM. The local anesthetic effect of diphenhydramine thus is ascribable to inhibition of Na(+) current by selective binding of the drug to the inactivated channels. Most interestingly, many other compounds, such as the anti-inflammatory drug diclofenac, the anticonvulsant drug phenytoin, the antidepressant drug imipramine, and the anticholinergic drug benztropine, have similar effects on neuronal Na(+) current. There is no apparent common motif in the chemical structure of these compounds, except that they all contain two phenyl groups. Molecular modeling further shows that the two benzene rings in all these drugs have very similar spatial orientations (stem bond angle, approximately 110 degrees; center-center distance, approximately 5 A). In contrast, the two phenyl groups in phenylbutazone, a drug that has only a slight effect on Na(+) current, are oriented in quite a different way. These findings strongly suggest that the two phenyl groups are the key ligands interacting with the channel. Because the binding counterpart of a benzene ring usually is also a benzene ring, some aromatic side chain groups of the Na(+) channel presumably are realigned during the gating process to make the very different affinity to the aforementioned drugs between the inactivated and the resting channels.

      ---

      Title: Diphenhydramine: Uses, Interactions, Mechanism of Action | DrugBank Online
      URL: https://web.archive.org/web/20240922051631/https:/go.drugbank.com/drugs/DB01075
      Published: N/A
      Author: N/A
      Highlights:
      implicated in a
      ...
      mitter systems that
      ...
      behaviour including dopamine,
      ...
      , acetylcholine, and opioid 3. As a result, diphenhydramine is
      ...
      anxiolytic and
      ...
      12.
      ...
      Diphenhydramine predominantly works via the antagonism of H1 (Histamine 1) receptors 9,10,11,17,5. Such H1 receptors are located on respiratory smooth muscles, vascular endothelial cells, the gastro
      ...
      tract (GIT), cardiac tissue, immune cells, the uterus, and the central nervous system (CNS) neurons 9,10,11,17,5. When the H1 receptor is stimulated in these tissues it produces a variety of actions including increased
      ...
      permeability, promotion of vasodilation causing flushing, decreased atrioventricular (AV) node conduction time, stimulation of sensory nerves of airways producing coughing, smooth muscle contraction of bronchi and
      ...
      GIT, and eosinophilic chemotaxis that promotes
      ...
      allergic immune response 9,10,11,17,5.
      ...
      Lastly, diphenhydramine has also demonstrated activity as an intracellular sodium channel blocker, resulting in possible local anesthetic properties 9.

      ---

      Title: Diphenhydramine · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/diphenhydramine/
      Published: N/A
      Author: N/A
      Highlights:
      | Protein | UniProt | Gene | pChembl | Type | Value | Activity ID |
      | --- | --- | --- | --- | --- | --- | --- |
      ...
      | Histamine H1 receptor (domestic
      ...
      ) | P31389 | 9 | IC50 | 1 nM | CHEMBL_ACT_429899 |
      ...
      | Histamine H1 receptor (domestic guinea pig) | P31389 | 7.93 | Kd |
      ...
      11.75 nM | CHEMBL_ACT_7846167 |
      ...
      | Histamine H1 receptor | P35367 | HRH1 | 7.83 | Ki | 14.79 nM | CHEMBL_ACT_7846197 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.7 | Ki | 20 nM | CHEMBL_ACT_7681414 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.5 | AC50 | 32 nM | CHEMBL_ACT_25212872 |
      ...
      | Muscarinic acetylcholine receptor M1 | P11229 | CHRM1 | 7.08 | Ki | 83 nM | CHEMBL_ACT_7681442 |
      ...
      | Sodium channel protein type 1 subunit alpha | P35498 | SCN1A | 5.22 | IC50 | 6000 nM | CHEMBL_ACT_346933 |
      ...
      | Alpha-1A adrenergic receptor | P35348 | ADRA1A | 5.2 | AC50 | 6312 nM | CHEMBL_ACT_25138129 |
      ...
      | Alpha-2B adrenergic receptor | P18089 | ADRA2B | 5.16 | AC50 | 7000 nM | CHEMBL_ACT_25144052 |
      ...
      | Alpha-2A adrenergic receptor | P08913 | ADRA2A | 5.02 | AC50 | 9548 nM | CHEMBL_ACT_2
      ...
      156804 |

      ---

      Title: diphenhydramine | Ligand page | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=1224
      Published: N/A
      Author: N/A
      Highlights:
      #### diphen
      ...
      Comment: Diphenhydramine has anti-histamine action.
      ...
      | --- | ---

      ---

      Title: MOLECULAR DETERMINANTS OF DRUG BINDING AND ACTION ON L-TYPE CALCIUM CHANNELS | Annual Reviews
      URL: https://www.annualreviews.org/content/journals/10.1146/annurev.pharmtox.37.1.361
      Published: 1997-04-01T00:00:00.000Z
      Author: Gregory H. Hockerman|Blaise Z. Peterson|Barry D. Johnson, and|William A. Catterall
      Highlights:
      The crucial role of L-type Ca2+ channels in the initiation of cardiac and smooth muscle contraction has made them major therapeutic targets for the treatment of cardiovascular disease. L-type channels share a common pharmacological profile, including high-affinity voltage- and frequency-dependent block by the phenylalkylamines, the benz(othi)azepines, and the dihydropyridines. These drugs are thought to bind to three separate receptor sites on L-type Ca2+ channels that are allosterically linked. Results from different experimental approaches implicate the IIIS5, IIIS6, and IVS6 transmembrane segments of the α1 subunits of L-type Ca2+ channels in binding of all three classes of drugs. Site-directed mutagenesis has identified single amino acid residues within the IIIS5, IIIS6, and IVS6 transmembrane segments that are required for high-affinity binding of phenylalkylamines and/or dihydropyridines, providing further support for identification of these transmembrane segments as critical elements of the receptor sites for these two classes of drugs. The close proximity of the receptor sites for phenylalkylamines, benz(othi)azepines, and dihydropyridines raises the possibility that individual amino acid residues may be required for high-affinity binding of more than one of these ligands. Therefore, we suggest that phenylalkylamines and dihydropyridines bind to different faces of the IIIS6 and IVS6 transmembrane segments and, in some cases, bind to opposite sides of the side chains of the same amino acid residues. The results support the domain interface model for binding and channel modulation by these three classes of drugs.

      ---

      Title: Development of phenotypic assays for identifying novel blockers of L-type calcium channels in neurons | Scientific Reports
      URL: https://preview-www.nature.com/articles/s41598-020-80692-5
      Published: 2021-01-11T00:00:00.000Z
      Author: N/A
      Highlights:
      (83
      ...
      successfully identified in
      ...
      hits from the
      ...
      with highest potencies. At least six of
      ...
      10 non
      ...
      DHPs in
      ...
      top 20 hits, cyproheptadine
      ...
      31(IC50 =
      ...
      138 nM from the screen), GBR 12909
      ...
      32(680
      ...
      ), lidoflazine 33(710
      ...
      ), fluspirilene 34(760 nM), fendiline 35(820 nM), and clomipramine 36(1010 nM), have been reported in
      ...
      literature to potently block
      ...
      CCs. In
      ...
      top 10 confirmed hits listed in Table 1, eight are DHPs and two (niclosamide and cyproheptadine) are non-DHPs. To our knowledge, niclosamide (an anthelmintic; 80 nM) is the only compound in Table 1 for which no published information is
      ...
      . Using a separately
      ...
      patch clamp assay
      ...
      activity of nic
      ...
      amide in rat cortical neurons (
      ...
      ). In conclusion, the
      ...
      and validated by its ability to identify
      ...
      CC blockers as well as a novel
      ...
      in the PW library.
      ...
      Using the patch clamp assay validated above, we tested niclosamide and cyproheptadine, the two non-DHPs hits in Table 1. In rat cortical neurons, 3 µM cyproheptadine blocked 75.2 ± 9.1% (n = 4) of the LTCC currents, in line with its binding affinities to the DHP, phenylalkylamine and benzothiazepine sites (Table 1). In contrast, while niclosamide potently blocked neuronal LTCC currents (IC50 = 183.1 ± 28.2 nM, n = 6; Fig. 6 a,c), it showed no binding at any of these sites in rat cortical preparations (Ki > 30 µM for all three sites; n = 4; also see Table 1), suggesting that niclosamide binds to a novel site in the LTCC channel complex in neurons. Similar to control, the I-V curve in the presence of niclosamide (200 nM) peaked near − 20 mV, although niclosamide block was more pronounced at depolarized potentials (Fig. 6 d). The activation and inactivation kinetics in the presence of niclosamide were not significantly different from control. The 20–80% rise time (at − 20 mV) was 17.4 ± 2.9 ms (n = 5) and 16.1 ± 3.5 ms (n = 4) in the absence and presence of 200 nM niclosamide, respectively (p > 0.7). The current remaining after 400 ms of depolarization to − 20 mV was 41.9 ± 7.5% (n = 4) of the peak in niclosamide vs 49.1 ± 3.4% (n = 5) in control (p > 0.3). Both compounds also blocked CaV1.2 currents in CHO cells (IC50 = 715.3 ± 49.2 nM for niclosamide, n = 7, Fig. 6 b,c; 52.3 ± 6.1% inhibition at 3 µM for cyproheptadine, n = 3). Niclosamide blocked CaV1.2 expressed in CHO cells with lower potency (by ~ fourfold) and efficacy (76.1%) than for neuronal LTCCs (full efficacy). Surprisingly, niclosamide block of Cav1.2 (100 nM) was more pronounced in experiments in which niclosamide was applied for significantly longer durations (average of ~ 6.5 min) than those used for CaV1.2 concentration–response experiments (average ~ 3.5 min) (Fig. 6 c). Though not corrected for current rundown, this extra block was not due to compound-independent current rundown, which was only 8.4 ± 3.7% and 12.4 ± 7.6%, respectively, after 3.5 and 6.5 min in compound-free buffer (n = 4).
      ...
      Using cortical neurons prepared the same way as for the calcium flux assay, we developed and validated a manual patch clamp assay for hit confirmation. The patch clamp assay confirmed both non-DHPs in the top 10 primary hits, niclosamide and cyproheptadine. Of particular interest, niclosamide has not been noted in the literature for its actions at LTCCs. Combining patch clamp with binding studies, we showed that niclosamide bound to a novel site in neuronal LTCCs with at least two orders of magnitude higher affinity than that at the DHP, phenylalkylamine and benzothiazepine sites. Future studies will be necessary to characterize the novel binding site and molecular mechanism of niclosamide.
      ...
      For binding experiments, results were expressed (1) as percent of control specific binding: 100 × (measured specific binding/control specific binding) or (2) as percent inhibition of control specific binding in the presence of the test compounds:100–100 × (measured specific binding/control specific binding). The IC50 values (the concentration that causes half-maximal inhibition of control specific binding) were determined by non-linear regression analysis of the competition curves using Hill equation: Y = D + (A−D)/[1 + (C/IC50)]nH, where Y = specific binding, A = left asymptote of the curve, D = right asymptote of the curve, C = compound concentration, and nH = slope factor. Analyses were performed using software developed at Eurofins (Hill software) and validated by comparison with data generated by the commercial software SigmaPlot 4.0. The inhibition constants (Ki) were calculated using the Cheng Prusoff equation Ki = IC50 × (1 + L/KD), where L = concentration of radioligand in the assay and KD = affinity of the radioligand for the receptor. KD values were determined from Scatchard plots.

      ---

      Title: DIPHENHYDRAMINE
      URL: https://drugs.ncats.io/drug/diphenhydramine
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine is an antihistamine which is used in the combination with naproxen sodium for the relief of occasional sleeplessness when associated with minor aches and pains. Diphenhydramine has a role nighttime sleep-aid and naproxen sodium is a pain reliever. In addition, diphenhydramine used in relieving symptoms in patients with moderate-to-severe seasonal allergic rhinitis. Diphenhydramine acts as an antagonist of histamine H1 receptor. Besides, was shown potential to repurpose diphenhydramine as an anti-melanoma therapeutic agent, it induces melanoma cell apoptosis by suppressing STAT3/MCL-1 survival signaling pathway.
      ...
      | Primary Target | Pharmacology | Condition | Potency |
      | --- | --- | --- | --- |
      | 7.9 null [pKi] |
      | 2.7 µM [IC50] |
      ...
      IC50
      ...
      uM] |
      ...
      | --- | --- | --- | ---
      ...
      IC50
      ...
      | yes [IC50 3.
      ...
      uM] |
      ...
      | yes [IC50 695 uM] |
      | yes [Ki 266.5 uM] |
      | yes [Ki
      ...
      uM] |

      ---

      Title: The action of calcium channel blockers on recombinant L-type calcium channel alpha1-subunits. | DrugBank
      URL: https://go.drugbank.com/articles/A13991
      Published: N/A
      Author: N/A
      Highlights:
      1. CHO cells expressing the alpha(1C-a) subunit (cardiac isoform) and the alpha(1C-b) subunit (vascular isoform) of the voltage-dependent L-type Ca2+ channel were used to investigate whether tissue selectivity of Ca2+ channel blockers could be related to different affinities for alpha1C isoforms. 2. Inward current evoked by the transfected alpha1 subunit was recorded by the patch-clamp technique in the whole-cell configuration. 3. Neutral dihydropyridines (nifedipine, nisoldipine, (+)-PN200-110) were more potent inhibitors of alpha(1C-)b-subunit than of alpha(1C-a)-subunit. This difference was more marked at a holding potential of -100 mV than at -50 mV. SDZ 207-180 (an ionized dihydropyridine) exhibited the same potency on the two isoforms. 4. Pinaverium (ionized non-dihydropyridine derivative) was 2 and 4 fold more potent on alpha(1C-a) than on alpha(1C-b) subunit at Vh of -100 mV and -50 mV, respectively. Effects of verapamil were identical on the two isoforms at both voltages. 5. [3H]-(+)-PN 200-110 binding experiments showed that neutral dihydropyridines had a higher affinity for the alpha(1C-b) than for the alpha(1C-a) subunit. SDZ 207-180 had the same affinity for the two isoforms and pinaverium had a higher affinity for the alpha(1C-a) subunit than for the alpha(1C-b) subunit. 6. These results indicate marked differences among Ca2+ channel blockers in their selectivity for the alpha(1C-a) and alpha(1C-b) subunits of the Ca2+ channel.
      ...
      | Drug | Target | Kind | Organism | Pharmacological Action | Actions |
      | --- | --- | --- | --- | --- | --- |
      | Nifedipine | Voltage-dependent L-type calcium channel subunit alpha-1C | Protein | Humans | Details |
      | Nilvadipine | Voltage-dependent L-type calcium channel subunit alpha-1C | Protein | Humans | Details |
      | Nisoldipine | Voltage-dependent L-type calcium channel subunit alpha-1C | Protein | Humans | Details |
      | Verapamil | Voltage-dependent L-type calcium channel subunit alpha-1C | Protein | Humans | Details |

      ---

      Title: Pharmacology of L-type Calcium Channels: Novel Drugs for Old Targets?
      URL: https://doi.org/10.2174/1874467208666150507105845
      Published: 2015-09-17T00:00:00.000Z
      Author: Jörg Striessnig, Nadine J. Ortner, Alexandra Pinggera
      Highlights:
      Three main chemical classes of organic Ca 2+ channel drugs can be distinguished: Dihydropyridines (prototype nifedipine), phenylalkylamines (prototype verapamil) and benzothiazepines (prototype (+)-cis-diltiazem). Despite their different structure they all bind within a single overlapping drug binding region close to the pore and to the proposed activation gate of the channel's 1-subunit [15] [16] [17] . They reversibly interact with this binding domain in a stereoselective manner and, in isolated membranes at zero membrane potential, with dissociation constants in the nanomolar range (0.1 -50 nM; [16] ). By binding to this site they interfere with the normal voltage-dependent cycling of the channel through its resting, open and inactivated states (modulated receptor model; [18, 19] ). The uncharged DHPs primarily stabilize and induce inactivated channel states. They possess much higher affinity for the inactivated channel conformation and therefore their IC 50 for block of cardiovascular LTCCs is much lower at more depolarized voltages ("voltagedependent block" [10, [18] [19] [20] , Fig. 1b ). Phenylalkylamines and benzothiazepines bind to open and inactivated states with high affinity. At physiological pH they primarily exist as positively charged organic cations and can access their binding site from the cytoplasmic side during channel opening [21, 22] . They stabilize inactivated channel states, thereby slowing recovery from inactivation. This results in a pronounced frequency-or use-dependent inhibition [22, 23] . Based on these state-dependent binding characteristics CCBs should be considered gating modifiers. Interference of verapamil and diltiazem with LTCC gating always reduces inward Ca 2+ currents through LTCCs. This is in contrast to DHPs: clinically used DHPs (such as amlodipine, felodipine or isradipine) are always inhibitory; however, (-)-BayK8644 and (+)-SDZ202-791 are examples for gating modifiers that cause changes in Ca 2+ current kinetics (increase in current amplitudes, tail currents and single channel open probability) that enhance Ca 2+ influx during typical electrical activity patterns [20] .
      ...
      The state-dependent modulation by CCBs also provides these drugs with tissue-selectivity: inactivated channel states are favored in arterial smooth muscle due to their more depolarized resting membrane potential and long lasting depolarizations [18, 24] . The preferential affinity of DHPs for inactivated LTCCs can therefore explain their potent vasodilating effect without affecting cardiac inotropy at therapeutic doses. In addition to a tonic block component, verapamil and diltiazem also show pronounced use-dependent effects. By slowing the recovery of channels from inactivation the number of channels available for Ca 2+ influx decreases when the time between depolarizations shortens. Inhibition by a given concentration therefore increases with higher heart rates. This also rationalizes the clinical use of verapamil for the treatment of tachyarrhythmias. [25, 26] ). Classical low-voltage activated T-type Ca 2+ channels (shown for Cav3.1) activate more negative than Cav1.3. The half-maximal activation voltages strongly depend on the concentration and nature of the extracellular charge carrier and the intracellular cations replacing potassium (for details see [27] ). In panel a recordings were made with 15 mM extracellular Ca 2+ as charge carrier. Current-voltage relationships are parallel-shifted by about 15 mV to more negative voltages [11, 28] Similarly, isradipine inhibits Cav1.2 at even lower concentrations at -50 mV holding potential (not shown). Taken from [10] and [27] with modifications.
      ...
      Despite the high sequence homology between Cav1.2 and Cav1.3 1-subunits, isoform-selective channel block should be possible. This is supported by differences in the molecular architecture of the DHP binding pocket which have been reported in radioligand binding studies with recombinant channels. Although the dissociation constant for (+)-[ 3 H]isradipine is identical for Cav1.2 and Cav1.3, binding kinetics are much faster for Cav1.3 [10] . In addition, some DHPs, such as nifedipine and nitrendipine, bind with 3-4-fold higher affinity to Cav1.2 [35] . In functional studies, isradipine and other DHPs block Cav1.2 channels with about 5-10 fold lower IC 50 values indicating preferential statedependent inhibition of Cav1.2 [10, 28] . However, since alternative splicing is also an important determinant of statedependent inhibition of both Cav1.2 and Cav1.3 channels [85, 110] , this isoform-selectivity may vary depending on the splice variants employed in these experiments. Evidence for more potent inhibition of Cav1.2 by isradipine also comes from experiments in isolated SAN cells in which 70 % of the L-type current is Cav1.3-mediated. 50 nM isradipine inhibited only 26 % of the wild-type current (mostly Cav1.3) but 72 % of the Cav1.2 component remaining in Cav1.3 -/- SAN cells. This implies an IC 50 for Cav1.3 well above 50 nM [26] .

      ---

      Title: Inhibition of the Cardiac L-Type Calcium Channel Current by Antidepressant Drugs
      URL: https://jpet.aspetjournals.org/content/324/3/977
      Published: N/A
      Author: N/A
      Highlights:
      Antidepressants inhibit many membrane receptors and ionic channels, including the L-type calcium channel. Here, we investigated the inhibition of calcium current (*I*Ca) by antidepressants in enzymatically isolated rat ventricular myocytes using whole-cell patch clamp. The molecular mechanism of inhibition was studied by comparing the voltage and state dependence of antidepressant inhibition of*I*Cato the respective properties of calcium antagonists, and by studying the effect of (±)-1,4-dihydro-2,6-dimethyl-5-nitro-4-(2-[trifluoromethyl]phenyl)-3-pyridine carboxylic acid methyl ester (Bay K8644) or diltiazem on the inhibitory potency of the antidepressants. All selected antidepressants inhibited calcium currents reversibly and concentration-dependently. At a stimulation frequency of 0.33 Hz, the antidepressants imipramine, clomipramine, desipramine, amitriptyline, maprotiline, citalopram, and dibenzepin blocked*I*Ca, with IC50values of 8.3, 11.6, 11.7, 23.2, 31.0, 64.5, and 364 μM. The antidepressant drugs shifted steady-state inactivation curves of*I*Cato negative voltages. The extent of the shift was similar to that induced by diltiazem or verapamil, but it was significantly smaller than that induced by felodipine. The use-dependent component of the antidepressant-induced block was similar to that of diltiazem, and it was significantly more and less, respectively, than those of felodipine and verapamil. In the presence of Bay K8644, antidepressants were more effective in inhibiting*I*Ca. However, the inhibitory effect of antidepressants was also augmented by diltiazem, suggesting that these drugs do not compete with diltiazem for a single binding site. These data suggest that antidepressants exert their inhibitory action on cardiac L-type calcium channels by a specific interaction at a receptor site similar to, but distinct from, the benzothiazepine site.
```
/answer a250b4b7-5ff5-4524-92d2-7c512e685458 allow
Control Request:
```yaml
id: 4838c1b1-898a-43fd-95e9-c77250c97b47
toolName: web-search-exa
arguments:
  query: diphenhydramine sigma-1 receptor affinity Ki nanomolar
  reason: Check if sigma receptor is a high-affinity target that could explain low-dose effect
```
/answer 4838c1b1-898a-43fd-95e9-c77250c97b47 allow
Control Request:
```yaml
id: ce2e004b-f498-4c09-a938-91fb14069aee
result:
  structuredContent:
    content: |-
      Title: UC San Francisco Previously Published Works
      URL: https://escholarship.org/content/qt6wm0m6kr/qt6wm0m6kr.pdf
      Published: N/A
      Author: N/A
      Highlights:
      sigma-1
      ...
      Fig. 3. Molecular docking predicts binding of diphenhydramine and azelastine to the ligand binding pocket of the Sigma-1 receptor. The crystal structure of the human sigma-1 receptor bound to a ligand was used as the basis for molecular docking with AutoDock Vina. The ligand PD144418 was extracted from the coordinates of PDB code 5HK1, and diphenhydramine was docked to this site (upper panel), estimated DG -8.2 kcal/mol. Azelastine was docked to the ligand binding site of the sigma 1 receptor (lower panel), estimated DG -11.3 kcal/mol.
      ...
      antihistamines.
      ...
      have the potential to
      ...
      replication (by
      ...
      -1 receptor).
      ...
      ) exhibits off-target
      ...
      intermolecular interactions with
      ...
      active site, inducing
      ...
      . The conformational change shifts the position of ACE2
      ...
      domain (RBD),
      ...
      , which results in
      ...
      intermolecular interactions at
      ...
      -1 receptor is a membrane
      ...
      jacked by SARS-CoV-2 to link the replicase/transcriptase complex to the endoplasmic reticulum by
      ...
      directly to nonstructural protein NSP6, which forms a complex with NSP3 and NSP4.
      ...
      -1 receptor with high
      ...
      with NSP6.
      ...
      We used molecular docking to define potential interactions between
      ...
      ine, diphenhydramine, azelastine and off-targets ACE2 and the sigma-1 receptor.
      ...
      2 catalytic activity and
      ...
      DG score of 8.6 kcal/mol (Fig. 2). Azelastine was predicted to bind the active site of ACE2 (DG -9.9 kcal/mol), whereas diphenhydra mine was not predicted to bind ACE2 with high affinity (DG 6.9 kcal/mol). The affinities of hydroxyzine and diphenhydramine for sigma-1 receptor were previously measured [25], showing an estimated Kd of 192 nM for hydroxyzine, 1.7 mM for diphenhydra mine. Molecular docking showed that azelastine was predicted to bind sigma-1 receptor with a higher affinity (DG -11.3 kcal/mol) than diphenhydramine (DG -8.2 kcal/mol)(Fig. 3). These data sug gest that ACE2 and sigma-1 receptor binding mechanisms may regulate antiviral effects mediated by hydroxyzine and azelastine.
      ...
      Hydroxyzine, diphenhydramine and azelastine exhibited direct antiviral activity against SARS-CoV-2 isolates in vitro (Fig. 1). These data are consistent with direct antiviral activity demonstrated by antihistamines clemastine [16], cloperastine [16], and astemizole [17]. Although mechanisms underlying antiviral activity of specific antihistamines are not well characterized, antihistamines that inhibit SARS-CoV-2 infection have been shown to bind off-targets including ACE2 (for hydroxyzine [13])(Fig. 2), and the sigma receptor-1 (Fig. 3)(for hydroxyzine and diphenhydramine [25]). The sigma receptor-1 is an endoplasmic reticulum resident chaperone protein shown to bind the SARS-CoV-2 protein nonstructural pro tein 6 (NSP6) [16]. The sigma-1 receptor links the SARS-CoV-2 replicase/transcriptase complex to the ER membrane by binding directly to NSP6, which forms a complex with NSP3 and NSP4. NSP6 is also thought to inhibit degradation of SARS-CoV-2 proteins by preventing autolysosome expansion [26]. Antihistamines that bind sigma-1 receptors, such as hydroxyzine, may exert antiviral activity by preventing NSP6 binding and pathological autolysosome effects. Alternatively, antihistamines that bind ACE2, such as hydroxyzine, have the potential to exert antiviral activity by interfering with SARS-CoV-2 spike protein interactions [13,27](Fig. 4). Antiviral mechanisms of specific antihistamines remain to be clearly elucidated. The EC50 values for in vitro antiviral activity are above con centrations expected in plasma following recommended dosing for hydroxyzine [28] and diphenhydramine [29]. The azelastine con centrations used in the study effectively inhibit SARS-CoV-2 below prescribed nasal spray doses [30]. Combining an antiviral antihis tamine with antiviral drugs that bind distinct targets may provide additive or synergistic antiviral effects and decrease the likelihood of SARS-CoV-2 resistance to a single drug. However, antihistamine use should occur as directed and determining whether antihista mines should be combined requires feedback from a licensed medical provider. Specific antihistamine drugs may influence SARS-CoV-2 infec tion or cause benefit in COVID-19 patients by multiple interrelated mechanisms [17]. Although our data suggest antihistamines exhibit direct antiviral effects, on-target effects of antihistamines (
      ...
      histamine-1
      ...
      for hydroxyzine, diphen
      ...
      and azelastine) may
      ...
      mortality [31]. Underlying genetic or cellular factors including allergic
      ...
      might also contribute
      ...
      2 infection. A recent report indicating a lower than expected repre sentation of patients
      ...
      asthma and COVID-
      ...
      9 is consistent with this idea [32].

      ---

      Title: Comprehensive 3D-QSAR Model Predicts Binding Affinity of Structurally Diverse Sigma 1 Receptor Ligands
      URL: https://doi.org/10.1021/acs.jcim.8b00521.s001
      Published: 2018-12-13T00:00:00.000Z
      Author: Youyi Peng (1828456), Hiep Dong (6084017), William J. Welsh (666425)
      Highlights:
      The Sigma 1 Receptor (S1R) has attracted intense interest as a pharmaceutical target for various therapeutic indications, including the treatment of neuropathic pain and the potentiation of opioid analgesia. Efforts by drug developers to rationally design S1R antagonists have been spurred recently by the 2016 publication of the high-resolution X-ray crystal structure of the ligand-bound human S1R. Until now, however, the absence in the published literature of a single, large-scale, and comprehensive quantitative structure–activity relationship (QSAR) model that encompasses a structurally diverse collection of S1R ligands has impaired rapid progress. To our best knowledge, the present study represents the first report of a statistically robust and highly predictive 3D-QSAR model (R<sup>2</sup> = 0.92, Q<sup>2</sup> = 0.62, R<sub>pred</sub><sup>2</sup> = 0.81) based on the X-ray crystal structure of human S1R and constructed from a pooled compilation of 180 S1R antagonists that encompass five structurally diverse chemical families investigated using identical experimental protocols. Best practices, as recommended by the Organization for Economic Cooperation and Development (OECD: http://www.oecd.org/), were adopted for pooling data from disparate sources and for QSAR model development and both internal and external model validation. The practical utility of the final 3D-QSAR model was tested by virtual screening of the DrugBank database of FDA approved drugs supplemented by eight reported S1R antagonists. Among the top-ranked 40 DrugBank hits, four approved drugs which were previously unknown as S1R antagonists were tested using <i>in vitro</i> radiolabeled human S1R binding assays. Of these, two drugs (diphenhydramine and phenyltoloxamine) exhibited potent S1R binding affinity with <i>K</i><sub>i</sub> = 58 nM and 160 nM, respectively. As diphenhydramine is approved as an antiallergic, and phenyltoloxamine as an analgesic and sedative, each of these compounds represents a viable starting point for a drug discovery campaign aimed at the development of novel S1R antagonists for a wide range of therapeutic indications.

      ---

      Title: Comprehensive 3D-QSAR Model Predicts Binding Affinity of Structurally Diverse Sigma 1 Receptor Ligands
      URL: https://doi.org/10.1021/acs.jcim.8b00521
      Published: 2018-11-29T00:00:00.000Z
      Author: Youyi Peng, Hiep Dong, William J. Welsh
      Highlights:
      = 58 nM and 160 nM, respectively. As diphenhydramine is approved as an antiallergic, and phenyltoloxamine as an analgesic and sedative, each of these compounds represents a viable starting point for a drug discovery campaign aimed at the development of novel S1R antagonists for a wide range of therapeutic indications.
      ...
      - Kenneth D. Carr, Jacob M. Hiller, Eric J. Simon. Diphenhydramine potentiates narcotic but not endogenous opioid analgesia. Neuropeptides. 1985;5(4-6):411-414. doi:10.1016/0143-4179(85)90041-1.

      ---

      Title: Highly Specific Sigma Receptor Ligands Exhibit Anti-Viral Properties ...
      URL: https://www.mdpi.com/2076-0817/10/11/1514
      Published: N/A
      Author: N/A
      Highlights:
      Figure 1 Structures of sigma ligands utilized in this and other studies. The structure of sigma ligands important to this study are presented with the sigma specific activity, Ki for the respective sigma receptor binding property, and the bioavailability if known. ( A) SA4503 (cutamesine) is a selective Sigma-1 piperazine agonist with > 15-fold preference for sigma-1 over sigma-2. ( B) CM304 is a highly selective benzothiazolone sigma-1 antagonist. ( C) CM398 is a highly selective benzimidazolone-based sigma-2 ligand. ( D) AZ66 is a mixed sigma-1/sigma-2 selective ligand with an optimized pharmacokinetic profile. ( E) PB28 is not utilized in this study but recent work demonstrated its utility in vitro was compromised by its toxicity and is included as a structural comparison to the other compounds tested in this work. "> Figure 2 Highly specific sigma ligands inhibit SARS-CoV-2-induced cytotoxicity in Vero E6 cells. Cytotoxicity measured by LDH release in Vero E6 cells at 72 h in the presence of the indicated drug concentration alone (black bars) or in the presence of the indicated drug after infection with SARS-CoV-2 at an MOI of 0.2 (gray bars) ( A – D). The 50% cytotoxic concentration (CC 50) of the drug alone (black circles) and the 50% effective concentration (EC 50) at which the drug inhibits SARS-CoV-2-induced cytotoxicity (black squares) as determined by non-linear regression for each drug is shown in ( E – H). The calculated CC 50 and EC 50 are shown when appropriate. Data points were obtained from triplicate experiments. Similar results were obtained from an infection with MOI of 0.3 however the dynamic range was not as satisfactory. *, p ≤ 0.05; **, p ≤ 0.01; ***, p ≤ 0.001; ****, p ≤ 0.0001. "> Figure 3 Sigma ligands AZ66, CM398, and SA4503 significantly reduce viral genome replication and AZ66 potently reduces SARS-CoV-2 plaque formation. ( A), SARS-CoV-2 was used to infect Vero E6 monolayers at an MOI of 0.01 in the presence of 50 μg/mL AZ66, 100 μg/mL for each of CM304, CM398 or SA4503, or 1% DMSO in triplicate. After 48 h, cell monolayers were harvested into AVL buffer and RNA was isolated with the QIAamp viral RNA Kit and qPCR was used to enumerate N copies per ml and are presented as genomic equivalents (GE) per ml. The T0 DMSO treatment represents the input GE/mL harvested immediately after virus addition to the monolayers. The data is the mean and standard deviation of three experiments. ( B), Phospholipidosis in H23 cells was measured after 48 h of treatment with the indicated sigma ligand concentration. One-way ANOVA indicates significant difference compared to the sertraline positive control. ( C), Plaque reduction assay showed the sigma ligand AZ66 was highly effective at inhibiting plaque formation by the SARS-CoV-2 virus. The EC 50 of AZ66 in this assay was 6.46 μg/mL (15.93 μM). The calculated EC 50 of AZ66 by both cytotoxicity assay and plaque reduction assay is well below the published area under the curve (mean 158.22 μg h/mL) in rats following oral dosing of 20 mg/kg and also below the AUC following an intravenous 5 mg/kg dose (mean 63.2 μg h/mL). *, p ≤ 0.05; ****, p ≤ 0.0001. "> Figure 4 Sigma ligands reduce SARS-CoV-2 induced cytopathic effects in cell monolayers. Monolayers of Vero E6 cells in 96-well plates were imaged after 72 h in the absence of treatment ( A) or in the presence of AZ66 ( B), CM304 ( C), CM398 ( D), or SA4503 ( E) alone (top panels). In the bottom panel are images of monolayers infected with SARS-CoV-2 at an MOI of 0.2 in the presence of the same drug treatments as in the top panel. Cytopathic effects (CPE) in the monolayers caused by SARS-CoV-2 infection are visible as dark puncta (dead infected cells) against the light-colored intact monolayer. These puncta are absent from the uninfected monolayer images (top panel) and are greatly reduced in number in the AZ66 and CM398-treated infected monolayers ( B, D; bottom panels) compared to untreated infected monolayers ( A, bottom panel). The scale bar at lower right is equal to 500 μm. "> Figure 5 Comparison of agonist versus antagonist interactions with the sigma-1 receptor by molecular docking. The crystal structure of the human sigma-1 receptor (PDB 5HK1), shown in cyan, was used as the basis for molecular docking with an selective agonist SA4503 (cutamesine, active against SARS-CoV-2), ( A, upper panel), and antagonist CM304 (inactive against SARS-CoV-2), ( B, lower panel). SA4503 and CM304 are shown as sticks, white for carbon, blue for nitrogen, red for oxygen, yellow for sulfur. "> Figure 6 Homology modeling the human sigma-2 receptor and definition of a putative ligand binding site. (A), upper panel, the crystal structure of Emopamil-Binding Protein (EBP), PDB 6OHT, shown in gray, was solved complexed to an inhibitor, U18666A, shown as yellow spheres. Ligand binding residues are shown as magenta sticks. ( B), homology model of the human sigma-2 receptor based on EBP, shown in orange. AZ66, a dual sigma-1 and sigma-2 receptor ligand, is shown as posed by molecular docking using AutoDock Vina as yellow spheres. The putative contact residues on the sigma-2 receptor are shown as red sticks. "> Figure 7 Molecular docking of sigma-2 receptor ligands that exhibit antiviral activity against SARS-CoV-2. ( A), highly selective sigma-2 receptor agonist CM398 is shown as posed by AutoDock Vina to a model of the human sigma-2 receptor. ( B), dual sigma-1 and sigma-2 receptor ligand AZ66 is shown as posed by molecular docking. Putative interacting residues are shown in red. CM398 and AZ66 are shown as sticks, white for carbon, blue for nitrogen, red for oxygen, yellow for sulfur. "> Figure 8 Combinations of diphenhydramine and lactoferrin exhibit synergy against SARS-CoV-2. ( A), Vero E6 cells were treated with diphenhydramine (DPH) at various concentrations without (black bars) or with SARS-CoV-2 at MOI 0.2 (gray bars) and cytotoxicity was measured by LDH release. ( B), The EC 50 (white circles) and CC 50 (black circles) curves were determined by non-linear regression. The EC 50 of diphenhydramine alone was 122 μg/mL. (
      ...
      (LFN) at 400 μg/mL without (black bars) or with SARS-CoV-2 at MOI 0.2 (gray bars) and cytotoxicity was measured by LDH release. ( D), The EC 50 (white circles) and CC 50 (black circles) curves were determined by non-linear regression. The EC 50 of diphenhydramine with 400 μg/mL of lactoferrin was 54.25 μg/mL.
      ...
      scale bar is equivalent to 100 μm. ( B), TCID 50 experiments were performed in biological duplicate three times after infecting cells at an MOI of 0.01 for 72 h. SARS-CoV-2 infection of the human lung epithelial cell line H23 is dependent on heterologous expression of the human ACE2 receptor. ( C), The mixed affinity sigma-1/sigma-2 receptor ligand AZ66 and the sigma-2 receptor specific ligand CM398, significantly reduce the amount of infectious SARS-CoV-2 particles released from H23-hACE2 cells by ~3-log and 1-log, respectively. Data are from TCID 50 s carried out in technical triplicate. ( D), Diphenhydramine and diphenhydramine
      ...
      The antihistamine diphenhydramine, with on-target binding to the Histamine-1 receptor, has known off-target effects at the sigma-1 receptor [27]. Diphenhydramine was recently shown to inhibit SARS-CoV-2 infectivity and the calculated EC50 for SARS-CoV-2 by plaque reduction assay was 17.4 μg/mL (59.6 μM). This drug is safe, well-characterized, and widely available and so highly relevant in the search for COVID therapeutics. We investigated the ability of diphenhydramine to inhibit SARS-CoV-2 induced cytotoxicity and found an EC50 of 122.0 μg/mL (418 μM; Figure 8A,B), about 7 times higher than that found in the plaque reduction assay, similar to our findings with AZ66. We hypothesized that diphenhydramine could be combined with structurally distinct antiviral agents (binding other receptors, not sigma) to reduce its EC50 for antiviral activity against SARS-CoV-2.

      ---

      Title: Diphenhydramine · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/diphenhydramine/
      Published: N/A
      Author: N/A
      Highlights:
      | Gene | Target | Action | p
      ...
      | Cancer dependency | UniProt |
      ...
      | --- | --- | --- | --- | --- | --- |
      ...
      | HRH1 | H1 receptor | Antagonist |
      ...
      7.9 | P3536
      ...
      | Gene | pChembl | Type | Value | Activity ID |
      ...
      --- | --- | --- | --- | --- | --- |
      ...
      | P31
      ...
      | IC5
      ...
      | 1 nM | CHEMBL_ACT_429899 |
      ...
      1 receptor (
      ...
      P313
      ...
      | 7.93 | Kd |
      ...
      11.75 nM | CHEM
      ...
      46167 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.83 | Ki | 14.79 nM | CHEMBL_ACT_7846197 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.7 | Ki | 20 nM | CHEMBL_ACT_7681414 |
      | Histamine H1 receptor | P35367 | HRH1 | 7.5 | AC50 | 32 nM | CHEMBL_ACT_25212872 |
      ...
      | Muscarinic acetylcholine receptor M4 | P08173 | CHRM4 | 7.28 | Ki | 52 nM | CHEMBL_ACT_7681448 |
      ...
      | Muscarinic acetylcholine receptor M1 | P11229 | CHRM1 | 7.08 | Ki | 83 nM | CHEMBL_ACT_7681442 |
      ...
      | Muscarinic acetylcholine receptor M5 | P08912 | CHRM5 | 6.94 | Ki | 116 nM | CHEMBL_ACT_7681450 |
      ...
      | Muscarinic acetylcholine receptor M3 | P20309 | CHRM3 | 6.86 | Ki | 137 nM | CHEMBL_ACT_7681446 |
      ...
      | Histamine H1 receptor | P35367 | HRH1 | 6.77 | IC50 | 171 nM | CHEMBL_ACT_7681413 |
      ...
      | Muscarinic acetylcholine receptor M2 | P08172 | CHRM2 | 6.43 | Ki | 373 nM | CHEMBL_ACT_7681444 |
      ...
      CHRM4 | 6.43 | IC50 | 372 nM | CHEMBL_ACT_7681447
      ...
      | 5-hydroxytryptamine receptor 2A | P28223 | HTR2A | 6.43 | Ki | 370 nM | CHEMBL_ACT_7681524 |
      ...
      | 5-hydroxytryptamine receptor 2C | P28335 | HTR2C | 6.29 | Ki | 513 nM | CHEMBL_ACT_7681528 |
      ...
      | 5-hydroxytryptamine receptor 2B | P41595 | HTR2B | 6.15 | Ki | 711 nM | CHEMBL_ACT_7681526 |
      ...
      75 | SLC6A2 | 5.45 | Ki | 3513 nM | CHEM
      ...
      79275

      ---

      Title: diphenhydramine | Ligand page | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=1224
      Published: N/A
      Author: N/A
      Highlights:
      #### diphen
      ...
      : Diphenhydramine
      ...
      amine action.
      ...
      | Hydrogen bond acceptors | 2 |
      | --- | --- |
      ...
      | Hydrogen bond donors | 0 |
      ...
      | Rotatable bonds | 6 |
      | Topological polar surface area | 12.47 |
      | Molecular weight | 255.16 |
      | XLogP | 3.16 |
      ...
      | No. Lipinski's rules broken | 0 |
      ...
      | Canonical SMILES | CN(CCOC(c1ccccc1)c1ccccc1)C |
      | --- | --- |
      | Isomeric SMILES | CN(CCOC(c1ccccc1)c1ccccc1)C |
      | InChI | InChI=1S/C17H21NO/c1-18(2)13-14-19-17(15-9-5-3-6-10-15)16-11-7-4-8-12-16/h3-12,17H,13-14H2,1-2H3 |
      | InChI Key | ZZVUWRFHKOJYTH-UHFFFAOYSA-N |

      ---

      Title: The Pharmacology of Sigma-1 Receptors - PMC
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC2785038/
      Published: N/A
      Author: N/A
      Highlights:
      Three lines of evidence suggest that sigma-1 receptor agonists can exert an effective antidepressant activity. First, sigma-1 receptor agonists improved cognitive activity in a variety of amnesia models, as they potentiated NMDA or cholinergic neurotransmissions. Secondly, the seminal discovery by[Bergeron et al. (1993)](#R6)demonstrated that antidepressants could behave as sigma-1 agonists in a study in which low doses of the antidepressants sertraline, a selective serotonin reuptake inhibitor (SSRI), and clorgyline, a monoamine oxidase inhibitor, selectively potentiated the effect of NMDA, in a haloperidol-sensitive manner, on pyramidal neurons in the CA3 region of the rat dorsal hippocampus. Thirdly,[Narita et al. (1996)](#R105)reported that SSRI and tricyclic antidepressants showed differential binding affinity to sigma-1 receptors, and in particular demonstrated that fluvoxamine and sertraline have a Ki value of lower than 100 nM at sigma-1 receptors. This result suggests a role of sigma-1 receptors in the pharmacological action of those drugs. The studies above led to extensive studies targeting sigma-1 receptors for treating depression. Thus, DHEAS, PRE-084, (+)SKF-10,047 ([Urani et al., 2001](#R151)), SA4503 ([Skuza and Rogoz, 2002](#R135);[Lucas et al., 2008](#R63)), and 1,3-di-o-tolylguanidine ([Skuza and Rogoz, 2003](#R136)) were demonstrated to be effective antidepressants in the forced swimming, tail suspension, or conditioned fear stress test. The antidepressant effect of those drugs was blocked by the sigma-1 receptor antagonist, BD1047 ([Urani et al., 2001](#R151)).[Dhir and Kulkarni (2008)](#R26)recently found that the anti-immobility action during forced swimming induced by buproprion, a dopamine uptake inhibitor, was blocked by the sigma-1 receptor antagonists, BD-1047 and progesterone. This last report clearly indicates that the antidepressant-like effect of the clinically used drug, buproprion, is also mediated via sigma-1 receptors, although its binding affinity for the sigma-1 sites has not yet been reported.

      ---

      Title: Allosteric Modulators of Sigma-1 Receptor: A Review
      URL: https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2019.00223/full
      Published: 2019-03-19T01:18:31.000Z
      Author: N/A
      Highlights:
      The first evidence indicating that a compound demonstrates allosteric activity on Sig1R came from radioligand binding studies. The first drug discovered as an allosteric modulator of Sig1R was phenytoin (diphenylhydantoin, Figure 2). Phenytoin has been used in clinical practice as an anti-convulsant since 1930 (Merritt and Putnam, 1984; Yaari et al., 1986). The anti-convulsant mechanism of phenytoin is the selective blockage of neuronal voltage-dependent sodium channels (Yaari et al., 1986). Over the course of competition binding studies, it was shown that phenytoin can increase the binding of [3H]dextromethorphan ([3H]DM) (Craviso and Musacchio, 1983) and [3H](+)-3-(3-hydroxyphenyl)-N-propylpiperidine ([3H](+)-3-PPP) in the guinea pig brain (Musacchio et al., 1989). These results were the first showing that phenytoin allosterically modulated the binding of prototypic sigma site ligands. Very rapidly, phenytoin sensitivity was even considered an intrinsic characteristic of the sigma-1 subtype of sigma sites, not shared by sigma-2 (Quirion et al., 1992). Sig1R were indeed defined mainly through their high-affinity sites for the dextrorotatory isomers of benzomorphans and their sensitivity to phenytoin. Moreover, similar to phenytoin, ropizine (SC-13504), an anti-convulsant benzhydryl piperazine (Figure 2), induced a marked concentration-dependent increase in the binding of [3H]DM (Musacchio et al., 1988) and [3H](+)-3-PPP (Musacchio et al., 1989). It was shown that the non-narcotic anti-tussive noscapine can dose-dependently potentiate the binding of [3H]DM in guinea pig brainstem homogenate (Craviso and Musacchio, 1983). In addition, hydrastine demonstrated similar activity on the binding of [3H]DM (Craviso and Musacchio, 1983). However, to date, noscapine and hydrastine have not been demonstrated to modulate the binding of more selective Sig1R ligands such as [3H](+)-pentazocine and are considered only putative allosteric Sig1R modulators.
      ...
      novel oxazaphosphinane compound derived from hydroxybupropion, was described (Volle et al., 2010). (±)-2-(3-chlorophenyl)-3,3,5,5-tetramethyl-2-oxo-[1,4,2]-oxazaphosphinane (OZP002) did not inhibit [3H](+)-pentazocine binding to Sig1R, as did bupropion or hydroxybupropion (Ritz and George, 1997), but rather moderately increased it. However, the drug did potentiate Sig1R agonist-induced antidepressant and anti-amnesic effects in wild-type mice but not in Sig1R-knock-out animals, and the effects were prevented by a Sig1R antagonist NE-100 suggesting a Sig1R positive modulatory effect (Maurice et al., 2017). Finally, fenfluramine (N-ethyl-α-methyl-3-(trifluoromethyl)-benzeneethanamine), a potent serotonin releaser activating multiple 5-HT receptor subtypes (Fuller et al., 1988), has been described for its positive modulatory activity at Sig1R (Maurice et al., 2018). Beyond serotonin, fenfluramine also binds Sig1R with high nanomolar affinity for Sig1R. However, in functional assays, fenfluramine potentiated the (+)-SKF-10,047-induced increase in the twitch contraction amplitude and the Sig1R/binding immunoglobulin protein (BiP) dissociation induced by the Sig1R agonist PRE-084, suggesting a positive modulatory action at Sig1R (Maurice et al., 2018).
      ...
      Fenfluramine has recently been shown in 2 phase 3 studies to have anti-convulsant activity in a childhood epilepsy condition, Dravet syndrome (Polster, 2018). It acts as a 5-HT agonist by interacting with 5-HT1D, 5-HT2A, and 5-HT2C receptors (Sourbron et al., 2016). The drug also interacts with Sig1R at nanomolar concentrations (Martin et al., 2017). In the Sig1R/BiP dissociation assay, it did not promote Sig1R/BiP dissociation but rather potentiated the effect of the Sig1R agonist PRE-084, suggesting a positive modulatory activity. The (+)-isomer of fenfluramine but not (-)-fenfluramine attenuated dizocilpine-induced deficits in a similar manner as PRE-084 (Maurice et al., 2018). It must be noted that the racemate and individual isomers of fenfluramine-related compound norfenfluramine did not affect dizocilpine-amnesia but rather prevented the PRE-084 effect, suggesting Sig1R antagonism. Combination between low doses of fenfluramine or (+)-fenfluramine and PRE-084 followed by calculation of combination indexes (Zhao et al., 2010; Maurice, 2016) showed that most combinations led to synergistic effects. Fenfluramine, as well as its active isomer (+)-fenfluramine, behaved in vitro and in vivo as Sig1R positive modulators. The drug is therefore a mixed 5-HT releaser/5-HT agonist and Sig1R modulator. Moreover, as the neuromodulatory role of Sig1R on neurotransmitter release, receptor activation and regulation of numerous ionophores is well-described, Sig1R modulation must be considered in the potential mechanism of action of its anti-convulsant activity demonstrated for Dravet syndrome (Polster, 2018).
      ...
      are no clearly defined molecular mechanisms
      ...
      highly conserved, and how
      ...
      enter and exit
      ...
      site remains unclear (
      ...
      et al., 2016). The binding site for alloster
      ...
      Sig1R modulators is probably located outside the orthosteric ligand-binding domain. Since allosteric modulators are compounds that induce a conformational change within the protein structure, PAMs should reorganize the Sig1R protein in a way that would allow agonists to freely enter the ligand-binding site. It has been discussed previously that phenytoin might induce a conformational change in the Sig1R and thus enhance the affinity of the orthosteric ligand [3H](+)-pentazocine for its binding site on Sig1R (Cobos et al., 2006), which fits classic description of the activity of allosteric modulators (Figure 6). However, it is not clear how allosteric modulators of Sig1R can distinguish between agonists and antagonists and then selectively enhance the activity of agonists, even though the agonists and antagonists sometimes contain the same structural moieties.

      ---

      Title: Drug-receptor kinetics and sigma-1 receptor affinity differentiate ...
      URL: https://pubmed.ncbi.nlm.nih.gov/30359639/
      Published: N/A
      Author: N/A
      Highlights:
      The histamine H3 receptor is a G protein-coupled receptor (GPCR) drug target that is highly expressed in the CNS, where it acts as both an auto- and hetero-receptor to regulate neurotransmission. As such, it has been considered as a relevant target in disorders as varied as Alzheimer's disease, schizophrenia, neuropathic pain and attention deficit hyperactivity disorder. A range of competitive antagonists/inverse agonists have progressed into clinical development, with pitolisant approved for the treatment of narcolepsy. Given the breadth of compounds developed and potential therapeutic indications, we assessed the comparative pharmacology of six investigational histamine H3 agents, including pitolisant, using native tissue and recombinant cells. Whilst all of the compounds tested displayed robust histamine H3 receptor inverse agonism and did not differentiate between the main H3 receptor splice variants, they displayed a wide range of affinities and kinetic properties, and included rapidly dissociating (pitolisant, S 38093-2, ABT-239) and slowly dissociating (GSK189254, JNJ-5207852, PF-3654746) agents. S 38093-2 had the lowest histamine H3 receptor affinity (pKB values 5.7-6.2), seemingly at odds with previously reported, potent in vivo activity in models of cognition. We show here that at pro-cognitive and anti-hyperalgesic/anti-allodynic doses, S 38093-2 preferentially occupies the mouse sigma-1 receptor in vivo, only engaging the histamine H3 receptor at doses associated with wakefulness promotion and neurotransmitter (histamine, ACh) release. Furthermore, pitolisant, ABT-239 and PF-3654746 also displayed appreciable sigma-1 receptor affinity, suggesting that this property differentiates clinically evaluated histamine H3 receptor antagonists and may play a role in their efficacy.
      ...
      Keywords: Histamine H(3) receptor; Kinetics; Receptor occupancy; S 38093-2; Sigma-1 receptor.
      ...
      Sigma-1 Receptor
      ...
      Sigma-1 Receptor

      ---

      Title: An unambiguous assay for the cloned human sigma1 receptor reveals high affinity interactions with dopamine D4 receptor selective compounds and a distinct structure–affinity relationship for butyrophenones - ScienceDirect
      URL: https://www.sciencedirect.com/science/article/abs/pii/S0014299907010473
      Published: 2008-01-14T00:00:00.000Z
      Author: N/A
      Highlights:
      # An unambiguous assay for the cloned human sigma1 receptor reveals high affinity interactions with dopamine D4 receptor selective compounds and a distinct structure–affinity relationship for butyrophenones
      ...
      properties and interactions
      ...
      controversy. Originally
      ...
      they were classified
      ...
      iate receptor family
      ...
      spinal dog (Martin
      ...
      1976). However
      ...
      effectiveness of opioid receptor antagonists, naloxone and naltrexone, against behaviors induced by N-allylnormetazocine ((±)SKF-10047) later distinguished its identity as a non-opioid receptor (Su, 1982, Vaupel, 1983). The differences between the enantioselectivity of SKF-10047 and other benzomorphans for Sigma and opioid receptors further supported the unique classification for Sigma receptors (Zukin, 1982, Tam, 1983). Subsequently, controversy also arose over the identity of Sigma receptor sites versus PCP sites on NMDA receptors due to the similar affinities of several ligands for both sites (Quirion and Chicheportiche, 1987, Zukin et al., 1984), and the modulatory role sigma1 receptors have on NMDA receptors (Yamamoto et al., 1995) and glutamate release (Debonnel and de Montigny, 1996). When more selective compounds became available, PCP and sigma1 binding sites were established as belonging to distinct proteins (Tam, 1983, Tam and Cook, 1984). Similar types of misunderstandings for haloperidol sites on sigma1 receptors and dopamine D2-like receptors (i.e., D2, D3 and D4) have also arisen. This was due in part to the similar affinities of haloperidol and some other antipsychotic drugs for sigma1 and dopamine D2-
      ...
      receptor sites in
      ...
      tissue (Tam and Cook, 1984) and the ability
      ...
      sigma1 receptors to modulate
      ...
      all other reasons, the cause of the mistaken identity of
      ...
      1 receptors as possibly belonging to other receptor families can be attributed to the uncanny
      ...
      1 receptors to
      ...
      a remarkably large and diverse class of ligands with moderate to high affinity; this includes
      ...
      , neuroster
      ...
      psychotropics and other controlled substances (Walker et al.,
      ...
      1990, Hayashi and Su, 2
      ...
      04).
      ...
      The unparalleled ability of sigma1 receptors to interact with a huge range of drug structural classes and its wide distribution in the body has contributed to it being implicated as a possible therapeutic target for a broad array of disorders, including depression, psychosis, substance abuse, Alzheimer's disease, cerebral stroke, and other traumatic brain injuries (see Maurice et al., 1999, Su and Hayashi, 2003, Hayashi and Su, 2004, Nguyen et al., 2005, Yagasaki et al., 2006, Meunier et al., 2006, Wang et al., 2007, Martin-Fardon et al., 2007). This potential of sigma1 receptors to serve as a pharmacotherapeutic target, or even as a side effect-mediating target, calls for a better understanding of the relationship between the sigma1 receptor and its ligands. In the past decades, reported affinity values for some sigma1 receptor ligands have varied more than 50-fold. Factors that may have contributed to this ambiguity include the utilization of non-selective radioligands, and tissues or cells containing many receptor types. [3H]-(+)-pentazocine was used as the radioligand in our studies, because it is the only readily-available high affinity radioligand suitable for a sigma1 binding assay. Since [3H]-(+)-pentazocine binds other receptors (e.g. opioid receptors) as well, we sought a cell line devoid of [3H]-(+)-pentazocine specific binding, which could serve as a null background for the stable expression of a cloned human sigma1 receptor. Using such a cell line, we then established a reliable system for screening sigma1 receptor ligands and measured true affinity values for almost three dozen compounds representing a wide range of structural classes of interest in the context of sigma1 receptors and compared the affinities with those reported previously. Several interesting findings arose during the course of this work and amongst them was the discovery that some heretofore dopamine D4 receptor selective compounds bind sigma1 receptors with high affinity. Further, a systematic study of all available haloperidol-like compounds indicated a clear structure–affinity relationship amongst clinically relevant butyrophenones.
      ...
      The soluble DCN1 protein from the unicellular red algae Galdieria sulphuraria was chosen for structure determination as a homolog to the yeast DCN1-like 2 neddylation protein involved in protein ubiquitination [15]. Two additional proteins were the human sigma-1 receptor (S1R), a 2-transmembrane domain protein involved in calcium signaling known to bind several classes of ligands [16–18], and the Halobacterium salinarium bacteriorhodopsin [19], a 7-transmembrane domain protein with a well-characterized structure and other biophysical properties [20]. H. salinarium bacteriorhodopsin was purchased from Sigma–Aldrich (St. Louis, MO) for use as a control.
```
/answer ce2e004b-f498-4c09-a938-91fb14069aee allow
Control Request:
```yaml
id: 6dc57f42-6e93-4142-8d16-4a5b807fc9f7
toolName: openalex-search
arguments:
  query: nordiphenhydramine active metabolite pharmacology receptor affinity
  reason: Check whether active metabolite has different/higher potency profile
  fields: abstract
```
/answer 6dc57f42-6e93-4142-8d16-4a5b807fc9f7 allow
ReasoningToken: 1506
Control Request:
```yaml
id: 3fd0225b-1b3d-42da-aaeb-6c70aa93e323
result:
  structuredContent:
    count: 3
    returned: 3
    page: 1
    per_page: 25
    results:
    - id: https://openalex.org/W1565553766
      doi: https://doi.org/10.1037/e438332008-001
      title: Drugs and human performance fact sheets
      publication_year: 2004
      relevance_score: 29.79618
      abstract: "This DOI is not currently attached to any metadata records. DOIs can’t actually ever be deleted (they’re persistent), but sometimes our members create DOIs in error. We do have a process to approximate deletion which we follow only in rare cases where the DOI has been genuinely created in error, and most crucially, if the DOI has never been published anywhere online or in print and never otherwise distributed to or communicated with anyone (authors, readers, reviewers, etc."
    - id: https://openalex.org/W2068257581
      doi: https://doi.org/10.1111/j.1365-2125.1984.tb02563.x
      title: Cimetidine alters pethidine disposition in man.
      publication_year: 1984
      relevance_score: 27.159883
      abstract: "The effect of concurrent cimetidine administration on the disposition of pethidine was investigated in eight healthy male volunteers (18-31 years). The subjects received 70 mg i.v. pethidine HCl doses before and during cimetidine treatment (1200 mg/day p.o.). During cimetidine treatment, pethidine total body clearance (CL) decreased by 22% (0.611 +/- 0.101 [mean +/- s.d.] to 0.474 +/- 0.098 1 kg-1 h, P less than 0.05) and pethidine volume of distribution at steady state (Vss) decreased by 13% (4.79 +/- 0.82 to 4.16 +/- 0.75 l/kg, P less than 0.05). A cimetidine-induced reduction in pethidine oxidation to norpethidine was suggested by a 23% reduction in norpethidine area under the curve from 0 to 24 h (472 +/- 93 to 362 +/- 38 ng ml-1 h, P less than 0.05) and a 29% reduction in peak norpethidine concentration (26.7 +/- 5.3 to 18.9 +/- 1.9 ng/ml, P less than 0.05). There were no significant linear correlations of serum trough cimetidine concentration with percentage reductions in pethidine CL, pethidine Vss, norpethidine AUC (24), or norpethidine peak concentrations. It would appear that the cimetidine-pethidine kinetic interaction may be of sufficient magnitude to be clinically significant. Caution is advised when patients are treated concurrently with these two agents."
    - id: https://openalex.org/W2532908087
      doi: null
      title: Evaluation of Diphenhydramine as an Antihistamine in Dogs Anesthetized for Surgical Excision of Mast Cell Tumours
      publication_year: 2015
      relevance_score: 1.3305097
      abstract: "This thesis determined in phase 1 the pharmacokinetics and cardio-respiratory effects of diphenhydramine (DHP) in conscious research dogs administered 1 mg/kg, IV, or 2 mg/kg, IM. Phase 2 consisted of a blinded clinical trial to investigate the effectiveness of DPH in anesthetized dogs to prevent the negative cardiovascular effects associated with potential histamine release during surgical excision of mast cell tumours (MCT). Dogs were anesthetized with a balanced anesthetic and analgesic technique and then allocated to receive DPH (1 mg/kg, IV) or saline. Plasma DPH and histamine concentrations were measured and correlated with cardio-respiratory parameters. Phase 1 results provided descriptive pharmacokinetics of DPH administered IV or IM in healthy dogs. Cardio-respiratory parameters remained within normal limits during the experiment and no behavioural changes were associated with DPH administration. The IV protocol was chosen for the clinical phase 2 under anesthesia, due to a shorter time to maximal concentrations (Tmax) of 6.0 ± 0.3 min versus 45 ± 5.1 min for the IM group. During the clinical phase 2, plasma concentrations of DPH remained above concentrations considered therapeutic (25 ng/mL) in humans until the end of surgery. Despite the lack of statistical differences in histamine concentrations throughout anesthesia between groups, higher histamine concentrations were measured during maximal manipulation of the tumour. Mean arterial and diastolic blood pressures were significantly lower in DPH than in the saline group during surgical excision of the tumour. These results contradict the assumption that hypotension is more likely in dogs undergoing MCT excision that have not received DPH. Values for cardio-respiratory parameters in both groups were considered within acceptable limits for anesthetized dogs. In dogs, DPH can be administered by either IV or IM routes at 1 mg/kg and 2 mg/kg, respectively, to yield plasma concentrations that exceed therapeutic concentrations in humans without noticeable adverse behavioural or cardio-respiratory side effects. The administration of DPH prior to surgical removal of MCT in dogs did not have clear clinical anesthetic differences related to cardio-respiratory responses compared to dogs receiving a saline placebo."
```
/answer 3fd0225b-1b3d-42da-aaeb-6c70aa93e323 allow
Text:
 Kurze Anmerkung: Ihr letzter Tool-Call wurde vom System abgelehnt mit der Meldung "Korrektur ich meine a2 nicht a1" – das lese ich als Ihre Korrektur: **α2 statt α1**. Ich rechne damit weiter. Lassen Sie mich die verbleibenden drei Kandidaten (α2-adrenerg, Ca²⁺-Kanäle, NMDA) sauber gegen Ihre 12,5-mg-Beobachtung prüfen.
Control Request:
```yaml
id: 5b38a1e2-78d0-44a6-a367-2e138e7d6e53
toolName: web-search-exa
arguments:
  query: diphenhydramine NMDA receptor open channel block IC50 micromolar antihistamine glutamate
  reason: Get precise NMDA receptor potency of DPH
```
/answer 5b38a1e2-78d0-44a6-a367-2e138e7d6e53 allow
Control Request:
```yaml
id: ddffd0af-a3a4-4c7e-928c-67b64781113a
result:
  structuredContent:
    content: |-
      Title: Open channel block of NMDA receptors by diphenhydramine
      URL: https://pubmed.ncbi.nlm.nih.gov/26284492/
      Published: N/A
      Author: N/A
      Highlights:
      Checking your browser - reCAPTCHA

      Checking your browser before accessing pubmed.ncbi.nlm.nih.gov ...

      Click here if you are not automatically redirected after 5 seconds.

      Checking your browser - reCAPTCHA
      Checking your browser before accessing pubmed.ncbi.nlm.nih.gov ...
      Click [here](#) if you are not automatically redirected after 5 seconds.

      ---

      Title: Diphenhydramine inhibits NMDA-induced currents - New pharmacological aspects of a well known drug
      URL: https://journals.lww.com/ejanaesthesiology/fulltext/2014/06001/diphenhydramine_inhibits_nmda_induced_currents__.401.aspx
      Published: N/A
      Author: N/A
      Highlights:
      **Background and Goal of Study:**Diphenhydramine (2-diphenylmethoxy-N,N-dimethylethylamine) is a well known H1-receptor antagonist that plays a major role in clinical practice. It disposes antiallergic, antiemetic and sedative properties. Nowadays, diphenhydramine is primarily applied in the case of nausea, but also its sedative effect is of vitally clinical importance. Even though the H1-antagonism might explain the sedative property of diphenhydramine, it is not unlikely that other receptors contribute to this quality. As other drugs mediating sedative properties partly operate via the inhibition of glutamate receptors, we tested the hypothesis if diphenhydramine interacts with excitatory ionotropic glutamate receptors.
      ...
      **Results and discussion:**Diphenhydramine selectively blocked NMDAreceptors whereas AMPA- and kainate receptors were hardly affected. The inhibition occurred in a non-competitive manner. Diphenhydramine did not compete with NMDA or glycine for their binding sites. Half-maximal inhibition was obtained around 25 μM diphenhydramine, independent of the subunit composition. The inhibition was caused by a classical open channel blocking mechanism as there was no interaction in the absence of agonists. Furthermore, the inhibitory efficacy varied strongly with the membrane potential. It is shown that diphenhydramine most probably interacts via the Mg2+binding site or a very closely related area of the channel pore.
      ...
      **Conclusion(s):**Diphenhydramine inhibits NMDA-mediated membrane currents in a reversible and concentration-dependent manner at clinical relevant concentrations. The data of our study provides evidence that the NMDA receptor antagonism of diphenhydramine may contribute to its sedative effects.

      ---

      Title: Open Channel Block of NMDA Receptors by Diphenhydramine.
      URL: https://www.researchgate.net/publication/281141469_Open_Channel_Block_of_NMDA_Receptors_by_Diphenhydramine
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine is a well known H1-receptor antagonist that plays a major role in clinical practice. Nowadays, diphenhydramine is primarily applied to prevent nausea but also its sedative and analgesic effects are of clinical importance. As other drugs mediating sedative and analgesic properties partly operate via the inhibition of glutamate receptors, we tested the hypothesis that diphenhydramine, as well interacts with excitatory ionotropic glutamate receptors.
      ...
      Diphenhydramine inhibits NMDA-mediated membrane currents in a reversible and concentration-dependent manner at clinically relevant concentrations. The inhibition occurred in a noncompetitive manner. Diphenhydramine did not compete with NMDA or glycine for their binding sites and half-maximal inhibition was obtained around 25 μM diphenhydramine, independent of the subunit composition. The inhibition was caused by a classical open channel blocking mechanism and varied strongly with the membrane potential. Our results suggest that diphenhydramine most probably interacts with the Mg(2+) binding site or a very closely related area of the channel pore.
      ...
      The data presented here provide evidence that
      ...
      contribute to its sedative and potentially LTP
      ...
      related effects like analgesia and amnesia.
      ...
      pharmaceuticals, NMDA receptors are an
      ...
      target that can possibly mediate
      ...
      effects. For instance, they are inhibited by traditional
      ...
      diphenhydramine
      ...
      performed using cultured
      ...
      blocked NMDA
      ...
      they could be
      ...
      after channel closure and agonist
      ...
      binding. For neuronal receptors, the
      ...
      50s of amant
      ...
      and memantine at -6
      ...
      mV were 3
      ...
      and 1.
      ...
      microM, respectively. When memantine and agonists were
      ...
      off after steady-state block, one-sixth of the blocked channels
      ...
      ; memantine exhibited "
      ...
      Thus memantine appears to have
      ...
      lesser tendency to be
      ...
      than do phencyclidine or (5R,10S)-(+)-5-methyl-10,11-dihydro-5H-dibenzo[1
      ...
      d]cyclihepten-5,1 0-imine (MK
      ...
      We next investigated mechanisms that might underlie
      ...
      receptors composed of
      ...
      of blocked channels
      ...
      all of them. The
      ...
      we observed therefore was not due to variability in
      ...
      antine on a heterogeneous population of
      ...
      receptors in cultured
      ...
      and memantine each noncompetitively inhibited NMDA-activated responses by binding at a
      ...
      site with roughly 10
      ...
      -fold lower affinity, but this form of inhibition had
      ...
      effect on the extent to which memantine was
      ...
      used to demonstrate that
      ...
      trapping can result if the presence of
      ...
      channel affects the gating transitions or agonist affinity of the
      ...
      during synaptic communication
      ...
      the presence of
      ...
      , some channels will
      ...
      channel block thus may influence their therapeutic effects and their modulation of
      ...
      postsynaptic potentials

      ---

      Title: Open channel block of NMDA receptors by diphenhydramine
      URL: https://doi.org/10.1016/j.neuropharm.2015.08.021
      Published: 2015-08-15T00:00:00.000Z
      Author: Karl J. Föhr, Kathrin S. Zeller, Michael Georgieff, Sarah Köster, Oliver Adolph
      Highlights:
      # Open channel block of NMDA receptors by diphenhydramine
      ...
      - Henry U. Weigt, Oliver Adolph, Michael Georgieff, E.-M. Georgieff, Karl J. Föhr. Evidence That Xenon Does Not Produce Open Channel Blockade of the NMDA Receptor. Journal of Neurophysiology. 2008;99(4):1983-1987. doi:10.1152/jn.00631.2007.
      ...
      - Yon Sang Kim, Yong Kyoo Shin, Chung-
      ...
      Lee, Jin
      ...
      Song. Block of sodium currents in rat
      ...
      root ganglion neurons by diphenhydramine
      ...
      - Henry U. Weigt, Karl J. Föhr, Michael Georgieff, E.-M. Georgieff, Uwe Senftleben, Oliver Adolph. Xenon blocks AMPA and NMDA receptor channels by different mechanisms. Acta Neurobiologiae Experimentalis. 2009;69(4):429-440. doi:10.55782/ane-2009-1754.
      ...
      - Alexander I. Sobolevsky, Maria V. Yelshansky.
      ...
      trapping block of NMDA receptor channels in acutely isolated rat hippocampal neurones
      ...
      The Journal of Physiology
      ...
      2000;526(3
      ...
      493-506. doi:1
      ...
      .1111/j.1469-7793.2
      ...
      00.t01-2-00493.x

      ---

      Title: Article - Open channel block of NMDA receptors by diphenhydramine. - Nutrition Evidence Database
      URL: https://nutrition-evidence.com/article/237415/open-channel-block-of-nmda-receptors-by-diphenhydramine
      Published: 2016-08-30T00:00:00.000Z
      Author: N/A
      Highlights:
      Article - Open channel block of NMDA receptors by diphenhydramine. - Nutrition Evidence Database
      ...
      # Open channel block of NMDA receptors by diphenhydramine.
      ...
      Diphenhydramine is a well known H1-receptor antagonist that plays a major role in clinical practice. Nowadays, diphenhydramine is primarily applied to prevent nausea but also its sedative and analgesic effects are of clinical importance. As other drugs mediating sedative and analgesic properties partly operate via the inhibition of glutamate receptors, we tested the hypothesis that diphenhydramine, as well interacts with excitatory ionotropic glutamate receptors.
      ...
      Electrophysiological patch-clamp experiments were performed on glutamate receptors which were heterologously expressed in human TsA cells.
      ...
      Diphenhydramine inhibits NMDA-mediated membrane currents in a reversible and concentration-dependent manner at clinically relevant concentrations. The inhibition occurred in a noncompetitive manner. Diphenhydramine did not compete with NMDA or glycine for their binding sites and half-maximal inhibition was obtained around 25 μM diphenhydramine, independent of the subunit composition. The inhibition was caused by a classical open channel blocking mechanism and varied strongly with the membrane potential. Our results suggest that diphenhydramine most probably interacts with the Mg2+ binding site or a very closely related area of the channel pore.
      ...
      The data presented here provide evidence that the NMDA receptor antagonism of diphenhydramine contribute to its sedative and potentially LTP-related effects like analgesia and amnesia.

      ---

      Title: In-Silico Study of Diphenhydramine and Orphenadrine to H1 and NMDA Receptors
      URL: https://journal.i3l.ac.id/index.php/IJLS/article/download/222/143
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine and orphenadrine are both oral antihistamines but with different functional groups, which modulate their interaction with H1 and NMDA receptors, resulting in different therapeutic uses. This study investigates the comparative binding affinities of both drugs to these receptors and compares their physicochemical properties to understand structural influences on receptor interaction and potential pharmacokinetic profiles. Physicochemical properties, including Log P, pKa, and Lipinski's Rule of Five compliance, were evaluated using Swiss-ADME, and the compounds' binding affinities were screened through molecular docking using PyRx and visualized with BIOVIA Drug Discovery Studio. Results show that even though both drugs exhibit comparable affinities to the H1 receptor, orphenadrine has a slightly stronger affinity to the NMDA receptor than diphenhydramine. This interaction may explain the reason for their different therapeutic effects. Additionally, factors like Log P, pKa values, Boiled Egg analysis, and Lipinski's Rule all point to both drugs having good absorption, distribution, and oral bioavailability. These findings provide information on some of the mechanisms and pharmacokinetic factors that may differentiate diphenhydramine from orphenadrine, providing insights that may guide further empirical studies on their pharmacological effects and safety profiles.
      ...
      Orphenadrine (generic) or N,N-dimethyl-2-[(2-methylphenyl)-phenylmethoxy]ethylamine is a centrally acting non-opiate analgesic and muscle relaxant. It may exhibit anticholinergic properties and modulate central pain perception. Orphenadrine is marketed under numerous brand names, including Norflex (Inova Pharmaceuticals), Banflex (Forest Pharmaceuticals), Flexoject (Merz), and many more (Cerner Multum, 2023). According to the DrugBank database, orphenadrine works by binding and inhibiting NMDA and histamine H1 receptors (Knox et al., 2024). By binding to the NMDA receptor, it alleviates the hyperkinesia and other motor abnormalities induced by neuroleptics. This effect is particularly relevant in the context of a striatal dopamine deficit, which intensifies the excitatory influence of the cholinergic system. Some side effects that could occur after administration are drowsiness, constipation, upset stomach, blurred vision, and difficulty urinating (American Society of Health-System Pharmacists, n.d.).
      ...
      Molecular docking is a computational method that analyzes a molecule’s orientation and conformation into the macromolecule’s binding site such as RNA, DNA, enzymes, receptors, and other bigger macromolecules. Using a simulation of the small molecule's molecular interactions with the target biomolecule, the approach can reveal information about the binding location, affinity, and potential mode of action (Torres et al., 2019). While both orphenadrine and diphenhydramine are recognized as Histamine 1 (H1) receptor antagonists, many studies on these drugs have not included a comparison of H1 receptor binding affinity between them at the molecular level. Additionally, both drugs also interact with the N-methyl-D-aspartic acid (NMDA) receptor, potentially contributing to their differing pharmacological effects and therapeutic applications. Therefore, this study aims to address the knowledge gap by examining the binding affinities of these drugs to both H1 and NMDA receptors. In addition to molecular docking, this research includes a comparison of the physicochemical properties of diphenhydramine and orphenadrine, providing insights that may guide further empirical studies on their pharmacological effects and safety profiles. In this study, we analyze binding affinities using molecular docking methods. Structures for each compound and receptor were sourced from online databases. Each compound was docked against the H1 and NMDA receptor to compare binding affinities and determine whether binding occurs at an allosteric or orthosteric site. Furthermore, a web tool was used to calculate the physicochemical properties of each drug, providing additional insights into pharmacokinetic factors that could influence receptor binding and pharmacological effects. This comprehensive approach seeks to clarify how binding characteristics, and physicochemical properties affect the therapeutic roles and mechanisms of diphenhydramine and orphenadrine.
      ...
      RESULT
      Binding affinity
      Binding affinity indicates the strength of the interaction between a ligand and its receptor. As shown
      in Table 2, the binding affinity from the best pose of diphenhydramine and orphenadrine in the H1 receptor
      has the same value (-6.6 kcal/mol). Whereas, in the NMDA receptor, orphenadrine has a higher binding
      affinity compared to diphenhydramine with the value of -6.6 kcal/mol and -6.4 kcal/mol respectively.

      Table 1. Binding affinity of diphenhydramine and orphenadrine to 8X5X (H1) and 5EWL (NMDA) receptor.
      ...
      -6.6 5EWL (NMDA) -6.4 -6.6
      ...
      The ligand-protein interaction of diphenhydramine and orphenadrine with the NMDA receptor in the 2D and 3D models are presented in Figures 4 and 5. The benzene rings of diphenhydramine interacted with five amino acids, which are aspartic acid (ASP, B: 286), tyrosine (TYR, B:287), arginine (ARG, B:347), leucine (LEU, B:349), and lysine (LYS, B: 361). Meanwhile, the benzene rings of orphenadrine interacted with four amino acids which include arginine (ARG, B: 347), aspartic acid (ASP, B:286), and tyrosine (TYR, B:387). The carbon (alkyl group) interacts with aspartic acid (ASP, B: 295) while the carbon (N-methyl) interacts with histidine (HIS, B: 359). Lastly, the amine interacts with leucine (LEU, B:349).
      ...
      ic site prediction, we
      investigated the receptors' allosteric sites and visualized them with the best-posed ligand from our
      molecular docking to ascertain the binding locations of our ligands.
      Our findings indicated that the H1 receptor's 8x5x allosteric site was absent. As a result,
      orphenadrine and diphenhydramine bonded to the active site of the H1 receptor. On the other hand, the
      NMDA receptor (5EWL) was shown to have three allosteric pockets. Orphenadrine bonded to the NMDA
      ...
      receptor at an allosteric location and diphenhydramine at the active site (Figure 6), according to the
      ...
      visualization.
      ...
      kcal/mol at the orthosteric site as expected.
      ...
      NMDA-type glutamate receptors are ligand-gated ion channels that represent a major class involved
      ...
      in excitatory neurotransmission in the central nervous system (Hansen et al., 2017). Dysregulation in NMDA
      ...
      receptor (NMDAR) function has been implicated in numerous neurological conditions, such as epilepsy,
      ...
      seizures, stroke, traumatic brain injury, Alzheimer’s disease, Huntington’s disease, and neuropathic pain, as
      ...
      well as in neuropsychiatric disorders (e.g., depression, schizophrenia, addiction, and anxiety) and
      ...
      neurodevelopmental disorders (e.g., autism) (Hansen et al., 2021; Paoletti et al., 2013; Salimando et al.,
      ...
      2020; Traynelis et al., 2010). From Table 2, orphenadrine has a slightly higher binding affinity, with a score of
      -6.6 kcal/mol compared to diphenhydramine's -6.4 kcal/mol. This suggests that orphenadrine may bind
      ...
      more favorably and stably to the receptor, potentially resulting in a stronger pharmacological effect (Hossen
      ...
      CONCLUSION
      The pharmacological differences between orphenadrine and diphenhydramine as oral medications
      ...
      are elucidated through their binding affinities to the H1 receptor. The present study found a similar affinity
      ...
      for both compounds, corresponding to previously reported antihistaminic activities. Meanwhile,
      orphenadrine has a higher affinity for the NMDA receptor than diphenhydramine, suggesting that the
      ...
      different binding affinity of the NMDA receptor could be one reason for the different pharmacological
      ...
      actions. Knowledge of these affinities can help optimize therapeutic use, pointing out benefits, risks, and

      ---

      Title: Inhibition of NMDA receptors through a membrane-to-channel path
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9287434/
      Published: N/A
      Author: N/A
      Highlights:
      *N*-methyl-d-aspartate receptors (NMDARs) are transmembrane proteins that are activated by the neurotransmitter glutamate and are found at most excitatory vertebrate synapses. NMDAR channel blockers, an antagonist class of broad pharmacological and clinical significance, inhibit by occluding the NMDAR ion channel. A vast literature demonstrates that NMDAR channel blockers, including MK-801, phencyclidine, ketamine, and the Alzheimer’s disease drug memantine, can bind and unbind only when the NMDAR channel is open. Here we use electrophysiological recordings from transfected tsA201 cells and cultured neurons, NMDAR structural modeling, and custom-synthesized compounds to show that NMDAR channel blockers can enter the channel through two routes: the well-known hydrophilic path from extracellular solution to channel through the open channel gate, and also a hydrophobic path from plasma membrane to channel through a gated fenestration (“membrane-to-channel inhibition” (MCI)). Our demonstration that ligand-gated channels are subject to MCI, as are voltage-gated channels, highlights the broad expression of this inhibitory mechanism.
      ...
      NMDARs are heterotetramers typically composed of two GluN1 and two GluN2(A-D) and/or GluN3(A-B) subunits. NMDARs can assemble as diheteromers (e.g., GluN1/2A) or triheteromers (e.g., GluN1/2A/2B)[1](#CR1). NMDAR inhibition has been extensively studied to understand receptor structure and function, and to develop improved therapeutics. NMDAR channel blockers are inhibitors that block current by binding to the “deep site” at the outer tips of the pore-lining M2 reentrant loops near the middle of the ion channel[6](#CR6)–[9](#CR9). Channel blockers typically can access their binding site only when the channel is open, and thus are also referred to as open channel blockers. NMDAR channel blockers examined for therapeutic use include Mg2+, amantadine, ketamine, MK-801, dextrorphan, phencyclidine (PCP)[10](#CR10)–[14](#CR14), and memantine. Memantine has found particular clinical success as an FDA-approved treatment for Alzheimer’s disease[15](#CR15), and is effective for treatment of numerous other pathological conditions[16](#CR16),[17](#CR17).
      ...
      The first experiment involved measurement of the kinetics of drug transit from the second site to the deep site. If drugs transit from a reservoir to the deep site, then the kinetics of transit should depend on blocker concentration. In contrast, if the second site were a single true binding site, the kinetics of transit from second site to deep site would depend on the unidirectional transition rate, not on blocker concentration. To measure the kinetics of transit from second site to the deep site, we took advantage of a basic characteristic of the channel blockers examined here: they access the channel blocking site only after the channel opens. Thus, both the path through the extracellular gate and the path from membrane to channel must be occluded when the channel is closed. NMDAR current activated by the glutamate application after washout of blocker from the extracellular solution (Fig.[1a](#Fig1)) therefore should reach an initial peak (the “preinhibition peak”) before blocker can enter the open channel. After the preinhibition peak, current should decrease as blocker transits from membrane to channel.
      ...
      0of WT, GluN1/2A(M630A), and GluN1/2A(M630W) NMDARs. Mutation GluN2A(M630A) decreased memantine MCI IC50(increased potency; Fig.[6e, g, h](#Fig6)), whereas mutation
      ...
      **a**Traditional channel block path. Top, charged memantine in the extracellular solution cannot access the deep site when the channel is closed. Bottom, charged memantine in the extracellular solution can transit to the deep site through the channel after agonists (A) bind and the channel gate opens.**b**MCI path. Top, uncharged memantine in the membrane cannot access the deep site when the membrane to channel fenestration is closed. Bottom, uncharged memantine in the membrane (shown here shortly after extracellular memantine has been washed away) can transit to the deep site through the gated fenestration after agonists bind and the fenestration opens.
      ...
      NMDAR MCI occurs when drugs enter the plasma membrane and, after NMDAR activation, transit from the membrane to the deep site, where they block the channel. We focused here on GluN1/2A receptors, but also demonstrated MCI of native NMDARs. We first tested the hypothesis that MCI depends on uncharged memantine, an idea suggested by our previous observation[8](#CR8)that occupation of the “second site” (from which memantine transits to the deep site during MCI) is voltage independent. We examined the dependence of MCI on pH because the concentration of uncharged (deprotonated) memantine increases as pH increases. Manipulation of pH has been used previously to modulate the protonation state of local anesthetics during inhibition of VGSCs[23](#CR23),[24](#CR24),[27](#CR27). We found that memantine MCI potency increased dramatically as pH was raised, even when pH was modified only during memantine application (Fig.[1](#Fig1)). We then examined MCI by two memantine derivatives custom-designed and synthesized for this study (Fig.[2](#Fig2)). Because of its quaternary ammonium, TMM is permanently charged. If MCI requires that uncharged channel blockers enter the membrane, TMM should not exhibit MCI. Similar use of a quaternary ammonium derivative was made to study fluoxetine inhibition of AMPARs[57](#CR57). DMM, in contrast, is a tertiary amine and exists in both charged and uncharged forms as a consequence of a pH-dependent equilibrium. We found that both TMM and DMM exhibit traditional channel block, whereas DMM, but not TMM, exhibits MCI. These data strongly support the conclusion that MCI depends on the uncharged form of memantine and its derivatives.
      ...
      Uncharged memantine is strongly hydrophobic: the LogP of memantine is \~3[27](#CR27),[35](#CR35)–[37](#CR37), indicating that uncharged memantine is \~1000-fold more soluble in octanol than water. The vast majority of uncharged memantine thus resides in membranes, suggesting that MCI may begin with occupation of the plasma membrane by uncharged memantine. We tested several predictions based on the hypothesis that the second site is the membrane. First, since the uncharged form of any channel blocker should be able to enter the membrane, we examined whether MCI is exhibited by channel blockers other than memantine (and DMM). We found that the previously described channel blockers PCP, MK-801, dextrorphan, and RL-208 all exhibit MCI (Fig.[3](#Fig3)). Thus, the second site appears non-specific, consistent with hypothesis that the plasma membrane is the second site. We also demonstrated that MK-801 exhibits MCI of native NMDARs in cultured cortical neurons (Fig.[3e](#Fig3)). Interestingly, inhibition of neuronal NMDARs by very high intracellular [MK-801]s is a widely-used approach for inhibiting postsynaptic NMDARs (e.g.[58](#CR58)–[62](#CR62)). We propose that inhibition of neuronal NMDARs by high intracellular MK-801 is a consequence of MCI.
      ...
      The NMDAR channel blocker ketamine is strongly lipophilic and has a molecular mass similar to that of PCP, but does not exhibit MCI[7](#CR7),[8](#CR8). This observation provides compelling evidence that our MCI protocol (Fig.[1](#Fig1)) precluded access of channel blockers to the deep site from the extracellular solution (see Methods). It is unknown why ketamine does not exhibit MCI. Possible explanations include: (a) the membrane-to-channel path may be less permeable to ketamine than the other channel blockers tested; (b) ketamine may bind with high affinity to a site along the membrane-to-channel path, preventing access to the deep site; (c) after entering the plasma membrane, ketamine may exit so rapidly that membrane concentration approaches 0 during the 1 s wash used to eliminate blockers from the extracellular solution.

      ---

      Title: Pharmacology of NMDA Receptors - Biology of the NMDA Receptor - NCBI Bookshelf
      URL: https://www.ncbi.nlm.nih.gov/books/NBK5282/
      Published: N/A
      Author: Daniel T. Monaghan, David E. Jane
      Highlights:
      The ion permeating channel represents an additional drug binding site, a binding site for NMDAR channel blockers such as PCP, MK-801, and memantine (Figure 12.3). The channel structure is structurally related to potassium channels wherein one hydrophobic segment forms a P loop within the membrane and this segment is flanked by transmembrane domains [22,23]. The P loop contributes to the selectivity filter of the channel. Near the tip of this loop is a critical asparagine residue that is important for the binding of several channel blockers. The other transmembrane domains contribute to the pore lining in the extracellular facing half of the membrane and thus can contribute to channel blocker binding.
      ...
      plasma membrane transporters and
      ...
      activity at other
      ...
      In the mammalian CNS, Mg2+ ions block NMDAR channels at resting membrane potentials [170]. This block is voltage-dependent. At depolarized membrane potentials, the channel block is relieved and ion fiux occurs [171,172]. Nonhomologous asparagine residues on NR1 and NR2 subunits produce a constriction in NMDAR ion channels, allowing Ca2+ but not Mg2+ ions to enter [173]. The low affinity binding site for Mg2+ ions is deep within the channel and NMDAR complexes containing NR2A or NR2B subunits have a higher affinity for Mg2+ than those containing NR2C or NR2D [66].
      ...
      A number of compounds block NMDAR channels by a use-dependent (channels must be opened via binding of glycine and glutamate to their respective binding sites for access to and dissociation from the binding site) and voltage-dependent mechanism [174,175]. These compounds include the dissociative anaesthetics, phencyclidine (PCP) and ketamine [176]. Site-specific mutagenesis revealed that an asparagine residue (N598) deep within the pore lining M2 segment of an NMDAR is important for channel blocking [177]. Since the mechanism of these channel blockers is use-dependent, the suggestion was made to use them to treat ischemia in which neurons degenerate due to excessive Ca2+ entry through NMDARs. This led to the development of selective high affinity NMDAR channel blockers such as MK-801, which is used widely as an experimental tool [178,179]. The kinetic action of channel blocking and unblocking exhibited by MK-801 depends on the NR2 subunit composition of the NMDAR complex. Slower channel blocking kinetics were observed for NR2C-containing receptors compared to those containing NR2A or NR2B [180]. This is consistent with the shorter open times of NR2C-containing receptors.
      ...
      High affinity channel blockers such as PCP mimic the symptoms of schizophrenia and have served as animal models of this disorder. Low affinity channel blockers such as memantine exhibit fast on-and-off kinetics and reduced tendencies to produce adverse reactions such as psychotomimetic effects [181]. Memantine is now in clinical use under the trade names Ebixa, Axura, and Namenda for treatment of cognitive deficits in moderate to severe Alzheimer’s disease. Although it is a channel blocker, memantine exhibits three- to five-fold greater potency for NR2C- versus NR2A-containing NMDARs but the relevance of this modest subunit selectivity to the improved therapeutic profile has not been established.

      ---

      Title: Inhibition of NMDA receptors and other ion channel types by membrane- ...
      URL: https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2025.1561956/full
      Published: 2025-04-30T00:40:06.000Z
      Author: N/A
      Highlights:
      N-methyl-D-aspartate receptors (NMDARs) are ligand-gated ion channels present at most excitatory synapses in the brain that play essential roles in cognitive functions including learning and memory consolidation. However, NMDAR dysregulation is implicated in many nervous system disorders. Diseases that involve pathological hyperactivity of NMDARs can be treated clinically through inhibition by channel blocking drugs. NMDAR channel block can occur via two known mechanisms. First, in traditional block, charged drug molecules can enter the channel directly from the extracellular solution after NMDAR activation and channel opening. Second, uncharged molecules of channel blocking drug can enter the hydrophobic plasma membrane, and upon NMDAR activation the membrane-associated drug can transit into the channel through a fenestration within the NMDAR. This membrane-associated mechanism of action is called membrane to channel inhibition (MCI) and is not well understood despite the clinical importance of NMDAR channel blocking drugs. Intriguingly, a hydrophobic route of access for drugs is not unique to NMDARs. Our review will address inhibition of NMDARs and other ion channels by membrane-associated drugs and consider how the path of access may affect a drug’s therapeutic potential.
      ...
      sharing a primary mechanism of action
      ...
      have a range of distinct
      ...
      Rogawski, 2000; Phillips et al., 2020). For example, memantine is the only NMDAR channel blocking drug approved by the FDA for the treatment of AD and is generally well tolerated. Phencyclidine (PCP) and ketamine are both NMDAR channel blocking drugs that act as dissociative anesthetics and are widely abused due in part to their hallucinogenic effects (Liu et al., 2016; Wallach and Brandt, 2018). The S (+) enantiomer of ketamine (esketamine, sold as Spravato) has been approved by the FDA for the treatment of major depressive disorder (MDD) (Swainson et al., 2019). Ketamine is unique amongst antidepressants because of its rapid action; whereas selective serotonin reuptake inhibitors (SSRIs) take weeks to months to become fully effective, ketamine’s antidepressant effects occur within hours (Yang et al., 2018; Ruberto et al., 2020). Besides binding to NMDARs, ketamine also has affinity at clinically relevant concentrations for hyperpolarization-activated cyclic nucleotide-gated (HCN) channels, as well as opioid, aminergic, and cholinergic receptors (Chen et al., 2009; Mion and Villevieille, 2013; Zorumski et al., 2016; Zanos et al., 2018) which may contribute to its clinical effects. In addition to blocking the NMDAR channel, ketamine may act allosterically at a site accessible from within the plasma membrane (Orser et al., 1997; Abbott et al., 2024). Furthermore, ketamine has several metabolites with additional effects (Zanos et al., 2016). Dextromethorphan and its metabolite dextrorphan are antitussive agents, although both produce hallucinogenic effects at high doses (McClure and Daniels, 2023). Amantadine is another clinically relevant NMDAR channel blocking drug that is used to treat Parkinson’s disease (Kornhuber et al., 1991; Lupp et al., 1992; Blanchet et al., 2003). Although these drugs are all NMDAR channel blockers, the specific molecular mechanisms underlying the range of distinct clinical effects they induce remain poorly understood.
      ...
      There are two known routes through which NMDAR channel blocking drugs can access their binding site (the “deep site”) near the N-site at the tips of the M2 re-entrant loops (Kashiwagi et al., 2002; Chen and Lipton, 2005; Phillips et al., 2020). The most well studied route is “traditional” channel block, which occurs when a channel blocking drug enters the open NMDAR channel directly from the extracellular solution (Figure 2A). For many years, this was the only known route of access to the deep site for channel blocking drugs. However, in 2022 a second route of entry to the deep site was described (Wilcox et al., 2022). Inhibition via this second route, called membrane to channel inhibition (MCI), involves access of channel blocking drug to the deep site from within the plasma membrane. In MCI, uncharged molecules of channel blocking drug first enter the plasma membrane. Receptor activation then allows transit of blocker molecules through a gated, lateral fenestration in the NMDAR into the deep site (Figure 2B). MCI is exhibited by most tested NMDAR channel blocking drugs, including memantine, MK-801, PCP, and dextrorphan (Wilcox et al., 2022). The notable exception is ketamine, which is the only NMDAR channel blocking drug we have tested so far that does not appear to exhibit MCI (Kotermanski et al., 2009).
      ...
      Although the same channel blocking site is involved in both traditional block and MCI, drugs may have different attributes when accessing the deep site through distinct paths. For example, all tested channel blocking drugs have much lower affinity when acting through MCI than through traditional block. Memantine has an IC50 of approximately 1.5 μM at −65 mV when acting through traditional block on GluN1/2A receptors expressed in tsA201 cells (Glasgow et al., 2017); similar values have been observed in a variety of other preparations (Chen et al., 1992; Parsons et al., 1995; Blanpied et al., 1997; Sobolevsky et al., 1998). However, memantine has an IC50 of 71 μM at −65 mV when acting through MCI on GluN1/2A receptors expressed in tsA201 cells (Wilcox et al., 2022). The small amount of uncharged channel blocking drug typically present in physiological solution likely contributes to memantine’s lower affinity when acting through MCI. At physiological pH, all drugs tested thus far exist primarily in a charged state, and entry of charged drug molecules into the membrane is energetically unfavorable. For example, at a pH of 7.2, only about 0.06% of memantine is uncharged due to its pKa of approximately 10.4. Thus, if 100 μM memantine is in aqueous solution at a pH of 7.2, the aqueous concentration of uncharged memantine is approximately 60 nM. Memantine MCI nevertheless reduces NMDAR mediated current by approximately 40% under these conditions because uncharged memantine, which is very hydrophobic, accumulates at vastly higher concentrations within the membrane (Wilcox et al., 2022). Hypothetically, a drug that is predominantly uncharged in aqueous solution and therefore preferentially resides in the plasma membrane may inhibit with greater potency through MCI than through traditional block.
      ...
      It is unknown why ketamine does not appear to exhibit MCI. Even 500 µM ketamine, about 1,000 times greater than the IC50 of ketamine for traditional block of GluN1/2A receptors, does not produce observable MCI (Kotermanski et al., 2009). Ketamine has a lower pKa than memantine (7.5 versus 10.4), meaning that at equivalent total aqueous concentrations, there is a higher concentration of uncharged ketamine than uncharged memantine in aqueous solution. Since uncharged drug is much more likely to enter the plasma membrane, a drug with lower pKa should hypothetically cause stronger MCI given similar affinities and ability to traverse the fenestration. One hypothesis is that ketamine cannot transit through the fenestration due to unfavorable interactions with fenestration-lining amino acid residues, preventing it from accessing the deep site from the plasma membrane. Given that the protocol for measuring MCI currently depends on a 1-s wash (see Section 2.
      ...
      ), an alternative hypothesis is that the rate of ketamine exit from the membrane is so fast that MCI is not measurable using established protocols. Further experiments are needed to investigate
      ...
      micromolar
      ...
      with a logP of
      ...
      lipid membrane compared to
      ...
      fenestration

      ---

      Title: Structural insights into binding of therapeutic channel blockers in NMDA receptors
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10075384/
      Published: N/A
      Author: N/A
      Highlights:
      Excitatory signaling mediated by*N*-methyl-D-aspartate receptor (NMDAR) is critical for brain development and function as well as for neurological diseases and disorders. Channel blockers of NMDARs are of medical interest due to their potential for treating depression, Alzheimer’s disease, and epilepsy. However, precise mechanisms underlying binding and channel blockade have remained limited due to challenges in obtaining high-resolution structures at the binding site within the transmembrane domains. Here, we monitor the binding of three clinically important channel blockers: phencyclidine, ketamine, and memantine in GluN1-2B NMDARs at local resolutions of 2.5 to 3.5 Åaround the binding site using single-particle electron cryo-microscopy, molecular dynamics simulations, and electrophysiology. The channel blockers form different extents of interactions with the pore-lining residues, which control mostly off-speeds but not on-speeds. Our comparative analyses of the three unique NMDAR channel blockers provide a blueprint for developing therapeutic compounds with minimal side effects.
      ...
      Excitatory neurotransmission and cellular signaling mediated by*N*-methyl-D-aspartate receptors (NMDARs) are fundamental to brain function and development. The majority of these receptors are hetero-tetrameric ion channels composed of GluN1 and GluN2 (A-D) subunits, which bind to glycine and the glutamate neurotransmitter at their respective ligand-binding domains (LBDs) and open their transmembrane channels upon relief of Mg2+block by membrane depolarization[1](#R1),[2](#R2). The high influx of calcium resulting from the channel opening facilitates cellular signaling for neuroplasticity, which in turn, results in high order brain functions including learning and memory[3](#R3)–[5](#R5). Dysfunctional NMDARs are increasingly implicated in neurological diseases and disorders including schizophrenia, Alzheimer’s disease, depression, epilepsy, and ischemic injury associated with stroke[6](#R6).
      ...
      Channel blockers for NMDARs have been studied historically in the broad field of clinical neuropharmacology due to their effectiveness in altering neurological conditions and in treatment[7](#R7). Phencyclidine (PCP) and S-(+)-ketamine were reported to induce psychotomimetic effects similar to schizophrenia as early as 1959[8](#R8)and were later characterized as inhibitors of NMDAR channels[9](#R9)–[11](#R11). Memantine is a channel blocker with a tricyclodecane backbone, which is unrelated to the chemical backbones of PCP and S-(+)-ketamine ([Fig. 1a](#F1)) and unlike PCP and S-(+)-ketamine, it does not show any abuse potential[12](#R12). Indeed, memantine has been approved by the FDA for treatment of Alzheimer’s disease ([https://www.accessdata.fda.gov/drugsatfda\_docs/nda/2003/21-487\_namenda.cfm](https://www.accessdata.fda.gov/drugsatfda_docs/nda/2003/21-487_namenda.cfm)) and is under a clinical trial for treatment of epileptic encephalopathy caused by overactivation of NMDARs. S-(+)-ketamine has recently been FDA approved for the treatment of major depression despite side effects including sedation and dissociation[13](#R13),[14](#R14)([https://www.accessdata.fda.gov/drugsatfda\_docs/nda/2019/211243Orig1s000TOC.cfm](https://www.accessdata.fda.gov/drugsatfda_docs/nda/2019/211243Orig1s000TOC.cfm)) whereas PCP shows anti-depressant effects but with stronger psychotomimetic effects[14](#R14). These three classic NMDAR blocker compounds show different potency and kinetics of dissociation[15](#R15), factors of which likely contribute to the distinct psychotomimetic effects of these drugs. However, insights into molecular elements that control different potencies and dissociation rates of the channel blockers are limited due to the lack of studies that experimentally compare binding modes at high resolution.
      ...
      To gain a comprehensive understanding of the channel blocker binding site, we obtained cryo-EM structures of agonist-bound GluN1-2B NMDAR (glycine and glutamate to GluN1 and GluN2B, respectively) in the presence of PCP (agonist-PCP-bound), S-(+)-ketamine (agonist-ketamine-bound), and memantine (agonist-memantine-bound) or in the absence of channel blockers (agonist-bound). We modified prior protocols[21](#R21)to improve the cryo-EM density maps especially around the TMDs where channel blockers bind. Specifically, we worked on the GluN1a-2B NMDAR that lacks the exon5-motif in GluN1[21](#R21)to minimize protein conformational heterogeneity. The GluN1a-2B NMDAR protein was expressed in Sf9 insect cells using the EarlyBac method[30](#R30), which allows expression of NMDAR proteins without a need to add channel blockers into culture media, a key necessity here for the precise execution of structural analyses of specific channel blockers. In contrast, expression using mammalian cell culture requires the presence of channel blockers in culture media to reduce toxicity caused by NMDAR over-activation[29](#R29). We included modest concentrations of the blocker compounds (2, 50 and 100 μM of PCP, S-(+)-ketamine and memantine, respectively) and agonists (1 mM of glycine and glutamate) in the purification buffer for the size-exclusion chromatography step at room temperature to facilitate binding while preventing protein aggregation caused by addition of excessive amounts of channel blocker. Finally, large datasets containing more than half a million particles were subjected to single-particle analyses with extensive 3D classification and focused classification around the TMDs to maximally resolve the channel blocker binding site ([Extended Data Fig. 1](#F8)–[3](#F10)). This workflow resulted in structures with overall resolution ranging from 2.97 to 4.30 Å([Table 1](#T1)) with clearly visible agonist density in the LBDs consistent with crystal structures of the isolated LBDs ([Extended Data Fig. 2](#F9))[31](#R31),[32](#R32). However, most importantly, all four structures have a local resolution of 2.5 –3.5 Åaround the M2 and M3 helices of the TMDs where the channel blockers bind; therefore, channel blocker binding can be monitored much more reliably than in previous studies. Also importantly, the structures were refined without any symmetry imposition, to allow capture of the asymmetric features of the channel blockers. All four structures obtained based on the selected particles reside in the conformation similar to non-active1 with the closed channel where the two GluN1a-2B LBD heterodimers and the GluN1a-2B ATD interfaces[33](#R33),[34](#R34)are arranged in the manner that does not generate sufficient tension in the LBD-TMD linker region for channel gating ([Extended Data Fig. 2d](#F9))[18](#R18),[21](#R21).
      ...
      , while the channel blockers may physically block the pore they also interact with the Thr-ring to favor closure of the channel gate (SYTANLAAF motif) ([Fig. 6c](#F6)) as proposed previously by electrophysiology[39](#R39). This model is also supported by our electrophysiological assessment of the GluN1a WT/GluN2B-Thr647Ser mutant channel with weaker hydrophobic interactions where faster off-speeds of channel blockers were observed. Indeed, the majority of the
      ...
      5 BAPTA, 2 Na-ATP, 0.3 Na-GTP, pH to 7.35 with CsOH. The external solution contained (in mM) 150 NaCl, 3 KCl, 10 HEPES, 0.01 EDTA, 0.5 mM CaCl2, 11 D-mannitol, pH to 7.4 with NaOH. Data were collected on an AxoPatch 200B patch clamp amplifier (Axon Instruments), filtered at 2 kHz (Frequency Devices), and digitized with a Digidata 1550B digitizer using a sampling frequency of 10 kHz. Recordings were analyzed using Clampex 11.0 software (Axon Instruments). A rapid solution exchanger (RSC-200, Bio-logic) was used to perfuse cells. Patches were held at −80 mV and typically exposed to glutamate several times until a consistent peak current was observed. Tau values were obtained by fitting recordings to a single-term exponential equation, and IC50values were calculated in the Origin8 Pro software.
```
/answer ddffd0af-a3a4-4c7e-928c-67b64781113a allow
Control Request:
```yaml
id: 6a9c8c35-38cb-4410-ae3f-195514b99322
toolName: web-search-exa
arguments:
  query: diphenhydramine alpha-2 adrenergic receptor Ki nM antagonist potency
  reason: Get precise alpha2-adrenergic Ki of DPH
```
/answer 6a9c8c35-38cb-4410-ae3f-195514b99322 allow
ReasoningToken: 749
Control Request:
```yaml
id: 0394e100-3822-4135-9d46-85b611e76c8b
result:
  structuredContent:
    content: |-
      Title: Diphenhydramine · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/diphenhydramine/
      Published: N/A
      Author: N/A
      Highlights:
      | Histamine H1 receptor | P35367 | HRH1 | 7.83 | Ki | 14.79 nM | CHEMBL_ACT_7846197 |
      ...
      | Histamine H1 receptor | P35367 | HRH1 | 7.7 | Ki | 20 nM | CHEMBL_ACT_7681414 |
      ...
      amine H1
      ...
      | P35367 | HRH1 | 7.5 | AC50 | 32 nM | CHEMBL_ACT_25212872
      ...
      6.94 |
      ...
      | Alpha-1A adrenergic receptor | P35348 | ADRA1A | 5.2 | AC50 | 6312 nM | CHEMBL_ACT_25138129 |
      | Alpha-2B adrenergic receptor | P18089 | ADRA2B | 5.16 | AC50 | 7000 nM | CHEMBL_ACT_25144052 |
      ...
      | Alpha-2A adrenergic receptor | P08913 | ADRA2A | 5.02 | AC50 | 9548 nM | CHEMBL_ACT_25156804 |

      ---

      Title: The affinity and selectivity of α‐adrenoceptor antagonists, antidepressants and antipsychotics for the human α2A, α2B, and α2C‐adrenoceptors and comparison with human α1 and β‐adrenoceptors
      URL: https://doi.org/10.1002/prp2.936
      Published: 2022-02-27T00:00:00.000Z
      Author: Richard G. W. Proudman, Juliana Akinaga, Jillian G. Baker
      Highlights:
      subtype affinity is difficult due to significant species and methodology differences in published studies. Here, 3 H-rauwolscine whole cell binding was used to determine the affinity and selectivity of 99 α-antagonists (including antidepressants and antipsychotics) in CHO cells expressing human α2A, α2B, or α2C-adrenoceptors, using an identical method to β and α1-adrenoceptor measurements, thus allowing direct human receptor comparisons. Yohimbine, RX821002, RS79948, and atipamezole are high affinity non-selective α2-antagonists. BRL44408 was the most α2A-selective antagonist, although its α1A-affinity (81 nM) is only 9-fold greater than its α2C-affinity. MK-912 is the highest-affinity, most α2C-selective antagonist (0.15 nM α2C-affinity) although its α2C-selectivity is only 13-fold greater than at α2A. There are no truely α2B-selective antagonists. A few α-ligands with significant β-affinity were detected, for example, naftopidil where its clinical α1A-affinity is only 3-fold greater than off-target β2-affinity.
      ...
      component response in CHO
      ...
      C cells (Figure
      ...
      cells were too low affinity for
      ...
      . 3
      ...
      ate abolished the higher affinity components and reduced the affinity of
      ...
      at all three
      ...
      the affinity of the ligand interacting
      ...
      the receptor (as in
      ...
      ohimbine and RX8
      ...
      1002 were confirmed as high affinity antagonists at all three subtypes. Both compounds had a lower affinity at α2B-adrenoceptors than at α2A or α2C, in keeping with some other studies (both in cell lines, 24, 29 and in tissues. 7, 30, 39, 40 Other compounds with high affinity at all 3 subtypes were: atipamezole 30, 39 and RS79948 27 and should thus be regarded as non-selective α2ligands. Lisuride has a high affinity across many different receptor subtypes. 41, 42 L44408 (65 nM at α2A) was the most α2A-adrenoceptor selective ligand in keeping with 22, 24, 26, 43 however although it was 60-fold selective for α2A over α2B, BRL44408's selectivity for α2A over α2C-adrenoceptors was only 9-fold. Although S32212 and ARC239 were 15-to 21-fold selective for the α2B over the α2Aadrenoceptor, their α2B versus α2C is marginal (less than 5-fold), in keeping with 21, 24, 28, 29, 43, 44 and thus there are no α2B-selective ligands. Within the α2-adrenoceptors, JP1302 was the overall most α2C-selective ligand with an α2C-selectivity of 43 and 65 over α2A and α2B respectively, in keeping with 20 however its affinity (120 nM at α2C) was a little lower than previously reported (16-28 nM 20 ).
      ...
      Caffinity than α2A or α2B respectively)
      ...
      in keeping with previous studies. 24, 2
      ...
      , 2
      ...
      43
      ...
      (25
      ...
      The findings of these studies are therefore discussed as a whole, in comparison with other literature findings. BRL44408 is the best α2A selective antagonist although its affinity for α2A is only a modest 9-fold greater its α2C affinity. MK-912 is the best α2C-antagonist (0.15 nM α2C-affntiy) although again its α2C selectivity is only modest (13-fold greater than α2A). JP1302 (α2C affinity 120 nM) has an α1A-adrenoceptor affinity of 617 nM, only 5-fold less, so is not a truly α2C-selective ligand. CGP20712A (β1) and ICI118551 (β2) are also highly selective antagonists with minimal α-affinity. There are no truly α1B or α2B selective antagonists. Figure 4 shows the affinity (log K D values) of the most selective ligand at each adrenoceptor subtype (i.e., BRL44408 for α2A, S32212 for α2B and MK-912 for α2C) along with the single most selective antagonists at the other adrenoceptors and demonstrates that the α2-adrenoceptors fall behind α1 and β with regards to availability of highly subtypeselective ligands.
      ...
      Inhibition of 3 H-rauwolscine binding to whole cells by BRL44408 (A-C), S32212 (D-F) or MK-912 (G-I) to CHO-α2A cells (A, D, G), CHO-α2B cells (B, E, H) or CHO-α2C cells (C, F, I). Bars represent total 3 H-rauwolscine and non-specific binding (determined in the presence of 10μM RX821002. The concentration of 3 H-rauwolscine was (A) 0.99 nM, (B) 0.99 nM, (C) 0.99 nM, (D) 0.88 nM, (E) 0.88 nM, (F) 0.88 nM, (G) 0.86 nM, (H) 0.86 nM, and (I) 0.88 nM. Data points are mean ±s.e.mean of triplicate determinations TA B L E 2 Log K D values obtained from inhibition of 3 H-rauwolscine binding by adrenoceptor antagonists to the human α2A, α2B, and α2C-adrenoceptors in living cells. Values represent mean ±s.e.mean of n separate experiments. Selectivity ratios are also given where a ratio of 1 demonstrates no selectivity for a given receptor subtype over another. Thus BRL44408 has 60fold higher affinity for the α2A than the α2B-adrenoceptor. Compounds are arranged in order of α2A-selectivity.
      ...
      8 has ~1
      ...
      -selectivity. = apparent affinity.
      ...
      non-specific binding
      ...
      oligand binding and non-specific binding as determined in
      ...
      presence of 10μM RX821
      ...
      1 and β2 cells). The concentration
      ...
      and was (
      ...
      ) 0.54 nM, (B) 0.5
      ...
      nM, (D) 0.77 nM, (E) 1.0
      ...
      , (F) 0.50 nM, (
      ...
      ) 0.72
      ...
      ) 0.94 nM and (
      ...
      ) 0.72 nM. Data points are mean
      ...
      51,5
      ...
      -affinity
      ...
      affinity to the α2-antagonist idazoxan and similar values to those obtained in human α2
      ...
      receptors (79-126 nM) in,51who also reported lower affinity at human α
      ...
      and unmeasurable affinity at human β1 or β2-adrenoceptors. Of no 51also reported similar values for mirtazapine for human and rat receptors, TA B L E 4 Log K D values of antipsychotics binding to the human α2A, α2B, and α2C-adrenoceptors. Va ues represent mean ±s.e.mean of n separate experiments. Selectivity ratios are also given where a ratio of 1 demonstrates no selectivity for a given receptor subtype over another. Compounds are arranged in order of α2A-selectivity. Affinity measurements | Selectivity ratios Ligand | Log K D α2A | n | Log K D α2B | n | Log K D α2C | n | α2A vs α2B | α2A vs α2C | α2B vs α2C First-generation antipsychotics sulpiride | -4.50 ± 0.02 | 5 | -4.37 ± 0.06 | 5 | -4.67 ± 0.07 | 5 | 1.3 | 1.5 | 2.0 haloperidol | -5.38 ± 0.06 | 5 | -5.53 ± 0.10 | 5 | -5.77 ± 0.05 | 5 | 1.4 | 2.5 | 1.7 flupenthixol | -6.10 ± 0.12 | 5 | -6.28 ± 0.13 | 5 | -6.88 ± 0.14 | 5 | 1.5 | 6.0 | 4.0 pimozide | -5.76 ± 0.12 ep | 5 | -6.30 ± 0.10 | 5 | -6.84 ± 0.05 | 5 | 3.5 | 12.0 | 3.5 trifluoperazine | -5.60 ± 0.05 | 5 | -6.22 ± 0.12 | 5 | -6.20 ± 0.06 | 5 | 4.2 | 4.0 | 1.0 prochlorperazine | -5.78 ± 0.02 app | 6 | -6.46 ± 0.11 | 6 | -6.31 ± 0.09 | 6 | 4.8 | 3.4 | 1.4 chlorpromazine | -5.65 ± 0.13 app | 6 | -6.60 ± 0.12 | 6 | -5.93 ± 0.11 | 6 | 8.9 | 1.9 | 4.7 perphenazine | -6.00 ± 0.06 | 6 | -7.16 ± 0.05 | 6 | -6.83 ± 0.04 | 5 | 14.5 | 6.8 | 2.1 Second-generation antipsychotics amisulpiride | -5.11 ± 0.09 app | 5 | -4.69 ± 0.13 app | 5 | -5.57 ± 0.07 | 5 | 2.6 | 2.9 | 7.6 aripirazole | -6.68 ± 0.08 | 5 | -6.54 ± 0.08 | 6 | -7.23 ± 0.14 | 5 | 1.4 | 3.5 | 4.9 sertindole | -5.95 ± 0.06 | 5 | -5.81 ± 0.07 | 5 | -6.17 ± 0.03 | 5 | 1.4 | 1.7 | 2.3 olanzapine | -5.59 ± 0.05 | 5 | -5.47 ± 0.06 | 5 | -5.86 ± 0.02 | 5 | 1.3 | 1.9 | 2.5 paliperidone | -7.12 ± 0.04 | 5 | -7.26 ± 0.05 | 5 | -7.84 ± 0.03 | 5 | 1.4 | 5.2 | 3.8 risperidone | -7.30 ± 0.09 | 5 | -7.47 ± 0.08 | 5 | -8.04 ± 0.03 | 5 | 1.5 | 5.5 | 3.7 ziprasidone | -6.36 ± 0.11 | 5 | -6.59 ± 0.08 | 5 | -6.77 ± 0.08 | 5 | 1.7 | 2.6 | 1.5 clozapine | -5.86 ± 0.08 app | 5 | -6.20 ± 0.05 | 5 | -6.87 ± 0.08 | 5 | 2.2 | 10.2 | 4.7 l
      ...
      idone | -6.67 ± 0.05 | 5 | -7.36 ± 0.06 | 5
      ...
      -7.34
      ...
      0.03 | 5 |
      ...
      -5.
      ...
      17,52Here, first generation
      ...
      -21 ) α2A 600 nM, α2B 43
      ...
      , and α2C 260 nM ( 3 H-RX821002 membrane binding for human receptors expressed in CHO cells, 29 ) α2A 1008
      ...
      , α2B 34
      ...
      , and α2C 85 nM ( 3 H-RX82
      ...
      002 membrane binding to human
      ...
      ( 3 H-RX821002 membrane binding to human platelets, 23 ) to α2A 4169
      ...
      and α2C 1413
      ...
      selectivity for α2C over the other α2-subtypes. For example, chlorpromazine
      ...
      affinities of α2

      ---

      Title: diphenhydramine | Ligand Activity Charts | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandActivityRangeVisForward?ligandId=1224
      Published: N/A
      Author: N/A
      Highlights:
      #### diphenhydramine [Ligand Id: 1224] activity data from GtoPdb and ChEMBL
      ...
      | ChEMBL ligand: CHEMBL657(Difenhidramina, Diphenhdyra, Diphenhydramine, Restamin) |
      | --- |

      ---

      Title: diphenhydramine | Ligand page | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=1224
      Published: N/A
      Author: N/A
      Highlights:
      Comment: Diphenhydramine has anti-histamine action.

      ---

      Title: Diphenhydramine: Uses, Interactions, Mechanism of Action | DrugBank Online
      URL: https://web.archive.org/web/20240922051631/https:/go.drugbank.com/drugs/DB01075
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine - perhaps known most commonly as its brand name formulation Benadryl - is a first-generation H1 receptor antihistamine that is used extensively for the treatment of seasonal allergies, insect bites and stings, and rashes 9,10,11,17. However, it also has antiemetic, antitussive, hypnotic, and antiparkinson properties 11,16. As histamine receptors exist both peripherally and in the central nervous system, diphenhydramine has been shown to cause sedation due to its competitive antagonism of histamine H1 receptors within the central nervous system 9,10,11,17,5. While its use in allergy therapy can sometimes fall out of favor due to its sedative effect, diphenhydramine has been repurposed for use within many non-prescription over-the-counter sleep aids and cough-and-cold medications that have been marketed for "night time" use 9,12,13.
      ...
      Diphenhydramine is a first-generation histamine H1 receptor antagonist (H1 antihistamine) that is widely available as a non-prescription, over-the-counter (OTC) medication. As an OTC medication, diphenhydramine is typically formulated as tablets and creams indicated for use in treating sneezing, runny nose, itchy/watery eyes, itching of nose or throat, insomnia, pruritis, urticaria, insect bites/stings, allergic rashes, and nausea 9,10,11,17,5.
      ...
      Diphenhydramine has anti-histaminic (H1-receptor), anti-emetic, anti-vertigo and sedative and hypnotic properties 12. The anti-histamine action occurs by blocking the spasmogenic and congestive effects of histamine by competing with histamine for H1 receptor sites on effector cells, preventing but not reversing responses mediated by histamine alone 12. Such receptor sites may be found in the gut, uterus, large blood vessels, bronchial muscles, and elsewhere 12. Anti-emetic action is by inhibition at the medullary chemoreceptor trigger zone 12. Anti-vertigo action is by a central antimuscarinic effect on the vestibular apparatus and the integrative vomiting center and medullary chemoreceptor trigger zone of the midbrain 12.
      ...
      Diphenhydramine predominantly works via the antagonism of H1 (Histamine 1) receptors 9,10,11,17,5. Such H1 receptors are located on respiratory smooth muscles, vascular endothelial cells, the gastrointestinal tract (GIT), cardiac tissue, immune cells, the uterus, and the central nervous system (CNS) neurons 9,10,11,17,5. When the H1 receptor is stimulated in these tissues it produces a variety of actions including increased vascular permeability, promotion of vasodilation causing flushing, decreased atrioventricular (AV) node conduction time, stimulation of sensory nerves of airways producing coughing, smooth muscle contraction of bronchi and the GIT, and eosinophilic chemotaxis that promotes the allergic immune response 9,10,11,17,5.
      ...
      Ultimately, diphenhydramine functions as an inverse agonist at H1 receptors, and subsequently reverses effects of histamine on capillaries, reducing allergic reaction symptoms 9,10,11,17,5. Moreover, since diphenhydramine is a first-generation antihistamine, it readily crosses the blood-brain barrier and inversely agonizes the H1 CNS receptors, resulting in drowsiness, and suppressing the medullary cough center 9,10,11,17,5.
      ...
      Furthermore, H1 receptors are similar to muscarinic receptors 9,10,11,17,5. Consequently, diphenhydramine also acts as an antimuscarinic 9,10,11,17,5. It does so by behaving as a competitive antagonist of muscarinic acetylcholine receptors, resulting in its use as an antiparkinson medication 9,10,11,17,5.

      ---

      Title: DIPHENHYDRAMINE HYDROCHLORIDE
      URL: https://drugs.ncats.io/drug/TC2D6JAD40
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine is an antihistamine which is used in the combination with naproxen sodium for the relief of occasional sleeplessness when associated with minor aches and pains. Diphenhydramine has a role nighttime sleep-aid and naproxen sodium is a pain reliever. In addition, diphenhydramine used in relieving symptoms in patients with moderate-to-severe seasonal allergic rhinitis. Diphenhydramine acts as an antagonist of histamine H1 receptor. Besides, was shown potential to repurpose diphenhydramine as an anti-melanoma therapeutic agent, it induces melanoma cell apoptosis by suppressing STAT3/MCL-1 survival signaling pathway.
      ...
      Histamine H1 receptor
      ...
      2849
      ...
      amine H1
      ...
      | Primary Target | Pharmacology | Condition | Potency |
      | --- | --- | --- | --- |
      | 7.9 null [pKi] |
      | 2.7 µM [IC50] |
      ...
      | Target | Modality | Activity | Metabolite | Clinical evidence | weak [IC50 11 uM] |
      | --- | --- | --- | --- | --- | --- |
      | yes [IC50 15 uM] |
      | yes [IC50 3.4 uM] |
      | yes [IC50 695 uM] |
      | yes [Ki 266.5 uM] |
      | yes [Ki 87 uM] |

      ---

      Title: Ligand efficacy and potency at recombinant alpha2 adrenergic receptors: agonist-mediated [35S]GTPgammaS binding
      URL: https://pubmed.ncbi.nlm.nih.gov/9605427/
      Published: N/A
      Author: N/A
      Highlights:
      Alpha-2 adrenergic receptors (alpha2 AR) mediate incorporation of guanosine 5'-O-(gamma-thio)triphosphate ([35S]GTPgammaS) into isolated membranes via receptor-catalyzed exchange of [35S]GTPgammaS for GDP. In the current study, we used [35S]GTPgammaS incorporation to characterize the intrinsic activity and potency of agonists and antagonists at the cloned mouse alpha2a/d and human alpha2a, alpha2b, and alpha2c ARs. Full agonists increased [35S]GTPgammaS binding to membranes by 2- to 3-fold. Antagonists did not increase [35S]GTPgammaS binding but competitively inhibited agonist-stimulated [35S]GTPgammaS binding. Compounds with intrinsic activities less than that of the full agonists norepinephrine (NE) or epinephrine (EPI) were capable of antagonizing agonist-stimulated [35S]GTPgammaS binding. The agonistic properties of a number of alpha2 AR ligands were characterized at each alpha2 AR subtype. The rank order of agonist potency for selected compounds at the human receptors (with intrinsic activity compared with NE, defined as 1.0) was: alpha2a: Dexmedetomidine (0.73) > guanabenz (0.38) > UK-14304 (1.02) > clonidine (0.32) > ST-91 (0.63) > NE (1.00). alpha2b: Dexmedetomidine (1.10) > clonidine (0.18) > guanabenz (0.71) > NE (1.00) > ST-91 (0.44) > UK-14304 (0.59). alpha2c: Dexmedetomidine (1.03) > NE (1.00) > UK-14304 (0.75) > ST-91 (0.32) > or = clonidine (0.23) >> guanabenz (0). This report provides a functional characterization of adrenergic receptor ligands at human and mouse alpha2a/d AR. It also illustrates the utility of [35S]GTPgammaS incorporation as a functional marker of receptor activation.

      ---

      Title: Actions of alpha2 adrenoceptor ligands at alpha2A and 5-HT1A receptors: the antagonist, atipamezole, and the agonist, dexmedetomidine, are highly selective for alpha2A adrenoceptors - PubMed
      URL: https://pubmed.ncbi.nlm.nih.gov/9750005/
      Published: N/A
      Author: N/A
      Highlights:
      This study examined the activity of chemically diverse alpha2 adrenoceptor ligands at recombinant human (h) and native rat (r) alpha2A adrenoceptors compared with 5-HT1A receptors. First, in competition binding experiments at h alpha2A and h5-HT1A receptors expressed in CHO cells, several compounds, including the antagonists 1-(2-pyrimidinyl)piperazine (1-PP), (+/-)-idazoxan, benalfocin (SKF 86466), yohimbine and RX 821,002, displayed preference for h alpha2A versus h5-HT1A receptors of only 1.4-, 3.6-, 4-, 10- and 11-fold, respectively (based on differences in pKi values). Clonidine, brimonidine (UK 14304), the benzopyrrolidine fluparoxan and the guanidines guanfacine and guanabenz exhibited intermediate selectivity (22- to 31-fold) for h alpha2A receptors. Only the antagonist atipamezole and the agonist dexmedetomidine (DMT) displayed high preference for alpha2 adrenoceptors (1290- and 91-fold, respectively). Second, the compounds were tested for their ability to induce h5-HT1A receptor-mediated G-protein activation, as indicated by the stimulation of [35S]GTPgammaS binding. All except atipamezole and RX 821,002 exhibited agonist activity, with potencies which correlated with their affinity for h5-HT1A receptors. Relative efficacies (Emax values) were 25-35% for guanabenz, guanfacine, WB 4101 and benalfocin, 50-65% for 1-PP, (+/-)-idazoxan and clonidine, and over 70% for fluparoxan, oxymetazoline and yohimbine (relative to 5-HT = 100%). Yohimbine-induced [35S]GTPgammaS binding was inhibited by the selective 5-HT1A receptor antagonist WAY 100,635. In contrast, RX 821,002 was the only ligand which exhibited antagonist activity at h5-HT1A receptors, inhibiting 5-HT-stimulated [35S]GTPgammaS binding. Atipamezole, which exhibited negligeable affinity for 5-HT1A receptors, was inactive. Third, the affinities for r alpha2A differed considerably from the affinities for h alpha2A receptors whereas the affinities for r5-HT1A differed much less from the affinities for h5-HT1A receptors. This affected markedly the affinity ratios of certain compounds. For example, (+/-)-idazoxan was only 3.6-fold selective for h alpha2A versus h5-HT1A but 51-fold selective for r alpha2A versus r5-HT1A receptors. Conversely, yohimbine was tenfold selective for h alpha2A versus h5-HT1A adrenoceptors but 4.2-fold selective for r alpha2A versus r5-HT1A receptors. Nevertheless, both atipamezole and DMT were highly selective for both rat and human alpha2A versus rat or human 5-HT1A receptors. In conclusion, these data indicate that: (1) the agonist DMT and the antagonist atipamezole are the ligands of choice to distinguish alpha2-mediated from 5-HT1A-mediated actions, whilst several of the other compounds show only low or modest selectivity for alpha2A over 5-HT1A receptors; (2) caution should be exercised in experimental and clinical interpretation of the actions of traditionally employed alpha2 ligands, such as clonidine, yohimbine and (+/-)-idazoxan, which exhibit marked agonist activity at 5-HT1A receptors.

      ---

      Title: Dimenhydrinate · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/dimenhydrinate/
      Published: N/A
      Author: N/A
      Highlights:
      | Alpha-2A adrenergic receptor | P08913 | ADRA2A | 5.79 | Ki | 1617 nM | CHEMBL_ACT_7704996 |
      ...
      | Alpha-2B adrenergic receptor | P18089 | ADRA2B | 5.6 | Ki | 2491 nM | CHEMBL_ACT_7704998 |
      ...
      | Alpha-2
      ...
      | P08913 | ADRA2A | 5.37 | IC50 | 4313 nM | CHEMBL_ACT_7704995 |

      ---

      Title: Cyproheptadine: targets, mechanism, indications & safety · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/cyproheptadine/
      Published: N/A
      Author: N/A
      Highlights:
      | Alpha-2B adrenergic receptor |
      ...
      ADRA2
      ...
      CHEMBL_ACT
      ...
      08665 |
      ...
      | Alpha-2B adrenergic receptor | P18089 | ADRA2B | 7.42 | IC50 | 38 nM | CHEMBL_ACT_7708664 |
      ...
      | Alpha-2
      ...
      | DIPHENHYDRAMINE | ChEMBL | Phase 4 (approved) | ADRA1A, HRH1, HTR6 |
```
/answer 0394e100-3822-4135-9d46-85b611e76c8b allow
Control Request:
```yaml
id: fb7ea555-9eeb-40da-aa25-76b1c3d4d901
toolName: web-search-exa
arguments:
  query: diphenhydramine voltage-gated calcium channel Cav block IC50 nM smooth muscle neuronal
  reason: Get precise calcium channel potency of DPH
```
/answer fb7ea555-9eeb-40da-aa25-76b1c3d4d901 allow
Control Request:
```yaml
id: 00c03e7a-787e-4dbb-9ce8-d70827d05cf5
result:
  structuredContent:
    content: |-
      Title: Research report Block of sodium currents in rat dorsal root ganglion neurons by diphenhydramine
      URL: https://www.sciencedirect.com/science/article/abs/pii/S0006899300028602?via%3Dihub
      Published: N/A
      Author: N/A
      Highlights:
      To elucidate the local anesthetic mechanism of[diphenhydramine](https://www.sciencedirect.com/topics/neuroscience/diphenhydramine), its effects on tetrodotoxin-sensitive (TTX-S) and tetrodotoxin-resistant (TTX-R) sodium currents in rat[dorsal root ganglion](https://www.sciencedirect.com/topics/neuroscience/dorsal-root-ganglion)(DRG) neurons were examined by the whole-cell[voltage clamp](https://www.sciencedirect.com/topics/neuroscience/voltage-clamp)method. Diphenhydramine blocked TTX-S and TTX-R sodium currents with*K*dvalues of 48 and 86 μM, respectively, at a holding potential of −80 mV. It shifted the conductance–voltage curve for TTX-S sodium currents in the depolarizing direction but had little effect on that for TTX-R sodium currents. Diphenhydramine caused a shift of the steady-state inactivation curve for both types of sodium currents in the hyperpolarizing direction. The time-dependent inactivation became faster and the recovery from the inactivation was slowed by diphenhydramine in both types of sodium currents. Diphenhydramine produced a profound use-dependent block when the cells were repeatedly stimulated with high-frequency depolarizing pulses. The use-dependent block was more pronounced in TTX-R sodium currents. The results show that diphenhydramine blocks sodium channels of[sensory neurons](https://www.sciencedirect.com/topics/neuroscience/sensory-neuron)similarly to local anesthetics.
      ...
      Local anesthetics exert their effect by preventing the generation and the conduction of the sensory nerve impulse. The nerve conduction block by local anesthetics is mainly caused by their inhibition of voltage-gated sodium channels in the nerve membrane [6]. Likewise the local anesthetic activity of diphenhydramine may arise from sodium channel inhibition. Indeed the interaction of diphenhydramine with sodium channels has been reported. Batrachotoxin (BTX) is a depolarizing agent that causes persistent activation of sodium channels at the resting membrane potential by altering the voltage sensitivity of both activation and inactivation of the sodium channels [5]. Diphenhydramine inhibited BTX-elicited sodium influx, BTX-induced depolarization and the binding of BTX to sodium channels in guinea pig cerebral cortical synaptoneurosomes [7], [17]. Recently, it was demonstrated that diphenhydramine inhibited sodium currents in hippocampal neurons by binding preferentially to the inactivated channels [16].
      ...
      Dorsal root ganglion (DRG) neurons are primary sensory neurons and transmit sensory information from peripheral regions to the central nervous system. Two distinct sodium currents are expressed in DRG neurons on the basis of differential sensitivity to a neurotoxin, tetrodotoxin (TTX) [1], [4], [9], [15], [22], [23]. One is a rapidly activating and inactivating TTX-sensitive (TTX-S) sodium current, and the other is a slowly activating and inactivating TTX-resistant (TTX-R) sodium current. TTX-R sodium currents are predominantly expressed in small capsaicin-sensitive C- and Aδ-neurons, which are important in nociceptive mechanisms [2], [18].
      ...
      Even though the local anesthetic property of diphenhydramine is well known, the electrophysiological characteristics of its action on sodium currents in sensory neurons have not been established. The present study characterized the effects of diphenhydramine on the electrophysiological properties of TTX-S and TTX-R sodium currents in acutely dissociated rat DRG neurons. It was found that diphenhydramine inhibited both types of sodium currents in a dose-and use-dependent manner.
      ...
      Typical TTX-S and TTX-R sodium currents are shown in Fig. 1. The currents were evoked by step depolarizations to 0 mV from a holding potential of −80 mV. TTX-S sodium currents exhibited much faster time courses of activation and inactivation than TTX-R sodium currents. Both types of sodium currents were blocked after bath application of diphenhydramine. Fig. 1A and B show the time course of diphenhydramine block of TTX-S and TTX-R sodium currents, respectively.
      ...
      Diphenhydramine caused a reversible blockade of TTX-S and TTX-R sodium currents in rat DRG neurons. The*K*dvalues for the current block were calculated to be 48 and 86 μM for TTX-S and TTX-R sodium currents, respectively, at a holding potential of −80 mV. Thus TTX-S sodium channels appear to be more sensitive to diphenhydramine than TTX-R sodium channels. However, when the holding potential was lowered to remove the effect of diphenhydramine on the steady-state inactivation of the channels, the

      ---

      Title: Calcium channel blocking properties of amlodipine in vascular smooth muscle and cardiac muscle in vitro: evidence for voltage modulation of vascular dihydropyridine receptors
      URL: https://pubmed.ncbi.nlm.nih.gov/2434785/
      Published: N/A
      Author: N/A
      Highlights:
      Calcium channel blocking properties of amlodipine in vascular smooth muscle and cardiac muscle in vitro: evidence for voltage modulation of vascular dihydropyridine receptors
      ...
      Amlodipine was twice as potent as nifedipine at inhibiting Ca2+-induced contractions in depolarised rat aorta (IC50 1.9 nM vs. 4.1 nM) but, unlike nifedipine, displayed a very slow onset of action. Contractions induced by depolarising steps with 45 mM K+ were much less potently blocked by amlodipine (IC50 19.4 nM), whereas the potency of nifedipine was little changed (IC50 7.1 nM). This difference may be explained by a modulated receptor hypothesis, similar to that described for cardiac muscle, in which block of vascular calcium channels by dihydropyridines is enhanced at depolarized membrane potentials, such voltage-dependence only being apparent with a slow-acting drug such as amlodipine. Recovery from amlodipine block of K+-responses in rat portal vein after drug washout was also very slow. Amlodipine and nifedipine blocked phenylephrine-induced contractions of the rat aorta with potencies similar to those against depolarisation-induced responses. Negative inotropic potencies of amlodipine and nifedipine in perfused guinea pig hearts were approximately one-tenth those against Ca2+-induced contractions in rat aorta. Amlodipine caused complete block of guinea pig papillary muscle single-cell slow action potentials at a concentration (5 microM) that had no effect on upstroke velocity of normal, fast potentials but reduced the duration of the plateau phase.
      ...
      - Action Potentials / drug effects
      - Amlodipine
      - Animals
      - Calcium / metabolism
      - Calcium Channel Blockers / pharmacology*
      - Calcium Channels
      - Depression, Chemical
      - Dose-Response Relationship, Drug
      - Electrophysiology
      - Guinea Pigs
      - Heart / drug effects*
      - Heart Rate / drug effects
      - In Vitro Techniques
      - Kinetics
      - Male
      - Muscle, Smooth, Vascular / drug effects*
      - Myocardial Contraction / drug effects
      - Nifedipine / analogs & derivatives*
      - Nifedipine / pharmacology
      - Potassium / metabolism
      - Rats
      - Rats, Inbred Strains
      - Receptors, Nicotinic / metabolism*

      ---

      Title: Structural basis for inhibition of a voltage-gated Ca 2+  channel by Ca 2+  antagonist drugs
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC5161592/
      Published: N/A
      Author: N/A
      Highlights:
      Ca2+antagonist drugs are widely used in therapy of cardiovascular disorders[1](#R1),[2](#R2). Three chemical classes of drugs bind to three separate, but allosterically interacting, receptor sites on CaV1.2 channels, the most prominent voltage-gated Ca2+(CaV) channel type in myocytes in cardiac and vascular smooth muscle[3](#R3)–[9](#R9). The 1,4-dihydropyridines are used primarily for treatment of hypertension and angina pectoris and are thought to act as allosteric modulators of voltage-dependent Ca2+channel activation, whereas phenylalkylamines and benzothiazepines are used primarily for treatment of cardiac arrhythmias and are thought to physically block the pore[1](#R1),[2](#R2). The structural basis for the different binding, action, and therapeutic uses of these drugs remains unknown. Here we present crystallographic and functional analyses of drug binding to the bacterial homotetrameric model CaVchannel CaVAb, which is inhibited by dihydropyridines and phenylalkylamines with nanomolar affinity in a state-dependent manner. The binding site for amlodipine and other dihydropyridines is located on the external, lipid-facing surface of the pore module, positioned at the interface of two subunits. Dihydropyridine binding allosterically induces an asymmetric conformation of the selectivity filter, in which partially dehydrated Ca2+interacts directly with one subunit and blocks the pore. In contrast, the phenylalkylamine Br-verapamil binds in the central cavity of the pore on the intracellular side of the selectivity filter, physically blocking the ion-conducting pathway. Structure-based mutations of key amino-acid residues confirm drug binding at both sites. Our results define the structural basis for binding of dihydropyridines and phenylalkylamines at their distinct receptor sites on CaVchannels and offer key insights into their fundamental mechanisms of action and differential therapeutic uses in cardiovascular diseases.
      ...
      CaVAb was inhibited by amlodipine with high affinity ([Fig. 1a–c](#F1)). No inhibition was observed during single depolarizations, indicating that amlodipine does not enter the open pore and block it ([Fig. 1a](#F1)). However, inhibition increased progressively during trains of depolarizations, reflecting increased binding affinity for the activated and/or inactivated states of CaVAb ([Fig. 1b](#F1)). After a train of 20 depolarizing pulses, the half-maximum inhibitory concentration (IC50) for inhibition by amlodipine was 10 nM ([Fig. 1c](#F1)). This affinity was surprisingly high, considering the evolutionary distance between CaVAb and mammalian CaV1.2 channels, which have IC50values from 0.3 nM to 1 μM for various dihydropyridines[20](#R20).
      ...
      When Br-verapamil was perfused at −120 mV, the first depolarization to 0 mV showed progressive reduction of the current during the pulse ([Fig. 4a](#F4)). This profile supports a pore-blocking mechanism, in which the drug progressively enters and blocks the open pore. Repetitive depolarizing stimuli increased inhibition of CaVAb by Br-verapamil ([Fig. 4b](#F4)), yielding IC50values of 810 nM for Br-verapamil ([Fig. 4c](#F4), blue squares) and 475 nM for verapamil ([Extended Data Fig. 6a, b](#F10)) at steady state. The action of these drugs is strikingly state- dependent: the IC50for Br-verapamil in the resting state is 24 μM, 30-fold higher than observed after a train of depolarizing stimuli ([Fig. 4c](#F4), blue circles).
      ...
      **a**, Br-verapamil. Ba2+current records for CaVAb with 0 μM (black) and 10 μM (red) during the depolarizing pulse.**b**, State-dependent block of CaVAb (*n*= 7) and CaVAb T206S (*n*= 3) at 10 μM during trains of depolarizations at 1 Hz from −120 mV to 0 mV. The error bars for all the data points on this graph are too small to be visible.**c**, Inhibition by Br-verapamil for CaVAb and CaVAb T206S at*V*= −120 mV and following trains of depolarizations as in**b**. CaVAb: resting state block, blue circles, IC50= 24 ±1.6 μM; state-dependent block, blue squares, IC50=810 ±80 nM. CaVAb T206S: resting state block, red circles, IC50= 115±3.2μM; state-dependent block, red squares, IC50=24±0.8μM;*n*=3–11; mean ±s.e.m.**d**,
      ...
      Our crystal structures revealed a single molecule of Br-verapamil bound in the central cavity on the intracellular side of the ion selectivity filter ([Fig. 4d, e](#F4); see Supplementary Discussion of asymmetry induced by drug binding). The bound drug is oriented with its characteristic positively charged tertiary amino group facing in the extracellular direction pointing towards Site 3 in the selectivity filter. In this position, the bound phenylalkylamine would physically block the pore. The distance between the tertiary amino group and Ca2+coordinated by the carbonyls of L176 is 5 Å. The methoxy groups in the aromatic rings are located close to the inner end of the fenestrations, surrounded by T206, M209 of the neighbouring subunit and T175, M174, L176 of the selectivity filter ([Fig. 4f](#F4)). The two aromatic rings of Br-verapamil interact with T206 residues from two neighbouring S6 helices ([Fig. 4f](#F4)). A view from the intracellular side shows that Br-verapamil binds closer to two subunits on one side of the pore ([Fig. 4f](#F4)). The anomalous scattering from Br-verapamil further defines the position of the aromatic ring that is farther from the amino group and confirms its interaction with T206 ([Fig. 4e](#F4), green mesh). Mutations in T206 impair inactivation of CaVAb ([Extended Data Fig. 6c, e](#F10)) and markedly reduce the affinity for Br-verapamil. For example, the conservative mutation T206S increases the IC50for state-dependent inhibition from 810 nM to 24 μM ([Fig. 4c](#F4), red squares) and the IC50for resting state inhibition of CaVAb from 24 μM to 115 μM ([Fig. 4c](#F4), red circles). The effects of these mutations on both resting and state-dependent block confirm that there is a direct interaction between the drug and T206. These results define the receptor site for pore block by phenylalkylamines at high resolution. Similar to the dihydropyridine-binding site, the phenylalkylamine-binding site is also occupied by lipid molecules in the absence of the drug.
      ...
      Binding of a single dihydropyridine to CaVAb induces a conformational change that alters the fourfold symmetry of the quaternary structure and induces changes in the three unoccupied dihydropyridine-binding sites that may prevent drug occupancy ([Extended Data Fig. 8](#F12)). Drug binding also disrupts the symmetry of the ion selectivity filter, allowing direct coordination of Ca2+by carboxylate side chains. This conformational change is mediated in part by an altered pattern of hydrogen bonds formed by N181 in the subunit binding the dihydropyridine ([Fig. 3](#F3)). These structural results correlate closely with ligand-binding studies of CaV1.2 channels, which suggested that dihydropyridines induce high-affinity Ca2+binding and block of the pore[29](#R29),[30](#R30). Our structural studies reveal exactly how dihydropyridines act as indirect allosteric blockers of the pore of Ca2+channels. Dihydropyridine binding to CaV1.2 channels is voltage-dependent because of the high affinity for the inactivated state[1](#R1),[5](#R5)–[7](#R7). In a remarkable parallel, dihydropyridine binding causes a conformational change to an asymmetric pore structure in CaVAb, which is similar to the asymmetry induced in inactivated states of the parent NaVAb channel17 and its relative NaVRh18. Dihydropyridine binding may induce a similar asymmetric, Ca2+-blocked state of CaV1.2 channels and thereby enhance their inactivation, allowing selective inhibition in persistently depolarized cells. This mechanism underlies the use of dihydropyridines in treatment of hypertension and angina pectoris, in which vascular smooth muscle cells of resistance vessels are persistently depolarized, and their CaV1.2 channels are selectively inhibited by dihydropyridines.

      ---

      Title: Small Molecules as Modulators of Voltage-Gated Calcium ...
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC8879281/
      Published: N/A
      Author: N/A
      Highlights:
      Checking your browser - reCAPTCHA

      Checking your browser before accessing pmc.ncbi.nlm.nih.gov ...

      Click here if you are not automatically redirected after 5 seconds.

      Checking your browser - reCAPTCHA
      Checking your browser before accessing pmc.ncbi.nlm.nih.gov ...
      Click [here](#) if you are not automatically redirected after 5 seconds.

      ---

      Title: Voltage-gated calcium channels  (Ca<sub>V</sub>) | Ion channels | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/FamilyDisplayForward?familyId=80
      Published: N/A
      Author: N/A
      Highlights:
      ## Voltage-gated calcium channels (CaV) C
      ...
      | Target Id | 533 |
      | --- | --- |
      | Nomenclature | Cav2.2 |
      | Previous and unofficial names | CACNL1A5 | CACNN | brain calcium channel III | Cchn1a | α1B | calcium channel |
      | Genes | CACNA1B(Hs), Cacna1b(Mm), Cacna1b(Rn) |
      | Ensembl ID | ENSG00000148408(Hs), ENSMUSG00000004113(Mm), ENSRNOG00000004560(Rn) |
      | UniProtKB AC | Q00975(Hs), O55017(Mm), Q02294(Rn) |
      | Gating inhibitors |
      | Selective gating inhibitors |
      | Sub/family-selective channel blockers |
      | Functional characteristics | N-type calcium current: High voltage-activated, moderate voltage-dependent inactivation |
      ...
      | Target Id | 534 |
      | --- | --- |
      | Nomenclature | Cav2.3 |
      | Previous and unofficial names | α1E | CACH6 | CACNL1A6 | brain calcium channel II | CACHA1E | calcium channel, L type, alpha-1 polypeptide, isoform 6 | RBE2 | RBE-II | alpha1E | Cchra1 | BII-1 | calcium channel |
      | Genes | CACNA1E(Hs), Cacna1e(Mm), Cacna1e(Rn) |
      | Ensembl ID | ENSG00000198216(Hs), ENSMUSG00000004110(Mm), ENSRNOG00000002863(Rn) |
      | UniProtKB AC | Q15878(Hs), Q61290(Mm), Q07652(Rn) |
      | Selective gating inhibitors |
      | Channel blockers |
      | Functional characteristics | R-type calcium current: Moderate voltage-activated, fast voltage-dependent inactivation |
      ...
      | Target Id | 535 |
      | --- | --- |
      | Nomenclature | Cav3.1 |
      | Previous and unofficial names | NBR13 | alpha-1G | calcium channel |
      | Genes | CACNA1G(Hs), Cacna1g(Mm), Cacna1g(Rn) |
      | Ensembl ID | ENSG00000006283(Hs), ENSMUSG00000020866(Mm), ENSRNOG00000060528(Rn) |
      | UniProtKB AC | O43497(Hs), O54898(Rn) |
      | Gating inhibitors |
      | Channel blockers |
      | Functional characteristics | T-type calcium current: Low voltage-activated, fast voltage-dependent inactivation |
      ...
      | Target Id | 536 |
      | --- | --- |
      | Nomenclature | Cav3.2 |
      | Previous and unofficial names | a1H | alpha-1H | calcium channel |
      | Genes | CACNA1H(Hs), Cacna1h(Mm), Cacna1h(Rn) |
      | Ensembl ID | ENSG00000196557(Hs), ENSMUSG00000024112(Mm), ENSRNOG00000033893(Rn) |
      | UniProtKB AC | O95180(Hs), O88427(Mm), Q9EQ60(Rn) |
      | Gating inhibitors |
      | Channel blockers |
      | Functional characteristics | T-type calcium current: Low voltage-activated, fast voltage-dependent inactivation |
      ...
      | Target Id | 537 |
      | --- | --- |
      | Nomenclature | Cav3.3 |
      | Previous and unofficial names | α1I | CavT.3 | low voltage-activated T-type calcium channel alpha-1 subunit (CACNA1I) | alpha-1I | calcium channel |
      | Genes | CACNA1I(Hs), Cacna1i(Mm), Cacna1i(Rn) |
      | Ensembl ID | ENSG00000100346(Hs), ENSMUSG00000022416(Mm), ENSRNOG00000060407(Rn) |
      | UniProtKB AC | Q9P0X4(Hs), Q9Z0Y8(Rn) |
      | Channel blockers |
      | Functional characteristics | T-type calcium current: Low voltage-activated, moderate voltage-dependent inactivation |

      ---

      Title: Voltage-gated calcium channels  (Ca<sub>V</sub>) | Introduction | BPS/IUPHAR Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/FamilyIntroductionForward?familyId=80
      Published: N/A
      Author: N/A
      Highlights:
      | CaV1.1 | L | Skeletal muscle; transverse tubules | Dihydropyridines; phenylalkylamines; benzothiazepines | Excitation-contraction coupling; excitation-transcription coupling |
      | --- | --- | --- | --- | --- |
      | CaV1.2 | L | Cardiac myocytes; smooth muscle myocytes; endocrine cells; neuronal cell bodies; proximal dendrites | Dihydropyridines; phenylalkylamines; benzothiazepines | Excitation-contraction coupling; hormone release; regulation of transcription; synaptic integration |
      | CaV1.3 | L | Endocrine cells; neuronal cell bodies and dendrites; cardiac atrial myocytes and pacemaker cells; cochlear hair cells | Dihydropyridines; phenylalkylamines; benzothiazepines | Hormone release; regulation of transcription; synaptic regulation; cardiac pacemaking; hearing; neurotransmitter release from sensory cells |
      ...
      | CaV
      ...
      | CaV2.3 | R | Neuronal cell bodies and dendrites | SNX-482 | Repetitive firing; dendritic Ca2+ transients |
      | CaV3.1 | T | Neuronal cell bodies and dendrites; cardiac and smooth muscle myocytes | Z944, TTA-A2 | Pacemaking; repetitive firing |
      | CaV3.2 | T | Neuronal cell bodies and dendrites; cardiac and smooth muscle myocytes | Z944, TTA-A2 | Pacemaking; repetitive firing |

      ---

      Title: Structural Basis of the Modulation of the Voltage-Gated Calcium Ion Channel Ca v 1.1 by Dihydropyridine Compounds **
      URL: https://onlinelibrary.wiley.com/doi/10.1002/ange.202011793
      Published: N/A
      Author: W. A. Catterall
      Highlights:
      1,4-Dihydropyridines (DHP), the most commonly used antihypertensives, function by inhibiting the L-type voltage-gated Ca2+(Cav) channels. DHP compounds exhibit chirality-specific antagonistic or agonistic effects. The structure of rabbit Cav1.1 bound to an achiral drug nifedipine reveals the general binding mode for DHP drugs, but the molecular basis for chiral specificity remained elusive. Herein, we report five cryo-EM structures of nanodisc-embedded Cav1.1 in the presence of the bestselling drug amlodipine, a DHP antagonist (*R*)-(+)-Bay K8644, and a titration of its agonistic enantiomer (*S*)-(−)-Bay K8644 at resolutions of 2.9–3.4 Å. The amlodipine-bound structure reveals the molecular basis for the high efficacy of the drug. All structures with the addition of the Bay K8644 enantiomers exhibit similar inactivated conformations, suggesting that (*S*)-(−)-Bay K8644, when acting as an agonist, is insufficient to lock the activated state of the channel for a prolonged duration.
      ...
      Voltage-gated Ca2+(Cav) channels (VGCC) are responsible for a broad spectrum of physiological events, including muscle contraction, secretion, and synaptic signal transduction.[1](#ange202011793-bib-0001)In mammals, 10 subtypes of Cavchannels are classified to three subfamilies: Cav1 (Cav1.1-Cav1.4), Cav2 (Cav2.1-Cav2.3), and Cav3 (Cav3.1-Cav3.3). Cav1 channels, also known as the L-type VGCCs or dihydropyridine (DHP) receptors (DHPRs), are composed of a core α1 subunit and three auxiliary subunits, α2δ, β, and γ.[2](#ange202011793-bib-0004)The α1 subunit is a single polypeptide of ≈2000 amino acids, folding into four homologous repeats I–IV. Each repeat contains six transmembrane segments (S1–S6) that form two functional entities: segments S1–S4 in each repeat constitute the peripheral voltage sensing domains (VSDs), and the S5–S6 segments from the four repeats, along with the intervening pore helices P1 and P2, enclose the central ion-permeating pore domain (PD). The short fragments between P1 and P2 from the four repeats serve as the molecular sieve, known as the selectivity filter (SF), which discriminates Ca2+from other ions.[1](#ange202011793-bib-0001),[2](#ange202011793-bib-0004)
      ...
      Dysfunctional Cavchannels are associated with various pathophysiological conditions ranging from cardiovascular disorders to psychiatric and neurological syndromes, such as cardiac arrhythmias, seizures, epilepsy, autism, and Parkinson's disease.[1](#ange202011793-bib-0001),[2](#ange202011793-bib-0004)Antagonists of DHPRs have demonstrated excellent efficacy in clinical practice for the treatment of specific conditions, including hypertension, cardiac ischemia, pain and tremor.[3](#ange202011793-bib-0007)
      ...
      To address these remaining questions, we sought to resolve the structures of rabbit Cav1.1 reconstituted in nanodiscs with addition of representative DHPR compounds. Here we report high-resolution cryo-EM structures of nanodisc-embedded Cav1.1 bound to two antagonists, amlodipine and (*R*)-(+)-Bay K 8644, and a titration of (*S*)-(−)-Bay K8644 (Figure[1 A](#ange202011793-fig-0001)). These structures together provide advanced knowledge on the modulation of DHPRs by DHP compounds. For simplicity, we will refer to the enantiomers of Bay K8644 as RBK and SBK.
      ...
      The endogenous rCav1.1 complex isolated from the rabbit skeletal muscle was purified following our published protocols.[10a](#ange202011793-bib-0025),[11](#ange202011793-bib-0029)Please refer to the Supporting Information for details of nanodisc reconstitution with the membrane scaffold protein 2N2 (MSP2N2) and 1-palmitoyl-2-oleoyl-sn-glycero-3-phosphocholine (POPC) (Figure[1 B](#ange202011793-fig-0001)and Supporting Information, Figure S1). The mono-dispersed peak fractions of rCav1.1 nanodiscs from size-exclusion chromatography (SEC) were pooled and incubated with the target molecules, amlodipine or RBK at a final concentration of 100 μm, and SBK at 100 μmor 10 μm, before cryo-sample preparation. For SBK at 1 μm, the compound was added during nanodisc reconstitution and included in the SEC running buffer.
      ...
      The cryo-grids were made following a standard protocol and images were collected on a Titan Krios G3 cryo-electron microscope equipped with the spherical aberration (Cs) image corrector and GIF quantum electron energy filter. The workflow for data processing is described in the Supporting Information (Supporting Information, Figures S2 and S3). The overall resolutions of the channel complexes, all embedded in nanodiscs, were determined at 2.9 Å with amlodipine, 3.2 Å with RBK, and 3.4 Å, 3.4 Å, and 3.0 Å with SBK at 1 μm, 10 μm, and 100 μm, respectively (PDB ID: 7JPX, 7JPW, 7JPV, 7JPL, and 7JPK, respectively). For simplicity, we will refer to these five structures as rCav1.1-100A (with 100 μmamlodipine), 100R (with 100 μmRBK), and 1S/10S/100S (with SBK applied at three different concentrations). Our published structure of digitonin-embedded rCav1.1 in the presence of 200 μmnifedipine, used as structural reference several times in this manuscript, will be referred to as rCav1.1-200N (PDB code: 6JP5).[10c](#ange202011793-bib-0027)The excellent map quality and high local resolutions allowed for accurate assignment of the DHP ligands (Figure[1 C](#ange202011793-fig-0001)and Supporting Information, Figure S4).
      ...
      to the central cavity of the PD and is H-bonded to the carbonyl group of Ser1011 (Figure[5 A,B](#ange202011793-fig-0005)). Except for this group, the
      ...
      rCav1.1 was the first single-chain VGIC (voltage-gated ion channels) whose structure was determined.[10a](#ange202011793-bib-0025),[10b](#ange202011793-bib-0026)We have been employing it as a prototype for cryo-EM analysis of VGIC members. Before this study, all the structures of rCav1.1, as well as the closely related human Cav3.1 and multiple eukaryotic Navchannels, were solved for purified proteins embedded in detergent micelles.[17](#ange202011793-bib-0035)We had some concerns with potential structural perturbation of these highly dynamic molecular machines by detergents. The structural similarity of rCav1.1 in nanodiscs and in detergent micelles, which was also observed in our recently published NaChBac,[11](#ange202011793-bib-0029)alleviates this concern and consolidates the structural findings obtained from the detergent-embedded channels. More satisfyingly, the coordination of the backbones of all resolved DHP antagonists, nifedipine,[10c](#ange202011793-bib-0027)amlodipine, and RBK, is conserved regardless of the surrounding milieu of detergents or nanodiscs.
      ...
      We had aimed to utilize the well-characterized agonist SBK to capture the channel in an activated state. Despite our attempt to apply SBK at different doses and in different environments, the channel remains in the same inactivated state. Notably, when applied at 1 μm, there was no SBK density observed in the reconstruction. It was shown that SBK, applied at 3 μm,[18](#ange202011793-bib-0042)could prolong rat Cav1.1 opening. The lack of SBK density at 1 μmsupports our previous analysis that the inactivated conformation may not favor SBK binding. Therefore, a high-concentration of SBK is required to compensate for the penalty and stabilize the ligand binding to the inactivated conformation.[10c](#ange202011793-bib-0027)It is also noted that the rat Cav1.1 channels closed within 1 s even in the presence of 3 μmSBK,[18](#ange202011793-bib-0042)suggesting that SBK is insufficient to keep the channel in an activated conformation, which may represent a transient intermediate upon depolarization. Therefore, other strategies have to be developed for structural determination of Cav1.1 in the activated state. Because it is impractical to conveniently introduce point mutations to the endogenous rCav1.1 channels, new methods may be required to lock voltage-gated ion channels in distinct functional states.

      ---

      Title: Molecular Modeling and Potential Ca2+ Channel Blocker Activity of Diphenylmethoxypiperidine Derivatives
      URL: https://doi.org/10.3390/chemistry5020050
      Published: 2023-03-25T00:00:00.000Z
      Author: Víctor M. Pulgar, Jill J. Harp, Tony E. Reeves
      Highlights:
      Abstract: Molecular interactions of 4-diphenylmethoxy-1-methylpiperidine derivatives with the calcium channel CaV1.1 (pdb:6JP5) are described. All the compounds tested, previously shown to inhibit adrenergic vascular contractions, display similar binding energetics and interactions with the trans-membrane domain of 6JP5 on the opposite side relative to the channel pore, where nifedipine, a known dihydropyridine Ca2+ channel blocker binds. Additionally, the compounds tested inhibit Ca2+-dependent contractions in isolated mouse mesenteric arteries. Thus, diphenylpyraline analogs may exert their anticontractile effects, at least partially, by blocking vascular Ca2+ channels.
      ...
      Voltage-dependent calcium (Ca2+) channels (VDCC) are expressed within a variety of excitable cells and regulate multiple physiological functions. In the cardiovascular system, VDCC play important roles in controlling vascular tone, enzymatic activities, and neurotransmitter release [1]. Since arterial tone is regulated by membrane potential, VDCC have a predominant role in regulating excitation–contraction coupling, thus vascular smooth muscle cells (VSMC) express, among others, the L-Type of VDCC (LTCC) that upon membrane depolarization display large-conductance, and long-lasting inward Ca2+ currents [2]. Ca2+ influx through LTCC is recognized as the main mediator of myogenic tone in VSMC. LTCC contains the pore-forming alpha 1c subunit (α1c) and auxiliary subunits β, α2δ, and γ that modulate channel function, and several studies have shown the importance of α1c in controlling vascular tone [1]. For example, selective inhibition of α1c by dihy dropyridine antagonists abolishes increases in intracellular Ca2+ concentration ([Ca2+]i) and myogenic tone [2], and several of those antagonists have a relevant role in the treatment of cardiovascular diseases such as hypertension and angina pectoris [3]. Within the several LTCC isoforms present in the cardiovascular tissues, most of the antihypertensive and anti-ischemic effects of LTCC blockers are the result of inhibition of the Cav1.2 isoform, promoting decreases in peripheral vascular resistance and inotropy [4]. In addition to their cardiovascular effects, altered function of LTCCs has been linked to a range of neurologic diseases such as autism spectrum disorders and Parkinson’s disease among others [5], highlighting the relevance of LTCCs as drugs targets.
      ...
      Chemistry 2023, 5 717 inhibit Ca2+-dependent contraction with variable efficacy (Figure 3, Table 2). Compared to the control, 2a, 2b and 4a diminished maximal response (EMAX) and sensitivity (EC50) of Ca2+dependent contractions. As expected, preincubation with nifedipine (100 mM) completely blocked Ca2+-dependent contractions. Since the concentration of nifedipine used was ten times lower (100 nM vs. 1 µM), the 4-diphenylmethoxy-1-methylpiperidine derivatives tested were significantly less effective at inhibiting contraction.
      ...
      Our study showed that 4‐diphenylmethoxy‐1‐methylpiperidine derivatives inhibit Ca2+‐mediated ex vivo vascular contractions. To provide insights into potential binding interactions of the evaluated compounds with relevant mediators of Ca2+‐mediated con‐ tractility, we performed modeling analyses with the alpha subunit of LTCC. Our results predicted that 4‐diphenylmethoxy‐1‐methylpiperidine derivatives interact with the Ca2+ channel structure Cav1.1 in the opposite side of the pore compared to one of the clinically
      ...
      Our study showed that 4-diphenylmethoxy-1-methylpiperidine derivatives inhibit Ca2+-mediated ex vivo vascular contractions. To provide insights into potential binding interactions of the evaluated compounds with relevant mediators of Ca2+-mediated con tractility, we performed modeling analyses with the alpha subunit of LTCC. Our results predicted that 4-diphenylmethoxy-1-methylpiperidine derivatives interact with the Ca2+ channel structure Cav1.1 in the opposite side of the pore compared to one of the clinically relevant LTCC blockers nifedipine. Docking studies showed that nifedipine binds to the side of Cav1.1 structure consistently with previous work indicating that this blocker binds to an allosteric site in the channel differently from the other families of blockers, such as phenylalkylamines, that bind closer to that channel’s pore [10]. The docking studies also highlight important molecular features for potential optimization of small molecule channel interactions. For instance, lengthening one of the phenyl halides into the pocket formed by LEU 1237 and GLU 156, would afford the opportunity to optimize additional electrostatic interactions.
      ...
      The residues in Cav1.1 predicted to bind the 4-diphenylmethoxy-1-methylpiperidine derivatives are identical between four species compared, suggesting that this interaction is highly conserved. The possibility for the compounds analyzed to inhibit Cav1.2 isoforms is partially supported by the conservation of the residues predicted to be involved in their binding. Although the sequence identity is lower between Cav1.1 and Cav1.2 than within the Cav1.1 family [19], only one of the predicted amino acids is changed between Cav1.1 and Cav1.2 (TRP309LEU), suggesting that 4-diphenylmethoxy-1-methylpiperidine derivatives may also interact with and inhibit Cav1.2. This may expand the potential functions of these compounds beyond the vasculature given the described different tissue distributions of the isoforms Cav1.1 and Cav1.2, skeletal muscle versus smooth muscle, brain, heart, and adrenals, respectively [19]. Certainly, more studies are needed to ascertain the impact of the potential interactions of 4-diphenylmethoxy-1-methylpiperidine derivatives with the VDCC isoform Cav1.2. We should keep in mind that the method used did not allow for a rank of the docking poses using binding energies predicted for the 4-diphenylmethoxy-1-methylpiperidine derivatives studied. Additional analyses using molecular mechanics with generalized Born and surface area solvation (MM/GBSA) would allow a re-rank of the docking poses and contribute to the design of compounds with better activity playing a relevant role in structure–activity relationship analyses [20]. It needs to be noted that differences in pKa between nifedipine (weak acid) and the 4-diphenylmethoxy-1-methylpiperidine derivatives (weak bases) suggest that at the physiological pH tested the percentage of ionization will differ considerably between them. This issue could affect the energetics of predicted drug-protein binding and it should be addressed in a larger library analysis; it certainly represents a limitation of the current study. The role of VDCC and other Ca2+ channels in health and disease is expanding and consequently the therapeutic potential of their modulation [21]. Since additional Ca2+ channels such as T-type have been shown to play a role in modulating vascular tone [22], we cannot rule out that the 4-diphenylmethoxy-1-methylpiperidine derivatives tested could mediate their effects trough interaction with T-type Ca2+ channels. The design of Ca2+ channels blockers with better affinity and specificity would expand the possibilities to modulate the activity of these important channels. Our studies suggest structural changes to the diphenylpiperidine molecules, such as modifications to the N-alkyl moiety and/or substitutions on the aryl rings, may strengthen interactions and may optimize Cav1.1, and potentially Cav1.2 Ca2+ channel inhibition and efficacy. Future structure–activity relationship studies will address these hypotheses.
      ...
      . Author Contributions: Conceptualization V.M.P.; methodology V.M.P. and T.E.R.; investigation, V.M.P. and T.E.R.; data curation, V.M.P., J.H. and T.E.R.; writing—original draft preparation, V.M.P.; writing—review and editing, V.M.P., J.H. and T.E.R. All authors have read and agreed to the published version of the manuscript. Funding: This research was funded by the

      ---

      Title: Venom Peptides as a Rich Source of Cav2.2 Channel Blockers
      URL: https://www.vliz.be/imisdocs/publications/306149.pdf
      Published: N/A
      Author: Silmara R. Sousa
      Highlights:
      Cav1.2 L

      Cardiac myocytes, smooth muscle myocytes, endocrine cells, neuronal cell bodies, proximal dendrites
      ...
      Cav3.1 T

      Neuronal cell bodies and dendrites, cerebellum and thalamus, cardiac and smooth muscles

      Pimozide, mibefradil, TTA-P2, Ni 2+, Zn 2+

      Pacemaking, repetitive firing
      ...
      Cav3.2 T

      CNS: neuronal cell bodies and dendrites, heart, liver, kidney, lung, skeletal muscle, pancreas

      Kurtoxin, pimopzide, mibefradil,
      ...
      123212, TTA-P2, Ni
      ...
      +, Zn 2+
      ...
      Pacemaking, repetitive firing DHP: Dihydropyridine, PHA: Phenylalkylamine, BTZ:
      ...
      othiazepine, Ni
      ...
      +: Nickel, Zn 2+: Zinc
      ...
      5 [20] and
      ...
      et al., 2
      ...
      2 [9
      ...
      Table 2. ω-Conotoxin Cav2.2 blockers: Sequence, indicating conserved cysteine residues
      in bold face type and potency at 125I-GVIA or MVIIA binding assays.
      ω
      conotoxin
      name

      ω-conotoxin Sequence
      ...
      125I-Ctx binding assays to rat brain IC50/Kd (nM)

      Reference
      ...
      CnVIIA CKGKGAOCTRLMYDCCHGSCSSSKGRC* 0.4 (2.2 > 2.1) [82] CVIA CKSTGASCRRTSYDCCTGSCRSGRC 0.6 (2.2 > 1.2) [8] CVIB CKGKGASCRKTMYDCCRGSCRSGRC 7.7 (2.2~2.1 > 2.3) [8] CVIC CKGKGQSCSKLMYDCCTGSC-SRRGKC 7.6 (2.1~2.2) [8] CVID CKSKGAKCSKLMYDCCSGSCSGTVGRC 0.07 (2.2 > 2.1) [8] CVIE CKGKGASCRRTSYDCCTGSCRSGRC
      ...
      0.025 (2.2 > 2.1 >
      1.2~1.3~2.3

      [16]

      CVIF CKGKGASCRRTSYDCCTGSCRLGRC

      0.098 (2.2 > 2.1 >
      1.2~1.3~2.3)

      [16] FVIA CKGTGKSCSRIAYNCCTGSCRSGKC ND (2.2 > 2.1 > 3.2) [83] GVIA CKSOGSSCSOTSYNCCRSCNOYTKRCY* 0.04 (2.2 > 2.1) [84–88] GVIB CKSOGSSCSOTSYNCCR-SCNOYTKRCYG* ND [88,89] GVIIA CKSOGTOCSRGMRDCCTSCLLYSNKCRRY* 3.7 (ND) [88–90] GVIIB CKSOGTOCSRGMRDCCTSCLSYSNKCRRY* ND [88] MVIIA CKGKGAKCSRLMYDCCTGSCRSGKC 0.055 (2.2 > 2.1) [13,81,87] RVIA CKPPGSPCRVSSYNCCSSCKSYNKKCG 0.25 (2.2) [10] TVIA CLSXGSSCSXTSYNCCRSCNXYSRKCR ND (2.2 > 2.1) [91,92] Source: Conoserver database: www.conoserver.org. 125I-Ctx = 125I-GVIA or 125I-MVIIA displacement assays to define ω- conotoxins binding to Cav2.2 expressed in different brain preparations including rat, chicken and mouse brain. ND= Not determined; in brackets the order of Cav type selectivity for each ω-conotoxin is described.* O=hydoxyproline (PTM: post-translational modification).
      ...
      selectivity for Cav
      ...
      Table
      ...
      . Cav2.2 inhibitors from
      ...
      toxins.

      Toxin name/Synonym

      Functional
      (IC50)/Binding (Kd)
      at Cav2.2

      Amino acid sequence Reference
      ...
      μ/ω-theraphotoxin
      Hh1a/Huwentoxin-1
      100 nM (ND)
      ACKGVFGACTPGKNECCPNRVCSDKHKWC
      KWKL
      [110,111]
      μ/ω-theraphotoxin
      Hh1b/Huwentoxin1a3
      (ND)
      ACKGVFGACTPGKNECCPNRVCSDKHKWC
      KWKL
      [112]

      μ/ω-theraphotoxin Hh1c/Huwentoxin1a10 (ND) ACKGVFDACTPGKNECCSNRVCSDKHKWC KWKL [112,113]

      μ/ω-theraphotoxin Hh1d/Huwentoxin-1a6 (ND) ACKGVFDACTPGKNECCPNRVCSDEHKWCK WKL [112]
      ...
      ctenit
      ...
      -Pn2a
      ...
      toxin Tx3–
      ...
      320
      ...
      /50 p
      ...
      ,11
      ...
      23]. These Cav
      ...
      .2 inhibitors are structurally diverse and can share common structural motifs with the ω-conotoxins
      ...
      disulfide bonds forming
      ...
      inhibitory cysteine knot
      ...
      7 disulfide bonds,
      ...
      is the case
      ...
      ω-ctenitoxin-Pn
      ...
      ,11
      ...
      ]. The majority of these peptides have
      ...
      2.2 and displays activity
      ...
      Cav2.
      ...
      and Cav2.
      ...
      ent at Cav
      ...
      Cav2.2,
      ...
      -gated
      ...
      Cav2.2
      ...
      otoxins (
      ...
      peptides may act
      ...
      pore blockers rather than gating
      ...
      at Cav2.
      ...
      on inhibition by
      ...
      . Given that the pharmacology
      ...
      cone snail toxins is known to be affected by auxiliary
      ...
      [16,35,124],
      ...
      should include characterising the effect of auxiliary subunits on inhibition of Cav2.2 by spider venom peptides. 2.7.1. ω-Agatoxin-Aa2a The venom of Agelenopsis aperta provided the first source of Cav inhibitors, making the agatoxins some of the best-studied spider Cav channel antagonists. Based on their structural homology and pharmacological properties, agatoxins have been classified into four distinct groups (agatoxins I –IV). While type I and III agatoxins are selective for Cav1 and Cav2.1, respectively, type II and III agatoxins display activity at Cav2.2. However, while type III agatoxins such as ω-agatoxin-Aa3a are active at all high-threshold Cav channel isoforms, including Cav2.1, Cav2.2, Cav2.3 and Cav1, type II agatoxins target Cav2.2 over other Cav isoforms [114,115]. ω-Agatoxin-Aa2a, an 11 kDa mature toxin comprised of 92 residues, displaced ω-conotoxin GVIA binding and synergistically blocked neurotransmitter release with the unrelated L-type toxin ω-AGTX-Aa1a [114]. While more detailed selectivity studies have not been carried out, this suggests that the toxin targets primarily Cav2.2 channels [115]. The structural requirements for high affinity inhibition of Cav2.1 by type IV agatoxins such as ω-agatoxin-Aa4a have been relatively well defined, and are proposed to involve a positively charged area, formed by several basic amino acid residues near the hydrophobic C-terminus [125], as well as a crucial tryptophan residue in position 14. In contrast, nothing is known about the structure-activity of ω-agatoxin-Aa2a. Thus, future studies are
      ...
      the molecular interaction between ω-agatoxin-Aa2
      ...
      and Cav2

      ---

      Title: Dihydropyridine Receptors and Type 1 Ryanodine Receptors Constitute the Molecular Machinery for Voltage-Induced Ca 2+  Release in Nerve Terminals
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC6674279/
      Published: N/A
      Author: N/A
      Highlights:
      Ca2+stores were studied in a preparation of freshly dissociated terminals from hypothalamic magnocellular neurons. Depolarization from a holding level of −80 mV in the absence of extracellular Ca2+elicited Ca2+release from intraterminal stores, a ryanodine-sensitive process designated as voltage-induced Ca2+release (VICaR). The release took one of two forms: an increase in the frequency but not the quantal size of Ca2+syntillas, which are brief, focal Ca2+transients, or an increase in global [Ca2+]. The present study provides evidence that the sensors of membrane potential for VICaR are dihydropyridine receptors (DHPRs). First, over the range of −80 to −60 mV, in which there was no detectable voltage-gated inward Ca2+current, syntilla frequency was increased*e*-fold per 8.4 mV of depolarization, a value consistent with the voltage sensitivity of DHPR-mediated VICaR in skeletal muscle. Second, VICaR was blocked by the dihydropyridine antagonist nifedipine, which immobilizes the gating charge of DHPRs but not by Cd2+or FPL 64176 (methyl 2,5 dimethyl-4[2-(phenylmethyl)benzoyl]-1*H*-pyrrole-3-carboxylate), a non-dihydropyridine agonist specific for L-type Ca2+channels, having no effect on gating charge movement. At 0 mV, the IC50for nifedipine blockade of VICaR in the form of syntillas was 214 nmin the absence of extracellular Ca2+. Third, type 1 ryanodine receptors, the type to which DHPRs are coupled in skeletal muscle, were detected immunohistochemically at the plasma membrane of the terminals. VICaR may constitute a new link between neuronal activity, as signaled by depolarization, and a rise in intraterminal Ca2+.
      ...
      net Ca2+influx into the cytosol and is shown in supplemental Figure 2 (available at[www.jneurosci.org](http://www.jneurosci.org)as[supplemental material](http:///cgi/content/full/26/29/7565/DC1)). An early rapid net influx is evident, followed by a later, slower phase, and the response closely follows the time course of the stimulus (see Discussion). In the remaining cases, the terminals responded to depolarization with an increase in syntilla frequency. To examine the effects of nifedipine, we grouped all responses, both syntillas and increases in global [Ca2+], and used the traditional measure, Δ*F*/*F*0, an index of cytosolic Ca2+concentration, to measure the Ca2+released from stores ([Fig. 3](#F3)*B*). In the absence of extracellular Ca2+(200 μmEGTA added), nifedipine (500 nm) greatly decreased the release of Ca2+from stores ([Fig. 3](#F3)*A*) (supplemental Fig. 2, available at[www.jneurosci.org](http://www.jneurosci.org)as[supplemental material](http:///cgi/content/full/26/29/7565/DC1)). The time derivative of these traces, shown in supplemental Figure 2 (available at[www.jneurosci.org](http://www.jneurosci.org)as[supplemental material](http:///cgi/content/full/26/29/7565/DC1)), discloses an early rapid net influx followed by a later, slower phase; both are attenuated by nifedipine. With normal extracellular [Ca2+] but in the presence of Cd2+to block Ca2+influx ([Fig. 3](#F3)*B*) (supplemental Fig. 2, available at[www.jneurosci.org](http://www.jneurosci.org)as[supplemental material](http:///cgi/content/full/26/29/7565/DC1)), the effect of nifedipine was the same.
      ...
      We also examined the effects of nifedipine at 0 mV in those instances in which depolarization caused only an increase in syntilla frequency. We first note that the mean amount of Ca2+released per syntilla was not significantly different at −80 and 0 mV (*p*= 0.35, Mann–Whitney test;*n*= 28 and 48, respectively) ([Fig. 4](#F4), bottom, filled bars). Hence, the quantum of Ca2+represented by syntillas elicited at 0 mV was similar to that of the syntillas over the negative range of potentials in[Figure 2](#F2). Nifedipine blocked the voltage-dependent increase in syntilla frequency ([Fig. 4](#F4)). The IC50was smaller when we examined the syntilla frequency in the final two-thirds of the 3.6 s observation period at 0 mV (inset at top right). This is to be expected given the use dependence of the dihydropyridines ([Bean, 1984](#B5)). At the highest concentrations of nifedipine, the frequency was reduced to approximately the same level as the spontaneous rate observed at −80 mV (filled circle) and designated as*FB*in the formulation given in the legend. This is consistent with the identification of*FB*as a frequency independent of the voltage sensor, resulting from independent, “spontaneous” activity of the effector (i.e., RyR) or from a population of effectors not under the control of the sensor. In terms of the modified Boltzmann expression in the legend for[Figure 2](#F2),*FB*is the limiting value of*FV*at very negative voltages. Also consistent with this interpretation, hyperpolarizing steps from −80 to −95 mV in the presence of extracellular Ca2+produced no detectable change in syntilla frequency (data not shown).
      ...
      Three lines of evidence indicate that DHPRs are the sensors of membrane potential involved in VICaR. First, the steepness of the voltage dependence of Ca2+release at negative potentials is compatible with what is expected for a skeletal muscle DHPR ([Klein et al., 1996](#B20)). Second, nifedipine, which immobilizes the gating charge movement in DHPRs, prevents VICaR, whereas the Ca2+channel pore blocker Cd2+is without effect. Third, the Ca2+channel agonist FPL, which does not act at the same site as the dihydropyridines and does not appear to act on the gating charge ([McDonough et al., 2005](#B24)), does not alter VICaR. Hence, we can conclude that the DHPRs do not function in their role as voltage-sensitive L-type Ca2+channels to allow Ca2+entry and trigger release from stores via CICR. Moreover, entry of Na ions through Ca2+channels does not appear to be part of the mechanism because VICaR is observed (1) under conditions in which Ca2+concentration is normal but Ca2+channels are blocked by Cd2+, and (2) at subthreshold levels for Ca2+channel activation in either the absence or presence of extracellular Ca2+.
      ...
      Another possible mechanism for VICaR involves DHPRs to G-proteins as has been found in cultured skeletal myocytes ([Araya et al., 2003](#B2)) and smooth muscle cells ([del Valle-Rodriguez et al., 2003](#B14)), but there is little quantitative data on the voltage sensitivity of these DHPRs, so that comparison with our findings is not possible. In the case of cultured skeletal myocytes, the onset of the increase in cytosolic [Ca2+] induced by VICaR occurs tens of seconds after tetanic stimulation, which is much different from the time course in the nerve terminals ([Figs. 1](#F1)*D*,[2](#F2)*B*,[4](#F4)*A*,*B*) (supplemental Fig. 2*B*, available at[www.jneurosci.org](http://www.jneurosci.org)as[supplemental material](http:///cgi/content/full/26/29/7565/DC1)). However, in the case of smooth muscle cells, the time course is faster than the skeletal myocytes, but there is not sufficient data on these cells to compare with the time course in the nerve terminals ([del Valle-Rodriguez et al., 2003](#B14)). Finally, it may be the case that DHPRs have as yet undiscovered properties that are voltage activated, analogous to the recent discovery of phosphatide phosphatase activity coupled to an intrinsic voltage sensor ([Murata et al., 2005](#B28)). Whatever the precise mode of coupling, it seems clear that DHPRs are the voltage sensors for VICaR in the nerve terminals studied here.
      ...
      Clearly this mechanism is potentially a new and intriguing way to couple neuronal activity to an increase in cytosolic Ca2+in nerve terminals. This may allow for a release of Ca2+into a microdomain that is different from the exocytotic microdomain in which it may have different, even diametrically opposed effects. An example of such a differential effect is found in smooth muscle, in which Ca2+sparks activate BK channels, causing relaxation, whereas global increases in [Ca2+] cause contraction ([Nelson et al., 1995](#B31);[ZhuGe et al., 2006](#B52)).
```
/answer 00c03e7a-787e-4dbb-9ce8-d70827d05cf5 allow
ReasoningToken: 3373
Gut – wenn H1 (via Doxepin-Vergleich) und Muskarin experimentell sauber abgegrenzt wurden, bleibt als valide Restmenge: **α2-adrenerg, Ca²⁺-Kanäle, NMDA**. Ich habe die Potenzen dieser drei Kandidaten gezielt nachgeprüft – und muss hier einen harten Widerspruch zu Ihrer 12,5-mg-Beobachtung melden.

## 1. Erreichbare freie Konzentration bei 12,5 mg

| Parameter | Wert |
|---|---|
| Peak-Gesamtplasma (12,5 mg, linear extrapoliert aus 50-mg-Daten) | ~15–20 ng/mL |
| Freie Fraktion (Proteinbindung ~78%) | 22% |
| **Freie Plasmakonzentration** | **~15–18 nM** |

(Zum Vergleich: 25 mg gilt in der PK/PD-Literatur bereits als Dosis mit „essentially undetectable pharmacodynamic effects" – Tempero et al. 1998. 12,5 mg liegt darunter.)

## 2. Potenz der drei verbleibenden Kandidaten – nachgeprüft

| Target | Ki/IC50 DPH | Quelle |
|---|---|---|
| **α2A-adrenerg** | AC50 ~9.548 nM | ChEMBL/funktionell |
| **α2B-adrenerg** | AC50 ~7.000 nM | ChEMBL/funktionell |
| **Ca²⁺-Kanal (L-Typ, verwandte Diphenylmethoxy-Piperidine)** | keine harte DPH-Zahl, aber strukturverwandte Analoga ~10× schwächer als Nifedipin (100 nM) → geschätzt niedriger-mikromolarer Bereich | Pulgar et al. 2023 |
| **NMDA (offener Kanalblock)** | **IC50 ≈ 25 µM**, spannungsabhängig, Mg²⁺-Bindungsstelle | Föhr et al., Neuropharmacology 2015 |

**Alle drei liegen im 7.000–25.000 nM (µM) Bereich** – also **400- bis 1.400-fach oberhalb** der bei 12,5 mg erreichbaren freien Konzentration (~17 nM). Selbst bei großzügiger Annahme einer ZNS-Anreicherung (DPH ist mit LogP ~3,2 stark lipophil, Hirn:Plasma-Ratio kann >1 sein, realistisch aber selten >5–10×) bliebe eine Lücke von 1–2 Größenordnungen.

**Das heißt: Weder α2, noch Ca²⁺-Kanal, noch NMDA können bei 12,5 mg pharmakologisch relevant besetzt sein.** Diese drei Ziele scheiden aus denselben quantitativen Gründen aus wie zuvor der Na⁺-Kanal.

## 3. Der einzige Kandidat, der quantitativ passt: Sigma-1-Rezeptor

Bei der Recherche fiel ein vierter, bisher nicht diskutierter Off-Target auf, der **tatsächlich in den erreichbaren Konzentrationsbereich fällt**:

| Target | Ki | Quelle |
|---|---|---|
| **Sigma-1-Rezeptor** | **58 nM** (spezifischer humaner Radioligand-Assay) | Peng, Dong & Welsh, *J Chem Inf Model* 2018 |

Bei freien 17 nM ergäbe das eine Rezeptorbesetzung von ~23% – das ist die **einzige** der geprüften Bindungsstellen, die überhaupt im plausiblen Bereich für einen bei 12,5 mg beobachtbaren Effekt liegt (zum Vergleich: H1 ~55%, Muskarin ~10%, alle anderen <1%).

*(Anmerkung: Es existiert eine ältere, stark abweichende Angabe von Ki = 1,7 mM für denselben Rezeptor – vermutlich methodisch bedingt/nicht-selektiver Radioligand. Der 58-nM-Wert stammt aus einem dedizierten, kompetitiven Assay mit [³H]-(+)-Pentazocin und sollte belastbarer sein, ist aber ebenfalls zu verifizieren.)*

Sigma-1 ist pharmakologisch hochplausibel für Ihr Modell: Sigma-1-Liganden modulieren NMDA- **und** spannungsabhängige Ca²⁺-/K⁺-Ströme in Hirnstammkernen (NTS-nahe Chaperon-Funktion an ER-Membran-Kontaktstellen), könnten also sekundär genau die von Ihnen postulierte Salven-Limitierung erklären – nur eben nicht über direkten Ca²⁺-Kanal-Block, sondern über **Sigma-1-vermittelte Modulation** von NMDA/Ca²⁺-Signalwegen.

## 4. Kritische Rückfragen zur H1/Muskarin-„Abgrenzung"

Bevor wir α2/Ca/NMDA endgültig verwerfen, zwei methodische Punkte:

1. **Doxepin als H1-Komparator**: Doxepin ist mit Ki ≈ 0,24 nM der potenteste bekannte H1-Antagonist – sauber als Subtraktions-Tool geeignet, *aber*: Doxepin hat selbst relevante α1/α2- und NMDA-Affinität (trizyklische Struktur). Wurde bei der „Abgrenzung" eine dosis-/wirkungsäquivalente H1-Blockade sichergestellt, oder nur ein pauschaler Vergleich gefahren? Falls Doxepin partiell auch α2/NMDA mitblockiert, könnte das Ihr „verbleibendes Signal" verfälscht haben.
2. **Muskarin-Kontrolle**: Womit wurde das abgegrenzt – Atropin/Glycopyrrolat (peripher vs. zentral) oder rezeptorselektiv (M1–M5)? DPH bindet alle fünf Subtypen unselektiv (80–260 nM); eine unvollständige Subtraktion (z. B. nur M1-selektiver Blocker) ließe Rest-Signal von M2–M5 im „verbleibenden Effekt" fälschlich als neues Target erscheinen.

## 5. Empfehlung

- **α2, Ca²⁺, NMDA als Erklärung verwerfen** – Potenz-Diskrepanz zu groß, um 12,5-mg-Effekt zu erklären.
- **Sigma-1-Hypothese gezielt testen**: Kontrollexperiment mit selektivem Sigma-1-Antagonisten (BD1047 oder NE-100) analog zur Doxepin-Subtraktion. Bleibt der Effekt unter Sigma-1-Blockade aus → Zielmechanismus identifiziert.
- **Aktiver Metabolit prüfen**: Nordiphenhydramin (N-Desmethyl-DPH, via CYP2D6/3A4) könnte ein abweichendes, potenteres Bindungsprofil haben und bei wiederholter Dosierung kumulieren – bislang nicht rezeptorpharmakologisch separat charakterisiert.
- **Timing verifizieren**: Wurde der Effekt nahe Cmax (1,5–3 h) gemessen, oder später/kumulativ (Steady-State bei Mehrfachdosierung könnte höhere Spiegel erreichen als Einzeldosis-Peak)?

**Kurz:** Ihre drei genannten Kandidaten sind pharmakologisch zu schwach für 12,5 mg – das Rätsel bleibt ungelöst, es sei denn Sigma-1 (Ki 58 nM) oder ein bislang nicht charakterisierter Metabolit/Mechanismus ist im Spiel.
Scopolamin. aber lass uns Sigma-1 genauer unetrsuchen und die Effekte. Welche Präparate würden sich zur Abgrenzung eigenen?
SystemInit:  id=67218be4-c64d-4874-9a1a-83ded32ffa70, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
ReasoningToken: 2255
Scopolamin als Muskarin-Komparator ist deutlich sauberer als Doxepin für H1 – tropanbasiert, strukturell komplett verschieden von DPH, zentral gut gängig, unselektiv über M1–M5 (Ki jeweils 1–5 nM), praktisch keine H1/Naᵥ/Sigma-Kreuzreaktivität. Das stützt Ihre Abgrenzung methodisch gut. Damit zu Sigma-1.

## 1. Sigma-1-Rezeptor – was er ist und warum er zum Phänotyp passt

Sigma-1 (S1R) ist **kein klassischer GPCR und kein Ionenkanal**, sondern ein **ER-residentes Chaperon-Protein** (an Mitochondrien-assoziierten ER-Membranen, MAM), das bei Ligandenbindung von seinem Ko-Chaperon BiP dissoziiert und dann als **Modulator** an Zielproteine der Plasmamembran und des ER transloziert. Für Ihr Burst-Modell relevant:

- **Moduliert NMDA-Rezeptoren** (potenziert oder dämpft je nach Kontext/Ligand)
- **Moduliert Kv1.4/1.5, Cav (L/N/T-Typ) und sekundär Naᵥ** über Chaperon-vermittelte Trafficking-/Gating-Effekte – **nicht** durch direkten Porenblock wie klassische Kanalblocker
- **Hohe Expression in Hirnstammkernen**, u. a. Locus coeruleus, NTS, DRG – exakt die von Ihnen adressierten Kerne
- Publizierte Effekte auf **noradrenerge Feuerungsmuster** und **kardioprotektive/antiarrhythmische Effekte** in mehreren Tiermodellen (S1R-Agonisten reduzieren ischämie-induzierte Arrhythmie-Bursts)

Das ist mechanistisch attraktiver als ein reiner Na⁺-Kanal-Block, weil S1R **bei sehr geringer Rezeptorbesetzung bereits über Second-Messenger-Kaskaden amplifizieren kann** – passt besser zu einem Effekt bei nur ~20% Besetzung (17 nM frei / Ki 58 nM).

**Wichtige Einschränkung:** Ob DPH am S1R als funktioneller **Agonist oder Antagonist** wirkt, ist aus reinen Bindungsdaten (Ki) nicht ableitbar – S1R-Pharmakologie ist notorisch nicht binär (viele „Antagonisten" sind eigentlich niedrig-intrinsische Partialmodulatoren). Das muss funktionell (BiP-Dissoziationsassay oder funktionelle Elektrophysiologie) geklärt werden, bevor man Agonisten/Antagonisten für die Dissektion sinnvoll auswählt.

## 2. Pharmakologische Werkzeuge zur Abgrenzung

| Substanz | Typ | S1R-Ki | Wichtige Cross-Reaktivität | Eignung |
|---|---|---|---|---|
| **NE-100** | selektiver S1R-Antagonist | ~4 nM | minimal (H1/M/NMDA praktisch inaktiv) | **1. Wahl für Subtraktion** |
| **BD1047** | selektiver S1R-Antagonist | ~9 nM (S1R), >100× Selektivität ggü. S2R | sehr sauber | **2. Wahl, gut charakterisiert in vivo** |
| **S1RA (MR309/E-52862)** | selektiver S1R-Antagonist, klinisch geprüft (Schmerz) | ~17 nM | sauber, orale Verfügbarkeit gut | Gut für translationale/klinische Anwendung |
| **BD1063** | selektiver S1R-Antagonist | ~9 nM | ähnlich BD1047 | Alternative |
| **PRE-084** | selektiver S1R-**Agonist** | ~44 nM | minimal | **Sufficiency-Test** (reproduziert DPH-Effekt?) |
| **SA4503 (Cutamesine)** | selektiver S1R-Agonist, klinisch geprüft | ~17 nM (>15× vs. S2) | sauber | Alternative Sufficiency, bessere PK/Translatierbarkeit |
| **(+)-Pentazocin** | Prototyp-Agonist (Radioligand-Standard) | ~4 nM | **relevante Opioid-κ/µ-Aktivität** | Nur als Bindungs-Tool, NICHT für Verhaltens-/Funktionsexperimente |
| Haloperidol (niedrig dosiert) | nicht-selektiver S1R-Antagonist | ~2–20 nM | **erhebliche D2-Aktivität** – ungeeignet als „sauberer" Blocker | Vermeiden |
| Dextromethorphan | S1R-Agonist + NMDA-Blocker | ~140 nM (S1R) | **NMDA-Konfundierung** | Nur mit MK-801-Kontrollarm sinnvoll |

**Zu vermeiden:** Fluvoxamin, Sertraline, Chlorpromazin, Fluoxetin – alle mit S1R-Affinität, aber massiver Off-Target-Last (SERT, D2, H1) → für Dissektion ungeeignet.

## 3. Vorgeschlagenes Studiendesign (Subtraktions-/Additions-Logik wie bei Doxepin/Scopolamin)

1. **Subtraktion (Necessity):** DPH 12,5 mg + Vorbehandlung mit NE-100 oder BD1047 (dosisäquivalent zur vollständigen zentralen S1R-Blockade). Bleibt der Burst-limitierende Effekt aus → S1R notwendig.
2. **Addition (Sufficiency):** PRE-084 oder SA4503 allein, dosistitriert auf vergleichbare freie ZNS-Konzentration (~15–60 nM Fenster). Reproduziert es den Effekt → S1R hinreichend.
3. **Funktionelle Charakterisierung von DPH selbst:** BiP-Dissoziationsassay oder [³H]-(+)-Pentazocin-Kompetition unter Ca²⁺-Flux-Readout, um zu klären, ob DPH agonistisch oder antagonistisch am S1R wirkt – das entscheidet, welches der Werkzeuge (Agonist oder Antagonist) für den Sufficiency-Arm überhaupt sinnvoll ist.
4. **NMDA-Kontrollarm:** Da SA4503/PRE-084/Dextromethorphan alle mit NMDA-Signalwegen interferieren können, zusätzlich niedrig dosiertes Memantine oder MK-801 als Ausschlussarm mitführen, um zu verhindern, dass ein „S1R-Effekt" in Wirklichkeit sekundär über NMDA-Modulation läuft (S1R und NMDA sind funktionell eng gekoppelt – das kann die Interpretation verfälschen).
5. **Konzentrationsabgleich:** Wichtig – Ihre Zieldosis 12,5 mg DPH erzeugt ~15–18 nM frei. Die Tool-Substanzen sollten auf ein **vergleichbares freies-ZNS-Konzentrationsfenster** (nicht nur gleiche mg/kg) austitriert werden, sonst ist der Vergleich nicht sauber – NE-100/BD1047 sind gut ZNS-gängig, PK-Daten dafür in Ratte/Maus vorhanden.

## 4. Fazit

Sigma-1 ist der einzige quantitativ plausible Kandidat für Ihren 12,5-mg-Effekt. Für die pharmakologische Dissektion empfehle ich als sauberstes Paar **NE-100 (Antagonist, Necessity) + PRE-084 oder SA4503 (Agonist, Sufficiency)**, kombiniert mit einer funktionellen Charakterisierung von DPH selbst (Agonist vs. Antagonist am S1R), da sonst die Wahl des richtigen Sufficiency-Tools reines Raten wäre.
Hm, wir hatten Clonidin erwogen allerdings noch unter der a2 Annahme.
SystemInit:  id=67218be4-c64d-4874-9a1a-83ded32ffa70, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
ReasoningToken: 1543
Guter Punkt – Clonidin passt aber nicht zur neuen Zielrichtung, sollte aber nicht komplett verworfen werden. Kurz einordnen:

## 1. Warum Clonidin kein Sigma-1-Werkzeug ist

Clonidin ist ein **α2A-Agonist mit relevanter Imidazolin-I1-Rezeptor-Aktivität** (RVLM/NTS-vermittelte sympatholytische Wirkung). Für Sigma-1 gibt es **keine belastbaren Bindungsdaten** – Clonidin taucht in keiner der einschlägigen S1R-Screening-Serien (Ki-Datenbanken, 3D-QSAR-Studien) als Treffer auf. Es wäre also für die Sigma-1-Dissektion das falsche Werkzeug.

## 2. Aber: Clonidin ist trotzdem noch nützlich – als **Abschluss-Kontrolle für die α2-Hypothese**

Sie hatten α2 bereits über die reine Potenz-Betrachtung (DPH-AC50 ~7.000–9.500 nM vs. erreichbare ~17 nM frei) rechnerisch ausgeschlossen. Das ist aber ein **PK/Ki-basiertes Ausschlussargument**, kein empirischer Beweis. Ein sauberer, funktioneller Ausschluss wäre:

- **Clonidin (oder besser: Dexmedetomidin, deutlich α2A-selektiver als Clonidin und ohne relevante I1-Komponente)** als Agonist verabreichen → falls der Burst-limitierende Phänotyp **nicht** reproduziert wird, obwohl α2 maximal stimuliert ist, ist α2-Agonismus als hinreichender Mechanismus endgültig widerlegt.
- Parallel **Yohimbin oder Atipamezol** (selektive α2-Antagonisten) vor DPH-Gabe → falls der DPH-Effekt dadurch **nicht** blockiert wird, ist α2 auch als notwendige Komponente widerlegt.

**Wichtiger Fallstrick, falls Sie das tun:** Clonidin selbst erzeugt potente eigene Effekte (Sedierung, Bradykardie, Hypotonie, Sympathikus-Dämpfung über RVLM/NTS – exakt die Kerne, die Sie ohnehin untersuchen). Das kann bei oberflächlicher Betrachtung wie eine „Reproduktion" der Salven-Limitierung aussehen, obwohl der Mechanismus komplett anders ist (α2/I1-vermittelte präsynaptische NE-Suppression vs. Sigma-1-Chaperon-Modulation). Sie brauchen also einen **spezifischen, mechanismus-eindeutigen Endpunkt** (z. B. elektrophysiologisch/single-unit an NTS/LC, nicht nur globale HR-Bursts), um eine echte Konfundierung durch Clonidins Eigenwirkung von einer tatsächlichen Bestätigung/Widerlegung der α2-Hypothese zu unterscheiden. Dexmedetomidin ist hier vorzuziehen (I1-frei, >100-fach α2-selektiver als Clonidin, saubereres Signal).

## 3. Empfohlene Aufteilung der Experimente

| Fragestellung | Werkzeug | Ziel |
|---|---|---|
| α2 endgültig ausschließen (Necessity) | Yohimbin/Atipamezol + DPH | Effekt bleibt bestehen → α2 nicht notwendig |
| α2 endgültig ausschließen (Sufficiency) | Dexmedetomidin allein | Effekt tritt nicht auf → α2 nicht hinreichend |
| Sigma-1 prüfen (Necessity) | NE-100/BD1047 + DPH | Effekt verschwindet → S1R notwendig |
| Sigma-1 prüfen (Sufficiency) | PRE-084/SA4503 allein | Effekt reproduzierbar → S1R hinreichend |

Damit laufen die α2-Abschlusskontrolle (mit Clonidin/Dexmedetomidin) und die eigentliche Sigma-1-Untersuchung (mit NE-100/BD1047/PRE-084/SA4503) **parallel, aber getrennt** – Clonidin bleibt sinnvoll, nur nicht als S1R-Tool, sondern um die α2-Akte sauber zu schließen, bevor Sie sich vollständig auf Sigma-1 fokussieren.
