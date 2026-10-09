"""
HL7 Message parser
HL7 v2 messages are made of segments (lines), separated by carriage returns.
Each segment starts with a 3-letter code (MSH, PID, OBR, OBX, etc.)
and fields within a segment are separated by pipes "|".

This script parses a sample ORU (Observation Result) message.
"""

# A sample HL7 ORU^R01 message (lab result) - pipes separate fields
sample_hl7 = (
    "MSH|^~\\&|LAB|HOSPITAL|EPIC|HOSPITAL|20250101120000||ORU^R01|MSG00001|P|2.3\r"
    "PID|1||123456^^^MRN||DOE^JANE||19800101|F\r"
    "OBR|1|ORD123|RES456|CORT^Cortisol^L|||20250101110000\r"
    "OBX|1|NM|CORT^Cortisol^L||14.2|ug/dL|5.0-25.0|N|||F\r"
)


def parse_hl7(message: str) -> dict:
    #parse into dictionary of segments
    segments = message.strip().split("\r")
    parsed = {}

    for segment in segments:
        fields = segment.split("|")
        seg_type = fields[0]
        parsed.setdefault(seg_type, []).append(fields)

    return parsed


def extract_result_summary(parsed: dict) -> dict:
    #Pull out the key patient + result info in a readable format
    summary = {}

    #PID segment - patient info
    if "PID" in parsed:
        pid = parsed["PID"][0]
        summary["patient_id"] = pid[3] if len(pid) > 3 else None
        summary["patient_name"] = pid[5] if len(pid) > 5 else None

    #OBR segment - the order
    if "OBR" in parsed:
        obr = parsed["OBR"][0]
        summary["test_ordered"] = obr[4] if len(obr) > 4 else None

    #oBX segment(s) - the actual result value(s)
    if "OBX" in parsed:
        results = []
        for obx in parsed["OBX"]:
            results.append({
                "test_name": obx[3] if len(obx) > 3 else None,
                "value": obx[5] if len(obx) > 5 else None,
                "units": obx[6] if len(obx) > 6 else None,
                "reference_range": obx[7] if len(obx) > 7 else None,
                "abnormal_flag": obx[8] if len(obx) > 8 else None,
            })
        summary["results"] = results

    return summary


if __name__ == "__main__":
    parsed_message = parse_hl7(sample_hl7)
    summary = extract_result_summary(parsed_message)

    print("Parsed HL7 Summary")
    print("-" * 30)
    print(f"Patient ID:    {summary.get('patient_id')}")
    print(f"Patient Name:  {summary.get('patient_name')}")
    print(f"Test Ordered:  {summary.get('test_ordered')}")
    print()
    for result in summary.get("results", []):
        print(f"  {result['test_name']}: {result['value']} {result['units']} "
              f"(ref: {result['reference_range']}, flag: {result['abnormal_flag']})")
