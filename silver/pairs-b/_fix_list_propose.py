def fix(pairs):
    import re
    for p in pairs:
        pr=p["b"]["qs"][0]["prompt"]
        if re.search(r"\b(Want me|Shall I|Should I)\b", pr):
            p["b"]["qs"][0]["propose"]=True
