import os
import sys
import urllib.request
import time

papers = [
    {
        "name": "Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf",
        "url": "https://arxiv.org/pdf/2404.13208.pdf",
        "title": "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions"
    },
    {
        "name": "Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf",
        "url": "https://arxiv.org/pdf/2404.01318.pdf",
        "title": "JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models"
    },
    {
        "name": "Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf",
        "url": "https://arxiv.org/pdf/2310.06474.pdf",
        "title": "Multilingual Jailbreak Challenges in Large Language Models"
    },
    {
        "name": "Angelopoulos_2024_Conformal_Risk_Control.pdf",
        "url": "https://arxiv.org/pdf/2208.02814.pdf",
        "title": "Conformal Risk Control"
    }
]

target_dirs = [
    os.path.abspath("workspaces/truongnv/References"),
    os.path.abspath("Final-Report/References")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("=== STARTING ACADEMIC PAPER DOWNLOAD (4 UPGRADE PAPERS) ===")
for p in papers:
    filename = p["name"]
    url = p["url"]
    print(f"\n[PAPER] {p['title']}")
    print(f"  URL: {url}")
    
    # Download once to first dir, then copy to second dir
    first_target = os.path.join(target_dirs[0], filename)
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            if len(content) < 10000:
                print(f"  [WARNING] File size suspiciously small ({len(content)} bytes). May be error page.")
            else:
                for tdir in target_dirs:
                    os.makedirs(tdir, exist_ok=True)
                    target_path = os.path.join(tdir, filename)
                    with open(target_path, "wb") as f:
                        f.write(content)
                    print(f"  [SAVED] {target_path} ({len(content)} bytes)")
    except Exception as e:
        print(f"  [ERROR] Failed to download {url}: {e}")
    time.sleep(1)

print("\n=== COMPLETED DOWNLOADS ===")
