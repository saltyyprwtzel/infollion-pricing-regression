# Pricing Refactor Regression

## 1. Naive non-zero difference count

There are **16,000 orders** where `v2_total != v1_total`.

This is not a useful measure of genuine pricing regressions because the
`books` category had an intentional pricing change. In addition, small
cent-level differences are expected because the refactor changed the
order in which some numbers are added, resulting in harmless
floating-point rounding differences.

## 2. Genuine pricing regression

There are **985 orders** affected by a genuine pricing regression.

All 985 affected orders share the following input conditions:

- `category = fragile`
- `express = True`

The coupon value is not required for the regression. The affected
orders occur both with and without the `SAVE10` coupon.

The `books` category was excluded because its pricing change was
explicitly documented as intentional.

## 3. Total dollar amount overcharged

The total amount overcharged across the 985 affected orders is:

**$19,779.14**

This was calculated as:

`v2_total - v1_total`

for each affected order and then summed.

## 4. Sanity check

For orders that are not affected by the bug and are not in the
`books` category, the average:

`v1_total - v2_total`

is:

**$0.00022449**

The average absolute difference is:

**$0.00988265**

These differences are consistent with the expected small
floating-point/rounding noise. In contrast, the affected `fragile +
express` orders have much larger differences, ranging from **$5.08
to $34.98**, with an average difference of approximately **$20.08**.

This makes the affected population a distinct pattern rather than
normal numerical variation.

## 5. Bonus: likely code-level bug

Based on the observed input/output pattern, the refactored pricing
logic appears to be incorrectly applying a distance-dependent charge
when both `category = fragile` and `express = True`.

The overcharge has a very strong positive correlation with
`distance_km` (Pearson correlation ≈ **0.9946**), while other
non-books groups show only cent-level differences.

Without access to the pricing source code, the exact implementation
mistake cannot be confirmed.

## Investigation Process

- Loaded the CSV and verified the number of orders and available columns.
- Initially compared `v1_total` and `v2_total` directly and found 16,000 differing rows.
- Examined the distribution of differing rows by category and express status.
- Excluded the `books` category because its pricing change was explicitly documented as intentional.
- Calculated the actual price difference between the old and new pricing outputs.
- Examined the magnitude of the differences and found that most differences were within a few cents.
- Found a strong concentration of large differences in orders where `category = fragile` and `express = True`.
- Verified that all 985 orders in this group had substantial positive differences, rather than normal floating-point noise.
- Calculated the total overcharge for the affected population.
- Compared the affected population against the remaining orders to establish that the regression was a distinct pattern.