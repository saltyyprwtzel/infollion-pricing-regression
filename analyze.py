import pandas as pd

# Load data
df = pd.read_csv("pricing_diff.csv")

# Calculate price difference
df["difference"] = df["v2_total"] - df["v1_total"]

# --------------------------------------------------
# Q1: Naive count
# --------------------------------------------------

q1_count = (df["v2_total"] != df["v1_total"]).sum()

print("Q1 - Naive non-zero difference count:", q1_count)


# --------------------------------------------------
# Q2: Identify genuine regression
# --------------------------------------------------

# Exclude books because its pricing change was intentional.
non_books = df[df["category"] != "books"].copy()

# The remaining large, systematic differences occur for
# fragile + express orders.
affected = non_books[
    (non_books["category"] == "fragile") &
    (non_books["express"] == True)
].copy()

q2_count = len(affected)

print("Q2 - Genuine regression count:", q2_count)
print("Affected conditions:")
print("  category = fragile")
print("  express = True")


# --------------------------------------------------
# Q3: Total overcharge
# --------------------------------------------------

q3_total_overcharge = affected["difference"].sum()

print("Q3 - Total overcharge: $", round(q3_total_overcharge, 2))


# --------------------------------------------------
# Q4: Baseline sanity check
# --------------------------------------------------

# Remove books and the identified affected population.
baseline = non_books.drop(index=affected.index)

q4_mean = (
    baseline["v1_total"] - baseline["v2_total"]
).mean()

q4_mean_abs = baseline["difference"].abs().mean()

print("Q4 - Average v1_total - v2_total:", q4_mean)
print("Q4 - Average absolute difference:", q4_mean_abs)


# --------------------------------------------------
# Additional verification
# --------------------------------------------------

print("\nAffected difference statistics:")
print(affected["difference"].describe())

print("\nAffected orders by coupon:")
print(affected["coupon"].value_counts(dropna=False))

# Check relationship between distance and overcharge
correlation = affected["distance_km"].corr(affected["difference"])

print("\nCorrelation between distance and overcharge:")
print(correlation)

print("\nDistance vs overcharge examples:")
print(
    affected[["distance_km", "difference"]]
    .sort_values("distance_km")
    .head(10)
)

print(
    affected[["distance_km", "difference"]]
    .sort_values("distance_km")
    .tail(10)
)