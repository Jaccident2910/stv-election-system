# STV Election System

This is a Single-Transferrable Vote election system built for the Jesus College Oxford JCR (https://www.jesusoxfordjcr.com/). It is built to spec with the JCR's constitution, and I built it in my capacity as the JCR IT Rep.

It is designed to be used in tandem with Microsoft Forms, as using the "In this institution" option in Microsoft Forms means every JCR member can only vote once.

It uses pandas to interpret a csv of voting results. This csv should be converted from the excel spreadsheet that Microsoft Forms builds for you.

There is also an experimental multi-seat election system built with the Droop quota and fractional transfers, but this has not been tested in any capacity and will require significant amounts of work and testing before it can be used. Fortunately, Danny Kuhrt, the 2024 Secretary of the JCR, 
made an interpretation of the constutution that said that all multi-seat races are to be run as slates, making this part of the election system redundant. I decided to create this experimental version anyway to ensure the system stands the test of time.
