# Sum up 23 November's world news in one image

[![make.fun badge](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

Entry for the [make.fun bounty: Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123).

## The day in one image

Monday 23 November 2026 was a day of conflict at sea and in the air, stalemate in the climate talks, and milestones elsewhere: Ukrainian naval drones badly damaged the Russian corvette Merkury off Libya and hit the cargo ship MV Angara, while Iran said it shot down a US Reaper drone over the Strait of Hormuz and Indonesia seized a ship carrying 405 tonnes of rocket propellant chemical; the COP31 summit in Antalya ended with no deal on fossil fuels or finance; Democrats clinched 258 US House seats, their largest majority in over three decades; a Delta systems outage delayed more than 1,600 flights as Thanksgiving travel began and the penny's production ended; and South Korea became only the fourth economy ever to export more than $1 trillion in a year, powered by AI chip demand.

## Run

```sh
python3 draw.py        # rebuild news.png (build time only)
python3 main.py        # writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output)
```

`main.py` uses only the Python standard library: it verifies `news.png` is a real PNG, copies it to the output directory as `entry.png`, and is fully deterministic — two runs produce byte-identical output. No network, no clock, no randomness.
