import os
import pandas as pd
import pyreadstat

RAW_DATA_PATH = os.path.join("data", "raw", "ATP W27.sav")
OUTPUT_DIR = os.path.join("data", "processed")

os.makedirs(OUTPUT_DIR, exist_ok=True)

df, meta = pyreadstat.read_sav(RAW_DATA_PATH, apply_value_formats=True)

main_columns = [
    "WEIGHT_W27",
    "CAREREL_W27",
    "CAREGIV1_W27",
    "CAREGIV2_W27",
    "CAREGIV3A_W27",
    "CAREGIV3B_W27",
    "CAREGIV4_W27",
    "CAREGIV6A_W27",
    "CAREGIV6B_W27",
    "CAREGIV6C_W27",
    "CAREGIV6D_W27",
    "CAREGIV6E_W27",
    "CAREGIV6F_W27",
    "CAREGIV7_W27",
]

reason_mention_columns = [
    "CAREGIV5pos_m1",
    "CAREGIV5pos_m2",
    "CAREGIV5pos_m3",
    "CAREGIV5neg_m1",
    "CAREGIV5neg_m2",
]

available_reason_columns = [
    col for col in reason_mention_columns
    if col in df.columns
]

columns_needed = main_columns + available_reason_columns
caregiver_df = df[columns_needed].copy()

rename_map = {
    "WEIGHT_W27": "weight",
    "CAREREL_W27": "care_responsibility",
    "CAREGIV1_W27": "heard_before",
    "CAREGIV2_W27": "realistic",
    "CAREGIV3A_W27": "enthusiastic",
    "CAREGIV3B_W27": "worried",
    "CAREGIV4_W27": "willing_to_use",
    "CAREGIV6A_W27": "less_worried_about_family_care",
    "CAREGIV6B_W27": "society_saves_money",
    "CAREGIV6C_W27": "treat_robot_like_friend",
    "CAREGIV6D_W27": "older_adults_more_isolated",
    "CAREGIV6E_W27": "older_adults_more_independent",
    "CAREGIV6F_W27": "only_for_people_who_cannot_afford_human_caregiver",
    "CAREGIV7_W27": "camera_human_operator",
    "CAREGIV5pos_m1": "positive_reason_1",
    "CAREGIV5pos_m2": "positive_reason_2",
    "CAREGIV5pos_m3": "positive_reason_3",
    "CAREGIV5neg_m1": "negative_reason_1",
    "CAREGIV5neg_m2": "negative_reason_2",
}

caregiver_df = caregiver_df.rename(columns=rename_map)
caregiver_df = caregiver_df.dropna(subset=["weight"])


def weighted_percentage(data, column, positive_values):
    valid = data.dropna(subset=[column, "weight"]).copy()

    if valid.empty:
        return 0.0

    mask = valid[column].astype(str).isin(positive_values)
    numerator = valid.loc[mask, "weight"].sum()
    denominator = valid["weight"].sum()

    if denominator == 0:
        return 0.0

    return round((numerator / denominator) * 100, 1)


def weighted_distribution(data, column):
    valid = data.dropna(subset=[column, "weight"]).copy()

    grouped = (
        valid
        .groupby(column, dropna=False, observed=False)["weight"]
        .sum()
        .reset_index()
    )

    grouped["percentage"] = grouped["weight"] / grouped["weight"].sum() * 100
    grouped["percentage"] = grouped["percentage"].round(1)
    grouped = grouped.rename(columns={column: "response"})
    grouped["variable"] = column

    return grouped[["variable", "response", "percentage"]]


readiness_summary = pd.DataFrame([
    {
        "stage": "Heard at least a little",
        "percentage": weighted_percentage(
            caregiver_df,
            "heard_before",
            ["A lot", "A little"]
        ),
        "description": "Respondents who had heard, read, or thought about robot caregivers before the survey."
    },
    {
        "stage": "See it as realistic",
        "percentage": weighted_percentage(
            caregiver_df,
            "realistic",
            ["Extremely realistic", "Somewhat realistic"]
        ),
        "description": "Respondents who thought the robot caregiver concept seemed at least somewhat realistic."
    },
    {
        "stage": "Feel enthusiastic",
        "percentage": weighted_percentage(
            caregiver_df,
            "enthusiastic",
            ["Very enthusiastic", "Somewhat enthusiastic"]
        ),
        "description": "Respondents who felt at least somewhat enthusiastic about robot caregivers."
    },
    {
        "stage": "Would use it",
        "percentage": weighted_percentage(
            caregiver_df,
            "willing_to_use",
            ["Yes"]
        ),
        "description": "Respondents who would be interested in a robot caregiver for themselves or a family member."
    },
])

consequence_items = [
    {
        "variable": "less_worried_about_family_care",
        "label": "Less family worry",
        "category": "Benefit",
        "full_question": "Young people would feel less worried about caring for their aging relatives"
    },
    {
        "variable": "society_saves_money",
        "label": "Society saves money",
        "category": "Benefit",
        "full_question": "Society would save money on caring for older adults"
    },
    {
        "variable": "treat_robot_like_friend",
        "label": "Robot as human friend",
        "category": "Ambivalent",
        "full_question": "Many older adults would treat their robot caregiver like a human friend"
    },
    {
        "variable": "older_adults_more_isolated",
        "label": "More isolated",
        "category": "Concern",
        "full_question": "Older adults would feel more isolated than they do today"
    },
    {
        "variable": "older_adults_more_independent",
        "label": "More independent",
        "category": "Benefit",
        "full_question": "Older adults would feel more independent and self sufficient"
    },
    {
        "variable": "only_for_people_who_cannot_afford_human_caregiver",
        "label": "Only for those unable to afford human care",
        "category": "Concern",
        "full_question": "These robots would only be used by people who could not afford a human caregiver"
    },
]

consequence_rows = []

for item in consequence_items:
    consequence_rows.append({
        "label": item["label"],
        "category": item["category"],
        "full_question": item["full_question"],
        "percentage_likely": weighted_percentage(
            caregiver_df,
            item["variable"],
            ["Yes, likely"]
        )
    })

consequence_summary = pd.DataFrame(consequence_rows)

oversight_summary = weighted_distribution(caregiver_df, "camera_human_operator")

distribution_columns = [
    "heard_before",
    "realistic",
    "enthusiastic",
    "worried",
    "willing_to_use",
    "camera_human_operator",
]

distribution_summary = pd.concat(
    [weighted_distribution(caregiver_df, col) for col in distribution_columns],
    ignore_index=True
)

metric_definitions = [
    {
        "metric": "Heard at least a little",
        "column": "heard_before",
        "positive_values": ["A lot", "A little"]
    },
    {
        "metric": "Realistic",
        "column": "realistic",
        "positive_values": ["Extremely realistic", "Somewhat realistic"]
    },
    {
        "metric": "Enthusiastic",
        "column": "enthusiastic",
        "positive_values": ["Very enthusiastic", "Somewhat enthusiastic"]
    },
    {
        "metric": "Worried",
        "column": "worried",
        "positive_values": ["Very worried", "Somewhat worried"]
    },
    {
        "metric": "Would use",
        "column": "willing_to_use",
        "positive_values": ["Yes"]
    },
    {
        "metric": "Camera feels better",
        "column": "camera_human_operator",
        "positive_values": ["Better"]
    },
    {
        "metric": "More independent",
        "column": "older_adults_more_independent",
        "positive_values": ["Yes, likely"]
    },
    {
        "metric": "More isolated",
        "column": "older_adults_more_isolated",
        "positive_values": ["Yes, likely"]
    },
]

care_order = [
    "I am already doing this",
    "Very likely",
    "Somewhat likely",
    "Not too likely",
    "Not at all likely",
]

heatmap_rows = []

for group in care_order:
    group_df = caregiver_df[caregiver_df["care_responsibility"].astype(str) == group]

    if group_df.empty:
        continue

    for metric in metric_definitions:
        heatmap_rows.append({
            "care_responsibility": group,
            "metric": metric["metric"],
            "percentage": weighted_percentage(
                group_df,
                metric["column"],
                metric["positive_values"]
            )
        })

heatmap_summary = pd.DataFrame(heatmap_rows)


def clean_reason_text(value):
    if pd.isna(value):
        return None

    text = str(value).strip()

    invalid_values = [
        "",
        "nan",
        "none",
        "refused",
        "no answer",
        "not selected",
        "not selected/no answer",
    ]

    if text.lower() in invalid_values:
        return None

    return text


def build_reason_summary(data):
    rows = []

    positive_cols = [
        col for col in ["positive_reason_1", "positive_reason_2", "positive_reason_3"]
        if col in data.columns
    ]

    negative_cols = [
        col for col in ["negative_reason_1", "negative_reason_2"]
        if col in data.columns
    ]

    positive_base = data[data["willing_to_use"].astype(str).eq("Yes")].copy()
    negative_base = data[data["willing_to_use"].astype(str).eq("No")].copy()

    positive_denominator = positive_base["weight"].sum()
    negative_denominator = negative_base["weight"].sum()

    for _, row in positive_base.iterrows():
        for col in positive_cols:
            reason = clean_reason_text(row.get(col))

            if reason is not None:
                rows.append({
                    "reason": reason,
                    "stance": "Would use",
                    "weight": row["weight"]
                })

    for _, row in negative_base.iterrows():
        for col in negative_cols:
            reason = clean_reason_text(row.get(col))

            if reason is not None:
                rows.append({
                    "reason": reason,
                    "stance": "Would not use",
                    "weight": row["weight"]
                })

    reason_mentions = pd.DataFrame(rows)

    if reason_mentions.empty:
        return pd.DataFrame(columns=["reason", "stance", "percentage", "weighted_count"])

    grouped = (
        reason_mentions
        .groupby(["reason", "stance"], observed=False)["weight"]
        .sum()
        .reset_index()
        .rename(columns={"weight": "weighted_count"})
    )

    def calculate_percentage(row):
        if row["stance"] == "Would use":
            denominator = positive_denominator
        else:
            denominator = negative_denominator

        if denominator == 0:
            return 0.0

        return round(row["weighted_count"] / denominator * 100, 1)

    grouped["percentage"] = grouped.apply(calculate_percentage, axis=1)

    grouped = grouped.sort_values(["stance", "percentage"], ascending=[True, False])
    return grouped[["reason", "stance", "percentage", "weighted_count"]]


reason_summary = build_reason_summary(caregiver_df)

caregiver_df.to_csv(
    os.path.join(OUTPUT_DIR, "caregiver_respondent_clean.csv"),
    index=False
)

readiness_summary.to_csv(
    os.path.join(OUTPUT_DIR, "readiness_summary.csv"),
    index=False
)

consequence_summary.to_csv(
    os.path.join(OUTPUT_DIR, "consequence_summary.csv"),
    index=False
)

oversight_summary.to_csv(
    os.path.join(OUTPUT_DIR, "oversight_summary.csv"),
    index=False
)

distribution_summary.to_csv(
    os.path.join(OUTPUT_DIR, "distribution_summary.csv"),
    index=False
)

heatmap_summary.to_csv(
    os.path.join(OUTPUT_DIR, "care_responsibility_heatmap.csv"),
    index=False
)

reason_summary.to_csv(
    os.path.join(OUTPUT_DIR, "reason_bubble_summary.csv"),
    index=False
)

print("Clean data created successfully.")
print("Saved files:")
print("data/processed/caregiver_respondent_clean.csv")
print("data/processed/readiness_summary.csv")
print("data/processed/consequence_summary.csv")
print("data/processed/oversight_summary.csv")
print("data/processed/distribution_summary.csv")
print("data/processed/care_responsibility_heatmap.csv")
print("data/processed/reason_bubble_summary.csv")

print("\nReason summary:")
print(reason_summary.sort_values("percentage", ascending=False).head(30))