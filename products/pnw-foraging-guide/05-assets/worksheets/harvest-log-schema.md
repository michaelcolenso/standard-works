# Harvest Log Schema — PNW Foraging & Mycology Field Guide + Log System
## Version 1.0 — 2026-03-02

This document is the build spec for the Harvest Log spreadsheet (Excel + Google Sheets dual format). Implement from this schema. Do not add sheets or columns not listed here without a scope decision log entry.

---

## File Delivery Format

| Format | File name | Notes |
|---|---|---|
| Excel | `PNW-Harvest-Log-v1.xlsx` | Full functionality; works offline |
| Google Sheets | Shareable template link | Copy-to-Drive model; user gets their own instance |

Both versions must be functionally identical. Build Excel first; port to Sheets.

---

## Sheet 1: Find Log
*Primary daily-use sheet. Every find gets one row.*

### Column Spec

| Col | Field | Type | Validation | Notes |
|---|---|---|---|---|
| A | Date | Date | MM/DD/YYYY | Auto-format; default to today |
| B | Species (Scientific) | Text | Dropdown from Species List (Sheet 5) | Locked dropdown; free text fallback for unlisted |
| C | Common Name | Text | Auto-populate from Col B lookup | Formula: `=IFERROR(VLOOKUP(B2,SpeciesList,2,FALSE),"")` |
| D | Location Name | Text | Free text | User-defined spot name; cross-references Sheet 2 |
| E | GPS Coordinates | Text | Decimal degrees format (e.g., 47.6062, -122.3321) | Instruction note in header cell |
| F | Elevation (ft) | Number | Integer; 0–14,000 | |
| G | Habitat Type | Text | Dropdown: Coastal / Lowland Forest / Riparian / Mountain / Subalpine / Urban Edge | |
| H | Substrate | Text | Dropdown: Soil / Decaying Wood (Hardwood) / Decaying Wood (Conifer) / Living Tree / Duff / Leaf Litter / Rock / N/A | For fungi; N/A for plants |
| I | Harvest Weight (lbs) | Number | Decimal; 0–50 | 0 = found but not harvested |
| J | Confidence Level | Number | Dropdown: 1 (Certain) / 2 (Probable) / 3 (Uncertain) | Helper text: "Level 3 = do not eat without expert confirmation" |
| K | Notes | Text | Free text | Field observations; conditions; companions |
| L | Photo Reference | Text | Free text | File name or camera roll ID (e.g., IMG_4821) |

### Sheet Setup
- Row 1: Column headers (bold, frozen)
- Row 2: Instructions row (italic, light grey fill) — delete before use or keep as example row
- Conditional formatting: Confidence Level column — Level 3 rows highlighted in yellow
- Auto-filter enabled on all columns
- No macros; formulas only

---

## Sheet 2: Spot Tracker
*One row per recurring foraging location.*

### Column Spec

| Col | Field | Type | Validation | Notes |
|---|---|---|---|---|
| A | Spot Name | Text | Free text | Must match Location Name used in Find Log (Sheet 1, Col D) |
| B | GPS Coordinates | Text | Decimal degrees | Primary waypoint for the spot |
| C | Elevation (ft) | Number | Integer | |
| D | Habitat Type | Text | Dropdown (same list as Sheet 1, Col G) | |
| E | Best Species | Text | Free text; comma-separated | "Chanterelle, Hedgehog, Matsutake" |
| F | Best Month(s) | Text | Free text | "Sept–Oct"; reference Seasonal Calendar |
| G | Peak Years | Text | Free text | Fruiting body mushrooms are weather-dependent; note banner years |
| H | Notes | Text | Free text | Access difficulty, parking, permit requirements, land type |
| I | Return Priority | Text | Dropdown: High / Medium / Low | Based on yield and access |

### Sheet Setup
- Row 1: Column headers (bold, frozen)
- Sort by Return Priority (High first) as default view
- No auto-calculate; all fields manual

---

## Sheet 3: Species Running Tally
*Auto-calculated from Find Log. Do not edit manually — this sheet reads from Sheet 1.*

### Column Spec

| Col | Field | Formula source | Notes |
|---|---|---|---|
| A | Species (Scientific) | Static list from Sheet 5 | All 50 species listed; rows with no data show zeros |
| B | Common Name | Lookup from Sheet 5 | |
| C | Total Harvest (lbs) | `=SUMIF(FindLog[Species],A2,FindLog[Harvest Weight])` | |
| D | # Finds (rows) | `=COUNTIF(FindLog[Species],A2)` | |
| E | First Find Date | `=MINIFS(FindLog[Date],FindLog[Species],A2)` | |
| F | Best Single Haul Date | `=INDEX(FindLog[Date],MATCH(MAXIFS(FindLog[Harvest Weight],FindLog[Species],A2),FindLog[Harvest Weight],0))` | Date of highest single-day harvest |
| G | Best Single Haul (lbs) | `=MAXIFS(FindLog[Harvest Weight],FindLog[Species],A2)` | |
| H | Best Location | `=INDEX(FindLog[Location Name],MATCH(MAXIFS(FindLog[Harvest Weight],FindLog[Species],A2),FindLog[Harvest Weight],0))` | Location of best single haul |

### Sheet Setup
- Protected range — user cannot edit Col B–H; formulas only
- Sorted by Total Harvest (lbs) descending by default
- Note in cell A1: "This sheet updates automatically from Find Log. Do not edit columns B–H."

---

## Sheet 4: Annual Planner
*Season overview. One column per month; rows = species + planned outings.*

### Layout

Rows:
- Row 1: Header — "Annual Planner — [YEAR]" (user edits year)
- Row 2: Month headers (Jan through Dec), columns B–M
- Rows 3–52: Species rows (all 50 species from Sheet 5, Col A)
- Row 53: Divider
- Rows 54–66: "Planned Outings" section — 13 free-form rows for user to enter outing dates and targets by month column

### Species × Month Cell Content
Each cell at the intersection of a species row and month column contains one of:
- `●` — primary season (peak fruiting or growth; best harvest window)
- `◌` — marginal season (possible but not optimal; elevation-dependent)
- *(blank)* — out of season

Pre-fill all 50 species × 12 months from Seasonal Calendar data. This sheet is static (no formulas); it is a visual reference.

### Planned Outings Rows
User enters free text in the appropriate month column. Example cell content: "Oct 5 — Spot: North Fork trailhead — Target: Matsutake, Hedgehog."

### Sheet Setup
- Columns B–M: equal width (~60px)
- Species rows: alternating white/light grey fill for readability
- Month columns: header row bold
- Freeze Row 1–2 and Column A
- Protect species × month data range (Rows 3–52, Cols B–M) — content is pre-filled reference data; user only edits Rows 54–66

---

## Sheet 5: Species List (Reference — hidden from standard view)
*Lookup table used by Sheets 1, 2, 3. Not a user-facing sheet.*

### Column Spec

| Col | Field | Notes |
|---|---|---|
| A | Species (Scientific) | All 50 species; alphabetical |
| B | Common Name | |
| C | Section | Spring / Summer / Fall / Winter-YearRound |
| D | Type | Fungus / Plant |
| E | Primary Habitat | Coastal / Lowland Forest / Riparian / Mountain / Subalpine / Urban Edge |
| F | Peak Month Start | Month number (1–12) |
| G | Peak Month End | Month number (1–12) |
| H | Toxicity Rating | Edible / Edible with prep / Avoid |

### Sheet Setup
- Sheet tab named "SpeciesList"
- Hidden from default view (right-click → Hide Sheet); accessible via sheet navigation for advanced users
- Protected; no user editing

---

## Build Notes

1. **Named ranges:** Define `FindLog` as the full data range of Sheet 1 (dynamic, expands with new rows). All Sheet 3 formulas reference this named range.
2. **Dropdown source:** All dropdowns in Sheets 1–2 draw from fixed lists defined in a hidden "Validation" sheet tab (or from Sheet 5 for species dropdown). Do not hard-code dropdown values in cells.
3. **Google Sheets port:** MINIFS and MAXIFS are available in Sheets; VLOOKUP works identically. Sheet protection via Data → Protect Sheets and Ranges.
4. **Print setup:** Sheet 1 and Sheet 2 should be print-ready at landscape A4/Letter with headers frozen on every page (Page Layout → Print Titles in Excel; File → Print Settings → Headers in Sheets).
5. **File size target:** Under 2MB for Excel; no embedded images. Sheets template should load in under 5 seconds on a standard connection.
