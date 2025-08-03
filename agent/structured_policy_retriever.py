import json

def load_policy_data():
    try:
        with open("data/policy_matrix.json", "r") as f:
            data = json.load(f)
            print("DEBUG: Loaded policy data type =", type(data))
            return data
    except Exception as e:
        print(f"❌ Failed to load policy data: {e}")
        return {}

def safe_val(val):
    return str(val) if val is not None else "Not specified"

def summarize_leave_policy(policy_data, employee):
    band = employee.get("Band", "Unknown")
    leave_entitlements = policy_data.get("leave_entitlements", {})

    leave = leave_entitlements.get(band)
    if not isinstance(leave, dict):
        return f"Leave policy not available for Band {band}"

    return "\n".join([
        f"- Total Leave Days: {safe_val(leave.get('total_leave_days'))}",
        f"- Earned Leave: {safe_val(leave.get('earned_leave'))}",
        f"- Sick Leave: {safe_val(leave.get('sick_leave'))}",
        f"- Casual Leave: {safe_val(leave.get('casual_leave'))}",
        f"- Work From Home Eligibility: {safe_val(leave.get('wfh_eligibility'))}",
        f"- Minimum WFO Days: {safe_val(leave.get('wfo_min_days'))}",
    ])

def summarize_wfo_policy(policy_data, employee):
    department = employee.get("Department", "Unknown")
    wfo_policy = policy_data.get("wfo_policy", {})
    wfo = wfo_policy.get(department)

    if not isinstance(wfo, dict):
        return "WFO policy not available"

    return "\n".join([
        f"- Minimum Office Days: {safe_val(wfo.get('min_days'))}",
        f"- Suggested Days: {safe_val(wfo.get('suggested_days'))}",
        f"- Notes: {safe_val(wfo.get('notes'))}",
    ])

def summarize_travel_policy(policy_data, employee):
    band = employee.get("Band", "Unknown")
    travel_entitlements = policy_data.get("travel_policy", {})
    travel = travel_entitlements.get(band)

    if not isinstance(travel, dict):
        return f"Travel policy not available for Band {band}"

    return "\n".join([
        f"- Domestic Travel Mode: {safe_val(travel.get('travel_mode_domestic'))}",
        f"- International Eligibility: {safe_val(travel.get('international_eligibility'))}",
        f"- Flight Class: {safe_val(travel.get('flight_class'))}",
        f"- Hotel Cap/Night: {safe_val(travel.get('hotel_cap_per_night'))}",
        f"- Per Diem (Domestic): {safe_val(travel.get('per_diem_domestic'))}",
        f"- Per Diem (International): {safe_val(travel.get('per_diem_international'))}",
        f"- Approvals Required: {safe_val(travel.get('approval_required'))}",
    ])

def summarize_structured_policies(_, employee):
    policy_data = load_policy_data()

    try:
        leave_summary = summarize_leave_policy(policy_data, employee)
    except Exception as e:
        leave_summary = f"❌ Leave policy summary failed: {str(e)}"

    try:
        wfo_summary = summarize_wfo_policy(policy_data, employee)
    except Exception as e:
        wfo_summary = f"❌ WFO policy summary failed: {str(e)}"

    try:
        travel_summary = summarize_travel_policy(policy_data, employee)
    except Exception as e:
        travel_summary = f"❌ Travel policy summary failed: {str(e)}"

    return {
        "leave": leave_summary,
        "wfo": wfo_summary,
        "travel": travel_summary
    }
