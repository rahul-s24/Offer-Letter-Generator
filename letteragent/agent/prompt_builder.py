from datetime import datetime

def build_prompt(employee: dict, policy_chunks: list) -> str:
    name = employee["Employee Name"]
    department = employee["Department"]
    band = employee["Band"]
    base = employee["Base Salary (INR)"]
    bonus = employee["Performance Bonus (INR)"]
    retention = employee["Retention Bonus (INR)"]
    total = employee["Total CTC (INR)"]
    location = employee["Location"]
    joining = employee["Joining Date"]
    date_today = [datetime.today().strftime("%B %d, %Y")] 

    policies = "\n".join(policy_chunks)

    return f"""
Generate an offer letter with the following structure and data:

📄 Offer Letter – Company ABC
Date: {date_today}
Candidate Name: {name}
Position: [Your Defined Role, e.g., "Marketing Analyst"]
Band Level: {band}
Location: {location}
Joining Date: {joining}

1. 🎯 Appointment Details  
We are delighted to offer you the position of [Position] in the {department} team at Company ABC. This is a full-time role based out of our {location} office. Your employment will be governed by the terms outlined in this letter and the Employee Handbook.

2. 💰 Compensation Structure  
Component\tAnnual (INR)  
Fixed Salary\t₹{base}  
Performance Bonus\t₹{bonus}  
Retention Bonus (2 yrs)\t₹{retention}  
Total CTC\t₹{total}  

Performance bonuses are disbursed quarterly, subject to performance evaluation.

3. 🏖 Leave Entitlements (Band {band})  
{policies}

4. 🏢 Work From Office Policy ({department} Team)  
You are expected to follow a hybrid working model with a minimum of 3 days/week in office (suggested: Monday, Tuesday, Thursday). Exceptions for full-remote during sprints may be approved by your manager.

You are eligible for:  
- Rs. 1,000/month internet reimbursement  
- One-time Rs. 5,000 home-office setup support

5. ✈ Travel Policy (Band {band})  
You will be eligible for official travel as per Band {band} norms:  
- Domestic Travel: Economy flights standard  
- International Travel: Allowed for conferences and client meetings  
- Hotel Cap: Rs. 4,000/night  
- Per Diem: Rs. 3,000/day (domestic), USD 60/day (international)  
All travel must be approved by your reporting manager and booked via the designated platform.

6. 🔒 Confidentiality & IP Clause  
You are expected to maintain strict confidentiality of all proprietary data, financials, codebases, and client information. All work products created during employment shall remain the intellectual property of Company ABC. A separate NDA and IP Agreement will be shared along with this letter.

7. 🚨 Termination & Exit  
- Either party may terminate the employment with 60 days’ notice.  
- During probation (first 3 months), a 15-day notice period applies.  
- All company property and access must be returned on final working day.

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
