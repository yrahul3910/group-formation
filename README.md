# Group formation

This is a simple script to form groups automatically based on Google Forms responses. In summary, this should be the structure of your Google Form:

**Section 1:**

> Q1: What is your email ID? (short answer)

You can ask for any identifying ID here--these will be grouped.

> Q2: Do you want to form your own group? (multiple-choice)
> * Yes, and I have a group of 5 (or max group size) --> Go to Section 2
> * Yes, but I have a partial group --> Go to Section 3
> * No --> Submit form

**Section 2:**

> Q3: Please enter the email IDs of your group members, separated by commas (short answer)

I highly recommend you use a regex for this, or you'll get invalid submissions, whether through malice or incompetence. Here's the one I use:

```
([a-zA-Z0-9]+@ncsu.edu,\s*)+[a-zA-Z0-9]+@ncsu.edu
```

**Section 3:**

> Q4: How many group members do you have (including yourself)? (multiple-choice)
> * 2
> * 3
> * ...

> Q5: Please enter the email IDs of your group members, separated by commas. (short answer)

Again, please use a regex here.
