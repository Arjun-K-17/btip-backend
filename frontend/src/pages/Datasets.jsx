import { useState } from "react";

function Datasets({ onCompanyCreated }) {
  const [file, setFile] = useState(null);
  const [companyName, setCompanyName] = useState("");
  const [industry, setIndustry] = useState("");

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  const handleUpload = async () => {
    if (!companyName.trim()) {
      setError("Please enter the company name.");
      setResult(null);
      return;
    }

    if (!file) {
      setError("Please select a CSV or Excel file.");
      setResult(null);
      return;
    }

    const fileName = file.name;

    const formData = new FormData();

    formData.append("company_name", companyName.trim());
    formData.append(
      "industry",
      industry.trim() || "Unknown"
    );
    formData.append("file", file);

    try {
      setUploading(true);
      setError("");
      setResult(null);

      const response = await fetch(
        `${API_BASE_URL}/datasets/upload`,
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok) {
        let errorMessage = "Dataset evaluation failed.";

        if (typeof data.detail === "string") {
          errorMessage = data.detail;
        } else if (data.detail?.message) {
          errorMessage = data.detail.message;

          if (data.detail.evaluation?.warnings?.length) {
            errorMessage +=
              " " +
              data.detail.evaluation.warnings.join(" ");
          }
        } else if (data.detail) {
          errorMessage = JSON.stringify(data.detail);
        }

        throw new Error(errorMessage);
      }

      setResult({
        ...data,
        uploadedFileName: fileName
      });

      const newCompanyId = data.company?.id;

      if (newCompanyId) {
        localStorage.setItem(
          "btip_selected_company_id",
          String(newCompanyId)
        );

        if (onCompanyCreated) {
          onCompanyCreated(newCompanyId);
        }
      }

      setFile(null);

    } catch (err) {
      console.error(
        "Dataset upload error:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the backend."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (event) => {
    const selectedFile =
      event.target.files?.[0] || null;

    setFile(selectedFile);
    setResult(null);
    setError("");
  };

  const evaluation = result?.evaluation || {};
  const dataset = result?.dataset || {};
  const company = result?.company || {};

  const warnings = evaluation.warnings || [];
  const detectedColumns =
    evaluation.financial_columns_detected || [];

  const isReady =
    evaluation.status === "ready" &&
    evaluation.sales_revenue_detected === true;

  return (
    <div className="page">

      {/* =================================================
          Page Header
      ================================================= */}

      <div className="page-header">
        <div>
          <h2>Data Upload</h2>
          <p>
            Upload and evaluate financial data before
            running BTIP analysis.
          </p>
        </div>
      </div>

      {/* =================================================
          Upload Card
      ================================================= */}

      <div className="upload-card">

        <div className="upload-card-header">
          <div>
            <h3>Upload Financial Dataset</h3>
            <p>
              CSV or XLSX files are automatically evaluated
              and mapped to BTIP financial fields.
            </p>
          </div>

          <span className="upload-status-badge">
            Step 1
          </span>
        </div>

        {/* Company Name */}

        <div className="upload-field">

          <label htmlFor="company-name">
            Company Name
          </label>

          <input
            id="company-name"
            type="text"
            placeholder="Example: ABC Retail Pvt Ltd"
            value={companyName}
            onChange={(event) => {
              setCompanyName(event.target.value);
              setError("");
            }}
            disabled={uploading}
          />

        </div>

        {/* Industry */}

        <div className="upload-field">

          <label htmlFor="industry">
            Industry
            <span className="optional-label">
              Optional
            </span>
          </label>

          <input
            id="industry"
            type="text"
            placeholder="Example: Retail, IT, Manufacturing"
            value={industry}
            onChange={(event) => {
              setIndustry(event.target.value);
              setError("");
            }}
            disabled={uploading}
          />

        </div>

        {/* Dataset File */}

        <div className="upload-field">

          <label htmlFor="financial-dataset">
            Financial Dataset
          </label>

          <input
            id="financial-dataset"
            type="file"
            accept=".csv,.xlsx"
            onChange={handleFileChange}
            disabled={uploading}
          />

          {file && (
            <div className="selected-file">
              <span>Selected file</span>
              <strong>{file.name}</strong>
            </div>
          )}

        </div>

        {/* Upload Button */}

        <div className="upload-action">

          <button
            onClick={handleUpload}
            disabled={uploading}
          >
            {uploading
              ? "Evaluating Dataset..."
              : "Upload & Evaluate"}
          </button>

        </div>

        {/* Error */}

        {error && (
          <div className="error-message">

            <strong>
              Dataset Evaluation Failed
            </strong>

            <p>{error}</p>

          </div>
        )}

      </div>

      {/* =================================================
          Successful Evaluation
      ================================================= */}

      {result && (
        <div className="dataset-evaluation">

          {/* Evaluation Header */}

          <div className="evaluation-header">

            <div>

              <span className="evaluation-step">
                Step 2
              </span>

              <h3>
                Dataset Evaluation
              </h3>

              <p>
                {result.message ||
                  "Dataset evaluated successfully."}
              </p>

            </div>

            <div
              className={
                isReady
                  ? "evaluation-status ready"
                  : "evaluation-status failed"
              }
            >
              {isReady
                ? "READY FOR ANALYSIS"
                : "REVIEW REQUIRED"}
            </div>

          </div>

          {/* Company Information */}

          <div className="evaluation-company">

            <div className="evaluation-company-avatar">
              {company.name
                ? company.name
                    .charAt(0)
                    .toUpperCase()
                : "C"}
            </div>

            <div>

              <strong>
                {company.name || companyName}
              </strong>

              <span>
                {company.industry ||
                  industry ||
                  "Industry not specified"}
              </span>

            </div>

          </div>

          {/* Dataset Summary */}

          <div className="evaluation-summary">

            <div className="evaluation-summary-card">

              <span>File</span>

              <strong>
                {dataset.filename ||
                  result.uploadedFileName ||
                  "N/A"}
              </strong>

            </div>

            <div className="evaluation-summary-card">

              <span>Rows</span>

              <strong>
                {dataset.rows ?? "N/A"}
              </strong>

            </div>

            <div className="evaluation-summary-card">

              <span>Columns</span>

              <strong>
                {dataset.columns ?? "N/A"}
              </strong>

            </div>

            <div className="evaluation-summary-card">

              <span>Records Added</span>

              <strong>
                {dataset.records_added ?? "N/A"}
              </strong>

            </div>

          </div>

          {/* Detection Results */}

          <div className="evaluation-grid">

            {/* Sales / Revenue */}

            <div className="evaluation-check-card">

              <div className="evaluation-check-icon success">
                ✓
              </div>

              <div>

                <span>
                  Sales / Revenue
                </span>

                <strong>
                  {evaluation.sales_revenue_detected
                    ? "Detected"
                    : "Not Detected"}
                </strong>

              </div>

            </div>

            {/* Period */}

            <div className="evaluation-check-card">

              <div
                className={
                  evaluation.period_detected
                    ? "evaluation-check-icon success"
                    : "evaluation-check-icon warning"
                }
              >
                {evaluation.period_detected
                  ? "✓"
                  : "!"}
              </div>

              <div>

                <span>
                  Period / Date
                </span>

                <strong>
                  {evaluation.period_detected
                    ? "Detected"
                    : "Not Detected"}
                </strong>

              </div>

            </div>

          </div>

          {/* Financial Columns */}

          <div className="evaluation-section">

            <div className="evaluation-section-header">

              <h3>
                Detected Financial Fields
              </h3>

              <span>
                {detectedColumns.length}
              </span>

            </div>

            {detectedColumns.length > 0 ? (
              <div className="detected-fields">

                {detectedColumns.map(
                  (column) => (
                    <span
                      key={column}
                      className="detected-field"
                    >
                      {column
                        .replaceAll("_", " ")
                        .replace(
                          /\b\w/g,
                          (letter) =>
                            letter.toUpperCase()
                        )}
                    </span>
                  )
                )}

              </div>
            ) : (
              <p className="evaluation-empty">
                No additional financial fields detected.
              </p>
            )}

          </div>

          {/* Warnings */}

          {warnings.length > 0 && (
            <div className="evaluation-warnings">

              <div className="warning-heading">
                <span>!</span>

                <strong>
                  Evaluation Notes
                </strong>
              </div>

              <ul>
                {warnings.map(
                  (warning, index) => (
                    <li key={index}>
                      {warning}
                    </li>
                  )
                )}
              </ul>

            </div>
          )}

          {/* Ready State */}

          {isReady && (
            <div className="ready-analysis">

              <div className="ready-icon">
                ✓
              </div>

              <div>

                <strong>
                  Dataset Ready for Analysis
                </strong>

                <p>
                  The uploaded financial data has been
                  evaluated and added to BTIP. The selected
                  company is now available across the
                  Analytics, Crisis, Forecasting,
                  Simulation, Recommendations, Alerts,
                  and Reports modules.
                </p>

              </div>

            </div>
          )}

        </div>
      )}

    </div>
  );
}

export default Datasets;