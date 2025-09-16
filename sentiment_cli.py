# -*- coding: utf-8 -*-
import sys
import argparse
import warnings
from typing import Dict, Any
from openai import OpenAI

# Pretty console
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
except Exception:
    class Dummy:
        RESET_ALL = ""
    class ForeDummy(Dummy):
        RED = GREEN = CYAN = YELLOW = MAGENTA = BLUE = WHITE = ""
    class StyleDummy(Dummy):
        BRIGHT = NORMAL = DIM = ""
    Fore, Style = ForeDummy(), StyleDummy()

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

DEFAULT_MODEL = "meta-llama/llama-4-maverick:free"

SYSTEM_PROMPT = """You are a precise multilingual sentiment analysis engine.
Given a single user-provided sentence, you MUST:
1) Detect sentiment and assign integer probabilities (0-100%) for Positive, Neutral, Negative that sum to 100.
2) Provide a one-line overall label chosen by the highest probability.
3) Provide a concise, evidence-based explanation.
4) Return results in BOTH Traditional Chinese (zh-Hant) and English.

Output JSON only with this schema:
{
  "label": "Positive | Neutral | Negative",
  "scores": { "positive_pct": 0-100, "neutral_pct": 0-100, "negative_pct": 0-100 },
  "analysis_zh_hant": "Concise explanation in Traditional Chinese (繁體中文)",
  "analysis_en": "Concise explanation in English",
  "caveats": "Any caveats or ambiguities in English or Traditional Chinese"
}

Rules:
- Do NOT include any extra text outside the JSON.
- Percentages must be integers that sum to 100.
- Use Traditional Chinese (繁體中文) strictly for the Chinese field (no simplified characters).
- If the sentence is mixed/ambiguous, reflect uncertainty in scores and caveats.
"""

EMOJI_MAP = {
    "Positive": "😀",
    "Neutral": "😐",
    "Negative": "😠"
}

def banner():
    line = "═" * 68
    print(f"{Fore.CYAN}{Style.BRIGHT}╔{line}╗{Style.RESET_ALL}")
    title = "Sentiment Analyzer 情緒分析器 (繁體中文 + English)"
    print(f"{Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL} {title.center(66)} {Fore.CYAN}{Style.BRIGHT}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}╚{line}╝{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.WHITE}- Type one sentence per line to analyze sentiment.")
    print(f"- 每次輸入一句話以進行情緒分析（輸出為繁體中文 + 英文）。")
    print(f"{Fore.WHITE}- Press Ctrl+C or Ctrl+D to exit.")
    print(f"- 按 Ctrl+C 或 Ctrl+D 離開。{Style.RESET_ALL}")

def format_scores_bar(p: int, n: int, neg: int, width: int = 30) -> str:
    total = p + n + neg
    if total == 0:
        p_len = n_len = neg_len = width // 3
    else:
        p_len = round(p / 100 * width)
        n_len = round(n / 100 * width)
        neg_len = width - p_len - n_len
    return (
        f"{Fore.GREEN}{'█' * p_len}{Style.RESET_ALL}"
        f"{Fore.YELLOW}{'█' * n_len}{Style.RESET_ALL}"
        f"{Fore.RED}{'█' * neg_len}{Style.RESET_ALL}"
    )

def analyze_sentiment(client: OpenAI, model: str, text: str) -> Dict[str, Any]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text.strip()}
    ]
    resp = client.chat.completions.create(model=model, messages=messages)
    content = resp.choices[0].message.content.strip()

    import json
    try:
        data = json.loads(content)
        scores = data.get("scores", {})
        p = int(scores.get("positive_pct", 0))
        n = int(scores.get("neutral_pct", 0))
        neg = int(scores.get("negative_pct", 0))

        total = p + n + neg
        if total != 100:
            if total == 0:
                p, n, neg = 34, 33, 33
            else:
                from math import floor
                rp = floor(p * 100 / total)
                rn = floor(n * 100 / total)
                rneg = 100 - rp - rn
                p, n, neg = rp, rn, rneg
            data.setdefault("scores", {})
            data["scores"]["positive_pct"] = p
            data["scores"]["neutral_pct"] = n
            data["scores"]["negative_pct"] = neg

        max_score = max(p, n, neg)
        if (p > n) and (p > neg):
            inferred = "Positive"
        elif (n > p) and (n > neg):
            inferred = "Neutral"
        elif (neg > p) and (neg > n):
            inferred = "Negative"
        else:
            inferred = data.get("label", "Neutral")
        data["label"] = data.get("label", inferred)

        data.setdefault("analysis_zh_hant", "")
        data.setdefault("analysis_en", "")
        data.setdefault("caveats", "")
        return data
    except Exception:
        return {
            "label": "Neutral",
            "scores": {"positive_pct": 33, "neutral_pct": 34, "negative_pct": 33},
            "analysis_zh_hant": "無法解析模型回應格式，暫以中性評估並給出保守分數。",
            "analysis_en": "Could not parse model response. Returning a conservative neutral assessment.",
            "caveats": f"Raw model output: {content[:500]}"
        }

def print_result(result: Dict[str, Any]) -> None:
    label = result.get("label", "Neutral")
    emoji = EMOJI_MAP.get(label, "😐")
    scores = result.get("scores", {})
    p = int(scores.get("positive_pct", 0))
    n = int(scores.get("neutral_pct", 0))
    neg = int(scores.get("negative_pct", 0))
    zh = result.get("analysis_zh_hant", "")
    en = result.get("analysis_en", "")
    cav = result.get("caveats", "")

    color = Fore.GREEN if label == "Positive" else (Fore.YELLOW if label == "Neutral" else Fore.RED)
    print(f"\n{Style.BRIGHT}{color}▶ Overall / 總體判定: {label} {emoji}{Style.RESET_ALL}")

    bar = format_scores_bar(p, n, neg)
    print(f"{Style.BRIGHT}Scores / 百分比{Style.RESET_ALL}: "
          f"{Fore.GREEN}Pos {p}%{Style.RESET_ALL} | "
          f"{Fore.YELLOW}Neu {n}%{Style.RESET_ALL} | "
          f"{Fore.RED}Neg {neg}%{Style.RESET_ALL}")
    print(f"[{bar}]")

    print(f"\n{Style.BRIGHT}{Fore.CYAN}繁體中文分析{Style.RESET_ALL}")
    print(zh if zh else "（無）")
    print(f"\n{Style.BRIGHT}{Fore.CYAN}English Analysis{Style.RESET_ALL}")
    print(en if en else "(None)")

    if cav:
        print(f"\n{Style.BRIGHT}{Fore.MAGENTA}備註 / Caveats{Style.RESET_ALL}")
        print(cav)

    print(f"{Fore.CYAN}{'-' * 72}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="CLI Sentiment Analysis (Traditional Chinese + English) via OpenRouter.")
    parser.add_argument("--api-key", required=True, help="Your OpenRouter API key.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenRouter model name.")
    parser.add_argument("--base-url", default="https://openrouter.ai/api/v1", help="OpenRouter base URL.")
    args = parser.parse_args()

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)

    banner()

    # Bilingual prompts (English + 繁體中文)
    prompt_en = f"{Style.BRIGHT}{Fore.WHITE}Enter a line to analyze:{Style.RESET_ALL} "
    prompt_zh = f"{Style.BRIGHT}{Fore.WHITE}請輸入要分析的句子：{Style.RESET_ALL} "
    turn = 0

    while True:
        try:
            prompt = prompt_en if (turn % 2 == 0) else prompt_zh
            text = input("\n" + prompt).strip()
            turn += 1
            if not text:
                print(f"{Fore.YELLOW}Input is empty. Please try again. / 輸入為空，請再試一次。{Style.RESET_ALL}")
                continue
            result = analyze_sentiment(client, args.model, text)
            print_result(result)
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Bye! 感謝使用，再見！{Style.RESET_ALL}")
            break
        except EOFError:
            print(f"\n{Fore.CYAN}Bye! 感謝使用，再見！{Style.RESETS_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error / 錯誤: {e}{Style.RESET_ALL}", file=sys.stderr)

if __name__ == "__main__":
    main()
