Prüfe für den angefügten Mechanismus die Potenz und Selektivität von DPH. Ziel ist eine Dosisreduktion bei Erhalt des gewünschten Effektes der Limitierung der Salven unter berücksichtigung der Salven-abhängigen Kinetik.

# Mechanismus

**DPH-positiv → Membranstabilisierung, nicht Antihistaminik.** Diphenhydramin ist ein **use-dependent, inaktivierungs-selektiver Na⁺-Kanal-Blocker**: Kd ~10 µM am inaktivierten, >300 µM am Ruhekanal; „*profound use-dependent block when repeatedly stimulated with high-frequency depolarizing pulses*" (Kuo et al., Mol Pharmacol 2000; Kim et al., Brain Res 2000). Es teilt sich das Diphenyl-Pharmakophor mit **Phenytoin, Imipramin, Benztropin**. Das ist exakt die Biophysik, die Sie brauchen: bei normaler Frequenz nahezu stumm, bei der HR>130-Salve progressiv abklemmend. **DPH wirkt also vermutlich als „lokalanästhetischer" Membranstabilisator auf die NTS/LC-Salve, nicht über H1 und nicht über Muskarin.**

## Konsequenz für die Mechanismus-Trennung (Na⁺-Kanal vs. S1R)

Das lässt sich jetzt sauber weiterrechnen, wenn Sie die freie Hirnkonzentration bei 12,5 mg kennen (aus der 20 %-H1-Belegung bei bekanntem H1-Kd ~1–4 nM lässt sich die freie Konzentration über C = Kd × Occ/(1-Occ) zurückrechnen, grob **~0,3–1 nM freie Konzentration**):

- **H1 (Kd ~1–4 nM):** 20 % Belegung ✓ (Ihr Ausgangswert)
- **Muskarinrezeptoren (Ki ~100–1000 nM):** bei ~0,5–1 nM freier Konzentration → Belegung **<1 %** → muskarinerger Beitrag praktisch ausgeschlossen
- **Na⁺-Kanal, inaktivierter Zustand (Kd ~10 µM):** bei ~1 nM freier Konzentration → **Gleichgewichtsbelegung ~0,01 %** – auf den ersten Blick vernachlässigbar
- **S1R (Ki grob im µM-Bereich für DPH als Off-Target-Ligand):** ebenfalls **<0,1 %** Gleichgewichtsbelegung

Das wirkt zunächst wie ein Widerspruch zu Ihrer Na⁺-Kanal-Hypothese – **ist es aber nicht**: Genau hier liegt die Pointe des *use-dependent block* (Hille'sches modulated-receptor-Modell). Die Gleichgewichtsbindung ist bei Ruhefrequenz vernachlässigbar, aber bei einer HR>130-Salve akkumuliert die Bindung an den *inaktivierten* Kanalzustand mit jedem Aktionspotential neu – die effektive "funktionelle Belegung" während der hochfrequenten Salve kann dadurch um Größenordnungen über der Ruhe-Gleichgewichtsbelegung liegen, ohne dass die Gesamt-Rezeptorbelegung (wie bei H1) jemals hoch sein muss.

**Das ist genau das pharmakologische Unterscheidungsmerkmal, das Sie brauchen:** Ein H1-Effekt *kann* bei 20 % Belegung nicht robust auftreten (per PET-Literatur belegt). Ein frequenzabhängiger Na⁺-Kanal-Effekt *kann* dagegen bei nominell verschwindender Ruhebelegung trotzdem voll ausgeprägt sein, weil er nicht von der Gleichgewichtsbelegung, sondern von der Stimulationsfrequenz abhängt.
SystemInit:  id=0b6c12a1-e88d-4c35-ae14-3099ae2224a3, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
Control Request:
```yaml
id: 88f731b1-dceb-480d-8401-6e79d0f31886
toolName: openalex-search
arguments:
  query: diphenhydramine use-dependent block sodium channel Kuo
  reason: Find kinetic parameters for DPH use-dependent Na+ channel block
  fields: abstract
```
/answer 88f731b1-dceb-480d-8401-6e79d0f31886 allow
ReasoningToken: 497
Control Request:
```yaml
id: 9e0052cc-b7fd-4a97-a064-6f25a51ed682
result:
  structuredContent:
    count: 63
    returned: 25
    page: 1
    per_page: 25
    results:
    - id: https://openalex.org/W1977762789
      doi: https://doi.org/10.1038/sj.bjp.0706058
      title: "V102862 (Co 102862): a potent, broad‐spectrum state‐dependent blocker of mammalian voltage‐gated sodium channels"
      publication_year: 2005
      relevance_score: 154.49182
      abstract: "1. 4-(4-Fluorophenoxy)benzaldehyde semicarbazone (V102862) was initially described as an orally active anticonvulsant with robust activity in a variety of rodent models of epilepsy. The mechanism of action was not known. We used whole-cell patch-clamp techniques to study the effects of V102862 on native and recombinant mammalian voltage-gated Na+ channels. 2. V102862 blocked Na+ currents (I(Na)) in acutely dissociated cultured rat hippocampal neurons. Potency increased with membrane depolarization, suggesting a state-dependent mechanism of inhibition. There was no significant effect on the voltage dependence of activation of I(Na). 3. The dissociation constant for the inactivated state (K(I)) was approximately 0.6 microM, whereas the dissociation constant for the resting state (K(R)) was >15 microM. 4. The binding to inactivated channels was slow, requiring a few seconds to reach steady state at -80 mV. 5. The mechanism of inhibition was characterized in more detail using human embryonic kidney-293 cells stably expressing rat brain type IIA Na+ (rNa(v)1.2) channels, a major Na+ channel alpha subunit in rat hippocampal neurons. Similar to hippocampal neurons, V102862 was a potent state-dependent blocker of rNa(v)1.2 channels with a K(I) of approximately 0.4 microM and K(R) approximately 30 microM. V102862 binding to inactivated channels was relatively slow (k(+) approximately = 1.7 microM(-1) s(-1)). V102862 shifted the steady-state availability curve in the hyperpolarizing direction and significantly retarded recovery of Na+ channels from inactivation. 6. These results suggest that inhibition of voltage-gated Na+ channels is a major mechanism underlying the anticonvulsant properties of V102862. Moreover, understanding the biophysics of the interaction may prove to be useful in designing a new generation of potent Na+ channel blocker therapeutics."
    - id: https://openalex.org/W2125688251
      doi: https://doi.org/10.1016/j.jccase.2015.06.002
      title: Diphenhydramine and QT prolongation – A rare cardiac side effect of a drug used in common practice
      publication_year: 2015
      relevance_score: 111.83774
    - id: https://openalex.org/W2022126452
      doi: https://doi.org/10.1007/s00210-002-0669-0
      title: "Inhibition of skeletal muscle sodium currents by mexiletine analogues: specific hydrophobic interactions rather than lipophilia per se account for drug therapeutic profile"
      publication_year: 2003
      relevance_score: 80.03782
    - id: https://openalex.org/W1990826945
      doi: https://doi.org/10.1016/j.hrthm.2009.07.002
      title: "Drugs and Brugada syndrome patients: Review of the literature, recommendations, and an up-to-date website (www.brugadadrugs.org)"
      publication_year: 2009
      relevance_score: 79.20084
    - id: https://openalex.org/W2108712957
      doi: https://doi.org/10.1016/j.tiv.2014.11.010
      title: In vitro detection of cardiotoxins or neurotoxins affecting ion channels or pumps using beating cardiomyocytes as alternative for animal testing
      publication_year: 2014
      relevance_score: 77.298134
    - id: https://openalex.org/W1512491578
      doi: https://doi.org/10.1111/j.1528-1167.2012.03675.x
      title: "Loss of β<sub>1</sub>accessory Na<sup>+</sup>channel subunits causes failure of carbamazepine, but not of lacosamide, in blocking high‐frequency firing via differential effects on persistent Na<sup>+</sup>currents"
      publication_year: 2012
      relevance_score: 69.7628
      abstract: "PURPOSE: In chronic epilepsy, a substantial proportion of up to 30% of patients remain refractory to antiepileptic drugs (AEDs). An understanding of the mechanisms of pharmacoresistance requires precise knowledge of how AEDs interact with their targets. Many commonly used AEDs act on the transient and/or the persistent components of the voltage-gated Na(+) current (I(NaT) and I(NaP) , respectively). Lacosamide (LCM) is a novel AED with a unique mode of action in that it selectively enhances slow inactivation of fast transient Na(+) channels. Given that functional loss of accessory Na(+) channel subunits is a feature of a number of neurologic disorders, including epilepsy, we examined the effects of LCM versus carbamazepine (CBZ) on the persistent Na(+) current (I(NaP) ), in the presence and absence of accessory subunits within the channel complex. METHODS: Using patch-clamp recordings in intact hippocampal CA1 neurons of Scn1b null mice, I(NaP) was recorded using slow voltage ramps. Application of 100 μm CBZ or 300 μm LCM reduced the maximal I(NaP) conductance in both wild-type and control mice. KEY FINDINGS: As shown previously by our group in Scn1b null mice, CBZ induced a paradoxical increase of I(NaP) conductance in the subthreshold voltage range, resulting in an ineffective block of repetitive firing in Scn1b null neurons. In contrast, LCM did not exhibit such a paradoxical increase, and accordingly maintained efficacy in blocking repetitive firing in Scn1b null mice. SIGNIFICANCE: These results suggest that the novel anticonvulsant LCM maintains activity in the presence of impaired Na(+) channel β(1) subunit expression and thus may offer an improved efficacy profile compared with CBZ in diseases associated with an impaired expression of β sub-units as observed in epilepsy."
    - id: https://openalex.org/W2535605770
      doi: https://doi.org/10.3892/or.2016.5201
      title: Diphenhydramine induces melanoma cell apoptosis by suppressing STAT3/MCL-1 survival signaling and retards B16-F10 melanoma growth in vivo
      publication_year: 2016
      relevance_score: 67.781334
      abstract: "Melanoma is the most aggressive skin malignancy with a high rate of mortality and is frequently refractory to many therapeutics, thus demanding the discovery of novel effective anti-melanoma agents. Diphenhydramine (DPH) is an H1 histamine receptor antagonist and a relatively safe drug. Previous studies have revealed the in vitro cytotoxicity of DPH against melanoma cells, but the mechanisms involved concerning its cytotoxicity and the in vivo anti-melanoma effect remain unknown. We herein present the first evidence supporting that DPH is selectively proapoptotic for a panel of melanoma cell lines irrespective of BRAFV600E status while sparing normal melanocytes. Of note, DPH effectively suppressed tumor growth and prolonged the length of survival of mice bearing B16-F10 melanoma. Mechanistic investigation further revealed that DPH downregulated antiapoptotic MCL-1, whereas MCL-1 overexpression impeded the proapoptotic action of DPH. Moreover, DPH attenuated STAT3 activation, as evidenced by the reduced levels of tyrosine 705-phosphorylated STAT3. Notably, ectopic expression of constitutively active STAT3 mutant reduced DPH-induced apoptosis but also protected MCL-1 from downregulation by DPH, illustrating that DPH impairs STAT3 activation to block STAT3-mediated induction of MCL-1 in eliciting apoptosis. Collectively, we for the first time validate the in vivo anti‑melanoma effect of DPH and also establish DPH as a drug targeting STAT3/MCL-1 survival signaling pathway to induce apoptosis. Our discovery therefore suggests the potential to repurpose DPH as an anti-melanoma therapeutic agent."
    - id: https://openalex.org/W1979176178
      doi: https://doi.org/10.1111/j.1476-5381.1989.tb12652.x
      title: Vasodilator actions of HA1077 <i>in vitro</i> and <i>in vivo</i> putatively mediated by the inhibition of protein kinase
      publication_year: 1989
      relevance_score: 58.564644
      abstract: "The in vitro and in vivo vasorelaxant effects of HA1077, 1-(5-isoquinolinesulphonyl)-homopiperazine HCl, a novel vasodilator were examined. The inhibitory effects of HA1077 on contractile responses to various agonists were examined on strips of rabbit aorta. The concentration-response curves to 5-hydroxytryptamine, prostaglandin F2alpha, histamine, angiotensin II, noradrenaline and dopamine were concentration-dependently shifted to the right in the presence of HA1077 (0.3-3.0 microM). The in vivo vasodilator effects of HA1077 were examined in the constant-pressure autoperfused coronary vascular bed of dogs. Intra-coronary administration of HA1077 (3-30 micrograms per dog) dose-dependently increased coronary blood flow (CBF), with no effect on mean blood pressure (MBP) or heart rate (HR). Intra-coronary infusion of atropine, propranolol or diphenhydramine did not modify the in vivo coronary vasodilator response to HA1077. To determine the flow profile for HA1077 in dogs, blood flow in four vascular beds was measured, by use of noncannulating electromagnetic flow probes. HA1077 (0.01-0.3 mg kg-1, i.v.) dose-dependently decreased MBP and increased vertebral blood flow (VBF), CBF, renal blood flow (RBF) and femoral blood flow (FBF). A haemodynamic analysis showed that continuous i.v. infusion of HA1077 (0.01 and 0.033 mg kg-1min-1) dose-dependently decreased peripheral vascular resistance and increased cardiac output. There were no significant changes in right atrial pressure, dP/dt or ventricular minute work. The effects of HA1077 on various enzymes considered to be related to the regulation of smooth muscle contraction were examined. HA1077 had little effect on cyclic nucleotide phosphodiesterases, yet it potently inhibited protein kinases such as cyclic nucleotide dependent protein kinases and Ca2+/calmodulin dependent myosin light chain kinase. The present study demonstrates that HA1077 is a novel type of arterial vasodilator."
    - id: https://openalex.org/W4404728763
      doi: https://doi.org/10.2147/oaem.s473627
      title: "Droperidol Plus Diphenhydramine for Symptom Improvement in Suspected Cannabinoid Hyperemesis Syndrome: A Prospective Cohort Study"
      publication_year: 2024
      relevance_score: 57.51826
      abstract: "Background: Cannabinoid Hyperemesis Syndrome (CHS) is characterized by recurrent, paroxysmal episodes of nausea, vomiting, and abdominal discomfort in chronic cannabis users. Optimized CHS treatment data remain limited. Recent prospective evidence have demonstrated haloperidol superiority over ondansetron. Retrospective data suggest the utility of droperidol, a dopamine antagonist like haloperidol, for treating acute CHS. Objective: To prospectively assess the utility of droperidol plus diphenhydramine to mitigate common CHS symptoms. Methods: This was a multicenter, prospective interventional study in the emergency department (ED). Participants were administered a study regimen of droperidol and diphenhydramine to treat CHS after enrollment. The primary outcome measure was the change in VAS scores within the droperidol prospective cohort. Symptoms of nausea, vomiting, and abdominal pain were measured using a visual analogue scale (VAS) up to 120 minutes. Secondary measures assessed include repeat visits to the ED within seven days. Results: Amongst 47 droperidol participants, VAS for nausea and vomiting declined from baseline 8.3±2.0 to 3.1±3.3 at 30 minutes post treatment (p < 0.05), and 1.4±2.4 at 120 minutes (p < 0.05). For abdominal pain, VAS mean was 7.8±2.4 at baseline declining to 3.6±2.9 at 30 minutes (p < 0.05) and 1.7±2.9 at 120 minutes (p < 0.05). Return to the ED within 7 days following droperidol was 12.9% (n=47). Conclusion: This trial shows significant improvement in symptoms from baseline, 30 and 120 minutes post-treatment and return to the ED within a week post treatment with the study regimen."
    - id: https://openalex.org/W3205136031
      doi: https://doi.org/10.2147/dddt.s329547
      title: The Expanding Role of Pyridine and Dihydropyridine Scaffolds in Drug Design
      publication_year: 2021
      relevance_score: 52.931026
      abstract: "Pyridine-based ring systems are one of the most extensively used heterocycles in the field of drug design, primarily due to their profound effect on pharmacological activity, which has led to the discovery of numerous broad-spectrum therapeutic agents. In the US FDA database, there are 95 approved pharmaceuticals that stem from pyridine or dihydropyridine, including isoniazid and ethionamide (tuberculosis), delavirdine (HIV/AIDS), abiraterone acetate (prostate cancer), tacrine (Alzheimer's), ciclopirox (ringworm and athlete's foot), crizotinib (cancer), nifedipine (Raynaud's syndrome and premature birth), piroxicam (NSAID for arthritis), nilvadipine (hypertension), roflumilast (COPD), pyridostigmine (myasthenia gravis), and many more. Their remarkable therapeutic applications have encouraged researchers to prepare a larger number of biologically active compounds decorated with pyridine or dihydropyridine, expandeing the scope of finding a cure for other ailments. It is thus anticipated that myriad new pharmaceuticals containing the two heterocycles will be available in the forthcoming decade. This review examines the prospects of highly potent bioactive molecules to emphasize the advantages of using pyridine and dihydropyridine in drug design. We cover the most recent developments from 2010 to date, highlighting the ever-expanding role of both scaffolds in the field of medicinal chemistry and drug development."
    - id: https://openalex.org/W1644982027
      doi: https://doi.org/10.1002/14651858.cd008307.pub2
      title: Pharmacotherapy for the prevention of chronic pain after surgery in adults
      publication_year: 2013
      relevance_score: 36.60097
      abstract: "BACKGROUND: Chronic pain can often occur after surgery, substantially impairing patients' health and quality of life. It is caused by complex mechanisms that are not yet well understood. The predictable nature of most surgical procedures has allowed for the conduct of randomized controlled trials of pharmacological interventions aimed at preventing chronic postsurgical pain. OBJECTIVES: The primary objective was to evaluate the efficacy of systemic drugs for the prevention of chronic pain after surgery by examining the proportion of patients reporting pain three months or more after surgery. The secondary objective was to evaluate the safety of drugs administered for the prevention of chronic pain after surgery. SEARCH METHODS: We identified randomized controlled trials (RCTs) of various systemically administered drugs for the prevention of chronic pain after surgery from CENTRAL, MEDLINE, EMBASE and handsearches of other reviews and trial registries. The most recent search was performed on 17 July 2013. SELECTION CRITERIA: Included studies were double-blind, placebo-controlled, randomized trials involving adults and evaluating one or more drugs administered systemically before, during or after surgery, or both, which measured pain three months or more after surgery. DATA COLLECTION AND ANALYSIS: Data collected from each study included the study drug name, dose, route, timing and duration of dosing; surgical procedure; proportion of patients reporting any pain three months or more after surgery, reporting at least 4/10 or moderate to severe pain three months or more after surgery; and proportion of participants dropping out of the study due to treatment-emergent adverse effects. MAIN RESULTS: We identified 40 RCTs of various pharmacological interventions including intravenous ketamine (14 RCTs), oral gabapentin (10 RCTs), oral pregabalin (5 RCTs), non-steroidal anti-inflammatories (3 RCTs), intravenous steroids (3 RCTs), oral N-methyl-D-aspartate (NMDA) blockers (3 RCTs), oral mexiletine (2 RCTs), intravenous fentanyl (1 RCT), intravenous lidocaine (1 RCT), oral venlafaxine (1 RCT) and inhaled nitrous oxide (1 RCT). Meta-analysis suggested a modest but statistically significant reduction in the incidence of chronic pain after surgery following treatment with ketamine but not gabapentin or pregabalin. Results with ketamine should be viewed with caution since most of the included trials were small (that is < 100 participants per treatment arm), which could lead to the overestimation of treatment effect. AUTHORS' CONCLUSIONS: Additional evidence from better, well designed, large-scale trials is needed in order to more rigorously evaluate pharmacological interventions for the prevention of chronic pain after surgery. Furthermore, available evidence does not support the efficacy of gabapentin, pregabalin, non-steroidal anti-inflammatories, intravenous steroids, oral NMDA blockers, oral mexiletine, intravenous fentanyl, intravenous lidocaine, oral venlafaxine or inhaled nitrous oxide for the prevention of chronic postoperative pain."
    - id: https://openalex.org/W2188590881
      doi: https://doi.org/10.3390/ijms161226151
      title: Mast Cell-Mediated Mechanisms of Nociception
      publication_year: 2015
      relevance_score: 35.248608
      abstract: "Mast cells are tissue-resident immune cells that release immuno-modulators, chemo-attractants, vasoactive compounds, neuropeptides and growth factors in response to allergens and pathogens constituting a first line of host defense. The neuroimmune interface of immune cells modulating synaptic responses has been of increasing interest, and mast cells have been proposed as key players in orchestrating inflammation-associated pain pathobiology due to their proximity to both vasculature and nerve fibers. Molecular underpinnings of mast cell-mediated pain can be disease-specific. Understanding such mechanisms is critical for developing disease-specific targeted therapeutics to improve analgesic outcomes. We review molecular mechanisms that may contribute to nociception in a disease-specific manner."
    - id: https://openalex.org/W2808844694
      doi: https://doi.org/10.1007/s13300-018-0454-9
      title: "Diabetic Gastroparesis: Principles and Current Trends in Management"
      publication_year: 2018
      relevance_score: 27.609097
      abstract: "This article is a comprehensive review of diabetic gastroparesis, defined as delayed or disordered gastric emptying, including basic principles and current trends in management. This review includes sections on anatomy and physiology, diagnosis and differential diagnosis as well as management and current guidelines for treatment of diabetic gastroparesis. Diabetic gastroparesis (DGp) is a component of autonomic neuropathy resulting from long-standing poorly controlled type 1 and type 2 diabetes. The diagnostic workup of DGp first excludes obstruction and other causes including medications that may mimic delayed/disordered gastric emptying. Targeting nutrition, hydration, symptomatic relief and glycemic control are mainstays of treatment for DGp. Additionally, optimal treatment of DGp includes good glycemic management, often involving customizing insulin delivery using basal-bolus insulin and technology, including sensor-augmented pumps and continuous glucose monitoring systems. Prokinetic medications may be helpful in DGp symptoms, although only limited number of medications is currently available in the USA. Selected medication-refractory patients with DGp may benefit from gastric neuromodulation, and some from surgical interventions including pyloric therapies that can also be done endoscopically. As is true of any of the diabetic complications, prevention of DGp by early and optimal glycemic control is more cost-effective.Funding: Hansa Medcell, India."
    - id: https://openalex.org/W2889719465
      doi: https://doi.org/10.3389/fphar.2018.00913
      title: A History of Drug Discovery for Treatment of Nausea and Vomiting and the Implications for Future Research
      publication_year: 2018
      relevance_score: 25.612774
      abstract: "The origins of the major classes of current anti-emetics are examined. Serendipity is a recurrent theme in discovery of their anti-emetic properties and repurposing from one indication to another is a continuing trend. Notably, the discoveries occurred against a background of company mergers and changing anti-emetic requirements. Major drug classes include: (i) Muscarinic receptor antagonists - originated from historical accounts of plant extracts containing atropine and hyoscine with development stimulated by the need to prevent sea-sickness among soldiers during beach landings; (ii) Histamine receptor antagonists - searching for replacements for the anti-malaria drug quinine, in short supply because of wartime shipping blockade, facilitated the discovery of histamine (H1) antagonists (e.g. dimenhydrinate), followed by serendipitous discovery of anti-emetic activity against motion sickness in a patient undergoing treatment for urticaria; (iii) Phenothiazines and dopamine receptor antagonists - investigations of their pharmacology as “sedatives” (e.g. chlorpromazine) implicated dopamine receptors in emesis, leading to development of selective dopamine (D2) receptor antagonists (e.g. domperidone with poor ability to penetrate the blood-brain barrier) as anti-emetics in chemotherapy and surgery; (iv) Metoclopramide and selective 5-hydroxytryptamine3 (5-HT3) receptor antagonists - metoclopramide was initially assumed to act only via D2 receptor antagonism but subsequently its gastric motility stimulant effect (contributing to anti-emetic action) was shown to be due to 5-hydroxytryptamine4 receptor agonism. Pre-clinical studies showed that anti-emetic efficacy against the newly-introduced, highly emetic, chemotherapeutic agent cisplatin was due to antagonism at 5-HT3 receptors. The latter led to identification of selective 5-HT3 receptor antagonists (e.g. granisetron), a major breakthrough in treatment of chemotherapy-induced emesis; (v) Neurokinin1 receptor antagonists - antagonists of the actions of substance P were developed as analgesics but pre-clinical studies identified broad-spectrum anti-emetic effects; clinical studies showed particular efficacy in the delayed phase of chemotherapy-induced emesis. Finally, the repurposing of different drugs for treatment of nausea and vomiting is examined, particularly during palliative care, and also the challenges in identifying novel anti-emetic drugs, particularly for treatment of nausea as compared to vomiting. We consider the lessons from the past for the future and ask why there has not been a major breakthrough in the last 20 years."
    - id: https://openalex.org/W2966674226
      doi: https://doi.org/10.1210/er.2019-00007
      title: "Targeted Therapy for Advanced Thyroid Cancer: Kinase Inhibitors and Beyond"
      publication_year: 2019
      relevance_score: 25.470846
      abstract: "The treatment of advanced thyroid cancer has undergone rapid evolution in the last decade, with multiple kinase inhibitor drug approvals for each subtype of thyroid cancer and a number of other commercially available drugs that have been studied for this indication. Although most of the US Food and Drug Administration (FDA)-approved drugs are antiangiogenic multikinase inhibitors-vandetanib, cabozantinib, sorafenib, lenvatinib-there are two FDA indications that are mutation specific-dabrafenib/trametinib for BRAF-mutated anaplastic thyroid cancer and larotrectinib for NTRK-fusion thyroid cancer. Furthermore, other mutation-specific drugs, immunotherapies, and novel strategies for advanced thyroid cancer are under investigation. Understanding the molecular basis of thyroid cancer, the drugs of interest for treatment of advanced thyroid cancer, and how these drugs can be administered safely and in the appropriate clinical scenario are the topics of this review."
    - id: https://openalex.org/W3147714328
      doi: https://doi.org/10.3390/pharmaceutics13040450
      title: Topical Treatments and Their Molecular/Cellular Mechanisms in Patients with Peripheral Neuropathic Pain—Narrative Review
      publication_year: 2021
      relevance_score: 25.186327
      abstract: "Neuropathic pain in humans results from an injury or disease of the somatosensory nervous system at the peripheral or central level. Despite the considerable progress in pain management methods made to date, peripheral neuropathic pain significantly impacts patients' quality of life, as pharmacological and non-pharmacological methods often fail or induce side effects. Topical treatments are gaining popularity in the management of peripheral neuropathic pain, due to excellent safety profiles and preferences. Moreover, topical treatments applied locally may target the underlying mechanisms of peripheral sensitization and pain. Recent studies showed that peripheral sensitization results from interactions between neuronal and non-neuronal cells, with numerous signaling molecules and molecular/cellular targets involved. This narrative review discusses the molecular/cellular mechanisms of drugs available in topical formulations utilized in clinical practice and their effectiveness in clinical studies in patients with peripheral neuropathic pain. We searched PubMed for papers published from 1 January 1995 to 30 November 2020. The key search phrases for identifying potentially relevant articles were \"topical AND pain\", \"topical AND neuropathic\", \"topical AND treatment\", \"topical AND mechanism\", \"peripheral neuropathic\", and \"mechanism\". The result of our search was 23 randomized controlled trials (RCT), 9 open-label studies, 16 retrospective studies, 20 case (series) reports, 8 systematic reviews, 66 narrative reviews, and 140 experimental studies. The data from preclinical studies revealed that active compounds of topical treatments exert multiple mechanisms of action, directly or indirectly modulating ion channels, receptors, proteins, and enzymes expressed by neuronal and non-neuronal cells, and thus contributing to antinociception. However, which mechanisms and the extent to which the mechanisms contribute to pain relief observed in humans remain unclear. The evidence from RCTs and reviews supports 5% lidocaine patches, 8% capsaicin patches, and botulinum toxin A injections as effective treatments in patients with peripheral neuropathic pain. In turn, single RCTs support evidence of doxepin, funapide, diclofenac, baclofen, clonidine, loperamide, and cannabidiol in neuropathic pain states. Topical administration of phenytoin, ambroxol, and prazosin is supported by observational clinical studies. For topical amitriptyline, menthol, and gabapentin, evidence comes from case reports and case series. For topical ketamine and baclofen, data supporting their effectiveness are provided by both single RCTs and case series. The discussed data from clinical studies and observations support the usefulness of topical treatments in neuropathic pain management. This review may help clinicians in making decisions regarding whether and which topical treatment may be a beneficial option, particularly in frail patients not tolerating systemic pharmacotherapy."
    - id: https://openalex.org/W1602152914
      doi: https://doi.org/10.1111/bph.12023
      title: "Clinical pharmacology of analgesics assessed with human experimental pain models: bridging basic and clinical research"
      publication_year: 2012
      relevance_score: 24.62368
      abstract: "The medical impact of pain is such that much effort is being applied to develop novel analgesic drugs directed towards new targets and to investigate the analgesic efficacy of known drugs. Ongoing research requires cost-saving tools to translate basic science knowledge into clinically effective analgesic compounds. In this review we have re-examined the prediction of clinical analgesia by human experimental pain models as a basis for model selection in phase I studies. The overall prediction of analgesic efficacy or failure of a drug correlated well between experimental and clinical settings. However, correct model selection requires more detailed information about which model predicts a particular clinical pain condition. We hypothesized that if an analgesic drug was effective in an experimental pain model and also a specific clinical pain condition, then that model might be predictive for that particular condition and should be selected for development as an analgesic for that condition. The validity of the prediction increases with an increase in the numbers of analgesic drug classes for which this agreement was shown. From available evidence, only five clinical pain conditions were correctly predicted by seven different pain models for at least three different drugs. Most of these models combine a sensitization method. The analysis also identified several models with low impact with respect to their clinical translation. Thus, the presently identified agreements and non-agreements between analgesic effects on experimental and on clinical pain may serve as a solid basis to identify complex sets of human pain models that bridge basic science with clinical pain research."
    - id: https://openalex.org/W4385068316
      doi: https://doi.org/10.3390/ph16071031
      title: Lower Urinary Tract Disorders as Adverse Drug Reactions—A Literature Review
      publication_year: 2023
      relevance_score: 23.688734
      abstract: "A potential complication of pharmacotherapy for a given patient is the possibility of various side effects of drugs, which are manifested in many ways and constitute iatrogenic causes of diseases. Among the systemic side effects of drugs, there are also those involving the urinary tract, although these are less reported in the literature. The use of numerous drugs-especially of anticholinergics or drugs with anticholinergic potential, opioid analgesics, non-steroidal anti-inflammatory drugs, antidepressants, first-generation antipsychotics (classic neuroleptics) and selected cardiovascular drugs (beta-blockers, thiazides potassium-sparing diuretics, statins), as well as others-may increase the risk of developing urological disorders, such as urinary retention or incontinence, urinary tract infections, urolithiasis, erectile dysfunction in men and retroperitoneal fibrosis. The purpose of this paper is to characterise the abovementioned drug-induced disorders of the lower urinary tract on the basis of a non-systematic literature review."
    - id: https://openalex.org/W3023591122
      doi: https://doi.org/10.3389/fphys.2020.00431
      title: A Bitter Taste in Your Heart
      publication_year: 2020
      relevance_score: 23.040716
      abstract: "The human genome contains ∼29 bitter taste receptors (T2Rs), which are responsible for detecting thousands of bitter ligands, including toxic and aversive compounds. This sentinel function varies between individuals and is underpinned by naturally occurring T2R polymorphisms, which have also been associated with disease. Recent studies have reported the expression of T2Rs and their downstream signaling components within non-gustatory tissues, including the heart. Though the precise role of T2Rs in the heart remains unclear, evidence points toward a role in cardiac contractility and overall vascular tone. In this review, we summarize the extra-oral expression of T2Rs, focusing on evidence for expression in heart; we speculate on the range of potential ligands that may activate them; we define the possible signaling pathways they activate; and we argue that their discovery in heart predicts an, as yet, unappreciated cardiac physiology."
    - id: https://openalex.org/W3155685775
      doi: https://doi.org/10.1016/j.biopha.2021.111563
      title: "On the therapeutic targets and pharmacological treatments for pain relief following spinal cord injury: A mechanistic review"
      publication_year: 2021
      relevance_score: 22.226568
      abstract: "Spinal cord injury (SCI) is globally considered as one of the most debilitating disorders, which interferes with daily activities and life of the affected patients. Despite many developments in related recognizing and treating procedures, post-SCI neuropathic pain (NP) is still a clinical challenge for clinicians with no distinct treatments. Accordingly, a comprehensive search was conducted in PubMed, Medline, Scopus, Web of Science, and national database (SID and Irandoc). The relevant articles regarding signaling pathways, therapeutic targets and pharmacotherapy of post-SCI pain were also reviewed. Data were collected with no time limitation until November 2020. The present study provides the findings on molecular mechanisms and therapeutic targets, as well as developing the critical signaling pathways to introduce novel neuroprotective treatments of post-SCI pain. From the pathophysiological mechanistic point of view, post-SCI inflammation activates the innate immune system, in which the immune cells elicit secondary injuries. So, targeting the critical signaling pathways for pain management in the SCI population has significant importance in providing new treatments. Indeed, several receptors, ion channels, excitatory neurotransmitters, enzymes, and key signaling pathways could be used as therapeutic targets, with a pivotal role of n-methyl-D-aspartate, gamma-aminobutyric acid, and inflammatory mediators. The current review focuses on conventional therapies, as well as crucial signaling pathways and promising therapeutic targets for post-SCI pain to provide new insights into the clinical treatment of post-SCI pain. The need to develop innovative delivery systems to treat SCI is also considered."
    - id: https://openalex.org/W2937983897
      doi: https://doi.org/10.1124/jpet.118.255828
      title: Oral Drug Delivery Technologies—A Decade of Developments
      publication_year: 2019
      relevance_score: 19.99333
    - id: https://openalex.org/W2964801204
      doi: https://doi.org/10.1002/prp2.504
      title: Novel natural and synthetic inhibitors of solute carriers SGLT1 and SGLT2
      publication_year: 2019
      relevance_score: 19.907625
      abstract: "Abstract Selective analogs of the natural glycoside phloridzin are marketed drugs that reduce hyperglycemia in diabetes by inhibiting the active sodium glucose cotransporter SGLT2 in the kidneys. In addition, intestinal SGLT1 is now recognized as a target for glycemic control. To expand available type 2 diabetes remedies, we aimed to find novel SGLT1 inhibitors beyond the chemical space of glycosides. We screened a bioactive compound library for SGLT1 inhibitors and tested primary hits and additional structurally similar molecules on SGLT1 and SGLT2 (SGLT1/2). Novel SGLT1/2 inhibitors were discovered in separate chemical clusters of natural and synthetic compounds. These have IC 50 ‐values in the 10‐100 μmol/L range. The most potent identified novel inhibitors from different chemical clusters are (SGLT1‐IC 50 Mean ± SD, SGLT2‐IC 50 Mean ± SD): (+)‐pteryxin (12 ± 2 μmol/L, 9 ± 4 μmol/L), (+)‐ε‐viniferin (58 ± 18 μmol/L, 110 μmol/L), quinidine (62 μmol/L, 56 μmol/L), cloperastine (9 ± 3 μmol/L, 9 ± 7 μmol/L), bepridil (10 ± 5 μmol/L, 14 ± 12 μmol/L), trihexyphenidyl (12 ± 1 μmol/L, 20 ± 13 μmol/L) and bupivacaine (23 ± 14 μmol/L, 43 ± 29 μmol/L). The discovered natural inhibitors may be further investigated as new potential (prophylactic) agents for controlling dietary glucose uptake. The new diverse structure activity data can provide a starting point for the optimization of novel SGLT1/2 inhibitors and support the development of virtual SGLT1/2 inhibitor screening models."
    - id: https://openalex.org/W2058201309
      doi: https://doi.org/10.1590/1414-431x20142890
      title: Modulatory effects of taurine on jejunal contractility
      publication_year: 2014
      relevance_score: 18.766636
      abstract: "Taurine (2-aminoethanesulfonic acid) is widely distributed in animal tissues and has diverse pharmacological effects. However, the role of taurine in modulating smooth muscle contractility is still controversial. We propose that taurine (5-80 mM) can exert bidirectional modulation on the contractility of isolated rat jejunal segments. Different low and high contractile states were induced in isolated jejunal segments of rats to observe the effects of taurine and the associated mechanisms. Taurine induced stimulatory effects on the contractility of isolated rat jejunal segments at 3 different low contractile states, and inhibitory effects at 3 different high contractile states. Bidirectional modulation was not observed in the presence of verapamil or tetrodotoxin, suggesting that taurine-induced bidirectional modulation is Ca(2+) dependent and requires the presence of the enteric nervous system. The stimulatory effects of taurine on the contractility of isolated jejunal segments was blocked by atropine but not by diphenhydramine or by cimetidine, suggesting that muscarinic-linked activation was involved in the stimulatory effects when isolated jejunal segments were in a low contractile state. The inhibitory effects of taurine on the contractility of isolated jejunal segments were blocked by propranolol and L-NG-nitroarginine but not by phentolamine, suggesting that adrenergic β receptors and a nitric oxide relaxing mechanism were involved when isolated jejunal segments were in high contractile states. No bidirectional effects of taurine on myosin phosphorylation were observed. The contractile states of jejunal segments determine taurine-induced stimulatory or inhibitory effects, which are associated with muscarinic receptors and adrenergic β receptors, and a nitric oxide associated relaxing mechanism."
    - id: https://openalex.org/W2148901974
      doi: https://doi.org/10.1111/jphp.12026
      title: Effects of berberine on rat jejunal motility
      publication_year: 2013
      relevance_score: 17.978638
      abstract: "OBJECTIVES: The aim of the study was to evaluate berberine-induced bidirectional regulation on the contractility of jejunum. METHODS: Different low and high contractile states of isolated jejunal segment from rat were established to investigate the effects of berberine. KEY FINDINGS: Stimulatory effects on jejunal segment were exerted by berberine in six low contractile states and inhibitory effects were produced on jejunal segment in six high contractile states. The effects of berberine on myosin light chain kinase (MLCK) mRNA expression, MLCK protein content, and myosin phosphorylation in jejunum were also bidirectional. Bidirectional regulation was not observed in the presence of tetrodotoxin. No regulatory effects of berberine on jejunal contractility were observed in the presence of verapamil. The stimulatory effects of berberine on jejunal contractility were blocked by atropine. The inhibitory effects of berberine on jejunal contractility were abolished by phentolamine, propranolol and L-NG-nitro-arginine, respectively. CONCLUSIONS: Berberine-induced bidirectional regulation needed the presence of the enteric nervous system, and depended on the influx of extracellular Ca(2+) , related to the cholinergic system while jejunum was in low contractile states, and related to the adrenergic system and nitric oxide relaxing mechanism while jejunum was in high contractile states. The results suggested the potential clinical implication of berberine for alternating-type irritable bowel syndrome."
    - id: https://openalex.org/W2148997778
      doi: https://doi.org/10.1186/1471-2202-14-41
      title: "Method parameters’ impact on mortality and variability in rat stroke experiments: a meta-analysis"
      publication_year: 2013
      relevance_score: 16.577631
      abstract: "BACKGROUND: Even though more than 600 stroke treatments have been shown effective in preclinical studies, clinically proven treatment alternatives for cerebral infarction remain scarce. Amongst the reasons for the discrepancy may be methodological shortcomings, such as high mortality and outcome variability, in the preclinical studies. A common approach in animal stroke experiments is that A) focal cerebral ischemia is inflicted, B) some type of treatment is administered and C) the infarct sizes are assessed. However, within this paradigm, the researcher has to make numerous methodological decisions, including choosing rat strain and type of surgical procedure. Even though a few studies have attempted to address the questions experimentally, a lack of consensus regarding the optimal methodology remains. METHODS: We therefore meta-analyzed data from 502 control groups described in 346 articles to find out how rat strain, procedure for causing focal cerebral ischemia and the type of filament coating affected mortality and infarct size variability. RESULTS: The Wistar strain and intraluminal filament procedure using a silicone coated filament was found optimal in lowering infarct size variability. The direct and endothelin methods rendered lower mortality rate, whereas the embolus method increased it compared to the filament method. CONCLUSIONS: The current article provides means for researchers to adjust their middle cerebral artery occlusion (MCAo) protocols to minimize infarct size variability and mortality."
```
/answer 9e0052cc-b7fd-4a97-a064-6f25a51ed682 allow
Control Request:
```yaml
id: 2ecf6b27-a1c0-435b-9519-e7aa16917113
toolName: openalex-search
arguments:
  query: diphenhydramine sodium channel inactivated state binding kinetics neuron Kim Brain Research
  reason: Find rate constants for DPH binding to inactivated Na+ channel state
  fields: abstract
```
/answer 2ecf6b27-a1c0-435b-9519-e7aa16917113 allow
Control Request:
```yaml
id: 78d69d39-e90a-48e0-8ccd-5cf57303cffa
toolName: openalex-search
arguments:
  query: diphenhydramine block sodium current rat neurons GH3 cells Kuo Mol Pharmacol 2000
  reason: Locate exact paper for DPH Na+ channel kinetic rate constants
  fields: abstract
```
/answer 78d69d39-e90a-48e0-8ccd-5cf57303cffa allow
Control Request:
```yaml
id: 59f79cc6-b2bf-4f14-8652-5f583dd25858
result:
  structuredContent:
    count: 0
    returned: 0
    page: 1
    per_page: 25
    results: []
```
/answer 59f79cc6-b2bf-4f14-8652-5f583dd25858 allow
Control Request:
```yaml
id: af1ca269-9f97-4c59-bce4-cda53892377d
toolName: web-search-exa
arguments:
  query: diphenhydramine Na+ channel Kd inactivated state recovery kinetics onset offset rate constant use-dependent block
  reason: Find quantitative on/off rate constants for DPH use-dependent Na+ channel block
```
/answer af1ca269-9f97-4c59-bce4-cda53892377d allow
ReasoningToken: 1176
Control Request:
```yaml
id: d8766604-73c1-4a88-9784-99fd4a904315
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
      Local anesthetics exert their effect by preventing the generation and the conduction of the sensory
      ...
      The nerve conduction block
      ...
      is mainly caused by
      ...
      voltage-gated sodium channels in the nerve membrane [6]. Likewise the local anesthetic activity of diphenhyd
      ...
      may arise from sodium channel inhibition.
      ...
      the interaction of diphenhyd
      ...
      with sodium channels has
      ...
      reported. Batrachotoxin (BTX) is a depolarizing agent that causes persistent activation of sodium channels at the resting membrane potential by altering the voltage sensitivity of both activation and inactivation of the sodium channels [5]. Diphenhydramine inhibited BTX-elicited sodium influx, BTX-induced depolarization and the binding of BTX to sodium channels in guinea pig cerebral cortical synaptoneurosomes [7], [17
      ...
      Recently, it was demonstrated that diphenhydramine inhibited sodium currents in hippocampal neurons by binding preferentially to the inactivated channels [16].
      ...
      Even though the local anesthetic property of diphenhydramine is well known, the electrophysiological characteristics of its action on sodium currents in sensory neurons have not been established. The present study characterized the effects of diphenhydramine on the electrophysiological properties of TTX-S and TTX-R sodium currents in acutely dissociated rat DRG neurons. It was found that diphenhydramine inhibited both types of sodium currents in a dose-and use-dependent manner.
      ...
      Typical TTX-S and TTX-R sodium currents are shown in Fig. 1. The currents were evoked by step depolarizations to 0 mV from a holding potential of −80 mV. TTX-S sodium currents exhibited much faster time courses of activation and inactivation than TTX-R sodium currents. Both types of sodium currents were blocked after bath application of diphenhydramine. Fig. 1A and B show the time course of diphenhydramine block of TTX-S and TTX-R sodium currents, respectively.
      ...
      Diphenhydramine caused a reversible blockade of TTX-S and TTX-R sodium currents in rat DRG neurons. The*K*dvalues for the current block were calculated to be 48 and 86 μM for TTX-S and TTX-R sodium currents, respectively, at a holding potential of −80 mV. Thus TTX-S sodium channels appear to be more sensitive to diphenhydramine than TTX-R sodium channels. However, when the holding potential was lowered to remove the effect of diphenhydramine on the steady-state inactivation of the channels, the
      ...
      et al.,
      ...
      94; Pavlidakey et al.,
      ...
      et al.,
      ...
      characteristic of the blockade of Na+ currents (
      ...
      et al., 2
      ...
      et al., 2
      ...
      00), which is one of the major mechanisms of local anesthesia, produces spinal anesthesia, peripheral nerve block, and
      ...
      05).
      ...
      study of diphenhyd
      ...
      or pheniramine on spinal anesthesia has been reported

      ---

      Title: Block of sodium currents in rat dorsal root ganglion ...
      URL: https://pubmed.ncbi.nlm.nih.gov/11036158/
      Published: N/A
      Author: N/A
      Highlights:
      To elucidate the local anesthetic mechanism of diphenhydramine, its effects on tetrodotoxin-sensitive (TTX-S) and tetrodotoxin-resistant (TTX-R) sodium currents in rat dorsal root ganglion (DRG) neurons were examined by the whole-cell voltage clamp method. Diphenhydramine blocked TTX-S and TTX-R sodium currents with K(d) values of 48 and 86 microM, respectively, at a holding potential of -80 mV. It shifted the conductance-voltage curve for TTX-S sodium currents in the depolarizing direction but had little effect on that for TTX-R sodium currents. Diphenhydramine caused a shift of the steady-state inactivation curve for both types of sodium currents in the hyperpolarizing direction. The time-dependent inactivation became faster and the recovery from the inactivation was slowed by diphenhydramine in both types of sodium currents. Diphenhydramine produced a profound use-dependent block when the cells were repeatedly stimulated with high-frequency depolarizing pulses. The use-dependent block was more pronounced in TTX-R sodium currents. The results show that diphenhydramine blocks sodium channels of sensory neurons similarly to local anesthetics.

      ---

      Title: Classification of Drugs Based on Properties of Sodium Channel Inhibition: A Comparative Automated Patch-Clamp Study | PLOS One
      URL: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0015568
      Published: 2010-12-20T00:00:00.000Z
      Author: N/A
      Highlights:
      A comparative electrophysiological study of 35 compounds, including classic sodium channel inhibitors (anticonvulsants, antiarrhythmics and local anesthetics), as well as antidepressants, antipsychotics and neuroprotective agents, was carried out using rNav1.2 expressing HEK-293 cells and the QPatch automatic patch-clamp instrument. In the multi-dimensional space defined by the eight properties of inhibition (resting and inactivated affinity, potency, reversibility, time constants of onset and offset, use-dependence and state-dependence), at least three distinct types of inhibition could be identified; these probably reflect distinct modes of action. The compounds were clustered similarly in the multi-dimensional space defined by relevant chemical properties, including measures of lipophilicity, aromaticity, molecular size, polarity and electric charge. Drugs of the same therapeutic indication typically belonged to the same type. We identified chemical properties, which were important in determining specific properties of inhibition. State-dependence correlated with lipophilicity, the ratio of the neutral form of molecules, and aromaticity: We noticed that the highly state dependent inhibitors had at least two aromatic rings, logP>4.0, and pKa<8.0.
      ...
      From the first protocol, where 5 Hz trains of depolarizations were applied, we extracted potency, reversibility, time constants of onset and offset and use-dependence. Affinity to hyperpolarized state (commonly termed “resting state affinity”; Kr), affinity to depolarized states (commonly termed “inactivated state affinity”; Ki), and state dependence (calculated from the ratio of Kr and Ki) were extracted from “steady-state” availability curves (for details of the protocol, see Materials and Methods).
      ...
      We measured inhibition (Inh; from which we calculated IC50 values as described in Materials and Methods), reversibility of inhibition (Rev) and use-dependence (UD), as well as time constant of onset (τon) and offset (τoff). The calculation of IC50, quantification of Rev and UD, and the determination of time constants are illustrated in Figure 1A. Because τon should be concentration-dependent if we assume a single binding reaction, we excluded it from the analyses. Reversibility measured by the QPatch instrument did not match reversibility values obtained by classic patch clamp (data not shown). It has been observed that washout of lipophilic compounds is delayed in automated electrophysiology platforms (e.g. [25]). However, reversibility even under these experimental conditions is a useful source of information regarding the physicochemical properties of drugs. Comments on the interpretation of these properties (Rev, τon and UD) are in Results S1.
      ...
      were evoked by a 10 ms test pulse to −10 mV, preceded by 400 ms pre-pulses from −150 to −30 mV. The holding potential was −120 mV. Because the inhibition at hyperpolarized potentials (Inh−150), and the shift of the availability curves (ΔV1/2) are both concentration-dependent properties, we calculated affinities to hyperpolarized and depolarized states (“resting state affinity”: Kr, and “inactivated state affinity”: Ki), which, on the other hand, are
      ...
      ‘Type 1’ (Figure 1A) drugs had high potency (Ki 0.73 to 6.1 µM; IC50 14 to 43 µM), slow onset and offset kinetics (time constants between 10 and 53 s), partial reversibility (between 0.2 and 0.6) and use-dependence (1.09 to 1.66). Drugs belonging to this type were mostly antidepressants: fluoxetine, sertraline, paroxetine, amitriptyline, imipramine, desipramine and maprotiline, as well as the antipsychotic haloperidol, and the anxiolytic ritanserin.
      ...
      It is apparent that more potent drugs (whether potency was measured by Kr, Ki− Kapp, Ki−ΔV1/2 or IC50) tended to have slower onset and offset kinetics, tended to be less reversible, and tended to be more use-dependent. High inactivated state affinity (low Ki) predicted high state-dependence, while high resting affinity (low Kr) did not.
      ...
      Time constants were determined by aromaticity, lipophilicity and the size of the molecule: large, lipophilic molecules with multiple aromatic rings had slower onset/offset kinetics. From the descriptors which quantify different aspects of molecular size, minimum projection area was found to show somewhat higher correlation than molecular weight (Figure 4N–O). Larger molecules were also found to be more potent (Figure 4P), which may partly be due to the fact that larger molecules are also more lipophilic.
      ...
      Partition coefficient (logP) was a major determinant of potency, kinetics and reversibility. Lipophilic molecules tended to be more potent in terms of Kr, Ki and IC50 (measured at -90 mV, using the 5 Hz train protocol) values; in addition the inhibition was less reversible, with slower onset and offset kinetics. This is in accordance with studies on structure-activity relationships, where a linear relationship between logP and logIC50 values were described based on the inhibition of action potentials [17], [27] and of [3H]BTX binding [15], [16], [18]. A similar relationship between lipophilicity and potency has been shown for a number of other transmembrane proteins [28], [29], [30].
      ...
      On the other hand, if we consider resting affinity, we can notice that positively charged SCIs tended to be more potent. The finding, that positively charged molecules are better inhibitors of resting channels irrespectively of the lipophilicity of the charged form (Kr did not depend on logD7.3), suggests that in resting inhibition an interaction of the charged form and the channel occurs within a polar environment. The major determinant of resting affinity was found to be pKa, indicating the importance of positive charge in resting inhibition. It was also the most important determinant of use-dependence, which is in accordance with previous studies, where positively charged molecules had slower kinetics and showed more use-dependence [4], [17], [20], [21], [31], [32].
      ...
      The third major determinant of state-dependence is aromaticity. While resting affinity was not dependent on the number of aromatic rings, inactivated affinity showed a definite dependence. This suggests that interactions between aromatic rings (π-π interactions) are important in binding to inactivated state. Aromaticity also determined time constants and reversibility. This may be one explanation of the finding that dimers of lidocaine (containing two aromatic rings) show both increased potency and decreased reversibility [33].
      ...
      The role of aromaticity of the most important residue of the local anesthetic binding site (Phe1710 in rNav1.3) in use-dependent- but not resting inhibition has been shown by different amino acid substitutions. For resting inhibition hydrophobicity of the residue was sufficient, while effective use-dependent inhibition required that the residue was aromatic [34]. The role of the aromatic ring has also been investigated by using unnatural derivatives of phenylalanine (Phe1579 in rNav1.4) in which the π electron clouds were distorted. This affected use-dependent inhibition, and recovery from inactivated state, but left tonic inhibition (resting affinity) intact [10]. These results could be explained by either cation-π or π-π interactions. Our results support the role of π-π interaction, which is consistent with single channel analysis of the inhibition by local anesthetics; two distinct types of inhibition were observed at single channel level: rapid block (manifested as decreased single-channel conductance), and discrete block (appearance of distinct closed periods). The former could be reproduced by the charged amine fraction of local anesthetics, while phenol, which resembles the aromatic part of local anesthetics, caused discrete block [35]. Mutation of the phenylalanine residue (Phe1579 in rNav1.4) abolished discrete block, while not affecting rapid block [12].

      ---

      Title: Inhibition of Na +  Current by Imipramine and Related Compounds: Different Binding Kinetics as an Inactivation Stabilizer and as an Open Channel Blocker
      URL: https://molpharm.aspetjournals.org/content/62/5/1228
      Published: N/A
      Author: N/A
      Highlights:
      Use-dependent block of Na+channels plays an important role in the action of many medications, including the anticonvulsants phenytoin, carbamazepine, and lamotrigine. These anticonvulsants all slowly yet selectively bind to a common receptor site in inactivated but not resting Na+channels, constituting the molecular basis of the use-dependent block. However, it remains unclear what channel gating process “makes” the receptor, where the receptor is located, and how the slow drug binding rate (to the inactivated channels) is contrived. Imipramine has a diphenyl structural motif almost identical to that in carbamazepine (a dibenzazepine tricyclic compound), as well as a tertiary amine chain similar to that in many prototypical local anesthetics, and has also been reported to inhibit Na+channels in a use-dependent fashion. We found that imipramine selectively binds to the inactivated (dissociation constant ∼1.3 μM) rather than the resting Na+channels (dissociation constant &gt;130 μM). Moreover, imipramine rapidly blocks open Na+channels, with a binding rate ∼70-fold faster than its binding to the inactivated channels. Similarly, carbamazepine and diphenhydramine are open Na+channel blockers with faster binding rates to the open than to the inactivated channels. These findings indicate that the anticonvulsant receptor responsible for the use-dependent block of Na+channels is located in or near the pore (most likely in the pore mouth) and is made suitable for drug binding during channel activation. The receptor, however, continually changes its conformation in the subsequent gating process, causing the slower drug binding rates to the inactivated Na+channels.

      ---

      Title: Frontiers | Characterization of Compound-Specific, Concentration-Independent Biophysical Properties of Sodium Channel Inhibitor Mechanism of Action Using Automated Patch-Clamp Electrophysiology
      URL: https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2021.738460/full
      Published: 2021-08-23T00:00:00.000Z
      Author: N/A
      Highlights:
      the concentration. Our aim in this study was to quantify these properties. Primary biophysical data, such as onset rate, the shift of the half inactivation voltage, or the delay of recovery from inactivation, are concentration-dependent. We wanted to derive compound-specific properties, therefore, we had to neutralize the effect of concentration. This study describes how this is done, and shows how compound-specific properties reflect the mechanism of action, including binding dynamics, cooperativity, and interaction with the membrane phase. We illustrate the method using four well-known sodium channel inhibitor compounds, riluzole, lidocaine, benzocaine, and bupivacaine. Compound-specific biophysical properties may also serve as a basis for deriving parameters for kinetic modeling of drug action. We discuss how knowledge about the mechanism of action may help to predict the frequency-dependence of individual compounds, as well as their potential persistent current component selectivity. The analysis method described in this study, together with the
      ...
      We used a complex 17-pulse voltage protocol (Figure 1A), described in detail in the accompanying paper (Lukacs et al., 2021), which allowed the assessment of gating kinetics and gating equilibrium in the absence and the presence of inhibitor/modulator compounds. The protocol investigated the effect of different durations of depolarizations: 2.5, 7.5, 22.5, and 67.5 ms with 2.5 ms hyperpolarizing gaps between them; this section (pulses #1 to #5) is shown by different shades of green in Figure 1, and was named “state-dependent onset” (SDO). Next, pulses #6 to #12, as well as #1 investigated the effect of different durations of hyperpolarizations (1, 2, 4, 8, 16, 32, 64, and 498 ms, separated by 5 ms depolarizations) in the section shown by different shades of blue, and named “recovery from inactivation” (RFI). Finally, pulses #12 to #17 assessed the resting-inactivated equilibrium at different membrane potentials in the section named “steady-state inactivation” (SSI). The three sections were similar to protocols we used in previous studies (Lukacs et al., 2018; Földi et al., 2021).
      ...
      In the accompanying paper (Lukacs et al., 2021) we describe how different degrees of inhibition observed in the 17-pulse protocol can be interpreted as revealing the state-dependent onset (SDO; how the inhibition depended on the length of depolarizations), the recovery from inactivation (RFI; how the inhibition depended on the length of hyperpolarizations), and steady-state inactivation (SSI; how the inhibition depended on the membrane potential). We have distinguished “macro-dynamics,” which was the onset/offset upon drug perfusion and removal, and occurred on the second-timescale; and “micro-dynamics,” which was the onset/offset upon conformational transitions of the channel population, and occurred on the millisecond timescale. In this study we focus on micro-dynamics. We first explain the sequence of analysis on the example of riluzole (in four different concentrations) using data from a single cell ensemble. Then we show the same analysis on examples for three additional compounds in order to demonstrate how similar compounds may radically differ in their micro-dynamics. Finally, we show how these compound-specific biophysical properties may affect their action at actively firing excitable cells.
      ...
      Lidocaine (Figure 3) showed a slower micro-onset than riluzole. SDO ratio plots indicate that at 100 and 300 µM the onset did not reach its maximum even at the longest depolarization (67.5 ms) of the 17-pulse protocol. The recovery was also slower, substantial recovery only started after ∼10 ms of hyperpolarization, and continued up to ∼500 ms.
      ...
      The fastest micro-dynamics we have encountered thus far was shown by benzocaine (Figure 4). Recovery in fact was so fast that it compromised the measurement of SDO. At 2 ms gap duration, ∼70–90% of the channels have already recovered, therefore the 2.5 ms gap used in the SDO protocol was unable to reveal most of the inhibition caused by benzocaine binding. Although the plots of SDO ratios show the onset only on the remaining ∼10–30% of channels, it is still discernible that the full onset has been completed within the shortest (2.5 ms) pulse. Calculation of KI from SSI data (see Table 1) indicates that in fact more than half of the channels are inhibited by 100 µM of benzocaine, but this inhibition is difficult to detect whenever we use a hyperpolarizing gap before the test pulse.
      ...
      Benzocaine is known as one of the fastest-acting sodium channel inhibitors, due to its small size and neutrality. Indeed, it is one of the few compounds, for which the whole process of partitioning, entry through the fenestration, and binding to the local anesthetic site has been observed in molecular dynamics simulations (Boiteux et al., 2014; Martin and Corry, 2014). In our experiments we found extremely fast micro-offset kinetics, the offset was complete within 4 ms, and even the shortest interpulse interval (1 ms) already showed decreased potency (291 ± 22 μM, while the calculated KI was 79.4 ± 3.9 µM). This was the reason, why the SDO protocol only detected a small fraction of the onset of drug action. Even though depolarization must have caused a definite increase in EIP, as we can see from the membrane potential dependence of EIP (Figure 4), the 2.5 ms hyperpolarizing gap between pulses was enough to allow almost full recovery. Experimental results (which failed to detect the onset) are shown by open circles connected by a dotted line (Figure 2B), while we suppose that the actual dynamics of micro-onset must have been complete within a few milliseconds (dashed line in Figure 2B). It follows that significant frequency-dependence cannot be expected in the case of benzocaine, only at extremely high (>100 Hz) firing frequencies.
      ...
      While benzocaine is a smaller, neutral compound that acts much faster than lidocaine, bupivacaine is larger, and has a higher pKa than lidocaine (therefore a somewhat larger fraction is charged at neutral pH). In an earlier comparative study, we found it to have higher potency, and slower onset/offset kinetics (only macro-dynamics was studied) (Lenkey et al., 2010). In this study, we found that although its macro-dynamics was still relatively fast (macro-offset time constants were 1.72 ± 0.05 s for lidocaine, and 3.56 ± 0.43 s for bupivacaine, see Table 1), its micro-dynamics was slow, and therefore its EIP varied within a strikingly shallow range (between 27.3 ± 1.45 and 94.6 ± 10.7 µM). The KR/KI ratio was only 7.48 (while for riluzole, lidocaine, and benzocaine, it was 242, 69.7, and 28.3, respectively). This can also be seen on the concentration-inhibition curves (Figure 5), where the 17 different curves are very close to each other. The reason for a shallow micro-dynamics may be either that complete micro-onset of inhibition would require a depolarization even longer than 64 ms, or that the complete micro-offset would require a hyperpolarization even longer than 498 ms. Considering estimations of KR and KI from the literature [KR ≈ 317.4 µM, and KI ≈ 18.6 µM (Vladimirov et al., 2000); KR ≈ 618.9 µM, and KI ≈ 5.85 µM (Lenkey et al., 2010)], both could be the case for bupivacaine, therefore a more accurate assessment of its range of EIS values would require a protocol containing both longer depolarizations and longer hyperpolarizations. We presume that micro-onset and micro-offset both must be complete within 2–3 s since these processes cannot be slower than macro-offset, for which we observed a time constant of 3.56 s (Table 1). In the case of the simulated neuron firing at ∼25 Hz, we suppose that development of inhibition would require several tens of action potentials, and cells would not substantially recover from inhibition between two action potentials unless the firing rate was less than 1 Hz.

      ---

      Title: Fast- or Slow-inactivated State Preference of Na+ Channel ...
      URL: https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1000818
      Published: 2010-06-17T05:01:08.000Z
      Author: N/A
      Highlights:
      Special voltage protocols are used to evoke and study the slow-inactivated state. Availability of channels is studied after a prolonged depolarization (to induce slow inactivation), followed by a hyperpolarizing gap (to allow recovery from fast, but not slow inactivation). Because availability in such protocols is solely determined by the extent of slow inactivation, a drug that decreases availability is considered to be slow-inactivated state-preferring. However, gating rates (the rate of inactivation and rate of recovery from inactivation) are altered by drug binding. A fast-inactivated state-preferring drug stabilizes this state by delaying recovery. A delayed recovery does not necessarily indicate actual modification of the gating rate. For example if the bound drug prevents recovery from inactivation, then recovery will appear to be slowed because the drug needs first to dissociate [24], [25]. In our current study, however, we chose to use a model according to the modulated receptor hypothesis [26], [27], i.e., the change in affinity equals the actual modification of the gating rates. For this reason in our model increased affinity is synonymous with state stabilization. Altered gating rates have been experimentally demonstrated using gating charge measurements [28], [29]. Because of the altered gating, the rate of recovery from fast inactivation in the presence of the drug can easily overlap with the rate of recovery from slow-inactivated state. The rate of state-dependent association and dissociation of the drug should also be taken into account. As a result, interpretation of data obtained with these protocols is not straightforward (e.g. [9], [30]).
      ...
      For simulations two different kinds of models were used: a phenomenological Hodgkin-Huxley type model and a state model similar to the one published by Kuo and Bean [31]. In both models, however, we introduced slow-inactivated states and drug-bound states with altered gating transition rates. For a detailed description of the models see Methods and Text S1. The Hodgkin-Huxley type model, which will be referred to as the “tetracube” model because of its topology (see Methods), was used for most simulations. The Kuo-Bean type model, referred to as the “multi-step-activation” (MSA) model, was only used for testing the robustness of our observations. In the models, both the degree of alteration of the transition rates and the state preference (the difference between affinities for different states) were given by a single factor CF (for fast-inactivated state-preferring drugs) or CS (for slow-inactivated state-preferring drugs). The kinetics of association and dissociation to the resting state are defined by the rate constants ka and kd, respectively. Association and dissociation rate constants to other states were calculated as described in Methods.
      ...
      “Rec_t” (“Recovery from inactivation as a function of time”) monitors recovery after a 5 s depolarization to −20 mV as a function of hyperpolarizing gap duration (the gap is between the 5 s pre-pulse and the test pulse). In the absence of drugs, a 5 s depolarization causes both fast and slow inactivation (approximately 45–55%, respectively), and the protocol monitors recovery from both states. The time constants for recovery were 2.21 and 58.25 ms [32]. In the presence of drugs, measured recovery reflects the combination of dissociation and recovery from both inactivated states.
      ...
      of binding and gating, we simulated four prototypical mechanisms: either the fast- or the slow-inactivated state was preferred by the drug (“FI” and “SI”, respectively), and the drug had either fast or slow binding kinetics (“fb” and “sb”, respectively). Fast-inactivated state preference was introduced by setting CF = 10 (with CS = 1). Slow-inactivated state-preferring drugs were defined by CS = 10 (CF = 1). Association and dissociation rate constants for drugs with fast binding kinetics were set to the values: ka = 0.5 s−1µM−1 and kd = 100 s−1, while slow binding kinetics were defined as ka = 0.005 s−1µM−1 and kd = 1 s−1. The term “fast” is relative, of course. All SCIs associate relatively slowly compared to hydrophilic drugs that bind to a readily accessible extracellular site. We chose these values so that they would be close to the rate constants that had been determined in previous studies for classic sodium channel inhibitors (e.g. [12]). Combinations of these properties give the four prototypical “drugs.” Current hypotheses for the mechanism of antidepressant action are represented by either the drug “FI_sb” (fast-inactivated state is stabilized, with slow binding kinetics) or the “SI_fb” drug (slow-inactivated state is stabilized, and binding kinetics are not rate limiting). A
      ...
      In the “Rec_t” protocol, “FI_fb” behaved as expected, affecting only the part of the curve that is responsible for recovery from the fast-inactivated state. However, drug “FI_sb” was as effective as slow-inactivated state-preferring drugs. In experiments using this protocol, the recovery from inhibition is slowed down for two reasons: i) the slow dissociation rate of the drug; and ii) drug-bound channels display a slowed gating. In the case of “FI_sb,” the former seems to be the rate-limiting step and, if dissociation is slow enough, the curve is shifted, whichever state is preferred (Figure 3D).
      ...
      Binding kinetics: We simulated 10 different pairs of rate constants spanning five orders of magnitude from 5*10−4 to 15 µM−1s−1 (ka) and from 0.1 to 3000 s−1 (kd). The ratio of ka and kd was kept constant ka/kd = 5*10−3, ensuring that the affinity of the drug toward the resting channel remained constant.
      ...
      Hyperpolarizing gap duration of the “SInact_t” protocol: In simulations and experiments, we used a 10 ms gap duration, which is enough for a >90% recovery from the fast-inactivated state under control conditions. In the presence of a fast-inactivated state-stabilizing drug, recovery is slowed down. For this reason, in experiments where slow-inactivated state-stabilizing drugs are to be identified, gap duration is often chosen to be of a longer duration (up to 1 s) to ensure that the recovery from fast inactivation is complete. Our simulations indicated that “FI_sb” and “SI” type drugs nevertheless overlap in behavior no matter what hyperpolarizing gap duration is chosen (see Figure 3E). We tested the effect of setting the gap duration to 1 s (Figure 5F). “FI” and “SI” type drugs were no better separated with a 1 s than with the 10 ms gap duration.
      ...
      Nevertheless, the four prototypical mechanisms behaved appreciably differently. For this reason, we investigated the extent to which the two major mechanisms (“FI” and “SI”) could be distinguished using the combined information from different voltage protocols. Based on the nSOD(Rec_t) – nSOD(SInact_t) plots, we concluded that “FI” type drugs can be recognized, provided that their binding kinetics are fast enough. However, “FI” drugs with slower binding kinetics will overlap with “SI” drugs. Determination of the state preference would only be possible if we could measure the binding kinetics of individual drugs. However, distinguishing slow association from association to a slow-inactivated state is not trivial. In order to separate gating kinetics from binding kinetics, a rapid pulse application of the drug is necessary [32], [36]. Even in this case, association and dissociation rates cannot be correctly determined because the drug binding site on sodium channels is not extracellularly localized. Therefore, the onset rate of a drug effect may be determined by multiple processes: aqueous phase – membrane partitioning, outer to inner leaflet translocation, intramembrane diffusion and association, itself. Any one of these may be the rate limiting step, which obscures the microscopic association rate.

      ---

      Title: fphar-2021-738260 1..14
      URL: https://www.frontiersin.org/articles/10.3389/fphar.2021.738260/pdf
      Published: N/A
      Author: N/A
      Highlights:
      a rapid assessment of the mechanism of action of sodium channel inhibitors, including their
      ...
      state-dependent association and dissociation kinetics. The method is based on a complex
      ...
      voltage protocol, which is repeated at 1 Hz. Using this time resolution we could monitor the
      ...
      onset and offset of both channel block and modulation of gating upon drug perfusion and
      ...
      washout. Our results show that the onset and the offset of drug effects are complex
      ...
      processes, involving several steps, which may occur on different time scales. We could
      ...
      identify distinct sub-processes on the millisecond time scale, as well as on the second time
      ...
      Most small-molecule sodium channel inhibitors bind to the local anesthetic binding site, and they are
      ...
      strongly state-dependent, showing ∼10-fold–1,000-fold higher affinity to inactivated channels
      ...
      (Lenkey et al., 2011). For this reason, as it has long been recognized, determining an IC50 value
      ...
      in the case of fluoxetine (Lenkey et al., 2006)), and a shift of the steady-state availability curve caused
      ...
      by drug binding is a common phenomenon. These two phenomena are not only related, but they
      ...
      Abbreviations: Erel, relative error; %RMSE, percentage root mean square error; RFI, “recovery from inactivation” protocol;
      ...
      SDO, “state-dependent onset” protocol; SSI, “steady-state inactivation” protocol.
      ...
      resting-state-, and inactivated-state-affinities (KR and KI) are
      ...
      given for individual compounds. Once KR and KI are known,
      ...
      action potential is fired, sodium channels undergo a series of
      ...
      conformational transitions, and sodium channel inhibitors
      ...
      dynamically associate and dissociate depending on the actual
      ...
      conformational distribution of the channel population. The final
      ...
      effect of the inhibitor will depend on how the firing rate (the
      ...
      temporal pattern of the membrane potential) and binding/
      ...
      unbinding kinetics relate to each other. This is the basis of the
      ...
      certain pain syndromes and epilepsies. When assessing the onset/
      ...
      offset kinetics of a sodium channel inhibitor, one must consider
      ...
      the special position of the local anesthetic binding site: it is located
      ...
      within the central cavity of the channel, accessible only through
      ...
      the lipid membrane. The onset/offset process, therefore, cannot
      ...
      be simplified into a single-step binding/unbinding reaction
      ...
      (Vauquelin, 2016). The onset is often not diffusion-limited,
      ...
      but hindered by other possible rate-limiting steps:
      ...
      deprotonation of charged nitrogens (evidenced by the pHdependence of onset rates (Lazar et al., 2015)), partitioning
      ...
      into the membrane (evidenced by the correlation between
      ...
      lipophilicity and potency (Lenkey et al., 2010; Lenkey et al.,
      ...
      2011)), access to the central cavity through the fenestrations
      ...
      and the activation gate (these open up only at depolarized
      ...
      conformations (Yan et al., 2017)), and formation of the highaffinity binding site (the whole binding pocket is thought to be
      ...
      rearranged at depolarized conformations). Rate limiting steps
      ...
      during offset may include delayed conformational rearrangement
      ...
      of the protein, unbinding, egress from the central cavity, and
      ...
      partitioning of the drug molecule into the extracellular aqueous
      ...
      phase. The last process may be further delayed if the compound
      ...
      has accumulated within intracellular lipid compartments, the
      ...
      depletion of which might require a longer time.
      ...
      In excitable cells sodium channels continuously change their
      ...
      conformations depending on the membrane potential. On the
      ...
      one hand, binding and unbinding of drugs are conformationdependent, on the other hand, drug binding alters
      ...
      conformational transitions (gating) of channels. These
      ...
      interactions produce a special dynamics of continuously
      ...
      changing drug potency: it does not only depend on the actual
      ...
      value of membrane potential, but also on its recent history. To
      ...
      assess both membrane potential dependence and time
      ...
      dependence, we used the protocol illustrated in Figure 1. We
      ...
      choose to study three aspects of membrane potential-dependent
      ...
      dynamics of drug potency: First, the effect of inhibitors often
      ...
      needs some time to develop. In the first section of the protocol
      ...
      (pulse #1–#5), therefore, we intended to assess how fast the effect
      ...
      of the drug develops upon depolarization. We used progressively
      ...
      lengthened depolarizations and monitored the inhibition.
      ...
      Second, inhibitors most often dissociate from hyperpolarized
      ...
      (resting) channel conformation, therefore, drug potency
      ...
      gradually decreases upon prolonged hyperpolarization. In the
      ...
      second section of the protocol (pulses #6–#12) we assessed the
      ...
      dynamics of this recovery using progressively lengthened
      ...
      hyperpolarizations. Third, we assessed quasi-equilibrium
      ...
      conditions: we investigated in this section (pulses #13–#17)
      ...
      how the extent of inhibition depended on the membrane
      ...
      potential. The three sections of the protocol correspond with
      ...
      the protocols “state-dependent onset” (SDO), “recovery from
      ...
      inactivation” (RFI), and “steady-state inactivation” (SSI) we used
      ...
      in previous studies (Lukacs et al., 2018; Földi et al., 2021),
      ...
      although with some significant differences. Our priority with
      ...
      this current protocol was high time resolution.
      ...
      For this reason, the duration of the whole 17-pulse protocol
      ...
      was only 522 ms, and it was repeated every second throughout the
      ...
      experiment. A standard experiment included seven different drug
      ...
      applications, 40 s long each, with 60 or 80 s wash periods between
      ...
      them, then the whole sequence was repeated. This means that the
      ...
      experiment lasted for 28–30 min, during which ∼1,700–1,800
      ...
      sweeps were recorded.
      ...
      In the SDO section of the protocol (pulses #1–#5), we tested
      ...
      the effect of four depolarization durations (besides the control):
      ...
      2.5, 7.5, 22.5, and 67.5 ms. We used a cumulative arrangement,
      ...
      not allowing full recovery between depolarizations (only 2.5 ms at
      ...
      hyperpolarized potential between depolarizations). We used
      ...
      Port-a-Patch experiments (i.e., in gigaseal, single-cell
      ...
      recordings) to verify the effects observed in IonFlux
      ...
      experiments (i.e., in multi-cell recordings with varying seal
      ...
      resistance); and also to compare the effect of this cumulative
      ...
      arrangement of the protocol with the conventional multi-sweep
      ...
      protocol, where all sweeps are started with the whole channel
      ...
      population in resting state. Protocols similar to this one are often
      ...
      used to study slow inactivation. It is important to note that in our
      ...
      experiments the SDO protocol was not intended for the study of
      ...
      slow inactivation, but the study of drug effect onset, upon
      ...
      depolarization-induced conformational change. Depolarized
      ...
      conformations (open and inactivated) provide increased
      ...
      affinity, and/or increased accessibility to the binding site,
      ...
      thereby allowing the development of a new binding/unbinding
      ...
      equilibrium. The protocol investigates how fast this new
      ...
      equilibrium is reached. Slow inactivation may only play a
      ...
      minor role in the development of the effect, since even the
      ...
      experimental conditions. (i) The 17-pulse cumulative protocol used in IonFlux experiments, as described in Figures 1, 3. (ii) The three cumulative protocols used in Porta-Patch experiments. Colors of pulses indicate corresponding pulses in the IonFlux protocol. The SDO protocol was exactly the same as in the IonFlux protocol The SSI
      ...
      section contained an extra 40 ms interpulse interval at −120 mV. The interpulse intervals of the RFI section were: 1, 2, 4, 8, 16, 32, 64, 128, 256, and 512 ms. In
      ...
      contrast, the interpulse intervals in the IonFlux protocol were: 1, 2, 4, 8, 16, 32, 64 ms (preceding the shorter intervals), and 498 ms (time between sweeps). (iii) The three

      ---

      Title: An Inactivation Stabilizer of the Na+ Channel Acts as an Opportunistic Pore Blocker Modulated by External Na+ - PMC
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC2217501/
      Published: N/A
      Author: N/A
      Highlights:
      We have previously demonstrated that carbamazepine and imipramine accelerate macroscopic Na+ current decay in a linear dose-dependent fashion with macroscopic binding rate constants of ∼1.1 × 106 and ∼1.1 × 107 M−1s−1, respectively (Yang and Kuo, 2002). This finding strengthens the view that these use-dependent inhibitors bind to the Na+ channel with a one-to-one binding stoichiometry, and further suggests that carbamazepine and imipramine block the open Na+ channel pore in addition to stabilization of a nonconducting (or inactivated) state connected to the open state. This is because if only the latter case were true, then the forward rate (rate of genesis of this nonconducting state) must be much faster than 330 to 3300 s−1 to sustain the time constant of relaxation observed in the highest concentration (∼300 μM) of carbamazepine and imipramine (Yang and Kuo, 2002). Also, the corresponding backward rate must be quite sizable as compared with the forward rate to sustain the dose-dependent current decrease with time constants of relaxation linearly related to drug concentrations. It is thus hard to conceive such a nonconducting state, because it can be neither the fast inactivated state, which has a very slow backward rate (i.e., very high binding affinity of the inactivation lid to the open channel), nor the slow inactivated state, which usually takes a few hundred milliseconds or seconds to develop. If diclofenac and carbamazepine share the same binding site in Na+ channels, it is intuitive that diclofenac should also block the pore. Surprisingly, we found that diclofenac cannot block the open neuronal Na+ channel pore like what carbamazepine and imipramine do. With its even higher binding affinity to the inactivated channel than carbamazepine, diclofenac in concentrations of 300 μM to 1 mM (43- to 143-fold of K I) does not show any acceleration of the macroscopic current decay as that 300 μM (12-fold of K I) carbamazepine does (Fig. 4 A; Yang and Kuo, 2002). Actually, the current decay is slightly retarded rather than accelerated by diclofenac (Fig. 4, B–D). The significant and concentration-dependent retardation of current decay by diclofenac argues against the possibility that the lack of blocking effect is due to insignificant binding of diclofenac onto the open channel (e.g., the binding rate of diclofenac is too slow or the binding affinity is too low to the open channel). Instead, it seems that diclofenac significantly binds to the open channel and slightly retards channel inactivation without simultaneously blocking the pore. One may also note that the current peak is slightly shifted rightwardly (i.e., the time to current peak is slightly lengthened) and is reduced rather than enhanced despite of possible stabilization of the open channel by high concentrations of diclofenac (Fig. 4, A and B). The slightly rightwardly shifted and reduced peak implies that diclofenac, in such high concentrations, may bind to the resting Na+ channel and consequently slows the activation process upon depolarization, and/or that the diclofenac-bound open channel could still conduct Na+ currents but with a slightly decreased conductance. In any case, there must be significant diclofenac binding to the Na+ channel without blocking the channel pore, so that the gating alterations could be manifest.
      ...
      It is intriguing that diclofenac shares very similar features of Na+ channel gating modification to carbamazepine (Figs. 2 and 3; Kuo et al., 1997), but the effect on ion permeation is fundamentally different between these two drugs (Figs. 4 and 7; Yang and Kuo, 2002). In view of the possibility that the pore-blocking effect may be modulated by permeating ions, we examine the effect of Na+ on the action of carbamazepine and diclofenac. Surprisingly, we found that diclofenac is turned into an effective pore blocker and evidently accelerates the macroscopic neuronal Na+ current decay when the Na+ ions in the external solution are replaced by Cs+ (0 mM external and 150 mM internal Na+; Fig. 8, A and B). The onset of the effect is very rapid (Fig. 8 C), exactly analogous to the effect of carbamazepine in 150 mM external Na+ (Yang and Kuo, 2002). The linear correlation between the acceleration of current decay and the diclofenac concentration indicates a simple bimolecular reaction and gives a diclofenac binding rate constant of 4.1 × 105 M−1s−1 onto the open neuronal Na+ channel. This value is close to the previously reported binding rate constant of carbamazepine to the open channel (1.1 × 106 M−1s−1; Yang and Kuo, 2002). Actually the binding rate constants to the inactivated Na+ channel are also similar between these two drugs, and are ∼15–30 times slower than binding to the open channel in both cases (unpublished data; Kuo et al., 1997). In any case, it is clear that carbamazepine is always an open channel pore blocker and accelerates the macroscopic current decay irrespective of the external Na+ concentration, but diclofenac is a more versatile or an “opportunistic” pore blocker modulated by the Na+ ion in the external solution (Fig. 8 D). At first glance, the fundamentally different effects of diclofenac and carbamazepine on ion permeation in 150 mM external Na+ may seem to suggest two different sites for these two drugs. The mutual exclusion between binding of the two drugs then would be more likely ascribable to an allosteric rather than a direct interaction. However, the finding that diclofenac is turned into a pore blocker and shows an effect exactly analogous to carbamazepine in the absence of external Na+ would favor the possibility of a common binding site and a direct interaction between these two drugs again. In any case, the intriguing opportunistic pore-blocking effect strongly suggests that there is a binding site for the use-dependent Na+ channel inhibitor at the junction of the widened external vestibule and the narrowed part of the pore (see discussion and Fig. 11).
      ...
      Na+ channel (Figs. 2 and 6), very much analogous to the action of anticonvulsants carbamazepine, phenytoin, and lamotrigine (Kuo and Bean, 1994; Kuo and Lu, 1997; Kuo et al., 1997). Diclofenac thus is also a use-dependent inhibitor with one-to-one binding stoichiometry (Fig. 8 C) to the Na+ channel. However, diclofenac does not completely mimic the action of carbamazepine to block the open Na+ channel pore (Yang and Kuo, 2002). Diclofenac cannot block the pore in the presence of 150 mM external Na+ (Figs. 4–7), but is turned into an effective pore blocker with decreased external Na+ concentration (Figs. 8 and 10). We further show that the “opportunistic” pore-blocking effect of diclofenac is chiefly modulated by external Na+, but has little to do with internal Na+ or the direction of current flow (Figs. 8–10). Given its capability of blocking the pore at least in some experimental conditions, diclofenac should have its binding site in the ion conduction pathway of the Na+ channel. The findings that only external but not internal Na+ has an modulatory effect on the binding conformation of diclofenac would further limit the diclofenac binding site to a pore region that is effectively occupied by only external but not internal Na+ (see below). The diclofenac binding site thus must be located very “superficially” in the pore (i.e., at the external pore mouth). In the meanwhile, the opportunistic blocking effect would require diclofenac to bind to a site at the junction of a widened and a narrow part of the ion conduction pathway, so that its pore-blocking effect can be readily and drastically altered by some, presumably mild or modest, local conformational changes induced by Na+ binding (Fig. 11). Altogether these findings strongly indicate that diclofenac, a use-dependent inhibitor of the Na+ channel, binds to a site at the junction of the widened external vestibule and the narrow (possibly the selectivity filter, see below) part of

      ---

      Title: pone.0015568 1..17
      URL: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0015568&type=printable
      Published: N/A
      Author: N/A
      Highlights:
      . In the multi-dimensional space defined by the eight properties of inhibition (resting and inactivated affinity,
      ...
      potency, reversibility, time constants of onset and offset, use-dependence and state-dependence), at least three distinct
      ...
      could be identified;
      ...
      modes of action. The
      ...
      type. We identified chemical properties, which were important in determining specific properties of inhibition. Statedependence correlated with lipophilicity, the ratio of the neutral form of molecules, and aromaticity: We noticed that the
      ...
      had at least two aromatic rings
      ...
      logP.
      ...
      , and pKa
      ...
      From the first protocol, where 5 Hz trains of depolarizations
      ...
      were applied, we extracted potency, reversibility, time constants of
      ...
      onset and offset and use-dependence. Affinity to hyperpolarized
      ...
      state (commonly termed ‘‘resting state affinity’’; Kr), affinity to
      ...
      depolarized states (commonly termed ‘‘inactivated state affinity’’;
      ...
      ), and state dependence (calculated from the ratio of Kr and Ki)
      ...
      were extracted from ‘‘steady-state’’ availability curves (for details
      ...
      of the protocol, see Materials and Methods).
      ...
      has been shown to affect onset/offset kinetics and use-dependence
      ...
      20,21].
      ...
      Molecular weight has been shown to correlate with potency
      ...
      [17], and with the kinetics of inhibition [22,23]. More exactly it
      ...
      was not molecular weight that best predicted recovery kinetics, but
      ...
      the width of the molecule at the aromatic end [24].
      ...
      We succeeded to identify chemical descriptors which determine
      ...
      different types of inhibition, and which predict specific biophysical
      ...
      properties of inhibition (Kr, Ki, IC50, state-dependence, reversibility, use-dependence, onset and offset time constants). We
      ...
      observed that different chemical properties determine low Kr (high
      ...
      pKa and logP), and low Ki (high logP, logD and aromaticity).
      ...
      State-dependence, therefore can be predicted by calculating these
      ...
      chemical descriptors of molecules.
      ...
      The dynamics of the onset and offset of inhibition was
      ...
      monitored using 5 Hz trains of five depolarizing pulses from a
      ...
      holding potential of 290 mV to 210 mV. The trains were
      ...
      repeated every 20 s. Drugs were applied after 10 control trains and
      ...
      We measured inhibition (Inh; from which we calculated IC50
      ...
      values as described in Materials and Methods), reversibility of
      ...
      inhibition (Rev) and use-dependence (UD), as well as time constant
      ...
      of onset (ton) and offset (toff). The calculation of IC50,
      ...
      quantification of Rev and UD, and the determination of time
      ...
      constants are illustrated in Figure 1A. Because ton should be
      ...
      concentration-dependent if we assume a single binding reaction,
      ...
      Standard steady-state inactivation protocols were used to
      ...
      measure the shift of steady-state availability curve caused by the
      ...
      drugs. Currents were evoked by a 10 ms test pulse to 210 mV,
      ...
      preceded by 400 ms pre-pulses from 2150 to 230 mV. The
      ...
      holding potential was 2120 mV. Because the inhibition at
      ...
      hyperpolarized potentials (Inh2150), and the shift of the availability
      ...
      curves (DV1/2) are both concentration-dependent properties, we
      ...
      calculated affinities to hyperpolarized and depolarized states
      ...
      (‘‘resting state affinity’’: Kr, and ‘‘inactivated state affinity’’: Ki
      ...
      which, on the other hand, are concentration-independent
      ...
      characteristics of individual drugs. Calculation of Kr and Ki
      ...
      values are described in Materials and Methods, and illustrated in
      ...
      Figure 1E. State-dependence (SD) was quantified as the ratio Kr/
      ...
      . Values of the eight properties for individual drugs are shown in
      ...
      Table 2
      ...
      3. The calculated Kr and Ki values can be
      ...
      At least three distinct types of inhibition were identified by
      ...
      ‘Type 1’ (Figure 1A) drugs had high potency (Ki 0.73 to 6.1 mM;
      ...
      IC50 14 to 43 mM), slow onset and offset kinetics (time constants
      ...
      between 10 and 53 s), partial reversibility (between 0.2 and 0.6)
      ...
      and use-dependence (1.09 to 1.66). Drugs belonging to this type
      ...
      The properties of ‘Type 2’ drugs (Figure 1B and C) were low
      ...
      potency (Ki 17 to 88 mM; IC50 .95 mM), fast kinetics (time
      ...
      constants ,27 s) and almost full reversibility (.0.75) Drugs
      ...
      belonging to this type were the three effective anticonvulsants
      ...
      (carbamazepine, lamotrigine, phenytoin), the Class IB antiarrhythmic lidocaine and mexiletine, as well as diclofenac,
      ...
      venlafaxine, tolperisone, bupropion, ambroxol and memantine.
      ...
      The group can be further divided: lidocaine, mexiletine, ambroxol
      ...
      and tolperisone (Figure 1B) were use-dependent (UD 1.14 to 1.39).
      ...
      Anticonvulsants, memantine, venlafaxine, bupropion and diclofenac (Figure 1C), on the other hand, showed no significant usedependence (0.95 to 1.05).
      ...
      A distinct group, ‘Type 3’, was formed by the neuroprotectants
      ...
      flunarizine and lifarizine (Figure 1D). These drugs had high
      ...
      potency, very slow kinetics, apparent irreversibility (no recovery
      ...
      within the 200 s of washout within this experimental environment)
      ...
      and no use-dependence.
      ...
      drugs, bupivacaine,
      ...
      flecainide, nefazodone and riluzole seemed to have their own
      ...
      specific type of inhibition: Bupivacaine with high use-dependence
      ...
      and state-dependence; flecainide, with high use-depencence but
      ...
      low state-dependence and low Kr, indicating that it is an open
      ...
      channel blocker; nefazodone with an exceptionally high statedependence, and riluzole with high state-dependence and no usedependence.

      ---

      Title: Exploring the heterogeneity of use-dependent sodium channel inhibitor drugs. II: Drugs described by the modulated receptor hypothesis (MRH) and/or the guarded receptor hypothesis (GRH)
      URL: https://bmcpharma.biomedcentral.com/articles/10.1186/1471-2210-7-S2-A42
      Published: 2007-11-14T00:00:00.000Z
      Author: N/A
      Highlights:
      All therapeutically used sodium channel inhibitor drugs seem to act similarly: in a use-dependent and state-dependent manner. These properties, however, can be caused by multiple mechanisms, as we and others have previously shown [[1](https://bmcpharma.biomedcentral.com/articles/10.1186/1471-2210-7-S2-A42#ref-CR1)]. The two major hypotheses that explain use- and state-dependent inhibition are the MRH [[2](https://bmcpharma.biomedcentral.com/articles/10.1186/1471-2210-7-S2-A42#ref-CR2)] and the GRH [[3](https://bmcpharma.biomedcentral.com/articles/10.1186/1471-2210-7-S2-A42#ref-CR3)]. In this study we investigated which hypothesis better describes inhibition by various drugs, and whether drugs can be classified based on this aspect of their mechanism of action. We assumed that the two hypotheses are not mutually exclusive, and speculated that both altered affinity (as predicted by the MRH) and altered accessibility (as predicted by the GRH) to the inactivated state can be expressed as changes in association and dissociation rates upon conformational transition. We developed a method to test the relative contribution of affinity and accessibility in the effect of the drugs based on the degree of inhibition (reflecting affinity) and the time constant of the onset of inhibition (reflecting accessibility) as a function of changes in the voltage protocol. We tested the method by simulations and found that original parameters of a simulated drug can be deduced using the method. Experiments using 12 fast-inactivated state-preferring use-dependent sodium channel inhibitors suggest significant differences in this aspect of the mechanism.
      ...
      3. Starmer CF, Grant AO, Strauss HC: Mechanisms of use-dependent block of sodium channels in excitable membranes by local anesthetics. Biophys J. 1984, 46: 15-27.
      ...
      * [Time Constant](https://bmcpharma.biomedcentral.com/search?query=Time%20Constant&facet-discipline="Biomedicine")
      ...
      * [Sodium Channel](https://bmcpharma.biomedcentral.com/search?query=Sodium%20Channel&facet-discipline="Biomedicine")
      ...
      ](https://bmcpharma.biomedcentral.com/search?query=Multiple%20Mechanism&facet
      ...
      discipline="Biomedicine")
      ...
      * [Dissociation Rate](https://bmcpharma.biomedcentral.com/search?query=Dissociation%20Rate&facet-discipline="Biomedicine")
      ...
      * [Conformational Transition](https://bmcpharma.biomedcentral.com/search?query=Conformational%20Transition&facet-discipline="Biomedicine")
```
/answer d8766604-73c1-4a88-9784-99fd4a904315 allow
ReasoningToken: 8930
# Prüfung: Potenz & Selektivität von DPH als Salven-Limiter über Na⁺-Kanal-Block

## 1. Literaturabgleich der Kd-Werte

Ihre Annahme Kd,I ≈ 10 µM ist eher am unteren (optimistischen) Rand. Die direkten elektrophysiologischen Messungen an nativen Neuronen liegen tendenziell höher:

| Quelle | Präparation | Kd (gemessen) |
|---|---|---|
| Kim et al. 2000, Brain Res | Ratten-DRG, TTX-S | 48 µM (bei −80 mV Haltepotential) |
| Kim et al. 2000, Brain Res | Ratten-DRG, TTX-R | 86 µM |
| Yang/Kuo (Mol Pharmacol) | DPH als **Open-Channel-Blocker**, analog Carbamazepin/Imipramin | Bindung an *offenen* Kanal schneller als an *inaktivierten* – DPH ist damit kein reiner „modulated-receptor"-Inaktivierungsstabilisator wie Phenytoin, sondern eine Mischform |

Wichtig: DPH wird in der Kuo-Gruppe explizit **nicht** wie Imipramin (Kd,I ≈ 1,3 µM) klassifiziert, sondern in eine Gruppe mit schnellerer, aber schwächerer Bindung. Ich rechne im Folgenden sensitivitätsanalytisch mit Kd,I = 10–90 µM.

## 2. Der entscheidende Punkt: Use-Dependence hat eine Gleichgewichts-*Decke*, keine Wunderkraft

Das modulated-receptor-Modell (Hille/Hondeghem-Katzung) sagt korrekt, dass die Belegung während einer Salve gegen einen **höheren** Grenzwert konvergiert als im Ruhezustand. Aber dieser Grenzwert ist **nicht unabhängig von C** – er ist weiterhin durch die Standard-Bindungsisotherme gedeckelt:

$$Occ_{Salve,max} = \frac{C_{frei}}{C_{frei}+K_{d,I}} \quad (\text{Limes für } t\to\infty,\ f\to\infty)$$

Use-Dependence verschiebt also den *effektiven Kd* von Kd,R (>300 µM) auf Kd,I (10–90 µM) – sie erzeugt aber keine Bindung, die über C/(C+Kd,I) hinausgeht. Mit C ≈ 0,3–1 nM:

| Kd,I | Occ-Decke (Salve, theoretisches Maximum) |
|---|---|
| 10 µM | ~3–10 × 10⁻⁵ (0,003–0,01 %) |
| 48 µM | ~6–20 × 10⁻⁶ (0,0006–0,002 %) |
| 90 µM | ~3–11 × 10⁻⁶ |

Selbst im **bestmöglichen Fall** (unendlich lange, unendlich hochfrequente Salve, vollständige Konversion in den hochaffinen Zustand) liegt die Kanalbelegung 3–4 Zehnerpotenzen unter dem, was für eine funktionell relevante Leitungs-/Erregbarkeitsdämpfung nötig ist (Lokalanästhetika-Literatur: relevante Effekte typischerweise ab ~20–50 % Kanalblock).

## 3. Kinetische Realitätsprüfung: Wird die Decke innerhalb einer realen Salve überhaupt erreicht?

Nötige Bindungsrate pro Aktionspotential (Open-State-Fenster ~2 ms, k_on(offen) ≈ 10⁶–10⁷ M⁻¹s⁻¹ nach Kuo-Daten für Carbamazepin/Imipramin/DPH-Analoga):

$$p_{Bindung,pro\ AP} = k_{on}\cdot C \cdot \tau_{open} \approx 10^{6,5}\,M^{-1}s^{-1} \times 5\times10^{-10}M \times 2\times10^{-3}s \approx 3\times10^{-9}$$

Bei HR > 130/min (Zykluslänge < 460 ms) und einer realistischen Salvendauer von 10–60 s (≈ 22–130 Schläge):

$$Occ_{Salve,real} \approx N \times p \approx 130 \times 3\times10^{-9} \approx 4\times10^{-7}$$

Das ist **nochmals ~2 Größenordnungen unter der bereits verschwindend kleinen Gleichgewichtsdecke** (10⁻⁴–10⁻⁵). D.h.: Die Salve ist viel zu kurz, um überhaupt in die Nähe des theoretischen Maximums zu kommen. Die „profound use-dependent block"-Befunde von Kuo/Kim wurden bei **µM-Konzentrationen in vitro** erzielt – das ist 3–4 Zehnerpotenzen über der freien Hirnkonzentration bei 12,5 mg. Use-Dependence beschleunigt die *Kinetik* des Erreichens des Ceilings, sie kann aber nicht die fehlende absolute Substratmenge (freies DPH) kompensieren.

## 4. Selektivitäts-Check: Ist Na⁺-Kanal-Block überhaupt vom H1-Effekt trennbar?

Der entscheidende Vergleich ist nicht "Na-Kanal-Occ vs. Wirkschwelle", sondern **H1-Occ vs. Na-Kanal-Occ über den gesamten erreichbaren Dosisbereich**:

$$\frac{Occ_{H1}}{Occ_{Na,I}} \approx \frac{K_{d,I}}{K_{d,H1}} \approx \frac{10.000-90.000\ nM}{1-4\ nM} \approx 2.500-90.000$$

Dieses Verhältnis ist über weite C-Bereiche näherungsweise **dosisunabhängig** (solange C << beide Kd-Werte, was hier der Fall ist). Das bedeutet: **Es gibt keinen Dosisbereich, in dem DPH signifikant an Na⁺-Kanälen, aber nur wenig an H1 wirkt.** Im Gegenteil – um überhaupt in eine pharmakologisch relevante Na⁺-Kanal-Occ-Region zu kommen (z. B. 20 % Occ, C ≈ 0,25×Kd,I ≈ 2,5–22 µM), wäre H1 zu diesem Zeitpunkt bereits bei

$$Occ_{H1} = \frac{2.500-22.000}{2.500-22.000+2} \approx 99,9\,\%$$

**vollständig gesättigt**, ebenso vermutlich der Muskarinrezeptor (Ki 100–1000 nM → nahezu 100 % Occ) und kardiale Na⁺-/hERG-Kanäle (das QT-Verlängerungsrisiko von DPH ist klinisch dokumentiert – Sie hatten das Paper dazu selbst in Reichweite).

## 5. Fazit: Antwort auf die Dosisreduktions-Frage

**Die Na⁺-Kanal-Hypothese ist bei 12,5 mg quantitativ nicht tragfähig, unabhängig von der Use-Dependence-Korrektur.** Konsequenzen für Ihre Fragestellung:

1. **Es gibt bei diesem Mechanismus nichts zu „sparen"**: Der Na⁺-Kanal-Beitrag zur Salven-Limitierung ist bei 12,5 mg bereits bei ~10⁻⁵–10⁻⁷ Occ – pharmakologisch irrelevant. Eine Dosisreduktion kann diesen (ohnehin nicht existenten) Beitrag nicht weiter „schonen", weil er nie im wirksamen Bereich war.
2. **Eine Dosisreduktion würde stattdessen den einzigen Mechanismus schwächen, der bei dieser Konzentration überhaupt messbar besetzt ist – H1 (20 % → weniger).** Wenn der beobachtete Salven-limitierende Effekt real ist, ist er nach dieser Rechnung mit sehr viel höherer Wahrscheinlichkeit **H1-vermittelt** (zentrale H1-Blockade moduliert NTS/LC-Exzitabilität durchaus bekanntermaßen) als Na⁺-Kanal-vermittelt.
3. **Empfehlung**: Dosisreduktion **nicht** mit der Begründung „Na⁺-Kanal-Effekt bleibt via Use-Dependence erhalten, H1-Last sinkt" rechtfertigen – diese Trennung existiert bei den vorliegenden Affinitäten nicht. Falls Dosisreduktion aus Sicherheitsgründen (Anticholinergika-Last, QT, Sedierung) gewünscht ist, muss man akzeptieren, dass damit **proportional auch der H1-Beitrag zur Salven-Limitierung sinkt** – eine Erhaltung des Effekts ist auf dieser Rechnungsgrundlage nicht zu erwarten.
4. Sollte der Effekt dennoch bei Dosisreduktion klinisch erhalten bleiben, wäre das ein Hinweis auf einen **dritten, bisher nicht modellierten Mechanismus** (z. B. ein hochaffines Off-Target im niedrigen nM-Bereich, oder ein stark nichtlinearer/Schwelleneffekt an wenigen fokal-getriggerten Zellen) – dann lohnt sich eine gezielte Bindungsstudien-Suche statt einer Na⁺-Kanal-Kd-Rückrechnung.

**Kurz**: Potenz unzureichend (Kd,I 10–90 µM vs. C 0,3–1 nM → Occ-Decke 10⁻⁴–10⁻⁷), Selektivität invertiert (H1 immer 3–5 Zehnerpotenzen stärker besetzt als Na-Kanal, über den gesamten Dosisbereich), Salven-Kinetik reicht nicht aus, um die ohnehin niedrige Gleichgewichtsdecke zu erreichen. Die elegante Use-Dependence-Erklärung rettet den Mechanismus biophysikalisch korrekt beschrieben, aber nicht quantitativ bei dieser Dosis.
Na⁺-Kanal scheidet dann aus. Es verbleiben Sigma-1, a2 und NDMA. Die anderen wurden mittels Doxepin/Scopolamin abgegrenzt.
SystemInit:  id=0b6c12a1-e88d-4c35-ae14-3099ae2224a3, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
Control Request:
```yaml
id: e4fded35-8970-4d95-8fa7-3fd318e390c8
toolName: web-search-exa
arguments:
  query: diphenhydramine sigma-1 receptor binding affinity Ki nM
  reason: Get DPH sigma-1 receptor Ki for occupancy calculation
```
/answer e4fded35-8970-4d95-8fa7-3fd318e390c8 allow
Control Request:
```yaml
id: f03333a0-9fa1-47db-ba66-db2182de2440
result:
  structuredContent:
    content: |-
      Title: Comprehensive 3D-QSAR Model Predicts Binding Affinity of Structurally Diverse Sigma 1 Receptor Ligands
      URL: https://doi.org/10.1021/acs.jcim.8b00521
      Published: 2018-11-29T00:00:00.000Z
      Author: Youyi Peng, Hiep Dong, William J. Welsh
      Highlights:
      = 58 nM and 160 nM, respectively. As diphenhydramine is approved as an antiallergic, and phenyltoloxamine as an analgesic and sedative, each of these compounds represents a viable starting point for a drug discovery campaign aimed at the development of novel S1R antagonists for a wide range of therapeutic indications.
      ...
      - Kenneth D. Carr, Jacob M. Hiller, Eric J. Simon. Diphenhydramine potentiates narcotic but not endogenous opioid analgesia. Neuropeptides. 1985;5(4-6):411-414. doi:10.1016/0143-4179(85)90041-1.

      ---

      Title: Comprehensive 3D-QSAR Model Predicts Binding Affinity of Structurally Diverse Sigma 1 Receptor Ligands
      URL: https://doi.org/10.1021/acs.jcim.8b00521.s001
      Published: 2018-12-13T00:00:00.000Z
      Author: Youyi Peng (1828456), Hiep Dong (6084017), William J. Welsh (666425)
      Highlights:
      The Sigma 1 Receptor (S1R) has attracted intense interest as a pharmaceutical target for various therapeutic indications, including the treatment of neuropathic pain and the potentiation of opioid analgesia. Efforts by drug developers to rationally design S1R antagonists have been spurred recently by the 2016 publication of the high-resolution X-ray crystal structure of the ligand-bound human S1R. Until now, however, the absence in the published literature of a single, large-scale, and comprehensive quantitative structure–activity relationship (QSAR) model that encompasses a structurally diverse collection of S1R ligands has impaired rapid progress. To our best knowledge, the present study represents the first report of a statistically robust and highly predictive 3D-QSAR model (R<sup>2</sup> = 0.92, Q<sup>2</sup> = 0.62, R<sub>pred</sub><sup>2</sup> = 0.81) based on the X-ray crystal structure of human S1R and constructed from a pooled compilation of 180 S1R antagonists that encompass five structurally diverse chemical families investigated using identical experimental protocols. Best practices, as recommended by the Organization for Economic Cooperation and Development (OECD: http://www.oecd.org/), were adopted for pooling data from disparate sources and for QSAR model development and both internal and external model validation. The practical utility of the final 3D-QSAR model was tested by virtual screening of the DrugBank database of FDA approved drugs supplemented by eight reported S1R antagonists. Among the top-ranked 40 DrugBank hits, four approved drugs which were previously unknown as S1R antagonists were tested using <i>in vitro</i> radiolabeled human S1R binding assays. Of these, two drugs (diphenhydramine and phenyltoloxamine) exhibited potent S1R binding affinity with <i>K</i><sub>i</sub> = 58 nM and 160 nM, respectively. As diphenhydramine is approved as an antiallergic, and phenyltoloxamine as an analgesic and sedative, each of these compounds represents a viable starting point for a drug discovery campaign aimed at the development of novel S1R antagonists for a wide range of therapeutic indications.

      ---

      Title: Highly Specific Sigma Receptor Ligands Exhibit Anti-Viral ...
      URL: https://www.mdpi.com/2076-0817/10/11/1514
      Published: N/A
      Author: N/A
      Highlights:
      Figure 1 Structures of sigma ligands utilized in this and other studies. The structure of sigma ligands important to this study are presented with the sigma specific activity, Ki for the respective sigma receptor binding property, and the bioavailability if known. ( A) SA4503 (cutamesine) is a selective Sigma-1 piperazine agonist with > 15-fold preference for sigma-1 over sigma-2. ( B) CM304 is a highly selective benzothiazolone sigma-1 antagonist. ( C) CM398 is a highly selective benzimidazolone-based sigma-2 ligand. ( D) AZ66 is a mixed sigma-1/sigma-2 selective ligand with an optimized pharmacokinetic profile. ( E) PB28 is not utilized in this study but recent work demonstrated its utility in vitro was compromised by its toxicity and is included as a structural comparison to the other compounds tested in this work. "> Figure 2 Highly specific sigma ligands inhibit SARS-CoV-2-induced cytotoxicity in Vero E6 cells. Cytotoxicity measured by LDH release in Vero E6 cells at 72 h in the presence of the indicated drug concentration alone (black bars) or in the presence of the indicated drug after infection with SARS-CoV-2 at an MOI of 0.2 (gray bars) ( A – D). The 50% cytotoxic concentration (CC 50) of the drug alone (black circles) and the 50% effective concentration (EC 50) at which the drug inhibits SARS-CoV-2-induced cytotoxicity (black squares) as determined by non-linear regression for each drug is shown in ( E – H). The calculated CC 50 and EC 50 are shown when appropriate. Data points were obtained from triplicate experiments. Similar results were obtained from an infection with MOI of 0.3 however the dynamic range was not as satisfactory. *, p ≤ 0.05; **, p ≤ 0.01; ***, p ≤ 0.001; ****, p ≤ 0.0001. "> Figure 3 Sigma ligands AZ66, CM398, and SA4503 significantly reduce viral genome replication and AZ66 potently reduces SARS-CoV-2 plaque formation. ( A), SARS-CoV-2 was used to infect Vero E6 monolayers at an MOI of 0.01 in the presence of 50 μg/mL AZ66, 100 μg/mL for each of CM304, CM398 or SA4503, or 1% DMSO in triplicate. After 48 h, cell monolayers were harvested into AVL buffer and RNA was isolated with the QIAamp viral RNA Kit and qPCR was used to enumerate N copies per ml and are presented as genomic equivalents (GE) per ml. The T0 DMSO treatment represents the input GE/mL harvested immediately after virus addition to the monolayers. The data is the mean and standard deviation of three experiments. ( B), Phospholipidosis in H23 cells was measured after 48 h of treatment with the indicated sigma ligand concentration. One-way ANOVA indicates significant difference compared to the sertraline positive control. ( C), Plaque reduction assay showed the sigma ligand AZ66 was highly effective at inhibiting plaque formation by the SARS-CoV-2 virus. The EC 50 of AZ66 in this assay was 6.46 μg/mL (15.93 μM). The calculated EC 50 of AZ66 by both cytotoxicity assay and plaque reduction assay is well below the published area under the curve (mean 158.22 μg h/mL) in rats following oral dosing of 20 mg/kg and also below the AUC following an intravenous 5 mg/kg dose (mean 63.2 μg h/mL). *, p ≤ 0.05; ****, p ≤ 0.0001. "> Figure 4 Sigma ligands reduce SARS-CoV-2 induced cytopathic effects in cell monolayers
      ...
      Monolayers of Vero E6 cells in 96-well plates were imaged after 72 h in the absence of treatment ( A) or in the presence of AZ66 ( B), CM304 ( C), CM398 ( D), or SA4503 ( E) alone (top panels
      ...
      In the bottom panel are images of monolayers infected with SARS-CoV-2 at an MOI of 0.2 in the presence of the same drug treatments as in the top panel. Cytopathic effects (CPE) in the monolayers caused by SARS-CoV-2 infection are visible as dark puncta (dead infected cells) against the light-colored intact monolayer. These puncta are absent from the uninfected monolayer images (top panel) and are greatly reduced in number in the AZ66 and CM398-treated infected monolayers ( B, D; bottom panels) compared to untreated infected monolayers ( A, bottom panel). The scale bar at lower right is equal to 500 μm. "> Figure 5 Comparison of agonist versus antagonist interactions with the sigma-1 receptor by molecular docking. The crystal structure of the human sigma-1 receptor (PDB 5HK1), shown in cyan, was used as the basis for molecular docking with an selective agonist SA4503 (cutamesine, active against SARS-CoV-2), ( A, upper panel), and antagonist CM304 (inactive against SARS-CoV-2), ( B, lower panel). SA4503 and CM304 are shown as sticks, white for carbon, blue for nitrogen, red for oxygen, yellow for sulfur. "> Figure 6 Homology modeling the human sigma-
      ...
      receptor and definition of a putative ligand binding site. (A), upper panel, the crystal structure of Emopamil-Binding Protein (EBP), PDB 6OHT, shown in gray, was solved complexed to an inhibitor, U18666A, shown as yellow spheres. Ligand binding residues are shown as magenta sticks
      ...
      ( B), homology model of the human sigma-2 receptor based on EBP, shown in orange. AZ66, a dual sigma-1 and sigma-2 receptor ligand, is shown as posed by molecular docking using AutoDock Vina as yellow spheres. The putative contact residues on the sigma-
      ...
      Molecular docking of sigma-2 receptor ligands that exhibit antiviral activity against SARS-CoV-2. ( A), highly selective sigma-2 receptor agonist CM398 is shown as posed by AutoDock Vina to a model of the human sigma-2 receptor. ( B), dual sigma-1 and sigma-2 receptor ligand AZ66 is shown as posed by molecular docking. Putative interacting residues are shown in red. CM398 and AZ66 are shown as sticks, white for carbon, blue for nitrogen, red for oxygen, yellow for sulfur
      ...
      Figure 8 Combinations of diphenhydramine and lactoferrin exhibit synergy against SARS-CoV-2.
      ...
      DPH) at various concentrations
      ...
      The antihistamine diphenhydramine, with on-target binding to the Histamine-1 receptor, has known off-target effects at the sigma-1 receptor [27]. Diphenhydramine was recently shown to inhibit SARS-CoV-2 infectivity and the calculated EC50 for SARS-CoV-2 by plaque reduction assay was 17.4 μg/mL (59.6 μM). This drug is safe, well-characterized, and widely available and so highly relevant in the search for COVID therapeutics. We investigated the ability of diphenhydramine to inhibit SARS-CoV-2 induced cytotoxicity and found an EC50 of 122.0 μg/mL (418 μM; Figure 8A,B), about 7 times higher than that found in the plaque reduction assay, similar to our findings with AZ66. We hypothesized that diphenhydramine could be combined with structurally distinct antiviral agents (binding other receptors, not sigma) to reduce its EC50 for antiviral activity against SARS-CoV-2.
      ...
      -target sigma receptor binding activity, and also exhibit antiviral activity against SARS-CoV-2, including clemastine, cloperastine, astemizole, hydroxyzine, azelastine and diphenhydramine. Since diphenhydramine is the most commonly used antihistamine exhibiting antiviral activity, we asked if antiviral activity could be improved by combining a sigma receptor ligand with lactoferrin, an antiviral agent that binds distinct targets [28,29]. We found that co-administration of 400 μg/mL of lactoferrin with diphenhydramine reduced SARS-CoV-2 induced cytotoxicity and decreased the EC50 (Figure 8C,D). The antiviral enhancement effects of lactoferrin were more apparent at lower, therapeutically relevant concentrations of diphenhydramine (Figure 8E). Combining lactoferrin with diphenhydramine resulted in synergistic effects on antiviral activity against SARS-CoV-2 (Figure 8F). Compounds we found effective in Vero E6 were validated in their ability to reduce infectious SARS-CoV-2 production following infection of human lung epithelial cells (Figure 9C,D). These data suggest that sigma receptor ligands or formulated combinations of over-the-counter products have the potential to inhibit virus infection and/or decrease recovery time from COVID. Lastly, concentrations that inhibited SARS-CoV-2

      ---

      Title: Diphenhydramine · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/diphenhydramine/
      Published: N/A
      Author: N/A
      Highlights:
      | Protein | UniProt | Gene | pChembl | Type | Value | Activity ID |
      | --- | --- | --- | --- | --- | --- | --- |
      | Histamine H1 receptor (domestic guinea pig) | P31389 | 9 | IC50 | 1 nM | CHEMBL_ACT_429899 |
      | Histamine H1 receptor (domestic guinea pig) | P31389 | 7.93 | Kd | 11.75 nM | CHEMBL_ACT_7846167 |
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
      Muscarinic acetylcholine
      ...
      P08173 | CHRM4 | 6.43 | IC50 | 372 nM | CHEMBL_ACT_7681447 |
      ...
      | 5-hydroxytryptamine receptor 2A | P28223 | HTR2A | 6.43 | Ki | 370 nM | CHEMBL_ACT_7681524 |
      ...
      | 5-hydroxytryptamine receptor 2C | P28335 | HTR2C | 6.29 | Ki | 513 nM | CHEMBL_ACT_7681528 |
      ...
      | 5-hydroxytryptamine receptor 2B | P41595 | HTR2B | 6.15 | Ki | 711 nM | CHEMBL_ACT_7681526 |
      ...
      | 3513

      ---

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
      | Species | Value (nM) | Value Type | Reference |
      | --- | --- | --- | --- | --- |
      | Muscarinic M1 Receptor | Human | 80–100 | Ki | [1] |
      | Muscarinic M2 Receptor | Human | 120–490 | Ki | [1] |
      | Muscarinic M3 Receptor | Human | 84–229 | Ki |
      ...
      1] |
      ...
      | Muscarinic M4 Receptor | Human | 53–112 | Ki |
      ...
      | Muscarinic M
      ...
      Receptor | Human | 3
      ...
      –26
      ...
      | Ki |
      ...
      Table 1: Comparative Receptor Binding Affinities (Ki, nM) of
      ...
      henhydramine and Newer
      ...
      ihistamines
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
      A lower Ki value indicates a higher binding affinity.[7]
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

      ---

      Title: diphenhydramine | Ligand page | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=1224
      Published: N/A
      Author: N/A
      Highlights:
      ID: 12
      ...
      : Diphenhyd
      ...
      | Canonical SMILES | CN(CCOC(c1
      ...
      1)c1ccccc1)C |
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
      | Search Google for chemical match
      ...
      the InChIKey | ZZVUWRFHKOJYTH-UHFFFAOYSA-N |
      |
      ...
      backbone | ZZ
      ...
      FHKOJYTH |
      ...
      Diphenhydramine

      ---

      Title: Novel High Affinity Sigma-1 Receptor Ligands from Minimal Ensemble Docking-Based Virtual Screening - PMC
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC8347176/
      Published: N/A
      Author: N/A
      Highlights:
      The selective S1R agonist [3H]-(+)-pent
      ...
      ocine possessed a saturable, high affinity binding to a single class of sites with an equilibrium dissociation rate constant (Kd) of 1.8 nM and the maximal density of binding sites (Bmax) of 1072 fmol/mg protein in guinea pig liver membrane preparations at 37 °C. We also determined the Kd of the non-selective sigma receptor ligand, [3H]-DTG in rat liver membranes in the presence of (+)-pentazocine (100 nM) to mask S1R sites. The Kd value was found to be 47 nM (see Figure S1 in Supplementary Information).
      ...
      The binding affinities of the compounds for S1R and S2R were determined using in vitro competitive binding assays. The assay conditions were validated with the following S1R and S2R ligands: (+)-pentazocine, fluvoxamine, haloperidol, cutamesine, and DTG. The displacement curves and the measured binding parameters are presented in Figure 3 and Table 2, respectively. Competition binding assays in guinea pig liver membrane homogenate against the S1R specific radioligand [3H](+)-pentazocine revealed that all four compounds exhibited nanomolar S1R affinities and induced a similar maximal displacement (100%). The order of potencies of the prototypic sigma ligands were as (+)-pentazocine > haloperidol > cutamesine > fluvoxamine that is consistent with previous S1R pharmacology findings [40,64,65,66,67]. In homologous displacement experiments for the S2R, the non-selective S1R and S2R ligand, DTG exhibited a Ki value of 29 nM in rat liver membranes. In order to mask the S1R binding sites of the rat liver membrane preparation 100 nM (+)-pentazocine was applied [5,60].
      ...
      | Ligand | S1RKi ± S.E.M. (nM) | S2RKi ± S.E.M. (nM) | Selectivity(S2R/S1R) |
      | --- | --- | --- | --- |
      | (+)-pentazocine | 4.8 ± 0.4 | 1698 ± 103 | 354 |
      | DTG | n.d. | 29 ± 4 | n.d. |
      | fluvoxamine | 31 ± 3 | 6187 ± 296 | 200 |
      | haloperidol | 5.2 ± 1.3 | n.d. | n.d. |
      | cutamesine | 5.5 ± 1.1 | n.d. | n.d. |
      ...
      | ID |
      ...
      (nM) | Docking Score (kcal/mol) | Chemical Name | Structure of Best
      ...
      ed Stereois
      ...
      |
      | --- | --- | --- | --- | ---
      ...
      1 1 |
      ...
      1.6
      ...
      -Benzyl-6,7-dimethoxy-1,2,3,4-tetrahydro-1-isoquinolineethanamine dihydrochloride |
      | L2 1 | 91.0 | −12.41 | 3-Amino-N-(2-fluoro-3-(trifluoromethyl)benzyl]-3-phenylpropanamide hydrochloride |
      ...
      | L3 2 | 1
      ...
      .0 | −11.
      ...
      | 1-[(4-Methoxyphenoxy)methyl]-2-(1,2,3,4-tetrahydroisoquinolin-2-yl)ethanol |
      ...
      4 1 | 420.0 | −12.47 | 3-Amino-N-(3-fluoro-5-(trifluoromethyl)benzyl]-3-phenylpropanamide hydrochloride |
      | L5 1 | 463.0 | −10.74 | (±)-diendo-3′-amino-1-benzyl-5′,8′-methano-4′a,5′,8′,8′a-tetrahydrospiro[piperidine-4,2′(1′H)-quinazolin]-4′(3′H)-one |
      ...
      | L6 2 | 1036.0 | −11.12 | N-Benzyloxycarbonyl-(9-methyl-2,3,4,9-tetrahydro-1H-pyrido[3,4-b]indol-1-yl)methanamine |
      ...
      | L7 2 | 1381.0 | −1
      ...
      .56 | (1S,3R,4R,6R)-3-(benzylamino)methyl
      ...
      7,7-dimethylbicyclo[4.1.0]heptane-3,4-diol |
      ...
      | L8 2 | 1534.
      ...
      −10
      ...
      3-Amino-N-(2-fluoro-3-(trifluoromethyl)benzyl]-2-methylpropanamide trifluoroacetate |
      | L9 1 | 1716.0 | −10.87
      ...
      N-Benzyloxycarbonyl-(2,3,4,9-tetrahydro-1H-pyrido[3,4-b]indol-1-yl)methanamine |
      ...
      | L10 1 | 2154.0 | −11.58 | (4R*,11bR*)-9,10-Diethoxy-4-[4-(dimethylamino)phenyl]-1,3,4,6,7,11b-hexahydro-2H-pyrimido[6,1-a]isoquinoline |
      | L11 1 | 2381.0 | −10.55 | 1-{[(Benzyloxycarbonyl)amino]methyl}-6,7-dimethoxy-1,2,3,4-tetrahydroisoquinoline |
      ...
      | L12 2 | 3266.0 | −9.69 | (1R*,9bR*)-1-{[(4-Chlorophenyl)thio]methyl}-7,8-diethoxy-1,4,5,9b-tetrahydro-2H-azeto[2,
      ...
      [3H]
      ...
      | Ligand | S1RKi ± S.E.M. (nM) | S2RKi ± S.E.M. (nM) | Selectivity(S2R/S1R) |
      | --- | --- | --- | --- |
      | (S)-L1 | 11 ± 3 | 169 ± 15 | 15.4 |
      | (R)-L1 | 252 ± 12 | 94 ± 5.5 | 0.4 |
      | (S)-L2 | 81 ± 3 | 5108 ± 960 | 63 |
      | (R)-L2 | 699 ± 57 | 920 ± 25 | 1.3 |
      | (S)-L3 | 132 ± 23 | 463 ± 33 | 3.5 |
      | (R)-L3 | 58 ± 3 | 176 ± 21 | 3 |
      ...
      (S)-L1 (Ki = 11 nM) showed much higher affinity for S1R than S2R sites and exhibited a similar, 15-fold S1R selectivity, as was previously shown by the fluoroethyl analog of S1R agonist SA4503 (cutamesine), where the ratio was KiS2R/KiS1R = 14.1 [66]. (R)-L3 (Ki = 58 nM) possessed a good binding affinity towards S1R and displayed a 3-fold lower affinity to S2R. Compound (S)-L2 (Ki = 81 nM) had a moderate affinity for the S1R site and the most favorable S1R selectivity (KiS2R/KiS1R = 63). Compounds (S)-L3 (Ki = 132 nM), (R)-L1 (Ki = 252 nM), and (R)-L2 (Ki = 699 nM) showed modest affinities towards S1R, and weak S2R bindings, with the exception of compound (R)-L1 which is weakly S2R selective.

      ---

      Title: The Pharmacology of Sigma-1 Receptors - PMC
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC2785038/
      Published: N/A
      Author: N/A
      Highlights:
      Three lines of evidence suggest that sigma-1 receptor agonists can exert an effective antidepressant activity. First, sigma-1 receptor agonists improved cognitive activity in a variety of amnesia models, as they potentiated NMDA or cholinergic neurotransmissions. Secondly, the seminal discovery by[Bergeron et al. (1993)](#R6)demonstrated that antidepressants could behave as sigma-1 agonists in a study in which low doses of the antidepressants sertraline, a selective serotonin reuptake inhibitor (SSRI), and clorgyline, a monoamine oxidase inhibitor, selectively potentiated the effect of NMDA, in a haloperidol-sensitive manner, on pyramidal neurons in the CA3 region of the rat dorsal hippocampus. Thirdly,[Narita et al. (1996)](#R105)reported that SSRI and tricyclic antidepressants showed differential binding affinity to sigma-1 receptors, and in particular demonstrated that fluvoxamine and sertraline have a Ki value of lower than 100 nM at sigma-1 receptors. This result suggests a role of sigma-1 receptors in the pharmacological action of those drugs. The studies above led to extensive studies targeting sigma-1 receptors for treating depression. Thus, DHEAS, PRE-084, (+)SKF-10,047 ([Urani et al., 2001](#R151)), SA4503 ([Skuza and Rogoz, 2002](#R135);[Lucas et al., 2008](#R63)), and 1,3-di-o-tolylguanidine ([Skuza and Rogoz, 2003](#R136)) were demonstrated to be effective antidepressants in the forced swimming, tail suspension, or conditioned fear stress test. The antidepressant effect of those drugs was blocked by the sigma-1 receptor antagonist, BD1047 ([Urani et al., 2001](#R151)).[Dhir and Kulkarni (2008)](#R26)recently found that the anti-immobility action during forced swimming induced by buproprion, a dopamine uptake inhibitor, was blocked by the sigma-1 receptor antagonists, BD-1047 and progesterone. This last report clearly indicates that the antidepressant-like effect of the clinically used drug, buproprion, is also mediated via sigma-1 receptors, although its binding affinity for the sigma-1 sites has not yet been reported.

      ---

      Title: Novel High Affinity Sigma-1 Receptor Ligands from Minimal Ensemble Docking-Based Virtual Screening
      URL: https://www.mdpi.com/1422-0067/22/15/8112
      Published: 2021-07-29T00:00:00.000Z
      Author: N/A
      Highlights:
      The selective S1R agonist [3H]-(+)-pentazocine possessed a saturable, high affinity binding to a single class of sites with an equilibrium dissociation rate constant (Kd) of 1.8 nM and the maximal density of binding sites (Bmax) of 1072 fmol/mg protein in guinea pig liver membrane preparations at 37 °C. We also determined the Kd of the non-selective sigma receptor ligand, [3H]-DTG in rat liver membranes in the presence of (+)-pentazocine (100 nM) to mask S1R sites. The Kd value was found to be 47 nM (see Figure S1 in Supplementary Information).
      ...
      The binding affinities of the compounds for S1R and S2R were determined using in vitro competitive binding assays. The assay conditions were validated with the following S1R and S2R ligands: (+)-pentazocine, fluvoxamine, haloperidol, cutamesine, and DTG. The displacement curves and the measured binding parameters are presented in Figure 3 and Table 2, respectively. Competition binding assays in guinea pig liver membrane homogenate against the S1R specific radioligand [3H](+)-pentazocine revealed that all four compounds exhibited nanomolar S1R affinities and induced a similar maximal displacement (100%). The order of potencies of the prototypic sigma ligands were as (+)-pentazocine > haloperidol > cutamesine > fluvoxamine that is consistent with previous S1R pharmacology findings [40,64,65,66,67]. In homologous displacement experiments for the S2R, the non-selective S1R and S2R ligand, DTG exhibited a Ki value of 29 nM in rat liver membranes. In order to mask the S1R binding sites of the rat liver membrane preparation 100 nM (+)-pentazocine was applied [5,60].
      ...
      | ID | Measured Ki (nM) | Docking Score (kcal/mol) | Chemical Name | Structure of Best Docked Stereoisomer |
      | --- | --- | --- | --- | --- |
      | L1 1 | 32.0 | −11.62 | N-Benzyl-6,7-dimethoxy-1,2,3,4-tetrahydro-1-isoquinolineethanamine dihydrochloride |
      | L2 1 | 91.0 | −12.41 | 3-Amino-N-(2-fluoro-3-(trifluoromethyl)benzyl]-3-phenylpropanamide hydrochloride |
      | L3 2 | 110.0 | −11.95 | 1-[(4-Methoxyphenoxy)methyl]-2-(1,2,3,4-tetrahydroisoquinolin-2-yl)ethanol |
      | L4 1 | 420.0 | −12.47 | 3-Amino-N-(3-fluoro-5-(trifluoromethyl)benzyl]-3-phenylpropanamide hydrochloride |
      | L5 1 | 463.0 | −10.74 | (±)-diendo-3′-amino-1-benzyl-5′,8′-methano-4′a,5′,8′,8′a-tetrahydrospiro[piperidine-4,2′(1′H)-quinazolin]-4′(3′H)-one |
      | L6 2 | 1036.0 | −11.12 | N-Benzyloxycarbonyl-(9-methyl-2,3,4,9-tetrahydro-1H-pyrido[3,4-b]indol-1-yl)methanamine |
      | L7 2 | 1381.0 | −11.56 | (1S,3R,4R,6R)-3-(benzylamino)methyl)-7,7-dimethylbicyclo[4.1.0]heptane-3,4-diol |
      ...
      | L8 2 | 1534.0 | −10.68 | 3-Amino-N-(2-fluoro-3-(trifluoromethyl)benzyl]-2-methylpropanamide trifluoroacetate |
      | L9 1 | 1716.0 | −10.87 | N-Benzyloxycarbonyl-(2,3,4,9-tetrahydro-1H-pyrido[3,4-b]indol-1-yl)methanamine |
      | L10 1 | 2154.0 | −11.58 | (4R*,11bR*)-9,10-Diethoxy-4-[4-(dimethylamino)phenyl]-1,3,4,6,7,11b-hexahydro-2H-pyrimido[6,1-a]isoquinoline |
      | L11 1 | 2381.0 | −10.55 | 1-{[(Benzyloxycarbonyl)amino]methyl}-6,7-dimethoxy-1,2,3,4-tetrahydroisoquinoline |
      | L12 2 | 3266.0 | −9.69 | (1R*,9bR*)-1-{[(4-Chlorophenyl)thio]methyl}-7,8-diethoxy-1,4,5,9b-tetrahydro-2H-azeto[2,1a]-isoquinoline |
      ...
      The three highest ranked compounds are chiral molecules, which have two enantiomeric forms. The enantiomers were separated and their binding affinities to S1R and S2R were measured separately (Table 4 and Figure 4). The binding constants to S1R were determined similarly to those of the racemic compounds. In the case of S2R, competition binding experiments were carried out by incubating rat liver membranes with 17 nM of [3H]DTG (Kd = 47 nM) in the presence of 100 nM (+)-pentazocine to mask S1R binding sites.
      ...
      (S)-L1 (Ki = 11 nM) showed much higher affinity for S1R than S2R sites and exhibited a similar, 15-fold S1R selectivity, as was previously shown by the fluoroethyl analog of S1R agonist SA4503 (cutamesine), where the ratio was KiS2R/KiS1R = 14.1 [66]. (R)-L3 (Ki = 58 nM) possessed a good binding affinity towards S1R and displayed a 3-fold lower affinity to S2R. Compound (S)-L2 (Ki = 81 nM) had a moderate affinity for the S1R site and the most favorable S1R selectivity (KiS2R/KiS1R = 63). Compounds (S)-L3 (Ki = 132 nM), (R)-L1 (Ki = 252 nM), and (R)-L2 (Ki = 699 nM) showed modest affinities towards S1R, and weak S2R bindings, with the exception of compound (R)-L1 which is weakly S2R selective.
      ...
      ). Each of
      ...
      pose of the antagonist. Only (R
      ...
      L1 enters, at least partially, the binding pocket P2 occupied by (+)-pentazocine in the original X-ray structure. In
      ...
      case of L1, these poses belong to the complex formed with the 6DK1A S1
      ...
      model. (S)-L1 has a better docking score (−11.62 kcal/mol) than (R)-L1 (−10.97 kcal/mol) in accordance with the measured Ki values (Table 4). The most preferred binding mode of (R)/(S)-L2 belongs to chain 5HK1A/6DK1C, respectively, with a docking score of −12.41/−12.28 kcal/mol. Their order
      ...
      opposite to that obtained from our measurements. Finally
      ...
      enantiomers of
      ...
      5HK1A binding
      ...
      docking score values of
      ...
      kcal/mol and −11
      ...
      95 kcal/mol for
      ...
      (S) and (R) enantiomers properly reflect
      ...
      experimental binding affinities.

      ---

      Title: Structural features important for sigma 1 receptor binding
      URL: https://pubmed.ncbi.nlm.nih.gov/8164264/
      Published: 1994-04-15T08:46:53.000Z
      Author: N/A
      Highlights:
      Two problems that have hampered sigma receptor research are (i) a lack of high-affinity agents and (ii) the recent identification of multiple populations of sigma receptors (i.e., sigma 1 and sigma 2 sites). Recently, several high-affinity sigma ligands have been identified, and the term superpotent sigma ligands has been coined to describe agents with Ki values of < 1 nM. We have previously shown that appropriately N-substituted phenylalkylamines bind at sigma receptors with high affinity. In the present investigation, we examine the structure-affinity relationships of these phenylalkylamine derivatives for sigma 1 binding and describe some of the first superpotent sigma 1 ligands. A binding model was developed to account for the structural features of the phenylalkylamines that appear to be important for the interaction of these agents with sigma 1 sites.
```
/answer f03333a0-9fa1-47db-ba66-db2182de2440 allow
Control Request:
```yaml
id: be3def83-9cec-4417-841b-81717a33cef7
toolName: web-search-exa
arguments:
  query: diphenhydramine NMDA receptor affinity binding Ki antagonist
  reason: Get DPH NMDA receptor Ki for occupancy calculation
```
/answer be3def83-9cec-4417-841b-81717a33cef7 allow
ReasoningToken: 316
Control Request:
```yaml
id: e813209d-5ba2-4dd4-a119-557509f39cf9
result:
  structuredContent:
    content: "Title: Open channel block of NMDA receptors by diphenhydramine\nURL: https://pubmed.ncbi.nlm.nih.gov/26284492/\nPublished: N/A\nAuthor: N/A\nHighlights:\nChecking your browser - reCAPTCHA\n\nChecking your browser before accessing pubmed.ncbi.nlm.nih.gov ...\n\nClick here if you are not automatically redirected after 5 seconds.\n\nChecking your browser - reCAPTCHA\nChecking your browser before accessing pubmed.ncbi.nlm.nih.gov ...\nClick [here](#) if you are not automatically redirected after 5 seconds.\n\n---\n\nTitle: Diphenhydramine inhibits NMDA-induced currents - New pharmacological aspects of a well known drug\nURL: https://journals.lww.com/ejanaesthesiology/fulltext/2014/06001/diphenhydramine_inhibits_nmda_induced_currents__.401.aspx\nPublished: N/A\nAuthor: N/A\nHighlights:\n**Background and Goal of Study:**Diphenhydramine (2-diphenylmethoxy-N,N-dimethylethylamine) is a well known H1-receptor antagonist that plays a major role in clinical practice. It disposes antiallergic, antiemetic and sedative properties. Nowadays, diphenhydramine is primarily applied in the case of nausea, but also its sedative effect is of vitally clinical importance. Even though the H1-antagonism might explain the sedative property of diphenhydramine, it is not unlikely that other receptors contribute to this quality. As other drugs mediating sedative properties partly operate via the inhibition of glutamate receptors, we tested the hypothesis if diphenhydramine interacts with excitatory ionotropic glutamate receptors.\n...\n**Results and discussion:**Diphenhydramine selectively blocked NMDAreceptors whereas AMPA- and kainate receptors were hardly affected. The inhibition occurred in a non-competitive manner. Diphenhydramine did not compete with NMDA or glycine for their binding sites. Half-maximal inhibition was obtained around 25 μM diphenhydramine, independent of the subunit composition. The inhibition was caused by a classical open channel blocking mechanism as there was no interaction in the absence of agonists. Furthermore, the inhibitory efficacy varied strongly with the membrane potential. It is shown that diphenhydramine most probably interacts via the Mg2+binding site or a very closely related area of the channel pore.\n...\n**Conclusion(s):**Diphenhydramine inhibits NMDA-mediated membrane currents in a reversible and concentration-dependent manner at clinical relevant concentrations. The data of our study provides evidence that the NMDA receptor antagonism of diphenhydramine may contribute to its sedative effects.\n\n---\n\nTitle: In-Silico Study of Diphenhydramine and Orphenadrine Binding Affinities to H1 and NMDA Receptors: Implications for Pharmacological Effects\n\t\t\t\t\t\t\t| Indonesian Journal of Life Sciences\nURL: https://journal.i3l.ac.id/index.php/IJLS/article/view/222\nPublished: N/A\nAuthor: metatags generator\nHighlights:\nDiphenhydramine and orphenadrine are oral drugs designed to possess different functional groups that affect H1 and NMDA receptors, although for different purposes. This study compares their binding affinities with the two receptors to investigate whether it influences the differing pharmacological effects exerted. This could help better understand the mechanisms, benefits, and risks of the drugs. The physicochemical properties were analyzed using Swiss-ADME, while the binding affinities were tested by molecular docking with PyRx. Lastly, visualization and analysis were done using the BIOVIA Drug Discovery Studio. The result suggests that both drugs have the same affinity for H1 receptors, however, orphenadrine has a slightly higher affinity to NMDA than diphenhydramine. This finding suggests that the binding ability and affinity of orphenadrine to NMDA is the factor of its pharmacological effect difference compared to diphenhydramine. Moreover, the difference in the functional group possessed by the two drugs will make a difference in their absorption and distribution.\n\n---\n\nTitle: Open Channel Block of NMDA Receptors by Diphenhydramine.\nURL: https://www.researchgate.net/publication/281141469_Open_Channel_Block_of_NMDA_Receptors_by_Diphenhydramine\nPublished: N/A\nAuthor: N/A\nHighlights:\nDiphenhydramine is a well known H1-receptor antagonist that plays a major role in clinical practice. Nowadays, diphenhydramine is primarily applied to prevent nausea but also its sedative and analgesic effects are of clinical importance. As other drugs mediating sedative and analgesic properties partly operate via the inhibition of glutamate receptors, we tested the hypothesis that diphenhydramine, as well interacts with excitatory ionotropic glutamate receptors.\n...\nDiphenhydramine inhibits NMDA-mediated membrane currents in a reversible and concentration-dependent manner at clinically relevant concentrations. The inhibition occurred in a noncompetitive manner. Diphenhydramine did not compete with NMDA or glycine for their binding sites and half-maximal inhibition was obtained around 25 μM diphenhydramine, independent of the subunit composition. The inhibition was caused by a classical open channel blocking mechanism and varied strongly with the membrane potential. Our results suggest that diphenhydramine most probably interacts with the Mg(2+) binding site or a very closely related area of the channel pore.\n...\nThe data presented here\n...\ncontribute to its sedative and potentially LTP-related effects like\n...\nia and amnesia.\n...\ncell recordings were performed using cultured\n...\ncortical neurons or Chinese hamster ovary (CHO) cells expressing\n...\nDA receptors. Both\n...\nand memantine\n...\nNMDA-\n...\nto a site at which they could be trapped after channel closure and agonist unbinding. For neuronal receptors, the IC50s of amantadine and memantine at -67 mV were 39 and 1.4 microM, respectively. When memantine and agonists were washed off after steady-state block, one-sixth of the blocked channels released rather than trapped the blocker; memantine exhibited \"partial trapping.\" Thus memantine appears to have a lesser tendency to be trapped than do phencyclidine or (5R,10S)-(+)-5-methyl-10,11-dihydro-5H-dibenzo[1,d]cyclihepten-5,1 0-imine (MK-801). We next investigated mechanisms that might underlie partial trapping. Memantine blocked and could be trapped by recombinant NMDA receptors composed of NR1 and either NR\n...\nA or NR2B subunits. In these receptors, as in the native receptors, the drug was released from one-sixth of blocked channels rather than being trapped in all of them. The partial trapping we observed therefore was not due to variability in the action of memantine on a heterogeneous population of NMDA receptors in cultured cortical neurons. Amantadine and memantine each noncompetitively inhibited NMDA-activated responses by binding at a second site with roughly 100-fold lower affinity, but this form of inhibition had little effect on the extent to which memantine was trapped. A simple kinetic model of blocker action was used to demonstrate that partial trapping can result if the presence of memantine in the channel affects the gating transitions or agonist affinity of the NMDA receptor. Partial trapping guarantees that during synaptic communication in the presence of blocker, some channels will release the blocker between synaptic responses. The extent to which amantadine and memantine become trapped after channel block thus may influence their therapeutic effects and their modulation of NMDA-receptor-mediated excitatory postsynaptic potentials.\n\n---\n\nTitle: In-Silico Study of Diphenhydramine and Orphenadrine to H1 and NMDA Receptors\nURL: https://journal.i3l.ac.id/index.php/IJLS/article/download/222/143\nPublished: N/A\nAuthor: N/A\nHighlights:\nDiphenhydramine and orphenadrine are both oral antihistamines but with different functional groups, which modulate their interaction with H1 and NMDA receptors, resulting in different therapeutic uses. This study investigates the comparative binding affinities of both drugs to these receptors and compares their physicochemical properties to understand structural influences on receptor interaction and potential pharmacokinetic profiles. Physicochemical properties, including Log P, pKa, and Lipinski's Rule of Five compliance, were evaluated using Swiss-ADME, and the compounds' binding affinities were screened through molecular docking using PyRx and visualized with BIOVIA Drug Discovery Studio. Results show that even though both drugs exhibit comparable affinities to the H1 receptor, orphenadrine has a slightly stronger affinity to the NMDA receptor than diphenhydramine. This interaction may explain the reason for their different therapeutic effects. Additionally, factors like Log P, pKa values, Boiled Egg analysis, and Lipinski's Rule all point to both drugs having good absorption, distribution, and oral bioavailability. These findings provide information on some of the mechanisms and pharmacokinetic factors that may differentiate diphenhydramine from orphenadrine, providing insights that may guide further empirical studies on their pharmacological effects and safety profiles.\n...\nH I G H L I G H T S\n\n❖ Diphenhydramine and orphenadrine have a comparable binding affinity toward H1 (8X5X)\nreceptor\n❖ Orphenadrine has a slightly higher binding affinity than diphenhydramine in NMDA (5EWL)\nreceptor\n❖ Orphenadrine has a higher bioavailability and a lower distribution to the brain in comparison to\ndiphenhydramine\n\nINTRODUCTION\n...\nMolecular docking is a computational method that analyzes a molecule’s orientation and conformation into the macromolecule’s binding site such as RNA, DNA, enzymes, receptors, and other bigger macromolecules. Using a simulation of the small molecule's molecular interactions with the target biomolecule, the approach can reveal information about the binding location, affinity, and potential mode of action (Torres et al., 2019). While both orphenadrine and diphenhydramine are recognized as Histamine 1 (H1) receptor antagonists, many studies on these drugs have not included a comparison of H1 receptor binding affinity between them at the molecular level. Additionally, both drugs also interact with the N-methyl-D-aspartic acid (NMDA) receptor, potentially contributing to their differing pharmacological effects and therapeutic applications. Therefore, this study aims to address the knowledge gap by examining the binding affinities of these drugs to both H1 and NMDA receptors. In addition to molecular docking, this research includes a comparison of the physicochemical properties of diphenhydramine and orphenadrine, providing insights that may guide further empirical studies on their pharmacological effects and safety profiles. In this study, we analyze binding affinities using molecular docking methods. Structures for each compound and receptor were sourced from online databases. Each compound was docked against the H1 and NMDA receptor to compare binding affinities and determine whether binding occurs at an allosteric or orthosteric site. Furthermore, a web tool was used to calculate the physicochemical properties of each drug, providing additional insights into pharmacokinetic factors that could influence receptor binding and pharmacological effects. This comprehensive approach seeks to clarify how binding characteristics, and physicochemical properties affect the therapeutic roles and mechanisms of diphenhydramine and orphenadrine.\n...\nRESULT\nBinding affinity\nBinding affinity indicates the strength of the interaction between a ligand and its receptor. As shown\nin Table 2, the binding affinity from the best pose of diphenhydramine and orphenadrine in the H1 receptor\nhas the same value (-6.6 kcal/mol). Whereas, in the NMDA receptor, orphenadrine has a higher binding\naffinity compared to diphenhydramine with the value of -6.6 kcal/mol and -6.4 kcal/mol respectively.\n\nTable 1. Binding affinity of diphenhydramine and orphenadrine to 8X5X (H1) and 5EWL (NMDA) receptor.\n...\nBinding Affinity Diphenhydramine (kcal/mol)\n\nBinding Affinity Orphenadrine (kcal/mol) 8X5X (H1) -6.6 -6.6 5EWL (NMDA) -6.4 -6.6\n...\nThe ligand-protein interaction of diphenhydramine and orphenadrine with the NMDA receptor in the 2D and 3D models are presented in Figures 4 and 5. The benzene rings of diphenhydramine interacted with five amino acids, which are aspartic acid (ASP, B: 286), tyrosine (TYR, B:287), arginine (ARG, B:347), leucine (LEU, B:349), and lysine (LYS, B: 361). Meanwhile, the benzene rings of orphenadrine interacted with four amino acids which include arginine (ARG, B: 347), aspartic acid (ASP, B:286), and tyrosine (TYR, B:387). The carbon (alkyl group) interacts with aspartic acid (ASP, B: 295) while the carbon (N-methyl) interacts with histidine (HIS, B: 359). Lastly, the amine interacts with leucine (LEU, B:349).\n...\n(Salahudeen & Nishtala,\n...\n2017). Using an online tool for all\n...\nprediction, we\ninvestigated the receptors' allosteric sites and visualized them with the best-posed ligand from our\nmolecular docking to ascertain the binding locations of our ligands.\nOur findings indicated that the H1 receptor's 8x5x allosteric site was absent. As a result,\norphenadrine and diphenhydramine bonded to the active site of the H1 receptor. On the other hand, the\nNMDA receptor (5EWL) was shown to have three allosteric pockets. Orphenadrine bonded to the NMDA\nreceptor at an allosteric location and diphenhydramine at the active site (Figure 6), according to the\nvisualization.\n...\n). As shown in Table\n...\nfor both dip\n...\non the\n...\nreceptor (8X\n...\nyielded the same binding affinity of -6.6 kcal/mol at the orthosteric site as expected.\n...\nNMDA-type\n...\n2020; Traynelis et al., 2010). From Table 2, orphenadrine has a slightly higher binding affinity, with a score of\n...\n-6.6 kcal/mol compared to diphenhydramine's -6.4 kcal/mol. This suggests that orphenadrine may bind\n...\nto the receptor\n...\nparameter prediction for dip\n...\n. The two compounds showed almost\n...\naffinities for the H1 receptors, but orphenadrine showed a slightly higher affinity for the NMDA receptors\n...\nCONCLUSION\nThe pharmacological differences between orphenadrine and diphenhydramine as oral medications\nare elucidated through their binding affinities to the H1 receptor. The present study found a similar affinity\n...\nfor both compounds, corresponding to previously reported antihistaminic activities. Meanwhile,\norphenadrine has a higher affinity for the NMDA receptor than diphenhydramine, suggesting that the\n...\ndifferent binding affinity of the NMDA receptor could be one reason for the different pharmacological\n...\nactions. Knowledge of these affinities can help optimize therapeutic use, pointing out benefits, risks, and\n\n---\n\nTitle: In-Silico Study of Diphenhydramine and Orphenadrine Binding Affinities to H1 and NMDA Receptors: Implications for Pharmacological Effects\nURL: https://doi.org/10.54250/ijls.v7i1.222\nPublished: 2025-03-19T00:00:00.000Z\nAuthor: Andrea Dhieta Utama, Azura Luna Widiyanto, Elizabeth Ervin, Lia Elvina, Rachel Josephine Cahya, Silvania Feliecia, et al.\nHighlights:\n# In-Silico Study of Diphenhydramine and Orphenadrine Binding Affinities to H1 and NMDA Receptors: Implications for Pharmacological Effects\n...\nDiphenhydramine and orphenadrine are oral drugs designed to possess different functional groups that affect H1 and NMDA receptors, although for different purposes. This study compares their binding affinities with the two receptors to investigate whether it influences the differing pharmacological effects exerted. This could help better understand the mechanisms, benefits, and risks of the drugs. The physicochemical properties were analyzed using Swiss-ADME, while the binding affinities were tested by molecular docking with PyRx. Lastly, visualization and analysis were done using the BIOVIA Drug Discovery Studio. The result suggests that both drugs have the same affinity for H1 receptors, however, orphenadrine has a slightly higher affinity to NMDA than diphenhydramine. This finding suggests that the binding ability and affinity of orphenadrine to NMDA is the factor of its pharmacological effect difference compared to diphenhydramine. Moreover, the difference in the functional group possessed by the two drugs will make a difference in their absorption and distribution.\n\n---\n\nTitle: Article - Open channel block of NMDA receptors by diphenhydramine. - Nutrition Evidence Database\nURL: https://nutrition-evidence.com/article/237415/open-channel-block-of-nmda-receptors-by-diphenhydramine\nPublished: 2016-08-30T00:00:00.000Z\nAuthor: N/A\nHighlights:\nDiphenhydramine is a well known H1-receptor antagonist that plays a major role in clinical practice. Nowadays, diphenhydramine is primarily applied to prevent nausea but also its sedative and analgesic effects are of clinical importance. As other drugs mediating sedative and analgesic properties partly operate via the inhibition of glutamate receptors, we tested the hypothesis that diphenhydramine, as well interacts with excitatory ionotropic glutamate receptors.\n...\nDiphenhydramine inhibits NMDA-mediated membrane currents in a reversible and concentration-dependent manner at clinically relevant concentrations. The inhibition occurred in a noncompetitive manner. Diphenhydramine did not compete with NMDA or glycine for their binding sites and half-maximal inhibition was obtained around 25 μM diphenhydramine, independent of the subunit composition. The inhibition was caused by a classical open channel blocking mechanism and varied strongly with the membrane potential. Our results suggest that diphenhydramine most probably interacts with the Mg2+ binding site or a very closely related area of the channel pore.\n...\nThe data presented here provide evidence that the NMDA receptor antagonism of diphenhydramine contribute to its sedative and potentially LTP-related effects like analgesia and amnesia.\n\n---\n\nTitle: Open channel block of NMDA receptors by diphenhydramine\nURL: https://doi.org/10.1016/j.neuropharm.2015.08.021\nPublished: 2015-08-15T00:00:00.000Z\nAuthor: Karl J. Föhr, Kathrin S. Zeller, Michael Georgieff, Sarah Köster, Oliver Adolph\nHighlights:\n# Open channel block of NMDA receptors by diphenhydramine\n...\n- Henry U. Weigt, Oliver Adolph, Michael Georgieff, E.-M. Georgieff, Karl J. Föhr. Evidence That Xenon Does Not Produce Open Channel Blockade of the NMDA Receptor. Journal of Neurophysiology. 2008;99(4):1983-1987. doi:10.1152/jn.00631.2007.\n...\nHenry U. Weigt, Karl J. Föhr, Michael\n...\n, E.-M. Georg\n...\nff, Uwe Senftleben, Oliver Adolph. Xenon blocks AMPA and NMDA receptor channels by different mechanisms. Acta\n...\n29-44\n...\nane-2\n...\n09-1\n...\n- Geoff Mealing, Thomas H. Lanthorn, Christine L. Murray, Daniel L. Small, Paul\n...\n22-3\n...\n)379\n...\nSean D. Done\n\n---\n\nTitle: Garuda - Garba Rujukan Digital\nURL: https://garuda.kemdiktisaintek.go.id/documents/detail/5619563\nPublished: N/A\nAuthor: kementrian riset, teknologi dan pendidikan tinggi\nHighlights:\n### In-Silico Study of Diphenhydramine and Orphenadrine Binding Affinities to H1 and NMDA Receptors: Implications for Pharmacological Effects\n...\nDiphenhydramine and orphenadrine are oral drugs designed to possess different functional groups that affect H1 and NMDA receptors, although for different purposes. This study compares their binding affinities with the two receptors to investigate whether it influences the differing pharmacological effects exerted. This could help better understand the mechanisms, benefits, and risks of the drugs. The physicochemical properties were analyzed using Swiss-ADME, while the binding affinities were tested by molecular docking with PyRx. Lastly, visualization and analysis were done using the BIOVIA Drug Discovery Studio. The result suggests that both drugs have the same affinity for H1 receptors, however, orphenadrine has a slightly higher affinity to NMDA than diphenhydramine. This finding suggests that the binding ability and affinity of orphenadrine to NMDA is the factor of its pharmacological effect difference compared to diphenhydramine. Moreover, the difference in the functional group possessed by the two drugs will make a difference in their absorption and distribution.\n\n---\n\nTitle: Mechanisms of NMDA Receptor Inhibition by Sepimostat—Comparison with Nafamostat and Diarylamidine Compounds\nURL: https://doi.org/10.3390/ijms242115685\nPublished: 2023-10-27T00:00:00.000Z\nAuthor: Arseniy S. Zhigulin, Oleg I. Barygin\nHighlights:\nDextromethorphan-yet another NMDA receptor channel blocker-is an antitussive agent that was recently approved for treatment of major depressive disorder in combination with bupropion [8] . For many other pharmaceuticals, NMDA receptors are an additional target that can possibly mediate negative or positive side effects. For instance, they are inhibited by traditional antidepressants desipramine and fluoxetine [9, 10] , antihistamine com-2 of 15 pounds promethazine [11] and diphenhydramine [12] , and local anesthetics bupivacaine, lidocaine, procaine, and tetracaine [13] .\n...\nIn this paper, we used patch clamping to check whether sepimostat would be able to inhibit native NMDA receptors and to describe its kinetics and molecular mechanisms of action. We compared the mechanisms of NMDA receptor inhibition by sepimostat to those of nafamostat and gabexate [17] , furamidine [17] , pentamidine, diminazene, and DAPI [16] . All these compounds are somewhat structurally similar, having aromatic cycles in the central parts of the molecules and positively charged nitrogene-containing groups on at least one side. Our comparative analysis demonstrated that the action of all these compounds can be readily described by the two-component mechanism. All compounds demonstrated similar affinity to the shallow site, which is responsible for the voltage-independent inhibition with binding constants in the range of 3-30 µM. In contrast, affinities to the deep site, which corresponds to the open-channel block, differed dramatically, with nafamostat, furamidine, and pentamidine being much more active. Among the compounds, only flexible pentamidine demonstrated a trapping block, gabexate did not demonstrate any signs of a \"foot-in-the-door\" or trapping channel block, and all others were \"foot-in-the-door\" blockers.\n...\n. We decided to reanalyze our data on the voltage-dependencies of the action of nafamostat, furamidine, pentamidine, diminazene, gabexate, and DAPI [16, 17] using Equation (2) for the first time. The binding constants for the deep (K vd ) and shallow (K vi ) sites are presented in Table 1 . * binding constants calculated using Equation (2) with fixed zδ values of 0.55 and 1.1 for mono-and dicationic compounds, respectively. Sepimostat was considered as monocation.\n...\nAll parameters are very close for the voltage-dependent blockers nafamostat, furamidine, and pentamidine, including zδ values of 1.1 to 1.4. The second group includes sepimostat and diminazene with large Kvd values and zδ values of 0.6 and 0.9, respectively. For the voltage-independent inhibitors DAPI and gabexate, the parameters, which describe a voltage-dependent block, cannot be estimated reliably. However, the experimental data on gabexate and DAPI can be readily fitted with the consensus zδ value 1.1 for the doubly charged DAPI (taken from fitting of nafamostat and furamidine) and 0.55 for the single-charged gabexate (taken from fitting of sepimostat) (see Table 1 and Figure 6 ). According to this fitting, all compounds demonstrate the presence of a voltageindependent component of action. Moreover, the obtained binding constants to the shallow site all laid in the narrow range from 3 to 30 µ M. The voltage-dependent component of the action is described by consensus zδ values of 0.55 for monocationic compounds and 1.1 for dicationic compounds. The binding constants for the deep site * binding constants calculated using Equation (2) with fixed zδ values of 0.55 and 1.1 for mono-and dicationic compounds, respectively. Sepimostat was considered as monocation. ** not applicable.\n...\nAll parameters are very close for the voltage-dependent blockers nafamostat, furamidine, and pentamidine, including zδ values of 1.1 to 1.4. The second group includes sepimostat and diminazene with large K vd values and zδ values of 0.6 and 0.9, respectively. For the voltage-independent inhibitors DAPI and gabexate, the parameters, which describe a voltage-dependent block, cannot be estimated reliably. However, the experimental data on gabexate and DAPI can be readily fitted with the consensus zδ value 1.1 for the doubly charged DAPI (taken from fitting of nafamostat and furamidine) and 0.55 for the singlecharged gabexate (taken from fitting of sepimostat) (see Table 1 and Figure 6 ). According to this fitting, all compounds demonstrate the presence of a voltage-independent component of action. Moreover, the obtained binding constants to the shallow site all laid in the narrow range from 3 to 30 µM. The voltage-dependent component of the action is described by consensus zδ values of 0.55 for monocationic compounds and 1.1 for dicationic compounds. The binding constants for the deep site differed dramatically, ranging from 10 µM for nafamostat to >1 mM for sepimostat, diminazene, and DAPI. Thus, the main variations in the voltage dependence seen in Figure 6 are due to the difference in only one characteristic (K vd ). The single exception is camostat, which exhibited low activity and was not studied in detail.\n...\nWe have also systematically compared molecular mechanisms of inhibition by sepimostat to those of other serine protease inhibitors (nafamostat, gabexate, and camostat) and diarylamidine compounds (pentamidine, furamidine, diminazene, and DAPI). Except for DAPI, abovementioned compounds demonstrated complex voltage dependence with voltage-dependent and voltage-independent components, suggesting binding to the deep site in the pore and a superficial site. The action of DAPI was completely voltageindependent. Likely, affinity for the deep binding site is low, and a weak voltage-dependent component of the action is masked by the voltage-independent inhibition. The analysis of voltage dependencies of nafamostat, furamidine, and diminazene gave zδ values of about 1.0. That of pentamidine was higher-1.4. This subtle difference can be easily explained by the flexibility of pentamidine molecule, resulting in the interaction of both charged groups with the selectivity filter [16] . In the case of nafamostat, furamidine, and diminazene, the first charged group interacts with the selectivity filter while the second one is situated shallower because of the rigidity of these molecules [16, 17] . The zδ value for sepimostat was two times smaller (0.6), which is in a good agreement with the domination of its +1 charged form. The deep site for channel blockers (Mg 2+ , memantine, ketamine, MK-801, and others) in the NMDA receptor channel pore is well characterized [29, 30] . Such compounds bind to the NMDA receptor selectivity filter asparagines. Their interactions with pore-lining residues are slightly different [30] , but the binding region is the same. Our data suggest that the voltage-dependent component of the action of nafamostat, sepimostat, pentamidine, furamidine, and diminazene corresponds to the binding to this site.\n...\nOpen channel block of NMDA receptors by diphenhydramine K J Fohr K Zeller M Georgieff S Koster O Adolph 10.1016/j.neuropharm.2015.08.021 Neuropharmacology 99 2015 Fohr, K.J.; Zeller, K.; Georgieff, M.; Koster, S.; Adolph, O. Open channel block of NMDA receptors by diphenhydramine. Neuropharmacology 2015, 99, 459-470. [CrossRef] [PubMed] 10. Barygin, O.I.; Nagaeva, E.I.; Tikhonov, D.B.; Belinskaya, D.A.; Vanchakova, N.P.; Shestakova, N.N. Inhibition of the NMDA and AMPA receptor channels by antidepressants and antipsychotics. Brain Res. 2017, 1660, 58–66. [CrossRef]\n...\nPentamidine is an N-methyl-D-aspartate receptor antagonist and is neuroprotective in vitro I J Reynolds E Aizenman 10.1523/JNEUROSCI.12-03-00970.1992 J. Neurosci 12 1992 Reynolds, I.J.; Aizenman, E. Pentamidine is an N-methyl-D-aspartate receptor antagonist and is neuroprotective in vitro. J. Neurosci. 1992, 12, 970-975. [CrossRef] 12. Fohr, K.J.; Zeller, K.; Georgieff, M.; Koster, S.; Adolph, O. Open channel block of NMDA receptors by diphenhydramine. Neuropharmacology 2015, 99, 459–470. [CrossRef] [PubMed]"
```
/answer e813209d-5ba2-4dd4-a119-557509f39cf9 allow
Control Request:
```yaml
id: 17322281-97b3-4c4f-ad26-6b21a4e77f40
toolName: web-search-exa
arguments:
  query: diphenhydramine alpha-2 adrenergic receptor binding affinity Ki
  reason: Get DPH alpha2 receptor Ki for occupancy calculation
```
/answer 17322281-97b3-4c4f-ad26-6b21a4e77f40 allow
Control Request:
```yaml
id: e4745ecc-2417-4638-9b8b-bbf839953f69
result:
  structuredContent:
    content: |-
      Title: Diphenhydramine · Sugi Atlas
      URL: https://sugi.bio/atlas/drug/diphenhydramine/
      Published: N/A
      Author: N/A
      Highlights:
      | Alpha-1A adrenergic receptor | P35348 | ADRA1A | 5.2 | AC50 | 6312 nM | CHEMBL_ACT_25138129 |
      | Alpha-2B adrenergic receptor | P18089 | ADRA2B | 5.16 | AC50 | 7000 nM | CHEMBL_ACT_25144052 |
      ...
      | Alpha-2A adrenergic receptor | P08913 | ADRA2A | 5.02 | AC50 | 9548 nM | CHEMBL_ACT_25156804 |

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
      #### diphenhydramine
      ...
      Comment: Diphenhydramine has anti-histamine action.
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

      ---

      Title: The affinity and selectivity of α‐adrenoceptor antagonists, antidepressants and antipsychotics for the human α2A, α2B, and α2C‐adrenoceptors and comparison with human α1 and β‐adrenoceptors
      URL: https://doi.org/10.1002/prp2.936
      Published: 2022-02-27T00:00:00.000Z
      Author: Richard G. W. Proudman, Juliana Akinaga, Jillian G. Baker
      Highlights:
      subtype affinity is difficult due to significant species and methodology differences in published studies. Here, 3 H-rauwolscine whole cell binding was used to determine the affinity and selectivity of 99 α-antagonists (including antidepressants and antipsychotics) in CHO cells expressing human α2A, α2B, or α2C-adrenoceptors, using an identical method to β and α1-adrenoceptor measurements, thus allowing direct human receptor comparisons. Yohimbine, RX821002, RS79948, and atipamezole are high affinity non-selective α2-antagonists. BRL44408 was the most α2A-selective antagonist, although its α1A-affinity (81 nM) is only 9-fold greater than its α2C-affinity. MK-912 is the highest-affinity, most α2C-selective antagonist (0.15 nM α2C-affinity) although its α2C-selectivity is only 13-fold greater than at α2A. There are no truely α2B-selective antagonists. A few α-ligands with significant β-affinity were detected, for example, naftopidil where its clinical α1A-affinity is only 3-fold greater than off-target β2-affinity.
      ...
      The affinity and selectivity of a large range of α-adrenoceptor antagonists was evaluated (Figure 1 ; Table 2 ). It is clear that there are few α2-subtype selective ligands. Dibenamine and phenoxybenzamine inhibited 3 H-rauwolscine binding in a manner best described by a two-component response in CHO-α2B cells for both compounds and for phenoxybenzamine in CHO-α2C cells (Figure 2 , Table 2 ) in a manner similar to that seen in the α1-adrenoceptors. 33 The responses in CHO-α2A cells and for dibenamine in CHO-α2C cells were too low affinity for a second component to be clearly determined. Dibenamine and phenoxybenzamine both contain a nitrogen mustard group, which cyclises to form ethyleniminium ions. 38 Sodium thiosulphate reacts with the ethyleniminium ions preventing them interacting with α-adrenoceptors. 38 Preincubation with sodium thiosulphate abolished the higher affinity components and reduced the affinity of both ligands at all three receptors a follows: dibenamine 2 are therefore highly likely to be the affinity of the ligand interacting with the receptor (as in 33 ).
      ...
      had a lower affinity
      ...
      2B-adrenoceptors
      ...
      or α2C, in keeping with
      ...
      , 29 and in tissues. 7, 3
      ...
      40 Other compounds with high affinity at all 3 subtypes were: atipamezole 3
      ...
      , 39 and RS79948 27 and should thus be regarded as non-selective α2ligands. Lisuride has a high affinity across many different
      ...
      subtypes. 41, 42 L44408 (65 nM at α2A) was the most α2A-adrenoceptor selective ligand in keeping with 22, 24, 26, 43 however although
      ...
      was 60-fold selective for α2
      ...
      B, BRL44408
      ...
      s selectivity for α
      ...
      over α2C-adrenoceptors was only 9-fold. Although S32212 and ARC
      ...
      were 15-to
      ...
      21-fold selective for
      ...
      is marginal (
      ...
      fold), in keeping with
      ...
      and thus there are no
      ...
      however its affinity (120 nM at
      ...
      (16-2
      ...
      renoceptors. Values represent mean ±s.e.mean of n separate
      ...
      . Selectivity ratios are also given, where
      ...
      selectivity for a given
      ...
      in order of
      ...
      selectivity. Note
      ...
      -adrenoceptor
      ...
      however others suggest a human
      ...
      13 nM.
      ...
      3 betolol and carvedilol are often usually referred to as
      ...
      α/βblockers (e.g.,. 49 ). Labetolol (affinities of β2 6-9 nM, β1 11-23 nM, and α1A 47 nM) has very poor affinity at α1B, α1D,
      ...
      β3-adrenoceptors and thus
      ...
      affinity at only
      ...
      out of 6 α-adrenoceptors. A β/α1A-antagonist would be a more accurate description. Likewise
      ...
      .1-0.4 nM, β1
      ...
      -1.8 nM, and β3 of 5 nM also has highest α-affinity for α1A (4 nM) over α1B or α1D (14 nM) or α2-adrenoceptors (48-490 nM
      ...
      with affinities up to 1000-fold different across the 9 different adrenoceptors should not be considered a pan α/β-blocker. The lack of affinity of other β
      ...
      inhibit specific binding and
      ...
      to previous α1 and βadrenoceptor studies, allows comparison of ligand affinity, and thus selectivity, between the α
      ...
      β-adrenoceptor subtypes. Overall, there is huge variation in the
      ...
      ligands (more so
      ...
      β), and for which species differences appear to play
      ...
      significant role,
      ...
      technique may also
      ...
      important. Whilst selective antagonists exist
      ...
      Inhibition of 3 H-ra
      ...
      olscine binding to whole cells by BRL44408 (A-C), S32212 (D-F) or MK-912 (G-I) to CHO-α2A cells (A, D, G), CHO-α2B cells (B, E, H) or CHO-α2C cells (C, F, I). Bars represent total 3 H-rauwolscine and non-specific binding (determined in
      ...
      presence of 10μM RX821002. The concentration of 3 H-rauwolscine was (A) 0.99 nM, (B) 0.99 nM, (C) 0.99 nM, (D) 0.88 nM, (E) 0.88 nM, (F) 0.88 nM, (G) 0.86 nM, (H) 0.86 nM, and (I) 0.88 nM. Data points are mean ±s.e.mean of triplicate determinations TA B L E 2 Log K D values obtained from inhibition of 3 H-rauwolscine binding by adrenoceptor antagonists to the human α2A, α2B, and α2C-adrenoceptors in living cells. Values represent mean ±s.e.mean of n separate experiments. Selectivity ratios are also given where a ratio of 1 demonstrates no selectivity for a given receptor subtype over another. Thus BRL44408 has 60fold higher affinity for the α2A than the α2B-adrenoceptor. Compounds are arranged in order of α2A-selectivity.
      ...
      | 5 | 1
      ...
      | 4.
      ...
      -5.
      ...
      oxan and
      ...
      values to those obtained in
      ...
      126 nM) in,5
      ...
      -adrenoceptors. Of no 51also reported similar values for mirtazapine for human and rat receptors, TA B L E
      ...
      Log K D values of antipsychotics binding to the human α2A, α2B, and α2C-adrenoceptors. Va ues represent mean ±s.e.mean of n separate experiments. Selectivity ratios are also given where
      ...
      ratio of 1 demonstrates no selectivity for a given receptor subtype over another. Compounds are arranged in order of α2A-selectivity. Affinity measurements | Selectivity ratios Ligand | Log K D α2A | n | Log K D α2B | n | Log K D α2C | n | α2A vs α2B | α2A vs α2C | α2B vs α2C First-generation antipsychotics sulpiride | -4.50 ± 0.02 | 5 | -4.37 ± 0.06 | 5 | -4.67 ± 0.07 | 5 | 1.3 | 1.5 | 2.0 haloperidol | -5.38 ± 0.06 | 5 | -5.53 ± 0.10 | 5 | -5.77 ± 0.05 | 5 | 1.4 | 2.5 | 1.7 flupenthixol | -6.10 ± 0.12 | 5 | -6.28 ± 0.13 | 5 | -6.88 ± 0.14 | 5 | 1.5 | 6.0 | 4.0 pimozide | -5.76 ± 0.12 ep | 5 | -6.30 ± 0.10 | 5 | -6.84 ± 0.05 | 5 | 3.5 | 12.0 | 3.5 trifluoperazine | -5.60 ± 0.05 | 5 | -6.22 ± 0.12 | 5 | -6.20 ± 0.06 | 5 | 4.2 | 4.0 | 1.0 prochlorperazine | -5.78 ± 0.02 app | 6 | -6.46 ± 0.11 | 6 | -6.31 ± 0.09 | 6 | 4.8 | 3.4 | 1.4 chlorpromazine | -5.65 ± 0.13 app | 6 | -6.60 ± 0.12 | 6 | -5.93 ± 0.11 | 6 | 8.9 | 1.9 | 4.7 perphenazine | -6.00 ± 0.06 | 6 | -7.16 ± 0.05 | 6 | -6.83 ± 0.04 | 5 | 14.5 | 6.8 | 2.1 Second-generation antipsychotics amisulpiride | -5.11 ± 0.09 app | 5 | -4.69 ± 0.13 app | 5 | -5.57 ± 0.07 | 5 | 2.6 | 2.9 | 7.6 aripirazole | -6.68 ± 0.08 | 5 | -6.54 ± 0.08 | 6 | -7.23 ± 0.14 | 5 | 1.4 | 3.5 | 4.9 sertindole | -5.95 ± 0.06 | 5 | -5.81 ± 0.07 | 5 | -6.17 ± 0.03 | 5 | 1.4 | 1.7 | 2.3 olanzapine | -5.59 ± 0.05 | 5 | -5.47 ± 0.06 | 5 | -5.86 ± 0.02 | 5 | 1.3 | 1.9 | 2.5 paliperidone | -7.12 ± 0.04 | 5 | -7.26 ± 0.05 | 5 | -7.84 ± 0.03 | 5 | 1.4 | 5.2 | 3.8 risperidone | -7.30 ± 0.09 | 5 | -7.47 ± 0.08 | 5 | -8.04 ± 0.03 | 5 | 1.5 | 5.5 | 3.7 ziprasidone | -6.36 ± 0.11 | 5 | -6.59 ± 0.08 | 5 | -6.77 ± 0.08 | 5 | 1.7 | 2.6 | 1.5 clozapine | -5.86 ± 0.08 app | 5 | -6.20 ± 0.05 | 5 | -6.87 ±
      ...
      0.08 | 5 | 2
      ...
      | 1
      ...
      17,52Here, first generation antipsychotics had
      ...
      1 ) α2A 600 nM, α2B 43 nM, and α2C 260 nM ( 3 H-RX821002 membrane binding for human receptors expressed in CHO cells, 29 ) α2
      ...
      nM, α2B 34 nM, and α2C 85 nM ( 3 H-RX
      ...
      1002 membrane binding to human receptors expressed in
      ...
      2245 nM ( 3 H-RX821002 membrane binding to human platelets, 23 ) to α2A 4169 nM and α2C 1413
      ...
      2-adrenoceptor
      ...
      α1-adrenoceptors,
      ...
      had little selectivity for α2C over the other α2-sub
      ...
      . For example,

      ---

      Title: Diphenhydramine: Uses, Interactions, Mechanism of Action | DrugBank Online
      URL: https://web.archive.org/web/20240922051631/https:/go.drugbank.com/drugs/DB01075
      Published: N/A
      Author: N/A
      Highlights:
      Diphenhydramine - perhaps known most commonly as its brand name formulation Benadryl - is a first-generation H1 receptor antihistamine that is used extensively for the treatment of seasonal allergies, insect bites and stings, and rashes 9,10,11,17. However, it also has antiemetic, antitussive, hypnotic, and antiparkinson properties 11,16. As histamine receptors exist both peripherally and in the central nervous system, diphenhydramine has been shown to cause
      ...
      due to its competitive antagonism of histamine H1 receptors within the
      ...
      nervous system 9,10,11,17,5. While its use in allergy therapy can sometimes fall out of favor due to its sedative effect, diphenhydramine has been repurposed for use within many non-prescription
      ...
      -the-counter sleep aids and cough-and-cold medications that have been marketed for "night time" use 9,12,13.
      ...
      Diphenhydramine predominantly works via the antagonism of H1 (Histamine 1) receptors 9,10,11,17,5. Such H1 receptors are located on respiratory smooth muscles, vascular endothelial cells, the gastrointestinal tract (GIT), cardiac tissue, immune cells, the uterus, and the central nervous system (CNS) neurons 9,10,11,17,5. When the H1 receptor is stimulated in these tissues it produces a variety of actions including increased vascular permeability, promotion of vasodilation causing flushing, decreased atrioventricular (AV) node conduction time, stimulation of sensory nerves of airways producing coughing, smooth muscle contraction of bronchi and the GIT, and eosinophilic chemotaxis that promotes the allergic immune response 9,10,11,17,5.
      ...
      , diphenhydramine functions as
      ...
      9,1
      ...
      ,11
      ...
      17,5. Moreover
      ...
      since diphenhydramine is a first-generation antihist
      ...
      readily crosses the blood-brain barrier and inversely agon
      ...
      in drowsiness, and suppressing
      ...
      9,10,11
      ...
      Furthermore, H1 receptors are similar to muscarinic receptors 9,10,11,17,5. Consequently, diphenhydramine also acts as an antimuscarinic 9,10,11,17,5. It does so by behaving as a competitive antagonist of muscarinic acetylcholine receptors, resulting in its use as an antiparkinson medication 9,10,11,17,5.
      ...
      | Drug | Interaction |
      | --- | --- |
      | 1,2-Benzodiazep
      ...
      The risk or severity of CNS depression
      ...
      Diphenhydramine is
      ...
      1,2-Benz
      ...
      ine. |
      | Abat
      ...
      The metabolism of Diphenhydramine
      ...
      be increased when combined with Abatacept. |
      ...
      Abemaciclib

      ---

      Title: BindingDB BDBM50017674 (2-Benzhydryloxy-ethyl)-dimethyl-amine::2-(benzhydryloxy)-N,N-dimethylethanamine::2-(diphenylmethoxy)-N,N-dimethylethanamine::Antitussive::Beldin::Belix::Benadryl::Benylin::CHEMBL657::DIMENHYDRINATE::DIPHENHYDRAMINE::Dibenil::Diphen::Hydramine::N-[2-(BENZHYDRYLOXY)ETHYL]-N,N-DIMETHYLAMINE::Silphen::US9138431, DIPHENHYDRAMINE (Benadryl)::US9333199, DIPHENHYDRAMINE (Benadryl)
      URL: https://www.bindingdb.org/rwd/bind/chemsearch/marvin/MolStructure.jsp?monomerid=50017674
      Published: N/A
      Author: Tiqing Liu
      Highlights:
      Data 20 KI 22 IC50 1 Kd
      ...
      Affinity DataKi: 9.20nM More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 9.57nM More data for this Ligand-
      ...
      Target Alpha-1A adrenergic receptor(Rat)TBACurated by PDSP Ki Database
      ...
      BDBM
      ...
      4(Hydramine |
      ...
      LESCopy InChI
      ...
      Affinity DataKi: 3.50E+3nM More data for this Ligand-Target Pair
      ...
      Target Alpha-1A adrenergic receptor(Rat)TBACurated by PDSP Ki Database
      ...
      Ligand BDBM50017674(Hydramine | Benylin | Silphen | (2-Benzhydryloxy-e...)Copy SMILESCopy InChI
      ...
      Affinity DataKi: 3.50E+3nM More data for this Ligand-Target Pair

      ---

      Title: diphenhydramine | Ligand page | IUPHAR/BPS Guide to PHARMACOLOGY
      URL: https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=1224&tab=structure
      Published: N/A
      Author: N/A
      Highlights:
      #### diphenhydramine
      ...
      #### GtoPdb Ligand ID: 1224
      ...
      Synonyms: Benadryl® | benzhydramine | dimehydrinate
      ...
      diphenhydramine is an approved drug (FDA
      ...
      Comment: Diphenhydramine has anti-histamine action.
      ...
      (CCOC(c
      ...
      ccccc1)
      ...
      | --- | --- |
      ...
      | Isomeric SMILES | CN(CCOC
      ...
      1ccccc1)c1ccccc1)C |
      ...
      | InChI | InChI=1S/C17H21NO/c1-18(2)13-14-19-17(15-9-5-3-6-10-15)16-11-7-4-8-12-16/h
      ...
      12,17H,1
      ...
      -14H
      ...
      ,1-2H3 |
      | InChI Key | ZZVUWRFHKOJYTH-UHFFFAOYSA-N |

      ---

      Title: S-EPMC8882856 - The affinity and selectivity of α-adrenoceptor antagonists, antidepressants and antipsychotics for the human α2A, α2B, and α2C-adrenoceptors and comparison with human α1 and β-adrenoceptors. - OmicsDI
      URL: https://www.omicsdi.org/dataset/biostudies-literature/S-EPMC8882856
      Published: N/A
      Author: N/A
      Highlights:
      ABSTRACT: α2-Adrenoceptors, subdivided into α2A, α2B, and α2C subtypes and expressed in heart, blood vessels, kidney, platelets and brain, are important for blood pressure, sedation, analgesia, and platelet aggregation. Brain α2C-adrenoceptor blockade has also been suggested to be beneficial for antipsychotic action. However, comparing α2-adrenoceptor subtype affinity is difficult due to significant species and methodology differences in published studies. Here, 3 H-rauwolscine whole cell binding was used to determine the affinity and selectivity of 99 α-antagonists (including antidepressants and antipsychotics) in CHO cells expressing human α2A, α2B, or α2C-adrenoceptors, using an identical method to β and α1-adrenoceptor measurements, thus allowing direct human receptor comparisons. Yohimbine, RX821002, RS79948, and atipamezole are high affinity non-selective α2-antagonists. BRL44408 was the most α2A-selective antagonist, although its α1A-affinity (81 nM) is only 9-fold greater than its α2C-affinity. MK-912 is the highest-affinity, most α2C-selective antagonist (0.15 nM α2C-affinity) although its α2C-selectivity is only 13-fold greater than at α2A. There are no truely α2B-selective antagonists. A few α-ligands with significant β-affinity were detected, for example, naftopidil where its clinical α1A-affinity is only 3-fold greater than off-target β2-affinity. Antidepressants (except mirtazapine) and first-generation antipsychotics have higher α1A than α2-adrenoceptor affinity but poor β-affinity. Second-generation antipsychotics varied widely in their α2-adrenoceptor affinity. Risperidone (9 nM) and paliperidone (14 nM) have the highest α2C-adrenoceptor affinity however this is only 5-fold selective over α2A, and both have a higher affinity for α1A (2 nM and 4 nM, respectively). So, despite a century of yohimbine use, and decades of α2-subtype studies, there remains plenty of scope to develop α2-subtype selective antagonists.
      ...
      α2-Adreno

      ---

      Title: BindingDB PrimarySearch_ki
      URL: https://www.bindingdb.org/rwd/jsp/dbsearch/PrimarySearch_ki.jsp?Increment=50&column=KI&complexid=50001641&energyterm=kcal%2Fmole&startPg=0&submit=Search&tag=comki&target=UNIPROT%3AP19328
      Published: N/A
      Author: Tiqing Liu
      Highlights:
      Affinity DataKi: 0.0150nMAssay Description:In vitro binding affinity against alpha-2 adrenergic receptor in rat More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.126nMAssay Description:In vitro binding affinity against alpha-2 adrenergic receptor of rat in presence of [3H]-RX 821002 radioligand More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.355nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.355nMAssay Description:Binding affinity against alpha-2 adrenergic receptor in rat cerebral cortical membrane, determined using [3H]- yohimbine as the radioligand. More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.428nMAssay Description:In vitro binding affinity at Alpha-2 adrenergic receptor in rat cortex by radioligand binding assay using [3H]rauwolscine More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.450nMAssay Description:Binding affinity against alpha-2 adrenergic receptor was determined by the displacement of [3H]clonidine from rat brain cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.457nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.470nMAssay Description:Binding affinity against alpha-2 adrenergic receptor was determined by the displacement of [3H]clonidine from rat brain cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.5nMAssay Description:In vitro binding affinity at Alpha-2 adrenergic receptor in rat cortex by radioligand binding assay using [3H]rauwolscine More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.550nMAssay Description:Binding affinity for alpha-2 adrenergic receptor in rat cortex using [3H]rauwolscine. More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.560nMAssay Description:Binding affinity towards Alpha-2 adrenergic receptor in rat cerebral cortex using [3H]rauwolscine More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.603nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.646nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.661nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.661nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.661nMAssay Description:Binding affinity against alpha-2 adrenergic receptor in rat cerebral cortical membrane, determined using [3H]- yohimbine as the radioligand. More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.708nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.708nMAssay Description:In vitro binding affinity at Alpha-2 adrenergic receptor in rat cortex by radioligand binding assay using [3H]rauwolscine More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.708nMAssay Description:In vitro binding affinity at Alpha-2 adrenergic receptor in rat cortex by radioligand binding assay using [3H]rauwolscine More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.720nMAssay Description:Binding affinity against alpha-2 adrenergic receptor was determined by the displacement of [3H]clonidine from rat brain cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.794nMAssay Description:In vitro binding affinity against alpha-2 adrenergic receptor of rat in presence of [3H]-RX 821002 radioligand More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.910nMAssay Description:Binding affinity against alpha-2 adrenergic receptor was determined by the displacement of [3H]clonidine from rat brain cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.910nMAssay Description:Binding affinity against alpha-2 adrenergic receptor was determined by the displacement of [3H]clonidine from rat brain cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.10nMAssay Description:Evaluated for its ability to displace [3H]rauwolscine from alpha-2 adrenergic receptor of rat cerebral cortex More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.10nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.10nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.30nMAssay Description:In vitro binding affinity against alpha-2 adrenergic receptor of rat in presence of [3H]-RX 821002 radioligand More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.30nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.30nMAssay Description:In vitro binding affinity against alpha-2 adrenergic receptor of rat in presence of [3H]-RX 821002 radioligand More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.5nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.5nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.5nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.5nMAssay Description:In vitro binding affinity was measured as the inhibition of [3H]clonidine binding to alpha-2 adrenergic receptor of rat cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.5nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.5nMAssay Description:Binding affinity against alpha-2 adrenergic receptor was determined by the displacement of [3H]clonidine from rat brain cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.5nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 1.60nMAssay Description:In vitro binding affinity against alpha-2 adrenergic receptor of rat in presence of [3H]-RX 821002 radioligand More data for this Ligand-Target Pair
      ...
      Ki: 1.60nMAssay Description:Evaluated for its ability to displace
      ...
      Affinity DataKi: 1.60nMAssay Description:Binding affinity to alpha-2 adrenergic receptor determined by measurement of [3H]yohimbine displacement from rat cortical membrane More data for this Ligand-Target Pair

      ---

      Title: BindingDB PrimarySearch_ki
      URL: https://www.bindingdb.org/rwd/jsp/dbsearch/PrimarySearch_ki.jsp?Increment=50&column=ki&energyterm=kJ%2Fmole&reactant1=Alpha-2A+adrenergic+receptor+%5B16-465%5D%2FAlpha-2B+adrenergic+receptor%2FAlpha-2C+adrenergic+receptor&reactant2=BDBM50226938&startPg=0&submit=Search&tag=r20
      Published: N/A
      Author: Tiqing Liu
      Highlights:
      Affinity DataKi: 0.450nMAssay Description:Binding affinity against alpha-2 adrenergic receptor was determined by the displacement of [3H]clonidine from rat brain cortical membranes More data for this Ligand-Target Pair
      ...
      Affinity DataKi: 0.690nMAssay Description:Inhibition of saturable binding of [3H]idazoxan to alpha2-site in rat cerebral cortical membranes. More data for this Ligand-Target Pair
```
/answer e4745ecc-2417-4638-9b8b-bbf839953f69 allow
ReasoningToken: 6036
# Prüfung: Sigma-1, α2-Adrenozeptor, NMDA als Kandidaten für die Salven-Limitierung

Gleiches Vorgehen wie beim Na⁺-Kanal: Ki/Kd aus der Literatur, Occupancy bei C_frei ≈ 0,3–1 nM, Prüfung ob Salven-abhängige Kinetik den Ceiling anheben kann.

## 1. Affinitätsdaten

| Target | Ki/IC50 (DPH) | Quelle/Charakter |
|---|---|---|
| **S1R** | **58 nM** | Peng/Dong/Welsh 2018, humanes S1R, radioligand [³H]-Bindung |
| **α2-Adrenozeptor** | **~7.600 nM** (α2A AC50 9.548 nM, α2B AC50 7.000 nM) | ChEMBL/PDSP – schwacher Off-Target, klassisches GPCR-Gleichgewicht |
| **NMDA-R** | **IC50 ~25 µM**, spannungsabhängiger Open-Channel-Block an/nahe der Mg²⁺-Bindungsstelle | Föhr et al., Neuropharmacology 2015 – „klassischer" Open-Channel-Blocker, nicht-kompetitiv |

Zum Vergleich: **H1 Ki (in-vitro-Bindung) ≈ 14–20 nM**, Ihre ursprüngliche PET-abgeleitete Kd ≈ 1–4 nM (methodenabhängige Diskrepanz zwischen in-vitro-Ki und in-vivo-Occupancy-Kd – für die folgende Rechnung nehme ich beide als Sensitivitätsspanne).

## 2. Occupancy-Check bei C_frei ≈ 0,3–1 nM

$$Occ = \frac{C}{C+K_d}$$

| Target | Occ bei C=0,3–1 nM | Verhältnis zu H1-Occ (20 %) |
|---|---|---|
| H1 (Kd 1–4 nM) | ~20 % (Ausgangswert) | 1× |
| **S1R (58 nM)** | **~0,5–1,7 %** | ~12–40× niedriger |
| α2 (7.600 nM) | ~0,004–0,013 % | ~1.500–5.000× niedriger |
| NMDA (25.000 nM, open-state) | ~0,001–0,004 % | ~5.000–20.000× niedriger |

## 3. α2 und NMDA: gleiches Problem wie der Na⁺-Kanal → beide ausscheidend

- **α2**: reines GPCR-Gleichgewicht, keine publizierte Use-Dependence. Bei Ki 7,6 µM ist die Occupancy 3–4 Zehnerpotenzen unter H1 und bleibt es bei jeder klinisch erreichbaren Dosis – **ausscheiden**.
- **NMDA**: Der Föhr-Mechanismus (spannungs-/agonistabhängiger Open-Channel-Block, „klassischer" Mg²⁺-Site-Blocker) hat exakt die gleiche mathematische Struktur wie Ihr ursprünglicher Na⁺-Kanal-Ansatz: eine Salven-abhängige *Kinetik* kann den effektiven Ceiling maximal auf C/(C+Ki_open) anheben. Mit Ki_open ~25 µM und C ~0,3–1 nM liegt dieser Ceiling bei ~10⁻⁵ – **gleiches Verdikt, gleiche Begründung wie beim Na⁺-Kanal: ausscheiden.**

## 4. S1R: der einzige quantitativ plausible Kandidat – aber mit einer neuen Einschränkung

S1R ist das einzige Target, dessen Ki (58 nM) nah genug an H1 liegt (~4–15-fach höher, nicht 1.000–10.000-fach), um überhaupt in einem realistischen Konzentrationsfenster mitzuspielen. Zusätzlich ist S1R kein klassischer Ionenkanal, sondern ein ligandengesteuertes ER-Chaperon (moduliert IP3R3, Kv1.2, NR1, Nav1.5 u.a.) mit dokumentierter **Ca²⁺-/aktivitätsabhängiger Translokation** (BiP-Dissoziation, Umverteilung ER → Plasmamembran/MAM bei repetitiver Stimulation – Hayashi & Su). Das wäre ein *echter*, literaturgestützter Salven-abhängiger Verstärkungsmechanismus – aber **mechanistisch fundamental anders** als die Na⁺-Kanal-Use-Dependence: keine Kd-Verschiebung durch Kanalzustand, sondern Änderung der subzellulären Verfügbarkeit/Kopplungseffizienz des Rezeptors selbst. Das ist bisher nicht für kardiale/autonome Salven-Phänomene direkt belegt – als Hypothese plausibel, aber nicht verifiziert.

### Der entscheidende Dosis-Reduktions-Check für S1R vs. H1

Hier liegt das eigentliche Problem für Ihr Dosisreduktions-Ziel. Die Steigung der Occupancy-Kurve im log-log-Raum ist:

$$\frac{d(\ln Occ)}{d(\ln C)} = 1-Occ$$

- Bei H1 (Occ=20 %): Steigung ≈ 0,80
- Bei S1R (Occ≈1 %): Steigung ≈ 0,99 (**praktisch linear proportional zu C**)

Konkret bei Dosishalbierung (C→C/2):
- H1-Occupancy: 20 % → 11,1 % (relative Reduktion ~44 %)
- S1R-Occupancy: ~1 % → ~0,5 % (relative Reduktion ~50 %)

**Beide Targets fallen bei Dosisreduktion nahezu parallel** – S1R sogar geringfügig *stärker* relativ, weil es weiter von der Sättigung entfernt ist. Es gibt bei diesen Kd-Werten **keinen Dosisbereich, in dem H1-Occupancy überproportional stärker sinkt als S1R-Occupancy.** Eine Selektivitätslücke via Dosistitration entsteht erst, wenn die Kd-Werte um ≥2–3 Zehnerpotenzen auseinanderliegen (dann kann man im Konzentrationsfenster zwischen den beiden Sättigungskurven „surfen"). Mit nur Faktor 4–15 zwischen H1- und S1R-Kd ist dieses Fenster nicht vorhanden.

## 5. Fazit

1. **α2 und NMDA sind aus Potenzgründen auszuschließen** – exakt dieselbe quantitative Logik wie beim Na⁺-Kanal (Ki bzw. Ki_open 3–5 Zehnerpotenzen über C_frei, auch Use-Dependence beim NMDA-Blocker hebt den Ceiling nicht ausreichend an).
2. **S1R ist der einzig quantitativ ernstzunehmende verbleibende Kandidat**, weil seine Affinität nah genug an H1 liegt, um bei 12,5 mg überhaupt eine (wenn auch niedrige, ~0,5–1,7 %) Occupancy zu erzeugen – plus einem literaturgestützten, aktivitätsabhängigen Translokationsmechanismus, der (im Unterschied zum Na⁺-Kanal) eine echte Salven-Selektivität *unabhängig von der Gleichgewichts-Kd* erzeugen könnte.
3. **Aber**: Genau weil H1 und S1R so nah beieinanderliegen, ist **Dosisreduktion als Strategie zur Trennung von unerwünschtem (H1) und erwünschtem (S1R) Effekt untauglich** – beide Occupancies skalieren im niedrigen Occupancy-Bereich nahezu linear und parallel mit der freien Konzentration. Eine Dosisreduktion, die die H1-Last spürbar senkt, senkt die S1R-Belegung mindestens im gleichen, eher stärkeren relativen Ausmaß.
4. **Konsequenz für Ihre Zielsetzung**: Wenn der Salven-limitierende Effekt tatsächlich S1R-vermittelt ist, lässt er sich mit DPH selbst nicht dosis-selektiv von der H1-Wirkung trennen. Das würde einen Wechsel auf eine chemisch andere Substanz mit echtem S1R:H1-Selektivitätsverhältnis (>100–1000×) erfordern – nicht eine Titration von DPH.
