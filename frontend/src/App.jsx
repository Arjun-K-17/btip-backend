import { useEffect, useState } from "react";

import Dashboard from "./pages/Dashboard";
import Datasets from "./pages/Datasets";
import Analytics from "./pages/Analytics";
import Crisis from "./pages/Crisis";
import Forecasting from "./pages/Forecasting";
import Simulation from "./pages/Simulation";
import Recommendations from "./pages/Recommendations";
import Alerts from "./pages/Alerts";
import Reports from "./pages/Reports";

import AIChatbot from "./components/AIChatbot";


function App() {
  const [activePage, setActivePage] = useState("Dashboard");

  const [companies, setCompanies] = useState([]);

  const [selectedCompanyId, setSelectedCompanyId] = useState(() => {
    const savedId = localStorage.getItem(
      "btip_selected_company_id"
    );

    return savedId
      ? Number(savedId)
      : null;
  });

  const [loadingCompanies, setLoadingCompanies] = useState(true);


  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


  const fetchCompanies = async () => {
    try {
      setLoadingCompanies(true);

      const response = await fetch(
        `${API_BASE_URL}/dashboard/companies`
      );

      if (!response.ok) {
        throw new Error(
          "Unable to load companies."
        );
      }

      const data = await response.json();

      const companyList =
        data.companies || [];

      setCompanies(companyList);


      const savedId = Number(
        localStorage.getItem(
          "btip_selected_company_id"
        )
      );


      const savedCompanyExists =
        companyList.some(
          (company) =>
            company.id === savedId
        );


      if (savedCompanyExists) {

        setSelectedCompanyId(
          savedId
        );

      } else if (
        companyList.length > 0
      ) {

        const firstCompanyId =
          companyList[0].id;

        setSelectedCompanyId(
          firstCompanyId
        );

        localStorage.setItem(
          "btip_selected_company_id",
          String(firstCompanyId)
        );

      } else {

        setSelectedCompanyId(null);

        localStorage.removeItem(
          "btip_selected_company_id"
        );
      }

    } catch (error) {

      console.error(
        "Company loading error:",
        error
      );

    } finally {

      setLoadingCompanies(false);

    }
  };


  useEffect(() => {
    fetchCompanies();
  }, []);


  const handleCompanyCreated = async (
    companyId
  ) => {

    const id = Number(companyId);

    if (!id || id < 1) {
      return;
    }

    await fetchCompanies();

    setSelectedCompanyId(id);

    localStorage.setItem(
      "btip_selected_company_id",
      String(id)
    );

    setActivePage("Dashboard");
  };


  const handleCompanyChange = (
    event
  ) => {

    const companyId = Number(
      event.target.value
    );

    if (!companyId) {
      return;
    }


    const companyExists =
      companies.some(
        (company) =>
          company.id === companyId
      );


    if (!companyExists) {
      return;
    }


    setSelectedCompanyId(
      companyId
    );

    localStorage.setItem(
      "btip_selected_company_id",
      String(companyId)
    );
  };


  const menuItems = [
    "Dashboard",
    "Datasets",
    "Analytics",
    "Crisis Detection",
    "Forecasting",
    "Simulation",
    "Recommendations",
    "Alerts",
    "Reports"
  ];


  const renderPage = () => {

    switch (activePage) {

      case "Dashboard":
        return (
          <Dashboard
            companyId={
              selectedCompanyId
            }
          />
        );


      case "Datasets":
        return (
          <Datasets
            companyId={
              selectedCompanyId
            }
            onCompanyCreated={
              handleCompanyCreated
            }
          />
        );


      case "Analytics":
        return (
          <Analytics
            companyId={
              selectedCompanyId
            }
          />
        );


      case "Crisis Detection":
        return (
          <Crisis
            companyId={
              selectedCompanyId
            }
          />
        );


      case "Forecasting":
        return (
          <Forecasting
            companyId={
              selectedCompanyId
            }
          />
        );


      case "Simulation":
        return (
          <Simulation
            companyId={
              selectedCompanyId
            }
          />
        );


      case "Recommendations":
        return (
          <Recommendations
            companyId={
              selectedCompanyId
            }
          />
        );


      case "Alerts":
        return (
          <Alerts
            companyId={
              selectedCompanyId
            }
          />
        );


      case "Reports":
        return (
          <Reports
            companyId={
              selectedCompanyId
            }
          />
        );


      default:
        return (
          <Dashboard
            companyId={
              selectedCompanyId
            }
          />
        );
    }
  };


  return (
    <div className="app">

      <aside className="sidebar">

        <h2>BTIP</h2>

        <nav>

          {menuItems.map(
            (item) => (
              <p
                key={item}
                className={
                  activePage === item
                    ? "active"
                    : ""
                }
                onClick={() =>
                  setActivePage(item)
                }
              >
                {item}
              </p>
            )
          )}

        </nav>

      </aside>


      <main className="main-content">

        <header className="header">

          <div>

            <h1>
              {activePage}
            </h1>

            <p>
              Business Turnaround
              Intelligence Platform
            </p>

          </div>


          <div className="company-selector">

            <label htmlFor="company-select">
              Company
            </label>

            <select
              id="company-select"
              value={
                selectedCompanyId || ""
              }
              onChange={
                handleCompanyChange
              }
              disabled={
                loadingCompanies ||
                companies.length === 0
              }
            >

              {companies.length === 0 ? (

                <option value="">
                  No companies available
                </option>

              ) : (

                companies.map(
                  (company) => (

                    <option
                      key={company.id}
                      value={company.id}
                    >
                      {company.name}

                      {company.industry
                        ? ` — ${company.industry}`
                        : ""}
                    </option>

                  )
                )

              )}

            </select>

          </div>

        </header>


        <section className="dashboard">

          {renderPage()}

        </section>


        {/* ============================================
            BTIP BUSINESS TURNAROUND ASSISTANT
            ============================================ */}

        <AIChatbot
          companyId={
            selectedCompanyId
          }
        />

      </main>

    </div>
  );
}


export default App;