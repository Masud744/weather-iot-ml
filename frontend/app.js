// ---------- API URLs ----------
const API_URL = "http://127.0.0.1:8000/api/weather/latest";
const PREDICT_API_URL = "http://127.0.0.1:8000/api/weather/predict";

// ---------- Chart Setup ----------
const ctx = document.getElementById("tempChart").getContext("2d");

const tempChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Live Temperature (°C)",
        data: [],
        borderColor: "#ff6384",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        tension: 0.4,
        fill: true,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      x: {
        title: { display: true, text: "Time" },
      },
      y: {
        title: { display: true, text: "Temperature (°C)" },
      },
    },
  },
});

// ---------- Fetch Live Weather ----------
async function fetchWeather() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    // Update cards
    document.getElementById("time").innerText = data.time;
    document.getElementById("temperature").innerText = data.temperature;
    document.getElementById("humidity").innerText = data.humidity;
    document.getElementById("pressure").innerText = data.pressure;
    document.getElementById("wind_speed").innerText = data.wind_speed;
    document.getElementById("wind_direction").innerText = data.wind_direction;

    document.getElementById("status").innerText = "Live data updated ✔";

    // ---- Chart update (INSIDE try block) ----
    const timeLabel = new Date(data.time).toLocaleTimeString();

    tempChart.data.labels.push(timeLabel);
    tempChart.data.datasets[0].data.push(data.temperature);

    // keep last 20 points only
    if (tempChart.data.labels.length > 20) {
      tempChart.data.labels.shift();
      tempChart.data.datasets[0].data.shift();
    }

    tempChart.update();

  } catch (error) {
    document.getElementById("status").innerText = "Error fetching data ❌";
    console.error("Weather fetch error:", error);
  }
}

// ---------- Fetch ML Prediction ----------
async function fetchPrediction() {
  try {
    const response = await fetch(PREDICT_API_URL);
    const data = await response.json();

    // prediction cards (order matters)
    document.querySelectorAll(".prediction-value")[0].innerText =
      data.temperature + " °C";

    document.querySelectorAll(".prediction-value")[1].innerText =
      data.humidity + " %";

  } catch (error) {
    console.error("Prediction fetch failed:", error);
  }
}

// ---------- Initial Load ----------
fetchWeather();
fetchPrediction();

// ---------- Auto Refresh ----------
setInterval(fetchWeather, 5000);      // live data every 5 sec
setInterval(fetchPrediction, 30000);  // prediction every 30 sec
