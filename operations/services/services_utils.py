def determine_risk_profile(critical_alerts, total_alerts):
    if critical_alerts >= 10:
        health = "High Risk"
    elif total_alerts >= 20:
        health = "Watch"
    else:
        health = "Healthy"
    return health
    