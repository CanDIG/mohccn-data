import mappings


def province_from_site(mapping):
    site_str = mappings.single_val({"Site": mapping["Site"]})
    """
    Infers the province from the site string
    """
    site_mapping = {"BCCA Vancouver Cancer Centre": "British Columbia",
                    "Princess Margaret Cancer Centre": "Ontario"}

    result = "Unknown"
    site = site_str.strip()
    if site in site_mapping:
        result = site_mapping[site]

    return result

#"Treatment.0,{COMPARISON.treatment(Subject, THER_TX_NAME, STRT_DT, LAST_DATE, THER_BR)}
def treatment(mapping):
#         ("Treatment", {
#             "patientId": "Subject",
#             "therapeuticModality": (lambda s: s.lower(), "THER_TX_NAME"),
#             "startDate": (date_from_datetime, "STRT_DT"),
#             "stopDate": (date_from_datetime, "LAST_DATE"),
#             "responseToTreatment": "THER_BR"
#         })
    treatment = []
    patient = mappings.single_val({"sub": mapping["Subject"]})
    ther_txs = mappings.list_val({"THER_TX_NAME": mapping["THER_TX_NAME"]})
    strt_dts = mappings.list_val({"STRT_DT": mapping["STRT_DT"]})
    last_dts = mappings.list_val({"LAST_DATE": mapping["LAST_DATE"]})
    ther_brs = mappings.list_val({"THER_BR": mapping["THER_BR"]})
    if len(ther_txs) != len(strt_dts) or len(ther_txs) != len(last_dts) or len(ther_txs) != len(ther_brs):
        raise SyntaxError(f"For sample {patient}, there are {len(ther_txs)} THER_TX_NAME but {len(strt_dts)} STRT_DT, {len(last_dts)} LAST_DATE, and {len(ther_brs)} THER_BR")
    for i in range(0, len(ther_txs)):
        treatment_dict = {
            "patientId": patient,
            "therapeuticModality": ther_txs[i].lower(),
            "startDate": mappings.date({"date": strt_dts[i]}),
            "stopDate": mappings.date({"date": last_dts[i]}),
            "responseToTreatment": ther_brs[i]
        }
        treatment.append(treatment_dict)
    return treatment


#"Outcome.0",{COMPARISON.outcome(Subject, FU_STATUS_DT, DISEASE_STATUS)}
def outcome(mapping):
#         ("Outcome", {
#             "patientId": "Subject",
#             "dateOfAssessment": (date_from_datetime, "FU_STATUS_DT"),
#             "diseaseResponseOrStatus": (lambda s: s.strip('"'), "DISEASE_STATUS"),
#             "localId": (outcome_label, "Subject")
#         })
    outcome = []
    patient = mappings.single_val({"Subject": mapping["Subject"]})
    dates = mappings.list_val({"FU_STATUS_DT": mapping["FU_STATUS_DT"]})
    statuses = mappings.list_val({"DISEASE_STATUS": mapping["DISEASE_STATUS"]})
    if len(dates) != len(statuses):
        raise SyntaxError(f"For sample {patient}, there are {len(dates)} FU_STATUS_DT but {len(statuses)} DISEASE_STATUS")
    for i in range(0, len(dates)):
        outcome_dict = {
            "patientId": patient,
            "dateOfAssessment": mappings.date({"date": dates[i]}),
            "diseaseResponseOrStatus": statuses[i].strip('"'),
            "localId": f"{patient}_outcome_{i}"
        }
        outcome.append(outcome_dict)
    return outcome



#"Sample.0",{COMPARISON.sample(Subject, SAMPLE_ID, SURG_DT, ARCH_TMR_SITE, CANCER_TYPE_LONG)}
def sample(mapping):
#         ("Sample", {
#             "patientId": "Subject",
#             "sampleId": "SAMPLE_ID",
#             "collectionDate": (date_from_datetime, "SURG_DT"),
#             "sampleType": "ARCH_TMR_SITE",
#             "cancerType": (lambda s: s.lower(), "CANCER_TYPE_LONG")
#         })
    sample = []
    patient = mappings.single_val({"Subject": mapping["Subject"]})
    sampleIds = mappings.list_val({"SAMPLE_ID": mapping["SAMPLE_ID"]})
    collectionDates = mappings.list_val({"SURG_DT": mapping["SURG_DT"]})
    sampleTypes = mappings.list_val({"ARCH_TMR_SITE": mapping["ARCH_TMR_SITE"]})
    cancerTypes = mappings.list_val({"CANCER_TYPE_LONG": mapping["CANCER_TYPE_LONG"]})
#     if len(sampleIds) != len(collectionDates) or len(collectionDates) != len(sampleTypes) or len(sampleTypes) != len(cancerTypes):
#         raise SyntaxError(f"For sample {patient}, there are {len(sampleIds)} SAMPLE_ID but {len(collectionDates)} SURG_DT, {len(sampleTypes)} ARCH_TMR_SITE, and {len(cancerTypes)} CANCER_TYPE_LONG")
    for i in range(0, len(cancerTypes)):
        sample_dict = {
            "patientId": patient,
            "sampleId": sampleIds[i],
            "collectionDate": mappings.date({"date": collectionDates[i]}),
            "sampleType": sampleTypes[i],
            "cancerType": cancerTypes[i].lower()
        }
    
    return sample
