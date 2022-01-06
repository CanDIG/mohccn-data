import mappings


def province_from_site(mapping):
    site_str = mappings.single_val({"Site": mapping["Site"]})
    if site_str is None:
        return None
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

#"Treatment.0,{candigv1.treatment(Subject, "1st line Chemo- Cycle 1"."Agent Name", "1st line Chemo- Cycle 1"."Start Date")}
def treatment(mapping):
#         ("Treatment", {
#             "patientId": "Subject",
#             "therapeuticModality": (lambda s: s.lower(), "THER_TX_NAME"),
#             "startDate": (date_from_datetime, "STRT_DT"),
#             "stopDate": (date_from_datetime, "LAST_DATE"),
#             "responseToTreatment": "THER_BR"
#         })
    treatment = []
    return treatment
    patient = mappings.single_val({"sub": mapping["Subject"]})
    ther_txs = mappings.list_val({"Agent Name": mapping["Agent Name"]})
    strt_dts = mappings.list_val({"Agent Name": mapping["Agent Name"]})
    for i in range(0, len(ther_txs)):
        print(ther_txs[i])
        treatment_dict = {
            "patientId": patient,
            "therapeuticModality": ther_txs[i].lower(),
            "startDate": None
        }
        if len(strt_dts) > 0:
            if len(strt_dts) == len(ther_txs):
                treatment_dict["startDate"] = mappings.date({"date": strt_dts[i]})
            else:
                raise mappings.MappingError(f"There are {len(ther_txs)} Agent Name but only {len(strt_dts)} Start Date")

        treatment.append(treatment_dict)
    return treatment


#"Outcome.0",{candigv1.outcome(Subject, Survival."Date of Death", Survival."Patient Status")}
def outcome(mapping):
#         ("Outcome", {
#             "patientId": "Subject",
#             "dateOfAssessment": (date_from_datetime, "FU_STATUS_DT"),
#             "diseaseResponseOrStatus": (lambda s: s.strip('"'), "DISEASE_STATUS"),
#             "localId": (outcome_label, "Subject")
#         })
    outcome = []
    patient = mappings.single_val({"Subject": mapping["Subject"]})
    dates = mappings.single_val({"Date of Death": mapping["Date of Death"]})
    statuses = mappings.single_val({"Patient Status": mapping["Patient Status"]})
    outcome_dict = {
        "patientId": patient,
        "dateOfAssessment": mappings.date({"date": dates}),
        "diseaseResponseOrStatus": statuses.strip('"'),
        "localId": f"{patient}_outcome_0"
    }
    outcome.append(outcome_dict)
    return outcome



#"Sample.0",{candigv1.sample(Subject, Biopsy."Date of biopsy", Biopsy.Location)}
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
    collectionDates = mappings.single_val({"Date of biopsy": mapping["Date of biopsy"]})
    sampleTypes = mappings.single_val({"Location": mapping["Location"]})
    sample_dict = {
        "patientId": patient,
        "sampleId": f"{patient}_0",
        "collectionDate": mappings.date({"date": collectionDates}),
        "sampleType": sampleTypes
    }
    sample.append(sample_dict)
    
    return sample
