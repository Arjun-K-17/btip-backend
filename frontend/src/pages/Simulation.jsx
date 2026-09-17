import { useEffect, useState } from "react";

function Simulation({ companyId }) {
  const [company, setCompany] = useState(null);
  const [result, setResult] = useState(null);
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
        setResult(null);
        setError(
          "Please upload or select a company first."
        );
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
  // Format Currency
  // =====================================================

  const formatCurrency = (value) => {
    if (
      value === null ||
      value === undefined
    ) {
      return "N/A";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return "N/A";
    }

    return `₹${number.toLocaleString(
      "en-IN",
      {
        maximumFractionDigits: 2,
      }
    )}`;
  };

  // =====================================================
  // Format Percentage
  // =====================================================

  const formatPercentage = (value) => {
    if (
      value === null ||
      value === undefined
    ) {
      return "N/A";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return "N/A";
    }

    return `${(
      number * 100
    ).toFixed(2)}%`;
  };

  // =====================================================
  // Run Simulation
  // =====================================================

  const handleSimulation = async () => {
    if (!companyId) {
      setError(
        "Please upload or select a company first."
      );
      return;
    }

    if (!company) {
      setError(
        "The selected company could not be verified."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await fetch(
        `${API_BASE_URL}/simulation/run/${companyId}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let errorMessage =
          "Recovery simulation failed.";

        if (
          typeof data.detail === "string"
        ) {
          errorMessage =
            data.detail;
        } else if (data.detail) {
          errorMessage =
            JSON.stringify(
              data.detail
            );
        }

        throw new Error(
          errorMessage
        );
      }

      setResult(data);
    } catch (err) {
      console.error(
        "Simulation error:",
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
  // No Company Selected
  // =====================================================

  if (!companyId) {
    return (
      <div className="page">

        <h2>
          Recovery Simulation
        </h2>

        <p>
          Simulate a business turnaround
          strategy and compare projected
          financial performance with the
          current baseline.
        </p>

        <div className="error-message">

          <strong>
            No Company Selected
          </strong>

          <p>
            Please upload a financial
            dataset before using
            Recovery Simulation.
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

        <h2>
          Recovery Simulation
        </h2>

        <div className="simulation-control">

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

        <h2>
          Recovery Simulation
        </h2>

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

      <h2>
        Recovery Simulation
      </h2>

      <p>
        Simulate a business turnaround
        strategy and compare projected
        financial performance with the
        current baseline.
      </p>

      {/* =================================================
          Company Information
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
          Simulation Control
      ================================================= */}

      <div className="simulation-control">

        <h3>
          Recovery Scenario
        </h3>

        <label>
          Selected Company
        </label>

        <input
          type="text"
          readOnly
          value={`${company.name} — ${
            company.industry ||
            "Industry not specified"
          }`}
        />

        <div className="scenario-info">

          <h4>
            Scenario Parameters
          </h4>

          <div className="scenario-grid">

            <div>
              <span>
                Revenue Growth
              </span>

              <strong>
                10%
              </strong>
            </div>

            <div>
              <span>
                Expense Reduction
              </span>

              <strong>
                5%
              </strong>
            </div>

            <div>
              <span>
                Debt Reduction
              </span>

              <strong>
                10%
              </strong>
            </div>

          </div>

        </div>

        <button
          onClick={handleSimulation}
          disabled={loading}
        >
          {loading
            ? "Running Simulation..."
            : "Run Recovery Simulation"}
        </button>

      </div>

      {/* =================================================
          Error
      ================================================= */}

      {error && (
        <div className="error-message">

          <strong>
            Simulation Error
          </strong>

          <p>
            {error}
          </p>

        </div>
      )}

      {/* =================================================
          Results
      ================================================= */}

      {result && (
        <div className="simulation-dashboard">

          {/* =================================================
              Result Header
          ================================================= */}

          <div className="analysis-header">

            <div>

              <h3>
                {company.name}
                {" — "}
                Recovery Simulation
              </h3>

              <p>
                Industry:{" "}
                {company.industry ||
                  "Not specified"}
              </p>

              <p>
                Company ID:{" "}
                {company.id}
              </p>

            </div>

            <div className="analysis-status">
              Simulation Completed
            </div>

          </div>

          {/* =================================================
              Scenario
          ================================================= */}

          <h3 className="section-title">
            Recovery Strategy
          </h3>

          <div className="detail-cards">

            <div className="detail-card">

              <span>
                Revenue Growth
              </span>

              <strong>
                {formatPercentage(
                  result.scenario
                    ?.revenue_growth
                )}
              </strong>

            </div>

            <div className="detail-card">

              <span>
                Expense Reduction
              </span>

              <strong>
                {formatPercentage(
                  result.scenario
                    ?.expense_reduction
                )}
              </strong>

            </div>

            <div className="detail-card">

              <span>
                Debt Reduction
              </span>

              <strong>
                {formatPercentage(
                  result.scenario
                    ?.debt_reduction
                )}
              </strong>

            </div>

          </div>

          {/* =================================================
              Baseline
          ================================================= */}

          <h3 className="section-title">
            Current Financial Baseline
          </h3>

          <div className="analytics-cards">

            <div className="analytics-card">

              <span>
                Revenue
              </span>

              <strong>
                {formatCurrency(
                  result.baseline?.revenue
                )}
              </strong>

            </div>

            <div className="analytics-card">

              <span>
                Expenses
              </span>

              <strong>
                {formatCurrency(
                  result.baseline?.expenses
                )}
              </strong>

            </div>

            <div className="analytics-card">

              <span>
                Profit
              </span>

              <strong>
                {formatCurrency(
                  result.baseline?.profit
                )}
              </strong>

            </div>

            <div className="analytics-card">

              <span>
                Cash
              </span>

              <strong>
                {formatCurrency(
                  result.baseline?.cash
                )}
              </strong>

            </div>

            <div className="analytics-card">

              <span>
                Debt
              </span>

              <strong>
                {formatCurrency(
                  result.baseline?.debt
                )}
              </strong>

            </div>

          </div>

          {/* =================================================
              Projection
          ================================================= */}

          <h3 className="section-title">
            Projected Recovery
          </h3>

          <div className="analytics-cards">

            <div className="analytics-card simulation-positive">

              <span>
                Projected Revenue
              </span>

              <strong>
                {formatCurrency(
                  result.projection?.revenue
                )}
              </strong>

            </div>

            <div className="analytics-card">

              <span>
                Projected Expenses
              </span>

              <strong>
                {formatCurrency(
                  result.projection?.expenses
                )}
              </strong>

            </div>

            <div className="analytics-card simulation-positive">

              <span>
                Projected Profit
              </span>

              <strong>
                {formatCurrency(
                  result.projection?.profit
                )}
              </strong>

            </div>

            <div className="analytics-card">

              <span>
                Projected Cash
              </span>

              <strong>
                {formatCurrency(
                  result.projection?.cash
                )}
              </strong>

            </div>

            <div className="analytics-card">

              <span>
                Projected Debt
              </span>

              <strong>
                {formatCurrency(
                  result.projection?.debt
                )}
              </strong>

            </div>

          </div>

          {/* =================================================
              Comparison
          ================================================= */}

          <h3 className="section-title">
            Baseline vs Recovery Comparison
          </h3>

          <div className="simulation-comparison">

            <pre>
              {JSON.stringify(
                result.comparison,
                null,
                2
              )}
            </pre>

          </div>

        </div>
      )}

    </div>
  );
}

export default Simulation;