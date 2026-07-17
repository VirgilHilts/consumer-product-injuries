import csv
import re
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

diagnosis_map = {
    41: "Ingestion",
    42: "Aspiration",
    46: "Burns, Electrical",
    47: "Burns, Not Specified",
    48: "Burns, Scald",
    49: "Burns, Chemical",
    50: "Amputation",
    51: "Burns, Thermal",
    52: "Concussions",
    53: "Contusions, Abrasions",
    54: "Crushing",
    55: "Dislocation",
    56: "Foreign Body",
    57: "Fracture",
    58: "Hematoma",
    59: "Laceration",
    60: "Dental Injury",
    61: "Nerve Damage",
    62: "Internal Organ Injury",
    63: "Puncture",
    64: "Strain, Sprain",
    65: "Anoxia",
    66: "Hemorrhage",
    67: "Electric Shock",
    68: "Poisoning",
    69: "Submersion",
    71: "Other/Not Stated",
    72: "Avulsion",
    73: "Burns, Radiation",
    74: "Dermatitis, Conjunctivitis",
}

body_part_map = {
    0: "Internal",
    30: "Shoulder",
    31: "Upper Trunk",
    32: "Elbow",
    33: "Lower Arm",
    34: "Wrist",
    35: "Knee",
    36: "Lower Leg",
    37: "Ankle",
    38: "Pubic Region",
    75: "Head",
    76: "Face",
    77: "Eyeball",
    79: "Lower Trunk",
    80: "Upper Arm",
    81: "Upper Leg",
    82: "Hand",
    83: "Foot",
    84: "25-50% of Body",
    85: "All Parts Body",
    87: "Not Stated/Unknown",
    88: "Mouth",
    89: "Neck",
    92: "Finger",
    93: "Toe",
    94: "Ear",
}

disposition_map = {
    1: "Treated/Examined and Released",
    2: "Treated and Transferred",
    4: "Treated and Admitted/Hospitalized",
    5: "Held for Observation",
    6: "Left Without Being Seen",
    8: "Fatality, Incl. DOA, Died in ER",
    9: "Unknown, Not Stated",
}

location_map = {
    0: "Not Recorded",
    1: "Home",
    2: "Farm/Ranch",
    4: "Street or Highway",
    5: "Other Public Property",
    6: "Mobile/Manufactured Home",
    7: "Industrial",
    8: "School/Daycare",
    9: "Place of Recreation or Sports",
}


# --- Severity Mapping ---
severity_text_map = {
    0: 'Simple',
    1: 'Hospitalization',
    2: 'Amputation',
    3: 'Fatality'
}


broad_category_pattern = {
    "child nursery equipment and supplies": [
        r"baby|infant|toddler|nursery|crib|bassinet|cradle|stroller|carriage|high chair|booster|playpen|play yard|play center|walker|jumper|bouncer|exerciser|carrier|car seat|diaper|pacifier|teething|rattle|changing table|potty|bathinette|night light|baby mattress|baby scale|sterilizer|bottle warmer|infant seat|playpen pad"
    ],
    "household appliances": [
        r"refrigerator|freezer|microwave|oven|stove|range|dishwasher|washer|dryer|vacuum|iron|toaster|blender|mixer|coffee maker|heater|fan|air conditioner|humidifier|dehumidifier|purifier|garbage disposer|trash compactor|water heater|kettle|slow cooker|deep fryer"
    ],
    "furniture and furnishings": [
        r"furniture|chair|table|bed|sofa|couch|dresser|chest|bureau|desk|nightstand|bookcase|shelf|cabinet|mattress|box spring|curtain|rug|carpet|lampshade|recliner|ottoman|bean bag|futon"
    ],
    "toys and children's products": [
        r"toy|doll|action figure|blocks|building set|stuffed|plush|game|board game|ride-on|pretend|dollhouse|playhouse|inflatable toy|balloon|marble|remote control toy|toy weapon"
    ],
    "sports and recreation equipment": [
        r"sport|recreation|exercise|bicycle|bike|skate|ski|snowboard|surf|swim|pool|ball|bat|glove|helmet|camping|hiking|fishing|hunting|gym|weight lifting|gymnastics|playground|swing|slide|trampoline|amusement|ride"
    ],
    "tools and workshop equipment": [
        r"tool|drill|saw|hammer|screwdriver|wrench|ladder|power tool|workshop|garden tool|pruning|chainsaw|lawn mower|snow blower|paint sprayer|welder|compressor"
    ],
    "cleaning equipment and chemicals": [
        r"cleaner|detergent|bleach|ammonia|caustic|drain cleaner|abrasive|polish|wax|spot remover|soap|disinfectant|bucket|pail|mop|broom|vacuum|scrubber"
    ],
    "kitchen and cooking equipment": [
        r"cookware|pot|pan|knife|utensil|cutting board|mixing bowl|blender|food processor|grill|barbecue|pressure cooker|fondue|chafing dish|flatware|tableware|glassware"
    ],
    "lighting and electrical equipment": [
        r"lamp|light|bulb|chandelier|flashlight|extension cord|outlet|receptacle|power strip|generator|battery charger|adapter|surge protector|night-light"
    ],
    "clothing apparel and accessories": [
        r"clothing|apparel|shirt|pants|shoe|footwear|jacket|coat|hat|glove|sock|nightwear|day wear|costume|accessory|jewelry|watch|belt|purse|backpack"
    ],
    "home entertainment and electronics": [
        r"television|tv|radio|stereo|speaker|computer|game console|phone|cell phone|headphone|projector|camera|musical instrument"
    ],
    "outdoor and garden equipment": [
        r"garden|lawn|mower|trimmer|pruner|hose|sprinkler|grill|patio|fence|pool|hot tub|fire pit|outdoor heater|decorative yard"
    ],
    "personal care and cosmetics": [
        r"razor|shaver|hair dryer|curler|makeup|cosmetic|toothbrush|oral hygiene|hairbrush|comb|manicure|pedicure|bath sponge|loofah"
    ],  
    "packaging and containers": [
        r"bottle|jar|can|container|bag|bucket|pail|box|cardboard|plastic container|aerosol|pressurized container"
    ],
    "home structures and construction materials": [
        r"door|ceiling|counter|fence|rail|insulation|lumber|ramp|stair|window|door|ceiling|floor"
    ],
  "other / not elsewhere classified": []   # fallback
}

product_map = {}
with open('NEISS_prod.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        product_map[int(row['FORMAT'])] = row['LABEL']

def assign_category(title: str) -> str:
    title_lower = title.lower()
    for cat, patterns in broad_category_pattern.items():
        for pat in (patterns if isinstance(patterns, list) else [patterns]):
            if pat and re.search(pat, title_lower):
                return cat
    return "other / not elsewhere classified"

def assign_product_name(code):
    if code not in product_map:
        return "UNCATEGORIZED PRODUCT (TO BE ASSIGNED)"
    else:
        return product_map[code]

def compute_funny_score(df):
    # Make a copy so we don't modify original
    df = df.copy()
    
    text = df['Narrative_1'].fillna("").astype(str).str.lower()
    
    # 1. Length component (longer = potentially funnier)
    length_score = text.str.len() / 100.0   # normalize roughly
    
    # 2. Keyword score - absurd/slapstick keywords
    funny_keywords = [
        r'\b(trip|tripped|slipped|fell|falling|landed on|hit.*(floor|table|sink|toilet|dog|bone))',
        r'\b(toilet|bathroom|shower|bed|chair|stairs|porch|ladder|trampoline)',
        r'\b(dog|cat|pet|bone|vape|pot|conditioner|sink|toilet)',
        r'\b(embarrassing|ridiculous|stupid|crazy|hilarious|wtf|omg|lol)',
        r'\b(stood up|stood from|got up from).*?(toilet|bed|chair)',
        r'\b(slid|sliding|missed.*step|gave out|buckled|collapsed)'
    ]
    
    keyword_score = text.str.contains('|'.join(funny_keywords), regex=True, na=False).astype(int) * 3
    
    # 3. Bonus for multiple funny elements
    num_elements = (
        text.str.contains(r'\b(fell|trip|slip)', na=False).astype(int) +
        text.str.contains(r'\b(toilet|bathroom|dog|bone|vape)', na=False).astype(int) +
        text.str.contains(r'\b(pot|conditioner|sink|stairs)', na=False).astype(int)
    )
    
    # Final score
    df['funny_score'] = (
        length_score * 0.4 +
        keyword_score * 1.2 +
        num_elements * 2.0
    ).round(2)
    
    return df


# 2. Load the file (update the path after upload)
file_path = 'neiss2025(NEISS_2025).csv'

df = pd.read_csv(file_path, low_memory=False)

df['Diagnosis_Text']     = df['Diagnosis'].map(diagnosis_map)
df['Body_Part_Text']     = df['Body_Part'].map(body_part_map)

df['Location_Text']      = df['Location'].map(location_map)

df['Amputation'] = df['Diagnosis'] == 50
df['Fatality']  = df['Disposition'] == 8
df['Hospitalized'] = (df['Disposition'] == 2) | \
                     (df['Disposition'] == 4) | \
                     (df['Disposition'] == 5)
df['Severity'] = ( df['Fatality'] * 8) + \
    (df['Amputation'] * 4) + \
    (df['Hospitalized'] * 2)

df["Product_1_Text"] = df["Product_1"].apply(assign_product_name)
df["Product_2_Text"] = df["Product_2"].apply(assign_product_name)

mask = (df['Product_2'] != 0) & df['Product_2'].notna()
df['Prod'] = np.where(mask, df['Product_2_Text'], df['Product_1_Text'])
df['Prod'] = df['Prod'].fillna("Unknown Product")
df["broad_category"] = df["Prod"].apply(assign_category).fillna("Other / Unknown")

print(df["broad_category"].value_counts())

df = compute_funny_score(df)

# See the funniest ones
pd.set_option('display.max_colwidth', None)   # Show full text
print(df.nlargest(10, 'funny_score')[['Narrative_1', 'funny_score']])

df.to_csv('Full Labeled Set,csv')

# now filter on Severity
filtered = df[df['Severity'] > 1]
filtered.to_csv('bad_cases.csv')


agg_all = df.groupby(['broad_category', 'Prod']).agg(
    national_estimate=('Weight', 'sum'),
    avg_Severity=('Severity', 'mean')
).reset_index()

agg_all['national_estimate'] = agg_all['national_estimate'].round(0).astype(int)
agg_all['avg_Severity'] = agg_all['avg_Severity'].round(2)
agg_all.to_csv('agg_all.csv')


# Filter the ORIGINAL df for cases with Amputation or Fatality
serious_df = df[(df['Amputation'] == True) | (df['Fatality'] == True)]

# Re-aggregate only those serious cases
agg_serious = serious_df.groupby(['broad_category', 'Prod']).agg(
    national_estimate=('Weight', 'sum'),
    avg_Severity=('Severity', 'mean')
).reset_index()

agg_serious['national_estimate'] = agg_serious['national_estimate'].round(0).astype(int)
agg_serious['avg_Severity'] = agg_serious['avg_Severity'].round(2)

agg_serious.to_csv('agg_serious.csv')





