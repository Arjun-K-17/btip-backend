import re
import pandas as pd


# =========================================================
# Industry / Field Signatures
# =========================================================

INDUSTRY_SIGNATURES = {
    "retail": [
        "retail",
        "product",
        "product_category",
        "quantity",
        "price",
        "transaction",
        "customer_id",
        "store",
        "sales",
        "units_sold",
        "total_amount",
    ],
    "hospitality": [
        "cafe",
        "restaurant",
        "hotel",
        "menu",
        "food",
        "beverage",
        "room",
        "booking",
        "guest",
        "table",
        "order",
        "occupancy",
    ],
    "healthcare": [
        "hospital",
        "patient",
        "diagnosis",
        "treatment",
        "doctor",
        "physician",
        "admission",
        "discharge",
        "medical",
        "ward",
        "bed",
        "length_of_stay",
    ],
    "manufacturing": [
        "manufacturing",
        "production",
        "machine",
        "factory",
        "units_produced",
        "raw_material",
        "material_cost",
        "production_cost",
        "defect",
        "downtime",
        "inventory",
        "supplier",
    ],
    "it": [
        "software",
        "project",
        "developer",
        "employee",
        "client",
        "ticket",
        "sprint",
        "hours",
        "billable_hours",
        "cloud",
        "subscription",
        "license",
    ],
    "finance": [
        "revenue",
        "profit",
        "expense",
        "asset",
        "liability",
        "debt",
        "equity",
        "cash_flow",
        "balance_sheet",
        "income_statement",
        "loan",
        "interest",
    ],
}


FIELD_SIGNATURES = {
    "revenue": [
        "revenue",
        "sales",
        "sale",
        "net_sales",
        "total_sales",
        "sales_amount",
        "sales_value",
        "net_revenue",
        "total_revenue",
        "turnover",
        "operating_revenue",
        "income",
        "total_amount",
        "amount",
        "transaction_value",
        "order_value",
        "bill_amount",
        "billing_amount",
    ],
    "expenses": [
        "expenses",
        "expense",
        "total_expenses",
        "operating_expenses",
        "operating_expense",
        "total_cost",
        "total_costs",
        "costs",
        "operating_cost",
        "operating_costs",
        "cost",
        "treatment_cost",
        "material_cost",
        "production_cost",
        "labor_cost",
        "salary_cost",
        "operating_cost",
    ],
    "profit": [
        "profit",
        "net_profit",
        "net_income",
        "profit_after_tax",
        "earnings",
        "profit_loss",
        "net_profit_loss",
    ],
    "quantity": [
        "quantity",
        "qty",
        "units",
        "units_sold",
        "quantity_sold",
        "units_produced",
        "volume",
        "patient_count",
        "patients",
        "number_of_patients",
    ],
    "price": [
        "price",
        "price_per_unit",
        "unit_price",
        "selling_price",
        "rate",
        "unit_rate",
        "cost_per_unit",
    ],
    "assets": [
        "assets",
        "total_assets",
        "asset",
    ],
    "liabilities": [
        "liabilities",
        "total_liabilities",
        "liability",
    ],
    "debt": [
        "debt",
        "total_debt",
        "borrowings",
        "total_borrowings",
        "loans",
        "loan",
    ],
    "equity": [
        "equity",
        "shareholders_equity",
        "shareholder_equity",
        "owners_equity",
        "owner_equity",
        "net_worth",
        "share_capital",
    ],
    "cash": [
        "cash",
        "cash_balance",
        "cash_and_cash_equivalents",
        "cash_equivalents",
        "cash_on_hand",
        "bank_balance",
    ],
    "date": [
        "date",
        "period",
        "year",
        "month",
        "quarter",
        "financial_year",
        "fiscal_year",
        "reporting_period",
        "admission_date",
        "discharge_date",
        "transaction_date",
        "order_date",
        "booking_date",
    ],
    "customer": [
        "customer",
        "customer_id",
        "client",
        "client_id",
        "consumer",
        "buyer",
    ],
    "product": [
        "product",
        "product_id",
        "product_category",
        "category",
        "item",
        "item_name",
        "service",
        "service_type",
    ],
    "patient": [
        "patient",
        "patient_id",
        "diagnosis",
        "treatment",
        "admission",
        "discharge",
        "doctor",
        "physician",
    ],
    "production": [
        "production",
        "units_produced",
        "output",
        "machine",
        "downtime",
        "defect",
        "defects",
        "raw_material",
        "material",
    ],
    "project": [
        "project",
        "project_id",
        "developer",
        "sprint",
        "ticket",
        "billable_hours",
        "hours_worked",
        "employee",
    ],
}


def normalize_column_name(column_name):
    """Convert a real-world column name into snake_case."""
    value = str(column_name).strip().lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def normalized_columns(dataframe):
    """Return original column -> normalized column mapping."""
    return {
        column: normalize_column_name(column)
        for column in dataframe.columns
    }


def score_keyword_matches(normalized_names, signatures):
    """Score how strongly a dataset matches a list of keywords."""
    score = 0
    matched = []

    for name in normalized_names:
        for keyword in signatures:
            keyword_normalized = normalize_column_name(keyword)

            if name == keyword_normalized:
                score += 3
                matched.append(name)
                break

            if keyword_normalized in name or name in keyword_normalized:
                score += 1
                matched.append(name)
                break

    return score, sorted(set(matched))


def detect_industry(dataframe, supplied_industry=None):
    """
    Detect the most likely industry from column names.

    A user-supplied industry is treated as supporting context,
    not as a replacement for dataset inspection.
    """
    mapping = normalized_columns(dataframe)
    names = list(mapping.values())

    scores = {}

    for industry, signatures in INDUSTRY_SIGNATURES.items():
        score, matched = score_keyword_matches(names, signatures)
        scores[industry] = {
            "score": score,
            "matched_fields": matched,
        }

    supplied = normalize_column_name(supplied_industry or "")

    if supplied:
        for industry in scores:
            if supplied == industry or supplied in industry or industry in supplied:
                scores[industry]["score"] += 4

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1]["score"],
        reverse=True,
    )

    if not ranked or ranked[0][1]["score"] == 0:
        return {
            "industry": "unknown",
            "confidence": "low",
            "scores": scores,
            "matched_fields": [],
        }

    best_industry, best_result = ranked[0]

    if best_result["score"] >= 8:
        confidence = "high"
    elif best_result["score"] >= 4:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "industry": best_industry,
        "confidence": confidence,
        "scores": scores,
        "matched_fields": best_result["matched_fields"],
    }


def detect_fields(dataframe):
    """
    Detect common business, operational, and financial concepts.

    More than one uploaded column can represent the same concept;
    the first strongest match is selected as the primary field.
    """
    mapping = normalized_columns(dataframe)
    detected = {}
    matches = {}

    for field, signatures in FIELD_SIGNATURES.items():
        candidates = []

        for original, normalized in mapping.items():
            for signature in signatures:
                signature_normalized = normalize_column_name(signature)

                if normalized == signature_normalized:
                    candidates.append((3, original))
                    break

                if (
                    signature_normalized in normalized
                    or normalized in signature_normalized
                ):
                    candidates.append((1, original))
                    break

        candidates.sort(key=lambda item: (-item[0], str(item[1])))

        if candidates:
            detected[field] = candidates[0][1]
            matches[field] = [column for _, column in candidates]

    return {
        "primary": detected,
        "matches": matches,
    }


def detect_date_like_columns(dataframe):
    """Find columns containing a useful proportion of date-like values."""
    candidates = []

    for column in dataframe.columns:
        series = dataframe[column]

        if series.empty:
            continue

        parsed = pd.to_datetime(series, errors="coerce")
        valid_ratio = parsed.notna().mean()

        if valid_ratio >= 0.6:
            candidates.append(
                {
                    "column": column,
                    "valid_ratio": round(float(valid_ratio), 3),
                }
            )

    candidates.sort(key=lambda item: item["valid_ratio"], reverse=True)
    return candidates


def classify_dataset(dataframe, detected_fields, industry):
    """
    Classify the dataset by structure rather than requiring
    a particular financial column.
    """
    rows = len(dataframe)
    columns = len(dataframe.columns)

    primary = detected_fields["primary"]

    has_financial = any(
        field in primary
        for field in [
            "revenue",
            "expenses",
            "profit",
            "assets",
            "liabilities",
            "debt",
            "equity",
            "cash",
        ]
    )

    has_transaction = any(
        field in primary
        for field in [
            "quantity",
            "price",
            "customer",
            "product",
        ]
    )

    if has_financial and has_transaction:
        dataset_type = "financial_transactional"
    elif has_financial:
        dataset_type = "financial"
    elif has_transaction:
        dataset_type = "transactional"
    elif industry in ["healthcare", "manufacturing", "it", "hospitality"]:
        dataset_type = "industry_operational"
    else:
        dataset_type = "general_business"

    return {
        "type": dataset_type,
        "rows": rows,
        "columns": columns,
        "has_financial_fields": has_financial,
        "has_transaction_fields": has_transaction,
    }


def determine_compatibility(detected_fields, dataset_type):
    """
    Determine what level of BTIP analysis is supported.

    This does not reject datasets. It describes what BTIP can
    reliably calculate from the available information.
    """
    primary = detected_fields["primary"]

    financial_core = [
        field
        for field in [
            "revenue",
            "expenses",
            "profit",
            "assets",
            "liabilities",
            "debt",
            "equity",
            "cash",
        ]
        if field in primary
    ]

    operational_fields = [
        field
        for field in [
            "quantity",
            "price",
            "customer",
            "product",
            "patient",
            "production",
            "project",
        ]
        if field in primary
    ]

    has_revenue = "revenue" in primary
    has_expenses = "expenses" in primary
    has_profit = "profit" in primary
    has_date = "date" in primary

    if has_revenue and (has_profit or has_expenses):
        level = "high"
    elif has_revenue or financial_core or operational_fields:
        level = "partial"
    else:
        level = "limited"

    available_modules = ["Dataset Inspection", "Data Profiling"]

    if financial_core or has_revenue:
        available_modules.extend(
            [
                "Financial Analysis",
                "Business Health",
                "Crisis Detection",
                "Recommendations",
            ]
        )

    if has_date:
        available_modules.append("Forecasting")

    if has_revenue or has_expenses or operational_fields:
        available_modules.append("Scenario Analysis")

    warnings = []

    if not has_revenue:
        warnings.append(
            "Revenue/Sales is not directly available. Financial revenue analysis may be limited."
        )

    if not has_expenses:
        warnings.append(
            "Expenses/Cost is not directly available. Profitability analysis may be limited."
        )

    if not has_date:
        warnings.append(
            "No date/period field was detected. Time-series forecasting may be limited."
        )

    return {
        "level": level,
        "financial_fields_available": financial_core,
        "operational_fields_available": operational_fields,
        "available_modules": list(dict.fromkeys(available_modules)),
        "warnings": warnings,
    }


def profile_dataset(dataframe, supplied_industry=None):
    """
    Main entry point.

    Returns a complete dataset profile without requiring the
    dataset to contain a Revenue/Sales column.
    """
    if dataframe is None:
        raise ValueError("A dataframe is required.")

    if dataframe.empty:
        raise ValueError("The dataset contains no usable records.")

    dataframe = dataframe.dropna(axis=1, how="all").dropna(axis=0, how="all")

    if dataframe.empty or len(dataframe.columns) == 0:
        raise ValueError("The dataset contains no usable rows or columns.")

    field_result = detect_fields(dataframe)
    industry_result = detect_industry(dataframe, supplied_industry)
    date_candidates = detect_date_like_columns(dataframe)

    if "date" not in field_result["primary"] and date_candidates:
        field_result["primary"]["date"] = date_candidates[0]["column"]
        field_result["matches"].setdefault(
            "date",
            [item["column"] for item in date_candidates],
        )

    dataset_result = classify_dataset(
        dataframe,
        field_result,
        industry_result["industry"],
    )

    compatibility = determine_compatibility(
        field_result,
        dataset_result["type"],
    )

    missing_values = int(dataframe.isna().sum().sum())
    duplicate_rows = int(dataframe.duplicated().sum())

    return {
        "status": "profiled",
        "dataset": dataset_result,
        "industry": {
            "detected": industry_result["industry"],
            "confidence": industry_result["confidence"],
            "matched_fields": industry_result["matched_fields"],
        },
        "fields": {
            "primary": field_result["primary"],
            "matches": field_result["matches"],
        },
        "data_quality": {
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
        },
        "date_candidates": date_candidates,
        "compatibility": compatibility,
        "columns": [
            {
                "original": original,
                "normalized": normalized,
                "data_type": str(dataframe[original].dtype),
            }
            for original, normalized in normalized_columns(dataframe).items()
        ],
    }
