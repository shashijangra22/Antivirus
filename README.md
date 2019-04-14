# Design of an antivirus system

## Part 1 (Signature based virus detection)
- Searching all the given signatures into a test file, if found writing the output to a seperate file stating which signatures has been found in given file.
    - Syntax : `sudo python3 antivirus.py -o 1 -f <filepath> `

## Part 2 (Sandbox based virus detection)
- Running the vulnerable `.jar` files inside a docker java container.
- if `cpu_usage > 80% or mem_usage > 35MB` declare it as a virus and write the output to a seperate output file
    - Syntax : `sudo python3 antivirus.py -o 2 -f <filepath>`