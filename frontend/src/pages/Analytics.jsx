import { useEffect, useState } from "react";

function Analytics({ companyId }) {
  const [company, setCompany] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [error, setError] = useState("");

  const [loadingCompany, setLoadingCompany] = useState(false);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  // =====================================================
  // Load Selected Company
  // =====================================================

  useEffect(() => {
    const loadCompany = async () => {
      if (!companyId) {
        setCompany(null);
        setAnalytics(null);
        setError(
          "Please upload or select a company first."
        );
        return;
      }

      try {
        setLoadingCompany(true);
        setError("");
        setAnalytics(null);

        const response = await fetch(
          `${API_BASE_URL}/dashboard/${companyId}`
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            typeof data.detail === "string"
              ? data.detail
              : "Unable to verify the selected company."
          );
        }

        setCompany(data.company);
      } catch (err) {
        console.error(
          "Company verification error:",
          err
        );

        setCompany(null);

        setError(
          err instanceof Error
            ? err.message
            : "Unable to verify company."
        );
      } finally {
        setLoadingCompany(false);
      }
    };

    loadCompany();
  }, [companyId]);

  // =====================================================
  // Analyze Financial Data
  // =====================================================

  const handleAnalyze = async () => {
    if (!companyId) {
      setError(
        "Please upload or select a company first."
      );
      setAnalytics(null);
      return;
    }

    if (!company) {
      setError(
        "The selected company could not be verified."
      );
      setAnalytics(null);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnalytics(null);

      const response = await fetch(
        `${API_BASE_URL}/analytics/financial/${companyId}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json"
          }
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let errorMessage =
          "Analytics request failed.";

        if (
          typeof data.detail === "string"
        ) {
          errorMessage = data.detail;
        } else if (data.detail) {
          errorMessage = JSON.stringify(
            data.detail
          );
        }

        throw new Error(errorMessage);
      }

      setAnalytics(data);
    } catch (err) {
      console.error(
        "Analytics error:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // API Response Data
  // =====================================================

  const analysisData =
    analytics?.data ||
    analytics ||
    {};

  const financialMetrics =
    analysisData.financial_metrics ||
    {};

  const profitability =
    analysisData.profitability ||
    {};

  const liquidity =
    analysisData.liquidity ||
    {};

  const leverage =
    analysisData.leverage ||
    {};

  const cashFlow =
    analysisData.cash_flow ||
    {};

  const crisisAnalysis =
    analysisData.crisis_analysis ||
    {};

  // =====================================================
  // Formatting
  // =====================================================

  const formatCurrency = (value) => {
    if (
      value === null ||
      value === undefined ||
      value === ""
    ) {
      return "N/A";
    }

    const number = Number(value);

    if (isNaN(number)) {
      return "N/A";
    }

    return `₹${number.toLocaleString(
      "en-IN",
      {
        maximumFractionDigits: 2
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
      value === ""
    ) {
      return "N/A";
    }

    const number = Number(value);

    if (isNaN(number)) {
      return "N/A";
    }

    return number.toFixed(decimals);
  };

  // =====================================================
  // Risk Helpers
  // =====================================================

  const getRiskClass = (riskLevel) => {
    const level = String(
      riskLevel || ""
    ).toLowerCase();

    if (
      level === "high" ||
      level === "critical" ||
      level === "severe"
    ) {
      return "risk-high";
    }

    if (
      level === "medium" ||
      level === "moderate"
    ) {
      return "risk-medium";
    }

    return "risk-low";
  };

  // =====================================================
  // Chart Data
  // =====================================================

  const chartData = [
    {
      label: "Revenue",
      value:
        Number(
          financialMetrics.revenue
        ) || 0,
      className:
        "analytics-chart-bar revenue-bar"
    },
    {
      label: "Expenses",
      value:
        Number(
          financialMetrics.expenses
        ) || 0,
      className:
        "analytics-chart-bar expenses-bar"
    },
    {
      label: "Profit",
      value:
        Number(
          financialMetrics.profit
        ) || 0,
      className:
        "analytics-chart-bar profit-bar"
    },
    {
      label: "Cash",
      value:
        Number(
          financialMetrics.cash
        ) || 0,
      className:
        "analytics-chart-bar cash-bar"
    },
    {
      label: "Debt",
      value:
        Number(
          leverage.debt
        ) || 0,
      className:
        "analytics-chart-bar debt-bar"
    }
  ];

  const chartMaxValue =
    chartData.length > 0
      ? Math.max(
          ...chartData.map(
            (item) => item.value
          ),
          1
        )
      : 1;

  // =====================================================
  // No Company Selected
  // =====================================================

  if (!companyId) {
    return (
      <div className="page">
        <h2>Analytics</h2>

        <p>
          Analyze financial performance
          and key business indicators.
        </p>

        <div className="error-message">
          <strong>
            No Company Selected
          </strong>

          <p>
            Please upload or select a
            company before using Analytics.
          </p>
        </div>
      </div>
    );
  }

  // =====================================================
  // Loading Company
  // =====================================================

  if (loadingCompany) {
    return (
      <div className="page">
        <h2>Analytics</h2>

        <div className="analytics-control">
          <h3>
            Verifying Company...
          </h3>

          <p>
            Loading company information
            and financial data.
          </p>
        </div>
      </div>
    );
  }

  // =====================================================
  // Company Verification Failed
  // =====================================================

  if (!company) {
    return (
      <div className="page">
        <h2>Analytics</h2>

        <div className="error-message">
          <strong>
            Company Verification Failed
          </strong>

          <p>
            {error ||
              "The selected company could not be found."}
          </p>
        </div>
      </div>
    );
  }

  // =====================================================
  // Main UI
  // =====================================================

  return (
    <div className="page">

      {/* =================================================
          Page Header
      ================================================= */}

      <h2>Analytics</h2>

      <p>
        Analyze financial performance
        and key business indicators.
      </p>

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
            {company.name}
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
          Analytics Control
      ================================================= */}

      <div className="analytics-control">

        <h3>
          Financial Analysis
        </h3>

        <p>
          Analyze the selected company's
          latest financial data and generate
          key financial health indicators.
        </p>

        <button
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Financial Data"}
        </button>

      </div>

      {/* =================================================
          Error
      ================================================= */}

      {error && (
        <div className="error-message">

          <strong>
            Analytics Error
          </strong>

          <p>
            {error}
          </p>

        </div>
      )}

      {/* =================================================
          Analytics Results
      ================================================= */}

      {analytics && (

        <div className="analytics-dashboard">

          {/* =================================================
              Analysis Header
          ================================================= */}

          <div className="analysis-header">

            <div>

              <h3>
                Financial Analysis
              </h3>

              <p>
                Analysis ID:{" "}
                <strong>
                  {analysisData.analysis_id ||
                    "N/A"}
                </strong>
              </p>

            </div>

            <span className="analysis-status">
              Analysis Completed
            </span>

          </div>

          {/* =================================================
              Financial Overview
          ================================================= */}

          <h3 className="section-title">
            Financial Overview
          </h3>

          <div className="analytics-cards">

            <div className="analytics-card">
              <span>
                Revenue
              </span>

              <strong>
                {formatCurrency(
                  financialMetrics.revenue
                )}
              </strong>
            </div>

            <div className="analytics-card">
              <span>
                Expenses
              </span>

              <strong>
                {formatCurrency(
                  financialMetrics.expenses
                )}
              </strong>
            </div>

            <div className="analytics-card">
              <span>
                Profit
              </span>

              <strong>
                {formatCurrency(
                  financialMetrics.profit
                )}
              </strong>
            </div>

            <div className="analytics-card">
              <span>
                Profit Margin
              </span>

              <strong>
                {formatNumber(
                  financialMetrics.profit_margin
                )}
                %
              </strong>
            </div>

            <div className="analytics-card">
              <span>
                Cash
              </span>

              <strong>
                {formatCurrency(
                  financialMetrics.cash
                )}
              </strong>
            </div>

            <div className="analytics-card">
              <span>
                Debt
              </span>

              <strong>
                {formatCurrency(
                  leverage.debt
                )}
              </strong>
            </div>

          </div>

          {/* =================================================
              Financial Performance Chart
          ================================================= */}

          <h3 className="section-title">
            Financial Performance
          </h3>

          <div className="analytics-chart-card">

            <div className="analytics-chart-header">

              <div>

                <h3>
                  Financial Indicators
                </h3>

                <p>
                  Comparison of major financial
                  indicators from the latest
                  analysis.
                </p>

              </div>

            </div>

            <div className="analytics-chart">

              <div className="analytics-chart-y-axis">

                <span>
                  {formatCurrency(
                    chartMaxValue
                  )}
                </span>

                <span>
                  {formatCurrency(
                    chartMaxValue * 0.75
                  )}
                </span>

                <span>
                  {formatCurrency(
                    chartMaxValue * 0.5
                  )}
                </span>

                <span>
                  {formatCurrency(
                    chartMaxValue * 0.25
                  )}
                </span>

                <span>
                  ₹0
                </span>

              </div>

              <div className="analytics-chart-area">

                <div className="analytics-grid-lines">
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <div className="analytics-bars">

                  {chartData.map(
                    (item, index) => {

                      const height =
                        item.value > 0
                          ? Math.max(
                              (
                                item.value /
                                chartMaxValue
                              ) * 100,
                              5
                            )
                          : 0;

                      return (
                        <div
                          className="analytics-bar-column"
                          key={`${item.label}-${index}`}
                        >

                          <div className="analytics-bar-value">
                            {formatCurrency(
                              item.value
                            )}
                          </div>

                          <div className="analytics-bar-wrapper">

                            <div
                              className={
                                item.className
                              }
                              style={{
                                height:
                                  `${height}%`
                              }}
                            ></div>

                          </div>

                          <div className="analytics-bar-label">
                            {item.label}
                          </div>

                        </div>
                      );
                    }
                  )}

                </div>

              </div>

            </div>

            {/* Chart Legend */}

            <div className="analytics-chart-legend">

              <span>
                <i className="analytics-legend-dot revenue-dot"></i>
                Revenue
              </span>

              <span>
                <i className="analytics-legend-dot expenses-dot"></i>
                Expenses
              </span>

              <span>
                <i className="analytics-legend-dot profit-dot"></i>
                Profit
              </span>

              <span>
                <i className="analytics-legend-dot cash-dot"></i>
                Cash
              </span>

              <span>
                <i className="analytics-legend-dot debt-dot"></i>
                Debt
              </span>

            </div>

          </div>

          {/* =================================================
              Profitability
          ================================================= */}

          <h3 className="section-title">
            Profitability
          </h3>

          <div className="detail-cards">

            <div className="detail-card">

              <span>
                Revenue
              </span>

              <strong>
                {formatCurrency(
                  profitability.revenue
                )}
              </strong>

            </div>

            <div className="detail-card">

              <span>
                Profit
              </span>

              <strong>
                {formatCurrency(
                  profitability.profit
                )}
              </strong>

            </div>

            <div className="detail-card">

              <span>
                Profit Margin
              </span>

              <strong>
                {formatNumber(
                  profitability.profit_margin
                )}
                %
              </strong>

            </div>

          </div>

          {/* =================================================
              Liquidity and Leverage
          ================================================= */}

          <div className="analytics-two-column">

            {/* Liquidity */}

            <div className="analytics-section">

              <h3>
                Liquidity
              </h3>

              <div className="metric-row">

                <span>
                  Current Assets
                </span>

                <strong>
                  {formatCurrency(
                    liquidity.current_assets
                  )}
                </strong>

              </div>

              <div className="metric-row">

                <span>
                  Current Liabilities
                </span>

                <strong>
                  {formatCurrency(
                    liquidity.current_liabilities
                  )}
                </strong>

              </div>

              <div className="metric-row">

                <span>
                  Cash
                </span>

                <strong>
                  {formatCurrency(
                    liquidity.cash
                  )}
                </strong>

              </div>

              <div className="metric-row">

                <span>
                  Current Ratio
                </span>

                <strong>
                  {formatNumber(
                    liquidity.current_ratio
                  )}
                </strong>

              </div>

            </div>

            {/* Leverage */}

            <div className="analytics-section">

              <h3>
                Leverage
              </h3>

              <div className="metric-row">

                <span>
                  Debt
                </span>

                <strong>
                  {formatCurrency(
                    leverage.debt
                  )}
                </strong>

              </div>

              <div className="metric-row">

                <span>
                  Equity
                </span>

                <strong>
                  {formatCurrency(
                    leverage.equity
                  )}
                </strong>

              </div>

              <div className="metric-row">

                <span>
                  Assets
                </span>

                <strong>
                  {formatCurrency(
                    leverage.assets
                  )}
                </strong>

              </div>

              <div className="metric-row">

                <span>
                  Debt-to-Equity
                </span>

                <strong>
                  {formatNumber(
                    leverage.debt_to_equity
                  )}
                </strong>

              </div>

              <div className="metric-row">

                <span>
                  Debt Ratio
                </span>

                <strong>
                  {formatNumber(
                    leverage.debt_ratio
                  )}
                </strong>

              </div>

            </div>

          </div>

          {/* =================================================
              Cash Flow
          ================================================= */}

          <h3 className="section-title">
            Cash Flow
          </h3>

          <div className="detail-cards">

            <div className="detail-card">

              <span>
                Operating Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  cashFlow.operating_cash_flow
                )}
              </strong>

            </div>

            <div className="detail-card">

              <span>
                Investing Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  cashFlow.investing_cash_flow
                )}
              </strong>

            </div>

            <div className="detail-card">

              <span>
                Financing Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  cashFlow.financing_cash_flow
                )}
              </strong>

            </div>

            <div className="detail-card">

              <span>
                Net Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  cashFlow.net_cash_flow
                )}
              </strong>

            </div>

          </div>

          {/* =================================================
              Crisis Analysis
          ================================================= */}

          <h3 className="section-title">
            Financial Risk Assessment
          </h3>

          <div className="crisis-card">

            <div>

              <span>
                Risk Score
              </span>

              <strong>
                {crisisAnalysis.risk_score ??
                  "N/A"}
              </strong>

            </div>

            <div>

              <span>
                Risk Level
              </span>

              <strong
                className={getRiskClass(
                  crisisAnalysis.risk_level
                )}
              >
                {crisisAnalysis.risk_level ||
                  "N/A"}
              </strong>

            </div>

            <div>

              <span>
                Crisis Detected
              </span>

              <strong
                className={
                  crisisAnalysis.crisis_detected
                    ? "risk-high"
                    : "risk-low"
                }
              >
                {crisisAnalysis.crisis_detected
                  ? "Yes"
                  : "No"}
              </strong>

            </div>

          </div>

        </div>
      )}

    </div>
  );
}

export default Analytics;