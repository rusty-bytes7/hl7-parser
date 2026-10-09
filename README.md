# HL7 Message Parser

A simple Python script that parses HL7 v2 messages- specifically an ORU^R01 (Observation Result) message, the kind of message sent for lab results.

## Why I Built This

As someone with hands-on Epic Beaker experience moving into the analyst side of health IT, I wanted to get a better understanding of how lab result data actually moves between systems. HL7 is the messaging standard behind a lot of that communication- this project was a way to get hands-on with the structure of those messages rather than just seeing the end result in Beaker.

## What It Does

- Parses a sample HL7 message into its component segments (MSH, PID, OBR, OBX)
- Extracts key patient and result information:
  - Patient ID and name
  - Test ordered
  - Result value, units, reference range, and abnormal flag
- Prints a clean, readable summary

## How It Works

HL7 v2 messages are made up of segments (one per line), each starting with a 3-letter code. Fields within a segment are separated by pipes (`|`). This script splits the message into segments, then pulls the relevant fields out of each one into a simple dictionary structure.

## Usage

```bash
python3 hl7_parser.py
```

## Example Output

```
Parsed HL7 Summary
------------------------------
Patient ID:    123456^^^MRN
Patient Name:  DOE^JANE
Test Ordered:  CORT^Cortisol^L

  CORT^Cortisol^L: 14.2 ug/dL (ref: 5.0-25.0, flag: N)
```
