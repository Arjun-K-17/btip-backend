import io
import re

import pandas as pd
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Company, FinancialData
from dataset_engine.dataset_profiler import profile_dataset


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


# =========================================================
# Column Aliases
# =========================================================

COLUMN_ALIASES = {
    "period": [
        "period", "date", "year", "month", "quarter", "financial_year",
        "fiscal_year", "fy", "reporting_period", "transaction_date",
        "invoice_date", "order_date", "sale_date", "sales_date",
        "admission_date", "discharge_date", "booking_date",
        "project_date", "production_date",
    ],
    "revenue": [
        "revenue", "sales", "sale", "net_sales", "total_sales",
        "sales_amount", "sales_value", "net_revenue", "total_revenue",
        "turnover", "operating_revenue", "gross_sales", "gross_revenue",
        "income", "total_income", "total_amount", "transaction_amount",
        "transaction_value", "order_amount", "order_value",
        "invoice_amount", "amount", "billing_amount", "bill_amount",
        "service_revenue", "project_revenue", "room_revenue",
        "treatment_revenue",
    ],
    "expenses": [
        "expenses", "expense", "total_expenses", "operating_expenses",
        "operating_expense", "total_cost", "total_costs", "costs",
        "operating_cost", "operating_costs", "cost",
        "cost_of_goods_sold", "cogs", "cost_of_sales", "business_expenses",
        "treatment_cost", "medical_cost", "material_cost", "production_cost",
        "labor_cost", "salary_cost", "staff_cost", "food_cost",
        "maintenance_cost", "operating_cost",
    ],
    "profit": [
        "profit", "net_profit", "net_income", "net_profit_loss",
        "profit_after_tax", "pat", "earnings", "profit_loss",
        "net_earnings", "operating_profit", "gross_profit",
        "ebit", "ebitda",
    ],
    "assets": ["assets", "total_assets", "asset", "total_asset"],
    "liabilities": [
        "liabilities", "total_liabilities", "liability", "total_liability"
    ],
    "debt": [
        "debt", "total_debt", "borrowings", "total_borrowings",
        "loans", "loan", "borrowed_funds", "borrowings_amount",
    ],
    "equity": [
        "equity", "shareholders_equity", "shareholder_equity",
        "owners_equity", "owner_equity", "net_worth",
        "share_capital", "total_equity",
    ],
    "cash": [
        "cash", "cash_balance", "cash_and_cash_equivalents",
        "cash_equivalents", "cash_on_hand", "bank_balance",
    ],
    "current_assets": [
        "current_assets", "total_current_assets", "current_asset"
    ],
    "current_liabilities": [
        "current_liabilities", "total_current_liabilities",
        "current_liability",
    ],
    "operating_cash_flow": [
        "operating_cash_flow", "cash_from_operations",
        "cash_flow_from_operations", "cfo", "operating_cf",
        "net_cash_from_operating_activities",
    ],
    "investing_cash_flow": [
        "investing_cash_flow", "cash_from_investing",
        "cash_flow_from_investing", "cfi", "investing_cf",
        "net_cash_from_investing_activities",
    ],
    "financing_cash_flow": [
        "financing_cash_flow", "cash_from_financing",
        "cash_flow_from_financing", "cff", "financing_cf",
        "net_cash_from_financing_activities",
    ],
    "quantity": [
        "quantity", "qty", "units", "units_sold",
        "quantity_sold", "number_of_units", "units_produced",
        "production_quantity", "patient_count", "number_of_patients",
        "patients", "orders", "order_count",
    ],
    "price_per_unit": [
        "price_per_unit", "unit_price", "price", "selling_price",
        "sale_price", "product_price", "rate", "unit_rate",
    ],
    "transaction_id": [
        "transaction_id", "transaction", "transaction_number",
        "invoice_id", "invoice_number", "order_id", "order_number",
        "sale_id", "receipt_id", "booking_id",
    ],
    "product_category": [
        "product_category", "product_type", "category",
        "product", "item_category", "item", "service_type",
    ],
}

ALIAS_LOOKUP = {
    re.sub(
        r"_+",
        "_",
        re.sub(
            r"[^a-z0-9]+",
            "_",
            str(alias).strip().lower().replace("&", " and "),
        ),
    ).strip("_"): standard
    for standard, aliases in COLUMN_ALIASES.items()
    for alias in aliases
}


# =========================================================
# Utility Functions
# =========================================================

def normalize_column_name(column_name):
    value = str(column_name).strip().lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_")


def detect_financial_columns(dataframe):
    detected = {}

    for column in dataframe.columns:
        normalized = normalize_column_name(column)
        standard = ALIAS_LOOKUP.get(normalized)

        if standard and standard not in detected:
            detected[standard] = column

    return detected


def safe_float(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if isinstance(value, str):
        value = (
            value.strip()
            .replace(",", "")
            .replace("₹", "")
            .replace("$", "")
            .replace("€", "")
            .replace("£", "")
            .replace("%", "")
        )

        if not value:
            return None

        if value.startswith("(") and value.endswith(")"):
            value = "-" + value[1:-1]

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_period(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")

    if hasattr(value, "strftime"):
        try:
            return value.strftime("%Y-%m-%d")
        except Exception:
            pass

    text = str(value).strip()

    if not text:
        return None

    if re.fullmatch(r"\d{4}\.0", text):
        return text[:4]

    return text


def detect_period_column(dataframe, detected_columns):
    if "period" in detected_columns:
        return detected_columns["period"]

    candidates = []

    for column in dataframe.columns:
        if normalize_column_name(column) in ALIAS_LOOKUP:
            continue

        series = dataframe[column]

        if series.empty:
            continue

        numeric = pd.to_numeric(series, errors="coerce")
        numeric_valid = numeric.dropna().between(1900, 2100).mean()

        if numeric_valid >= 0.6:
            candidates.append((column, numeric_valid))
            continue

        dates = pd.to_datetime(series, errors="coerce")
        date_valid = dates.notna().mean()

        if date_valid >= 0.6:
            candidates.append((column, date_valid))

    if not candidates:
        return None

    return max(candidates, key=lambda item: item[1])[0]


def read_uploaded_file(file_bytes, filename):
    try:
        filename_lower = (filename or "").lower()

        if filename_lower.endswith(".csv"):
            return pd.read_csv(io.BytesIO(file_bytes))

        if filename_lower.endswith(".xlsx"):
            return pd.read_excel(io.BytesIO(file_bytes))

        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a CSV or XLSX file.",
        )

    except HTTPException:
        raise

    except Exception as exc:
        print("Dataset reading error:", exc)

        raise HTTPException(
            status_code=400,
            detail=(
                "Unable to read the uploaded dataset. "
                "Please verify that the file is valid."
            ),
        )


def clean_dataframe(dataframe):
    dataframe = dataframe.copy()

    dataframe = dataframe.dropna(
        axis=1,
        how="all",
    )

    dataframe = dataframe.dropna(
        axis=0,
        how="all",
    )

    return dataframe


# =========================================================
# Flexible Dataset Detection
# =========================================================

def is_transaction_dataset(detected_columns):
    return (
        "transaction_id" in detected_columns
        and (
            "quantity" in detected_columns
            or "price_per_unit" in detected_columns
            or "revenue" in detected_columns
        )
    )


def derive_transaction_revenue(dataframe, detected_columns):
    """
    Derive transaction revenue from Quantity × Price when a
    direct amount/revenue field is unavailable.
    """
    if "revenue" in detected_columns:
        return dataframe

    if {
        "quantity",
        "price_per_unit",
    }.issubset(detected_columns):
        quantity = dataframe[
            detected_columns["quantity"]
        ].apply(safe_float)

        price = dataframe[
            detected_columns["price_per_unit"]
        ].apply(safe_float)

        dataframe = dataframe.copy()

        dataframe["__btip_derived_revenue"] = (
            quantity * price
        )

        detected_columns["revenue"] = (
            "__btip_derived_revenue"
        )

    return dataframe


def apply_profiler_mappings(
    dataframe,
    detected_columns,
    profile,
):
    """
    Use the intelligent dataset profiler to supplement the
    existing financial/transaction aliases.
    """
    primary_fields = (
        profile.get("fields", {})
        .get("primary", {})
    )

    field_map = {
        "revenue": "revenue",
        "expenses": "expenses",
        "profit": "profit",
        "assets": "assets",
        "liabilities": "liabilities",
        "debt": "debt",
        "equity": "equity",
        "cash": "cash",
        "date": "period",
        "quantity": "quantity",
        "price": "price_per_unit",
        "customer": "customer",
        "product": "product_category",
    }

    for profiler_field, standard_field in field_map.items():
        source_column = primary_fields.get(profiler_field)

        if (
            source_column
            and standard_field not in detected_columns
            and source_column in dataframe.columns
        ):
            detected_columns[standard_field] = source_column

    return detected_columns


def build_flexible_evaluation(
    dataframe,
    detected_columns,
    profile,
    transaction_dataset,
):
    """
    Evaluate any dataset without requiring Sales/Revenue.

    A dataset is considered acceptable when it contains useful
    financial OR operational information. It is not rejected
    merely because financial values are unavailable.
    """
    primary = (
        profile.get("fields", {})
        .get("primary", {})
    )

    financial_fields = [
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
        if field in detected_columns or field in primary
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
        if field in primary or field in detected_columns
    ]

    measurable_numeric_columns = []

    for column in dataframe.columns:
        numeric = dataframe[column].apply(safe_float)

        if numeric.notna().sum() > 0:
            measurable_numeric_columns.append(column)

    warnings = []

    if "revenue" not in detected_columns:
        warnings.append(
            "Revenue/Sales was not directly detected. "
            "BTIP will use available operational or cost metrics "
            "and will not invent revenue."
        )

    if "expenses" not in detected_columns:
        warnings.append(
            "Expenses/Cost was not directly detected. "
            "Profitability analysis may be limited."
        )

    if "period" not in detected_columns:
        warnings.append(
            "No period/date field was detected. "
            "Time-series forecasting may be limited."
        )

    if not financial_fields:
        warnings.append(
            "No standard financial fields were detected. "
            "Financial health, crisis, and leverage calculations "
            "may be unavailable."
        )

    if not operational_fields:
        warnings.append(
            "No recognized industry-specific operational fields "
            "were detected."
        )

    if not measurable_numeric_columns:
        warnings.append(
            "No numeric business measurements were detected. "
            "Only dataset inspection and profiling can be performed."
        )

    compatibility = profile.get("compatibility", {})

    available_modules = compatibility.get(
        "available_modules",
        ["Dataset Inspection", "Data Profiling"],
    )

    dataset_info = profile.get("dataset", {})

    if transaction_dataset:
        dataset_type = "transaction"
    else:
        dataset_type = dataset_info.get(
            "type",
            "general_business",
        )

    return {
        "status": "ready",
        "sales_revenue_detected": "revenue" in detected_columns,
        "period_detected": "period" in detected_columns,
        "dataset_type": dataset_type,
        "industry_detected": profile.get(
            "industry",
            {},
        ).get("detected", "unknown"),
        "industry_confidence": profile.get(
            "industry",
            {},
        ).get("confidence", "low"),
        "financial_columns_detected": financial_fields,
        "operational_fields_detected": operational_fields,
        "available_modules": available_modules,
        "derived_fields": [],
        "warnings": warnings,
    }


# =========================================================
# Financial Record Conversion
# =========================================================

def build_financial_record(
    row,
    detected_columns,
    period_column,
):
    def get_value(field):
        column = detected_columns.get(field)

        if not column:
            return None

        return safe_float(
            row.get(column)
        )

    revenue = get_value("revenue")
    expenses = get_value("expenses")
    profit = get_value("profit")

    if (
        profit is None
        and revenue is not None
        and expenses is not None
    ):
        profit = revenue - expenses

    return {
        "period": (
            normalize_period(
                row.get(period_column)
            )
            if period_column
            else None
        ),
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "assets": get_value("assets"),
        "liabilities": get_value("liabilities"),
        "debt": get_value("debt"),
        "equity": get_value("equity"),
        "cash": get_value("cash"),
        "current_assets": get_value("current_assets"),
        "current_liabilities": get_value(
            "current_liabilities"
        ),
        "operating_cash_flow": get_value(
            "operating_cash_flow"
        ),
        "investing_cash_flow": get_value(
            "investing_cash_flow"
        ),
        "financing_cash_flow": get_value(
            "financing_cash_flow"
        ),
    }


def aggregate_transaction_dataframe(
    dataframe,
    detected_columns,
    period_column,
):
    """
    Aggregate transaction-level revenue by period.

    Other non-financial transaction fields are intentionally not
    forced into the FinancialData table.
    """
    if (
        not period_column
        or "revenue" not in detected_columns
    ):
        return dataframe

    revenue_column = detected_columns["revenue"]

    working = dataframe.copy()

    working["__btip_revenue_numeric"] = (
        working[revenue_column].apply(safe_float)
    )

    working["__btip_period"] = (
        working[period_column].apply(
            normalize_period
        )
    )

    working = working.dropna(
        subset=["__btip_revenue_numeric"]
    )

    if working.empty:
        return working

    grouped = (
        working.groupby(
            "__btip_period",
            dropna=False,
        )["__btip_revenue_numeric"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "__btip_revenue_numeric":
                    "__btip_aggregated_revenue"
            }
        )
    )

    return grouped


def build_dataset_profile(
    dataframe,
    detected_columns,
    profile,
    transaction_dataset,
):
    dataset_info = profile.get(
        "dataset",
        {},
    )

    industry_info = profile.get(
        "industry",
        {},
    )

    return {
        "dataset_type": (
            "transaction"
            if transaction_dataset
            else dataset_info.get(
                "type",
                "general_business",
            )
        ),
        "rows": int(len(dataframe)),
        "columns": int(len(dataframe.columns)),
        "transaction_data_detected": transaction_dataset,
        "industry_detected": industry_info.get(
            "detected",
            "unknown",
        ),
        "industry_confidence": industry_info.get(
            "confidence",
            "low",
        ),
        "recognized_fields": profile.get(
            "fields",
            {},
        ).get(
            "primary",
            {},
        ),
        "data_quality": profile.get(
            "data_quality",
            {},
        ),
        "compatibility": profile.get(
            "compatibility",
            {},
        ),
        "description": (
            "Transaction-level business data detected."
            if transaction_dataset
            else (
                "Financial or business dataset detected."
                if dataset_info.get(
                    "has_financial_fields",
                    False,
                )
                else "Industry or operational dataset detected."
            )
        ),
    }


# =========================================================
# Upload Dataset
# =========================================================

@router.post("/upload")
async def upload_dataset(
    company_name: str = Form(...),
    industry: str = Form("Unknown"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # Validate Company
    # -----------------------------------------------------

    company_name = (
        company_name or ""
    ).strip()

    if not company_name:
        raise HTTPException(
            status_code=400,
            detail="Company name is required.",
        )

    # -----------------------------------------------------
    # Validate File
    # -----------------------------------------------------

    filename = (
        file.filename or ""
    ).strip()

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a dataset file.",
        )

    if not filename.lower().endswith(
        (".csv", ".xlsx")
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format. "
                "Please upload a CSV or XLSX file."
            ),
        )

    # -----------------------------------------------------
    # Read Dataset
    # -----------------------------------------------------

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    dataframe = clean_dataframe(
        read_uploaded_file(
            file_bytes,
            filename,
        )
    )

    if dataframe.empty:
        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded dataset contains "
                "no usable records."
            ),
        )

    if len(dataframe.columns) == 0:
        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded dataset contains "
                "no usable columns."
            ),
        )

    # -----------------------------------------------------
    # Preserve Original Columns
    # -----------------------------------------------------

    original_columns = list(
        dataframe.columns
    )

    # Normalize names for internal processing.
    dataframe = dataframe.rename(
        columns={
            column: normalize_column_name(column)
            for column in original_columns
        }
    )

    # -----------------------------------------------------
    # Intelligent Dataset Profiling
    # -----------------------------------------------------

    try:
        profile = profile_dataset(
            dataframe,
            supplied_industry=industry,
        )
    except Exception as exc:
        print(
            "Dataset profiling error:",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail=(
                "Unable to understand the uploaded dataset. "
                "Please verify that the file contains readable "
                "rows and columns."
            ),
        )

    # -----------------------------------------------------
    # Existing BTIP Mapping + Profiler Mapping
    # -----------------------------------------------------

    detected_columns = (
        detect_financial_columns(
            dataframe
        )
    )

    detected_columns = (
        apply_profiler_mappings(
            dataframe,
            detected_columns,
            profile,
        )
    )

    # -----------------------------------------------------
    # Transaction Revenue Derivation
    # -----------------------------------------------------

    transaction_dataset = (
        is_transaction_dataset(
            detected_columns
        )
    )

    dataframe = derive_transaction_revenue(
        dataframe,
        detected_columns,
    )

    transaction_dataset = (
        transaction_dataset
        or (
            {
                "transaction_id",
                "quantity",
                "revenue",
            }.issubset(
                detected_columns
            )
        )
    )

    # -----------------------------------------------------
    # Period Detection
    # -----------------------------------------------------

    period_column = detect_period_column(
        dataframe,
        detected_columns,
    )

    if period_column:
        detected_columns["period"] = (
            period_column
        )

    # -----------------------------------------------------
    # Flexible Evaluation
    # -----------------------------------------------------

    evaluation = build_flexible_evaluation(
        dataframe,
        detected_columns,
        profile,
        transaction_dataset,
    )

    # -----------------------------------------------------
    # Find / Create Company
    # -----------------------------------------------------

    company = (
        db.query(Company)
        .filter(
            Company.name == company_name
        )
        .first()
    )

    if company:
        if (
            industry
            and industry.strip()
            and industry.strip().lower()
            != "unknown"
        ):
            company.industry = (
                industry.strip()
            )

    else:
        company = Company(
            name=company_name,
            industry=(
                industry.strip()
                if industry
                else "Unknown"
            ),
        )

        db.add(company)
        db.commit()
        db.refresh(company)

    # -----------------------------------------------------
    # Store Financially Compatible Records
    # -----------------------------------------------------

    records_dataframe = dataframe
    storage_columns = detected_columns
    storage_period_column = (
        period_column
    )

    if (
        transaction_dataset
        and period_column
        and "revenue" in detected_columns
    ):
        aggregated = (
            aggregate_transaction_dataframe(
                dataframe,
                detected_columns,
                period_column,
            )
        )

        if not aggregated.empty:
            records_dataframe = aggregated

            storage_columns = {
                "revenue":
                    "__btip_aggregated_revenue",
                "period":
                    "__btip_period",
            }

            storage_period_column = (
                "__btip_period"
            )

    records_to_add = []

    # Only create FinancialData records when at least
    # one recognized financial value exists. This prevents
    # operational fields from being turned into fake
    # financial values.
    financial_storage_fields = {
        "revenue",
        "expenses",
        "profit",
        "assets",
        "liabilities",
        "debt",
        "equity",
        "cash",
        "current_assets",
        "current_liabilities",
        "operating_cash_flow",
        "investing_cash_flow",
        "financing_cash_flow",
    }

    for _, row in records_dataframe.iterrows():
        financial_record = (
            build_financial_record(
                row,
                storage_columns,
                storage_period_column,
            )
        )

        has_financial_value = any(
            financial_record.get(field)
            is not None
            for field in financial_storage_fields
        )

        if has_financial_value:
            records_to_add.append(
                FinancialData(
                    company_id=company.id,
                    **financial_record,
                )
            )

    # -----------------------------------------------------
    # Save Financial Records When Available
    # -----------------------------------------------------

    try:
        if records_to_add:
            db.add_all(
                records_to_add
            )

        db.commit()

    except Exception as exc:
        db.rollback()

        print(
            "Dataset database error:",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to save the uploaded "
                "dataset."
            ),
        )

    # -----------------------------------------------------
    # Final Profile / Evaluation
    # -----------------------------------------------------

    dataset_profile = (
        build_dataset_profile(
            dataframe,
            detected_columns,
            profile,
            transaction_dataset,
        )
    )

    detected_standard_fields = sorted(
        set(
            detected_columns.keys()
        )
    )

    evaluation_result = {
        **evaluation,
        "status": "ready",
        "message": (
            "Dataset evaluated successfully. "
            "BTIP identified the available business "
            "and operational information."
        ),
        "financial_columns_detected": (
            detected_standard_fields
        ),
        "records_stored": len(
            records_to_add
        ),
        "profile": dataset_profile,
    }

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return {
        "message": (
            "Dataset uploaded and evaluated "
            "successfully."
        ),
        "company": {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
        },
        "dataset": {
            "filename": filename,
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "records_added": len(
                records_to_add
            ),
            "original_columns": (
                original_columns
            ),
            "normalized_columns": list(
                dataframe.columns
            ),
            "financial_columns_detected": (
                detected_standard_fields
            ),
            "period_column": (
                period_column
            ),
            "dataset_type": (
                "transaction"
                if transaction_dataset
                else profile.get(
                    "dataset",
                    {},
                ).get(
                    "type",
                    "general_business",
                )
            ),
            "industry_detected": profile.get(
                "industry",
                {},
            ).get(
                "detected",
                "unknown",
            ),
            "industry_confidence": profile.get(
                "industry",
                {},
            ).get(
                "confidence",
                "low",
            ),
            "profile": dataset_profile,
        },
        "evaluation": evaluation_result,
    }
