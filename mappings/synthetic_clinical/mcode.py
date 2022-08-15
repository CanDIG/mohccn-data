import mappings
import re


def connect_variant(mapping):
    genomic_id = mappings.single_val({"GenomicID": mapping["1000 Genomes_ID"]})
    if genomic_id is None:
        return None
    return {"genomic_id": genomic_id}

def connect_code(mapping):
    return "code"
    
def connect_org(mapping):
    return "org"
    
def date(mapping):
    return "2022-04-05"
    
def language(mapping):
    return "English"

def placeholder_ontology(mapping):
    return {
                "id": "UNK:0000",
                "label": "abcd"
            }

#Local ontologies for ecog perfomance status saved in a dict  
def ecog_performance_status(mapping):
    ecog_performance_status_dict =  {
        '0': {
            'id': 'ECOG: 0',
            'label': 'Fully active, able to carry on all pre-disease performance without restriction'
        },
        '1': {
            'id': 'ECOG: 1',
            'label': 'Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature, e.g., light house work, office work'
        },
        '2': {
            'id': 'ECOG: 2',
            'label': 'Ambulatory and capable of all selfcare but unable to carry out any work activities; up and about more than 50% of waking hours'
        },
        '3': {
            'id': 'ECOG: 3',
            'label': 'Capable of only limited selfcare; confined to bed or chair more than 50% of waking hours'
        },
        '4': {
            'id': 'ECOG: 4',
            'label': 'Completely disabled; cannot carry on any selfcare; totally confined to bed or chair'
        },
        '5': {
            'id': 'ECOG: 5',
            'label': 'Dead'
        }
    }
    if len(mapping['ECOG']["Vital Signs"]) > 0:
        ecog_val = mapping['ECOG']["Vital Signs"].pop()
        if re.match(r"\d", ecog_val) is not None and int(ecog_val) < 5:
            return ecog_performance_status_dict[ecog_val]
    return None

def cancer_condition(mapping):
    subject_id = mappings.single_val({"Subject": mapping["Subject"]})
    body_site = [placeholder_ontology({"Site": mapping["Site"]})]
    date = mappings.single_date({'Date of Diagnosis': mapping['Date of Diagnosis']})

    if body_site is None and date is None: 
        new_dict = {
            "id": f"{subject_id}-0" ,
            "condition_type": "primary",
            "code": {
                "id": "SNOMED:103329007",
                "label": "Not available"
            },
        }
    elif date is None:
        new_dict = {
            "id": f"{subject_id}-0" ,
            "condition_type": "primary",
            "body_site": body_site,
            "code": {
                "id": "SNOMED:103329007",
                "label": "Not available"
            },
        }
    elif body_site == None:
         new_dict = {
            "id": f"{subject_id}-0" ,
            "condition_type": "primary",
            "body_site": body_site,
            "code": {
                "id": "SNOMED:103329007",
                "label": "Not available"
            },
        }
    else:
        new_dict = {
            "id": f"{subject_id}-0" ,
            "condition_type": "primary",
            "body_site": body_site,
            "code": {
                "id": "SNOMED:103329007",
                "label": "Not available"
            },
            "date_of_diagnosis": date
        }

    return new_dict

#Local ontology for disease status stored in a dict based on RECIST codes
def disease_status(mapping):
    status_val = mappings.single_val({"Overall Response": mapping["Overall Response"]})

     #Gets latest recored disease status value
    if status_val is None or status_val == "NA":
        status_val = ""

    disease_status_dict = {
        'SD': {
            'id': 'SNOMED:359746009',
            'label': 'Patient\'s condition stable (finding)'
        },
        'PD': {
            'id': 'SNOMED:271299001',
            'label': 'Patient\'s condition worsened (finding)'
        },
        'NE': {
            'id': 'SNOMED:709137006',
            'label': 'Patient condition undetermined (finding)'
        },
        'CR': {
            'id': 'USCRS-352236	',
            'label': 'Cancer in complete remission (finding)'
        },
        'PR': {
            'id': 'USCRS-352237',
            'label': 'Cancer in partial remission (finding)'
        }
    }

    if status_val in disease_status_dict.keys():
        return disease_status_dict[status_val]
    return None

# Medication statement dicts (based on termination_reason dict) stored in a array 
def med_code(mapping): #(Subject, "Agent Name", "1st line Chemo- Cycle 1"."Start Date", "Off treatment date", "Off Treatment"."Reason")
    medication_statement_list = None
    medication = mappings.single_val({"Agent Name": mapping["Agent Name"]})
    
    medication_dict = {
        "irinotecan": "RXCUI:51499",
        "fluorouracil": "RXCUI:4492",
        "oxaliplatin": "RXCUI:32592",
        "leucovorin": "RXCUI:6313",
        "gemcitabine": "RXCUI:12574",
        "Abraxane": "RXCUI:589511"
    }

    for med in medication_dict.keys():
        if medication.lower() == med.lower():
            medication_statement_list = {"id": medication_dict[med], "label": med}
    return medication_statement_list

def med_statement_id(mapping):
    return mappings.single_val({"Subject": mapping["Subject"]}) + "-med" + mappings.single_val({"index": mapping["index"]})
