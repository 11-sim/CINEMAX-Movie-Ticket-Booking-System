# CINEMAX-Movie Ticket Booking System

A refined, terminal-based cinema counter simulation built using Python's built-in standard library. The application models an interactive theatre ticket booking system featuring interactive seat selection grids, independent show auditoriums, strict double-booking prevention, booking management and cancellation with refund simulation, and persistent JSON data storage.

---

## Table of Contents
- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Interactive Seating Matrix](#interactive-seating-matrix)
- [Booking and Cancellation Workflow](#booking-and-cancellation-workflow)
- [Data Persistence](#data-persistence)
- [Python Concepts Demonstrated](#python-concepts-demonstrated)
- [Technologies Used](#technologies-used)
- [How to Run the Project](#how-to-run-the-project)
- [Project Structure](#project-structure)
- [Team Members](#team-members)
- [Repository](#repository)

---

## About the Project
The Movie Ticket Booking System simulates a real-world multiplex box office counter. It allows customers to browse currently showing movies, inspect showtimes and ticket pricing, interactively choose seats on a 10×10 theatre layout, review calculated totals (including 18% GST), generate clean printable tickets, inspect booking history, and cancel reservations with simulated refunds.

The project strictly preserves:
- 4 iconic movies (*Inception*, *The Dark Knight*, *Interstellar*, *Dune*).
- Exactly 3 distinct showtimes per movie.
- 10×10 seating arrangements with row labels A–J and columns 1–10.
- Accurate 18% GST calculations.
- Beginner-friendly, procedural Python without external dependencies.

---

## Key Features

1. **Interactive 10×10 Seating Grid**
   - Clear visual representation of the cinema screen.
   - Distinct seat markers: `[O]` Available, `[X]` Booked, and `[S]` Selected.
   - Dynamic real-time highlighting of selected seats during the booking process.
   - Live availability and booking statistics displayed above and below the grid.

2. **Strict Double-Booking Prevention & Independent Auditoriums**
   - Each movie and showtime maintains an independent seating arrangement. Booking seat A1 for *Inception* at 10:00 AM does not block A1 for the 02:00 PM show.
   - Comprehensive coordinate validation (A1 to J10).
   - Rejection of duplicate seat selections in a single transaction.
   - Pre-confirmation atomic verification of seat availability before finalizing reservations.

3. **Booking Management & History**
   - Tracks unique booking IDs (`BK-XXXXX`), movie titles, showtimes, seats, ticket counts, price breakdowns, and statuses (`CONFIRMED` / `CANCELLED`).
   - Summary statistics: total bookings, active tickets, cancelled tickets, and total expenditure.
   - Individual ticket lookup by Booking ID.

4. **Booking Cancellation & Refund Simulation**
   - Allows users to cancel confirmed bookings using their Booking ID.
   - Validates booking existence and prevents double-cancellations.
   - Automatically releases seats back to the specific auditorium grid.
   - Simulates refund crediting to the original payment method.

5. **Aesthetic Terminal Interface & Main Menu**
   - Clean welcome banner and ASCII formatted tickets.
   - Central main menu allowing continuous navigation without restarting the program:
     1. View Movies
     2. Book Tickets
     3. View My Bookings
     4. Cancel Booking
     5. Exit (with confirmation prompt)

6. **Automatic JSON Data Persistence**
   - All booking records and auditorium seat grids are saved in `theatre_data.json`.
   - Data is automatically loaded upon application startup.
   - Cancelled and booked statuses persist seamlessly across program restarts.
   - Pre-booked demo seats are generated only on the very first launch and never overwrite existing saved data.

---

## Interactive Seating Matrix

The terminal interface displays a 10×10 seating matrix aligned directly under the screen:

```text
==============================================
                    SCREEN                    
----------------------------------------------
       1   2   3   4   5   6   7   8   9  10 
  A   [O] [O] [X] [O] [S] [O] [O] [O] [X] [O]
  B   [O] [X] [O] [O] [O] [O] [O] [S] [O] [O]
  C   [O] [O] [O] [X] [O] [O] [O] [O] [O] [O]
  D   [O] [O] [O] [O] [O] [O] [O] [O] [O] [O]
  E   [O] [O] [O] [O] [O] [O] [O] [O] [O] [O]
  F   [O] [O] [O] [O] [O] [O] [O] [O] [O] [O]
  G   [O] [O] [O] [O] [O] [O] [O] [O] [O] [O]
  H   [O] [O] [O] [O] [O] [O] [O] [O] [O] [O]
  I   [O] [O] [O] [O] [O] [O] [O] [O] [O] [O]
  J   [O] [O] [O] [O] [O] [O] [O] [O] [O] [O]
----------------------------------------------
Legend: [O] Available   [X] Booked   [S] Selected
Available: 95 | Booked: 3 | Selected: 2
==============================================
```

---

## Booking and Cancellation Workflow

### Booking Tickets
1. Choose **Option 2 (Book Tickets)** from the Main Menu.
2. Select a movie from the list (or enter `0` to return).
3. Select a showtime (or enter `0` to return).
4. Review the seating layout and enter the number of tickets.
5. Enter seat coordinates (e.g., `A1, A2`). Seats are highlighted on the grid with `[S]`.
6. Review the booking summary (base price, 18% GST, and total payable).
7. Confirm with `y` to finalize the reservation and print the official ticket.

### Cancelling a Booking
1. Choose **Option 4 (Cancel Booking)** from the Main Menu.
2. Enter the unique Booking ID (e.g., `BK-12345`).
3. Verify booking details and confirm cancellation with `y`.
4. The seats are immediately restored to the exact show's layout, the status is marked `CANCELLED`, and a simulated refund receipt is displayed.

---

## Data Persistence

The system utilizes Python's built-in `json` module to manage application state:
- **File**: `theatre_data.json` (created automatically in the project folder).
- **Structure**:
  - `auditoriums`: Maps each unique `movie_show` key (e.g. `"0_1"`) to its 10×10 boolean seat matrix.
  - `bookings`: Stores the list of booking dictionaries containing IDs, customer seat allocations, timestamps, financial totals, and status.
- **Resilience**: Gracefully handles missing, empty, or corrupted files by re-initializing fresh demo auditoriums without crashing.

---

## Python Concepts Demonstrated

- **Variables & Data Types**: Strings, integers, floats, booleans.
- **Data Structures**:
  - 2D Lists: Representing 10×10 seating matrices.
  - Dictionaries: Storing movie metadata, showtimes, and booking records.
  - Sets: Managing unique booking IDs and selected coordinates.
  - Tuples: Coordinate pairs `(row, col)`.
- **Functions & Modularity**: Reusable functions with clear responsibilities and docstrings.
- **Control Flow**: `while` loops for continuous menu navigation and `if/elif/else` branches.
- **Defensive Input Validation**: Validating numeric inputs, coordinates, duplicate selections, and cancellation IDs.
- **String Formatting**: Formatted strings (`f-strings`), alignment specifiers (`<`, `>`, `^`), and ASCII borders.
- **File I/O & JSON Serialization**: Reading and writing structured application state with `json.load()` and `json.dump()`.
- **Random Module**: Generating random demo bookings and booking IDs (`BK-XXXXX`).

---

## Technologies Used

- **Language**: Python 3 (Built-in Standard Library only)
- **Editor**: Visual Studio Code
- **Version Control**: Git and GitHub

---

## How to Run the Project

1. Ensure Python 3 is installed:
   ```bash
   python --version
   ```

2. Clone or open the repository folder:
   ```bash
   git clone https://github.com/11-sim/Movie-Ticket-Booking-System.git
   cd Movie-Ticket-Booking-System
   ```

3. Run the script:
   ```bash
   python "Python Project.py"
   ```

4. Follow the intuitive on-screen prompts.

---

## Project Structure

```text
Movie-Ticket-Booking-System/
│
├── Movie Ticket Booking System.py      # Main application script containing complete logic
├── README.md              # Project documentation and specifications
└── theatre_data.json      # Auto-generated persistent data store (on first run)
```

---

## Team Members

- **Member 1**: Simran Kumari - 46
- **Member 2**: Aryavrat Chakraborty - 9
- **Member 3**: Tanvi Sachin Chavan - 36

---

## Repository

https://github.com/11-sim/Movie-Ticket-Booking-System
