# TechTides Derry 2026

This is the repository for the talk slides and the demo code that I used for the *What No One Asks In the Claude Demo* talk. 

## The Files

- `README.md` This file you're reading.
- `techtides2026.pdf` The slides from the talk presented in Derry on 27th October 2026.
- `spec.md` The demo Claude spec that causes the bad code. 
- `bad_spec` This directory has the generated code that follows the spec but basically does it wrong. It's right, tests pass and the code runs, but it's wrong....
- `fixed` The corrected code, with tests.

## Executing the Code.

### The Bad Code
```
cd bad_spec

python3 -m unittests -v 
# The tests will pass....

python3 repro_launch_day.py
# Shows the output running, but 
# there's an issue, everyone got a 
# discount instead of one customer.
```

### The Good Code
```
cd fixed
python3 -m unittests -v 
# The tests will pass....

python3 repro_launch_day_fixed.py
# Look at the output this time. 
# Only one customer gets the deal. 
# The rest are rejected.
```
## Citing this work

If you use this talk, the case study or the code in your own work, please cite it. GitHub's **Cite this repository** button (right-hand sidebar) is generated from [`CITATION.cff`](CITATION.cff), or you can copy the BibTeX below.

```bibtex
@misc{bell2026techtides,
  author       = {Bell, Jason},
  title        = {{Everything They Don't Tell You in the Claude Demo}},
  year         = {2026},
  month        = oct,
  howpublished = {Conference talk and companion code, TechTides 2026},
  url          = {https://github.com/jasebell/techtides2026},
  note         = {Includes the one-time coupon redemption case study (spec, code, review, race condition, fix)}
}
```
