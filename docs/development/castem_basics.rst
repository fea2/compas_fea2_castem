********************************************************************************
Cast3M basics
********************************************************************************

Gibiane language
=================================

**Gibiane** is the domain-specific programming language used within the French finite element code **Cast3M**, developed by the CEA (Commissariat à l'énergie atomique et aux énergies alternatives). It is designed specifically to define and control simulations in computational mechanics.

Overview
--------

Gibiane is a **object-oriented** language developped by the CEA and based on **Fortran 77** language. It allows users to:

- Define finite element models (geometry, materials, boundary conditions)
- Launch simulations
- Post-process results
- Script complex workflows through custom procedures and loops

Unlike general-purpose programming languages, Gibiane is structured around **commands** that manipulate entities like `MAILLAGE` (mesh), `CHAMP` (field), or `MODELE` (model).

Basic Syntax
------------

Gibiane syntax is unique and may feel unfamiliar at first. A typical command looks like this:

::

  MODE1 = MODE MAIL1 'MECANIQUE' 'ELASTIQUE' '3D' ;

This line creates a mechanical 3D elastic model based on the predefined mesh MAIL1 and stores it in the variable `MODE1`.

Some specificities of the language :

- Every command must be ended with a semicolon **;** mark.
- Indentation does not matter
- The dollar $ mark enables to do comments
- The input file must end with "FIN;"


Learning More
-------------

For more details, consult the official documentation:

- `Cast3M Documentation <http://www-cast3m.cea.fr>`_




