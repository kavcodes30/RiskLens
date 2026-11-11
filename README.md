# 🏥 Insurance Premium Predictor

A machine learning web app that predicts a person's **insurance premium category** from basic personal details such as age, weight, height, income, city, occupation and smoking status.

It is packaged as a **single Docker image**. Pull it, run one command, and the web UI opens ready to use. No Python setup is needed.

---

## ✨ What it does

1. You fill in a simple form (age, weight, height, income, smoker, city, occupation).
2. The app converts your inputs into the features the model needs (BMI, age group, lifestyle risk, city tier).
3. The trained model predicts the premium category.
4. You see the **predicted category**. The backend also returns a confidence score and per-class probabilities.

---

## 🚀 Quick start (Docker)

**Requirement:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

Run this one command:

```bash
docker run -d --name insurance-app -p 8501:8501 --restart unless-stopped kaveri30/insurance-app:latest
```

Then open **http://localhost:8501** in your browser.

Docker downloads the image automatically the first time. You do not need the source code.

### Handy commands

| Task | Command |
|------|---------|
| Check it is running | `docker ps` |
| View logs | `docker logs -f insurance-app` |
| Stop the app | `docker stop insurance-app` |
| Start it again | `docker start insurance-app` |
| Remove the container | `docker rm -f insurance-app` |
| Update to the newest version | `docker pull kaveri30/insurance-app:latest` (then remove and re-run the container) |

> **Port 8501 already in use?** Use another port, for example `-p 9000:8501`, and open http://localhost:9000.

---

## 🧩 How it works

The app has two parts that run **inside one container**:

```
   Your browser
        │
        ▼  (port 8501, the only port exposed)
┌─────────────────────────── Docker container ───────────────────────────┐
│                                                                        │
│   Streamlit frontend  ──────►  FastAPI backend  ──────►  ML model      │
│   (frontend.py)        HTTP    (app.py)                  (model.pkl)   │
│                    127.0.0.1:8000                                      │
│                    (private, not exposed)                              │
└────────────────────────────────────────────────────────────────────────┘
```

| Part | File | Role |
|------|------|------|
| **Frontend** | `frontend.py` | Streamlit form that the user sees and interacts with |
| **Backend** | `app.py` | FastAPI server that validates input and returns predictions |
| **Prediction logic** | `model/predict.py` | Loads the trained model and produces the prediction |
| **Trained model** | `model/model.pkl` | The saved scikit-learn model |
| **Input validation** | `schema/user_input.py` | Validates the form data and computes BMI, age group, lifestyle risk and city tier |
| **Response format** | `schema/prediction_response.py` | Defines the shape of API responses |
| **City tiers** | `config/city_tier.py` | Maps cities to tier categories |
| **Startup script** | `start.sh` | Starts the backend and frontend together inside the container |

The backend listens only on `127.0.0.1` inside the container, so it cannot be reached from outside. Only the UI is available to users.

---

## 📥 Inputs and output

**What you enter in the UI**

| Field | Description |
|-------|-------------|
| Age | Age in years |
| Weight | Weight in kg |
| Height | Height in metres |
| Income (LPA) | Annual income in lakhs per annum |
| Smoker | Yes or no |
| City | Your city (used to derive a city tier) |
| Occupation | retired, student, freelancer, government_job, private_job, business_owner, unemployed |

**What the model uses (computed automatically)**

`bmi`, `age_group`, `lifestyle_risk`, `city_tier`, `income_lpa`, `occupation`

**What you get back**

- `predicted_category`: the premium category
- `confidence`: the probability of the predicted class
- `class_probabilities`: the probability of every category

---

## 🗂️ Project structure

```
insurance_model/
├── app.py                  # FastAPI backend
├── frontend.py             # Streamlit frontend
├── start.sh                # Starts both services in the container
├── Dockerfile              # Builds the single image
├── requirements.txt        # Python dependencies (pinned versions)
├── .dockerignore           # Files excluded from the image
├── insurance.csv           # Training data (not included in the image)
├── config/
│   ├── __init__.py
│   └── city_tier.py
├── model/
│   ├── __init__.py
│   ├── predict.py
│   └── model.pkl
└── schema/
    ├── __init__.py
    ├── user_input.py
    └── prediction_response.py
```

---

## 🛠️ Run locally without Docker (for development)

**Requirements:** Python 3.12 and the packages in `requirements.txt`.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the backend (terminal 1)
python -m uvicorn app:app --reload

# 4. Start the frontend (terminal 2)
streamlit run frontend.py
```

Open **http://localhost:8501** for the UI.

When running locally, the backend is also available at http://localhost:8000. Interactive API docs are at http://localhost:8000/docs.

### API endpoints (local development)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check (status, model version, model loaded) |
| POST | `/predict` | Returns the predicted premium category |

Example request body for `POST /predict`:

```json
{
  "age": 30,
  "weight": 70.0,
  "height": 1.70,
  "income_lpa": 10.0,
  "smoker": false,
  "city": "Pune",
  "occupation": "private_job"
}
```

---

## 🐳 Build and publish your own image

```bash
# Build
docker build -t YOUR_DOCKERHUB_USERNAME/insurance-app:1.0 -t YOUR_DOCKERHUB_USERNAME/insurance-app:latest .

# Test locally
docker run --rm -p 8501:8501 YOUR_DOCKERHUB_USERNAME/insurance-app:1.0

# Push to Docker Hub
docker login
docker push YOUR_DOCKERHUB_USERNAME/insurance-app:1.0
docker push YOUR_DOCKERHUB_USERNAME/insurance-app:latest
```

If you build on one CPU type (for example Intel/AMD) and run on another (for example Apple Silicon), build for both:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t YOUR_DOCKERHUB_USERNAME/insurance-app:latest --push .
```

---

## 🩺 Troubleshooting

| Problem | What to do |
|---------|------------|
| Page does not load | Run `docker ps` and check the container is running, then `docker logs insurance-app` for errors |
| `pull access denied` or `not found` | Check the image name and that the `latest` tag exists on Docker Hub. For a private repo, run `docker login` first |
| "Could not connect to the FastAPI backend" | The backend failed to start. Check `docker logs insurance-app` for an import error |
| Docker build says a file is "not found" | Make sure `app.py`, `frontend.py` and `start.sh` are in the project root, next to the `Dockerfile` |
| Port already in use | Use `-p 9000:8501` and open http://localhost:9000 |
| Cannot open it from another computer | Use `http://MACHINE_IP:8501` and allow inbound TCP port 8501 in the firewall |

---

## 🧰 Tech stack

- **Python 3.12**
- **Streamlit** for the web UI
- **FastAPI** and **Uvicorn** for the backend API
- **scikit-learn**, **pandas** and **NumPy** for the model and data handling
- **Pydantic** for input validation
- **Docker** for packaging and distribution

---

## 📌 Notes

- The model was trained with the library versions pinned in `requirements.txt`. Keep them unchanged, since a different scikit-learn version can break loading `model.pkl`.
- This project is for learning and demonstration. The predictions are not real insurance quotes or financial advice.
