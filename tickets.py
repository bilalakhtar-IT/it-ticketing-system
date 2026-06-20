"""
IT Ticketing System
"""

import csv
import os
import datetime

# File where all tickets are saved
DATA_FILE = "data/tickets.csv"

# All possible ticket fields
FIELDNAMES = ["ticket_id", "title", "category", "priority", "status", "assignee", "created_at", "updated_at", "description", "notes"]

# Valid choices for each field
CATEGORIES = ["Hardware", "Software", "Network", "Account/Access", "Printer", "Other"]
PRIORITIES  = ["Low", "Medium", "High", "Critical"]
STATUSES    = ["Open", "In Progress", "Resolved", "Closed"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def ensure_data_file():
    """Create the CSV file with headers if it doesn't exist yet."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_tickets():
    """Read all tickets from the CSV and return them as a list of dicts."""
    ensure_data_file()
    with open(DATA_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_tickets(tickets):
    """Write the full ticket list back to the CSV file."""
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(tickets)


def next_ticket_id(tickets):
    """Auto-increment: find the highest existing ID and add 1."""
    if not tickets:
        return "TKT-001"
    ids = [int(t["ticket_id"].replace("TKT-", "")) for t in tickets]
    return f"TKT-{max(ids) + 1:03d}"


def now():
    """Return the current date/time as a readable string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def pick_from_list(prompt, options):
    """Display a numbered menu and return the user's choice."""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("  Invalid choice. Try again.")


def print_ticket(ticket):
    """Pretty-print a single ticket."""
    print("\n" + "─" * 50)
    print(f"  Ticket:      {ticket['ticket_id']}")
    print(f"  Title:       {ticket['title']}")
    print(f"  Category:    {ticket['category']}")
    print(f"  Priority:    {ticket['priority']}")
    print(f"  Status:      {ticket['status']}")
    print(f"  Assignee:    {ticket['assignee'] or 'Unassigned'}")
    print(f"  Created:     {ticket['created_at']}")
    print(f"  Updated:     {ticket['updated_at']}")
    print(f"  Description: {ticket['description']}")
    if ticket["notes"]:
        print(f"  Notes:       {ticket['notes']}")
    print("─" * 50)


# ── Core actions ─────────────────────────────────────────────────────────────

def create_ticket():
    """Walk the user through opening a new ticket."""
    print("\n── Create New Ticket ──")
    tickets = load_tickets()

    title       = input("Short title (e.g. 'Printer offline in Room 204'): ").strip()
    description = input("Full description: ").strip()
    category    = pick_from_list("Category:", CATEGORIES)
    priority    = pick_from_list("Priority:", PRIORITIES)
    assignee    = input("Assign to (name or leave blank): ").strip()

    ticket = {
        "ticket_id":   next_ticket_id(tickets),
        "title":       title,
        "category":    category,
        "priority":    priority,
        "status":      "Open",
        "assignee":    assignee,
        "created_at":  now(),
        "updated_at":  now(),
        "description": description,
        "notes":       "",
    }

    tickets.append(ticket)
    save_tickets(tickets)
    print(f"\n✓ Ticket {ticket['ticket_id']} created successfully.")


def list_tickets():
    """Display all tickets, with optional filtering."""
    tickets = load_tickets()
    if not tickets:
        print("\nNo tickets found.")
        return

    # Optional filter
    filter_status = input("\nFilter by status (or press Enter to show all): ").strip()
    if filter_status:
        tickets = [t for t in tickets if t["status"].lower() == filter_status.lower()]

    if not tickets:
        print("No tickets match that filter.")
        return

    # Summary table
    print(f"\n{'ID':<10} {'Title':<35} {'Priority':<10} {'Status':<12} {'Assignee'}")
    print("─" * 85)
    for t in tickets:
        print(f"{t['ticket_id']:<10} {t['title'][:33]:<35} {t['priority']:<10} {t['status']:<12} {t['assignee'] or '—'}")
    print(f"\n{len(tickets)} ticket(s) shown.")


def view_ticket():
    """View the full details of a single ticket."""
    ticket_id = input("\nEnter ticket ID (e.g. TKT-001): ").strip().upper()
    tickets   = load_tickets()
    matches   = [t for t in tickets if t["ticket_id"] == ticket_id]

    if not matches:
        print(f"Ticket {ticket_id} not found.")
        return

    print_ticket(matches[0])


def update_ticket():
    """Update the status, assignee, or add a note to an existing ticket."""
    ticket_id = input("\nEnter ticket ID to update: ").strip().upper()
    tickets   = load_tickets()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            print(f"\nUpdating {ticket_id}: {ticket['title']}")
            print("What would you like to update?")
            print("  1. Status")
            print("  2. Priority")
            print("  3. Assignee")
            print("  4. Add a note")
            choice = input("Choice: ").strip()

            if choice == "1":
                ticket["status"] = pick_from_list("New status:", STATUSES)
            elif choice == "2":
                ticket["priority"] = pick_from_list("New priority:", PRIORITIES)
            elif choice == "3":
                ticket["assignee"] = input("New assignee: ").strip()
            elif choice == "4":
                note = input("Note to add: ").strip()
                existing = ticket["notes"]
                ticket["notes"] = f"{existing} | {now()}: {note}" if existing else f"{now()}: {note}"
            else:
                print("Invalid choice.")
                return

            ticket["updated_at"] = now()
            save_tickets(tickets)
            print(f"✓ Ticket {ticket_id} updated.")
            return

    print(f"Ticket {ticket_id} not found.")


def close_ticket():
    """Mark a ticket as Closed."""
    ticket_id = input("\nEnter ticket ID to close: ").strip().upper()
    tickets   = load_tickets()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            ticket["status"]     = "Closed"
            ticket["updated_at"] = now()
            save_tickets(tickets)
            print(f"✓ Ticket {ticket_id} marked as Closed.")
            return

    print(f"Ticket {ticket_id} not found.")

def delete_ticket():
    """Delete a ticket from the system."""
    ticket_id = input("\nEnter ticket ID to delete: ").strip().upper()
    tickets   = load_tickets()
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            tickets.remove(ticket)
            save_tickets(tickets)
            print(f"✓ Ticket {ticket_id} deleted.")
            return
    print(f"Ticket {ticket_id} not found.")

def search_tickets():
    """Search tickets by keyword in title or description."""
    query   = input("\nSearch keyword: ").strip().lower()
    tickets = load_tickets()
    results = [t for t in tickets if query in t["title"].lower() or query in t["description"].lower()]

    if not results:
        print("No tickets match that search.")
        return

    for t in results:
        print_ticket(t)


def summary_report():
    """Print a quick stats summary of all tickets."""
    tickets = load_tickets()
    if not tickets:
        print("\nNo tickets in the system.")
        return

    total    = len(tickets)
    by_status   = {}
    by_priority = {}
    by_category = {}

    for t in tickets:
        by_status[t["status"]]     = by_status.get(t["status"], 0) + 1
        by_priority[t["priority"]] = by_priority.get(t["priority"], 0) + 1
        by_category[t["category"]] = by_category.get(t["category"], 0) + 1

    print(f"\n── Ticket Summary Report ({now()}) ──")
    print(f"\nTotal tickets: {total}")

    print("\nBy Status:")
    for k, v in sorted(by_status.items()):
        bar = "█" * v
        print(f"  {k:<15} {bar} ({v})")

    print("\nBy Priority:")
    for k, v in sorted(by_priority.items()):
        print(f"  {k:<15} {v}")

    print("\nBy Category:")
    for k, v in sorted(by_category.items()):
        print(f"  {k:<15} {v}")


# ── Main menu ─────────────────────────────────────────────────────────────────

def main():
    ensure_data_file()
    print("=" * 50)
    print("       IT Help Desk Ticketing System")
    print("=" * 50)

    menu = {
        "1": ("Create new ticket",    create_ticket),
        "2": ("List all tickets",     list_tickets),
        "3": ("View ticket details",  view_ticket),
        "4": ("Update a ticket",      update_ticket),
        "5": ("Close a ticket",       close_ticket),
        "6": ("Delete a ticket",      delete_ticket),
        "7": ("Search tickets",       search_tickets),
        "8": ("Summary report",       summary_report),
        "9": ("Exit",                 None),
    }

    while True:
        print("\n── Main Menu ──")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")

        choice = input("\nChoose an option: ").strip()

        if choice == "9":
            print("\nGoodbye!\n")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
