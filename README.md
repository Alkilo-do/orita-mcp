# orita-mcp

<!-- mcp-name: io.github.Alkilo-do/orita-provider-resolution -->

> MCP server that exposes the [Orita](https://orita.online) Provider Resolution API as tools for AI agents (Claude, Cursor, and compatible agents).

[![PyPI](https://img.shields.io/pypi/v/orita-mcp)](https://pypi.org/project/orita-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What is this?

`orita-mcp` implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) so that AI agents can:

- **Look up event types** and available booking slots
- **Book appointments** on behalf of users
- **Retrieve or cancel bookings**
- **Browse public profiles** (no auth needed)

All powered by the [Orita scheduling API](https://orita.online/developers).

---

## Install

```bash
pip install orita-mcp
```

---

## Configure

Get your API key from [orita.online/dashboard](https://orita.online/dashboard) → API Keys.

```bash
export ORITA_API_KEY=orita_your_key_here
```

Optional — override the base URL (useful for self-hosted or staging):

```bash
export ORITA_BASE_URL=https://orita.online   # default
```

---

## Run

```bash
# stdio mode (for Claude Desktop, Cursor, etc.)
python -m orita_mcp

# or via the installed script
orita-mcp
```

---

## Claude Desktop integration

Add to your `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "orita": {
      "command": "python",
      "args": ["-m", "orita_mcp"],
      "env": {
        "ORITA_API_KEY": "orita_your_key_here"
      }
    }
  }
}
```

Restart Claude Desktop. You should see the Orita tools available in the tools panel.

---

## Cursor integration

Add to your Cursor MCP config (`.cursor/mcp.json` in your project root, or the global config at `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "orita": {
      "command": "python",
      "args": ["-m", "orita_mcp"],
      "env": {
        "ORITA_API_KEY": "orita_your_key_here"
      }
    }
  }
}
```

Restart Cursor. The Orita tools will be available in Cursor's agent mode.

---

## Smithery

Install and run `orita-mcp` directly via [Smithery](https://smithery.ai/server/gbueno/orita-mcp) without any local setup:

```bash
npx -y @smithery/cli install gbueno/orita-mcp --client claude
```

Or browse the listing and connect directly at **[smithery.ai/server/gbueno/orita-mcp](https://smithery.ai/server/gbueno/orita-mcp)**.

---

## Remote MCP endpoint

Orita also exposes a hosted MCP endpoint — no local install required:

```
https://orita.online/api/mcp
```

Add it directly in any MCP-compatible client that supports remote servers.

---

## Available tools

| Tool | Description | Auth |
|------|-------------|------|
| `orita_get_event_types` | List all event types for your account | ✅ API key |
| `orita_get_slots` | Get available slots for an event type on a date | ✅ API key |
| `orita_book_appointment` | Book an appointment (name, email, time) | ✅ API key |
| `orita_get_booking` | Retrieve booking details by id | ✅ API key |
| `orita_cancel_booking` | Cancel a booking with optional reason | ✅ API key |
| `orita_get_profile` | Get a public Orita profile by username | 🌐 Public |

---

## Example usage (in Claude)

```
What event types do I have set up?
→ orita_get_event_types()

Show me available slots for event type "abc123" on August 15, 2025
→ orita_get_slots("abc123", "2025-08-15")

Book the 10:00am slot for John Doe (john@example.com)
→ orita_book_appointment(...)

Cancel booking xyz789
→ orita_cancel_booking("xyz789", reason="Schedule conflict")
```

---

## Development

```bash
git clone https://github.com/Alkilo-do/orita-mcp
cd orita-mcp
pip install -e ".[dev]"
python -m orita_mcp
```

---

## License

MIT — see [LICENSE](LICENSE).

Built by the [Orita](https://orita.online) team.
