async function calculateSWP() {
    const button = document.getElementById("calculateButton");
    const statusMessage = document.getElementById("statusMessage");
    const chartLayout = {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(247,250,252,0.65)",
        font: {
            family: "Inter, Segoe UI, Arial, sans-serif",
            color: "#17202f"
        },
        title: {
            font: {
                size: 18,
                color: "#17202f"
            }
        },
        xaxis: {
            gridcolor: "#e5ebf2",
            zerolinecolor: "#dce4ee",
            title: { font: { color: "#68758a" } }
        },
        yaxis: {
            gridcolor: "#e5ebf2",
            zerolinecolor: "#dce4ee",
            title: { font: { color: "#68758a" } }
        },
        legend: {
            orientation: "h",
            y: 1.12,
            x: 0,
            bgcolor: "rgba(255,255,255,0)"
        }
    };
    const chartConfig = {
        responsive: true,
        displayModeBar: false
    };

    button.disabled = true;
    button.textContent = "Calculating...";
    statusMessage.textContent = "Running SWP model and Monte Carlo simulation.";
    statusMessage.className = "status-message";

    const payload = {
        initial_corpus: document.getElementById("initialCorpus").value,
        withdrawal_rate: document.getElementById("withdrawalRate").value,
        inflation_rate: document.getElementById("inflationRate").value,
        years: document.getElementById("years").value,
        simulations: document.getElementById("simulations").value
    };

    try {
        const response = await fetch("/api/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error("Calculation failed. Please check input values.");
        }

        const data = await response.json();

        document.getElementById("staticCorpus").textContent = data.metrics.static_final_corpus;
        document.getElementById("smartCorpus").textContent = data.metrics.smart_final_corpus;
        document.getElementById("survivalProbability").textContent = data.metrics.survival_probability;

        document.getElementById("avgCorpus").textContent = data.monte_carlo.average_final_corpus;
        document.getElementById("medianCorpus").textContent = data.monte_carlo.median_final_corpus;
        document.getElementById("minCorpus").textContent = data.monte_carlo.minimum_final_corpus;
        document.getElementById("maxCorpus").textContent = data.monte_carlo.maximum_final_corpus;
        document.getElementById("avgImprovement").textContent = data.validation.average_improvement;
        document.getElementById("outperformanceRate").textContent = data.validation.outperformance_rate;
        document.getElementById("validationFolds").textContent = data.validation.folds;
        document.getElementById("futureRiskLevel").textContent = data.future_plan.risk_level;
        document.getElementById("futureCurrentDate").textContent = data.future_plan.current_date;
        document.getElementById("futureRecommendation").textContent = data.future_plan.recommendation;
        document.getElementById("nextWithdrawal").textContent = data.future_plan.next_month_withdrawal;
        document.getElementById("futureMarketSignal").textContent = data.future_plan.market_signal;
        document.getElementById("futureGuardFactor").textContent = data.future_plan.guard_factor;
        document.getElementById("futureReason").textContent = `${data.future_plan.reason}. Expected monthly return assumption: ${data.future_plan.expected_monthly_return}.`;

        const validationRows = data.validation.fold_results.map((row) => {
            return `
                <tr>
                    <td>${row.fold}</td>
                    <td>${row.start_date} to ${row.end_date}</td>
                    <td>${row.static_final}</td>
                    <td>${row.smart_final}</td>
                    <td>${row.improvement}</td>
                </tr>
            `;
        }).join("");

        document.getElementById("validationRows").innerHTML = validationRows;

        const futurePlanRows = data.future_plan.plan.map((row) => {
            return `
                <tr>
                    <td>${row.month}</td>
                    <td>${row.date}</td>
                    <td>${row.static_withdrawal}</td>
                    <td>${row.suggested_withdrawal}</td>
                    <td>${row.projected_corpus}</td>
                </tr>
            `;
        }).join("");

        document.getElementById("futurePlanRows").innerHTML = futurePlanRows;

        Plotly.newPlot("corpusChart", [
            {
                x: data.corpus_chart.static_dates,
                y: data.corpus_chart.static,
                type: "scatter",
                mode: "lines",
                name: "Static SWP",
                line: { color: "#3478f6", width: 3 }
            },
            {
                x: data.corpus_chart.smart_dates,
                y: data.corpus_chart.smart,
                type: "scatter",
                mode: "lines",
                name: "Smart SWP",
                line: { color: "#0f9f8f", width: 3 }
            }
        ], {
            ...chartLayout,
            title: "Portfolio Corpus Comparison",
            xaxis: { ...chartLayout.xaxis, title: "Date" },
            yaxis: { ...chartLayout.yaxis, title: "Corpus" },
            margin: { t: 50, r: 30, b: 50, l: 70 }
        }, chartConfig);

        Plotly.newPlot("withdrawalChart", [
            {
                x: data.withdrawal_chart.static_dates,
                y: data.withdrawal_chart.static,
                type: "scatter",
                mode: "lines",
                name: "Static Withdrawal",
                line: { color: "#3478f6", width: 3 }
            },
            {
                x: data.withdrawal_chart.smart_dates,
                y: data.withdrawal_chart.smart,
                type: "scatter",
                mode: "lines",
                name: "Smart Withdrawal",
                line: { color: "#d99a2b", width: 3 }
            }
        ], {
            ...chartLayout,
            title: "Monthly Withdrawal Comparison",
            xaxis: { ...chartLayout.xaxis, title: "Date" },
            yaxis: { ...chartLayout.yaxis, title: "Withdrawal" },
            margin: { t: 50, r: 30, b: 50, l: 70 }
        }, chartConfig);

        Plotly.newPlot("monteCarloChart", [
            {
                x: data.monte_carlo.final_values,
                type: "histogram",
                marker: {
                    color: "#0f9f8f",
                    line: { color: "#ffffff", width: 1 }
                },
                name: "Final Corpus"
            }
        ], {
            ...chartLayout,
            showlegend: false,
            title: "Monte Carlo Final Corpus Distribution",
            xaxis: { ...chartLayout.xaxis, title: "Final Corpus" },
            yaxis: { ...chartLayout.yaxis, title: "Frequency" },
            margin: { t: 50, r: 20, b: 50, l: 60 }
        }, chartConfig);

        statusMessage.textContent = "Calculation complete.";
    } catch (error) {
        statusMessage.textContent = error.message;
        statusMessage.className = "status-message error";
    } finally {
        button.disabled = false;
        button.textContent = "Calculate Strategy";
    }
}

window.onload = calculateSWP;
