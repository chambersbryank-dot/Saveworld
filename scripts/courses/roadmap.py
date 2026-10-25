"""Oct 24 2026 (founder-approved): four-year aerospace/STEM self-study track on Courses.html, built one course at a time.
A course goes live when scripts/courses/<id>.py exists with the same ID and STATUS = 'live' (build-courses.py reads it);
until then its card shows 'Coming soon'. Keep entries short: title, code-style label, one line on what it covers."""
YEARS = [
 ('Year 1 · Freshman', [
  ('chem110', 'General Chemistry I + Lab', 'Atoms, reactions, bonding, gases and energy, with three labs.'),
  ('phys110', 'Physics I + Lab', 'Motion, forces, energy and momentum, with labs.'),
  ('calc1', 'Calculus I', 'Limits, derivatives and an introduction to integrals.'),
  ('calc2', 'Calculus II', 'Integration methods, sequences and series.'),
  ('aero101', 'Intro to Aerospace Engineering', 'How aircraft and spacecraft are designed, built and flown.'),
  ('cad101', 'Engineering Graphics / CAD', 'Technical drawing and 3D computer-aided design.'),
  ('prog101', 'Intro Programming', 'Writing programs to solve engineering problems.')]),
 ('Year 2 · Sophomore', [
  ('calc3', 'Calculus III', 'Multivariable calculus and vector fields.'),
  ('diffeq', 'Differential Equations', 'Modeling change: ODEs and their solutions.'),
  ('phys2', 'Physics II', 'Electricity, magnetism, waves and optics.'),
  ('statics', 'Statics', 'Forces and moments on structures at rest.'),
  ('dynamics', 'Dynamics', 'Motion of particles and rigid bodies.'),
  ('mom', 'Mechanics of Materials', 'Stress, strain and how parts bend, twist and fail.'),
  ('linalg', 'Linear Algebra', 'Vectors, matrices and systems of equations.'),
  ('circuits', 'Circuits', 'DC and AC circuit analysis.')]),
 ('Year 3 · Junior', [
  ('aero1', 'Aerodynamics I', 'Lift, drag and airflow over wings.'),
  ('thermo', 'Thermodynamics', 'Energy, entropy, cycles and engines.'),
  ('fluids', 'Fluid Mechanics', 'How liquids and gases flow.'),
  ('perf', 'Aircraft Performance', 'Range, endurance, climb and takeoff.'),
  ('struct', 'Aerospace Structures', 'Light, strong structures for flight.'),
  ('orbit', 'Orbital Mechanics', 'Orbits, transfers and mission design.'),
  ('numerics', 'Numerical Methods', 'Solving engineering math on a computer.'),
  ('probstat', 'Probability & Statistics', 'Uncertainty, data and reliability.')]),
 ('Year 4 · Senior', [
  ('prop', 'Propulsion', 'Jet engines and rockets.'),
  ('fdc', 'Flight Dynamics & Controls', 'Stability and control of aircraft and spacecraft.'),
  ('scdesign', 'Spacecraft Design', 'Subsystems, power, thermal and mission requirements.'),
  ('heat', 'Heat Transfer', 'Conduction, convection and radiation.'),
  ('avionics', 'Avionics & Systems Engineering', 'Flight electronics and managing complex systems.'),
  ('capstone', 'Capstone (aircraft or CubeSat)', 'A full design project from requirements to review.'),
  ('sustain', 'Sustainable Aviation', 'Cleaner fuels, efficient aircraft and lower emissions.')]),
]
