from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def build_html(employee, summaries):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("offer_template.html")
    
    today = datetime.today().strftime("%B %d, %Y")
    
    # Ensure all three summaries are passed to the template
    leave_policy_summary = summaries.get('leave', 'Leave policy not available.')
    travel_policy_summary = summaries.get('travel', 'Travel policy not available.')
    wfo_policy_summary = summaries.get('wfo', 'Work From Office policy not available.')

    context = {
        'date': today,
        'candidate_name': employee["Employee Name"],
        'position': employee["Department"],
        'band_level': employee["Band"],
        'location': employee["Location"],
        'joining_date': employee["Joining Date"],
        'base_salary': f"{employee['Base Salary (INR)']:,}",
        'performance_bonus': f"{employee['Performance Bonus (INR)']:,}",
        'retention_bonus': f"{employee['Retention Bonus (INR)']:,}",
        'total_ctc': f"{employee['Total CTC (INR)']:,}",
        'leave_policy_summary': leave_policy_summary,
        'travel_policy_summary': travel_policy_summary,
        'wfo_policy_summary': wfo_policy_summary,
        'department': employee["Department"]
    }
    
    html_string = template.render(context)
    return html_string