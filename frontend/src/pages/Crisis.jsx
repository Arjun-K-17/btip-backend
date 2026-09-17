import { useEffect, useState } from "react";

function Crisis({ companyId }) {
  const [company, setCompany] = useState(null);
  const [analysis, setAnalysis] = useState(null);
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
        setAnalysis(null);
        setError("Please upload or select a company first.");
        return;
      }

      try {
        setLoadingCompany(true);
        setError("");
        setAnalysis(null);

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
        console.error("Company verification error:", err);

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
  // Detect Crisis
  // =====================================================

  const handleDetection = async () => {
    if (!companyId) {
      setError("Please upload or select a company first.");
      return;
    }

    if (!company) {
      setError("The selected company could not be verified.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnalysis(null);

      const response = await fetch(
        `${API_BASE_URL}/crisis/detect/${companyId}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let errorMessage = "Crisis detection failed.";

        if (typeof data.detail === "string") {
          errorMessage = data.detail;
        } else if (data.detail) {
          errorMessage = JSON.stringify(data.detail);
        }

        throw new Error(errorMessage);
      }

      setAnalysis(data);
    } catch (err) {
      console.error("Crisis detection error:", err);

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
  // Crisis Data
  // =====================================================

  const crisisAnalysis =
    analysis?.crisis_analysis || {};

  const riskScore =
    crisisAnalysis.risk_score ?? "N/A";

  const riskLevel =
    crisisAnalysis.risk_level || "N/A";

  const crisisDetected =
    crisisAnalysis.crisis_detected ?? false;

  const warnings =
    crisisAnalysis.warnings || [];

  // =====================================================
  // Risk Color
  // =====================================================

  const getRiskColor = () => {
    const level =
      String(riskLevel).toLowerCase();

    if (level === "low") {
      return "#16a34a";
    }

    if (level === "medium") {
      return "#d97706";
    }

    if (level === "high") {
      return "#dc2626";
    }

    return "#374151";
  };

  // =====================================================
  // No Company
  // =====================================================

  if (!companyId) {
    return (
      <div className="page">
        <h2>Crisis Detection</h2>

        <p>
          Detect financial distress and identify
          potential business crisis indicators.
        </p>

        <div className="error-message">
          <strong>No Company Selected</strong>

          <p>
            Please upload a financial dataset
            before using Crisis Detection.
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
        <h2>Crisis Detection</h2>

        <div className="error-message">
          <strong>Verifying Company...</strong>

          <p>
            Loading company information and
            financial data.
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
        <h2>Crisis Detection</h2>

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
    <div
      className="page"
      style={{
        width: "100%",
        padding: "0",
      }}
    >
      {/* =================================================
          PAGE HEADER
      ================================================= */}

      <h2
        style={{
          fontSize: "24px",
          marginBottom: "8px",
          color: "#1f2937",
        }}
      >
        Crisis Detection
      </h2>

      <p
        style={{
          marginTop: "8px",
          marginBottom: "25px",
          color: "#666",
          fontSize: "16px",
        }}
      >
        Detect financial distress and identify
        potential business crisis indicators.
      </p>

      {/* =================================================
          COMPANY INFORMATION
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
          DETECTION CONTROL
      ================================================= */}

      <div
        style={{
          backgroundColor: "#ffffff",
          padding: "25px",
          borderRadius: "8px",
          boxShadow:
            "0 2px 6px rgba(0, 0, 0, 0.08)",
          maxWidth: "600px",
          marginTop: "25px",
        }}
      >

        <label
          style={{
            display: "block",
            marginBottom: "8px",
            fontWeight: "bold",
            color: "#374151",
          }}
        >
          Selected Company
        </label>

        <input
          type="text"
          readOnly
          value={`${company.name} — ${
            company.industry ||
            "Industry not specified"
          }`}
          style={{
            width: "100%",
            padding: "10px 12px",
            marginBottom: "15px",
            border: "1px solid #d1d5db",
            borderRadius: "5px",
            fontSize: "14px",
            outline: "none",
            backgroundColor: "#f9fafb",
          }}
        />

        <button
          onClick={handleDetection}
          disabled={loading}
          style={{
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            cursor: loading
              ? "not-allowed"
              : "pointer",
            backgroundColor: "#1f2937",
            color: "#ffffff",
            fontSize: "14px",
            opacity: loading ? 0.6 : 1,
          }}
        >
          {loading
            ? "Analyzing..."
            : "Detect Financial Crisis"}
        </button>

      </div>

      {/* =================================================
          ERROR
      ================================================= */}

      {error && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            backgroundColor: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: "6px",
            color: "#b91c1c",
            maxWidth: "900px",
          }}
        >
          <strong
            style={{
              display: "block",
              marginBottom: "6px",
            }}
          >
            Crisis Detection Error
          </strong>

          <p
            style={{
              margin: 0,
              color: "#b91c1c",
            }}
          >
            {error}
          </p>
        </div>
      )}

      {/* =================================================
          RESULTS
      ================================================= */}

      {analysis && (
        <div
          style={{
            marginTop: "30px",
            maxWidth: "1100px",
          }}
        >

          {/* =================================================
              ANALYSIS HEADER
          ================================================= */}

          <div
            style={{
              backgroundColor: "#ffffff",
              padding: "25px",
              borderRadius: "8px",
              boxShadow:
                "0 2px 6px rgba(0, 0, 0, 0.08)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: "20px",
            }}
          >

            <div>

              <h3
                style={{
                  marginBottom: "8px",
                  fontSize: "20px",
                  color: "#1f2937",
                }}
              >
                {company.name}
                {" — "}
                Crisis Analysis
              </h3>

              <p
                style={{
                  color: "#666",
                  fontSize: "14px",
                  margin: 0,
                }}
              >
                Industry:{" "}
                {company.industry ||
                  "Not specified"}

                {" • "}

                Company ID:{" "}
                {company.id}
              </p>

            </div>

            <span
              style={{
                backgroundColor: crisisDetected
                  ? "#fee2e2"
                  : "#dcfce7",
                color: crisisDetected
                  ? "#b91c1c"
                  : "#166534",
                padding: "8px 15px",
                borderRadius: "20px",
                fontSize: "13px",
                fontWeight: "bold",
                whiteSpace: "nowrap",
              }}
            >
              {crisisDetected
                ? "Crisis Detected"
                : "No Crisis Detected"}
            </span>

          </div>


          {/* =================================================
              RISK METRICS
          ================================================= */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(3, minmax(0, 1fr))",
              gap: "20px",
              marginTop: "25px",
            }}
          >

            {/* Risk Score */}

            <div
              style={{
                backgroundColor: "#ffffff",
                padding: "25px",
                borderRadius: "8px",
                boxShadow:
                  "0 2px 6px rgba(0, 0, 0, 0.08)",
              }}
            >

              <span
                style={{
                  display: "block",
                  color: "#6b7280",
                  fontSize: "14px",
                  marginBottom: "10px",
                }}
              >
                Risk Score
              </span>

              <strong
                style={{
                  fontSize: "24px",
                  color: "#1f2937",
                }}
              >
                {riskScore}
              </strong>

            </div>


            {/* Risk Level */}

            <div
              style={{
                backgroundColor: "#ffffff",
                padding: "25px",
                borderRadius: "8px",
                boxShadow:
                  "0 2px 6px rgba(0, 0, 0, 0.08)",
              }}
            >

              <span
                style={{
                  display: "block",
                  color: "#6b7280",
                  fontSize: "14px",
                  marginBottom: "10px",
                }}
              >
                Risk Level
              </span>

              <strong
                style={{
                  fontSize: "24px",
                  color: getRiskColor(),
                }}
              >
                {String(
                  riskLevel
                ).toUpperCase()}
              </strong>

            </div>


            {/* Crisis Detected */}

            <div
              style={{
                backgroundColor: "#ffffff",
                padding: "25px",
                borderRadius: "8px",
                boxShadow:
                  "0 2px 6px rgba(0, 0, 0, 0.08)",
              }}
            >

              <span
                style={{
                  display: "block",
                  color: "#6b7280",
                  fontSize: "14px",
                  marginBottom: "10px",
                }}
              >
                Crisis Detected
              </span>

              <strong
                style={{
                  fontSize: "24px",
                  color: crisisDetected
                    ? "#dc2626"
                    : "#16a34a",
                }}
              >
                {crisisDetected
                  ? "YES"
                  : "NO"}
              </strong>

            </div>

          </div>


          {/* =================================================
              WARNINGS
          ================================================= */}

          <div
            style={{
              backgroundColor: "#ffffff",
              padding: "25px",
              borderRadius: "8px",
              boxShadow:
                "0 2px 6px rgba(0, 0, 0, 0.08)",
              marginTop: "30px",
            }}
          >

            <h3
              style={{
                marginBottom: "20px",
                color: "#1f2937",
              }}
            >
              Warnings
            </h3>


            {warnings.length === 0 ? (

              <div
                style={{
                  padding: "18px",
                  backgroundColor: "#f0fdf4",
                  border:
                    "1px solid #bbf7d0",
                  borderRadius: "6px",
                  color: "#166534",
                }}
              >

                <strong
                  style={{
                    display: "block",
                    marginBottom: "6px",
                  }}
                >
                  No warnings detected.
                </strong>

                <p
                  style={{
                    margin: 0,
                    color: "#374151",
                  }}
                >
                  The company currently has
                  no identified financial
                  distress warnings.
                </p>

              </div>

            ) : (

              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "10px",
                }}
              >

                {warnings.map(
                  (warning, index) => (

                    <div
                      key={index}
                      style={{
                        padding: "15px",
                        backgroundColor:
                          "#fff7ed",
                        border:
                          "1px solid #fed7aa",
                        borderRadius: "6px",
                        color: "#9a3412",
                      }}
                    >
                      ⚠ {warning}
                    </div>

                  )
                )}

              </div>

            )}

          </div>

        </div>
      )}

      {/* =================================================
          RESPONSIVE STYLE
      ================================================= */}

      <style>
        {`
          @media (max-width: 768px) {

            .crisis-mobile-grid {
              grid-template-columns: 1fr !important;
            }

          }
        `}
      </style>

    </div>
  );
}

export default Crisis;