---
name: add-eclipse-mcp
description: Register the Eclipse MCP server suite (eclipse-ide, duck-duck-search, time, webpage-reader, memory, eclipse-coder, eclipse-runner, eclipse-context, eclipse-git, eclipse-pde) for this project. Prompts for a bearer token and writes project-scoped .mcp.json HTTP server entries. Use when the user wants to add, install, configure, or re-add the Eclipse MCP servers / localhost:18080/mcp endpoints.
---

# Add Eclipse MCP servers

Registers the ten Eclipse MCP HTTP servers as **project-scoped** entries in
`.mcp.json` at the repo root. All endpoints live behind one local gateway at
`http://localhost:18080/mcp/<name>` and share a single bearer token sent as an
`Authorization: Bearer …` header.

## Endpoints

| Server name      | URL                                          |
| ---------------- | -------------------------------------------- |
| `eclipse-ide`    | `http://localhost:18080/mcp/eclipse-ide`     |
| `duck-duck-search` | `http://localhost:18080/mcp/duck-duck-search` |
| `time`           | `http://localhost:18080/mcp/time`            |
| `webpage-reader` | `http://localhost:18080/mcp/webpage-reader`  |
| `memory`         | `http://localhost:18080/mcp/memory`          |
| `eclipse-coder`  | `http://localhost:18080/mcp/eclipse-coder`   |
| `eclipse-runner` | `http://localhost:18080/mcp/eclipse-runner`  |
| `eclipse-context`| `http://localhost:18080/mcp/eclipse-context` |
| `eclipse-git`    | `http://localhost:18080/mcp/eclipse-git`     |
| `eclipse-pde`    | `http://localhost:18080/mcp/eclipse-pde`     |

## Steps

1. **Ask for the bearer token.** Use `AskUserQuestion` (or a plain prompt) to
   collect the token. Never echo it back in full. If the user already exported
   `ECLIPSE_MCP_BEARER` in their environment and wants to reuse it, skip the
   write in step 3 and keep the `${ECLIPSE_MCP_BEARER}` placeholder.

2. **Keep the secret out of git.** The token must NOT be committed. Ensure
   `.gitignore` contains `/.claude/settings.local.json` (add the line if
   missing). The real token goes into `.claude/settings.local.json`, the
   committed `.mcp.json` only references it via `${ECLIPSE_MCP_BEARER}`.

3. **Store the token locally.** Merge an `env` block into
   `.claude/settings.local.json` (read the existing file first, preserve all
   other keys):

   ```json
   {
     "env": {
       "ECLIPSE_MCP_BEARER": "<token from step 1>"
     }
   }
   ```

4. **Write `.mcp.json`.** Read any existing `.mcp.json` first and merge into its
   `mcpServers` object (do not clobber unrelated servers). Each Eclipse entry
   uses HTTP transport with the bearer header:

   ```json
   {
     "mcpServers": {
       "eclipse-ide": {
         "type": "http",
         "url": "http://localhost:18080/mcp/eclipse-ide",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "duck-duck-search": {
         "type": "http",
         "url": "http://localhost:18080/mcp/duck-duck-search",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "time": {
         "type": "http",
         "url": "http://localhost:18080/mcp/time",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "webpage-reader": {
         "type": "http",
         "url": "http://localhost:18080/mcp/webpage-reader",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "memory": {
         "type": "http",
         "url": "http://localhost:18080/mcp/memory",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "eclipse-coder": {
         "type": "http",
         "url": "http://localhost:18080/mcp/eclipse-coder",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "eclipse-runner": {
         "type": "http",
         "url": "http://localhost:18080/mcp/eclipse-runner",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "eclipse-context": {
         "type": "http",
         "url": "http://localhost:18080/mcp/eclipse-context",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "eclipse-git": {
         "type": "http",
         "url": "http://localhost:18080/mcp/eclipse-git",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       },
       "eclipse-pde": {
         "type": "http",
         "url": "http://localhost:18080/mcp/eclipse-pde",
         "headers": { "Authorization": "Bearer ${ECLIPSE_MCP_BEARER}" }
       }
     }
   }
   ```

5. **Approve the servers and allow their tools.** Writing `.mcp.json` alone is
   **not enough** — the servers stay `⏸ Pending approval` and never connect.
   The interactive "New MCP servers found" prompt is unreliable and may **never
   appear at all** — observed in practice even on a fresh session start with the
   servers showing `⏸ Pending approval`. So do **not** rely on it. Instead set
   both gates explicitly in `.claude/settings.local.json` (merge, preserve
   existing keys). These two keys are independent:

   - `enabledMcpjsonServers` — the **approval/load** gate that clears
     `Pending approval` and lets the servers connect.
   - `permissions.allow` entries `mcp__<server>` — the **tool-permission** gate
     that lets their tool calls run without a per-call prompt.

   ```json
   {
     "enabledMcpjsonServers": [
       "eclipse-ide", "duck-duck-search", "time", "webpage-reader", "memory",
       "eclipse-coder", "eclipse-runner", "eclipse-context", "eclipse-git", "eclipse-pde"
     ],
     "permissions": {
       "allow": [
         "mcp__eclipse-ide", "mcp__duck-duck-search", "mcp__time",
         "mcp__webpage-reader", "mcp__memory", "mcp__eclipse-coder",
         "mcp__eclipse-runner", "mcp__eclipse-context", "mcp__eclipse-git",
         "mcp__eclipse-pde"
       ]
     }
   }
   ```

   Set these in the project-local `settings.local.json` rather than
   `~/.claude.json`: the local settings file is only read (not rewritten on
   exit), so the edit survives even if a Claude Code session is currently
   running, and it stays project-scoped.

6. **Tell the user to reload.** A full Claude Code restart is the reliable way to
   pick up the new servers and approvals. Verify with `claude mcp list` or the
   `/mcp` command — each server should show **connected** instead of
   `⏸ Pending approval`.

## Notes

- The `${ECLIPSE_MCP_BEARER}` expansion is resolved by Claude Code from the
  environment; the `env` block in `settings.local.json` provides it. If the user
  prefers, they can instead export it in their shell rc and skip step 3.
- All servers share one token because they sit behind the same gateway; rotating
  the token means changing only the single `env` value.
- If the gateway is down, servers show **failed**; start the local Eclipse MCP
  gateway on port `18080` first.
