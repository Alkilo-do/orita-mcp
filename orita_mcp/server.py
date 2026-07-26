"""
Orita MCP Server

Exposes the Orita scheduling API (https://orita.online/api/v1) as MCP tools
so AI agents (Claude, GPT, etc.) can book, query, and cancel appointments.

Configuration via environment variables:
  ORITA_API_KEY   — your Orita API key (required for authenticated endpoints)
  ORITA_BASE_URL  — override base URL (default: https://orita.online)
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = os.environ.get("ORITA_BASE_URL", "https://orita.online").rstrip("/")
API_KEY = os.environ.get("ORITA_API_KEY", "")

mcp = FastMCP(
    name="orita",
    instructions=(
        "You have access to the Orita scheduling API. "
        "Use these tools to look up event types and available slots, "
        "book appointments, retrieve booking details, and cancel bookings. "
        "orita_get_profile requires only a username (public). "
        "All other tools require ORITA_API_KEY to be set in the environment."
    ),
)


def _auth_headers() -> dict:
    """Return authorization headers. Raises if API key is not configured."""
    if not API_KEY:
        raise ValueError(
            "ORITA_API_KEY environment variable is not set. "
            "Export your Orita API key before running the server."
        )
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def _get(path: str, params: dict | None = None, auth: bool = True) -> dict:
    headers = _auth_headers() if auth else {"Content-Type": "application/json"}
    url = f"{BASE_URL}{path}"
    with httpx.Client(timeout=30) as client:
        resp = client.get(url, headers=headers, params=params or {})
        resp.raise_for_status()
        return resp.json()


def _post(path: str, body: dict, auth: bool = True) -> dict:
    headers = _auth_headers() if auth else {"Content-Type": "application/json"}
    url = f"{BASE_URL}{path}"
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, headers=headers, json=body)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def orita_get_event_types() -> dict:
    """
    Retrieve all event types configured for the authenticated Orita account.

    Returns a list of event types, each with an id, title, duration (minutes),
    slug, and whether it is active. Use the id when calling orita_get_slots.

    Requires ORITA_API_KEY to be set.
    """
    return _get("/api/v1/event-types")


@mcp.tool()
def orita_get_slots(event_type_id: str, date: str) -> dict:
    """
    Retrieve available booking slots for a specific event type on a given date.

    Args:
        event_type_id: The id of the event type (from orita_get_event_types).
        date: The date to check in YYYY-MM-DD format (e.g. "2025-08-15").

    Returns a list of available time slots with start and end times in ISO 8601.

    Requires ORITA_API_KEY to be set.
    """
    return _get("/api/v1/slots", params={"eventTypeId": event_type_id, "date": date})


@mcp.tool()
def orita_book_appointment(
    event_type_id: str,
    start: str,
    end: str,
    attendee_name: str,
    attendee_email: str,
    attendee_notes: str = "",
    timezone: str = "UTC",
) -> dict:
    """
    Book an appointment for a specific event type and time slot.

    Args:
        event_type_id: The id of the event type to book.
        start: ISO 8601 start datetime of the slot (e.g. "2025-08-15T10:00:00Z").
        end:   ISO 8601 end datetime of the slot   (e.g. "2025-08-15T10:30:00Z").
        attendee_name:  Full name of the person booking.
        attendee_email: Email address of the person booking.
        attendee_notes: Optional notes or reason for the meeting.
        timezone: IANA timezone string of the attendee (default: "UTC").

    Returns the created booking object including its id, confirmation code,
    and meeting link if applicable.

    Requires ORITA_API_KEY to be set.
    """
    body = {
        "eventTypeId": event_type_id,
        "start": start,
        "end": end,
        "attendee": {
            "name": attendee_name,
            "email": attendee_email,
            "notes": attendee_notes,
            "timezone": timezone,
        },
    }
    return _post("/api/v1/bookings", body)


@mcp.tool()
def orita_get_booking(booking_id: str) -> dict:
    """
    Retrieve details of an existing booking by its id.

    Args:
        booking_id: The unique identifier of the booking.

    Returns full booking details including status, attendee info, and times.

    Requires ORITA_API_KEY to be set.
    """
    return _get(f"/api/v1/bookings/{booking_id}")


@mcp.tool()
def orita_cancel_booking(booking_id: str, reason: str = "") -> dict:
    """
    Cancel an existing booking.

    Args:
        booking_id: The unique identifier of the booking to cancel.
        reason:     Optional cancellation reason to include in the notification.

    Returns the updated booking object with status set to "cancelled".

    Requires ORITA_API_KEY to be set.
    """
    body = {"reason": reason} if reason else {}
    return _post(f"/api/v1/bookings/{booking_id}/cancel", body)


@mcp.tool()
def orita_get_profile(username: str) -> dict:
    """
    Retrieve the public scheduling profile of an Orita user by their username.

    This endpoint is public — no API key is required.

    Args:
        username: The Orita username (slug) to look up (e.g. "jane-smith").

    Returns the profile including display name, bio, avatar URL, and
    the list of active event types available for public booking.
    """
    return _get("/api/v1/profile", params={"username": username}, auth=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    mcp.run()


if __name__ == "__main__":
    main()
