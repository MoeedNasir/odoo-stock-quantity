# Stock - Show Inward Quantity in Moves History

## Overview

This Odoo module customizes the **Stock Move Lines** tree view to display **only the inward (incoming) quantity** in the **Quantity** column. It ensures that aggregated quantities in grouped views reflect only incoming quantities.

- Original `quantity` values for outgoing moves remain unchanged at the record level.
- Aggregated sums in tree or pivot views are replaced with the sum of **inward quantities**.

---

## Features

- Adds a computed field `inward_quantity` on `stock.move.line` to capture only incoming stock.
- Overrides `read_group` to aggregate `inward_quantity` instead of the total `quantity`.
- Updates the stock move line tree view to include `inward_quantity` for correct group calculations.

---

## Installation

1. Copy the module folder to your Odoo `addons` directory.
2. Update the Apps list.
3. Install the module **Stock - Show Inward Quantity in Moves History**.

---

## Technical Details

### Models

- **stock.move.line**
  - `inward_quantity` (Float, stored): Computed field to store incoming quantity.
  - `_compute_inward_quantity()`: Computes the inward quantity based on source/destination locations.
  - `read_group()`: Overrides the default method to replace aggregated `quantity` with the sum of `inward_quantity`.

### Views

- Inherits `stock.view_move_line_tree` to include the `inward_quantity` field (hidden by default) for proper aggregation.

---

## Usage

- Navigate to **Inventory → Operations → Transfers → Move Lines**.
- The **Quantity** column now represents **only inward quantities** for incoming moves.
- Aggregated totals in groupings will reflect incoming quantities instead of total stock movement.

---

## Dependencies

- `stock` module (Odoo default)

---

## Version

- 1.0.0

---

## Author

- Moeed Nasir

---

## License

- LGPL-3
