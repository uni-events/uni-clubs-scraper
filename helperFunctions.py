def CleanClubNameStr(club_name_raw):
    club_name_clean = []
    for name in club_name_raw:
        name = name.lower()
        name = name.replace(' ', '_')
        club_name_clean.append(name)
    return club_name_clean
