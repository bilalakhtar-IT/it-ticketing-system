# IT Ticketing System

This is a simple help desk ticketing app I built using Python. It runs right in the terminal, no database, no setup headaches, just a CSV file storing everything behind the scenes.

I built this to get hands on practice with the kind of ticket tracking I'd actually be doing in a help desk or IT support role. Instead of just reading about how ticketing systems work, I wanted to build one myself so I understood the logic behind tools like Jira Service Desk or Freshdesk from the ground up.

## Purpose

- Create a new ticket (title, description, category, priority, who it's assigned to)
- List all tickets, with the option to filter by status
- Look up the full details of one ticket
- Update a ticket's status, priority, assignee, or add a note to it
- Close a ticket
- Search tickets by keyword
- Pull a quick summary report (how many tickets are open, by priority, by category, etc.)

Every ticket gets its own ID automatically (TKT-001, TKT-002, and so on).

## How it's built

Strictly Python, no extra libraries needed. It uses the built-in `csv` module to read and write tickets to a file, and `datetime` to timestamp everything. All the data lives in `data/tickets.csv`, so you can open it in Excel anytime and see exactly what the program is storing.

## Project files

```
it-ticketing-system/
├── tickets.py          → all the code lives here
├── data/
│   └── tickets.csv     → where tickets get saved
├── requirements.txt
├── .gitignore
└── README.md

```

## How to run it

You'll need Python installed. Then:

```bash
git clone https://github.com/YOUR-USERNAME/it-ticketing-system.git
cd it-ticketing-system
python tickets.py

```

That's it, no installs needed. You'll see a menu pop up in the terminal.

## What using it looks like

When you run it, you get a menu like this:

```
── Main Menu ──
  1. Create new ticket
  2. List all tickets
  3. View ticket details
  4. Update a ticket
  5. Close a ticket
  9. Delete a ticket
  6. Search tickets
  7. Summary report
  8. Exit

```

Creating a ticket walks you through a few quick questions:

```
Choose an option: 1

Short title: Printer offline in Room 204
Full description: HP LaserJet not responding to any print jobs
Category: 5 (Printer)
Priority: 3 (High)
Assign to: Bilal A.

✓ Ticket TKT-006 created successfully.

```

And the summary report gives you a quick snapshot:

```
Total tickets: 5

By Status:
  Open            ██ (2)
  In Progress     █ (1)
  Resolved        █ (1)
  Closed          █ (1)

```

## Why I built it this way

I wanted the data to be something I could actually look at and understand, which is why I used a plain CSV file instead of a real database. It also means I can pop it open in Excel and manually check that everything's saving correctly, which was a good way to test the script as I built it.

## About me

I'm Bilal Akhtar, a Computer Systems Technology student at George Brown College, currently building out my portfolio while job hunting for entry level IT roles in the Toronto area. This project came out of wanting practical, hands on experience with the kind of tools and workflows I'd be using day to day in a help desk job.