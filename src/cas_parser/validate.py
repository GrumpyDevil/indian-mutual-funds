def validate(holdings):
    """
    Validates holdings by checking if units * nav approx equals value.
    """
    valid = []
    error_log = []

    for h in holdings:
        calc_value = h["units"] * h["nav"]
        actual_value = h["value"]
        
        # If value is 0, just accept it
        if actual_value == 0:
            valid.append(h)
            continue
            
        # Check for 1% tolerance
        diff_pct = abs(calc_value - actual_value) / max(actual_value, 1)
        if diff_pct < 0.05: # Use 5% tolerance as NAVs in CAS might be slightly rounded or dated
            valid.append(h)
        else:
            error_log.append(f"Validation failed for {h['scheme']}: Calc={calc_value}, Actual={actual_value}")

    return valid, error_log
