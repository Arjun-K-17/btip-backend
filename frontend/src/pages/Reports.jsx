import { useEffect, useState } from "react";

function Reports({ companyId }) {
  const [company, setCompany] = useState(null);

  const [analysisId, setAnalysisId] = useState(null);
  const [report, setReport] = useState(null);

  const [error, setError] = useState("");
  const [downloadError, setDownloadError] = useState("");

  const [loadingCompany, setLoadingCompany] = useState(false);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  /*
   * =========================================
   * Load Selected Company
   * =========================================
   */

  useEffect(() => {
    const loadCompany = async () => {
      if (!companyId) {
        setCompany(null);
        setAnalysisId(null);
        setReport(null);
        setError("Please upload or select a company first.");
        return;
      }

      try {
        setLoadingCompany(true);
        setError("");
        setDownloadError("");
        setReport(null);
        setAnalysisId(null);

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
        setAnalysisId(null);

        setError(
          err instanceof Error
            ? err.message
            : "Unable to connect to the backend."
        );
      } finally {
        setLoadingCompany(false);
      }
    };

    loadCompany();
  }, [companyId]);

  /*
   * =========================================
   * Format Helpers
   * =========================================
   */

  const formatPercentage = (value) => {
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

    return `${number.toFixed(2)}%`;
  };

  const formatRatio = (value) => {
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

    return number.toFixed(2);
  };

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

    return `₹${number.toLocaleString("en-IN", {
      maximumFractionDigits: 2,
    })}`;
  };

  /*
   * =========================================
   * Run Financial Analysis
   * =========================================
   */

  const getLatestAnalysisId = async () => {
    const response = await fetch(
      `${API_BASE_URL}/analytics/financial/${companyId}`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      let message = "Financial analysis failed.";

      if (typeof data.detail === "string") {
        message = data.detail;
      } else if (data.detail) {
        message = JSON.stringify(data.detail);
      }

      throw new Error(message);
    }

    const generatedAnalysisId =
      data.analysis_id ||
      data.id ||
      data.analysis?.id;

    if (!generatedAnalysisId) {
      throw new Error(
        "Financial analysis completed, but no analysis ID was returned."
      );
    }

    return generatedAnalysisId;
  };

  /*
   * =========================================
   * Generate JSON Report
   * =========================================
   */

  const handleGenerateReport = async () => {
    if (!companyId) {
      setError("Please upload or select a company first.");
      setReport(null);
      return;
    }

    if (!company) {
      setError("The selected company could not be verified.");
      setReport(null);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setDownloadError("");
      setReport(null);

      /*
       * First generate a fresh financial analysis
       * for the selected company.
       */
      const generatedAnalysisId =
        await getLatestAnalysisId();

      setAnalysisId(generatedAnalysisId);

      /*
       * Generate report using the newly created
       * analysis ID.
       */
      const response = await fetch(
        `${API_BASE_URL}/reports/generate/${generatedAnalysisId}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let message = "Report generation failed.";

        if (typeof data.detail === "string") {
          message = data.detail;
        } else if (data.detail) {
          message = JSON.stringify(data.detail);
        }

        throw new Error(message);
      }

      setReport(data);
    } catch (err) {
      console.error("Report generation error:", err);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  /*
   * =========================================
   * Download Professional PDF
   * =========================================
   */

  const handleDownloadPDF = async () => {
    if (!companyId) {
      setDownloadError(
        "Please upload or select a company first."
      );
      return;
    }

    if (!company) {
      setDownloadError(
        "The selected company could not be verified."
      );
      return;
    }

    try {
      setDownloading(true);
      setDownloadError("");

      /*
       * If there is no analysis yet, create one
       * automatically for the selected company.
       */
      let currentAnalysisId = analysisId;

      if (!currentAnalysisId) {
        currentAnalysisId =
          await getLatestAnalysisId();

        setAnalysisId(currentAnalysisId);
      }

      const response = await fetch(
        `${API_BASE_URL}/reports/download/${currentAnalysisId}`,
        {
          method: "GET",
          headers: {
            Accept: "application/pdf",
          },
        }
      );

      if (!response.ok) {
        let message = "PDF report download failed.";

        try {
          const data = await response.json();

          if (typeof data.detail === "string") {
            message = data.detail;
          } else if (data.detail) {
            message = JSON.stringify(data.detail);
          }
        } catch {
          // Keep default error message
        }

        throw new Error(message);
      }

      const blob = await response.blob();

      if (!blob || blob.size === 0) {
        throw new Error(
          "The backend returned an empty PDF file."
        );
      }

      /*
       * Create a temporary browser download link.
       */
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");

      link.href = url;

      link.download =
        `BTIP_Financial_Turnaround_Report_` +
        `${company.name.replace(/[^a-z0-9]/gi, "_")}_` +
        `Analysis_${currentAnalysisId}.pdf`;

      document.body.appendChild(link);

      link.click();

      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF download error:", err);

      setDownloadError(
        err instanceof Error
          ? err.message
          : "Unable to download the PDF report."
      );
    } finally {
      setDownloading(false);
    }
  };

  /*
   * =========================================
   * Extract Report Data
   * =========================================
   */

  const reportData = report?.report || {};

  const financialSummary =
    reportData.financial_summary || {};

  const reportCompanyId =
    reportData.company_id ||
    report?.company_id ||
    company?.id ||
    "N/A";

  const reportTitle =
    reportData.report_title ||
    "Business Turnaround Analysis Report";

  const reportStatus =
    reportData.report_status ||
    "generated";

  /*
   * =========================================
   * Financial Summary Values
   * =========================================
   */

  const profitMargin =
    financialSummary.profit_margin;

  const currentRatio =
    financialSummary.current_ratio;

  const debtToEquity =
    financialSummary.debt_to_equity;

  const netCashFlow =
    financialSummary.net_cash_flow;

  /*
   * =========================================
   * No Company Selected
   * =========================================
   */

  if (!companyId) {
    return (
      <div className="page">

        <h2>Reports</h2>

        <p>
          Generate comprehensive financial analysis
          and professional business turnaround reports.
        </p>

        <div className="error-message">

          <strong>
            No Company Selected
          </strong>

          <p>
            Please upload or select a company before
            generating a report.
          </p>

        </div>

      </div>
    );
  }

  /*
   * =========================================
   * Loading Company
   * =========================================
   */

  if (loadingCompany) {
    return (
      <div className="page">

        <h2>Reports</h2>

        <div className="report-control">

          <h3>
            Loading Company...
          </h3>

          <p>
            Retrieving company information and
            financial data.
          </p>

        </div>

      </div>
    );
  }

  /*
   * =========================================
   * Company Verification Failed
   * =========================================
   */

  if (!company) {
    return (
      <div className="page">

        <h2>Reports</h2>

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

  /*
   * =========================================
   * JSX
   * =========================================
   */

  return (
    <div className="page">

      {/* =========================================
          Page Header
          ========================================= */}

      <h2>Reports</h2>

      <p>
        Generate comprehensive financial analysis
        and professional business turnaround reports.
      </p>

      {/* =========================================
          Company Information
          ========================================= */}

      <div className="company-banner">

        <div className="company-avatar">

          {company.name
            ? company.name.charAt(0).toUpperCase()
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

      {/* =========================================
          Report Controls
          ========================================= */}

      <div className="report-control">

        <h3>
          Report Generation
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

        <p>
          A fresh financial analysis will
          automatically be generated for the
          selected company before creating the
          report.
        </p>

        <div className="report-actions">

          <button
            onClick={handleGenerateReport}
            disabled={
              loading ||
              downloading
            }
          >
            {loading
              ? "Generating..."
              : "Generate Report"}
          </button>

          <button
            className="download-report-button"
            onClick={handleDownloadPDF}
            disabled={
              downloading ||
              loading
            }
          >
            {downloading
              ? "Preparing PDF..."
              : "Download PDF Report"}
          </button>

        </div>

      </div>

      {/* =========================================
          Generate Error
          ========================================= */}

      {error && (
        <div className="error-message">

          <strong>
            Report Error
          </strong>

          <p>
            {error}
          </p>

        </div>
      )}

      {/* =========================================
          PDF Download Error
          ========================================= */}

      {downloadError && (
        <div className="error-message">

          <strong>
            PDF Download Error
          </strong>

          <p>
            {downloadError}
          </p>

        </div>
      )}

      {/* =========================================
          Report Dashboard
          ========================================= */}

      {report && (
        <div className="report-dashboard">

          {/* =========================================
              Report Header
              ========================================= */}

          <div className="report-header">

            <div>

              <h3>
                Financial Analysis Report
              </h3>

              <p>
                Company:{" "}
                {company.name}
              </p>

              <p>
                Industry:{" "}
                {company.industry ||
                  "Not specified"}
              </p>

              <p>
                Analysis ID:{" "}
                {report.analysis_id ||
                  analysisId ||
                  "N/A"}
              </p>

              <p>
                Company ID:{" "}
                {reportCompanyId}
              </p>

            </div>

            <div className="report-header-actions">

              <span className="report-status">
                Report Generated
              </span>

              <button
                className="download-report-button"
                onClick={handleDownloadPDF}
                disabled={downloading}
              >
                {downloading
                  ? "Preparing PDF..."
                  : "Download PDF"}
              </button>

            </div>

          </div>

          {/* =========================================
              Financial Summary
              ========================================= */}

          <h3 className="section-title">
            Financial Summary
          </h3>

          <div className="report-metrics">

            {/* Profit Margin */}

            <div className="report-metric-card">

              <span>
                Profit Margin
              </span>

              <strong>
                {formatPercentage(
                  profitMargin
                )}
              </strong>

            </div>

            {/* Current Ratio */}

            <div className="report-metric-card">

              <span>
                Current Ratio
              </span>

              <strong>
                {formatRatio(
                  currentRatio
                )}
              </strong>

            </div>

            {/* Debt-to-Equity */}

            <div className="report-metric-card">

              <span>
                Debt-to-Equity
              </span>

              <strong>
                {formatRatio(
                  debtToEquity
                )}
              </strong>

            </div>

            {/* Net Cash Flow */}

            <div className="report-metric-card">

              <span>
                Net Cash Flow
              </span>

              <strong>
                {formatCurrency(
                  netCashFlow
                )}
              </strong>

            </div>

          </div>

          {/* =========================================
              Generated Report
              ========================================= */}

          <h3 className="section-title">
            Generated Report
          </h3>

          <div className="report-content">

            {/* Company */}

            <div className="report-item">

              <span>
                Company
              </span>

              <strong>
                {company.name}
              </strong>

            </div>

            {/* Industry */}

            <div className="report-item">

              <span>
                Industry
              </span>

              <strong>
                {company.industry ||
                  "Not specified"}
              </strong>

            </div>

            {/* Company ID */}

            <div className="report-item">

              <span>
                Company ID
              </span>

              <strong>
                {reportCompanyId}
              </strong>

            </div>

            {/* Analysis ID */}

            <div className="report-item">

              <span>
                Analysis ID
              </span>

              <strong>
                {report.analysis_id ||
                  analysisId ||
                  "N/A"}
              </strong>

            </div>

            {/* Report Title */}

            <div className="report-item">

              <span>
                Report Title
              </span>

              <strong>
                {reportTitle}
              </strong>

            </div>

            {/* Financial Summary */}

            <div className="report-item">

              <h4>
                Financial Summary
              </h4>

              <pre>
                {JSON.stringify(
                  financialSummary,
                  null,
                  2
                )}
              </pre>

            </div>

            {/* Report Status */}

            <div className="report-item">

              <span>
                Report Status
              </span>

              <strong>
                {reportStatus}
              </strong>

            </div>

          </div>

          {/* =========================================
              Report Data
              ========================================= */}

          <h3 className="section-title">
            Report Data
          </h3>

          <div className="report-json">

            <pre>
              {JSON.stringify(
                report,
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

export default Reports;