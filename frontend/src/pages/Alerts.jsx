import { useEffect, useState } from "react";

function Alerts({ companyId }) {
  const [company, setCompany] = useState(null);
  const [metrics, setMetrics] = useState(null);

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const [loadingCompany, setLoadingCompany] = useState(false);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  // =====================================================
  // Load Selected Company and Financial Metrics
  // =====================================================

  useEffect(() => {
    const loadCompanyData = async () => {
      if (!companyId) {
        setCompany(null);
        setMetrics(null);
        setResult(null);
        setError("Please upload or select a company first.");
        return;
      }

      try {
        setLoadingCompany(true);
        setError("");
        setResult(null);

        const response = await fetch(
          `${API_BASE_URL}/dashboard/${companyId}`
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            typeof data.detail === "string"
              ? data.detail
              : "Unable to load company financial data."
          );
        }

        setCompany(data.company);

        setMetrics({
          profit_margin: data.financial?.profit_margin ?? 0,
          current_ratio: data.financial?.current_ratio ?? 0,
          debt_to_equity: data.financial?.debt_to_equity ?? 0,
          net_cash_flow: data.financial?.net_cash_flow ?? 0
        });
      } catch (err) {
        console.error("Company data loading error:", err);

        setCompany(null);
        setMetrics(null);

        setError(
          err instanceof Error
            ? err.message
            : "Unable to connect to the backend."
        );
      } finally {
        setLoadingCompany(false);
      }
    };

    loadCompanyData();
  }, [companyId]);

  // =====================================================
  // Generate Alerts
  // =====================================================

  const handleGenerateAlerts = async () => {
    if (!companyId) {
      setError("Please upload or select a company first.");
      setResult(null);
      return;
    }

    if (!company || !metrics) {
      setError(
        "Financial data for the selected company is unavailable."
      );
      setResult(null);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      // The backend now gets the financial data directly
      // from the selected company's latest database record.
      const response = await fetch(
        `${API_BASE_URL}/alerts/generate/${companyId}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json"
          }
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let message = "Alert generation failed.";

        if (typeof data.detail === "string") {
          message = data.detail;
        } else if (data.detail) {
          message = JSON.stringify(data.detail);
        }

        throw new Error(message);
      }

      setResult(data);
    } catch (err) {
      console.error("Alert generation error:", err);

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
  // Alert Data
  // =====================================================

  const alerts = result?.alerts || [];

  // =====================================================
  // Severity Styling
  // =====================================================

  const getSeverityClass = (severity) => {
    const level = String(severity || "").toLowerCase();

    if (level === "high") {
      return "alert-severity high";
    }

    if (level === "medium") {
      return "alert-severity medium";
    }

    return "alert-severity low";
  };

  // =====================================================
  // No Company Selected
  // =====================================================

  if (!companyId) {
    return (
      <div className="page">
        <h2>Alerts</h2>

        <p>
          Generate financial risk alerts based on key business indicators.
        </p>

        <div className="error-message">
          <strong>No Company Selected</strong>

          <p>
            Please upload or select a company before generating alerts.
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
        <h2>Alerts</h2>

        <div className="alerts-control">
          <h3>Loading Financial Data...</h3>

          <p>
            Retrieving the latest financial indicators for the selected
            company.
          </p>
        </div>
      </div>
    );
  }

  // =====================================================
  // Company Verification Failed
  // =====================================================

  if (!company || !metrics) {
    return (
      <div className="page">
        <h2>Alerts</h2>

        <div className="error-message">
          <strong>Financial Data Unavailable</strong>

          <p>
            {error ||
              "Unable to retrieve financial information for the selected company."}
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
      <h2>Alerts</h2>

      <p>
        Generate financial risk alerts based on the selected company's
        financial indicators.
      </p>

      {/* =================================================
          Company Information
      ================================================= */}

      <div className="company-banner">
        <div className="company-avatar">
          {company.name
            ? company.name.charAt(0).toUpperCase()
            : "C"}
        </div>

        <div className="company-details">
          <h3>{company.name}</h3>

          <p>
            {company.industry || "Industry not specified"}
          </p>
        </div>

        <div className="company-id">
          Company ID: <strong>{company.id}</strong>
        </div>
      </div>

      {/* =================================================
          Financial Risk Assessment
      ================================================= */}

      <div className="alerts-control">
        <h3>Financial Risk Assessment</h3>

        <p>
          The following indicators are automatically retrieved from the
          selected company's latest financial data.
        </p>

        <div className="alert-input-grid">
          <div className="alert-input-group">
            <label>Profit Margin (%)</label>

            <input
              type="number"
              value={Number(metrics.profit_margin).toFixed(2)}
              readOnly
            />
          </div>

          <div className="alert-input-group">
            <label>Current Ratio</label>

            <input
              type="number"
              value={Number(metrics.current_ratio).toFixed(2)}
              readOnly
            />
          </div>

          <div className="alert-input-group">
            <label>Debt-to-Equity</label>

            <input
              type="number"
              value={Number(metrics.debt_to_equity).toFixed(2)}
              readOnly
            />
          </div>

          <div className="alert-input-group">
            <label>Net Cash Flow</label>

            <input
              type="number"
              value={Number(metrics.net_cash_flow).toFixed(2)}
              readOnly
            />
          </div>
        </div>

        <button
          onClick={handleGenerateAlerts}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Alerts"}
        </button>
      </div>

      {/* =================================================
          Error
      ================================================= */}

      {error && (
        <div className="error-message">
          <strong>Alert Generation Error</strong>

          <p>{error}</p>
        </div>
      )}

      {/* =================================================
          Results
      ================================================= */}

      {result && (
        <div className="alerts-dashboard">

          {/* =================================================
              Header
          ================================================= */}

          <div className="alerts-header">
            <div>
              <h3>
                {company.name} — Financial Alerts
              </h3>

              <p>
                Industry:{" "}
                {company.industry || "Not specified"}
              </p>

              <p>
                Risk assessment based on the latest financial indicators.
              </p>
            </div>

            <span
              className={getSeverityClass(result.risk_level)}
            >
              {String(
                result.risk_level || "low"
              ).toUpperCase()}
            </span>
          </div>

          {/* =================================================
              Summary Cards
          ================================================= */}

          <div className="alert-summary-cards">

            <div className="alert-summary-card">
              <span>Risk Score</span>

              <strong>
                {result.risk_score ?? 0}
              </strong>
            </div>

            <div className="alert-summary-card">
              <span>Risk Level</span>

              <strong
                className={getSeverityClass(
                  result.risk_level
                )}
              >
                {String(
                  result.risk_level || "low"
                ).toUpperCase()}
              </strong>
            </div>

            <div className="alert-summary-card">
              <span>Total Alerts</span>

              <strong>
                {result.count ?? alerts.length}
              </strong>
            </div>

          </div>

          {/* =================================================
              Alert List
          ================================================= */}

          <h3 className="section-title">
            Active Alerts
          </h3>

          {alerts.length === 0 ? (
            <div className="no-alerts">

              <div className="no-alerts-icon">
                ✓
              </div>

              <div>
                <strong>
                  No financial alerts detected.
                </strong>

                <p>
                  The current financial indicators do not contain any
                  identified risk warnings.
                </p>
              </div>

            </div>
          ) : (
            <div className="alerts-list">

              {alerts.map((alert, index) => (
                <div
                  className="alert-card"
                  key={alert.id || index}
                >

                  <div className="alert-icon">
                    !
                  </div>

                  <div className="alert-content">

                    <div className="alert-card-header">

                      <h3>
                        {alert.title ||
                          "Financial Risk Detected"}
                      </h3>

                      <span
                        className={getSeverityClass(
                          alert.severity
                        )}
                      >
                        {String(
                          alert.severity || "low"
                        ).toUpperCase()}
                      </span>

                    </div>

                    <p className="alert-message">
                      {alert.message}
                    </p>

                    <div className="alert-meta">

                      <span>
                        Category:{" "}
                        {alert.category ||
                          "financial"}
                      </span>

                      <span>
                        Status:{" "}
                        {alert.is_read
                          ? "Read"
                          : "Unread"}
                      </span>

                    </div>

                  </div>

                </div>
              ))}

            </div>
          )}

        </div>
      )}
    </div>
  );
}

export default Alerts;