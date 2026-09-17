import { useEffect, useState } from "react";

function Recommendations({ companyId }) {
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
  // Generate Recommendations
  // =====================================================

  const handleGenerate = async () => {
    if (!companyId) {
      setError(
        "Please upload or select a company first."
      );
      setResult(null);
      return;
    }

    if (!company) {
      setError(
        "The selected company could not be verified."
      );
      setResult(null);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      // -------------------------------------------------
      // Step 1: Run financial analysis
      // -------------------------------------------------

      const analysisResponse = await fetch(
        `${API_BASE_URL}/analytics/financial/${companyId}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json"
          }
        }
      );

      const analysisData =
        await analysisResponse.json();

      if (!analysisResponse.ok) {
        let message =
          "Financial analysis failed.";

        if (
          typeof analysisData.detail ===
          "string"
        ) {
          message =
            analysisData.detail;
        } else if (
          analysisData.detail
        ) {
          message =
            JSON.stringify(
              analysisData.detail
            );
        }

        throw new Error(message);
      }

      // -------------------------------------------------
      // Step 2: Get analysis ID
      // -------------------------------------------------

      const analysisId =
        analysisData.analysis_id ||
        analysisData.id ||
        analysisData.analysis?.id;

      if (!analysisId) {
        throw new Error(
          "Financial analysis completed, but no analysis ID was returned."
        );
      }

      // -------------------------------------------------
      // Step 3: Generate recommendations
      // -------------------------------------------------

      const response = await fetch(
        `${API_BASE_URL}/recommendations/generate/${analysisId}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json"
          }
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let message =
          "Recommendation generation failed.";

        if (
          typeof data.detail ===
          "string"
        ) {
          message =
            data.detail;
        } else if (
          data.detail
        ) {
          message =
            JSON.stringify(
              data.detail
            );
        }

        throw new Error(message);
      }

      setResult({
        ...data,
        analysis_id: analysisId
      });

    } catch (err) {
      console.error(
        "Recommendation generation error:",
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
  // Recommendation Data
  // =====================================================

  const recommendations =
    result?.recommendations || [];

  // =====================================================
  // Priority Styling
  // =====================================================

  const getPriorityClass = (priority) => {
    if (!priority) {
      return "priority-default";
    }

    const value =
      String(priority).toLowerCase();

    if (value === "high") {
      return "priority-high";
    }

    if (value === "medium") {
      return "priority-medium";
    }

    if (value === "low") {
      return "priority-low";
    }

    return "priority-default";
  };

  // =====================================================
  // Recommendation Title
  // =====================================================

  const getRecommendationTitle = (
    recommendation
  ) => {
    if (
      typeof recommendation ===
      "string"
    ) {
      return recommendation;
    }

    return (
      recommendation.title ||
      recommendation.recommendation ||
      recommendation.action ||
      recommendation.message ||
      "Recommendation"
    );
  };

  // =====================================================
  // Recommendation Description
  // =====================================================

  const getRecommendationDescription = (
    recommendation
  ) => {
    if (
      typeof recommendation ===
      "string"
    ) {
      return "";
    }

    return (
      recommendation.description ||
      recommendation.reason ||
      recommendation.details ||
      ""
    );
  };

  // =====================================================
  // Recommendation Priority
  // =====================================================

  const getRecommendationPriority = (
    recommendation
  ) => {
    if (
      typeof recommendation ===
      "string"
    ) {
      return "General";
    }

    return (
      recommendation.priority ||
      "General"
    );
  };

  // =====================================================
  // No Company Selected
  // =====================================================

  if (!companyId) {
    return (
      <div className="page">
        <h2>Recommendations</h2>

        <p>
          Generate data-driven recovery
          recommendations based on financial
          analysis.
        </p>

        <div className="error-message">
          <strong>No Company Selected</strong>

          <p>
            Please upload or select a
            company before generating
            recommendations.
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
        <h2>Recommendations</h2>

        <div className="recommendation-control">
          <h3>Loading Company...</h3>

          <p>
            Retrieving information for the
            selected company.
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
        <h2>Recommendations</h2>

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

      <h2>Recommendations</h2>

      <p>
        Generate data-driven recovery
        recommendations based on the selected
        company's financial analysis.
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
          Recommendation Controls
      ================================================= */}

      <div className="recommendation-control">

        <h3>
          Recommendation Engine
        </h3>

        <p>
          Generate recovery recommendations
          using the selected company's latest
          financial analysis.
        </p>

        <button
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading
            ? "Generating..."
            : "Generate Recommendations"}
        </button>

      </div>

      {/* =================================================
          Error
      ================================================= */}

      {error && (
        <div className="error-message">

          <strong>
            Recommendation Error
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
        <div className="recommendations-dashboard">

          {/* =================================================
              Result Header
          ================================================= */}

          <div className="recommendations-header">

            <div>

              <h3>
                Business Recovery Recommendations
              </h3>

              <p>
                Analysis ID:{" "}
                <strong>
                  {result.analysis_id}
                </strong>
              </p>

            </div>

            <span className="recommendations-status">
              Recommendations Generated
            </span>

          </div>

          {/* =================================================
              Recommendation Summary
          ================================================= */}

          <div className="recommendation-summary">

            <div className="recommendation-summary-card">

              <span>
                Total Recommendations
              </span>

              <strong>
                {recommendations.length}
              </strong>

            </div>

            <div className="recommendation-summary-card">

              <span>
                Analysis ID
              </span>

              <strong>
                {result.analysis_id}
              </strong>

            </div>

          </div>

          {/* =================================================
              Recommendation List
          ================================================= */}

          <h3 className="section-title">
            Recommended Actions
          </h3>

          {recommendations.length === 0 ? (

            <div className="no-recommendations">

              <strong>
                No recommendations generated.
              </strong>

              <p>
                The analysis engine did not
                identify any specific recovery
                actions for this analysis.
              </p>

            </div>

          ) : (

            <div className="recommendations-list">

              {recommendations.map(
                (
                  recommendation,
                  index
                ) => {

                  const title =
                    getRecommendationTitle(
                      recommendation
                    );

                  const description =
                    getRecommendationDescription(
                      recommendation
                    );

                  const priority =
                    getRecommendationPriority(
                      recommendation
                    );

                  return (
                    <div
                      className="recommendation-card"
                      key={
                        recommendation.id ||
                        `${title}-${index}`
                      }
                    >

                      <div className="recommendation-number">
                        {index + 1}
                      </div>

                      <div className="recommendation-content">

                        <div className="recommendation-card-header">

                          <h3>
                            {title}
                          </h3>

                          <span
                            className={`recommendation-priority ${getPriorityClass(
                              priority
                            )}`}
                          >
                            {String(
                              priority
                            ).toUpperCase()}
                          </span>

                        </div>

                        {description && (
                          <p>
                            {description}
                          </p>
                        )}

                      </div>

                    </div>
                  );
                }
              )}

            </div>
          )}

        </div>
      )}

    </div>
  );
}

export default Recommendations;