# MIT-depth checklist

Use this when a Saving Planets course should be comparable to an MIT OpenCourseWare course page. MIT 16.50 Introduction to Propulsion Systems (Spring 2012) is the model: https://ocw.mit.edu/courses/16-50-introduction-to-propulsion-systems-spring-2012/

A course meets the checklist when a reader can find all of these without leaving the page, except the linked sources:

1. Syllabus: what the course is, who it is for, prerequisites, and a clear line that it carries no credit and no school is involved.
2. Calendar: a week-by-week table.
3. Learning outcomes mapped to the unit that teaches them and to the practice on the page.
4. Lecture notes for each session. On this site the unit itself is the notes. Where MIT published a matching note, link that note. Do not invent a session.
5. Readings: the free public sources already used in the units, with the line that a listing is not an endorsement.
6. Problem sets with solutions. Every number is recomputed by `CHECKS()` in the course module before publish (`python3 scripts/build-courses.py --check`).
7. Exams with solutions, same check.
8. One openly licensed lecture video per unit only when a real MIT OpenCourseWare, Open Yale Courses, or Stanford Engineering Everywhere page exists and returns HTTP 200. Record it in `scripts/courses/lectures.json`. If none exists, leave the unit without a video.

## Applied November 18, 2026

- Propulsion (AERO 410) has the calendar, the outcomes map, the readings list, session links to MIT 16.50 lecture notes that were checked, problem sets with the solutions already on the page, and exams with solutions. Yale PHYS 200 Lecture 8 (momentum) and Lecture 23 (second law and Carnot) are linked on units 1 and 2. MIT 16.50 publishes notes, not lecture videos. Stanford Engineering Everywhere has no propulsion course. Units 3 through 10 have no verified open lecture video.
- The other 29 live courses already had a calendar, practice, and exams. This pass adds the outcomes map and the readings list, built from the units that were already on the page. It does not add new problem sets, new numbers, or new videos to those courses.
- Study-guide PDFs on R2 were not regenerated.

Checked sources for the Embry-Riddle comparison on Courses.html:

- https://erau.edu/academics/colleges/daytona-beach-college-of-engineering/aerospace-engineering
- https://catalog.erau.edu/programs/undergraduate/bachelors/aerospace-engineering/
