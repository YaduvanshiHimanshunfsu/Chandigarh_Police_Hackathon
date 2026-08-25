# 🤝 Contributing to PratiBimb Praman

Thank you for your interest in contributing to **PratiBimb Praman**! This project is dedicated to empowering law enforcement and digital forensic examiners with open, mathematically calibrated, and court-admissible synthetic media detection tools.

---

## 📋 Code of Conduct
We are committed to providing a welcoming, inclusive, and harassment-free experience for everyone. Please be respectful and constructive in all communications.

---

## 🛠️ Development Workflow

1. **Fork the Repository** on GitHub.
2. **Clone your Fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pratibimb-praman.git
   cd pratibimb-praman
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set Up Local Environment**:
   ```powershell
   python run.py
   ```
5. **Make your Changes** and write unit tests where appropriate.
6. **Commit with Clear Messages**:
   ```bash
   git commit -m "feat(module): add new forensic analyzer for audio spectral anomalies"
   ```
7. **Push to your Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Open a Pull Request** against the `main` branch.

---

## 📐 Guidelines for Forensic Modules
When adding or improving a forensic analysis module:
- **Calibrated Probability:** All modules must output a score normalized between `0.0` (Authentic) and `1.0` (AI-generated / Tampered).
- **Epistemic Uncertainty:** Provide an internal confidence measure for the sensor to enable proper weighting in the Dempster-Shafer fusion engine.
- **Explainability:** Always return a human-readable `explanation` string and detailed dictionary for courtroom presentation.
- **Zero Heavy Dependencies in Core:** Keep modules resilient to minimal CPU execution environments.

---

## 🧪 Testing
Run backend unit tests before opening a pull request:
```bash
cd backend
pytest tests/
```
