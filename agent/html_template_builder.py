from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def build_html(employee, summaries):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("offer_template.html")
    
    today = datetime.today().strftime("%B %d, %Y")

    return template.render(
        date=today,
        name=employee["Employee Name"],
        position=employee["Department"],
        band=employee["Band"],
        location=employee["Location"],
        joining_date=employee["Joining Date"],
        base=employee["Base Salary (INR)"],
        perf=employee["Performance Bonus (INR)"],
        ret=employee["Retention Bonus (INR)"],
        total=employee["Total CTC (INR)"],
        leave_summary=summaries["leave"],
        wfo_summary=summaries.get("wfo", "WFO policy not available"),
        travel_summary=summaries["travel"]
    )
