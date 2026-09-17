import { useEffect, useState } from "react";


function formatCurrency(value) {
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
}


function Forecasting({ companyId }) {

  // =====================================================
  // State
  // =====================================================

  const [company, setCompany] = useState(null);

  const [forecastPeriods, setForecastPeriods] =
    useState(3);

  const [result, setResult] = useState(null);

  const [error, setError] = useState("");

  const [loadingCompany, setLoadingCompany] =
    useState(false);

  const [loading, setLoading] =
    useState(false);


  // =====================================================
  // API Base URL
  // =====================================================

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL;


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

          let message =
            "Unable to verify the selected company.";

          if (typeof data.detail === "string") {
            message = data.detail;
          }

          throw new Error(message);
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
  // Generate Forecast
  // =====================================================

  const handleForecast = async () => {

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

    if (
      !forecastPeriods ||
      forecastPeriods < 1 ||
      forecastPeriods > 12
    ) {
      setError(
        "Forecast periods must be between 1 and 12."
      );
      return;
    }

    try {

      setLoading(true);
      setError("");
      setResult(null);

      const response = await fetch(
        `${API_BASE_URL}/forecast/predict/${companyId}?forecast_periods=${forecastPeriods}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {

        let message =
          "Forecast generation failed.";

        if (typeof data.detail === "string") {
          message = data.detail;
        } else if (data.detail) {
          message = JSON.stringify(
            data.detail
          );
        }

        throw new Error(message);
      }

      setResult(data);

    } catch (err) {

      console.error(
        "Forecast generation error:",
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
  // Data
  // =====================================================

  const historical =
    result?.historical_values || [];

  const predictions =
    result?.predictions || [];

  const allValues = [
    ...historical,
    ...predictions,
  ];

  const maxValue =
    allValues.length > 0
      ? Math.max(...allValues)
      : 1;


  // =====================================================
  // No Company Selected
  // =====================================================

  if (!companyId) {

    return (
      <div className="page">

        <h2>Forecasting</h2>

        <p>
          Generate revenue forecasts using
          historical financial data.
        </p>

        <div className="error-message">

          <strong>
            No Company Selected
          </strong>

          <p>
            Please upload a financial dataset
            before using Forecasting.
          </p>

        </div>

      </div>
    );
  }


  // =====================================================
  // Company Loading
  // =====================================================

  if (loadingCompany) {

    return (
      <div className="page">

        <h2>Forecasting</h2>

        <div className="forecast-control">

          <h3>
            Verifying Company...
          </h3>

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

        <h2>Forecasting</h2>

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
  // Render
  // =====================================================

  return (
    <div className="page">

      {/* =================================================
          Header
      ================================================= */}

      <h2>
        Forecasting
      </h2>

      <p>
        Generate revenue forecasts using
        historical financial data.
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
          Error
      ================================================= */}

      {error && (
        <div className="error-message">

          <strong>
            Forecast Error
          </strong>

          <p>
            {error}
          </p>

        </div>
      )}


      {/* =================================================
          Forecast Controls
      ================================================= */}

      <div className="forecast-control">

        <div>

          <label>
            Selected Company
          </label>

          <input
            type="text"
            value={`${company.name} — ${
              company.industry ||
              "Industry not specified"
            }`}
            readOnly
          />

        </div>


        <div>

          <label>
            Forecast Periods
          </label>

          <input
            type="number"
            min="1"
            max="12"
            value={forecastPeriods}
            onChange={(event) =>
              setForecastPeriods(
                Number(event.target.value)
              )
            }
          />

        </div>


        <button
          onClick={handleForecast}
          disabled={loading}
        >
          {loading
            ? "Generating..."
            : "Generate Forecast"}
        </button>

      </div>


      {/* =================================================
          Results
      ================================================= */}

      {result && (

        <div className="forecast-dashboard">

          {/* =============================================
              Forecast Header
          ============================================= */}

          <div className="forecast-header">

            <div>

              <h3>
                {company.name}
                {" — "}
                Revenue Forecast
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

            <span className="forecast-status">
              Forecast Completed
            </span>

          </div>


          {/* =============================================
              Historical Revenue
          ============================================= */}

          <h3 className="section-title">
            Historical Revenue
          </h3>

          <div className="forecast-cards">

            {historical.map(
              (value, index) => (

                <div
                  className="forecast-card"
                  key={`historical-${index}`}
                >

                  <span>
                    Period {index + 1}
                  </span>

                  <strong>
                    {formatCurrency(value)}
                  </strong>

                </div>

              )
            )}

          </div>


          {/* =============================================
              Forecasted Revenue
          ============================================= */}

          <h3 className="section-title">
            Forecasted Revenue
          </h3>

          <div className="forecast-cards">

            {predictions.map(
              (value, index) => (

                <div
                  className="forecast-card forecast-card-predicted"
                  key={`forecast-${index}`}
                >

                  <span>
                    Forecast Period{" "}
                    {index + 1}
                  </span>

                  <strong>
                    {formatCurrency(value)}
                  </strong>

                </div>

              )
            )}

          </div>


          {/* =============================================
              Revenue Forecast Chart
          ============================================= */}

          <h3 className="section-title">
            Revenue Forecast Chart
          </h3>

          <div
            style={{
              marginTop: "20px",
              backgroundColor: "#ffffff",
              padding: "30px",
              borderRadius: "8px",
              boxShadow:
                "0 2px 6px rgba(0, 0, 0, 0.08)",
              width: "100%",
              overflow: "hidden",
            }}
          >

            <h3
              style={{
                marginBottom: "30px",
                color: "#1f2937",
              }}
            >
              {company.name}
              {" — "}
              Historical vs Forecasted Revenue
            </h3>


            {/* Chart Wrapper */}

            <div
              style={{
                width: "100%",
                overflowX: "auto",
                overflowY: "hidden",
                paddingBottom: "10px",
              }}
            >

              {/* Chart */}

              <div
                style={{
                  minWidth: `${Math.max(
                    allValues.length * 85,
                    700
                  )}px`,
                  height: "420px",
                  display: "flex",
                  alignItems: "flex-end",
                  gap: "18px",
                  padding:
                    "20px 15px 0 15px",
                  borderBottom:
                    "1px solid #d1d5db",
                }}
              >

                {allValues.map(
                  (value, index) => {

                    const isForecast =
                      index >=
                      historical.length;

                    const height =
                      maxValue > 0
                        ? Math.max(
                            (Number(value) /
                              maxValue) *
                              300,
                            15
                          )
                        : 15;

                    const label =
                      isForecast
                        ? `Forecast ${
                            index -
                            historical.length +
                            1
                          }`
                        : `Period ${
                            index + 1
                          }`;

                    return (

                      <div
                        key={index}
                        style={{
                          width: "65px",
                          minWidth: "65px",
                          height: "380px",
                          display: "flex",
                          flexDirection:
                            "column",
                          justifyContent:
                            "flex-end",
                          alignItems:
                            "center",
                        }}
                      >

                        {/* Value */}

                        <div
                          style={{
                            fontSize: "11px",
                            color: "#374151",
                            marginBottom:
                              "8px",
                            whiteSpace:
                              "nowrap",
                          }}
                        >
                          {formatCurrency(
                            value
                          )}
                        </div>


                        {/* Bar */}

                        <div
                          style={{
                            width: "45px",
                            height: `${height}px`,
                            backgroundColor:
                              isForecast
                                ? "#60a5fa"
                                : "#374151",
                            borderRadius:
                              "5px 5px 0 0",
                            transition:
                              "height 0.3s ease",
                          }}
                          title={`${label}: ${formatCurrency(
                            value
                          )}`}
                        />


                        {/* Label */}

                        <div
                          style={{
                            marginTop:
                              "10px",
                            fontSize:
                              "11px",
                            color:
                              "#6b7280",
                            whiteSpace:
                              "nowrap",
                          }}
                        >
                          {label}
                        </div>

                      </div>

                    );
                  }
                )}

              </div>

            </div>


            {/* Legend */}

            <div
              style={{
                display: "flex",
                gap: "30px",
                marginTop: "25px",
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >

              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  fontSize: "13px",
                  color: "#374151",
                }}
              >

                <span
                  style={{
                    width: "13px",
                    height: "13px",
                    backgroundColor:
                      "#374151",
                    borderRadius: "2px",
                    display:
                      "inline-block",
                  }}
                />

                Historical Revenue

              </div>


              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  fontSize: "13px",
                  color: "#374151",
                }}
              >

                <span
                  style={{
                    width: "13px",
                    height: "13px",
                    backgroundColor:
                      "#60a5fa",
                    borderRadius: "2px",
                    display:
                      "inline-block",
                  }}
                />

                Forecasted Revenue

              </div>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}


export default Forecasting;