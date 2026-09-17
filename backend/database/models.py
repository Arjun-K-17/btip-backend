from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func

from database.connection import Base


# =========================================================
# User
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================================================
# Company
# =========================================================

class Company(Base):
    __tablename__ = "companies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    industry = Column(
        String(100)
    )

    owner_email = Column(
        String(150)
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================================================
# Financial Data
# =========================================================

class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    # -----------------------------------------------------
    # Financial Period
    # -----------------------------------------------------

    period = Column(
        String(50),
        nullable=True
    )

    # -----------------------------------------------------
    # Core Financial Information
    # -----------------------------------------------------

    revenue = Column(
        Float,
        default=0
    )

    expenses = Column(
        Float,
        default=0
    )

    profit = Column(
        Float,
        default=0
    )

    # -----------------------------------------------------
    # Balance Sheet
    # -----------------------------------------------------

    assets = Column(
        Float,
        default=0
    )

    liabilities = Column(
        Float,
        default=0
    )

    debt = Column(
        Float,
        default=0
    )

    equity = Column(
        Float,
        default=0
    )

    cash = Column(
        Float,
        default=0
    )

    # -----------------------------------------------------
    # Liquidity
    # -----------------------------------------------------

    current_assets = Column(
        Float,
        default=0
    )

    current_liabilities = Column(
        Float,
        default=0
    )

    # -----------------------------------------------------
    # Cash Flow
    # -----------------------------------------------------

    operating_cash_flow = Column(
        Float,
        default=0
    )

    investing_cash_flow = Column(
        Float,
        default=0
    )

    financing_cash_flow = Column(
        Float,
        default=0
    )

    # -----------------------------------------------------
    # Record Creation Time
    # -----------------------------------------------------

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================================================
# Analysis Result
# =========================================================

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    risk_score = Column(
        Float
    )

    risk_level = Column(
        String(30)
    )

    profit_margin = Column(
        Float
    )

    current_ratio = Column(
        Float
    )

    debt_to_equity = Column(
        Float
    )

    net_cash_flow = Column(
        Float
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================================================
# Recommendation
# =========================================================

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    title = Column(
        String(200)
    )

    description = Column(
        Text
    )

    priority = Column(
        String(30)
    )

    action = Column(
        Text
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================================================
# Alert
# =========================================================

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    title = Column(
        String(200)
    )

    message = Column(
        Text
    )

    severity = Column(
        String(30)
    )

    category = Column(
        String(100)
    )

    is_read = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )