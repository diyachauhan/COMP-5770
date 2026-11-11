# Calculator reference: formulas, scoring rules and units

This reference covers all 16 calculators in the course dataset. Use it when reading worked solutions or designing your evaluator. It specifies the course's formula versions, input units and point thresholds; it is not a completed evaluator.

A reference formula is general knowledge, not a patient-specific answer. The direct baseline does **not** receive these cards. If you give them to a model in a later experiment, report that change as formula-grounded/open-book solving. Gold patient-specific entities and answers remain evaluation-only.

Read the original note as well as the reference annotations. A correct formula with the wrong input or time point is still a faulty solution. Unmentioned findings are not automatically negative; state how you handle missing information and flag annotation assumptions. General calculator references can differ by version: use the one the question requests.

## Example of checking a solution

For a **constructed example** with weight 70 kg and height 175 cm, the correct BMI is `70 / 1.75^2 = 22.85714 kg/m^2`. A response saying `70 / 175^2 = 22.86` ends with an acceptable number but contains an invalid displayed calculation. This is a unit/substitution and arithmetic inconsistency. It is an illustration, not a result observed from a model.

The full cards below let you examine analogous errors: inputs and time points, units, formula version, thresholds, grouped criteria, arithmetic and final precision. You choose which of these your evaluator checks and how you validate it.

## CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk (ID 4)

`score = sum of the non-overlapping point categories below`

| Category | Points / condition |
|---|---|
| Age | <65: 0; 65–74: 1; >=75: 2 |
| Sex category | female: 1; male: 0 |
| Heart failure history | present: 1 |
| Hypertension history | present: 1 |
| Stroke, TIA or systemic thromboembolism history | any present: 2, counted once |
| Vascular disease history | prior MI, peripheral artery disease or aortic plaque: 1 |
| Diabetes history | present: 1 |

Output: integer 0–9. Age categories are mutually exclusive; stroke/TIA/thromboembolism is ONE category, worth at most 2 points. The requested version includes the female-sex point; CHA2DS2-VA is a different score.

References: [Source 1](https://www.mdcalc.com/calc/801/cha2ds2-vasc-score-atrial-fibrillation-stroke-risk).

## Mean Arterial Pressure (MAP) (ID 5)

`MAP = (SBP + 2*DBP)/3`

| Variable | Meaning | Formula input unit |
|---|---|---|
| SBP | systolic pressure | mm Hg |
| DBP | diastolic pressure | mm Hg |

Output: mm Hg. Use both pressures from the requested time point; this is the standard approximation, not a waveform integral.

References: [Source 1](https://www.mdcalc.com/calc/74/mean-arterial-pressure-map).

## Body Mass Index (BMI) (ID 6)

`BMI = weight_kg / height_m^2`

| Variable | Meaning | Formula input unit |
|---|---|---|
| weight | body weight | kg |
| height | height | m |

Output: kg/m^2. Convert cm to m by dividing by 100 before squaring. Do not substitute ideal or adjusted weight.

References: [Source 1](https://www.mdcalc.com/calc/29/body-mass-index-bmi-body-surface-area-bsa).

## Calcium Correction for Hypoalbuminemia (ID 7)

`corrected_calcium = calcium + 0.8*(4 - albumin)`

| Variable | Meaning | Formula input unit |
|---|---|---|
| calcium | measured total calcium | mg/dL |
| albumin | measured albumin | g/dL |

Output: mg/dL; normal albumin is fixed at 4 g/dL for this dataset. Albumin g/L / 10 gives g/dL; calcium mmol/L * 4.0078 gives mg/dL. This estimate is not a measured ionized calcium.

References: [Source 1](https://www.mdcalc.com/calc/31/calcium-correction-hypoalbuminemia).

## Child-Pugh Score for Cirrhosis Mortality (ID 15)

`score = bilirubin_points + albumin_points + INR_points + ascites_points + encephalopathy_points`

| Category | Points / condition |
|---|---|
| Total bilirubin (mg/dL) | <2: 1; 2 through 3: 2; >3: 3 |
| Albumin (g/dL) | >3.5: 1; 2.8 through 3.5: 2; <2.8: 3 |
| INR | <1.7: 1; 1.7 through 2.3: 2; >2.3: 3 |
| Ascites | none: 1; slight/mild: 2; moderate/severe: 3 |
| Hepatic encephalopathy | none: 1; grade I–II: 2; grade III–IV: 3 |

Output: integer 5–15. Each component contributes at least 1 point. Use the INR version and standard bilirubin cutoffs below. Albumin g/L / 10 -> g/dL; bilirubin µmol/L / 17.104 -> mg/dL. Ascites and encephalopathy grades require clinical interpretation.

References: [Source 1](https://www.mdcalc.com/calc/340/child-pugh-score-cirrhosis-mortality).

## Wells' Criteria for DVT (ID 16)

`score = positive_criteria_count - 2*alternative_diagnosis_at_least_as_likely`

| Category | Points / condition |
|---|---|
| Cancer | ongoing/recent treatment or palliation within 6 months: +1 |
| Immobility or surgery | bedridden >3 days OR major surgery within 12 weeks: +1 |
| Calf difference | >3 cm compared with other leg, at 10 cm below tibial tuberosity: +1 |
| Superficial collateral veins | nonvaricose collaterals: +1 |
| Leg swelling | whole symptomatic leg: +1 |
| Deep-vein tenderness | localized to deep venous distribution: +1 |
| Pitting edema | limited to symptomatic leg: +1 |
| Lower-limb immobilization | paralysis, paresis or recent plaster cast: +1 |
| Previous DVT | documented: +1 |
| Alternative diagnosis | at least as plausible as DVT: -2 |

Output: integer -2 through 9. The surgery/bed-rest item is one point even if both apply. This course uses the displayed >3-day bed-rest and >3-cm calf thresholds; preserve these boundary conventions.

References: [Source 1](https://www.mdcalc.com/calc/362/wells-criteria-dvt).

## Revised Cardiac Risk Index for Pre-Operative Risk (ID 17)

`RCRI = count of the six positive categories below`

| Category | Points / condition |
|---|---|
| Surgery | intraperitoneal, intrathoracic or suprainguinal vascular: +1 |
| Ischemic heart disease history | evidence of ischemic disease (MI, positive stress test, ischemic pain, nitrate therapy or pathological Q waves): +1 |
| Heart failure history | present: +1 |
| Cerebrovascular disease history | prior stroke or TIA: +1 |
| Preoperative insulin treatment | present: +1 |
| Preoperative creatinine | >2 mg/dL: +1 |

Output: integer 0–6, not a percent risk. Diabetes alone does not satisfy the insulin-treatment item. Creatinine must be >2 mg/dL, not >=2. Convert creatinine µmol/L / 88.4 -> mg/dL.

References: [Source 1](https://www.mdcalc.com/calc/1739/revised-cardiac-risk-index-pre-operative-risk).

## Fibrosis-4 (FIB-4) Index for Liver Fibrosis (ID 19)

`FIB4 = (age * AST) / (platelets * sqrt(ALT))`

| Variable | Meaning | Formula input unit |
|---|---|---|
| age | age | years |
| AST | aspartate aminotransferase | U/L |
| ALT | alanine aminotransferase | U/L |
| platelets | platelet count | 10^9/L |

Output: conventional FIB-4 index (no output unit). K/µL has the same numeric value as 10^9/L; counts per µL or mm^3 must be divided by 1000. ALT and platelet count must be positive.

References: [Source 1](https://www.mdcalc.com/calc/2200/fibrosis-4-fib-4-index-liver-fibrosis).

## Centor Score (Modified/McIsaac) for Strep Pharyngitis (ID 20)

`modified_Centor = age_adjustment + fever + tonsillar_finding + anterior_nodes + absence_of_cough`

| Category | Points / condition |
|---|---|
| Age | 3–14: +1; 15–44: 0; >=45: -1 (not specified here for age <3) |
| Temperature | >38 °C: +1 |
| Tonsillar finding | exudate OR swelling: +1, counted once |
| Anterior cervical nodes | tender/swollen: +1 |
| Cough | documented absence: +1; present: 0 |

Output: integer -1 through 5. This is Modified Centor/McIsaac, not original Centor without age adjustment. Fever uses >38 °C. Convert Fahrenheit with (F-32)*5/9. Not mentioning cough is not the same as explicitly documenting its absence.

References: [Source 1](https://www.mdcalc.com/calc/104/centor-score-modified-mcisaac-strep-pharyngitis).

## Glasgow Coma Score (GCS) (ID 21)

`GCS = eye + verbal + motor`

| Category | Points / condition |
|---|---|
| Eye | spontaneous: 4; to sound: 3; to pressure/pain: 2; none: 1 |
| Verbal | oriented: 5; confused: 4; isolated/inappropriate words: 3; sounds: 2; none: 1 |
| Motor | obeys: 6; localizes: 5; normal flexion/withdrawal: 4; abnormal flexion: 3; extension: 2; none: 1 |

Output: integer 3–15 when all three components are assessable. Abnormal flexion (3) differs from normal withdrawal (4). A missing or untestable component is not automatically normal. The source annotations may use assumptions; flag such discrepancies rather than treating that assumption as a clinical rule.

References: [Source 1](https://www.glasgowcomascale.org/downloads/GCS-Assessment-Aid.pdf); [Source 2](https://www.glasgowcomascale.org/faq/).

## Sodium Correction for Hyperglycemia (ID 26)

`corrected_sodium = measured_sodium + 0.024*(glucose - 100)`

| Variable | Meaning | Formula input unit |
|---|---|---|
| measured_sodium | measured sodium | mEq/L |
| glucose | serum glucose | mg/dL |

Output: mEq/L. The course questions use the Hillier 2.4 mEq/L per 100 mg/dL convention. The alternative 1.6 coefficient is a different convention, not an arithmetic equivalent. Glucose mmol/L * 18.01559 gives mg/dL. Sodium mmol/L is numerically equivalent to mEq/L.

References: [Source 1](https://www.mdcalc.com/calc/50/sodium-correction-hyperglycemia).

## Serum Osmolality (ID 30)

`calculated_osm = 2*sodium + BUN/2.8 + glucose/18`

| Variable | Meaning | Formula input unit |
|---|---|---|
| sodium | sodium | mmol/L or mEq/L |
| BUN | blood urea nitrogen | mg/dL |
| glucose | serum glucose | mg/dL |

Course answer unit: mOsm/kg (the conventional calculated estimate). This version excludes ethanol. BUN is nitrogen mass, not total urea mass: urea mmol/L * 2.80134 gives BUN mg/dL. Distinguish measured osmolality, calculated osmolar concentration, and effective osmolality.

References: [Source 1](https://www.mdcalc.com/calc/91/serum-osmolality-osmolarity).

## Anion Gap (ID 39)

`anion_gap = sodium - (chloride + bicarbonate)`

| Variable | Meaning | Formula input unit |
|---|---|---|
| sodium | sodium | mEq/L |
| chloride | chloride | mEq/L |
| bicarbonate | bicarbonate | mEq/L |

Output: mEq/L. The question version excludes potassium and albumin correction. These monovalent ions have numerically equivalent mmol/L and mEq/L values. Do not substitute an albumin-corrected gap.

References: [Source 1](https://www.mdcalc.com/calc/1669/anion-gap).

## CURB-65 Score for Pneumonia Severity (ID 45)

`CURB65 = count of the five positive categories below`

| Category | Points / condition |
|---|---|
| Confusion | present: +1 |
| Urea/BUN | BUN >19 mg/dL (urea >7 mmol/L convention): +1 |
| Respiration | respiratory rate >=30/min: +1 |
| Blood pressure | SBP <90 mm Hg OR DBP <=60 mm Hg: +1 |
| Age | >=65 years: +1 |

Output: integer 0–5. Low systolic OR diastolic pressure counts once. Course BUN cutoff: >19 mg/dL; the referenced alternative is urea >7 mmol/L. BUN and urea are not interchangeable mass measurements.

References: [Source 1](https://www.mdcalc.com/calc/324/curb-65-score-pneumonia-severity).

## SIRS Criteria (ID 51)

`SIRS_count = count of the four positive groups below`

| Category | Points / condition |
|---|---|
| Temperature | >38 °C OR <36 °C: +1 |
| Heart rate | >90/min: +1 |
| Respiration | respiratory rate >20/min OR PaCO2 <32 mm Hg: +1 |
| Leukocytes | WBC >12000/mm^3 OR <4000/mm^3 OR immature bands >10%: +1 |

Output: integer 0–4. Multiple abnormal values within one group still contribute only one point. WBC K/µL * 1000 gives cells/µL, numerically equivalent to cells/mm^3. This task counts traditional adult SIRS criteria; it does not establish a current sepsis diagnosis.

References: [Source 1](https://www.mdcalc.com/calc/1096/sirs-sepsis-septic-shock-criteria).

## Body Surface Area Calculator (ID 60)

`BSA = sqrt(weight_kg * height_cm / 3600)`

| Variable | Meaning | Formula input unit |
|---|---|---|
| weight | body weight | kg |
| height | height | cm |

Output: m^2. Mosteller version. Height stays in centimetres, unlike BMI. Du Bois and other BSA equations are different versions.

References: [Source 1](https://www.mdcalc.com/calc/29/body-mass-index-bmi-body-surface-area-bsa).

