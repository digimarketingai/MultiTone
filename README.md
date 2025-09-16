# 🤖 MultiTone — Multilingual Sentiment Analyzer (CLI)

本文提供繁體中文與英文版本。 | This document is available in Traditional Chinese and English.

---

### 繁體中文說明 (Traditional Chinese)

**MultiTone** 是一個多語系命令列（CLI）情緒分析工具。您在終端機輸入任何語言的一句話後，MultiTone 會自動辨識語言並呼叫 OpenRouter（透過 OpenAI Python Client）進行分析，輸出：
- 整體情緒標籤與表情符號（😀 正向 / 😐 中性 / 😠 負向）
- 正向／中性／負向的整數百分比（合計 100）
- 以「輸入語言 + 英文」提供精簡且有依據的說明
- 以彩色堆疊條呈現的可讀性結果

依據 OpenRouter 官方頁面，單純的路徑字串「api/v1」不是模型名稱，請務必指定可用的模型（例：`meta-llama/llama-4-maverick:free`）。若該模型不可用，請改用其他支援的模型或至其 Discord 查詢。

#### ✨ 主要功能

- **多語系自動偵測**：自動辨識輸入語言，並同時提供該語言與英文之分析。
- **表情符號與彩色條**：😀 / 😐 / 😠 + 彩色堆疊百分比條，結果一目了然。
- **嚴謹分數規則**：正向／中性／負向百分比為整數且合計 100，並與整體標籤一致。
- **穩健回退**：若模型回傳的 JSON 不合規，會以「中性」作保護性回退並附上備註。
- **安裝簡單**：僅需 `openai` 與 `colorama`。

#### 🚀 快速開始

1. 安裝相依套件
   ```bash
   pip install -r requirements.txt
   ```
   建議 `requirements.txt`：
   ```text
   openai
   colorama
   ```

2. 執行程式
   ```bash
   python sentiment_cli.py --api-key 你的OpenRouter金鑰 --model meta-llama/llama-4-maverick:free
   # 可選：
   # --base-url https://openrouter.ai/api/v1
   ```

3. 使用方式
   - 在提示符輸入一句話並按 Enter。
   - 按 Ctrl+C 或 Ctrl+D 離開。

#### 🧩 範例

輸入：
```text
這次更新很有幫助，但速度還可以再快一點。
```

範例輸出（節錄）：
```text
▶ Overall / 總體判定: Neutral 😐
Scores / 百分比: Pos 35% | Neu 50% | Neg 15%
[██████████████████████████████]

Primary Analysis (zh-Hant)
...（模型產生的繁體中文說明）

English Analysis
... (concise evidence-based explanation)
```

> 注意：顏色與堆疊條需使用支援 UTF-8 的終端機。

#### 🛠️ 設定與注意事項

- 模型（--model）：請指定可用的 OpenRouter 模型（例：`meta-llama/llama-4-maverick:free`）。
- 金鑰（--api-key）：使用你的 OpenRouter API 金鑰。
- 端點（--base-url）：預設 `https://openrouter.ai/api/v1`。
- 安全性：請勿將 API 金鑰提交至版本控制；建議以環境變數或命令列參數提供。

---

### English

**MultiTone** is a multilingual command-line (CLI) sentiment analyzer. Enter any single sentence in your terminal—MultiTone auto-detects the language and calls OpenRouter (via the OpenAI Python client) to analyze it, returning:
- An overall emoji-backed label (😀 Positive / 😐 Neutral / 😠 Negative)
- Integer percentages for Positive/Neutral/Negative that sum to 100
- Concise, evidence-based explanations in the input language + English
- A colorful, stacked percentage bar for readability

Per OpenRouter’s site, the plain path “api/v1” is not a model. Specify a valid model (e.g., `meta-llama/llama-4-maverick:free`). If that model is unavailable, pick another supported one or check their Discord.

#### ✨ Key Features

- **Automatic Language Detection**: Primary explanation in the input language plus an English companion summary.
- **Emojis and Colors**: 😀 / 😐 / 😠 and a colored stacked bar for instant comprehension.
- **Strict Scoring**: Integer Pos/Neu/Neg scores sum to 100 and align with the label.
- **Robust Fallback**: Safe neutral fallback with caveats if the model’s JSON is malformed.
- **Minimal Setup**: Only `openai` and `colorama` are required.

#### 🚀 Quick Start

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
   Suggested `requirements.txt`:
   ```text
   openai
   colorama
   ```

2. Run
   ```bash
   python sentiment_cli.py --api-key YOUR_OPENROUTER_KEY --model meta-llama/llama-4-maverick:free
   # Optional:
   # --base-url https://openrouter.ai/api/v1
   ```

3. Use
   - Type one sentence and press Enter.
   - Press Ctrl+C or Ctrl+D to exit.

#### 🧩 Example

Input:
```text
The support team was helpful, though response time could be faster.
```

Sample output (abbreviated):
```text
▶ Overall / 總體判定: Neutral 😐
Scores / 百分比: Pos 38% | Neu 47% | Neg 15%
[██████████████████████████████]

Primary Analysis (en)
... (model’s explanation in input language)

English Analysis
... (concise evidence-based explanation)
```

> Note: Colors and the bar require a UTF-8 capable terminal.

#### 🛠️ Configuration & Notes

- Model (`--model`): Provide a valid OpenRouter model (e.g., `meta-llama/llama-4-maverick:free`).
- API Key (`--api-key`): Use your OpenRouter API key.
- Endpoint (`--base-url`): Defaults to `https://openrouter.ai/api/v1`.
- Security: Never commit API keys; prefer environment variables or CLI flags.

---

## Security | 安全性

- Never commit API keys to version control.  
  請勿將 API 金鑰提交至版本控制。
- Prefer environment variables or CLI flags.  
  建議使用環境變數或命令列參數傳遞金鑰。
