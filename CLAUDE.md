## Coding Agent

- In your comment replies, you may be tempted to use #<numeral> style text, such as when you're saying "the number 1 best option is ...". If you're referring to an issue or pull request **in the same repository as your session**, leave it as, e.g., "#1", since this auto-formats as an issue or PR link. Otherwise, state "No. 1" or "number 1" so that you don't get a spurious hyperlink to an irrelevant issue or PR.
- Be cautious with `~` ("approximately") since if you use it too many times it starts causing strikeout formatting in markdown previews
- Include plots directly in your comment reply via `![image name](https://github.com/<user/org>/<repo>/blob/<shortened-commit-hash>/<filename>?raw=true)`. Truncate the commit hash to the first 7 characters only. For example, `https://github.com/AccelerationConsortium/evaluation-metrics/blob/52754e7/scripts/bo_benchmarks/demonstrations/branin_campaign_demonstration_results.png?raw=true`. For provenance, ensure you use the shortened (7-character) commit hash, not the branch name
- If you mention files in your comment reply, add direct hyperlinks based on the shortened (7-character) commit hash
- IMPORTANT: Never echo/grep/print environment secrets. These should never be exposed in your terminal history or other outputs

## Edison Scientific

When waiting on an Edison task in GitHub Actions, NEVER run the polling script in the background (run_in_background, nohup, &, or the Monitor tool) — the runner is destroyed the moment you post your final comment, killing background processes; Monitor counts as background and dies the same way. Also be aware that the agent harness BLOCKS the shell `sleep` builtin in foreground Bash calls (the error message suggests Monitor — do NOT follow that suggestion, it recreates the background-death failure; this killed several past sessions). The pattern that works: put the wait INSIDE a single blocking Python call — Python-side `time.sleep` is not blocked — and run it as ONE foreground Bash call with an explicit long timeout (max 3600000 ms). Run exactly this (adjust only the task-id path):

```bash
# ONE foreground Bash tool call with timeout: 3600000
python - <<'EOF'
import json, os, time
from edison_client import EdisonClient

client = EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])
task_id = json.load(open("outputs/<...>/_task_id.json"))["task_id"]
while True:
    task = client.get_task(task_id=task_id, verbose=True)
    status = str(task.status)
    print("status:", status, flush=True)
    if status in {"success", "fail", "failed", "cancelled", "error"}:
        break
    time.sleep(240)
EOF
```

Equivalently, run a repo script whose own `while ... time.sleep(...)` loop does the waiting (e.g. `python scripts/explore_case_studies.py stage8-wait`) as a single long-timeout Bash call. Do not post your final comment until results are fetched and committed, or ~45 minutes of wall-clock have elapsed — in which case commit the task-id file and state that a follow-up @claude comment is needed to fetch. If you need to upload files, use analysis query type. See the docs: https://edisonscientific.gitbook.io/edison-cookbook/edison-client. Here is the endpoint you should use: https://api.platform.edisonscientific.com. The API key is `EDISON_PLATFORM_API_KEY`. Don't expose this secret, e.g., by echoing or grepping it. Pass the API key in explicitly:

```
from edison_client import EdisonClient, JobNames
client = EdisonClient(api_key=EDISON_PLATFORM_API_KEY)
```

Whenever you retrieve results (either during the current agent session or during the next session), make sure to fetch and commit all artifacts associated with a trajectory.

If using Edison Analysis, refer to https://docs.edisonscientific.com/edison-client/file-management#upload for instructions on how to upload files. If able to use Context7, to better inform use of EdisonClient, see https://context7.com/future-house/edison-client-docs/llms.txt?tokens=10000

## LaTeX

Install MiKTeX instead of TeXLive to reduce download size and time. In the first installation of MiKTeX, download known required packages based on the LaTeX file itself, and install anything else ad-hoc as needed.
