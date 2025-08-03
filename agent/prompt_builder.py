from datetime import datetime
import unicodedata

def clean_unicode(text):
    # Replace problematic Unicode characters with ASCII equivalents
    replacements = {
        "–": "-",  # en dash
        "—": "-",  # em dash
        "“": '"', "”": '"',  # double quotes
        "‘": "'", "’": "'",  # single quotes
        "•": "-",  # bullet
        "●": "-",  # filled circle
        "→": "->",
        " ": " ",  # non-breaking space
    }
    for bad_char, good_char in replacements.items():
        text = text.replace(bad_char, good_char)
    return unicodedata.normalize("NFKD", text)

def build_prompt(employee, summaries):
    current_date = datetime.today().strftime("%B %d, %Y")

    name = employee["Employee Name"]
    department = employee["Department"]
    band = employee["Band"]
    location = employee["Location"]
    joining_date = employee["Joining Date"]
    base = employee["Base Salary (INR)"]
    perf = employee["Performance Bonus (INR)"]
    ret = employee["Retention Bonus (INR)"]
    total = employee["Total CTC (INR)"]

    prompt = f"""
Offer Letter - Company ABC
Date: {current_date}
Candidate Name: {name}
Position: {department}
Band Level: {band}
Location: {location}
Joining Date: {joining_date}

1. 🎯 Appointment Details
We are delighted to offer you the position of {department} in the {department} team at Company ABC. This is a full-time role based out of our {location} office. Your employment will be governed by the terms outlined in this letter and the Employee Handbook.

2. 💰 Compensation Structure
Component              Annual (INR)
Fixed Salary           {base}
Performance Bonus      {perf}
Retention Bonus        {ret}
Total CTC              {total}
Performance bonuses are disbursed quarterly, subject to performance evaluation.

3. 🏖 Leave Entitlements (Band {band})
{summaries['leave']}

4. 🏢 Work From Office Policy ({department} Team)
{summaries.get('wfo', 'WFO policy not available.')}

5. ✈️ Travel Policy (Band {band})
{summaries['travel']}

6. 🔒 Confidentiality & IP Clause
You are expected to maintain strict confidentiality of all proprietary data, financials, codebases, and client information. All work products created during employment shall remain the intellectual property of Company ABC.
A separate NDA and IP Agreement will be shared along with this letter.

7. 🚨 Termination & Exit
- Either party may terminate the employment with 60 days' notice
- During probation (first 3 months), a 15-day notice period applies
- All company property and access must be returned on final working day

8. ✅ Next Steps
Please confirm your acceptance of this offer by signing and returning this letter via DocuSign within 5 working days.
Upon acceptance, your onboarding buddy and People Ops partner will reach out with pre-joining formalities.

Warm regards,
Aarti Nair
HR Business Partner
Company ABC
📧 peopleops@companyabc.com
🌐 www.companyabc.com
    """

    return clean_unicode(prompt)
