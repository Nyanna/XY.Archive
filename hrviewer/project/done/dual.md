Das Skript `/home/user/xyan/XY.Archiv/hrviewer/run_pipeline.py` soll dual ausgelegt sein und auch auf dem Server laufen können. Das HIVE_REMOTE_DIR muss konfigurierbar sein so wie auch die Download Location von DB_PATH. Auf dem Server arbeitet das Skript direkt im Worktree. Der "pull" entfällt so wie auch das "push" jedoch nicht der "commit". Das kann das Skript auch selbst ermitteln da ein "pull" dort ohne remote natürlich kein Ergebnis liefert. 
SystemInit:  id=6436bd08-ddfa-4180-81bb-88bccce0c8c4, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 4db6-20
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/run_pipeline.py
  reason: "Aktuellen Inhalt des Pipeline-Skripts prüfen, um Dual-Mode (lokal/Server) und konfigurierbare Pfade zu implementieren"
```
/answer 4db6-20 allow
ReasoningToken: 11
Control Request:
```yaml
id: 4db6-21
toolName: ask-user
arguments:
  question: |-
    Kurze Bestätigung zum Design, bevor ich es umsetze:

    1. Konfigurierbarkeit via Umgebungsvariablen (HIVE_REMOTE_DIR, HRV_DB_PATH) plus optionale CLI-Flags (--hive-remote-dir, --db-path) – reicht das, oder soll es ausschließlich über ENV-Variablen laufen?
    2. Server-Erkennung: Ich lasse das Skript automatisch erkennen, dass es "auf dem Server" arbeitet, indem geprüft wird, ob der lokale Hive-Arbeitsordner (HIVE_PATH) mit HIVE_REMOTE_DIR übereinstimmt (dann kein separates Klonen/Pull/Push nötig, nur add+commit). Auf dem Server müsste also z.B. HIVE_PATH (bzw. eine neue Variable dafür) direkt auf HIVE_REMOTE_DIR zeigen. Passt das zu eurem Deployment, oder gibt es ein anderes verlässliches Server-Kennzeichen (z.B. eine Umgebungsvariable wie HRV_SERVER_MODE=1 oder Hostname-Check)?
  reason: "Das Design für Dual-Mode (lokal/Server) und Konfigurierbarkeit der Pfade muss geklärt werden, bevor der bestehende Pipeline-Code sinnvoll angepasst wird, da mehrere gleichwertige Implementierungsvarianten möglich sind."
```
/answer 4db6-21 allow 1. passt, Eigentlich dachte ich eher an robustheit. Wenn pull und push keine Ergebnisse liefern oder kein remote konfiguriert ist können bestimmte Teile konditional ausgeführt werden.
ReasoningToken: 4423
Control Request:
```yaml
id: 4db6-22
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/run_pipeline.py
  old_text: |-
    HERE = Path(__file__).parent
    DB_PATH = HERE / "Gadgetbridge"
    DB_REMOTE_URL = "https://drive.google.com/file/d/1yropB-j0couqP8f-XItaAJm3dVsfgc1t/view?usp=sharing"
    DB_TMP_PATH = DB_PATH.with_suffix(".tmp")

    HIVE_PATH = HERE / "hive"
    HIVE_SSH_KEY = Path("/home/user/.ssh/hivebee")
    HIVE_SSH_USER = "hivebee"
    HIVE_SSH_HOST = "proxy.xyan.icu"
    HIVE_REMOTE_DIR = "/home/admin/hive"
    HIVE_GIT_BRANCH = "master"
  new_text: |-
    HERE = Path(__file__).parent

    # Download location for the Gadgetbridge source DB. Configurable so a server
    # deployment (or any alternate host) can point it at a different path than
    # the default "next to this script".
    DB_PATH = Path(os.environ.get("HRV_DB_PATH", str(HERE / "Gadgetbridge")))
    DB_REMOTE_URL = "https://drive.google.com/file/d/1yropB-j0couqP8f-XItaAJm3dVsfgc1t/view?usp=sharing"
    DB_TMP_PATH = DB_PATH.with_suffix(".tmp")

    # Local working copy of the Hive. On a dev machine this is a separate git
    # clone that is pulled/pushed against the remote below. On the server, this
    # script is meant to run directly inside the Hive worktree itself — in that
    # case simply point HRV_HIVE_PATH at the same directory as HIVE_REMOTE_DIR
    # (or leave both at their respective defaults if they already coincide).
    # Whether a remote sync is possible/necessary is *not* hardcoded via a mode
    # flag; sync_hive() figures it out at runtime by trying it and skipping
    # pull/push gracefully wherever no usable "origin" remote is configured.
    HIVE_PATH = Path(os.environ.get("HRV_HIVE_PATH", str(HERE / "hive")))
    HIVE_SSH_KEY = Path("/home/user/.ssh/hivebee")
    HIVE_SSH_USER = "hivebee"
    HIVE_SSH_HOST = "proxy.xyan.icu"
    # Directory of the Hive git repo on the server. Configurable because it is
    # also used verbatim to build the ssh remote URL for pull/push from a
    # non-server machine.
    HIVE_REMOTE_DIR = os.environ.get("HIVE_REMOTE_DIR", "/home/admin/hive")
    HIVE_GIT_BRANCH = "master"
  reason: HIVE_REMOTE_DIR und DB_PATH konfigurierbar machen via Umgebungsvariablen
```
/answer 4db6-22 allow
ReasoningToken: 2284
Control Request:
```yaml
id: 4db6-23
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/run_pipeline.py
  start: def _git(args
  end: "print(f\"Runtime [git {direction}]: {elapsed:.1f}s\")"
  reason: Aktuellen Stand der git-Sync-Funktionen erneut prüfen vor dem Umbau auf robustes Pull/Push-Handling
```
/answer 4db6-23 allow
Control Request:
```yaml
id: 4db6-24
result:
  structuredContent:
    checksum: 73672f81c751a7d00783098a06cc1b08716ca2ece68407cd87d7b62cb7a2376b
    content: |-
      def _git(args: list[str]) -> None:
          """Run a git command against the local Hive repo, abort pipeline on error."""
          result = subprocess.run(
              ["git", "-c", "protocol.version=2", "-C", str(HIVE_PATH), *args],
              env=HIVE_GIT_ENV,
          )
          if result.returncode != 0:
              print(f"ERROR: git {' '.join(args)} exited with code {result.returncode}. Aborting pipeline.")
              sys.exit(result.returncode)


      def _ensure_hive_repo() -> None:
          """Make sure the local Hive dir is a git repo with `origin` set correctly."""
          HIVE_PATH.mkdir(parents=True, exist_ok=True)
          if not (HIVE_PATH / ".git").exists():
              _git(["init", "-b", HIVE_GIT_BRANCH])

          remote = subprocess.run(
              ["git", "-C", str(HIVE_PATH), "remote", "get-url", "origin"],
              env=HIVE_GIT_ENV, capture_output=True, text=True,
          )
          if remote.returncode != 0:
              _git(["remote", "add", "origin", HIVE_GIT_REMOTE_URL])
          elif remote.stdout.strip() != HIVE_GIT_REMOTE_URL:
              _git(["remote", "set-url", "origin", HIVE_GIT_REMOTE_URL])


      def sync_hive(direction: str) -> None:
          """Sync the local Hive with the remote Git repo over ssh.

          direction="pull": fetch + fast-forward the local Hive before running.
          direction="push": commit local changes and push them. HIVE_REMOTE_DIR is
          a non-bare checkout on the server with receive.denyCurrentBranch set to
          updateInstead, so `git push` alone already updates its worktree to match
          the new HEAD — no separate remote checkout step is needed.
          """
          _ensure_hive_repo()
          print(f"Syncing Hive ({direction}) via git: {HIVE_PATH} <-> {HIVE_GIT_REMOTE_URL}")
          t = time.monotonic()

          if direction == "pull":
              _git(["pull", "--ff-only", "origin", HIVE_GIT_BRANCH])
          elif direction == "push":
              _git(["add", "-A"])
              status = subprocess.run(
                  ["git", "-C", str(HIVE_PATH), "status", "--porcelain"],
                  env=HIVE_GIT_ENV, capture_output=True, text=True,
              )
              if status.stdout.strip():
                  _git(["commit", "-m", f"pipeline sync {time.strftime('%Y-%m-%d %H:%M:%S')}"])
              else:
                  print("No local Hive changes to commit.")
              _git(["push", "origin", HIVE_GIT_BRANCH])
          else:
              raise ValueError(f"invalid direction: {direction}")

          elapsed = time.monotonic() - t
          print(f"Runtime [git {direction}]: {elapsed:.1f}s")
```
/answer 4db6-24 allow
ReasoningToken: 587
Control Request:
```yaml
id: 4db6-25
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/run_pipeline.py
  old_text: |-
    def _git(args: list[str]) -> None:
        """Run a git command against the local Hive repo, abort pipeline on error."""
        result = subprocess.run(
            ["git", "-c", "protocol.version=2", "-C", str(HIVE_PATH), *args],
            env=HIVE_GIT_ENV,
        )
        if result.returncode != 0:
            print(f"ERROR: git {' '.join(args)} exited with code {result.returncode}. Aborting pipeline.")
            sys.exit(result.returncode)


    def _ensure_hive_repo() -> None:
        """Make sure the local Hive dir is a git repo with `origin` set correctly."""
        HIVE_PATH.mkdir(parents=True, exist_ok=True)
        if not (HIVE_PATH / ".git").exists():
            _git(["init", "-b", HIVE_GIT_BRANCH])

        remote = subprocess.run(
            ["git", "-C", str(HIVE_PATH), "remote", "get-url", "origin"],
            env=HIVE_GIT_ENV, capture_output=True, text=True,
        )
        if remote.returncode != 0:
            _git(["remote", "add", "origin", HIVE_GIT_REMOTE_URL])
        elif remote.stdout.strip() != HIVE_GIT_REMOTE_URL:
            _git(["remote", "set-url", "origin", HIVE_GIT_REMOTE_URL])


    def sync_hive(direction: str) -> None:
        """Sync the local Hive with the remote Git repo over ssh.

        direction="pull": fetch + fast-forward the local Hive before running.
        direction="push": commit local changes and push them. HIVE_REMOTE_DIR is
        a non-bare checkout on the server with receive.denyCurrentBranch set to
        updateInstead, so `git push` alone already updates its worktree to match
        the new HEAD — no separate remote checkout step is needed.
        """
        _ensure_hive_repo()
        print(f"Syncing Hive ({direction}) via git: {HIVE_PATH} <-> {HIVE_GIT_REMOTE_URL}")
        t = time.monotonic()

        if direction == "pull":
            _git(["pull", "--ff-only", "origin", HIVE_GIT_BRANCH])
        elif direction == "push":
            _git(["add", "-A"])
            status = subprocess.run(
                ["git", "-C", str(HIVE_PATH), "status", "--porcelain"],
                env=HIVE_GIT_ENV, capture_output=True, text=True,
            )
            if status.stdout.strip():
                _git(["commit", "-m", f"pipeline sync {time.strftime('%Y-%m-%d %H:%M:%S')}"])
            else:
                print("No local Hive changes to commit.")
            _git(["push", "origin", HIVE_GIT_BRANCH])
        else:
            raise ValueError(f"invalid direction: {direction}")

        elapsed = time.monotonic() - t
        print(f"Runtime [git {direction}]: {elapsed:.1f}s")
  new_text: |-
    def _git(args: list[str]) -> None:
        """Run a git command against the local Hive repo, abort pipeline on error."""
        result = subprocess.run(
            ["git", "-c", "protocol.version=2", "-C", str(HIVE_PATH), *args],
            env=HIVE_GIT_ENV,
        )
        if result.returncode != 0:
            print(f"ERROR: git {' '.join(args)} exited with code {result.returncode}. Aborting pipeline.")
            sys.exit(result.returncode)


    def _git_soft(args: list[str]) -> bool:
        """Run a git command against the local Hive repo without aborting the pipeline.

        Used for the remote-facing operations (pull/push) so that a missing or
        unreachable `origin` — as is the case when this script runs directly
        inside the server's own Hive worktree (HIVE_PATH == HIVE_REMOTE_DIR) —
        is treated as "nothing to sync" rather than a fatal error. Returns
        whether the command succeeded.
        """
        result = subprocess.run(
            ["git", "-c", "protocol.version=2", "-C", str(HIVE_PATH), *args],
            env=HIVE_GIT_ENV,
        )
        return result.returncode == 0


    def _origin_configured() -> bool:
        """Whether the local Hive repo has a usable `origin` remote to sync with."""
        remote = subprocess.run(
            ["git", "-C", str(HIVE_PATH), "remote", "get-url", "origin"],
            env=HIVE_GIT_ENV, capture_output=True, text=True,
        )
        return remote.returncode == 0 and bool(remote.stdout.strip())


    def _same_path(a: Path, b: Path) -> bool:
        try:
            return a.resolve() == b.resolve()
        except OSError:
            return str(a) == str(b)


    def _ensure_hive_repo() -> None:
        """Make sure the local Hive dir is a git repo, wiring up `origin` if useful.

        When HIVE_PATH already *is* HIVE_REMOTE_DIR (the server running this
        script directly inside its own Hive worktree), configuring an `origin`
        pointing at itself over ssh would be pointless, so it is skipped — the
        pull/push steps in sync_hive() then naturally find nothing to sync
        against and skip themselves too.
        """
        HIVE_PATH.mkdir(parents=True, exist_ok=True)
        if not (HIVE_PATH / ".git").exists():
            _git(["init", "-b", HIVE_GIT_BRANCH])

        if _same_path(HIVE_PATH, Path(HIVE_REMOTE_DIR)):
            return

        remote = subprocess.run(
            ["git", "-C", str(HIVE_PATH), "remote", "get-url", "origin"],
            env=HIVE_GIT_ENV, capture_output=True, text=True,
        )
        if remote.returncode != 0:
            _git(["remote", "add", "origin", HIVE_GIT_REMOTE_URL])
        elif remote.stdout.strip() != HIVE_GIT_REMOTE_URL:
            _git(["remote", "set-url", "origin", HIVE_GIT_REMOTE_URL])


    def sync_hive(direction: str) -> None:
        """Sync the local Hive with the remote Git repo over ssh — robustly.

        direction="pull": fetch + fast-forward the local Hive before running, if
        an `origin` remote is configured and reachable. Otherwise this is a
        no-op (e.g. on the server, which works directly in the worktree and has
        nothing to pull from).

        direction="push": always commits local changes (this must succeed), but
        only pushes them if `origin` is configured and reachable. HIVE_REMOTE_DIR
        is a non-bare checkout on the server with receive.denyCurrentBranch set
        to updateInstead, so `git push` alone already updates its worktree to
        match the new HEAD — no separate remote checkout step is needed. On the
        server itself there is no `origin` to push to, so the push is skipped
        and the commit stands as the only effect.
        """
        _ensure_hive_repo()
        t = time.monotonic()

        if direction == "pull":
            if not _origin_configured():
                print("No Hive `origin` remote configured — skipping pull (nothing to sync from).")
                return
            print(f"Syncing Hive (pull) via git: {HIVE_PATH} <- {HIVE_GIT_REMOTE_URL}")
            if not _git_soft(["pull", "--ff-only", "origin", HIVE_GIT_BRANCH]):
                print("WARNING: Hive pull failed/unavailable — continuing without it.")
        elif direction == "push":
            _git(["add", "-A"])
            status = subprocess.run(
                ["git", "-C", str(HIVE_PATH), "status", "--porcelain"],
                env=HIVE_GIT_ENV, capture_output=True, text=True,
            )
            if status.stdout.strip():
                _git(["commit", "-m", f"pipeline sync {time.strftime('%Y-%m-%d %H:%M:%S')}"])
            else:
                print("No local Hive changes to commit.")

            if not _origin_configured():
                print("No Hive `origin` remote configured — skipping push (nothing to sync to).")
                return
            print(f"Syncing Hive (push) via git: {HIVE_PATH} -> {HIVE_GIT_REMOTE_URL}")
            if not _git_soft(["push", "origin", HIVE_GIT_BRANCH]):
                print("WARNING: Hive push failed/unavailable — commit was kept locally.")
        else:
            raise ValueError(f"invalid direction: {direction}")

        elapsed = time.monotonic() - t
        print(f"Runtime [git {direction}]: {elapsed:.1f}s")
  reason: "sync_hive robust gestalten: pull/push nur bei konfiguriertem/erreichbarem Remote, commit bleibt immer erhalten (Serverbetrieb direkt im Worktree)"
```
/answer 4db6-25 allow
Control Request:
```yaml
id: 4db6-26
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/run_pipeline.py
  start: "def main() -> None:"
  reason: "main()-Funktion einsehen, um CLI-Overrides für HIVE_REMOTE_DIR und DB_PATH zu ergänzen"
```
/answer 4db6-26 allow
Control Request:
```yaml
id: 4db6-27
result:
  structuredContent:
    checksum: 48b84e172de22b7a8c45924ac91494e71223b604e756667836fb19acb26b6aac
    content: |
      def main() -> None:
          parser = argparse.ArgumentParser(add_help=False)
          parser.add_argument(
              "--db",
              nargs="+",
              type=Path,
              metavar="DB_FILE",
              help=(
                  "Process one or more local Gadgetbridge SQLite files in sequence "
                  "instead of the default DB (supports shell wildcards, e.g. "
                  "--db /path/to/*.db). Skips the remote download step."
              ),
          )
          args, passthrough_args = parser.parse_known_args()

          t_total = time.monotonic()

          sync_hive("pull")

          if args.db:
              db_files = sorted(args.db)
              print(f"Processing {len(db_files)} local database file(s), download skipped.")
              for i, db_file in enumerate(db_files, start=1):
                  print(f"\n=== [{i}/{len(db_files)}] {db_file} ===")
                  if not db_file.exists():
                      print(f"ERROR: database file not found: {db_file}")
                      sys.exit(1)
                  run_pipeline_once(db_file, passthrough_args)
          else:
              t_download = ensure_db()
              if t_download > 0:
                  print(f"Download time: {t_download:.1f}s")
              run_pipeline_once(DB_PATH, passthrough_args)

          sync_hive("push")

          print(f"\nTotal time: {time.monotonic() - t_total:.1f}s")


      if __name__ == "__main__":
          main()
```
/answer 4db6-27 allow
Control Request:
```yaml
id: 4db6-28
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/run_pipeline.py
  old_text: |-
    def main() -> None:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "--db",
            nargs="+",
            type=Path,
            metavar="DB_FILE",
            help=(
                "Process one or more local Gadgetbridge SQLite files in sequence "
                "instead of the default DB (supports shell wildcards, e.g. "
                "--db /path/to/*.db). Skips the remote download step."
            ),
        )
        args, passthrough_args = parser.parse_known_args()

        t_total = time.monotonic()
  new_text: |-
    def main() -> None:
        global DB_PATH, DB_TMP_PATH, HIVE_REMOTE_DIR, HIVE_GIT_REMOTE_URL

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "--db",
            nargs="+",
            type=Path,
            metavar="DB_FILE",
            help=(
                "Process one or more local Gadgetbridge SQLite files in sequence "
                "instead of the default DB (supports shell wildcards, e.g. "
                "--db /path/to/*.db). Skips the remote download step."
            ),
        )
        parser.add_argument(
            "--db-path",
            type=Path,
            metavar="PATH",
            help=(
                "Download location for the Gadgetbridge DB (overrides "
                "HRV_DB_PATH / the default 'Gadgetbridge' next to this script)."
            ),
        )
        parser.add_argument(
            "--hive-remote-dir",
            metavar="DIR",
            help=(
                "Hive git repo directory on the server (overrides HIVE_REMOTE_DIR). "
                "Used both to build the ssh remote URL and, if it matches the "
                "local Hive working dir, to detect server-side operation."
            ),
        )
        args, passthrough_args = parser.parse_known_args()

        if args.db_path:
            DB_PATH = args.db_path
            DB_TMP_PATH = DB_PATH.with_suffix(".tmp")
        if args.hive_remote_dir:
            HIVE_REMOTE_DIR = args.hive_remote_dir
            HIVE_GIT_REMOTE_URL = f"{HIVE_SSH_USER}@{HIVE_SSH_HOST}:{HIVE_REMOTE_DIR}"

        t_total = time.monotonic()
  reason: "CLI-Overrides --db-path und --hive-remote-dir ergänzen, die die env-basierten Defaults überschreiben"
```
/answer 4db6-28 allow
Control Request:
```yaml
id: 4db6-29
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  script: python3 -m py_compile run_pipeline.py && echo OK
  reason: Syntaxprüfung des geänderten Pipeline-Skripts
```
/answer 4db6-29 allow
Control Request:
```yaml
id: 4db6-2a
result:
  structuredContent:
    stdout: |
      OK
```
/answer 4db6-2a allow
Control Request:
```yaml
id: 4db6-2b
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  script: grep -n "HIVE_REMOTE_DIR\|HRV_DB_PATH\|HRV_HIVE_PATH\|def sync_hive\|def _ensure_hive_repo\|def _same_path\|def _origin_configured" run_pipeline.py
  reason: Finale Übersicht der geänderten Stellen zur Kontrolle
```
/answer 4db6-2b allow
Control Request:
```yaml
id: 4db6-2c
result:
  structuredContent:
    stdout: |
      24:DB_PATH = Path(os.environ.get("HRV_DB_PATH", str(HERE / "Gadgetbridge")))
      31:# case simply point HRV_HIVE_PATH at the same directory as HIVE_REMOTE_DIR
      36:HIVE_PATH = Path(os.environ.get("HRV_HIVE_PATH", str(HERE / "hive")))
      43:HIVE_REMOTE_DIR = os.environ.get("HIVE_REMOTE_DIR", "/home/admin/hive")
      48:HIVE_GIT_REMOTE_URL = f"{HIVE_SSH_USER}@{HIVE_SSH_HOST}:{HIVE_REMOTE_DIR}"
      75:    inside the server's own Hive worktree (HIVE_PATH == HIVE_REMOTE_DIR) —
      86:def _origin_configured() -> bool:
      95:def _same_path(a: Path, b: Path) -> bool:
      102:def _ensure_hive_repo() -> None:
      105:    When HIVE_PATH already *is* HIVE_REMOTE_DIR (the server running this
      115:    if _same_path(HIVE_PATH, Path(HIVE_REMOTE_DIR)):
      128:def sync_hive(direction: str) -> None:
      137:    only pushes them if `origin` is configured and reachable. HIVE_REMOTE_DIR
      245:    global DB_PATH, DB_TMP_PATH, HIVE_REMOTE_DIR, HIVE_GIT_REMOTE_URL
      265:            "HRV_DB_PATH / the default 'Gadgetbridge' next to this script)."
      272:            "Hive git repo directory on the server (overrides HIVE_REMOTE_DIR). "
      283:        HIVE_REMOTE_DIR = args.hive_remote_dir
      284:        HIVE_GIT_REMOTE_URL = f"{HIVE_SSH_USER}@{HIVE_SSH_HOST}:{HIVE_REMOTE_DIR}"
```
/answer 4db6-2c allow
ReasoningToken: 9
ReasoningToken: 278
ReasoningToken: 89
Text:
 Jetzt kurz prüfen, ob das Skript syntaktisch sauber ist und die Kernlogik konsistent bleibt.
ReasoningToken: 43
Alles kompiliert sauber und die Änderungen sind konsistent. Zusammenfassung der Anpassungen in `run_pipeline.py`:

**Konfigurierbarkeit**
- `HIVE_REMOTE_DIR`: jetzt über die Umgebungsvariable `HIVE_REMOTE_DIR` (Default weiterhin `/home/admin/hive`) sowie zusätzlich per CLI-Flag `--hive-remote-dir` überschreibbar.
- Download-Ziel der DB (`DB_PATH`): über `HRV_DB_PATH` bzw. `--db-path` konfigurierbar (Default weiterhin `Gadgetbridge` neben dem Skript).
- Neu auch `HRV_HIVE_PATH` für den lokalen Hive-Arbeitsordner – auf dem Server zeigt man ihn einfach direkt auf denselben Pfad wie `HIVE_REMOTE_DIR`.

**Dual-Mode ohne explizites Server-Flag (robuste Selbstermittlung)**
- `_ensure_hive_repo()`: richtet `origin` gar nicht erst ein, wenn `HIVE_PATH` (per Pfadauflösung) mit `HIVE_REMOTE_DIR` übereinstimmt – auf dem Server macht ein SSH-Remote auf sich selbst keinen Sinn.
- `sync_hive("pull")`: prüft zuerst, ob überhaupt ein `origin`-Remote konfiguriert ist. Fehlt es (Server-Fall) oder schlägt der Pull fehl, wird das nur als Warnung geloggt und die Pipeline läuft weiter – kein harter Abbruch mehr.
- `sync_hive("push")`: `add` + `commit` laufen **immer** (auch im Server-Betrieb direkt im Worktree). Der eigentliche `git push` wird nur versucht, wenn ein `origin` konfiguriert ist, und schlägt er fehl, bleibt es bei einer Warnung statt Abbruch – der Commit bleibt lokal erhalten.
- Damit „ermittelt das Skript selbst“, ob Pull/Push sinnvoll sind, statt sich auf einen expliziten Modus-Schalter zu verlassen – genau wie gewünscht.

Kein Verhalten wurde für den bisherigen lokalen Ablauf geändert (Pull vor, Push nach der Pipeline, Commit-Message identisch).
