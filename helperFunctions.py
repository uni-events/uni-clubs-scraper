def CleanClubNameStr(club_name_raw):
    club_name_clean = club_name_raw.lower()
    club_name_clean = club_name_clean.replace(' ', '_')
    return club_name_clean
