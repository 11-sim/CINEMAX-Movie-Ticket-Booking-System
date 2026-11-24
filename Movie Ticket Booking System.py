# Movie Ticket Booking System
"""Theatre counter simulation: shows, seat selection, and GST tickets."""
import json
import os
import random

GST_RATE = 0.18
ROWS = 10
COLS = 10
ROW_LABELS = "ABCDEFGHIJ"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theatre_data.json")

MOVIES = [
    {
        "name": "Inception",
        "shows": [
            {"time": "10:00 AM", "price": 180},
            {"time": "02:00 PM", "price": 220},
            {"time": "06:30 PM", "price": 280},
        ],
    },
    {
        "name": "The Dark Knight",
        "shows": [
            {"time": "11:15 AM", "price": 200},
            {"time": "03:00 PM", "price": 240},
            {"time": "07:45 PM", "price": 300},
        ],
    },
    {
        "name": "Interstellar",
        "shows": [
            {"time": "09:30 AM", "price": 190},
            {"time": "01:00 PM", "price": 230},
            {"time": "08:00 PM", "price": 320},
        ],
    },
    {
        "name": "Dune",
        "shows": [
            {"time": "12:00 PM", "price": 210},
            {"time": "04:30 PM", "price": 260},
            {"time": "09:15 PM", "price": 340},
        ],
    },
]


def create_seat_grid():
    """Return a 10x10 grid. False means available, True means booked."""
    return [[False for _ in range(COLS)] for _ in range(ROWS)]


def seed_booked_seats(grid):
    """Mark a random handful of seats as already sold for demonstration."""
    total = ROWS * COLS
    taken = random.randint(8, 18)
    picks = random.sample(range(total), taken)
    for index in picks:
        row, col = divmod(index, COLS)
        grid[row][col] = True


def build_auditoriums():
    """One independent seat grid per movie showtime."""
    auditoriums = {}
    for movie_index, movie in enumerate(MOVIES):
        for show_index in range(len(movie["shows"])):
            grid = create_seat_grid()
            seed_booked_seats(grid)
            auditoriums[f"{movie_index}_{show_index}"] = grid
    return auditoriums


def load_data():
    """Load saved auditoriums and bookings from JSON. Seed demo seats only if file is absent."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        auditoriums = build_auditoriums()
        bookings = []
        save_data(auditoriums, bookings)
        return auditoriums, bookings

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        auditoriums = data.get("auditoriums", {})
        bookings = data.get("bookings", [])

        # Ensure every movie show has an independent seating grid
        for movie_index, movie in enumerate(MOVIES):
            for show_index in range(len(movie["shows"])):
                key = f"{movie_index}_{show_index}"
                if key not in auditoriums:
                    grid = create_seat_grid()
                    seed_booked_seats(grid)
                    auditoriums[key] = grid

        return auditoriums, bookings
    except (json.JSONDecodeError, OSError):
        auditoriums = build_auditoriums()
        bookings = []
        save_data(auditoriums, bookings)
        return auditoriums, bookings


def save_data(auditoriums, bookings):
    """Save current auditoriums and bookings to JSON file."""
    data = {
        "auditoriums": auditoriums,
        "bookings": bookings,
    }
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=2)
    except OSError as error:
        print(f"Warning: Could not save data: {error}")


def seat_label(row, col):
    """Convert 0-indexed row and col into label like A1 or J10."""
    return f"{ROW_LABELS[row]}{col + 1}"


def parse_seat(token):
    """Turn 'A1' or 'b10' into (row, col), or None if the label is invalid."""
    text = token.strip().upper()
    if len(text) < 2 or text[0] not in ROW_LABELS:
        return None
    number = text[1:]
    if not number.isdigit():
        return None
    col = int(number)
    if col < 1 or col > COLS:
        return None
    return ROW_LABELS.index(text[0]), col - 1


def prompt_int(message, low, high):
    """Prompt user for an integer within range [low, high]."""
    while True:
        raw = input(message).strip()
        if raw.isdigit():
            value = int(raw)
            if low <= value <= high:
                return value
        print(f"Invalid input. Please enter a number between {low} and {high}.")


def confirm(message):
    """Ask user for yes/no confirmation."""
    while True:
        answer = input(message).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' for yes or 'n' for no.")


def new_booking_id(used_ids):
    """Generate a unique booking ID formatted like BK-12345."""
    while True:
        booking_id = f"BK-{random.randint(10000, 99999)}"
        if booking_id not in used_ids:
            used_ids.add(booking_id)
            return booking_id


def display_movies():
    """Display currently showing movies, showtimes, and ticket price ranges."""
    print("\n" + "=" * 56)
    print(f"{'NOW SHOWING':^56}")
    print("=" * 56)
    for index, movie in enumerate(MOVIES, start=1):
        times = ", ".join(show["time"] for show in movie["shows"])
        prices = [show["price"] for show in movie["shows"]]
        price_range = f"Rs {min(prices)} - Rs {max(prices)}"
        print(f"{index}. {movie['name']}")
        print(f"   Shows  : {times}")
        print(f"   Tickets: {price_range}")
    print("=" * 56)


def display_shows(movie):
    """Display showtimings and prices for the chosen movie."""
    print(f"\n--- Shows for {movie['name']} ---")
    for index, show in enumerate(movie["shows"], start=1):
        print(f"{index}. {show['time']:<12}  Rs {show['price']}")
    print("-" * 35)


def display_seats(grid, selected=None):
    """Display 10x10 seating matrix with screen, legend, and counts."""
    selected_set = set(selected) if selected else set()
    total_seats = ROWS * COLS
    booked_count = sum(1 for row in grid for cell in row if cell)
    available_count = total_seats - booked_count
    selected_count = len(selected_set)

    print("\n" + "=" * 46)
    print(f"{'SCREEN':^46}")
    print("-" * 46)
    header = "      " + " ".join(f"{col:^3}" for col in range(1, COLS + 1))
    print(header)
    for row in range(ROWS):
        cells = []
        for col in range(COLS):
            if (row, col) in selected_set:
                cells.append("[S]")
            elif grid[row][col]:
                cells.append("[X]")
            else:
                cells.append("[O]")
        print(f"  {ROW_LABELS[row]}   " + " ".join(cells))
    print("-" * 46)
    print("Legend: [O] Available   [X] Booked   [S] Selected")
    print(f"Available: {available_count - selected_count} | Booked: {booked_count} | Selected: {selected_count}")
    print("=" * 46)


def available_count(grid):
    """Count available seats in a 10x10 grid."""
    free = 0
    for row in grid:
        for booked in row:
            if not booked:
                free += 1
    return free


def choose_seats(grid, count):
    """
    Prompt user to select `count` seats.
    Shows current selections on grid using [S].
    Returns list of (row, col) coordinates or None if cancelled.
    """
    chosen = []
    while len(chosen) < count:
        remaining = count - len(chosen)
        if chosen:
            selected_labels = ", ".join(seat_label(r, c) for r, c in chosen)
            print(f"\nCurrently selected ({len(chosen)}/{count}): {selected_labels}")
            display_seats(grid, chosen)

        prompt = f"Select {remaining} seat(s) (e.g., A1, B2) or 'c' to cancel: "
        raw = input(prompt).strip()
        if raw.lower() in ("c", "cancel"):
            return None
        if not raw:
            continue

        tokens = [token.strip() for token in raw.split(",") if token.strip()]
        for token in tokens:
            if len(chosen) == count:
                print(f"Already selected required {count} seat(s). Extra seat '{token}' ignored.")
                break

            seat = parse_seat(token)
            if seat is None:
                print(f"Error: '{token}' is not a valid seat label. (Use row A-J and col 1-10, e.g., A1, J10)")
                continue

            row, col = seat
            label = seat_label(row, col)
            if grid[row][col]:
                print(f"Error: Seat {label} is already booked. Please choose an available seat.")
                continue

            if seat in chosen:
                print(f"Error: You have already selected seat {label} in this booking.")
                continue

            chosen.append(seat)
            print(f"Selected: {label}")

    print(f"\nAll {count} seat(s) selected: {', '.join(seat_label(r, c) for r, c in chosen)}")
    display_seats(grid, chosen)
    return chosen


def print_ticket(booking):
    """Print an aesthetically formatted movie ticket with ASCII borders."""
    line = "=" * 48
    print("\n" + line)
    print(f"{'CINEMA / THEATRE BOOKING':^48}")
    print(line)
    print(f" Booking ID     : {booking['booking_id']}")
    print(f" Booking Status : {booking.get('status', 'CONFIRMED')}")
    print(f" Movie Name     : {booking['movie_name']}")
    print(f" Showtime       : {booking['show_time']}")
    seats_str = ", ".join(booking["seats"]) if isinstance(booking["seats"], list) else str(booking["seats"])
    print(f" Selected Seats : {seats_str}")
    quantity = booking["ticket_quantity"]
    price = booking["ticket_price"]
    print(f" Ticket Quantity: {quantity} x Rs {price:.2f}")
    print("-" * 48)
    print(f" Base Amount    : Rs {booking['base_amount']:.2f}")
    print(f" GST (18%)      : Rs {booking['gst']:.2f}")
    print(f" Final Amount   : Rs {booking['final_amount']:.2f}")
    print(line)
    print(f"{'Thank you! Enjoy your movie!':^48}")
    print(line)


def book_show(auditoriums, bookings, used_ids):
    """Handle the interactive ticket booking process."""
    display_movies()
    print("Enter 0 to return to Main Menu.")
    movie_choice = prompt_int("Select a movie (1-4, or 0 to return): ", 0, len(MOVIES))
    if movie_choice == 0:
        return
    movie_index = movie_choice - 1
    movie = MOVIES[movie_index]

    display_shows(movie)
    print("Enter 0 to return to Main Menu.")
    show_choice = prompt_int("Select a showtime (1-3, or 0 to return): ", 0, len(movie["shows"]))
    if show_choice == 0:
        return
    show_index = show_choice - 1
    show = movie["shows"][show_index]

    grid_key = f"{movie_index}_{show_index}"
    grid = auditoriums[grid_key]
    free = available_count(grid)
    if free == 0:
        print("\nSorry, this show is HOUSEFULL! Please select another showtime.")
        return

    print(f"\n{movie['name']} | Show: {show['time']} | Ticket Price: Rs {show['price']}")
    display_seats(grid)
    print(f"\n{free} seat(s) currently available.")
    print("Enter 0 to return to Main Menu.")
    max_tickets = min(10, free)
    count = prompt_int(f"Number of tickets (1-{max_tickets}, or 0 to return): ", 0, max_tickets)
    if count == 0:
        return

    seats = choose_seats(grid, count)
    if seats is None:
        print("Seat selection cancelled. No seats reserved.")
        return

    labels = [seat_label(r, c) for r, c in seats]
    base_amount = show["price"] * count
    gst_amount = base_amount * GST_RATE
    final_amount = base_amount + gst_amount

    print("\n" + "-" * 48)
    print(f"{'BOOKING SUMMARY':^48}")
    print("-" * 48)
    print(f" Movie        : {movie['name']}")
    print(f" Showtime     : {show['time']}")
    print(f" Seats        : {', '.join(labels)}")
    print(f" Tickets      : {count} x Rs {show['price']:.2f}")
    print(f" Base Amount  : Rs {base_amount:.2f}")
    print(f" GST (18%)    : Rs {gst_amount:.2f}")
    print(f" Payable Total: Rs {final_amount:.2f}")
    print("-" * 48)

    if not confirm("Confirm booking? (y/n): "):
        print("Booking cancelled by user. Seats were not reserved.")
        return

    # Strictly recheck all selected seats immediately before confirming
    for row, col in seats:
        if grid[row][col]:
            print(f"Error: Seat {seat_label(row, col)} is no longer available. Booking aborted.")
            return

    # Mark seats as booked
    for row, col in seats:
        grid[row][col] = True

    booking_id = new_booking_id(used_ids)
    booking = {
        "booking_id": booking_id,
        "movie_index": movie_index,
        "show_index": show_index,
        "movie_name": movie["name"],
        "show_time": show["time"],
        "seats": labels,
        "ticket_quantity": count,
        "ticket_price": show["price"],
        "base_amount": base_amount,
        "gst": gst_amount,
        "final_amount": final_amount,
        "status": "CONFIRMED",
    }
    bookings.append(booking)
    save_data(auditoriums, bookings)

    print("\n>>> BOOKING CONFIRMED SUCCESSFULLY! <<<")
    print_ticket(booking)
    print("\nUpdated Theatre Seating Grid:")
    display_seats(grid)


def view_bookings(bookings):
    """Display booking history, summary statistics, and individual ticket details."""
    print("\n" + "=" * 72)
    print(f"{'BOOKING HISTORY':^72}")
    print("=" * 72)
    if not bookings:
        print("No bookings found in history.")
        print("=" * 72)
        return

    active_bookings = [b for b in bookings if b["status"] == "CONFIRMED"]
    cancelled_bookings = [b for b in bookings if b["status"] == "CANCELLED"]
    total_spent = sum(b["final_amount"] for b in active_bookings)

    print(f"Total Bookings: {len(bookings)} | Active: {len(active_bookings)} | Cancelled: {len(cancelled_bookings)}")
    print(f"Total Money Spent (Active): Rs {total_spent:.2f}")
    print("-" * 72)
    print(f"{'Booking ID':<10} {'Movie Name':<16} {'Showtime':<10} {'Seats':<14} {'Amount':<10} {'Status':<10}")
    print("-" * 72)
    for booking in bookings:
        seats_str = ", ".join(booking["seats"])
        if len(seats_str) > 13:
            seats_str = seats_str[:10] + "..."
        movie_title = booking["movie_name"]
        if len(movie_title) > 15:
            movie_title = movie_title[:12] + "..."
        print(
            f"{booking['booking_id']:<10} "
            f"{movie_title:<16} "
            f"{booking['show_time']:<10} "
            f"{seats_str:<14} "
            f"Rs {booking['final_amount']:<7.2f} "
            f"{booking['status']:<10}"
        )
    print("=" * 72)

    bid = input("\nEnter Booking ID to view full ticket details (or press Enter to return): ").strip().upper()
    if bid:
        match = next((b for b in bookings if b["booking_id"] == bid), None)
        if match:
            print_ticket(match)
        else:
            print(f"Error: Booking ID '{bid}' not found.")


def cancel_booking(auditoriums, bookings):
    """Handle booking cancellation, seat release, and refund simulation."""
    print("\n" + "=" * 50)
    print(f"{'CANCEL BOOKING':^50}")
    print("=" * 50)
    if not bookings:
        print("No bookings available to cancel.")
        return

    bid = input("Enter Booking ID to cancel (or press Enter to return): ").strip().upper()
    if not bid:
        return

    booking = next((b for b in bookings if b["booking_id"] == bid), None)
    if not booking:
        print(f"Error: Booking ID '{bid}' not found.")
        return

    if booking["status"] == "CANCELLED":
        print(f"Error: Booking '{bid}' is already cancelled.")
        return

    print("\nBooking Details Found:")
    print(f"  Movie       : {booking['movie_name']}")
    print(f"  Showtime    : {booking['show_time']}")
    print(f"  Seats       : {', '.join(booking['seats'])}")
    print(f"  Total Paid  : Rs {booking['final_amount']:.2f}")
    print(f"  Refund Due  : Rs {booking['final_amount']:.2f}")

    if not confirm("\nAre you sure you want to cancel this booking? (y/n): "):
        print("Cancellation aborted. Booking remains confirmed.")
        return

    # Release seats in the specific auditorium showtime
    grid_key = f"{booking['movie_index']}_{booking['show_index']}"
    if grid_key in auditoriums:
        grid = auditoriums[grid_key]
        for label in booking["seats"]:
            parsed = parse_seat(label)
            if parsed:
                row, col = parsed
                grid[row][col] = False

    booking["status"] = "CANCELLED"
    save_data(auditoriums, bookings)

    print("\n" + "=" * 50)
    print(f"{'CANCELLATION CONFIRMED':^50}")
    print("=" * 50)
    print(f"Booking ID     : {booking['booking_id']}")
    print(f"Movie          : {booking['movie_name']} ({booking['show_time']})")
    print(f"Released Seats : {', '.join(booking['seats'])}")
    print(f"Refund Amount  : Rs {booking['final_amount']:.2f}")
    print("Booking Status : CANCELLED")
    print("Simulated refund processed successfully to original payment method.")
    print("=" * 50)


def print_banner():
    """Display attractive welcome banner."""
    print("=" * 56)
    print(f"{'CINEMAX THEATRE BOOKING SYSTEM':^56}")
    print(f"{'Experience Movies Like Never Before':^56}")
    print("=" * 56)


def main():
    """Main program loop and menu navigation."""
    print_banner()
    auditoriums, bookings = load_data()
    used_ids = {b["booking_id"] for b in bookings}

    while True:
        print("\n" + "=" * 44)
        print(f"{'MAIN MENU':^44}")
        print("=" * 44)
        print("  1. View Movies")
        print("  2. Book Tickets")
        print("  3. View My Bookings")
        print("  4. Cancel Booking")
        print("  5. Exit")
        print("=" * 44)

        choice = prompt_int("Enter your choice (1-5): ", 1, 5)

        if choice == 1:
            display_movies()
        elif choice == 2:
            book_show(auditoriums, bookings, used_ids)
        elif choice == 3:
            view_bookings(bookings)
        elif choice == 4:
            cancel_booking(auditoriums, bookings)
        elif choice == 5:
            if confirm("\nAre you sure you want to exit? (y/n): "):
                print("\nThank you for choosing Cinemax! Have a great day.\n")
                break


if __name__ == "__main__":
    main()