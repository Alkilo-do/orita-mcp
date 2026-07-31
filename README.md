# orita-mcp

<!-- mcp-name: io.github.Alkilo-do/orita-provider-resolution -->

> MCP server for the [Orita Provider Resolution API](https://orita.online) — lets AI agents search a provider network, apply eligibility rules, resolve availability, and safely confirm bookings.

[![PyPI](https://img.shields.io/pypi/v/orita-mcp)](https://pypi.org/project/orita-mcp/)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-listed-teal)](https://registry.modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What this does

Orita resolves the provider-routing problem:

> Your application knows what service the customer needs, but not which professional is eligible and available.

This MCP server exposes that resolution workflow as tools that AI agents (Claude, Cursor, and compatible clients) can call natively.

## Primary workflow

```
resolve_scheduling          → search provider network, return ranked options
hold_scheduling_option      → temporarily reserve the selected slot
confirm_scheduling_resolution → confirm booking after customer approval
```

## Tools

| Tool | Description | Modifies state? |
|------|-------------|-----------------|
| `resolve_scheduling` | Search provider network, apply eligibility rules, return ranked explained options | No |
| `get_resolution` | Retrieve resolution with options, exclusions, and expiry | No |
| `hold_scheduling_option` | Temporarily hold a slot (2 min default, 10 min max) | Application-defined |
| `release_scheduling_option` | Release a held slot | Yes |
| `confirm_scheduling_resolution` | Create the booking after customer approval | **Yes — requires approval** |
| `reschedule_booking` | Move to a new approved slot | **Yes — requires approval** |
| `cancel_booking` | Cancel a booking | **Yes — requires approval** |
| `get_booking` | Retrieve booking details | No |
| `list_professionals` | List providers in the network | No |
| `get_slots` | Get slots for a known provider | No |

## Agent safety

```
✓ resolve_scheduling, get_resolution, list_professionals, get_slots
  → No customer approval required

⚠ hold_scheduling_option
  → Application-defined

✗ confirm_scheduling_resolution, reschedule_booking, cancel_booking
  → Require explicit customer approval before calling
  → Display provider, service, time, timezone, and cancellation policy first
```

**Never** call `confirm_scheduling_resolution` until the customer has explicitly approved:
- Provider name
- Service
- Date and time
- Timezone
- Cancellation policy

## Connect via remote server

```json
{
  "mcpServers": {
    "orita": {
      "url": "https://orita.online/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ORITA_API_KEY"
      }
    }
  }
}
```

> **Note:** Requests must include `Accept: application/json, text/event-stream`. MCP-compatible clients send this automatically.

## Install via PyPI

```bash
pip install orita-mcp
ORITA_API_KEY=orita_... python -m orita_mcp
```

## Get an API key

Free at [orita.online/sign-up](https://orita.online/sign-up) — no credit card. 50 active providers, 5,000 resolutions/month included on the free plan.

## Resources

- [Developer docs](https://orita.online/developers)
- [MCP documentation](https://orita.online/developers/mcp.md)
- [API reference](https://orita.online/developers/reference)
- [OpenAPI spec](https://orita.online/openapi.json)
- [Node.js SDK](https://github.com/Alkilo-do/orita-node)
- [Python SDK](https://github.com/Alkilo-do/orita-python)
