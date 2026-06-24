<div align="center">
<img src="https://github.com/Tech-Psycho95/KhetAI/blob/main/logo/khetAI%20-%20logo.jpg" width="400" height="90%">
</div>

# KhetAI: AI Crop Disease Diagnostic Tool

KhetAI is a full-stack, offline-first web application designed to help Indian farmers diagnose crop diseases using AI. By leveraging a local multimodal AI model, it provides crucial agricultural advice even without an internet connection, breaking down barriers of connectivity and language.

![KhetAI Screenshot](https://i.imgur.com/your-screenshot.png)

## The Problem

A significant portion of India's agricultural community operates in rural areas with limited or no internet access. When crops are affected by diseases or pests, farmers struggle to get timely and accurate advice. This can lead to incorrect treatments, reduced yields, and financial loss. Language barriers further complicate access to expert knowledge.

KhetAI tackles this by:
1.  **Offline First:** Running entirely on a local machine, requiring no internet for its core diagnostic functions.
2.  **AI-Powered Diagnosis:** Using a powerful multimodal AI model to analyze images of crops.
3.  **Multilingual Support:** Providing advice in multiple Indian languages to ensure accessibility.
4.  **Actionable Guidance:** Offering clear, practical steps for treatment, prevention, and local remedies.

## Tech Stack

-   **Backend:** FastAPI (Python)
-   **Frontend:** Plain HTML, CSS, and JavaScript with Tailwind CSS via CDN.
-   **AI Model:** Ollama running `gemma4:e4b` (or a similar multimodal model).

## Setup and Installation

Follow these steps to get KhetAI running on your local machine.

### 1. Install Ollama and Pull the AI Model

First, you need to install Ollama, a tool for running large language models locally.

-   Download and install Ollama from [ollama.com](https://ollama.com/).
-   Once installed, open your terminal and pull the `gemma4:e4b` model. This model is powerful enough for multimodal analysis (image and text) and runs efficiently on consumer hardware.

```bash
ollama pull gemma4:e4b
```

### 2. Set Up the Python Backend

The backend is built with FastAPI.

-   **Clone the repository (or download the files):**
    ```bash
    git clone https://github.com/your-repo/KhetAI.git
    cd agri-advisor
    ```
-   **Create a virtual environment and install dependencies:**
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate it (Windows)
    .\venv\Scripts\activate

    # Activate it (macOS/Linux)
    source venv/bin/activate

    # Install required packages
    pip install "fastapi[all]" uvicorn python-multipart ollama
    ```
-   **Run the backend server:**
    The server will start on `http://localhost:8000`.
    ```bash
    uvicorn main:app --reload
    ```

### 3. Launch the Frontend

The frontend is a single `index.html` file that communicates with the local backend.

-   Simply open the `index.html` file in your web browser.
-   The application will automatically check the status of the backend. If the status dot is green, you are ready to go!

## Why Gemma 4?

The `gemma4` family of models represents a significant step in open-source AI. For the KhetAI project, `gemma4:4b` was chosen for several key reasons:

-   **Multimodality:** It can process both images and text simultaneously, which is essential for analyzing a crop photo and a farmer's question together.
-   **Performance on Local Hardware:** It is optimized to run efficiently on standard CPUs and GPUs, making it accessible without requiring expensive cloud infrastructure.
-   **Strong Reasoning Capabilities:** The model provides detailed and relevant diagnoses, treatment plans, and preventive advice.
-   **Offline Capability:** As it runs locally via Ollama, it enables the core mission of providing a completely offline diagnostic tool.

## Scalability Roadmap

This project is designed with future growth in mind. The following table outlines a potential roadmap for scaling the application.

| Phase | Name                  | Description                                                                                                       | Key Technologies                               |
| :---- | :-------------------- | :---------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| **1** | **Local MVP**         | **(Current Stage)** A fully offline, single-user application running on a local machine.                            | FastAPI, Ollama, HTML/JS                       |
| **2** | **Local Network Hub** | A single powerful machine in a village or community center hosts the app, accessible to others on the local Wi-Fi.  | LAN/WLAN, Bonjour/mDNS for service discovery   |
| **3** | **Hybrid Online**     | The app can optionally sync with a central server to update models, contribute anonymized data, and get new advice. | AWS/Azure, Docker, PostgreSQL/MongoDB          |
| **4** | **Mobile App**        | Native mobile apps (Android/iOS) with offline capabilities, using a lightweight, on-device model for instant triage. | React Native/Flutter, TensorFlow Lite/Core ML  |
| **5** | **Platform Ecosystem**| A full platform with farmer profiles, historical data, regional disease tracking, and a marketplace for supplies.    | Microservices, Kafka, GIS, Advanced Analytics  |

                                                     Built with ❤️ By Shivam
