# University Exam Scheduling Using Constraint Satisfaction

A Python implementation of a university exam timetabling problem modeled as a **Constraint Satisfaction Problem (CSP)**. The project explores several search strategies and constraint-propagation methods for assigning courses to examination periods.

> **Academic project:** Developed for an Artificial Intelligence I course. The scheduling model and experiment driver are implemented in `timetable.py`; the supporting `csp.py`, `search.py`, and `utils.py` modules are based on educational AI search/CSP code.

## Problem formulation

Each course is a CSP variable. Its domain consists of pairs `(period, day)`, where there are **three examination periods per day** and **21 possible days**. Course properties are read from `h3-data.csv`, including semester, instructor, whether the course is considered difficult, and whether it has a laboratory component.

The model encodes restrictions such as:

- Two written exams cannot occupy the same time slot.
- Courses in the same semester cannot be examined on the same day.
- Difficult courses must be separated by at least two days.
- Courses taught by the same instructor cannot be examined on the same day.
- Laboratory exams require an additional consecutive period, with restrictions on when they can be scheduled.

## Algorithms and experiments

The program compares five configurations:

| Configuration | Variable selection | Value ordering | Inference / search |
| --- | --- | --- | --- |
| FC + MRV | Minimum Remaining Values | Least Constraining Value | Forward Checking |
| MAC + MRV | Minimum Remaining Values | Least Constraining Value | Maintaining Arc Consistency |
| FC + dom/wdeg | Custom `dom_wdeg` function | Least Constraining Value | Forward Checking |
| MAC + dom/wdeg | Custom `dom_wdeg` function | Least Constraining Value | Maintaining Arc Consistency |
| Min-Conflicts | — | — | Local search |

For each configuration, the script reports elapsed time, the number of constraint checks, and the number of variable assignments. It then prints a timetable from the final search result.

## Repository contents

```text
exam-scheduling-csp/
├── timetable.py    # Scheduling model, constraints, experiments and output
├── csp.py          # General-purpose CSP algorithms
├── search.py       # Search problem abstractions and algorithms
├── utils.py        # Shared utilities
└── h3-data.csv     # Course information
```

## Requirements

- Python 3
- `pandas`
- `sortedcontainers`

Install dependencies:

```bash
python -m pip install pandas sortedcontainers
```

## Run

From the repository root:

```bash
python timetable.py
```

Run the script from the directory containing `h3-data.csv`, because the CSV path is relative to the current working directory.

## Implementation notes

- The CSP is formulated with pairwise constraints between courses.
- The custom `dom_wdeg` selector is the implementation included in this project; it should not be assumed to match every standard weighted-degree heuristic formulation.
- The source contains a period-index check in the laboratory constraints (`b[1] == 3`) that should be reviewed before treating the schedule as fully validated.
- Runtime measurements depend on the machine, installed Python packages, and solver behavior. No benchmark results are claimed here.

## Attribution

This is a university coursework project. The exam-specific CSP model, constraints, and experiment setup are contained in `timetable.py`. The general-purpose AI/CSP modules (`csp.py`, `search.py`, `utils.py`) originate from educational search/CSP material. They are included to support the assignment and should not be presented as entirely original implementations.
