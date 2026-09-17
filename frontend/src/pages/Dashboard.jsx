import { useEffect, useState } from "react";

function Dashboard({ companyId }) {
  // =====================================================
  // State
  // =====================================================

  const [dashboard, setDashboard] = useState(null);
  const [loadingDashboard, setLoadingDashboard] = useState(false);

  const [error, setError] = useState("");

  // =====================================================
  // API URLs
  // =====================================================

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  // =====================================================
  // Load Dashboard
  // =====================================================

  const fetchDashboard = async (companyId) => {
    if (!companyId) {
      setDashboard(null);
      return;
    }

    try {
      setLoadingDashboard(true);
      setError("");

      const response = await fetch(
        `${API_BASE_URL}/dashboard/${companyId}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : `Unable to load dashboard data. Server returned ${response.status}.`
        );
      }

      setDashboard(data);
    } catch (err) {
      console.error(
        "Dashboard loading error:",
        err
      );

      setDashboard(null);

      setError(
        err.message ||
          "Unable to load dashboard data."
      );
    } finally {
      setLoadingDashboard(false);
    }
  };

  // =====================================================
  // Load Dashboard When Company Changes
  // =====================================================

  useEffect(() => {
    setDashboard(null);
    setError("");

    if (companyId) {
      fetchDashboard(companyId);
    }
  }, [companyId]);

  // =====================================================
  // Refresh
  // =====================================================

  const handleRefresh = async () => {
    if (companyId) {
      await fetchDashboard(companyId);
    }
  };

  // =====================================================
  // Formatting Functions
  // =====================================================

  const formatCurrency = (value) => {
    if (
      value === null ||
      value === undefined ||
      isNaN(value)
    ) {
      return "N/A";
    }

    return `₹${Number(value).toLocaleString(
      "en-IN",
      {
        maximumFractionDigits: 0,
      }
    )}`;
  };

  const formatNumber = (
    value,
    decimals = 2
  ) => {
    if (
      value === null ||
      value === undefined ||
      isNaN(value)
    ) {
      return "N/A";
    }

    return Number(value).toFixed(decimals);
  };

  const formatPercentage = (value) => {
    if (
      value === null ||
      value === undefined ||
      isNaN(value)
    ) {
      return "N/A";
    }

    return `${Number(value).toFixed(2)}%`;
  };

  // =====================================================
  // No Company Selected
  // =====================================================

  if (!companyId) {
    return (
      <div className="dashboard-page">

        <div className="dashboard-error">

          <div className="error-icon">
            !
          </div>

          <h3>
            No Company Selected
          </h3>

          <p>
            Upload a financial dataset first,
            then select the created company
            to view its dashboard.
          </p>

        </div>

      </div>
    );
  }

  // =====================================================
  // Dashboard Loading
  // =====================================================

  if (
    loadingDashboard &&
    !dashboard
  ) {
    return (
      <div className="dashboard-page">

        <div className="dashboard-header">

          <div>

            <p className="dashboard-eyebrow">
              BUSINESS INTELLIGENCE
            </p>

            <h2>
              Financial Dashboard
            </h2>

          </div>

        </div>

        <div className="dashboard-loading">

          <div className="loading-spinner"></div>

          <h3>
            Loading Financial Data...
          </h3>

          <p>
            Preparing the selected company's
            financial overview.
          </p>

        </div>

      </div>
    );
  }

  // =====================================================
  // Safety Check
  // =====================================================

  if (!dashboard) {
    return null;
  }

  // =====================================================
  // Data Extraction
  // =====================================================

  const company =
    dashboard.company || {};

  const financial =
    dashboard.financial || {};

  const risk =
    dashboard.risk || {};

  const recommendations =
    dashboard.recommendations || [];

  const alerts =
    dashboard.alerts || [];

  // =====================================================
  // Risk Styling
  // =====================================================

  const riskLevel = String(
    risk.risk_level || "N/A"
  ).toLowerCase();

  let riskClass = "risk-neutral";

  if (
    riskLevel === "low" ||
    riskLevel === "safe"
  ) {
    riskClass = "risk-low";
  } else if (
    riskLevel === "medium" ||
    riskLevel === "moderate"
  ) {
    riskClass = "risk-medium";
  } else if (
    riskLevel === "high" ||
    riskLevel === "critical"
  ) {
    riskClass = "risk-high";
  }

  // =====================================================
  // Profit Status
  // =====================================================

  const profit =
    Number(financial.profit || 0);

  const profitStatus =
    profit > 0
      ? "Positive"
      : profit < 0
      ? "Negative"
      : "Break-even";

  // =====================================================
  // Cash Flow Status
  // =====================================================

  const netCashFlow =
    Number(financial.net_cash_flow || 0);

  const cashFlowStatus =
    netCashFlow > 0
      ? "Positive"
      : netCashFlow < 0
      ? "Negative"
      : "Neutral";

  // =====================================================
  // Render
  // =====================================================

  return (
    <div className="dashboard-page">

      {/* =================================================
          Dashboard Header
      ================================================= */}

      <div className="dashboard-header">

        <div>

          <p className="dashboard-eyebrow">
            BUSINESS INTELLIGENCE
          </p>

          <h2>
            Financial Dashboard
          </h2>

          <p className="dashboard-subtitle">
            Monitor financial health, risk, and
            turnaround opportunities.
          </p>

        </div>

        <div className="dashboard-header-actions">

          {/* Refresh */}

          <button
            className="dashboard-refresh-button"
            onClick={handleRefresh}
            disabled={loadingDashboard}
          >
            {loadingDashboard
              ? "↻ Loading..."
              : "↻ Refresh"}
          </button>

        </div>

      </div>

      {/* =================================================
          Company Banner
      ================================================= */}

      <div className="company-banner">

        <div className="company-avatar">

          {company.name
            ? company.name
                .charAt(0)
                .toUpperCase()
            : "C"}

        </div>

        <div className="company-details">

          <h3>
            {company.name ||
              "Company"}
          </h3>

          <p>
            {company.industry ||
              "Industry not specified"}
          </p>

        </div>

        <div className="company-id">

          Company ID:{" "}

          <strong>
            {company.id}
          </strong>

        </div>

      </div>

      {/* =================================================
          Error Notification
      ================================================= */}

      {error && (
        <div className="dashboard-inline-error">
          {error}
        </div>
      )}

      {/* =================================================
          KPI Cards
      ================================================= */}

      <div className="dashboard-kpi-grid">

        {/* Revenue */}

        <div className="dashboard-kpi-card">

          <div className="kpi-card-top">

            <span className="kpi-label">
              Revenue
            </span>

            <span className="kpi-icon">
              ₹
            </span>

          </div>

          <h3>
            {formatCurrency(
              financial.revenue
            )}
          </h3>

          <p className="kpi-description">
            Total recorded revenue
          </p>

        </div>

        {/* Expenses */}

        <div className="dashboard-kpi-card">

          <div className="kpi-card-top">

            <span className="kpi-label">
              Expenses
            </span>

            <span className="kpi-icon">
              −
            </span>

          </div>

          <h3>
            {formatCurrency(
              financial.expenses
            )}
          </h3>

          <p className="kpi-description">
            Total operating expenses
          </p>

        </div>

        {/* Profit */}

        <div className="dashboard-kpi-card">

          <div className="kpi-card-top">

            <span className="kpi-label">
              Net Profit
            </span>

            <span className="kpi-icon">
              ↗
            </span>

          </div>

          <h3>
            {formatCurrency(
              financial.profit
            )}
          </h3>

          <p className="kpi-description">
            {profitStatus} profitability
          </p>

        </div>

        {/* Cash */}

        <div className="dashboard-kpi-card">

          <div className="kpi-card-top">

            <span className="kpi-label">
              Cash
            </span>

            <span className="kpi-icon">
              $
            </span>

          </div>

          <h3>
            {formatCurrency(
              financial.cash
            )}
          </h3>

          <p className="kpi-description">
            Available cash position
          </p>

        </div>

      </div>

      {/* =================================================
          Financial Health + Risk
      ================================================= */}

      <div className="dashboard-main-grid">

        {/* Financial Health */}

        <div className="dashboard-section-card">

          <div className="section-card-header">

            <div>

              <h3>
                Financial Health
              </h3>

              <p>
                Key financial performance
                indicators
              </p>

            </div>

          </div>

          <div className="financial-health-grid">

            <div className="health-metric">

              <span>
                Profit Margin
              </span>

              <strong>
                {formatPercentage(
                  financial.profit_margin
                )}
              </strong>

            </div>

            <div className="health-metric">

              <span>
                Current Ratio
              </span>

              <strong>
                {formatNumber(
                  financial.current_ratio
                )}
              </strong>

            </div>

            <div className="health-metric">

              <span>
                Debt to Equity
              </span>

              <strong>
                {formatNumber(
                  financial.debt_to_equity
                )}
              </strong>

            </div>

            <div className="health-metric">

              <span>
                Net Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  financial.net_cash_flow
                )}
              </strong>

            </div>

          </div>

        </div>

        {/* Risk Analysis */}

        <div className="dashboard-section-card risk-card">

          <div className="section-card-header">

            <div>

              <h3>
                Risk Analysis
              </h3>

              <p>
                Current financial distress
                assessment
              </p>

            </div>

          </div>

          <div className="risk-content">

            <div
              className={`risk-indicator ${riskClass}`}
            >

              <span className="risk-score">

                {risk.risk_score !==
                  null &&
                risk.risk_score !==
                  undefined
                  ? formatNumber(
                      risk.risk_score,
                      0
                    )
                  : "N/A"}

              </span>

              <span className="risk-score-label">
                Risk Score
              </span>

            </div>

            <div className="risk-details">

              <span className="risk-label">
                Risk Level
              </span>

              <strong
                className={`risk-level ${riskClass}`}
              >
                {risk.risk_level ||
                  "N/A"}
              </strong>

              <p>

                {risk.crisis_detected
                  ? "Potential financial distress detected."
                  : "No significant financial distress detected."}

              </p>

            </div>

          </div>

        </div>

      </div>

      {/* =================================================
          Balance Sheet
      ================================================= */}

      <div className="dashboard-section-card">

        <div className="section-card-header">

          <div>

            <h3>
              Balance Sheet Overview
            </h3>

            <p>
              Current assets, liabilities,
              debt and equity
            </p>

          </div>

        </div>

        <div className="balance-sheet-grid">

          <div className="balance-item">

            <span>
              Total Assets
            </span>

            <strong>
              {formatCurrency(
                financial.assets
              )}
            </strong>

          </div>

          <div className="balance-item">

            <span>
              Total Liabilities
            </span>

            <strong>
              {formatCurrency(
                financial.liabilities
              )}
            </strong>

          </div>

          <div className="balance-item">

            <span>
              Debt
            </span>

            <strong>
              {formatCurrency(
                financial.debt
              )}
            </strong>

          </div>

          <div className="balance-item">

            <span>
              Equity
            </span>

            <strong>
              {formatCurrency(
                financial.equity
              )}
            </strong>

          </div>

        </div>

      </div>

      {/* =================================================
          Cash Flow + Financial Position
      ================================================= */}

      <div className="dashboard-main-grid">

        {/* Cash Flow */}

        <div className="dashboard-section-card">

          <div className="section-card-header">

            <div>

              <h3>
                Cash Flow Overview
              </h3>

              <p>
                Cash generated and used
                across activities
              </p>

            </div>

            <span
              className={`cash-flow-status ${
                netCashFlow >= 0
                  ? "positive"
                  : "negative"
              }`}
            >
              {cashFlowStatus}
            </span>

          </div>

          <div className="cash-flow-list">

            <div className="cash-flow-row">

              <span>
                Operating Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  financial.operating_cash_flow
                )}
              </strong>

            </div>

            <div className="cash-flow-row">

              <span>
                Investing Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  financial.investing_cash_flow
                )}
              </strong>

            </div>

            <div className="cash-flow-row">

              <span>
                Financing Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  financial.financing_cash_flow
                )}
              </strong>

            </div>

            <div className="cash-flow-row total">

              <span>
                Net Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  financial.net_cash_flow
                )}
              </strong>

            </div>

          </div>

        </div>

        {/* Financial Position */}

        <div className="dashboard-section-card">

          <div className="section-card-header">

            <div>

              <h3>
                Financial Position
              </h3>

              <p>
                Capital structure and
                liquidity
              </p>

            </div>

          </div>

          <div className="position-list">

            <div className="position-row">

              <span>
                Current Assets
              </span>

              <strong>
                {formatCurrency(
                  financial.current_assets
                )}
              </strong>

            </div>

            <div className="position-row">

              <span>
                Current Liabilities
              </span>

              <strong>
                {formatCurrency(
                  financial.current_liabilities
                )}
              </strong>

            </div>

            <div className="position-row">

              <span>
                Current Ratio
              </span>

              <strong>
                {formatNumber(
                  financial.current_ratio
                )}
              </strong>

            </div>

            <div className="position-row">

              <span>
                Debt / Equity
              </span>

              <strong>
                {formatNumber(
                  financial.debt_to_equity
                )}
              </strong>

            </div>

          </div>

        </div>

      </div>

      {/* =================================================
          Alerts + Recommendations
      ================================================= */}

      <div className="dashboard-main-grid">

        {/* Alerts */}

        <div className="dashboard-section-card">

          <div className="section-card-header">

            <div>

              <h3>
                Recent Alerts
              </h3>

              <p>
                Important financial warnings
              </p>

            </div>

            <span className="section-count">
              {alerts.length}
            </span>

          </div>

          {alerts.length === 0 ? (

            <div className="empty-dashboard-state">

              <span>
                ✓
              </span>

              <p>
                No recent alerts.
              </p>

            </div>

          ) : (

            <div className="dashboard-alert-list">

              {alerts.map(
                (alert) => (

                  <div
                    className="dashboard-alert-item"
                    key={alert.id}
                  >

                    <div className="alert-indicator">
                      !
                    </div>

                    <div className="alert-content">

                      <strong>
                        {alert.title ||
                          "Financial Alert"}
                      </strong>

                      <p>
                        {alert.message ||
                          "No additional information available."}
                      </p>

                      <span>
                        {alert.category ||
                          "General"}
                      </span>

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

        {/* Recommendations */}

        <div className="dashboard-section-card">

          <div className="section-card-header">

            <div>

              <h3>
                Top Recommendations
              </h3>

              <p>
                Suggested turnaround
                actions
              </p>

            </div>

            <span className="section-count">
              {recommendations.length}
            </span>

          </div>

          {recommendations.length === 0 ? (

            <div className="empty-dashboard-state">

              <span>
                ✓
              </span>

              <p>
                No recommendations
                available.
              </p>

            </div>

          ) : (

            <div className="dashboard-recommendation-list">

              {recommendations.map(
                (recommendation) => (

                  <div
                    className="dashboard-recommendation-item"
                    key={recommendation.id}
                  >

                    <div className="recommendation-number">
                      →
                    </div>

                    <div className="recommendation-content">

                      <strong>
                        {recommendation.title ||
                          "Recommendation"}
                      </strong>

                      <p>
                        {recommendation.description ||
                          recommendation.action ||
                          "No additional information available."}
                      </p>

                      {recommendation.priority && (
                        <span
                          className={`recommendation-priority ${String(
                            recommendation.priority
                          ).toLowerCase()}`}
                        >
                          {recommendation.priority}
                        </span>
                      )}

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      </div>

      {/* =================================================
          Footer
      ================================================= */}

      <div className="dashboard-footer">

        <span>
          BTIP Financial Intelligence Platform
        </span>

        <span>
          Data source: Financial Analysis Engine
        </span>

      </div>

    </div>
  );
}

export default Dashboard;