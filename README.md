# 🎙️ Deepgram Pharmacy Voice Agent

> A real-time AI voice agent that answers pharmacy phone calls — powered by **Deepgram**, **Twilio**, and Python's `asyncio`.

---

## 🚀 Live Demo

> 📞 *Call the demo line or watch the [screen recording](#)* ← *(add your Loom/YouTube link here)*

---

## 🧠 What It Does

This project turns a regular phone number into an intelligent pharmacy assistant. When a customer calls:

1. **Twilio** receives the call and streams raw audio over WebSocket
2. The Python server forwards that audio in real time to **Deepgram's Voice Agent API**
3. Deepgram transcribes speech, runs an LLM, and streams back synthesised audio
4. The agent can **call backend functions** mid-conversation — checking prescriptions, placing orders, verifying drug interactions — and speak the results naturally
5. **Barge-in** is fully supported: the caller can interrupt the agent at any time

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────────┐
                    │          Caller (Phone)             │
                    └──────────────┬──────────────────────┘
                                   │  PSTN / VoIP
                    ┌──────────────▼──────────────────────┐
                    │           Twilio                    │
                    │  (receives call, streams μ-law PCM) │
                    └──────────────┬──────────────────────┘
                                   │  WebSocket (Media Streams)
                    ┌──────────────▼──────────────────────┐
                    │       Python Server (main.py)       │
                    │  asyncio · websockets · 3 coroutines│
                    │  ┌──────────┐  ┌─────────────────┐  │
                    │  │twilio_rx │  │   sts_sender    │  │
                    │  │twilio_tx │  │   sts_receiver  │  │
                    └──┴──────────┴──┴────────┬────────┴──┘
                                              │  WebSocket (WSS)
                    ┌─────────────────────────▼───────────┐
                    │     Deepgram Voice Agent API        │
                    │  (STT → LLM → TTS, function calls)  │
                    └─────────────────────────┬───────────┘
                                              │  FunctionCallRequest JSON
                    ┌─────────────────────────▼───────────┐
                    │       pharmacy_functions.py         │
                    │  get_drug_info · check_prescription │
                    │  request_refill · check_interactions│
                    │  place_order · lookup_order         │
                    │  get_store_info                     │
                    └─────────────────────────────────────┘
```

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🔴 **Real-time streaming** | Bidirectional audio streamed over WebSocket with ~200ms latency |
| 🧩 **Function calling** | Agent invokes Python functions mid-conversation and speaks results |
| 🗣️ **Barge-in support** | Caller can interrupt the agent; Twilio's audio buffer is cleared instantly |
| 💊 **7 pharmacy actions** | Drug info, Rx status, refill requests, interaction checks, orders, store info |
| ⚡ **Async architecture** | Three concurrent coroutines — no blocking I/O anywhere |
| 🔒 **Secure config** | API keys via `.env`, never committed |

---

## 🛠️ Tech Stack

- **Python 3.12** — async/await, `asyncio`, `websockets`
- **Deepgram Voice Agent API** — speech-to-text, LLM, text-to-speech in one WebSocket
- **Twilio Media Streams** — WebSocket-based real-time phone audio
- **`python-dotenv`** — environment variable management
- **`uv`** — fast Python package manager

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.12+
- A [Deepgram](https://deepgram.com) account (free tier works)
- A [Twilio](https://twilio.com) account with a phone number
- [`uv`](https://docs.astral.sh/uv/) installed (`pip install uv`)

### 1 — Clone & install

```bash
git clone https://github.com/muhammadhamza179/DeepgramVoiceAgent-main.git
cd DeepgramVoiceAgent-main
uv sync
```

### 2 — Configure environment

```bash
cp .env.example .env
# then edit .env and add your keys
```

```env
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### 3 — Expose your local server

```bash
# Install ngrok if needed: https://ngrok.com
ngrok http 5000
```

Copy the HTTPS URL (e.g. `https://abc123.ngrok.io`) — you'll need it for Twilio.

### 4 — Configure Twilio

1. In the Twilio Console, go to your phone number settings
2. Under **"A call comes in"**, set the webhook to:
   ```
   https://abc123.ngrok.io/twilio
   ```
   with method `POST`

### 5 — Start the server

```bash
uv run python main.py
```

Call your Twilio number — the agent will answer! 🎉

---

## 📞 What You Can Ask the Agent

Once connected, try phrases like:

- *"What is ibuprofen used for?"*
- *"Check prescription RX-10045"*
- *"I'd like to refill my prescription, it's RX-10331 for Umar Sheikh"*
- *"Are aspirin and ibuprofen safe to take together?"*
- *"I'd like to order acetaminophen"*
- *"What are your store hours at the DHA branch?"*

---

## 📁 Project Structure

```
.
├── main.py                  # WebSocket server — Twilio ↔ Deepgram bridge
├── pharmacy_functions.py    # All callable pharmacy functions + mock data
├── config.json              # Deepgram agent configuration (voice, prompt, tools)
├── .env                     # API keys (never committed)
├── .env.example             # Template for environment variables
└── pyproject.toml           # Dependencies
```

---

## 🔭 Roadmap / Future Improvements

- [ ] Add PostgreSQL backend to replace in-memory mock data
- [ ] Build a real-time web dashboard (FastAPI + WebSocket) showing live transcripts
- [ ] Add patient authentication via SMS one-time passcode
- [ ] Deploy to Railway / Render with a persistent public phone number
- [ ] Add multilingual support (Urdu / Arabic) via Deepgram's language options

---

## 🙋 Author

**Muhammad Hamza**
- GitHub: [@muhammadhamza179](https://github.com/muhammadhamza179)
- LinkedIn: www.linkedin.com/in/muhammad-hamza-23893a176

---

## 📄 License

MIT — free to use, modify, and distribute.
