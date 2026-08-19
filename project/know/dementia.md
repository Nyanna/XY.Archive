Ich glaube mich zu erinnern gelesen zu haben das der Einsatz von Diphenhydramin, Implikationen auf Alzheimer oder Demenzerkrankungen hat?
SystemInit:  id=46b3aa31-cb72-48c0-9ea7-6c8bbfec9a9a, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
Control Request:
```yaml
id: ec2b3273-598a-4a0e-93a5-92b152311c3b
toolName: openalex-search
arguments:
  query: diphenhydramine anticholinergic dementia risk
  reason: Suche nach wissenschaftlichen Studien zum Zusammenhang zwischen Diphenhydramin und Demenz/Alzheimer-Risiko
  fields: core
  limit: 15
```
/answer ec2b3273-598a-4a0e-93a5-92b152311c3b allow
ReasoningToken: 41
Control Request:
```yaml
id: 2ca8e90b-a9f5-4b33-97f5-e2ee44026bd1
result:
  content:
  - type: text
    text: "Cannot reach OpenAlex (https://api.openalex.org/works?search=diphenhydramine+anticholinergic+dementia+risk&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Clanguage%2Cprimary_location%2Copen_access%2Ccited_by_count%2Cprimary_topic%2Crelevance_score&page=1&per-page=15&mailto=openalex%40xyan.icu&api_key=%2A%2A%2A): The read operation timed out"
  isError: true
```
/answer 2ca8e90b-a9f5-4b33-97f5-e2ee44026bd1 allow
Control Request:
```yaml
id: 260cac8f-4cc1-45ad-87c3-ba9970ca2ed6
toolName: web-search-exa
arguments:
  query: Diphenhydramine anticholinergic dementia risk study
  reason: Aktuelle Übersichtsartikel und Erklärungen zum Zusammenhang zwischen Diphenhydramin und Demenzrisiko finden
  numResults: 8
```
/answer 260cac8f-4cc1-45ad-87c3-ba9970ca2ed6 allow
Control Request:
```yaml
id: b1bb6f9d-f718-484c-87bb-3bc7fa32587a
result:
  structuredContent:
    content: |-
      Title: Cognitive and Other Adverse Effects of Diphenhydramine Use in Hospitalized Older Patients
      URL: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/649062
      Published: N/A
      Author: N/A
      Highlights:
      BackgroundDiphenhydramine hydrochloride is a commonly prescribed medicine in hospitalized patients, but its adverse effects on older patients remain unclear.MethodsWe enrolled 426 hospitalized medical patients aged 70 years or older in a prospective cohort study in a university hospital. Measurements included baseline and daily assessments including Mini-Mental State Examination scores, Confusion Assessment Method ratings, direct observations for medical devices (urinary catheter or physical restraints), and blinded medical record extractions for diphenhydramine use.ResultsOf the 426 patients, 114 (27%) received diphenhydramine during hospitalization and shared similar baseline characteristics including age, sex, delirium risk, and Mini-Mental State Examination scores compared with nonexposed patients. The diphenhydramine-exposed group was at an increased risk for any delirium symptoms (relative risk [RR], 1.7; 95% confidence interval [CI], 1.3-2.3) and for individual delirium symptoms, including inattention (RR, 3.0; 95% CI, 1.5-5.9), disorganized speech (RR, 5.5; 95% CI, 1.0-29.8), and altered consciousness (RR, 3.1; 95% CI, 1.6-6.1). Exposed patients also had increased risk for urinary catheter placement (RR, 2.5; 95% CI, 1.0-6.0) and longer median length of stay (7 vs 6 days;P= .009). A dose-response relationship was demonstrated for most adverse outcomes. Overall, 24% of diphenhydramine doses were administered inappropriately.ConclusionsDiphenhydramine administration in older hospitalized patients is associated with an increased risk of cognitive decline and other adverse effects with a dose-response relationship. Careful review of its use is necessary in this vulnerable population." Cognitive and Other Adverse Effects of Diphenhydramine Use in Hospitalized Older Patients | Dementia and Cognitive Impairment | JAMA Internal Medicine | JAMA Network
      ...
      Results Of the 426 patients, 114 (27%) received diphenhydramine during hospitalization and shared similar baseline characteristics including age, sex, delirium risk, and Mini-Mental State Examination scores compared with nonexposed patients. The diphenhydramine-exposed group was at an increased risk for any delirium symptoms (relative risk [RR], 1.7; 95% confidence interval [CI], 1.3-2.3) and for individual delirium symptoms, including inattention (RR, 3.0; 95% CI, 1.5-5.9), disorganized speech (RR, 5.5; 95% CI, 1.0-29.8), and altered consciousness (RR, 3.1; 95% CI, 1.6-6.1). Exposed patients also had increased risk for urinary catheter placement (RR, 2.5; 95% CI, 1.0-6.0) and longer median length of stay (7 vs 6 days; P = .009). A dose-response relationship was demonstrated for most adverse outcomes. Overall, 24% of diphenhydramine doses were administered inappropriately.
      ...
      The use of medications with anticholinergic effects in particular leads to important problems in older patients.9 Overall, these medications are associated with delirium more commonly than any other drug class.10 Other potential adverse effects include orthostasis, central nervous system depression, paradoxical excitement, visual disturbances, tachycardia, dry mouth, urinary retention, and constipation.11,12 Even mild disturbances in these cholinergic pathways can initiate a range of adverse effects that decrease an older patient's independence in functioning and ability to withstand the stressors of inpatient hospitalization.
      ...
      The current data about the effect of anticholinergic medications on cognitive function in the elderly are conflicting. Three prospective studies14-16 have shown no association between the use of anticholinergic drugs and delirium, while a prospective study of elderly patients treated for femoral neck fractures showed that anticholinergic drugs were a contributing factor for acute states of confusion.17 Small studies of older patients given diphenhydramine specifically have reported results ranging from a lack of sedative and cognitive effects (using visual analog scales, reaction times, verbal recall, and digit-symbol substitution)18 to some degree of cognitive impairment (using verbal memory, visuospatial cognition, and Trails B testing)19 to delirium in patients with mild dementia.20 Thus, further study is needed to clarify the effects of diphenhydramine use on cognitive outcomes as well as other adverse effects during hospitalization.
      ...
      The specific aims of our present study are to examine the rate of diphenhydramine use in a large prospective cohort of elderly hospitalized patients; to evaluate potential adverse outcomes (eg, cognitive, behavioral, and other anticholinergic effects) associated with diphenhydramine use; and to describe current diphenhydramine use in the study cohort. Our underlying hypothesis is that diphenhydramine use results in an increased risk of adverse outcomes and that this risk will increase with the dose of diphenhydramine received.
      ...
      as a large referral base. All patients were admitted to the general medical service in a non–intensive care setting between March 1995 and February 1998. Patients were required to be 70 years or older
      ...
      The presence of delirium symptoms was much more likely to occur in the diphenhydramine-exposed group than the nonexposed group (Table 2). There was a 70% increased risk of cognitive decline in the diphenhydramine-exposed group (42% of those exposed vs 24% of those not exposed [RR, 1.7; 95% CI, 1.3-2.3; P<.05]). In addition, the diphenhydramine-exposed group was at significantly increased risk for inattention (RR, 3.0), disorganized speech (RR, 5.5), altered level of consciousness (RR, 3.1), abnormal psychomotor activity (RR, 2.3), altered sleep-wake cycle (RR, 2.0), and behavioral disturbance (RR, 5.6). New urinary catheter use occurred in 8% of the diphenhydramine-exposed group compared with 3% in the nonexposed group (RR, 2.5; 95% CI, 1.0-6.0). Length of stay was significantly longer on average in the diphenhydramine-exposed group (median of 7 vs 6 days; P = .009).
      ...
      In a multiple logistic regression model involving 423 observations (3 excluded for missing variables), the adjusted odds ratio for the risk of cognitive decline in the diphenhydramine-exposed group was 2.3 (95% CI, 1.4-3.6). This result controlled for age, sex, and baseline delirium risk, none of which were independently statistically significant. These multivariable results confirm the bivariate analyses reported above.
      ...
      This study shows that diphenhydramine use in hospitalized elderly patients carries substantial risk. Diphenhydramine use was associated with significant risk of cognitive decline, behavioral disturbance, and urinary catheter placement, of which the latter 2 may be markers of the anticholinergic effects of delirium resulting in agitation and urinary retention. In addition, a dose-response relationship was demonstrated for many of these adverse outcomes, and length of stay was significantly longer. Finally, diphenhydramine was inappropriately administered to 24% of patients. This study represents, to our knowledge, the largest and most detailed prospective cohort study in older patients that examines cognitive and other adverse outcomes following diphenhydramine use.
      ...
      In summary, this study suggests that diphenhydramine use in the hospitalized older patient contributes most notably to cognitive decline, behavioral disturbance, and initiation of bladder catheterization. Based on these data, we recommend that diphenhydramine be used with caution in elderly patients and not, for instance, administered as a routine sleep aid. Also, the practice of administering diphenhydramine prophylactically prior to blood transfusions in the absence of previous transfusion reaction has no documented benefit and should be curtailed. Increased attention to the potential for serious adverse effects in the elderly should lead to modification of common prescribing patterns and heightened awareness concerning the limited use of diphenhydramine in geriatric patients.

      ---

      Title: Cumulative use of strong anticholinergics and incident dementia: a prospective cohort study - PubMed
      URL: https://pubmed.ncbi.nlm.nih.gov/25621434/
      Published: N/A
      Author: N/A
      Highlights:
      Cumulative use of strong anticholinergics and incident dementia: a prospective cohort study
      ...
      Importance: Many medications have anticholinergic effects. In general, anticholinergic-induced cognitive impairment is considered reversible on discontinuation of anticholinergic therapy. However, a few studies suggest that anticholinergics may be associated with an increased risk for dementia.
      ...
      Objective: To examine whether cumulative anticholinergic use is associated with a higher risk for incident dementia.
      ...
      Design, setting, and participants: Prospective population-based cohort study using data from the Adult Changes in Thought study in Group Health, an integrated health care delivery system in Seattle, Washington. We included 3434 participants 65 years or older with no dementia at study entry. Initial recruitment occurred from 1994 through 1996 and from 2000 through 2003. Beginning in 2004, continuous replacement for deaths occurred. All participants were followed up every 2 years. Data through September 30, 2012, were included in these analyses.
      ...
      Exposures: Computerized pharmacy dispensing data were used to ascertain cumulative anticholinergic exposure, which was defined as the total standardized daily doses (TSDDs) dispensed in the past 10 years. The most recent 12 months of use was excluded to avoid use related to prodromal symptoms. Cumulative exposure was updated as participants were followed up over time.
      ...
      Main outcomes and measures: Incident dementia and Alzheimer disease using standard diagnostic criteria. Statistical analysis used Cox proportional hazards regression models adjusted for demographic characteristics, health behaviors, and health status, including comorbidities.
      ...
      Results: The most common anticholinergic classes used were tricyclic antidepressants, first-generation antihistamines, and bladder antimuscarinics. During a mean follow-up of 7.3 years, 797 participants (23.2%) developed dementia (637 of these [79.9%] developed Alzheimer disease). A 10-year cumulative dose-response relationship was observed for dementia and Alzheimer disease (test for trend, P < .001). For dementia, adjusted hazard ratios for cumulative anticholinergic use compared with nonuse were 0.92 (95% CI, 0.74-1.16) for TSDDs of 1 to 90; 1.19 (95% CI, 0.94-1.51) for TSDDs of 91 to 365; 1.23 (95% CI, 0.94-1.62) for TSDDs of 366 to 1095; and 1.54 (95% CI, 1.21-1.96) for TSDDs greater than 1095. A similar pattern of results was noted for Alzheimer disease. Results were robust in secondary, sensitivity, and post hoc analyses.
      ...
      Conclusions and relevance: Higher cumulative anticholinergic use is associated with an increased risk for dementia. Efforts to increase awareness among health care professionals and older adults about this potential medication-related risk are important to minimize anticholinergic use over time.

      ---

      Title: Cumulative Use of Strong Anticholinergics and Incident ...
      URL: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2091745
      Published: N/A
      Author: N/A
      Highlights:
      ImportanceMany medications have anticholinergic effects. In general, anticholinergic-induced cognitive impairment is considered reversible on discontinuation of anticholinergic therapy. However, a few studies suggest that anticholinergics may be associated with an increased risk for dementia.ObjectiveTo examine whether cumulative anticholinergic use is associated with a higher risk for incident dementia.Design, Setting, and ParticipantsProspective population-based cohort study using data from the Adult Changes in Thought study in Group Health, an integrated health care delivery system in Seattle, Washington. We included 3434 participants 65 years or older with no dementia at study entry. Initial recruitment occurred from 1994 through 1996 and from 2000 through 2003. Beginning in 2004, continuous replacement for deaths occurred. All participants were followed up every 2 years. Data through September 30, 2012, were included in these analyses.ExposuresComputerized pharmacy dispensing data were used to ascertain cumulative anticholinergic exposure, which was defined as the total standardized daily doses (TSDDs) dispensed in the past 10 years. The most recent 12 months of use was excluded to avoid use related to prodromal symptoms. Cumulative exposure was updated as participants were followed up over time.Main Outcomes and MeasuresIncident dementia and Alzheimer disease using standard diagnostic criteria. Statistical analysis used Cox proportional hazards regression models adjusted for demographic characteristics, health behaviors, and health status, including comorbidities.ResultsThe most common anticholinergic classes used were tricyclic antidepressants, first-generation antihistamines, and bladder antimuscarinics. During a mean follow-up of 7.3 years, 797 participants (23.2%) developed dementia (637 of these [79.9%] developed Alzheimer disease). A 10-year cumulative dose-response relationship was observed for dementia and Alzheimer disease (test for trend,P < .001). For dementia, adjusted hazard ratios for cumulative anticholinergic use compared with nonuse were 0.92 (95% CI, 0.74-1.16) for TSDDs of 1 to 90; 1.19 (95% CI, 0.94-1.51) for TSDDs of 91 to 365; 1.23 (95% CI, 0.94-1.62) for TSDDs of 366 to 1095; and 1.54 (95% CI, 1.21-1.96) for TSDDs greater than 1095. A similar pattern of results was noted for Alzheimer disease. Results were robust in secondary, sensitivity, and post hoc analyses.Conclusions and RelevanceHigher cumulative anticholinergic use is associated with an increased risk for dementia. Efforts to increase awareness among health care professionals and older adults about this potential medication-related risk are important to minimize anticholinergic use over time." Cumulative Use of Strong Anticholinergics and Incident Dementia: A Prospective Cohort Study | Dementia and Cognitive Impairment | JAMA Internal Medicine | JAMA Network
      ...
      Importance Many medications have anticholinergic effects. In general, anticholinergic-induced cognitive impairment is considered reversible on discontinuation of anticholinergic therapy. However, a few studies suggest that anticholinergics may be associated with an increased risk for dementia.
      ...
      Objective To examine whether cumulative anticholinergic use is associated with a higher risk for incident dementia.
      ...
      Results The most common anticholinergic classes used were tricyclic antidepressants, first-generation antihistamines, and bladder antimuscarinics. During a mean follow-up of 7.3 years, 797 participants (23.2%) developed dementia (637 of these [79.9%] developed Alzheimer disease). A 10-year cumulative dose-response relationship was observed for dementia and Alzheimer disease (test for trend, P < .001). For dementia, adjusted hazard ratios for cumulative anticholinergic use compared with nonuse were 0.92 (95% CI, 0.74-1.16) for TSDDs of 1 to 90; 1.19 (95% CI, 0.94-1.51) for TSDDs of 91 to 365; 1.23 (95% CI, 0.94-1.62) for TSDDs of 366 to 1095; and 1.54 (95% CI, 1.21-1.96) for TSDDs greater than 1095. A similar pattern of results was noted for Alzheimer disease. Results were robust in secondary, sensitivity, and post hoc analyses.
      ...
      Conclusions and Relevance Higher cumulative anticholinergic use is associated with an increased risk for dementia. Efforts to increase awareness among health care professionals and older adults about this potential medication-related risk are important to minimize anticholinergic use over time.
      ...
      The objective of this study was to examine the association between 10-year cumulative anticholinergic use and the risk for dementia. We hypothesized that greater cumulative use of anticholinergics would be associated with increased risk.
      ...
      , 1 to 90, 91 to 365, 366 to 1095, or greater than 1095 (ie, >3 years), with cut points based on clinical interpretability and the exposure distribution observed in our sample. As an example, individuals would reach the heaviest level of exposure if they took any of the following medications daily for more than 3 years: oxybutynin chloride, 5 mg; chlorpheniramine maleate, 4 mg; olanzapine, 2.5 mg; meclizine hydrochloride, 25 mg; or
      ...
      During a mean (SD) follow-up of 7.3 (4.8) years, 797 participants (23.2%) developed dementia, of whom 637 (79.9%) were considered to have possible or probable AD. Table 3 shows unadjusted and adjusted risk estimates for dementia and AD associated with cumulative anticholinergic use. A 10-year cumulative dose-response relationship was observed for dementia and AD (test for trend, P < .001). In particular, participants in the highest exposure category (TSDD >1095) had a statistically significant increased risk for dementia (adjusted HR, 1.54 [95% CI, 1.21-1.96]) or AD (adjusted HR, 1.63 [95% CI, 1.24-2.14]) compared with those with no use. Participants in the next highest exposure level (TSDD, 366-1095) had a slightly elevated risk for dementia (adjusted HR, 1.23 [95% CI, 0.94-1.62]) and AD (adjusted HR, 1.30 [95% CI, 0.96-1.76]) compared with no use.
      ...
      In this population-based, longitudinal study of persons 65 years or older, we found that higher cumulative use of anticholinergics is associated with an increased risk for all-cause dementia and AD. Our findings were robust in secondary and sensitivity analyses, including those performed to take into account the potential use of anticholinergics (eg, antidepressants) for prodromal symptoms of dementia. The increased risk for dementia that remained consistent across anticholinergic subclasses is worth noting, with an increased risk found for people with high use of anticholinergics other than antidepressants, such as first-generation antihistamines and bladder antimuscarinics. Thus, our findings do not appear to be explained by protopathic bias due to treatment of depression, a condition commonly seen in patients with early undiagnosed dementia.
      ...
      An increased risk for dementia was seen in people with higher use of anticholinergics. Our findings suggest that a person taking an anticholinergic, such as oxybutynin chloride, 5 mg/d, or doxepin hydrochloride, 10 mg/d, for more than 3 years would have a greater risk for dementia. Prescribers should be aware of this potential association when considering anticholinergics for their older patients and should consider alternatives when possible. For conditions with no therapeutic alternatives, prescribers should use the lowest effective dose and discontinue therapy if ineffective. These findings also have public health implications for the education of older adults about potential safety risks because some anticholinergics are available as over-the-counter products. Given the devastating consequences of dementia, informing older adults about this potentially modifiable risk would allow them to choose alternative products and collaborate with their health care professionals to minimize overall anticholinergic use. Additional studies are needed to confirm these findings and to understand the underlying mechanisms.

      ---

      Title: Anticholinergic drugs and the risk of dementia: A systematic review and meta-analysis - PubMed
      URL: https://pubmed.ncbi.nlm.nih.gov/33933505/
      Published: N/A
      Author: N/A
      Highlights:
      Anticholinergic drugs and the risk of dementia: A systematic review and meta-analysis - PubMed
      ...
      Dementia is one of the greatest global challenges for public health; however, the relationship between anticholinergic drugs and dementia remains unclear. The aim of the present study was to perform a systematic review and meta-analysis of the predictive roles of anticholinergic drugs in dementia risk. After pooling fourteen longitudinal and case-control studies with a total of 1,564,181 subjects, anticholinergic drug use was associated with an increased risk of all-cause dementia and Alzheimer's disease. Both low and high anticholinergic drug burdens were associated with dementia. Moreover, there was a dose-dependent relationship between anticholinergic drugs and risk of dementia. With respect to the categories of anticholinergic drugs, antiparkinson, urological drugs, and antidepressants increased the risk for dementia; however, cardiovascular and gastrointestinal drugs played potentially protective roles. These findings underscore the importance of anticholinergic drugs as a potential modifiable risk factor for dementia and provide treatment priorities to optimize dementia prevention.
      ...
      analysis; Risk; Systematic review.

      ---

      Title: Long-term use of diphenhydramine - PMC - NIH
      URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC4592307/
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

      Title: Anticholinergic Drug Exposure and the Risk of Dementia :  A Nested Case-Control Study
      URL: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2736353
      Published: N/A
      Author: N/A
      Highlights:
      in 58 769 patients with a diagnosis of dementia and 225 574 controls 55 years or older matched by age, sex, general practice, and calendar time. Information on prescriptions for 56 drugs with strong anticholinergic properties was used to calculate measures of cumulative anticholinergic drug exposure. Data were analyzed from May 2016 to June 2018.ExposuresThe primary exposure was the total standardized daily doses (TSDDs) of anticholinergic drugs prescribed in the 1 to 11 years prior to the date of diagnosis of dementia or equivalent date in matched controls (index date).Main Outcomes and MeasuresOdds ratios (ORs) for dementia associated with cumulative exposure to anticholinergic drugs, adjusted for confounding variables.ResultsOf the entire study population (284 343 case patients and matched controls), 179 365 (63.1%) were women, and the mean (SD) age of the entire population was 82.2 (6.8) years. The adjusted OR for dementia increased from 1.06 (95% CI, 1.03-1.09) in the lowest overall anticholinergic exposure category (total exposure of 1-90 TSDDs) to 1.49 (95% CI, 1.44-1.54) in the highest category (>1095 TSDDs), compared with no anticholinergic drug prescriptions in the 1 to 11 years before the index date. There were significant increases in dementia risk for the anticholinergic antidepressants (adjusted OR [AOR], 1.29; 95% CI, 1.24-1.34), antiparkinson drugs (AOR, 1.52; 95% CI, 1.16-2.00), antipsychotics (AOR, 1.70; 95% CI, 1.53-1.90), bladder antimuscarinic drugs (AOR, 1.65; 95% CI, 1.56-1.75), and antiepileptic drugs (AOR, 1.39; 95% CI, 1.22-1.57) all for more than 1095 TSDDs. Results were similar when exposures were restricted to exposure windows of 3 to 13 years (AOR, 1.46; 95% CI, 1.41-1.52) and 5 to 20 years (AOR, 1.44; 95% CI, 1.32-1.57) before the index date for more than 1095 TSDDs. Associations were stronger in cases diagnosed before the age of 80 years.
      ...
      Findings In this nested case-control study of 58 769 patients with a diagnosis of dementia and 225 574 matched controls, there were statistically significant associations of dementia risk with exposure to anticholinergic antidepressants, antiparkinson drugs, antipsychotic drugs, bladder antimuscarinics, and antiepileptic drugs after adjusting for confounding variables.
      ...
      Design, Setting, and Participants This nested case-control study took place in general practices in England that contributed to the QResearch primary care database. The study evaluated whether exposure to anticholinergic drugs was associated with dementia risk in 58 769 patients with a diagnosis of dementia and 225 574 controls 55 years or older matched by age, sex, general practice, and calendar time. Information on prescriptions for 56 drugs with strong anticholinergic properties was used to calculate measures of cumulative anticholinergic drug exposure. Data were analyzed from May 2016 to June 2018.
      ...
      Results Of the entire study population (284 343 case patients and matched controls), 179 365 (63.1%) were women, and the mean (SD) age of the entire population was 82.2 (6.8) years. The adjusted OR for dementia increased from 1.06 (95% CI, 1.03-1.09) in the lowest overall anticholinergic exposure category (total exposure of 1-90 TSDDs) to 1.49 (95% CI, 1.44-1.54) in the highest category (>1095 TSDDs), compared with no anticholinergic drug prescriptions in the 1 to 11 years before the index date. There were significant increases in dementia risk for the anticholinergic antidepressants (adjusted OR [AOR], 1.29; 95% CI, 1.24-1.34), antiparkinson drugs (AOR, 1.52; 95% CI, 1.16-2.00), antipsychotics (AOR, 1.70; 95% CI, 1.53-1.90), bladder antimuscarinic drugs (AOR, 1.65; 95% CI, 1.56-1.75), and antiepileptic drugs (AOR, 1.39; 95% CI, 1.22-1.57) all for more than 1095 TSDDs. Results were similar when exposures were restricted to exposure windows of 3 to 13 years (AOR, 1.46; 95% CI, 1.41-1.52) and 5 to 20 years (AOR, 1.44; 95% CI, 1.32-1.57) before the index date for more than 1095 TSDDs. Associations were stronger in cases diagnosed before the age of 80 years. The population-attributable fraction associated with total anticholinergic drug exposure during the 1 to 11 years before diagnosis was 10.3%.
      ...
      The AOR associated with total cumulative anticholinergic exposure in the 1 to 11 years before the index date increased from 1.06 (95% CI, 1.03-1.09) for 1 to 90 TSDDs to 1.49 (95% CI, 1.44-1.54) for more than 1095 TSDDs, compared with nonuse (Table 4). Results were similar but with slightly lower ORs when restricted to the 3 to 13 and 5 to 20 years before the index date; for example, for the 5 to 20 years before the index date the AOR was 1.44 (95% CI, 1.32-1.57) for more than 1095 TSDDs (Table 4).
      ...
      Quiz Ref IDAmong specific types of anticholinergic drugs there were significant increases in risk associated with use of antidepressants, antiparkinson drugs, antipsychotics, bladder antimuscarinics, and antiepileptic drugs (Table 5). Adjusted odds ratios in the highest exposure category (>1095 TSDDs) were 1.29 (95% CI, 1.24-1.34) for antidepressants, 1.52 (95% CI, 1.16-2.00) for antiparkinson drugs, 1.70 (95% CI, 1.53-1.90) for antipsychotics, 1.65 (95% CI, 1.56-1.75) for bladder antimuscarinics, and 1.39 (95% CI, 1.22-1.57) for antiepileptic drugs, all compared with nonuse. For antivertigo/antiemetic drugs, as detailed in Table 5, there was a significantly increased risk associated with 366 to 1095 TSDDs, but not for the highest exposure category. There were no significant increases in risk associated with antihistamines, skeletal muscle relaxants, gastrointestinal antispasmodics, antiarrhythmics, or antimuscarinic bronchodilators, although the numbers of patients exposed were small for skeletal muscle relaxants and antiarrhythmics. Patterns of risk were similar in the 3- to 13- and 5- to 20-year exposure windows (eTable 6 in the Supplement), except for antipsychotic drug exposure in the 5- to 20-year window, where there were no statistically significant increases in risk; the AOR for more than 1095 TSDDs was 1.23 (95% CI, 0.93-1.62). For some drug types, numbers were too small to allow analysis for the 5 to 20 years before the index date (eTable 7 in the Supplement).
      ...
      The population-attributable fraction associated with total anticholinergic drug exposure during the 1 to 11 years before diagnosis was 10.3%. For the 3 to 13 years before diagnosis, it was 9.0%, and it was 9.7% for the 5 to 20 years before diagnosis.
      ...
      This large, nested case-control study found an increased risk of dementia associated with anticholinergic medication use. Associations were strongest for the anticholinergic antidepressants, bladder antimuscarinics, antipsychotics, and antiepileptic drugs. Quiz Ref IDAssociations were also stronger in cases diagnosed before the age of 80 years and in cases diagnosed with vascular dementia rather than with Alzheimer disease. There were no significantly increased risks for antihistamines, gastrointestinal antispasmodics, antimuscarinic bronchodilators, antiarrhythmics, or skeletal muscle relaxants, although the numbers of patients prescribed skeletal muscle relaxants and antiarrhythmic drugs were small, giving imprecise estimates.
      ...
      The present study adds further evidence of potential risks associated with strong anticholinergic drugs, particularly those that are antidepressants, bladder antimuscarinic drugs, antiparkinson drugs, and epilepsy drugs. Adverse effects should be considered alongside benefits when these drugs are prescribed, and alternative treatments should be considered where possible, such as other types of antidepressant or nonpharmacological treatments for depression, alternative antiparkinsonian drugs, and bladder training or mirabegron for overactive bladders.42,43 We found greater increases in risk associated with people diagnosed with dementia before the age of 80, which indicates that anticholinergic drugs should be prescribed with caution in middle-aged and older people.

      ---

      Title: Drugs With Anticholinergic Properties, Cognitive Decline, and Dementia in an Elderly General Population :  The 3-City Study
      URL: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/224695
      Published: N/A
      Author: N/A
      Highlights:
      Background Despite the high intake of medications with anticholinergic properties by community-dwelling elderly persons, the effects on cognitive decline and dementia have rarely been evaluated.
      ...
      Methods Participants were 4128 women and 2784 men 65 years or older from a population-based cohort recruited from 3 French cities. Cognitive performance, clinical diagnosis of dementia, and anticholinergic use were evaluated at baseline and 2 and 4 years later.
      ...
      Results A total of 7.5% of the participants reported anticholinergic drug use at baseline. Multivariate-adjusted logistic regression indicated that women reporting use of anticholinergic drugs at baseline showed greater decline over 4 years in verbal fluency scores (odds ratio [OR], 1.41; 95% confidence interval [CI], 1.11-1.79) and in global cognitive functioning (OR, 1.22; 95% CI, 0.96-1.55) than women not using anticholinergic drugs. In men, an association was found with decline in visual memory (OR, 1.63; 95% CI, 1.08-2.47) and to a lesser extent in executive function (OR, 1.47; 95% CI, 0.89-2.44). Notable interactions were observed in women between anticholinergic use and age, apolipoprotein E, or hormone therapy. A 1.4- to 2-fold higher risk of cognitive decline was observed for those who continuously used anticholinergic drugs but not for those who had discontinued use. The risk of incident dementia over the 4-year follow-up period was also increased in continuous users (hazard ratio [HR], 1.65; 95% CI, 1.00-2.73) but not in those who discontinued the use of anticholinergic drugs (HR, 1.28; 95% CI, 0.59-2.76).
      ...
      Conclusions Elderly people taking anticholinergic drugs were at increased risk for cognitive decline and dementia. Discontinuing anticholinergic treatment was associated with a decreased risk. Physicians should carefully consider prescription of anticholinergic drugs in elderly people, especially in the very elderly and in persons at high genetic risk for cognitive disorder.
      ...
      Thus, although there is accumulating evidence to suggest that anticholinergics may increase the risk of cognitive decline and dementia, this hypothesis remains to be tested within a large prospective study that is able to take into account multiple independent and interactive causes of cognitive decline. To our knowledge, the possible reversible effect on cognitive functioning of stopping anticholinergic treatment has also never been evaluated. Our aim was to examine the relationship over time between anticholinergic use and cognitive decline and onset of dementia in community-dwelling elderly persons, taking into account sex and genetic vulnerability.
      ...
      Among the 7123 participants included in the analysis concerning dementia outcome, there were 221 newly diagnosed cases during follow-up, of whom 143 patients had Alzheimer disease. In the subsample from which intermittent users were excluded, a multiadjusted delayed-entry Cox model showed an increased risk for incident dementia or Alzheimer disease for persons who had used anticholinergic drugs continuously (hazard ratio [HR], 1.65; 95% CI, 1.00-2.73; P = .05; and HR, 1.94; 95% CI, 1.01-3.72; P = .05, respectively) but not for those who had discontinued anticholinergic treatment after the inclusion (Table 4).
      ...
      In this large prospective study, 7.5% of these community-dwelling elderly persons reported taking anticholinergics. Our results indicate an increased risk in cognitive decline and dementia, which remained significant after adjustment for the other multiple possible codeterminants of cognitive decline (see Table 2 and Table 4 for P values). It is worth noting that similar results were obtained in the unadjusted model (model 1) and in the model that adjusted for the diseases associated with anticholinergic treatment (model 2). This suggests that the anticholinergic drugs themselves rather than the underlying burden of illness is the likely cause of the cognitive decline. Further supporting a causative effect of the anticholinergic medications, we found that the cognitive decline seemed reversible after
      ...
      could at least partly account for the
      ...
      We observed an important association between anticholinergic use at baseline and the risk of developing dementia at 4-year follow-up. In a previous study10 conducted with an independent cohort, we found anticholinergic use to be a risk factor for MCI, but the numbers of patients with dementia were insufficient to determine the risk of dementia incidence. In the present study, we observed that chronic anticholinergic users were at higher risk of incident dementia compared with nonusers or persons having discontinued intake at the beginning of the follow-up. Although this finding has not been previously reported to our knowledge, it agrees with the study by Perry et al40 on autopsied patients with Parkinson disease treated with anticholinergics; Alzheimer-type disease was observed in patients who had been treated for more than 2 years compared with those treated with short-term anticholinergics or untreated patients.
      ...
      In conclusion, findings from this study suggest that the use of medication with anticholinergic effects was associated with an increased risk of cognitive dysfunction and dementia in elderly persons. Discontinuing anticholinergic treatment was associated with a decreased risk. Physicians should monitor current anticholinergic drug use in elderly patients and seek pharmacological alternatives before considering administration of neuroprotective medications to persons with MCI, thus escalating a prescription cascade involving cholinesterase inhibitors and anticholinergic drugs.10,44,45 This is especially important considering that long-term concomitant therapy with anticholinergics may be associated with clinically significant deleterious effects on acetylcholinesterase therapy and may have adverse effects on the clinical course of Alzheimer disease.46,47

      ---

      Title: Anticholinergic drugs and risk of dementia: case-control study
      URL: https://www.bmj.com/content/361/bmj.k1315
      Published: N/A
      Author: N/A
      Highlights:
      **Objectives**To estimate the association between the duration and level of exposure to different classes of anticholinergic drugs and subsequent incident dementia.
      ...
      **Design**Case-control study.
      ...
      **Participants**40 770 patients aged 65-99 with a diagnosis of dementia between April 2006 and July 2015, and 283 933 controls without dementia.
      ...
      **Interventions**Daily defined doses of anticholinergic drugs coded using the Anticholinergic Cognitive Burden (ACB) scale, in total and grouped by subclass, prescribed 4-20 years before a diagnosis of dementia.
      ...
      **Results**14 453 (35%) cases and 86 403 (30%) controls were prescribed at least one anticholinergic drug with an ACB score of 3 (definite anticholinergic activity) during the exposure period. The adjusted odds ratio for any anticholinergic drug with an ACB score of 3 was 1.11 (95% confidence interval 1.08 to 1.14). Dementia was associated with an increasing average ACB score. When considered by drug class, gastrointestinal drugs with an ACB score of 3 were not distinctively linked to dementia. The risk of dementia increased with greater exposure for antidepressant, urological, and antiparkinson drugs with an ACB score of 3. This result was also observed for exposure 15-20 years before a diagnosis.
      ...
      **Conclusions**A robust association between some classes of anticholinergic drugs and future dementia incidence was observed. This could be caused by a class specific effect, or by drugs being used for very early symptoms of dementia. Future research should examine anticholinergic drug classes as opposed to anticholinergic effects intrinsically or summing scales for anticholinergic exposure.
      ...
      We present a nested case-control study using the UK’s Clinical Practice Research Datalink (CPRD), in which we select patients with a new diagnosis of dementia, and compare their prescriptions of anticholinergic drugs 4-20 years before a diagnosis of dementia with that of a matched group of control patients without dementia. We had three objectives. Firstly, to estimate the association between chronic anticholinergic drug use and future dementia incidence while controlling for potential confounders. Secondly, to explore whether any observed effect was specific to a particular drug class. Thirdly, to test how the association varied with the time to dementia incidence and amount of exposure within each class.
      ...
      [Table 2](#T2)shows that there was a positive and significant association between the prescription of any drug with an ACB score of 1, 2, or 3 and dementia with corresponding odds ratios of 1.10 (95% confidence interval 1.06 to 1.15), 1.10 (1.03 to 1.16), and 1.11 (1.08 to 1.14). These values were adjusted for covariates measured at the end of the DEP. A dose-response effect was evident for prescribed doses of drugs with an ACB score of 2 or 3. However, there was no dose-response effect for drugs with an ACB score of 1.[Table 2](#T2)shows that an odds ratio of approximately 1.1 was seen for those prescribed drugs with an ACB score of 1, regardless of the number prescribed, including those with less than 14 DDD exposure. The associations are attenuated from the crude rates when adjusting for drug use at the
      ...
      [Table 3](#T3)shows that, when analysed by class, there was a significant association between dementia incidence and any prescription of antidepressant, antiparkinson, or urological drugs with an ACB score of 3, but no association with antispasmodic, antipsychotic, antihistamine, or other drugs with an ACB score of 3. Prescriptions for drugs with an ACB score of 2 were relatively rare, and so results are imprecise in this group, but there is some evidence for an association between dementia incidence and prescription of antiparkinson drugs. We found positive associations for antidepressant drugs with an ACB score of 1 with an increased risk of dementia, but not with any other drugs with an ACB score of 1. Supplementary materials table 2 shows the associations between dementia incidence and the number of DDDs by drug class. These associations are consistent with the findings in[table 3](#T3), except that a tentative effect of antihistamines with an ACB score of 3 is seen for patients with more than 365 DDDs prescribed during the DEP. Use of gastrointestinal drugs with an ACB score of 1 or 3, and cardiovascular drugs with an ACB score of 1 was associated with a minor reduction in the risk of dementia.
      ...
      [Table 4](#T4)shows the effect of exposure in three different periods (4-10, 10-15, and 15-20 years) before the index date. Associations with prescriptions for drugs with an ACB score of 3 were consistent across the DEP. Associations with prescriptions for drugs with an ACB score of 1 and 2 were more apparent closer to the index date. In particular, the prescription of any drug with an ACB score of 3 15-20 years before a diagnosis of dementia was significantly associated with greater dementia incidence with an odds ratio of 1.17 (95% confidence interval 1.10 to 1.24) adjusted for covariates at the start of the DEP. Prescriptions at 15-20 years before a diagnosis of dementia for antidepressant and urological drugs with an ACB score of 3 remained consistently significantly associated with dementia incidence with odds ratios of 1.19 (1.10 to 1.29) and 1.27 (1.09 to 1.48) respectively. However, for antidepressants with an ACB score of 1, the association with dementia increased for prescriptions given in periods closer to a diagnosis of dementia. Similarly, the negative association between gastrointestinal drugs and dementia was not seen for exposures 15-20 years before the index date.
      ...
      In this case-control study of older adults in the UK, there was a noticeable association between increasing total anticholinergic burden over the previous 4-20 years and incident dementia diagnosis. However, this dose-response effect was not seen for cumulative use of drugs with an Anticholinergic Cognitive Burden (ACB) score of 1 (possibly anticholinergic), and was only evident for certain classes of anticholinergic drugs. Antidepressants (predominantly amitriptyline, dosulepin, and paroxetine) and urologicals (predominantly oxybutynin and tolterodine) with an ABC score of 3 (definitely anticholinergic) were consistently associated with incident dementia. These relations were seen even for exposures 15-20 years before the diagnosis of dementia, suggesting that reverse causation or confounding with early dementia symptoms are less likely explanations for the effect. Prescription of gastrointestinal drugs**w**ith an ACB score of 3 was not positively associated with dementia in any of our analyses. Other antidepressants (predominantly selective serotonin reuptake inhibitors) with an ACB score of 1 were associated with dementia, but that association was greater for prescriptions close to dementia incidence, suggesting that reverse causation could be a possible explanation for this observed association. Other drugs with an ACB score of 1 were not associated with increased dementia incidence.
      ...
      Many people use anticholinergic drugs at some point in their lives, and many are prescribed to manage chronic conditions leading to potentially long exposures. There are robust associations between levels of anticholinergic antidepressants, antiparkinsons, and urologicals and the risk of a diagnosis of dementia up to 20 years after exposure. Other anticholinergics appear not to be linked to the risk of dementia, and risks remain uncertain for other drugs. Clinicians should continue to be vigilant with respect to the use of anticholinergic drugs, and should consider the risk of long term cognitive effects, as well as short term effects, associated with specific drug classes when performing their risk-benefit analysis.
      ...
      * Antidepressant, urological, and antiparkinson drugs with definite anticholinergic activity are linked to future dementia incidence, with associations persisting up to 20 years after exposure
```
/answer b1bb6f9d-f718-484c-87bb-3bc7fa32587a allow
# Ja, Ihre Erinnerung ist richtig – hier der wissenschaftliche Hintergrund

Diphenhydramin (Wirkstoff z. B. in Vomex-Präparaten, manchen Einschlafhilfen und älteren Antihistaminika/H1-Blockern) hat tatsächlich **anticholinerge Eigenschaften**, und genau diese Klasse von Substanzen wird seit Jahren im Zusammenhang mit einem erhöhten Demenz- und Alzheimer-Risiko diskutiert.

## Was ist "anticholinerg" und warum ist das relevant?

Diphenhydramin blockiert Acetylcholin-Rezeptoren im Gehirn. Acetylcholin ist ein Botenstoff, der für Gedächtnis, Aufmerksamkeit und kognitive Funktionen zentral wichtig ist – genau das System, das bei Alzheimer ohnehin degeneriert (die meisten Alzheimer-Medikamente wie Donepezil wirken sogar in die *entgegengesetzte* Richtung, indem sie Acetylcholin-Abbau hemmen).

## Wichtigste Studienbefunde

**1. Gray et al. 2015 (JAMA Internal Medicine)** – die bekannteste Studie:
- Kohortenstudie mit 3.434 Personen ≥65 Jahre über ~7 Jahre
- Bei **kumulativ hoher** Anwendung starker Anticholinergika (>3 Jahre tägliche Standarddosis) war das Demenzrisiko um **54% erhöht** (HR 1,54) und das Alzheimer-Risiko um **63%** (HR 1,63)
- Es zeigte sich ein klarer **Dosis-Wirkungs-Zusammenhang**: je mehr/länger, desto höher das Risiko
- Häufigste Substanzklassen: trizyklische Antidepressiva, **Antihistaminika der 1. Generation** (dazu zählt Diphenhydramin) und Blasenmedikamente

**2. Richardson et al. 2018 (BMJ)** – Fall-Kontroll-Studie mit über 300.000 Personen:
- Bestätigte den Zusammenhang, allerdings war er bei **reinen Antihistaminika schwächer/inkonsistenter** ausgeprägt als bei anticholinergen Antidepressiva, Blasen- und Parkinson-Medikamenten
- Ein Effekt zeigte sich vor allem bei sehr hoher kumulativer Exposition (>365 Tagesdosen)

**3. Fox et al. – 3-City-Studie (Frankreich):**
- Kontinuierliche Anwender anticholinerger Medikamente hatten ein erhöhtes Demenzrisiko (HR 1,65)
- Wichtig: Bei **Absetzen** der Medikamente sank das Risiko wieder – ein Hinweis, dass der Effekt zumindest teilweise reversibel sein könnte

**4. Kurzzeiteffekte (JAMA Internal Medicine, ältere Krankenhauspatienten):**
- Auch akut zeigte Diphenhydramin bei über 70-Jährigen ein 70% erhöhtes Delir-Risiko und Konzentrations-/Bewusstseinsstörungen – dosisabhängig

## Einordnung – was heißt das konkret?

- Es geht primär um **regelmäßige, langfristige** Einnahme (Jahre), nicht um den gelegentlichen Gebrauch als Einschlafhilfe oder bei Reisekrankheit
- Der Zusammenhang ist **statistisch robust**, aber **Kausalität nicht zweifelsfrei bewiesen** – es könnte auch sein, dass Menschen mit beginnender (noch unentdeckter) Demenz mehr Schlafmittel/Antihistaminika nehmen (Reverse Causation), auch wenn mehrere Studien versucht haben, das herauszurechnen
- Besonders betroffen: **ältere Menschen** – bei ihnen ist die anticholinerge Belastung ("Anticholinergic Cognitive Burden", ACB-Score) generell ein anerkanntes geriatrisches Risikokonzept
- Diphenhydramin gilt auf der ACB-Skala als Substanz mit **hoher anticholinerger Last** (Score 3)

## Praktische Konsequenz

Geriater und Fachgesellschaften (z. B. Beers-Liste in den USA, PRISCUS-Liste in Deutschland) führen Diphenhydramin bereits seit Jahren als **potenziell inadäquates Medikament für ältere Menschen** und raten zu:
- möglichst kurzzeitigem Einsatz
- Alternativen bei älteren Patienten (z. B. Antihistaminika der 2. Generation ohne relevante ZNS-Gängigkeit)
- Vorsicht bei Kombination mit anderen anticholinergen Substanzen (Kumulationseffekt)

Falls Sie oder Angehörige Diphenhydramin regelmäßig einnehmen (z. B. als Schlafmittel), wäre das definitiv ein guter Punkt, um es beim nächsten Arztbesuch anzusprechen – nicht aus akuter Panik, aber als sinnvolle Medikamenten-Überprüfung, besonders im höheren Lebensalter.
Versuche nochmal open-alex
SystemInit:  id=46b3aa31-cb72-48c0-9ea7-6c8bbfec9a9a, cwd=/home/user/xyan/XY.Archiv, model=claude-sonnet-5
Control Request:
```yaml
id: 416ad376-8836-4be8-af4d-f824bb630f61
toolName: openalex-search
arguments:
  query: diphenhydramine anticholinergic dementia Alzheimer
  reason: Wissenschaftliche Studien in OpenAlex zum Zusammenhang zwischen Diphenhydramin und Demenz/Alzheimer finden
  fields: core
  limit: 15
```
/answer 416ad376-8836-4be8-af4d-f824bb630f61 allow
Control Request:
```yaml
id: 15987fab-4c85-45e7-8f0e-29e6a8fad291
result:
  content:
  - type: text
    text: "Cannot reach OpenAlex (https://api.openalex.org/works?search=diphenhydramine+anticholinergic+dementia+Alzheimer&select=id%2Cdoi%2Ctitle%2Cdisplay_name%2Cpublication_year%2Cpublication_date%2Ctype%2Clanguage%2Cprimary_location%2Copen_access%2Ccited_by_count%2Cprimary_topic%2Crelevance_score&page=1&per-page=15&mailto=openalex%40xyan.icu&api_key=%2A%2A%2A): The read operation timed out"
  isError: true
```
/answer 15987fab-4c85-45e7-8f0e-29e6a8fad291 allow