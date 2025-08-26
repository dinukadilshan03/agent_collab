from agents.extractor import run_agent

# Sample medical report text
sample_report = """
GENERAL HOSPITAL
123 Healthcare Avenue, Metropolis, NY 10001
Tel: (555) 123-4567 | Fax: (555) 123-4098

PATIENT INFORMATION

Name: SMITH, Johnathan Robert

MRN: 789456123

Date of Birth: April 12, 1958

Age: 66

Gender: Male

Admission Date: October 26, 2023

Discharge Date: October 28, 2023

ATTENDING PHYSICIAN

Name: Dr. Eleanor Vance, MD

Department: Internal Medicine

NPI: 1234567890

HISTORY OF PRESENT ILLNESS
Mr. Smith is a 66-year-old male with a past medical history significant for hypertension, hyperlipidemia, and type 2 diabetes mellitus who presented to the Emergency Department with a chief complaint of acute onset, substernal chest pain radiating to his left jaw and associated with diaphoresis and shortness of breath. The pain began approximately 3 hours prior to arrival while he was watching television. He rates the pain as 8/10 in severity. He took 1 sublingual nitroglycerin tablet from a friend without significant relief.

PAST MEDICAL HISTORY

Hypertension (HTN)

Hyperlipidemia (HLD)

Type 2 Diabetes Mellitus (T2DM), diagnosed 2010

Gastroesophageal Reflux Disease (GERD)

PAST SURGICAL HISTORY

Appendectomy (1972)

Cholecystectomy (2001)

FAMILY HISTORY
Father: died of myocardial infarction at age 62. Mother: history of dementia. No known family history of cancer.

SOCIAL HISTORY
Patient is a former smoker (1 pack per day for 20 years, quit in 2005). He denies current alcohol or illicit drug use. He works as a retired electrician.

ALLERGIES

Penicillin: causes hives

Lisinopril: causes angioedema

No known food allergies

HOME MEDICATIONS ON ADMISSION

Metformin 500 mg oral tablet, take one tablet twice daily

Atorvastatin 20 mg oral tablet, take one tablet at bedtime

Aspirin 81 mg oral tablet, take one tablet daily

Omeprazole 20 mg oral tablet, take one tablet daily

REVIEW OF SYSTEMS
As per HPI, otherwise negative.

PHYSICAL EXAMINATION ON ADMISSION

Vitals: Temp 98.7°F, BP 168/95, HR 102, RR 18, SpO2 96% on room air.

General: Anxious-appearing male, clutching his chest.

Cardiovascular: Tachycardic rate, regular rhythm, no murmurs, rubs, or gallops.

Respiratory: Lungs clear to auscultation bilaterally.

Abdomen: Soft, non-tender, non-distended.

HOSPITAL COURSE & DISCHARGE MEDICATIONS
Patient was admitted to the telemetry floor. ECG showed ST-segment depression in anterolateral leads. Initial troponin I was elevated at 1.8 ng/mL (ref: <0.04 ng/mL). He was started on a heparin drip and given 325 mg aspirin. A coronary angiogram was performed on 10/27/2023, which revealed a 90% stenosis of the left anterior descending (LAD) artery. A drug-eluting stent was successfully placed. Post-procedure, he was started on Clopidogrel. His symptoms resolved. He was hemodynamically stable at discharge and was instructed to follow a cardiac diet.

DISCHARGE DIAGNOSES

Acute Non-ST Elevation Myocardial Infarction (NSTEMI) - I21.4

Hypertension - I10

Hyperlipidemia - E78.5

Type 2 Diabetes Mellitus - E11.9

DISCHARGE MEDICATIONS

Aspirin 81 mg oral tablet, take one tablet daily

Atorvastatin 40 mg oral tablet, take one tablet at bedtime (INCREASED DOSE)

Clopidogrel 75 mg oral tablet, take one tablet daily (NEW)

Metoprolol Succinate 25 mg oral tablet, take one tablet daily (NEW)

Metformin 500 mg oral tablet, take one tablet twice daily

Omeprazole 20 mg oral tablet, take one tablet daily

PROCEDURES PERFORMED

Coronary Angiogram with Percutaneous Coronary Intervention (PCI) and stent placement to LAD artery - October 27, 2023.

DISCHARGE INSTRUCTIONS

Follow up with Dr. Vance in 7 days.

Follow up with Cardiology (Dr. Ibanez) in 14 days.

Cardiac rehabilitation referral provided.

Diet: Low sodium, low fat, diabetic diet.

Activity: No heavy lifting >10 lbs for 1 week.

Dr. Eleanor Vance, MD
October 28, 2023 14:30
Electronically Signed
"""

# Run the extractor agent
result = run_agent(sample_report)

# Print the result
print("Extracted Data:")
print(result)
